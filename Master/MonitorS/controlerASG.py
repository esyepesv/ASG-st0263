import boto3
from botocore.exceptions import ClientError

# Importar variables de configuración de archivo config.py
from config import aws_access_key_id, aws_secret_access_key, aws_region, id_AMI, session_token

# Inicializar cliente de boto3 para trabajar con Amazon EC2 y Auto Scaling
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=session_token,
    region_name=aws_region
)

class EC2Manager:

    @staticmethod
    def openFile():
        with open('../ips.txt', 'r') as file:
            contenido = file.read()
        return eval(contenido)

    @staticmethod
    def closeFile(ips):
        with open('../ips.txt', 'w') as file:
            file.write(str(ips))

    @staticmethod
    def create_ec2_instance():
        try:
            response = ec2_client.run_instances(
                ImageId=id_AMI,
                InstanceType='t2.micro',
                MaxCount=1,
                MinCount=1,
                UserData='''#!/bin/bash
                    git clone https://github.com/esyepesv/ASG-st0263.git
                    cd /home/ubuntu/ASG-st0263/Instance/MonitorC1
                    chmod +x script.sh
                    bash script.sh
                ''',
                SecurityGroupIds=['sg-09460bf625a8b6ffb'],
                SubnetId='subnet-0b9b72090fcfa4ae2'
            )
            instance_id = response['Instances'][0]['InstanceId']
            private_ip = response['Instances'][0]['PrivateIpAddress']

            # Agregamos la IP y el ID en el diccionario de instancias
            ips = EC2Manager.openFile()
            ips[private_ip] = instance_id
            EC2Manager.closeFile(ips)

            print("Dirección IP privada:", private_ip)
            print("Instance created successfully. Instance ID:", instance_id)
            return instance_id
        except ClientError as e:
            print("Error creating instance:", e)
            return None

    @staticmethod
    def terminate_instance():
        ips = EC2Manager.openFile()
        instance_ip, instance_id = ips.popitem()
        EC2Manager.closeFile(ips)

        try:
            response = ec2_client.terminate_instances(
                InstanceIds=[instance_id],
            )
            print("Instance terminated successfully.")
        except ClientError as e:
            print("Error terminating instance:", e)


"""
if __name__ == '__main__':
    #EC2Manager.create_ec2_instance()
    EC2Manager.terminate_instance()
"""