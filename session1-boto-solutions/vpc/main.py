"""play with boto and aws resources"""

import awsops

def main():

    aws = awsops.AwsOperation()
    aws.create_vpc()

if __name__ == '__main__':
    main()