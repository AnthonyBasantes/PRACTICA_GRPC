# Práctica de gRPC con Python

**Asignatura:** Sistemas Distribuidos  
**Autor:** Anthony Josue Basantes Aguirre  
**Tecnologías:** Python, gRPC, Protocol Buffers y HTTP/2  
**Entorno de desarrollo:** Ubuntu y VSCodium

---

## 1. Descripción general

Este repositorio contiene el desarrollo de dos ejercicios prácticos de comunicación distribuida mediante gRPC y Protocol Buffers.

**Ejercicio 1 — RPC Unario:** implementación de un microservicio de validación de pagos y detección de fraude para comercio electrónico.

**Ejercicio 2 — Server Streaming:** implementación de un sistema de monitoreo de temperatura y ubicación de camiones que transportan vacunas bajo cadena de frío.

Ambos ejercicios se desarrollaron en Python y se probaron localmente mediante la comunicación entre clientes y servidores gRPC.

## 2. Objetivos

- Comprender el funcionamiento de gRPC y Protocol Buffers.
- Implementar comunicación cliente-servidor mediante RPC unario.
- Implementar transmisión continua de datos mediante Server Streaming.
- Gestionar errores utilizando códigos de estado gRPC.
- Validar reglas de negocio en los servicios desarrollados.
- Medir la latencia del servicio de pagos y verificar el objetivo de respuesta inferior a 50 milisegundos.

## 3. Estructura del proyecto

```text
PRACTICA_GRPC/
│
├── Ejercicio1_Pagos/
│   ├── pagos.proto
│   ├── pagos_pb2.py
│   ├── pagos_pb2_grpc.py
│   ├── servidor.py
│   ├── cliente.py
│   └── prueba_latencia.py
│
├── Ejercicio2_ServerStreaming/
│   ├── telemetria.proto
│   ├── telemetria_pb2.py
│   ├── telemetria_pb2_grpc.py
│   ├── servidor.py
│   └── cliente.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

Los archivos `*_pb2.py` y `*_pb2_grpc.py` son generados mediante Protocol Buffers y permiten la comunicación entre clientes y servidores.

El entorno virtual `venv` se utiliza localmente y no se incluye en el repositorio.

## 4. Instalación y configuración

### 4.1 Requisitos

- Python 3
- pip
- grpcio
- grpcio-tools
- Ubuntu
- VSCodium o Visual Studio Code

### 4.2 Crear el entorno virtual

Desde la carpeta principal del proyecto:

```bash
python3 -m venv venv
```

Activar el entorno:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
python3 -m pip install -r requirements.txt
```

### 4.3 Generar archivos gRPC

Para el primer ejercicio:

```bash
cd Ejercicio1_Pagos

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
```

Para el segundo ejercicio:

```bash
cd ../Ejercicio2_ServerStreaming

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. telemetria.proto
```

Los archivos generados ya están incluidos en el repositorio, por lo que normalmente no es necesario volver a generarlos.

---

# 5. EJERCICIO 1 — VALIDACIÓN DE PAGOS CON RPC UNARIO

## 5.1 Descripción

Se desarrolló un microservicio que permite validar transacciones de pago utilizando comunicación gRPC.

El cliente envía los datos de una transacción y el servidor determina si debe aprobarse, rechazarse por una política de fraude o generar un error.

Se utiliza el patrón RPC unario, en el que cada solicitud produce una única respuesta.

## 5.2 Contrato Protocol Buffers

El archivo `pagos.proto` define el servicio:

**ValidadorPagos**

Método:

```protobuf
rpc VerificarTransaccion(SolicitudPago) returns (ResultadoPago);
```

La solicitud contiene:

- ID de transacción.
- Número de tarjeta.
- Monto.
- Código de moneda.
- País de origen.

La respuesta contiene:

- Estado de aprobación.
- Código de autorización.
- Motivo de rechazo.

## 5.3 Reglas de validación

El servidor implementa las siguientes condiciones:

| Condición | Resultado |
|---|---|
| Monto menor o igual a cero | INVALID_ARGUMENT |
| Tarjeta que no tenga exactamente 16 dígitos | INVALID_ARGUMENT |
| Tarjeta que comienza por 4000 | PERMISSION_DENIED |
| Monto mayor a 10000 y país distinto de US o MX | Pago rechazado |
| Transacción válida | Pago aprobado |

Estas reglas corresponden a una simulación académica de validación de pagos.

## 5.4 Ejecución del servidor

Desde la carpeta principal del proyecto:

```bash
source venv/bin/activate
cd Ejercicio1_Pagos
python3 servidor.py
```

El servidor utiliza el puerto **50051**.

## 5.5 Ejecución del cliente

En una segunda terminal:

```bash
source venv/bin/activate
cd Ejercicio1_Pagos
python3 cliente.py
```

El cliente realiza cuatro pruebas.

## 5.6 Resultados de las pruebas

| Prueba | Descripción | Resultado |
|---|---|---|
| TX001 | Transacción válida | Aprobada |
| TX002 | Monto negativo | INVALID_ARGUMENT |
| TX003 | Tarjeta bloqueada por fraude | PERMISSION_DENIED |
| TX004 | Monto elevado desde Ecuador | Rechazada por política de fraude |

Ejemplo de salida:

```text
--- Prueba: TX001 ---
Aprobado: True
Codigo de autorizacion: 46C67D61
Motivo de rechazo:

--- Prueba: TX002 ---
[Error gRPC] Codigo: StatusCode.INVALID_ARGUMENT
[Error gRPC] Detalle: Monto o número de tarjeta inválido

--- Prueba: TX003 ---
[Error gRPC] Codigo: StatusCode.PERMISSION_DENIED
[Error gRPC] Detalle: Tarjeta bloquada por fraude

--- Prueba: TX004 ---
Aprobado: False
Codigo de autorizacion:
Motivo de rechazo: Rechazado por politica de fraude
```

El código de autorización puede variar en cada ejecución.

## 5.7 Prueba de latencia gRPC

### Objetivo

Comprobar que el servicio de validación de pagos presenta un tiempo de respuesta inferior a **50 milisegundos**.

### Implementación

Se desarrolló el archivo:

`Ejercicio1_Pagos/prueba_latencia.py`

Este programa realiza 100 solicitudes consecutivas al servidor gRPC.

Para medir el tiempo de respuesta de cada solicitud se utiliza:

```python
time.perf_counter()
```

Después se calculan la latencia mínima, máxima y promedio.

### Ejecución

**Terminal 1 — Servidor:**

```bash
cd ~/PRACTICA_GRPC/Ejercicio1_Pagos
source ../venv/bin/activate
python3 servidor.py
```

**Terminal 2 — Prueba de latencia:**

```bash
cd ~/PRACTICA_GRPC/Ejercicio1_Pagos
source ../venv/bin/activate
python3 prueba_latencia.py
```

### Resultados obtenidos

La prueba se ejecutó correctamente en Ubuntu, realizando 100 solicitudes al servidor de validación de pagos.

| Métrica | Resultado |
|---|---|
| Solicitudes realizadas | 100 |
| Latencia mínima | 0.352 ms |
| Latencia máxima | 2.378 ms |
| Latencia promedio | 0.470 ms |
| Objetivo establecido | Menor a 50 ms |
| **Cumplimiento** | **CUMPLE** |

### Salida obtenida

```text
=== PRUEBA DE LATENCIA gRPC ===

Pruebas realizadas: 100
Latencia minima: 0.352 ms
Latencia maxima: 2.378 ms
Latencia promedio: 0.47 ms

RESULTADO: CUMPLE el objetivo de latencia menor a 50 ms
```

### Análisis de resultados

Los resultados demuestran que el servicio de validación de pagos cumplió el objetivo establecido durante las 100 solicitudes realizadas.

La latencia promedio fue de **0.470 ms**, mientras que la latencia máxima registrada fue de **2.378 ms**.

Debido a que el valor máximo es inferior a 50 ms, todas las solicitudes medidas cumplieron el requisito de rendimiento.

Es importante señalar que las mediciones se realizaron mediante `localhost`, con el cliente y el servidor ejecutándose en la misma computadora. Por tanto, estos resultados representan el rendimiento local del servicio y no garantizan los mismos tiempos en redes externas o entornos de producción.

**Conclusión del ejercicio 1:** Se implementó correctamente el servicio RPC unario, se verificaron las reglas de validación y se comprobó el cumplimiento del objetivo de latencia en las pruebas locales realizadas.

---

# 6. EJERCICIO 2 — SERVER STREAMING PARA CADENA DE FRÍO

## 6.1 Descripción

Se desarrolló un sistema de monitoreo de temperatura y ubicación para camiones que transportan vacunas.

El servidor genera lecturas simuladas de temperatura y coordenadas geográficas.

El cliente se suscribe a un camión y recibe continuamente los datos enviados por el servidor.

Este ejercicio utiliza **Server Streaming**, donde una solicitud del cliente permite recibir múltiples respuestas.

## 6.2 Contrato Protocol Buffers

El archivo `telemetria.proto` define el servicio:

**MonitorCadenaFrio**

Método:

```protobuf
rpc TransmitirTelemetria(SuscripcionCamion) returns (stream LecturaSensor);
```

La solicitud contiene:

- Identificador del camión.
- Intervalo de transmisión en segundos.

Cada lectura contiene:

- Identificador del camión.
- Temperatura en grados Celsius.
- Latitud.
- Longitud.
- Fecha y hora.
- Estado de alerta crítica.

## 6.3 Reglas implementadas

| Condición | Resultado |
|---|---|
| Camión CAM-001 | Válido |
| Camión CAM-002 | Válido |
| Camión inexistente | NOT_FOUND |
| Intervalo menor o igual a cero | INVALID_ARGUMENT |
| Temperatura menor a 2 °C | Alerta crítica |
| Temperatura mayor a 8 °C | Alerta crítica |
| Temperatura entre 2 °C y 8 °C | Temperatura normal |

Las temperaturas y coordenadas son generadas mediante una simulación.

## 6.4 Ejecución del servidor

Desde la carpeta principal:

```bash
source venv/bin/activate
cd Ejercicio2_ServerStreaming
python3 servidor.py
```

El servidor utiliza el puerto **50052**.

## 6.5 Ejecución del cliente

En otra terminal:

```bash
source venv/bin/activate
cd Ejercicio2_ServerStreaming
python3 cliente.py
```

El programa solicita:

```text
=== MONITOR DE CADENA DE FRIO ===

Ingrese el ID del camion: CAM-001
Intervalo en segundos: 2
```

El cliente recibe las lecturas mediante:

```python
for respuesta in stub.TransmitirTelemetria(peticion):
```

Las alertas críticas se resaltan en rojo en la terminal.

Para detener el monitoreo se utiliza `Ctrl + C`.

## 6.6 Pruebas realizadas

| Prueba | Resultado |
|---|---|
| Suscripción a CAM-001 | Lecturas recibidas correctamente |
| Temperatura dentro del rango | Temperatura normal |
| Temperatura fuera del rango | Alerta crítica |
| Suscripción a CAM-999 | NOT_FOUND |
| Intervalo de 0 segundos | INVALID_ARGUMENT |

### Ejemplo de alerta crítica

```text
Camion: CAM-001
Temperatura: 8.74 °C

!!! ALERTA CRITICA !!!
TEMPERATURA FUERA DEL RANGO
```

### Error de camión inexistente

```text
[Error gRPC]
Codigo: StatusCode.NOT_FOUND
Detalle: El camion no existe
```

### Error de intervalo inválido

```text
[Error gRPC]
Codigo: StatusCode.INVALID_ARGUMENT
Detalle: El intervalo debe ser mayor a 0
```

**Conclusión del ejercicio 2:** Se implementó correctamente la transmisión continua de lecturas mediante Server Streaming, incluyendo alertas de temperatura y manejo de errores gRPC.

---

# 7. COMPARACIÓN DE LOS DOS EJERCICIOS

| Característica | RPC Unario | Server Streaming |
|---|---|---|
| Ejercicio | Validación de pagos | Monitoreo de cadena de frío |
| Solicitud del cliente | Una | Una suscripción |
| Respuestas del servidor | Una | Múltiples |
| Puerto | 50051 | 50052 |
| Aplicación | Validación de transacciones | Monitoreo continuo |
| Método destacado | return | yield |
| Manejo de errores | INVALID_ARGUMENT y PERMISSION_DENIED | NOT_FOUND e INVALID_ARGUMENT |

Ambos ejercicios demuestran diferentes formas de comunicación distribuida mediante gRPC.

---

# 8. EVIDENCIAS DE FUNCIONAMIENTO

Durante el desarrollo de la práctica se realizaron pruebas para verificar el funcionamiento de los servicios implementados.

Las evidencias obtenidas incluyen:

1. Ejecución del servidor y cliente de validación de pagos.
2. Pruebas de transacciones aprobadas y rechazadas.
3. Manejo de errores mediante códigos gRPC.
4. Ejecución del servidor y cliente de telemetría.
5. Recepción continua de lecturas de temperatura.
6. Visualización de alertas críticas.
7. Validación de camiones inexistentes e intervalos incorrectos.
8. Medición de latencia mediante 100 solicitudes al servicio de pagos.

Las capturas correspondientes se utilizan como evidencia en el informe de laboratorio.

---

# 9. CONCLUSIONES GENERALES

El desarrollo de esta práctica permitió comprender e implementar dos patrones de comunicación mediante gRPC utilizando Python y Protocol Buffers.

En el primer ejercicio se implementó un microservicio de validación de pagos mediante RPC unario, incorporando reglas de negocio, aprobación y rechazo de transacciones, así como el manejo de errores mediante códigos de estado gRPC.

Adicionalmente, se realizó una prueba de rendimiento con 100 solicitudes consecutivas. Se obtuvo una latencia mínima de 0.352 ms, una máxima de 2.378 ms y un promedio de 0.470 ms, verificando el cumplimiento del objetivo inferior a 50 milisegundos en el entorno local.

En el segundo ejercicio se implementó un sistema de monitoreo de cadena de frío mediante Server Streaming. El cliente recibió múltiples lecturas de temperatura y ubicación, identificó valores fuera del rango permitido y gestionó correctamente las solicitudes inválidas.

Finalmente, ambos ejercicios permitieron fortalecer los conocimientos sobre comunicación cliente-servidor, servicios distribuidos, transmisión de datos y manejo de errores mediante gRPC.

---

# 10. ALCANCE Y LIMITACIONES

Este proyecto fue desarrollado con fines académicos.

Los pagos, las temperaturas y las ubicaciones son simulados y no corresponden a transacciones bancarias ni a dispositivos físicos reales.

La prueba de latencia se realizó localmente mediante `localhost`, por lo que sus resultados no representan necesariamente el comportamiento del servicio en una red externa o bajo una carga de trabajo elevada.

Para una implementación en producción sería necesario incorporar mecanismos adicionales de seguridad, autenticación, cifrado y monitoreo.

---

**Autor:** Anthony Josue Basantes Aguirre  
**Asignatura:** Sistemas Distribuidos  
**Proyecto:** Práctica de gRPC con Python
