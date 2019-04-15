#!/usr/bin/python3
"""
Create Internet gateway, Dhcp options and attach to a vpc
"""

import argparse
import awsops

def select_vpc(vpc_ids):
    """
    Selected a vpc id chosen by user
    :param vpc_ids: [String] of vpcids
    :return: String id of the vpc selected
    """
    print("Select vpc to act on:")
    for vpc_id in vpc_ids:
        print(vpc_id)
    id_selected = input("Enter id: ")
    return id_selected


def args_parser():
    """ validate arguments and return them """
    parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
    parser.add_argument("--region", "-r", help="Get target region",
                        required=True)
    return parser.parse_args()


def main():
    args = args_parser()
    vpc_ids = []
    aws = awsops.awsOperations(args.region)
    respone_vpcs = aws.describe_vpcs()
    for vpc in respone_vpcs['Vpcs']:
        vpc_ids.append(vpc['VpcId'])
    vpc_id = select_vpc(vpc_ids)
    response_igw = aws.create_internet_gateway()
    igw_id = response_igw['InternetGateway']['InternetGatewayId']
    aws.attach_internet_gateway(vpc_id, igw_id)
    response_create_dhcp_options = aws.create_dhcp_options()
    dhcp_options_id = response_create_dhcp_options['DhcpOptions']['DhcpOptionsId']
    aws.associate_dhcp_options(vpc_id, dhcp_options_id)


if __name__ == '__main__':
    main()
