"""
This is doc string
"""
#!/usr/bin/python

#import json
#import argparse
import boto3




def describe_azs():
    "describing availailty zone"
    response = EC2.describe_availability_zones()
    return response



if __name__ == '__main__':
    EC2 = boto3.client('ec2', "us-east-1")
    #main_response = describe_azs()
    MAIN_RESPONSE = describe_azs()
    print(MAIN_RESPONSE)
