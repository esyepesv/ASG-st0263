import grpc

import main_pb2
import main_pb2_grpc

def run():
    # Abre un canal gRPC al servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crea un stub (doble de objeto) para el servicio MonitorService
        stub = main_pb2_grpc.MonitorServiceStub(channel)

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

if __name__ == '__main__':
    run()
