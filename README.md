# info de la materia: ST0263 Tópicos Especiales en Telemática.

## Estudiantes: 
 - Stiven Yepes Vanegas, esyepesv@eafit.edu. co
 - Juan Pablo Cortes Gonzalez, jpcortesg@eafit.edu.co
 - Yhilmar Andres Chaverra, yachaverrc@eafit.edu.co
 - Andrés Felipe Téllez Rodríguez, aftellezr@eafit.edu.co

## Profesor: 
- Edwin Nelson Montoya Munera, emontoya@eafit.edu.co


# Proyecto 2

# 1. Breve descripción de la actividad
El objetivo de este proyecto es diseñar e implementar un servicio de auto escalamiento que operará sobre instancias EC2 de AWS de Amazon.
# 2. Paso a paso
Se requieren algunos preparativos para iniciar este proyecto. Lo primero que se hace es generar un archivo .protos, el cual servira como base para generar codigo fuente para cuando empecemos a desarrollar los monitores, y en este archivo se especifica lo que buscamos realizar, y lo que regresa. En este caso el servicio Ping/Pong, GetMetrics, Register y Deregister. Se instala boto3, grpcio-tools y google con el comando ```pip install```. Una vez esto realizado empezamos a trabajar con el ASG
# 2.1 ASG Controller
Para esta parte se genera el archivo config.py el cual se encarga de almacenar las variables de configuración. Aqui se guarda tanto la Id del access key como la secret access key el token de inicio de sesión, la region y la ID
```bash
aws_access_key_id = ''
aws_secret_access_key = ''
session_token = ''
aws_region = ''
id_AMI = '' 
```
Una vez listo ese archivo se crea el archivo main.py el cual tiene los procesos de crear y finalizar las instancias. Lo primero que se hace es importar boto3, y las variables que se habian definido en config.py, despues se inicializa el cliente de boto3 para que este pueda trabajar con AWS y con el auto scaling
```bash
ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token = session_token,
    region_name=aws_region
)
```
Se empieza la configuración del proceso para crear las instancias. Empezamos con el catcher de los errores y se corre el cliente para que genere el archivo, y se llenan las especificaciones necesarias, e.j. El tipo de instancia la data de usuario, la ID del grupo de seguridad, etc. Y se consigue la ID de la instancia creada junto con su IP
```bash
    try:
        response = ec2_client.run_instances(
            ImageId=id_AMI,
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            UserData = '''#!/bin/bash
                git clone https://github.com/esyepesv/ASG-st0263.git
                cd /home/ubuntu/ASG-st0263/Instance/MonitorC1
                chmod +x script.sh
                bash script.sh
            ''',
            SecurityGroupIds=['sg-09460bf625a8b6ffb'],
            SubnetId='subnet-0b9b72090fcfa4ae2',
            IamInstanceProfile={
                'Arn': 'arn:aws:iam::192666608429:instance-profile/EMR_EC2_DefaultRole'
            }
        )
        instance_id = response['Instances'][0]['InstanceId']
    
        private_ip = response['Instances'][0]['PrivateIpAddress']
        print("Dirección IP privada:", private_ip)
        print("Instance created successfully. Instance ID:", instance_id)
        return instance_id
    except ClientError as e:
        print("Error creating instance:", e)
        return None
```
Por otra parte se crea el proceso para finalizar las instancias el cual requiere la ID de la instancia que se genero

```bash
    try:
        response = ec2_client.terminate_instances(
            InstanceIds=[instance_id],
        )
        print("Instance terminated successfully.")
    except ClientError as e:
        print("Error terminating instance:", e)
```
# 2.2 Monitor S
Una vez realizado el ASG Controller se genera el archivo main_pb2.py y main_pb2_grpc.py los cuales fueron creados al correr el archivo protos que configuramos al inicio. Con eso se crea el archivo main, con el cual abrimos un canal gRPC con el monitor S, y alli se crea un stub el cual usamos para correr los procesos de Ping/Pong, GetMetrics, Register y Deregister pasando en donde es necesario la ID de la instancia.
```bash
    # Abre un canal gRPC al servidor
    with grpc.insecure_channel('44.202.30.128:50051') as channel:
        # Crea un stub
        stub = main_pb2_grpc.MonitorServiceStub(channel)

        # Llama al método PingPong del servicio y pasa un mensaje "ping" como parte de la solicitud
        response = stub.PingPong(main_pb2.PingRequest(message='ping'))
        print(f'Pong: {response.message}')
        
        # Llama al método GetMetrics 
        response = stub.GetMetrics(main_pb2.MetricsRequest(instance_id='my-instance-id'))
        print(f'Metrics: {response.load}')

        # Llama al método Register
        response = stub.Register(main_pb2.RegisterRequest(instance_id='my-instance-id'))
        print(f'Register: {response.success}')

        # Llama al método Deregister
        response = stub.Deregister(main_pb2.DeregisterRequest(instance_id='my-instance-id'))
        print(f'Deregister: {response.success}')
```
# 2.2 Monitor C
Al igual que el monitor S, con el monitor C se genera el archivo main_pb2.py y main_pb2_grpc.py los cuales fueron creados al correr el archivo protos que configuramos al inicio. Se crea el archivo server.py donde definimos las funciones que usaremos con la respuesta requerida

```bash
    def PingPong(self, request, context):
        message = request.message
        response = main_pb2.PongResponse(message="Pong!")
        return response
```
*Ejemplo de definicion de una de las funciones*

Y se pone a correr el servidor ademas de ponerlo a escuchar el puerto 50051, para cuando se conecte el monitor S

```bash
    # Crear un servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor())

    # Adjuntar el servicio al servidor
    main_pb2_grpc.add_MonitorServiceServicer_to_server(MonitorService(), server)

    # Escuchar en el puerto 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado en el puerto 50051")

    # Mantener el servidor en ejecución
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)
```




# Referencias:
#### [EC2 Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
#### [ASG Boto3](https://docs.aws.amazon.com/code-library/latest/ug/python_3_auto-scaling_code_examples.html)
#### [AWS Code Repository](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/auto-scaling#code-examples)
#### [Archivo Proto](https://www.file-extension.info/es/format/proto)

#### versión README.md -> 1.0
