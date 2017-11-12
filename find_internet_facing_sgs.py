#!/usr/bin/python
import boto3
ec2 = boto3.resource('ec2', region_name='ap-southeast-2')
sgs = ec2.security_groups.all()
security_groups = [sg.id for sg in sgs]
for security_group in security_groups:
    sg = ec2.SecurityGroup(security_group)
    for i in range(len(sg.ip_permissions)):
        for j in range(len(sg.ip_permissions[i]['IpRanges'])):
            if "0.0.0.0/0" in sg.ip_permissions[i]['IpRanges'][j]['CidrIp']:
                print(sg.group_name, sg.ip_permissions[i]['ToPort'], sg.ip_permissions[i]['IpRanges'][j]['CidrIp'])