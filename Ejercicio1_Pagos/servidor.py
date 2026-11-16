import grpc
import uuid
from concurrent import futures

import pagos_pb2
import pagos_pb2_grpc


class Validador(pagos_pb2_grpc.ValidadorPagosServicer):

    def VerificarTransaccion(self, request, context):

        print("Procesando transaccion:", request.id_transaccion)

        # Validar monto y tarjeta
        if request.monto <= 0 or not (
            len(request.numero_tarjeta) == 16
            and request.numero_tarjeta.isascii()
            and request.numero_tarjeta.isdigit()
        ):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Monto o número de tarjeta inválido")
            return pagos_pb2.ResultadoPago()

        # Tarjeta bloqueada
        if request.numero_tarjeta.startswith("4000"):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Tarjeta bloquada por fraude")
            return pagos_pb2.ResultadoPago()

        # Politica de fraude
        if request.monto > 10000 and request.pais_origen not in ["US", "MX"]:
            return pagos_pb2.ResultadoPago(
                aprobado=False,
                codigo_autorizacion="",
                motivo_rechazo="Rechazado por politica de fraude"
            )

        # Pago aprobado
        return pagos_pb2.ResultadoPago(
            aprobado=True,
            codigo_autorizacion=str(uuid.uuid4())[:8].upper(),
            motivo_rechazo=""
        )


def iniciar():

    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(
        Validador(), servidor
    )

    servidor.add_insecure_port("[::]:50051")
    servidor.start()

    print("Servidor de pagos iniciado en el puerto 50051")
    print("Esperando transacciones...")

    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar()