#!/usr/bin/python

import json
import argparse
import boto3


def describeAZS():
    response = ec2.describe_availability_zones()
    return(response)



if __name__ == '__main__':
    ec2 = boto3.client('ec2', "us-east-1")
    response = describeAZS()
    print(response)
