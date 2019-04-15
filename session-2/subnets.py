#!/usr/bin/env python3

import awsops
import parsing
import config


def main():
    parser = parsing.Parsing()
    args = parser.args_parser()
    aws = awsops.AwsOperations(args)
    public_cidr = config.MAPPING[config.PUBLIC_TAG]
    subnet_id = aws.create_subnet(public_cidr)
    aws.create_tags(subnet_id, config.PUBLIC_TAG)
    # get private subnet cidr	
    # create private subnet
    # tag the private subnet


if __name__ == '__main__':
    main()
