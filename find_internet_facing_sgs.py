#!/usr/bin/python
import boto3 # import boto3 library 

ec2 = boto3.resource('ec2', region_name='ap-southeast-2') # Initialize ec2 object 

sgs = ec2.security_groups.all() # Fetching all security groups from account

security_groups = [sg.id for sg in sgs] # Capturing all security groups in a list to avoid calling again and again

for security_group in security_groups: # Initialize for loop to go inside each security group to capture details
    sg = ec2.SecurityGroup(security_group) # Capture individual security group details
    for i in range(len(sg.ip_permissions)): # Capturing ingress rules only
        for j in range(len(sg.ip_permissions[i]['IpRanges'])): # Initializing nested loop to iterate over rules inside a security group
            if "0.0.0.0/0" in sg.ip_permissions[i]['IpRanges'][j]['CidrIp']:
                print(sg.group_name, sg.ip_permissions[i]['ToPort'], sg.ip_permissions[i]['IpRanges'][j]['CidrIp'])
