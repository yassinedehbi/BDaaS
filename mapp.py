import boto3
import paramiko
import time
import os
import xml.etree.ElementTree as ET
from requests import get
from joblib import Parallel, delayed
import confmaster
import socket

ACCESS_KEY = 'AKIAW35MWGYYKSAIROO5'
SECRET_KEY = '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'
REGION = 'us-east-1'
print("-------------------------")
print(ACCESS_KEY)
print(SECRET_KEY)
print(REGION)
print("-------------------------")
resource = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)


class Mapp:

    def __init__(self, jarfile:str, datasamples:str, nslaves:int, appname:str):
        self.jarfile = jarfile
        self.datasamples = datasamples
        self.nslaves = nslaves
        self.appname = appname

    def createKeyPairFile(self):
        outfile = open('Name.pem', 'w')
        key_pair = client.delete_key_pair(KeyName='Name')
        key_pair = client.create_key_pair(KeyName='Name')
        outfile.write((key_pair["KeyMaterial"]))
        outfile.close

    def createSecurityGroup(self):
        response = client.create_security_group(
            GroupName="group",
            Description="groupe description",
            VpcId='vpc-01dfa578a2d2d53f3'
        )
        gid = response['GroupId']
        client.authorize_security_group_ingress(
            GroupId=gid,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 9000,
                    'ToPort': 9000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

    def getIps(self):
        filters = [
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
        instances = resource.instances.filter(Filters=filters)

        ips = []
        for instance in instances:
            ips.append(instance.public_ip_address)
        return ips

    def createInstances(self):
        # create a new EC2 instance
        resource.create_instances(
            ImageId='ami-04505e74c0741db8d',
            MinCount=1,
            MaxCount=self.nslaves + 1,
            InstanceType='t2.micro',
            KeyName='Name',
            SecurityGroups=['group']
        )

    def execute_command(self, user_name, publicIp, cmd):
        os.system("chmod 400 /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem")
        try:
            bash_script = open(cmd).read()
        except FileNotFoundError:
            bash_script = cmd
        key = paramiko.RSAKey.from_private_key_file('/Users/yassinedehbi/PycharmProjects/bdaas/Name.pem')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(publicIp, port=22, username=user_name, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(bash_script)
        output = stdout.readlines()
        print(output)
        ssh.close()


    def setslaves(self, ipslaves):
        os.system("rm /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves")
        os.system("touch /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves")
        for ipp in ipslaves:
            cmmd = "echo " + ipp + " >> /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves"
            os.system(cmmd)

    def edit_ssh_conf(self,ips):
        f = open("/Users/yassinedehbi/PycharmProjects/bdaas/config", "w")
        f.write("Host 0.0.0.0" + "\n")
        f.write(" \t\tIdentityFile /home/ubuntu/Name.pem\n")
        f.write(" \t\tStrictHostKeyChecking no\n")
        f.write("Host localhost" + "\n")
        f.write(" \t\tIdentityFile /home/ubuntu/Name.pem\n")
        f.write(" \t\tStrictHostKeyChecking no\n")
        for ipp in ips:
            f.write("Host " + ipp + "\n")

            f.write(" \t\tIdentityFile /home/ubuntu/Name.pem\n")
            f.write(" \t\tStrictHostKeyChecking no\n")

    def lunch(self):
        #self.createKeyPairFile()
        #self.createSecurityGroup()
        self.createInstances()
        print("created")
        time.sleep(90)
        print("11")
        ipa = self.getIps()
        masterPublicIp = ipa[0]
        slavesips = ipa[1:]
        print(ipa)
        self.setslaves(slavesips)
        cmmmd = "sed -i -e s/export MASTERIP=.*/export MASTERIP=" + masterPublicIp + "/g /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/.bashrc"
        os.system(cmmmd)
        cmmmd = "sed -i -e s/export JARFILE=.*/export JARFILE=" + self.jarfile + "/g /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/.bashrc"
        os.system(cmmmd)
        cmmmd = "sed -i -e s/export APPNOM=.*/export APPNOM=" + self.appname + "/g /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/.bashrc"
        os.system(cmmmd)
        os.system("chmod 400 /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem")
        Parallel(n_jobs=len(ipa))(delayed(confmaster.config)(masterPublicIp, slavesips, ipp, self.jarfile, self.datasamples) for ipp in ipa)
        #for ipp in ipa:
        #    confmaster.config(masterPublicIp, slavesips, ipp, self.jarfile, self.datasamples)
        self.edit_ssh_conf(ips=ipa)
        for ipp in ipa:
            os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/config ubuntu@" + ipp + ":/home/ubuntu/.ssh/")

        os.system("scp -o StrictHostKeyChecking=no -i Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/ressources/lancer.sh ubuntu@" + masterPublicIp + ":/home/ubuntu/")
        self.execute_command_with_ssh('ubuntu', masterPublicIp, 'sh lancer.sh')
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        cmmd = "scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem ubuntu@" + masterPublicIp + ":/home/ubuntu/result.tar.gz yassinedehbi@" + local_ip +"://Users/yassinedehbi/PycharmProjects/bdaas/output"
        os.system("cmmd ")
        while(1):
            pass
