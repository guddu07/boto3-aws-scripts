#!/usr/bin/python
import boto3
import subprocess
import re
def lambda_handler(event, context):
  elb = boto3.client('elb')
  buk = boto3.resource('s3')
  elbs = elb.describe_load_balancers() # Getting all load balancers
  f1 = open('/tmp/elbs.html', 'w') # Making file empty for reuse
  f1.close()
  with open('/tmp/elbs.html', 'ab') as f: 
  
  # Initializing HTML injection
    f.write((""" <!DOCTYPE html>
		<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
               		<title> ELB Status </title>
               		<link rel="stylesheet" type="text/css" href="<<< css_file_s3_url >>>">
		</head>
		<body>
		<table>
			<tr>
   			  <th>ELB Name</th>
			    <th>ELB DNS </th>
    		  <th>Status</th>
  			</tr>
			""").encode())
    f.write(("<h1>ELB Status</h1><br />").encode())
    for i in range(len(elbs)): # Looping over each ELB to get the status details
      elb_dns = elbs.get('LoadBalancerDescriptions')[i]['DNSName']
      elb_name = elbs.get('LoadBalancerDescriptions')[i]['LoadBalancerName']
      status = subprocess.Popen(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', elb_dns], stdout=subprocess.PIPE) # Curl request to get ELB status by requesting its http_code
      final_status = re.sub('"', '', str(status.communicate()[0], 'utf-8')) # Replacing unwanted characters by using popular re.sub
      if final_status == "200":
        final_status_name = "Up"
        f.write(("<tr><td>"+elb_name+"</td> <td style='color:green;'>"+final_status_name+"</td></tr>").encode())
      else:
        final_status_name = "Down"
        f.write(("<tr><td>"+elb_name+"</td><td>"+elb_dns+"</td> <td style='color:red;'>"+final_status_name+"</td></tr>").encode())
    f.write(("""</table></body></html>""").encode())
  buk.Object('<<<s3_bucket_name>>>', 'elb.html').put(ACL='public-read', ContentType='text/html', Body=open('/tmp/elbs.html', 'rb')) # Pushing above temporary file to S3 bucket
