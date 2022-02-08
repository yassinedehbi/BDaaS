import time

import paramiko
import xml.etree.ElementTree as ET
import os

def execute_command(user_name, publicIp, cmd):
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
    #time.sleep(20)
    ssh.close()




def parsee(file,  value):
    xmlTree = ET.parse(file)
    rootElement = xmlTree.getroot()
    for element in rootElement.find('property'):
        # Find the book that has title as 'filed'
        if element.find('name'):
            # Change the value
            element.find('value').text = value
    # Write the modified xml file.
    xmlTree.write(file, encoding='UTF-8', xml_declaration=True)

def doo(ipmaster):

    root = ET.Element("configuration")
    doc = ET.SubElement(root, "property")

    ET.SubElement(doc, "name" ).text = "fs.default.name"
    ET.SubElement(doc, "value").text = "hdfs://"+ ipmaster+":9000"
    doc2 = ET.SubElement(root, "property")

    ET.SubElement(doc2, "name").text = "hadoop.tmp.dir"
    ET.SubElement(doc2, "value").text = "/tmp/hadoop"

    tree = ET.ElementTree(root)
    tree.write("/Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/core-site.xml",encoding='utf-8')

def edit_ssh_conf(ips):
    f = open("/Users/yassinedehbi/PycharmProjects/bdaas/config", "w")
    for ipp in ips:
        f.write("Host " + ipp + "\n")

        f.write(" \t\tIdentityFile /home/ubuntu/Name.pem\n")
        os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/config ubuntu@" + ipp + ":/home/ubuntu/.ssh/")
def config(ipmaster, ipslaves, ipdest, jarfile, datasamples):
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem ubuntu@" + ipdest + ":/home/ubuntu/")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/ressources/confmaster.sh ubuntu@" + ipdest + ":/home/ubuntu/")

    execute_command('ubuntu', publicIp=ipdest, cmd='sh confmaster.sh')
    print("configured")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/.bashrc ubuntu@" + ipdest + ":/home/ubuntu/")

    execute_command('ubuntu', publicIp=ipdest, cmd='source .bashrc')

    #final_output = execute_command_with_ssh("ubuntu", ipdest, '/Users/yassinedehbi/PycharmProjects/bdaas/ressources/confmaster.sh')

    #hdfs-site.xml
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/hdfs-site.xml ubuntu@" + ipdest + ":/home/ubuntu/hadoop-2.7.1/etc/hadoop/")
    print("hdfs modified")
    #slaves
    #setslaves(ipslaves)
        #hadoop
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves ubuntu@" + ipdest + ":/home/ubuntu/hadoop-2.7.1/etc/hadoop/")
         #spark
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves ubuntu@" + ipdest + ":/home/ubuntu/spark-2.4.3-bin-hadoop2.7/conf/")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/hadoop-env.sh ubuntu@" + ipdest + ":/home/ubuntu/hadoop-2.7.1/etc/hadoop/")

    #spark-env.sh
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/slaves ubuntu@" + ipdest + ":/home/ubuntu/spark-2.4.3-bin-hadoop2.7/conf/")
    cmmmd = "sed -i -e s/SPARK_MASTER_HOST=.*/SPARK_MASTER_HOST=" + ipmaster + "/g /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/spark-env.sh"
    os.system(cmmmd)
    #os.system("echo ")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem  /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/spark-env.sh ubuntu@" + ipdest + ":/home/ubuntu/spark-2.4.3-bin-hadoop2.7/conf/")

        #core-site.xmlpwd

    doo(ipmaster)
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/core-site.xml ubuntu@" + ipdest + ":/home/ubuntu/hadoop-2.7.1/etc/hadoop/")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem " + jarfile + " ubuntu@" + ipdest + ":/home/ubuntu/")
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem " + datasamples + " ubuntu@" + ipdest + ":/home/ubuntu/")
    #edit_ssh_conf(ips=ipa)
    os.system("scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/.profile ubuntu@" + ipdest + ":/home/ubuntu/")


# scp -o StrictHostKeyChecking=no -i /Users/yassinedehbi/PycharmProjects/bdaas/Name.pem /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/spark-env.sh ubuntu@52.6.5.187:/home/ubuntu/spark-2.4.3-bin-hadoop2.7/conf/
#   sed -i -e s/SPARK_MASTER_HOST=.*/SPARK_MASTER_HOST=54.159.132.68/g /Users/yassinedehbi/PycharmProjects/bdaas/configsmaster/spark-env.sh