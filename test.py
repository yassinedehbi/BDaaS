import mapp
import os
import cleanup
cleanup.cleanDC()
#app = mapp.Mapp(jarfile='/Users/yassinedehbi/PycharmProjects/bdaas/saves/wc.jar', datasamples='/Users/yassinedehbi/PycharmProjects/bdaas/saves/filesample.txt',appname='zeb.WordCount', nslaves=2)
#app.lunch()
#ipa = ['54.209.7.110', '3.88.252.12', '3.84.235.214']
def edit_ssh_conf(ipslaves, ipmaster):
    f = open("/Users/yassinedehbi/PycharmProjects/bdaas/config", "w")
    for ipp in ipslaves:
        f.write("Host " + ipp + "\n")

        f.write( " \t\tIdentityFile /home/ubuntu/Name.pem\n")

#edit_ssh_conf(ipa[1:], ipa[0])
