import boto3
from botocore.exceptions import ClientError

# Importar variables de configuración de archivo config.py
from config import aws_access_key_id, aws_secret_access_key, aws_region, id_AMI, session_token

# Inicializar cliente de boto3 para trabajar con Amazon EC2 y Auto Scaling
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token = session_token,
    region_name=aws_region
)

def create_ec2_instance():
    try:
        response = ec2_client.run_instances(
            ImageId=id_AMI,
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            UserData = '#!/bin/bash git clone https://github.com/esyepesv/ASG-st0263.git cd /home/ubuntu/ASG-st0263/Instance/MonitorC1 chmod +x script.sh bash script.sh ',
            SecurityGroupIds=['sg-09460bf625a8b6ffb'],
            SubnetId='subnet-0b9b72090fcfa4ae2'
        )
        instance_id = response['Instances'][0]['InstanceId']
    
        private_ip = response['Instances'][0]['PrivateIpAddress']
        #public_ip = response['Instances'][0]['PublicIpAddress']
        print("Dirección IP privada:", private_ip)
       # print("Dirección IP pública:", public_ip)
        print("Instance created successfully. Instance ID:", instance_id)
        return instance_id
    except ClientError as e:
        print("Error creating instance:", e)
        return None

def terminate_instance(instance_id):
    try:
        response = ec2_client.terminate_instances(
            InstanceIds=[instance_id],
        )
        print("Instance terminated successfully.")
    except ClientError as e:
        print("Error terminating instance:", e)


if __name__ == '__main__':
    create_ec2_instance()
    #terminate_instance('i-0b2a3b541ffa57704')
