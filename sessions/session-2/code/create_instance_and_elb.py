#!/usr/bin/env python3

import boto3
import config


def create_security_group(sg_name, sg_description, vpc_id):
    sg_response = EC2_CLIENT.create_security_group(GroupName=sg_name,
                                                   Description=sg_description,
                                                   VpcId=vpc_id)
    sg_id = sg_response['GroupId']
    return sg_id


def authorize_security_group(sg_id, sg_rules):
    response_authorize = EC2_CLIENT.authorize_security_group_ingress \
        (GroupId=sg_id,
         IpPermissions=sg_rules,
        )
    return response_authorize


def create_instance(security_group_id):
    ec2_resource = boto3.resource('ec2', region_name=config.REGION)
    response_instance = ec2_resource.create_instances(
        ImageId=config.AMI_ID,
        TagSpecifications=
        [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': config.INSTANCE_NAME
                    }
                ]
            },
        ],
        MinCount=1,
        MaxCount=1,
        KeyName="test-meetups",
        InstanceType="t2.micro",
        SecurityGroupIds=[
            security_group_id
        ],
        SubnetId=config.INSTANCE_SUBNET_ID,
        UserData=config.USERDATA,
        BlockDeviceMappings=
        [
            {
                'DeviceName': '/dev/sdb',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 10,
                    'VolumeType': 'gp2',
                    'Encrypted': True,
                }
            },
        ])
    return response_instance


def create_load_balancer(name, listeners, subnet_id, sg_id, scheme):
    ELB_CLIENT.create_load_balancer(
        LoadBalancerName=name,
        Listeners=listeners,
        Subnets=subnet_id,
        SecurityGroups=[sg_id],
        Scheme=scheme
    )


def configure_lb_health_check(name, health, interval, timeout, unhealth_threshold, health_threshold):
    ELB_CLIENT.configure_health_check(
        LoadBalancerName=name,
        HealthCheck=\
            {'Target': health,
             'Interval': interval,
             'Timeout': timeout,
             'UnhealthyThreshold': unhealth_threshold,
             'HealthyThreshold': health_threshold
            })


def register_instance_to_elb(instance_id):
    response_register = ELB_CLIENT.register_instances_with_load_balancer(
        LoadBalancerName=config.ELB_NAME,
        Instances=[
            {
                'InstanceId': instance_id
            },
        ]
    )
    return response_register


if __name__ == '__main__':
    EC2_CLIENT = boto3.client('ec2', region_name=config.REGION)
    ELB_CLIENT = boto3.client('elb', region_name=config.REGION)
    SG_INSTANCE_ID = create_security_group(config.INSTANCE_SG_NAME,
                                           config.INSTANCE_SG_DESCRIPTION,
                                           config.VPC_ID)
    authorize_security_group(SG_INSTANCE_ID, config.INSTANCE_SG_RULES)
    SG_ELB_ID = create_security_group(config.ELB_SG_NAME,
                                      config.ELB_SG_DESCRIPTION,
                                      config.VPC_ID)
    authorize_security_group(SG_ELB_ID, config.ELB_SG_RULES)
    create_load_balancer(config.ELB_NAME,
                         config.ELB_LISTENERS,
                         config.ELB_SUBNET_ID,
                         SG_ELB_ID,
                         config.ELB_SCHEME)
    configure_lb_health_check(config.ELB_NAME,
                              config.ELB_HEALTH,
                              config.ELB_INTERVAL,
                              config.ELB_TIMEOUT,
                              config.ELB_UNHEALTH_THRESHOLD,
                              config.ELB_HEALTH_THRESHOLD)
    INSTANCE_ID = create_instance(SG_INSTANCE_ID)
    for instance in INSTANCE_ID:
        register_instance_to_elb(instance.id)
