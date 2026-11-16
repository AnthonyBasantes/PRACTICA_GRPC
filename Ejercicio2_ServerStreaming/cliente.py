import grpc

import telemetria_pb2
import telemetria_pb2_grpc


def iniciar():

    print("=== MONITOR DE CADENA DE FRIO ===")

    camion = input("Ingrese el ID del camion: ")

    try:
        intervalo = int(input("Intervalo en segundos: "))

        with grpc.insecure_channel("localhost:50052") as canal:

            stub = telemetria_pb2_grpc.MonitorCadenaFrioStub(canal)

            peticion = telemetria_pb2.SuscripcionCamion(
                id_camion=camion,
                intervalo_segundos=intervalo
            )

            print("\nRecibiendo telemetria...\n")

            for respuesta in stub.TransmitirTelemetria(peticion):

                print("------------------------------")
                print("Camion:", respuesta.id_camion)
                print("Temperatura:", respuesta.temperatura_celsius, "°C")
                print("Latitud:", respuesta.latitud)
                print("Longitud:", respuesta.longitud)
                print("Fecha:", respuesta.timestamp)

                if respuesta.alerta_critica:
                    print("\033[91m")
                    print("!!! ALERTA CRITICA !!!")
                    print("TEMPERATURA FUERA DEL RANGO")
                    print("\033[0m")
                else:
                    print("\033[92mTemperatura normal\033[0m")

    except grpc.RpcError as e:
        print("\n[Error gRPC]")
        print("Codigo:", e.code())
        print("Detalle:", e.details())

    except ValueError:
        print("Error: ingrese un intervalo numerico")

    except KeyboardInterrupt:
        print("\nMonitoreo finalizado")


if __name__ == "__main__":
    iniciar()