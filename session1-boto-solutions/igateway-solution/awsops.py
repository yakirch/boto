#!/usr/bin/env python3

import config
import boto3



class awsOperations():


    def __init__(self, region):
        self.ec2 = boto3.client('ec2', region_name=config.REGION)

    def describe_vpcs(self):
        """ Return description of all vpcs in region """
        print ("Return description of all vpcs in region")
        all_vpcs = self.ec2.describe_vpcs()
        return all_vpcs

    def create_internet_gateway(self):
        """ Return description of created internet gateway """
        print("create_internet_gateway")
        response = self.ec2.create_internet_gateway(
            DryRun=False
        )
        return response


    def create_dhcp_options(self):
        """ Return description of created dhcp options """
        print ("create_dhcp_options")
        response = self.ec2.create_dhcp_options(
            DhcpConfigurations=config.DHCP_CONFIGURATION
        )
        return response


    def attach_internet_gateway(self, vpc_id, igw_id):
        """ Attach a given igw to a given vpc """
        print("attach_internet_gateway")
        self.ec2.attach_internet_gateway(
            DryRun=False,
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )

    def associate_dhcp_options(self, vpc_id, dhcp_options_id):
        """ Associate a given dhcp_options to a given vpc """
        response = self.ec2.associate_dhcp_options(
            DryRun=True,
            DhcpOptionsId=dhcp_options_id,
            VpcId=vpc_id,
        )
        return response

