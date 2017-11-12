#!/usr/bin/python

import boto3 #Calling Boto3 library

ec2 = boto3.resource('ec2', region_name='ap-southeast-2')
sgs = ec2.security_groups.all() # Fetching all security groups in AWS account

all_sgs = set([sg.group_name for sg in sgs]) # Creating a list of only security group names


instances = ec2.instances.all() # Getting all instances in AWS account

inssgs = set([sg['GroupName'] for ins in instances for sg in ins.security_groups]) # Getting all security groups attached to any instances


unused_sgs = all_sgs - inssgs # Removing duplicate SGs

for sg in unused_sgs:
  print(sg)
