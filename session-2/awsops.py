#!/usr/bin/env python3

import boto3
import logging
from botocore.exceptions import ClientError
import config

class AwsOperations():
    def __init__(self, args):
        """
         initiate ec2 object for creating resources
         """
        self.region = args.region
        self.vpcid = args.vpcid
        if args.internetgw:
            self.internetgw = args.internetgw
        if args.natgw:
            self.natgw = args.natgw
        if args.az:
            self.availability_zone = args.az
        self.ec2 = boto3.client('ec2', self.region)
        # self.ec2 = boto3.client('ec2', region_name=region,
        #                         aws_access_key_id=config.ACCESS_KEY,
        #                         aws_secret_access_key=config.SECRET_KEY)

    def allocate_address(self):
        """
        Allocate elastic IP address and return the response
        :return: String of the allocatedID of the elastic IP
        """

        try:
            response = self.ec2.allocate_address(Domain='vpc')
            return response['AllocationId']
        except ClientError as error:
            logging.error(error)


    def create_nat_gateway(self, subnet_id, eip):
        """ Get subnet id, elastic ip and creates a
            Nat gateway in the subnet id, using the
            elastic ip given
        """
        response = self.ec2.create_nat_gateway(
            AllocationId=eip,
            SubnetId=subnet_id
        )
        return response['NatGateway']['NatGatewayId']


    def wait_for_nat_gateway(self, nat_gateway_id):
        """ Use waiter method to wait till the nat gateway is ready """
        waiter = self.ec2.get_waiter('nat_gateway_available')
        print("Starting wait loop till Nat Gateway is available")
        waiter.wait(
            NatGatewayIds=[
                nat_gateway_id,
            ],
            WaiterConfig={
                'Delay': 20,
                'MaxAttempts': 15
            }
        )


    def create_subnet(self, cidr):
        """  Get availability zone, cidr and vpc id
             create a subnet and return its description
        """
        response = self.ec2.create_subnet(
            AvailabilityZone=self.availability_zone,
            CidrBlock=cidr,
            VpcId=self.vpcid
        )
        return response['Subnet']['SubnetId']


    def create_route_table(self):
        """ Get a vpc id and create a route table, return it's description"""
        response = self.ec2.create_route_table(
            VpcId=self.vpcid
        )
        return response['RouteTable']['RouteTableId']


    def add_nat_gateway_route(self, route_table_id, destination, nat_gateway_id):
        """ Gets route table id, destination(default gateway in our case)
            and nat gateway id and create a default gateway route in the
            given route table, return the response
        """
        response = self.ec2.create_route(
            DestinationCidrBlock=destination,
            RouteTableId=route_table_id,
            NatGatewayId=self.natgw
        )
        return response


    def add_internet_gateway_route(self, route_table_id, destination):
        """ Gets route table id, destination and internet gateway id
            and add a default gateway to the internet gateway in the route table
            return the response
        """
        response = self.ec2.create_route(
            DestinationCidrBlock=destination,
            RouteTableId=route_table_id,
            GatewayId=self.internetgw
        )
        return response


    def create_tags(self, resource_id, value):
        """ Get id and create tags for the resource """
        response = self.ec2.create_tags(
            Resources=[
                resource_id,
            ],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': value
                },
            ]
        )
        return response


    def associate_route_table(self, route_table_id, subnet_id):
        """ Gets route table id and subnet id and associate the route table
            to the subnet
        """
        response = self.ec2.associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id
        )
        return response


    def get_subnet_id(self, subnet_tag):
        dfilter = {'Name': 'tag:Name','Values': [subnet_tag]}
        response = self.ec2.describe_subnets(Filters=[dfilter])
        return response['Subnets'][0]['SubnetId']