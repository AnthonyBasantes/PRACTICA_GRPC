import grpc
import time
import random
from datetime import datetime
from concurrent import futures

import telemetria_pb2
import telemetria_pb2_grpc


class Monitor(telemetria_pb2_grpc.MonitorCadenaFrioServicer):

    def TransmitirTelemetria(self, request, context):

        camion = request.id_camion
        intervalo = request.intervalo_segundos

        # Verificar si el camion existe
        if camion not in ["CAM-001", "CAM-002"]:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                "El camion no existe"
            )

        # Validar intervalo
        if intervalo <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "El intervalo debe ser mayor a 0"
            )

        print("Monitoreando camion:", camion)

        while context.is_active():

            temperatura = round(random.uniform(0, 10), 2)

            latitud = round(random.uniform(-0.30, -0.10), 6)
            longitud = round(random.uniform(-78.60, -78.40), 6)

            alerta = temperatura < 2.0 or temperatura > 8.0

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("Camion:", camion, "- Temperatura:", temperatura)

            yield telemetria_pb2.LecturaSensor(
                id_camion=camion,
                temperatura_celsius=temperatura,
                latitud=latitud,
                longitud=longitud,
                timestamp=fecha,
                alerta_critica=alerta
            )

            time.sleep(intervalo)


def iniciar():

    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    telemetria_pb2_grpc.add_MonitorCadenaFrioServicer_to_server(
        Monitor(), servidor
    )

    servidor.add_insecure_port("[::]:50052")
    servidor.start()

    print("Servidor de telemetria iniciado en el puerto 50052")
    print("Esperando conexiones...")

    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar()