import grpc
import main_pb2
import main_pb2_grpc

'''
ofrece servicios como:
- ping pong o hearbeat
- GetMetrics (carga simulada)
- registro y desregistro
'''

def run_client():
    # Establecer la conexión con el servidor gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = main_pb2_grpc.MonitorServiceStub(channel)

    # Ejemplo de llamada al servicio PingPong
    ping_request = main_pb2.PingRequest(message="Ping!")
    pong_response = stub.PingPong(ping_request)
    print("Ping-Pong response:", pong_response.message)

    # Ejemplo de llamada al servicio GetMetrics
    metrics_request = main_pb2.MetricsRequest(instance_id="instance001")
    metrics_response = stub.GetMetrics(metrics_request)
    print("Metrics response:", metrics_response.load)

    # Ejemplo de llamada al servicio Register
    register_request = main_pb2.RegisterRequest(instance_id="instance001")
    register_response = stub.Register(register_request)
    print("Register response:", register_response.success)

    # Ejemplo de llamada al servicio Deregister
    deregister_request = main_pb2.DeregisterRequest(instance_id="instance001")
    deregister_response = stub.Deregister(deregister_request)
    print("Deregister response:", deregister_response.success)

if __name__ == '__main__':
    run_client()
