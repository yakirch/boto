#!/usr/bin/python
""" Create VPC """
import argparse
import boto3


def create_vpc(cidr, tenancy):
    """ Return VPC description after creation """
    response = EC2.create_vpc(CidrBlock=cidr, InstanceTenancy=tenancy)
    return response


def args_parser():
    """ validate arguments and return them """
    parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
    parser.add_argument("--region", "-r", help="Get target region",
                        required=True)
    parser.add_argument("--cidr", "-c", help="Get vpc cidr",
                        required=True)
    parser.add_argument("--tenancy", "-t", help="Get vpc default tenancy",
                        choices=["default", "dedicated", "host"],
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = args_parser()
    CIDR = ARGS.cidr
    EC2 = boto3.client('ec2', ARGS.region)
    EC2_RESOURCE = boto3.resource('ec2', ARGS.region)
    VPC_RESPONSE = create_vpc(ARGS.cidr, ARGS.tenancy)
    VPC_ID = VPC_RESPONSE['Vpc']['VpcId']
    VPC = EC2_RESOURCE.Vpc(VPC_ID)
    VPC.wait_until_exists()
    TAGS_RESPONSE = VPC.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'opsschool-1'
            },
        ]
    )
    print(TAGS_RESPONSE)
