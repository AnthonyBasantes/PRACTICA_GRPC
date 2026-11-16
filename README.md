# PRÁCTICA DE SISTEMAS DISTRIBUIDOS CON gRPC Y PYTHON

### Implementación de comunicación unaria y Server Streaming

**Asignatura:** Sistemas Distribuidos  
**Desarrollador:** Anthony Josue Basantes Aguirre  
**Lenguaje de programación:** Python  
**Entorno de desarrollo:** Ubuntu y VSCodium  
**Tecnologías:** gRPC, Protocol Buffers, HTTP/2 y Git  
**Repositorio:** AnthonyBasantes/PRACTICA_GRPC

---

## 1. DESCRIPCIÓN GENERAL

Este proyecto presenta la implementación de dos aplicaciones distribuidas utilizando **gRPC (Google Remote Procedure Call)** y el lenguaje de programación Python.

El propósito principal es comprender y aplicar diferentes patrones de comunicación entre un cliente y un servidor, utilizando Protocol Buffers para definir los contratos de comunicación y HTTP/2 como protocolo de transporte.

La práctica está dividida en dos ejercicios:

**Ejercicio 1 — Comunicación Unaria:** Desarrollo de un microservicio de validación de pagos electrónicos y detección de fraude para una plataforma de comercio electrónico.

**Ejercicio 2 — Server Streaming:** Implementación de un sistema de monitoreo de telemetría IoT para supervisar la temperatura de camiones que transportan productos farmacéuticos.

Ambos ejercicios incluyen validaciones, manejo de errores mediante códigos de estado gRPC y pruebas de funcionamiento.

---

## 2. OBJETIVOS

### Objetivo general

Implementar y comprobar el funcionamiento de servicios distribuidos mediante gRPC y Python, utilizando los patrones de comunicación unaria y Server Streaming para resolver problemas relacionados con pagos electrónicos y monitoreo de sensores.

### Objetivos específicos

- Comprender el funcionamiento de gRPC y su aplicación en sistemas distribuidos.
- Definir servicios y mensajes mediante archivos Protocol Buffers.
- Implementar la comunicación entre clientes y servidores utilizando Python.
- Desarrollar un servicio unario para validar transacciones electrónicas.
- Implementar un servicio Server Streaming para transmitir información continuamente.
- Aplicar reglas de negocio y validaciones en los servidores.
- Manejar errores mediante códigos de estado gRPC.
- Realizar pruebas para comprobar el funcionamiento de ambos sistemas.
- Utilizar Git y GitHub para organizar y almacenar el código fuente.

---

## 3. TECNOLOGÍAS UTILIZADAS

| Tecnología | Descripción |
|---|---|
| Python | Lenguaje utilizado para desarrollar clientes y servidores. |
| gRPC | Framework que permite ejecutar procedimientos remotos. |
| Protocol Buffers | Sistema de serialización y definición de mensajes. |
| HTTP/2 | Protocolo de transporte utilizado por gRPC. |
| Ubuntu | Sistema operativo utilizado durante el desarrollo. |
| VSCodium | Editor de código fuente. |
| Git | Sistema de control de versiones. |
| GitHub | Plataforma utilizada para almacenar el repositorio. |

### 3.1. ¿Qué es gRPC?

gRPC es un framework de comunicación remota que permite que diferentes aplicaciones intercambien información y ejecuten funciones ubicadas en otros procesos o servidores.

Su funcionamiento se basa en la definición de servicios que pueden ser invocados por clientes a través de una red.

### 3.2. ¿Qué es Protocol Buffers?

Protocol Buffers es un mecanismo desarrollado por Google que permite definir estructuras de datos y serializar información en un formato binario compacto.

En esta práctica se utilizan archivos `.proto` para establecer los mensajes y métodos disponibles en cada servicio.

### 3.3. Patrones de comunicación utilizados

**Comunicación unaria (Unary RPC):**

El cliente envía una solicitud al servidor y recibe una única respuesta.

Se utiliza en el Ejercicio 1 para verificar transacciones de pago.

**Server Streaming:**

El cliente envía una solicitud y el servidor responde mediante un flujo de múltiples mensajes.

Se utiliza en el Ejercicio 2 para transmitir continuamente lecturas de sensores.

---

## 4. ESTRUCTURA DEL PROYECTO

```text
PRACTICA_GRPC/
│
├── Ejercicio1_Pagos/
│   ├── pagos.proto
│   ├── pagos_pb2.py
│   ├── pagos_pb2_grpc.py
│   ├── servidor.py
│   └── cliente.py
│
├── Ejercicio2_ServerStreaming/
│   ├── telemetria.proto
│   ├── telemetria_pb2.py
│   ├── telemetria_pb2_grpc.py
│   ├── servidor.py
│   └── cliente.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Descripción de los archivos

| Archivo | Función |
|---|---|
| `pagos.proto` | Define el contrato del servicio de pagos. |
| `telemetria.proto` | Define el contrato del servicio de telemetría. |
| `servidor.py` | Implementa la lógica del servidor de cada ejercicio. |
| `cliente.py` | Realiza solicitudes y procesa las respuestas. |
| `*_pb2.py` | Contiene las clases de mensajes generadas por Protobuf. |
| `*_pb2_grpc.py` | Contiene las clases necesarias para implementar servicios gRPC. |
| `requirements.txt` | Registra las dependencias del proyecto. |
| `.gitignore` | Excluye archivos innecesarios del repositorio. |
| `README.md` | Contiene la documentación general. |

---

# 5. EJERCICIO 1: VALIDACIÓN DE PAGOS Y DETECCIÓN DE FRAUDE

## 5.1. Descripción

Este ejercicio consiste en desarrollar un microservicio que simula una pasarela de pagos electrónicos.

El cliente envía los datos de una transacción y el servidor verifica si cumple las condiciones necesarias para aprobarla.

El sistema utiliza el patrón **gRPC Unario**, donde cada solicitud genera una única respuesta.

## 5.2. Funcionamiento

El proceso se desarrolla de la siguiente manera:

1. El cliente crea una solicitud con los datos del pago.
2. La solicitud se envía al servidor mediante gRPC.
3. El servidor verifica el monto y el número de tarjeta.
4. Se comprueba si la tarjeta pertenece a la lista negra.
5. Se aplican las políticas de detección de fraude.
6. El servidor devuelve una respuesta de aprobación, rechazo o error.
7. El cliente muestra el resultado en la consola.

### Arquitectura

```text
       CLIENTE PYTHON
              |
              | SolicitudPago
              v
       SERVIDOR gRPC
              |
              v
     Validación de datos
              |
              v
     Verificación de fraude
              |
              v
        ResultadoPago
              |
              v
       CLIENTE PYTHON
```

## 5.3. Contrato Protocol Buffers

El archivo `pagos.proto` define el servicio:

```protobuf
syntax = "proto3";

service ValidadorPagos {
    rpc VerificarTransaccion (SolicitudPago) returns (ResultadoPago);
}

message SolicitudPago {
    string id_transaccion = 1;
    string numero_tarjeta = 2;
    double monto = 3;
    string codigo_moneda = 4;
    string pais_origen = 5;
}

message ResultadoPago {
    bool aprobado = 1;
    string codigo_autorizacion = 2;
    string motivo_rechazo = 3;
}
```

El método `VerificarTransaccion` recibe un mensaje `SolicitudPago` y devuelve un mensaje `ResultadoPago`.

## 5.4. Reglas de negocio

El servidor implementa las siguientes validaciones:

**Validación de argumentos:**

Si el monto es menor o igual a cero, o el número de tarjeta no contiene exactamente 16 dígitos, se devuelve:

`grpc.StatusCode.INVALID_ARGUMENT`

**Detección de tarjetas bloqueadas:**

Si el número de tarjeta comienza con `4000`, se devuelve:

`grpc.StatusCode.PERMISSION_DENIED`

**Política de fraude:**

Si el monto supera los 10.000 USD y el país de origen no corresponde a `US` o `MX`, la transacción es rechazada.

**Aprobación:**

Si la solicitud cumple las condiciones, el servidor aprueba el pago y genera un código de autorización.

## 5.5. Manejo de errores

El cliente utiliza:

```python
except grpc.RpcError as e:
    print("[Error gRPC] Codigo:", e.code())
    print("[Error gRPC] Detalle:", e.details())
```

Esto permite identificar los errores generados durante las llamadas remotas.

## 5.6. Pruebas realizadas

Se ejecutaron cuatro casos de prueba.

| Prueba | Descripción | Resultado |
|---|---|---|
| TX001 | Pago válido de 150 USD | Aprobado |
| TX002 | Pago con monto negativo | INVALID_ARGUMENT |
| TX003 | Tarjeta bloqueada | PERMISSION_DENIED |
| TX004 | Pago de 15.000 USD desde Ecuador | Rechazado por política de fraude |

### Resultados obtenidos

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

El código de autorización se genera automáticamente y puede variar entre ejecuciones.

## 5.7. Análisis de resultados

Las pruebas permitieron comprobar que el servicio distingue correctamente entre transacciones válidas, solicitudes con argumentos incorrectos, tarjetas bloqueadas y operaciones rechazadas por políticas de fraude.

También se verificó el manejo de excepciones gRPC mediante los códigos `INVALID_ARGUMENT` y `PERMISSION_DENIED`.

**Resultado:** el ejercicio cumplió satisfactoriamente las pruebas funcionales realizadas.

---

# 6. EJERCICIO 2: MONITOREO DE TELEMETRÍA IoT Y CADENA DE FRÍO

## 6.1. Descripción

Este ejercicio implementa un sistema de monitoreo que simula la transmisión de información desde camiones encargados de transportar vacunas.

Los productos farmacéuticos deben mantenerse dentro de un rango de temperatura comprendido entre **2 °C y 8 °C**.

El sistema permite que un cliente se suscriba a las lecturas de un camión y reciba información periódica.

Se utiliza el patrón **gRPC Server Streaming**.

## 6.2. Funcionamiento

El proceso se desarrolla de la siguiente manera:

1. El cliente solicita monitorear un camión.
2. Envía el identificador del vehículo y el intervalo de actualización.
3. El servidor comprueba que el camión exista.
4. Se generan temperaturas y coordenadas GPS simuladas.
5. Cada lectura se transmite mediante `yield`.
6. El cliente recibe continuamente los mensajes.
7. Cuando la temperatura está fuera del rango permitido, se muestra una alerta crítica.

### Arquitectura

```text
          CLIENTE
             |
             | SuscripcionCamion
             v
      SERVIDOR gRPC
             |
             v
    Generación de sensores
             |
             v
      LecturaSensor 1
             |
             v
      LecturaSensor 2
             |
             v
      LecturaSensor 3
             |
             v
           ...

    Flujo continuo de datos
```

## 6.3. Contrato Protocol Buffers

El archivo `telemetria.proto` contiene:

```protobuf
syntax = "proto3";

service MonitorCadenaFrio {
    rpc TransmitirTelemetria (SuscripcionCamion) returns (stream LecturaSensor);
}

message SuscripcionCamion {
    string id_camion = 1;
    int32 intervalo_segundos = 2;
}

message LecturaSensor {
    string id_camion = 1;
    double temperatura_celsius = 2;
    double latitud = 3;
    double longitud = 4;
    string timestamp = 5;
    bool alerta_critica = 6;
}
```

La palabra clave `stream` indica que el servidor puede enviar múltiples respuestas a partir de una única solicitud.

## 6.4. Generación de telemetría

El servidor utiliza la biblioteca `random` para generar temperaturas simuladas.

```python
temperatura = round(random.uniform(0, 10), 2)
```

Las temperaturas pueden encontrarse dentro o fuera del rango permitido.

También se generan coordenadas geográficas simuladas:

```python
latitud = round(random.uniform(-0.30, -0.10), 6)
longitud = round(random.uniform(-78.60, -78.40), 6)
```

Estas coordenadas son datos de prueba y no corresponden a mediciones GPS reales.

## 6.5. Detección de alertas

La condición utilizada es:

```python
alerta = temperatura < 2.0 or temperatura > 8.0
```

Cuando la temperatura es inferior a 2 °C o superior a 8 °C, la variable `alerta` toma el valor `True`.

El cliente muestra una advertencia resaltada en rojo.

## 6.6. Implementación de Server Streaming

El servidor transmite las lecturas mediante:

```python
yield telemetria_pb2.LecturaSensor(
    id_camion=camion,
    temperatura_celsius=temperatura,
    latitud=latitud,
    longitud=longitud,
    timestamp=fecha,
    alerta_critica=alerta
)
```

La instrucción `yield` permite producir sucesivamente los mensajes del flujo sin finalizar inmediatamente el método.

Por su parte, el cliente utiliza:

```python
for respuesta in stub.TransmitirTelemetria(peticion):
```

Este bucle permite procesar cada lectura conforme llega desde el servidor.

## 6.7. Manejo de errores

El servidor valida los identificadores de los camiones.

Los camiones permitidos son:

- `CAM-001`
- `CAM-002`

Si se solicita un identificador inexistente, se genera:

`grpc.StatusCode.NOT_FOUND`

También se comprueba que el intervalo sea mayor a cero.

Si el intervalo es inválido, se genera:

`grpc.StatusCode.INVALID_ARGUMENT`

## 6.8. Pruebas realizadas

| Prueba | Descripción | Resultado |
|---|---|---|
| 1 | Monitoreo de CAM-001 cada 2 segundos | Correcto |
| 2 | Temperatura superior a 8 °C | Alerta crítica |
| 3 | Camión CAM-999 | NOT_FOUND |
| 4 | CAM-002 con intervalo de 0 segundos | INVALID_ARGUMENT |

### Resultados del monitoreo

Durante la ejecución se obtuvieron las siguientes lecturas:

| Temperatura | Estado |
|---|---|
| 2.92 °C | Normal |
| 6.58 °C | Normal |
| 4.95 °C | Normal |
| 8.74 °C | Alerta crítica |
| 2.25 °C | Normal |

Cuando la temperatura alcanzó los 8.74 °C, el cliente mostró:

```text
Camion: CAM-001
Temperatura: 8.74 °C
Latitud: -0.144394
Longitud: -78.429362
Fecha: 2026-11-16 17:42:12

!!! ALERTA CRITICA !!!
TEMPERATURA FUERA DEL RANGO
```

### Prueba de camión inexistente

```text
Ingrese el ID del camion: CAM-999
Intervalo en segundos: 2

[Error gRPC]
Codigo: StatusCode.NOT_FOUND
Detalle: El camion no existe
```

### Prueba de intervalo inválido

```text
Ingrese el ID del camion: CAM-002
Intervalo en segundos: 0

[Error gRPC]
Codigo: StatusCode.INVALID_ARGUMENT
Detalle: El intervalo debe ser mayor a 0
```

## 6.9. Análisis de resultados

Las pruebas demostraron que el servidor transmite múltiples lecturas a partir de una única petición del cliente.

Se comprobó que las temperaturas fuera del rango permitido activan correctamente la bandera `alerta_critica`.

También se verificó el manejo de errores para camiones inexistentes e intervalos incorrectos.

**Resultado:** el sistema cumplió satisfactoriamente las pruebas funcionales del patrón Server Streaming.

---

# 7. INSTALACIÓN Y CONFIGURACIÓN

## 7.1. Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.
- pip.
- Soporte para entornos virtuales.
- Las bibliotecas gRPC.
- Una terminal de Linux, Windows o macOS.

Las pruebas originales se realizaron en Ubuntu.

## 7.2. Clonar el repositorio

```bash
git clone https://github.com/AnthonyBasantes/PRACTICA_GRPC.git
```

Ingresar al proyecto:

```bash
cd PRACTICA_GRPC
```

## 7.3. Crear el entorno virtual

En Ubuntu:

```bash
python3 -m venv venv
```

Si Ubuntu indica que falta el paquete `venv`, instalar el correspondiente a la versión de Python utilizada.

Activar el entorno:

```bash
source venv/bin/activate
```

## 7.4. Instalar dependencias

```bash
python3 -m pip install -r requirements.txt
```

## 7.5. Generar archivos Protocol Buffers

Los archivos generados se incluyen en el repositorio, pero pueden regenerarse cuando sea necesario.

Para el Ejercicio 1:

```bash
cd Ejercicio1_Pagos

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
```

Regresar a la carpeta principal:

```bash
cd ..
```

Para el Ejercicio 2:

```bash
cd Ejercicio2_ServerStreaming

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. telemetria.proto
```

---

# 8. EJECUCIÓN DE LOS EJERCICIOS

## 8.1. Ejercicio 1 — Validación de pagos

Abrir una terminal y ejecutar:

```bash
cd ~/PRACTICA_GRPC/Ejercicio1_Pagos
source ../venv/bin/activate
python3 servidor.py
```

El servidor utiliza el puerto `50051`.

Abrir una segunda terminal:

```bash
cd ~/PRACTICA_GRPC/Ejercicio1_Pagos
source ../venv/bin/activate
python3 cliente.py
```

El cliente ejecutará automáticamente los cuatro casos de prueba.

## 8.2. Ejercicio 2 — Server Streaming

Abrir una terminal:

```bash
cd ~/PRACTICA_GRPC/Ejercicio2_ServerStreaming
source ../venv/bin/activate
python3 servidor.py
```

El servidor utiliza el puerto `50052`.

Abrir una segunda terminal:

```bash
cd ~/PRACTICA_GRPC/Ejercicio2_ServerStreaming
source ../venv/bin/activate
python3 cliente.py
```

El programa solicitará:

```text
Ingrese el ID del camion: CAM-001
Intervalo en segundos: 2
```

El cliente comenzará a recibir lecturas periódicas.

Para finalizar el monitoreo, presionar:

```text
Ctrl + C
```

**Nota:** los comandos anteriores utilizan la ubicación original del proyecto en Ubuntu. Si se clonó en otra carpeta, se deben adaptar las rutas.

---

# 9. COMPARACIÓN ENTRE LOS EJERCICIOS

| Característica | Ejercicio 1 | Ejercicio 2 |
|---|---|---|
| Patrón gRPC | Unario | Server Streaming |
| Aplicación | Validación de pagos | Monitoreo IoT |
| Solicitudes del cliente | Una por transacción | Una por suscripción |
| Respuestas del servidor | Una por solicitud | Múltiples |
| Método principal | VerificarTransaccion | TransmitirTelemetria |
| Transmisión continua | No | Sí |
| Uso de yield | No | Sí |
| Puerto | 50051 | 50052 |
| Manejo de errores | INVALID_ARGUMENT y PERMISSION_DENIED | NOT_FOUND e INVALID_ARGUMENT |

### Diferencia principal

En el patrón unario, el servidor devuelve una sola respuesta por cada solicitud.

En Server Streaming, el servidor puede transmitir una secuencia de respuestas sin que el cliente tenga que realizar una nueva solicitud por cada mensaje.

---

# 10. CONCLUSIONES

La implementación de ambos ejercicios permitió comprender el funcionamiento de gRPC como tecnología de comunicación para sistemas distribuidos.

En el primer ejercicio se desarrolló un microservicio de validación de pagos mediante el patrón unario, comprobando la correcta aplicación de reglas de negocio y el manejo de errores.

En el segundo ejercicio se implementó un sistema de monitoreo mediante Server Streaming, demostrando cómo un servidor puede enviar información continuamente a un cliente.

El uso de Protocol Buffers permitió definir de manera estructurada los mensajes intercambiados entre las aplicaciones.

Las pruebas realizadas confirmaron el funcionamiento de los dos patrones de comunicación y la correcta generación de respuestas y códigos de error.

Finalmente, el desarrollo de esta práctica permitió fortalecer conocimientos relacionados con Python, gRPC, comunicación cliente-servidor, manejo de excepciones y control de versiones mediante Git y GitHub.

**Observación:** ambos ejercicios son simulaciones académicas. No procesan pagos reales ni reciben datos de sensores físicos. Tampoco se realizaron pruebas de rendimiento para verificar una latencia inferior a 50 milisegundos.

---

## 11. REFERENCIAS

- Documentación oficial de gRPC: https://grpc.io/docs/
- Documentación de gRPC para Python: https://grpc.io/docs/languages/python/
- Documentación de Protocol Buffers: https://protobuf.dev/
- Documentación oficial de Python: https://docs.python.org/3/
- Documentación oficial de Git: https://git-scm.com/doc

---

## AUTOR

**Anthony Josue Basantes Aguirre**

Estudiante de Ingeniería en Ciencias de la Computación.

**Asignatura:** Sistemas Distribuidos

**Proyecto:** Implementación de gRPC Unario y Server Streaming con Python.

**Estado del proyecto:** Ejercicios implementados y pruebas funcionales completadas.
