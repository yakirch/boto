#!/usr/bin/env python3
"""creating VPC and resources"""

import boto3
import config

class AwsOperation():

    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name=config.REGION)
        #self.ec2 = boto3.client('ec2', region_name=config.REGION,
        #                        aws_access_key_id=config.SCCESS_KEY,
        #                        aws_secret_access_key=config.SECRET_KEY)


    def create_vpc(self):
        """
        create vpc
        :return: None
        """
        self.ec2.create_vpc(CidrBlock=config.CIDR, InstanceTenancy=config.TENANCY)
