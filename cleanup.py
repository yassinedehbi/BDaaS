'''
Created on 21 sept. 2020

@author: hagimont
'''

import boto3
from botocore.exceptions import ClientError
import time


def cleanDC():


    my_session = boto3.session.Session(
        aws_access_key_id='AKIAW35MWGYYFCZDFBZV',
        aws_secret_access_key= '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',
        region_name='us-east-1')


    ####  INSTANCES
    clientec2 = my_session.client('ec2')
    response = clientec2.describe_instances()
    liste = []
    for r in response['Reservations']:
        for i in r['Instances']:
            liste.append(i['InstanceId'])
            print('INSTANCE:' + i['InstanceId'])
    try:
        if liste:
            clientec2.terminate_instances(InstanceIds=liste)
    except Exception as e:
        print("pb with terminate_instances")
        print(e)







