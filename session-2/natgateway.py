#!/usr/bin/env python3

import awsops
import parsing
import config

def main():
    parser = parsing.Parsing()
    args = parser.args_parser()
    aws = awsops.AwsOperations(args)
    allocate_id = aws.allocate_address()
    subnet_id = aws.get_subnet_id(get-the-correct-tag-from-config)
    nat_gateway_id = aws.create_nat_gateway(subnet_id, allocate_id)
    #use function wait_for_nat_gateway to wait till the nat gateway is in available state
    print(nat_gateway_id)


if __name__ == '__main__':
    main()

