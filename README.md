# Práctica de gRPC con Python

## Descripción

Esta práctica implementa dos sistemas distribuidos utilizando
gRPC, Protocol Buffers y Python.

## Ejercicio 1: Validación de Pagos

Implementación de un microservicio gRPC unario que permite
validar transacciones de comercio electrónico.

Funcionalidades:
- Validación de montos y números de tarjeta.
- Detección de tarjetas bloqueadas.
- Aplicación de políticas de fraude.
- Manejo de errores gRPC.
- Generación de códigos de autorización.

Pruebas realizadas:
- TX001: Pago aprobado.
- TX002: Monto negativo (INVALID_ARGUMENT).
- TX003: Tarjeta bloqueada (PERMISSION_DENIED).
- TX004: Rechazo por política de fraude.

## Ejercicio 2: Server Streaming

Implementación de un sistema de monitoreo de cadena de frío
para camiones que transportan vacunas.

Funcionalidades:
- Transmisión continua de lecturas.
- Generación de temperaturas y coordenadas GPS.
- Detección de temperaturas fuera del rango de 2 °C a 8 °C.
- Alertas críticas en tiempo real.
- Validación de identificadores de camiones.
- Manejo de errores gRPC.

Pruebas realizadas:
- CAM-001: Transmisión continua de telemetría.
- Temperatura superior a 8 °C: Alerta crítica.
- CAM-999: Camión inexistente (NOT_FOUND).
- CAM-002 con intervalo 0: INVALID_ARGUMENT.

## Tecnologías utilizadas

- Python
- gRPC
- Protocol Buffers
- Ubuntu
- VSCodium

## Instalación

Crear y activar el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución del Ejercicio 1

Terminal 1:

```bash
cd Ejercicio1_Pagos
python3 servidor.py
```

Terminal 2, desde la carpeta principal:

```bash
cd Ejercicio1_Pagos
python3 cliente.py
```

## Ejecución del Ejercicio 2

Terminal 1:

```bash
cd Ejercicio2_ServerStreaming
python3 servidor.py
```

Terminal 2, desde la carpeta principal:

```bash
cd Ejercicio2_ServerStreaming
python3 cliente.py
```

## Conclusión

Se implementaron correctamente dos patrones de comunicación
gRPC: Unario y Server Streaming.

El primer ejercicio permite validar pagos mediante una
solicitud y una respuesta.

El segundo permite recibir múltiples lecturas de sensores
a partir de una única solicitud de suscripción.