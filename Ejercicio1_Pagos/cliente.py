import grpc

import pagos_pb2
import pagos_pb2_grpc


def probar_pago(stub, id, tarjeta, monto, moneda, pais):

    print("\n--- Prueba:", id, "---")

    try:
        solicitud = pagos_pb2.SolicitudPago(
            id_transaccion=id,
            numero_tarjeta=tarjeta,
            monto=monto,
            codigo_moneda=moneda,
            pais_origen=pais
        )

        respuesta = stub.VerificarTransaccion(solicitud)

        print("Aprobado:", respuesta.aprobado)
        print("Codigo de autorizacion:", respuesta.codigo_autorizacion)
        print("Motivo de rechazo:", respuesta.motivo_rechazo)

    except grpc.RpcError as e:
        print("[Error gRPC] Codigo:", e.code())
        print("[Error gRPC] Detalle:", e.details())


def iniciar():

    with grpc.insecure_channel("localhost:50051") as canal:

        stub = pagos_pb2_grpc.ValidadorPagosStub(canal)

        # Prueba 1: Pago exitoso
        probar_pago(
            stub, "TX001", "1234567890123456", 150, "USD", "US"
        )

        # Prueba 2: Monto negativo
        probar_pago(
            stub, "TX002", "1234567890123456", -50, "USD", "US"
        )

        # Prueba 3: Tarjeta bloqueada
        probar_pago(
            stub, "TX003", "4000123456789012", 200, "USD", "MX"
        )

        # Prueba 4: Politica de fraude
        probar_pago(
            stub, "TX004", "1234567890123456", 15000, "USD", "EC"
        )


if __name__ == "__main__":
    iniciar()