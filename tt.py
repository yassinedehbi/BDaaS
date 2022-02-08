import os
import confmaster
import paramiko
from applescript import tell
ipaa = ['184.72.194.189', '54.172.78.84', '52.87.237.194']
def setslaves(ipslaves):
    os.system("rm /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves")
    os.system("touch /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves")
    for ipp in ipslaves:
        cmmd = "echo " + ipp + " >> /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves"
        os.system(cmmd)

#setslaves(ipaa)
#confmaster.config(ipaa[0], ipaa[1:],ipaa[0])


def execute_command_with_ssh( user_name, publicIp, cmd):

    try:
        bash_script = open(cmd).read()
    except FileNotFoundError:
        bash_script = cmd
    key = paramiko.RSAKey.from_private_key_file('Name.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(publicIp, port=22, username=user_name, pkey=key)
    stdin, stdout, stderr = ssh.exec_command(bash_script)
    output = stdout.readlines()
    print(output)
    ssh.close()
    #rint(output[-1])
    #return output[-1]

for ipp in ipaa:
    os.system("scp -o StrictHostKeyChecking=no -i Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/.bashrc ubuntu@" + ipp + ":/home/ubuntu/")
    execute_command_with_ssh('ubuntu',publicIp=ipp,cmd='sh confmaster.sh')