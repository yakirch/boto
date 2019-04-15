#!/usr/bin/env python3
import boto3

ec2 = boto3.client('ec2', region_name="us-east-1")
ec2.create_vpc(CidrBlock="10.24.0.0/16")
