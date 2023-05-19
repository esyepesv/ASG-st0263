import boto3
from botocore.exceptions import ClientError

# Importar variables de configuración de archivo config.py
from config import aws_access_key_id, aws_secret_access_key, aws_region, id_AMI

# Inicializar cliente de boto3 para trabajar con Amazon EC2 y Auto Scaling
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region

)
asg_client = boto3.client(
    'autoscaling',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region

)

'''
def create_auto_scaling_group():
    try:
        response = asg_client.create_auto_scaling_group(
            AutoScalingGroupName='my-asg',
            LaunchConfigurationName='my-launch-config',
            MinSize=1,
            MaxSize=5,
            DesiredCapacity=1,
            AvailabilityZones=['us-east-1']
        )
        print("Auto Scaling group created successfully.")
    except ClientError as e:
        print("Error creating Auto Scaling group:", e)
'''
def create_ec2_instance():
    try:
        response = ec2_client.run_instances(
            ImageId=id_AMI,
            InstanceType='t2.micro',
            KeyName='vockey.pem',
            MaxCount=1,
            MinCount=1,
            UserData='#!/bin/bash\n echo "Hello, World!" > index.html\n nohup python -m SimpleHTTPServer 80 &',
            #SecurityGroupIds=['sg-0123456789abcdef0'],
            #SubnetId='subnet-0123456789abcdef0',
        )
        instance_id = response['Instances'][0]['InstanceId']
        print("Instance created successfully. Instance ID:", instance_id)
        return instance_id
    except ClientError as e:
        print("Error creating instance:", e)
        return None

def attach_instance_to_asg(instance_id):
    try:
        response = asg_client.attach_instances(
            AutoScalingGroupName='my-asg',
            InstanceIds=[instance_id],
        )
        print("Instance attached to Auto Scaling group successfully.")
    except ClientError as e:
        print("Error attaching instance to Auto Scaling group:", e)

def detach_instance_from_asg(instance_id):
    try:
        response = asg_client.detach_instances(
            AutoScalingGroupName='my-asg',
            InstanceIds=[instance_id],
            ShouldDecrementDesiredCapacity=True,
        )
        print("Instance detached from Auto Scaling group successfully.")
    except ClientError as e:
        print("Error detaching instance from Auto Scaling group:", e)

def terminate_instance(instance_id):
    try:
        response = ec2_client.terminate_instances(
            InstanceIds=[instance_id],
        )
        print("Instance terminated successfully.")
    except ClientError as e:
        print("Error terminating instance:", e)

def delete_auto_scaling_group():
    try:
        response = asg_client.delete_auto_scaling_group(
            AutoScalingGroupName='my-asg',
            ForceDelete=True,
        )
        print("Auto Scaling group deleted successfully.")
    except ClientError as e:
        print("Error deleting Auto Scaling group:", e)


if __name__ == '__main__':
    #create_auto_scaling_group()
    create_ec2_instance()
