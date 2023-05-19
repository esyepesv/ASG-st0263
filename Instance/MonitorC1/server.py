import grpc
from concurrent import futures
import main_pb2
import main_pb2_grpc

class MonitorService(main_pb2_grpc.MonitorServiceServicer):
    def PingPong(self, request, context):
        message = request.message
        response = main_pb2.PongResponse(message="Pong!")
        return response

    def GetMetrics(self, request, context):
        instance_id = request.instance_id
        # Lógica para obtener las métricas del servidor usando el instance_id
        load = 10  # Ejemplo de valor de carga
        response = main_pb2.MetricsResponse(load=load)
        return response

    def Register(self, request, context):
        instance_id = request.instance_id
        # Lógica para registrar el servidor usando el instance_id
        success = True  # Ejemplo de éxito en el registro
        response = main_pb2.RegisterResponse(success=success)
        return response

    def Deregister(self, request, context):
        instance_id = request.instance_id
        # Lógica para desregistrar el servidor usando el instance_id
        success = True  # Ejemplo de éxito en la desregistración
        response = main_pb2.DeregisterResponse(success=success)
        return response

def run_server():
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

if __name__ == '__main__':
    run_server()
