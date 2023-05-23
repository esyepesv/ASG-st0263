import grpc

import main_pb2
import main_pb2_grpc

from ec2_manager import EC2Manager

MIN_INSTANCE = 2
MAX_INSTANCE = 5

def run():
    # Lista de IPs
    with open('../ips.txt', 'r') as file:
        contenido = file.read()
    ips = eval(contenido)

    cargaTotal = 0

    for ip, id in ips.items():
        try:
            # Abre un canal gRPC al servidor
            with grpc.insecure_channel(f'{ip}:50051') as channel:
                # Crea un stub (doble de objeto) para el servicio MonitorService
                stub = main_pb2_grpc.MonitorServiceStub(channel)

                # hacemos ping para ver que la instancia este corriendo
                response = stub.PingPong(main_pb2.PingRequest(message='ping'))
                print(response.message)
                if response.message != 'Pong!' and len(ips) <= MIN_INSTANCE:
                    EC2Manager.create_ec2_instance() #si no responde y hay menos del minimo de inmstancias, se crea una nueva
                
                response = stub.GetMetrics(main_pb2.MetricsRequest(instance_id=ip))
                print(f'Metrics: {response.load}')

                cargaTotal += response.load

        except (grpc.RpcError, grpc._channel._InactiveRpcError) as e:
            print(f'Error en gRPC: {str(e)}')

    nivelCarga = cargaTotal/len(ips)
    #nivelCarga = 80
    #nivelCarga = 20

    if nivelCarga >= 80:
        EC2Manager.create_ec2_instance()
    elif nivelCarga <= 20:
        EC2Manager.terminate_instance()

if __name__ == '__main__':
    run()


''' Metodos instancias:
                # Llama al método PingPong del servicio y pasa un mensaje "ping" como parte de la solicitud
                response = stub.PingPong(main_pb2.PingRequest(message='ping'))
                print(f'Pong: {response.message}')

                # Llama al método GetMetrics del servicio y pasa una instancia_id como parte de la solicitud
                response = stub.GetMetrics(main_pb2.MetricsRequest(instance_id='my-instance-id'))
                print(f'Metrics: {response.load}')

                # Llama al método Register del servicio y pasa una instancia_id como parte de la solicitud
                response = stub.Register(main_pb2.RegisterRequest(instance_id='my-instance-id'))
                print(f'Register: {response.success}')

                # Llama al método Deregister del servicio y pasa una instancia_id como parte de la solicitud
                response = stub.Deregister(main_pb2.DeregisterRequest(instance_id='my-instance-id'))
                print(f'Deregister: {response.success}')
'''
