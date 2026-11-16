import grpc
import time

import pagos_pb2
import pagos_pb2_grpc


def iniciar():

    canal = grpc.insecure_channel("localhost:50051")
    stub = pagos_pb2_grpc.ValidadorPagosStub(canal)

    solicitud = pagos_pb2.SolicitudPago(
        id_transaccion="LAT001",
        numero_tarjeta="1234567890123456",
        monto=150,
        codigo_moneda="USD",
        pais_origen="US"
    )

    tiempos = []

    print("=== PRUEBA DE LATENCIA gRPC ===")

    try:
        # Primera solicitud para establecer la conexion
        stub.VerificarTransaccion(solicitud, timeout=5)

        # Realizar 100 solicitudes
        for i in range(100):

            inicio = time.perf_counter()

            respuesta = stub.VerificarTransaccion(solicitud, timeout=5)

            fin = time.perf_counter()

            tiempo_ms = (fin - inicio) * 1000

            tiempos.append(tiempo_ms)

        promedio = sum(tiempos) / len(tiempos)

        print("\nPruebas realizadas:", len(tiempos))
        print("Latencia minima:", round(min(tiempos), 3), "ms")
        print("Latencia maxima:", round(max(tiempos), 3), "ms")
        print("Latencia promedio:", round(promedio, 3), "ms")

        if max(tiempos) < 50:
            print("\nRESULTADO: CUMPLE el objetivo de latencia menor a 50 ms")
        else:
            print("\nRESULTADO: NO CUMPLE el objetivo en todas las solicitudes")

    except grpc.RpcError as e:
        print("\n[Error gRPC]")
        print("Codigo:", e.code())
        print("Detalle:", e.details())

    finally:
        canal.close()


if __name__ == "__main__":
    iniciar()