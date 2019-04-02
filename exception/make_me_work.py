#!/usr/bin/python3

import argparse
import boto3


def args_parser():
    """ validate arguments and return them """
    parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
    parser.add_argument("--region", "-r", help="Get region",
                        required=True)
    parser.add_argument("--vpcid", "-i", help="Get vpc id",
                        required=True)
    return parser.parse_args()


def create_tags(vpc_id):
    ec2.create_tags(
        Resources=[
            vpc_id,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'opsschool'
            },
        ]
    )

def main():
    args = args_parser()
    ec2 = boto3.client('ec2', args.vpcid)
    create_tags(args.vpcid)

if __name__ == '__main__':
    if __name__ == '__main__':
        main()