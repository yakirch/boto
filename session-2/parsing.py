#!/usr/bin/env python3

import argparse


class Parsing():
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")

    def args_parser(self):
        """ validate arguments and return them """
        self.parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
        self.parser.add_argument("--vpcid", "-p", help="Get vpc id",
                            required=True)
        self.parser.add_argument("--region", "-r", help="Get target region",
                            required=True)
        self.parser.add_argument("--internetgw", "-i", help="Get Internet gateway",
                            required=False)
        self.parser.add_argument("--natgw", "-n", help="Get Nat gateway",
                                 required=False)
        self.parser.add_argument("--az", "-a", help="Get availability zone",
                                 required=False)
        return self.parser.parse_args()