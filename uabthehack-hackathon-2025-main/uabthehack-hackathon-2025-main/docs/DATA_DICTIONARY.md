# Data Dictionary - UAB WiFi Dataset

**Última actualización:** 8 de noviembre de 2025
**Dataset:** Datos de red WiFi del campus UAB (3 abril - 10 julio 2025)
**Evento:** UAB THE HACK! 2025

---

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Datos de Access Points](#datos-de-access-points)
3. [Datos de Clientes/Dispositivos](#datos-de-clientesdispositivos)
4. [Anonimización y Privacidad](#anonimización-y-privacidad)
5. [Relaciones entre Datos](#relaciones-entre-datos)
6. [Casos de Uso Frecuentes](#casos-de-uso-frecuentes)

---

## Visión General

El dataset contiene dos tipos principales de archivos JSON:

- **AP-info-v2-[timestamp].json**: Snapshots del estado de todos los Access Points (~1.169 APs)
- **client-info-[timestamp]-[count].json**: Información de dispositivos conectados (~10.000 dispositivos por snapshot)

**Frecuencia de captura:**
- Mayor durante horas lectivas (9:00-21:00)
- Intervalos de 15-30 minutos típicamente
- Período total: 3 de abril - 10 de julio de 2025

---

## Datos de Access Points

### Estructura General

Cada archivo contiene un array JSON con objetos que representan el estado de cada AP en ese momento.

```json
{
  "name": "AP-VET71",
  "serial": "AP_ea4f8dd0b2e0",
  "status": "Up",
  "client_count": 4,
  ...
}
```

### Campos Principales

#### Identificación

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `name` | string | `"AP-VET71"` | **Nombre del AP** - Identifica el edificio/ubicación. Formato: `AP-[EDIFICIO][NUMERO]`. **NO anonimizado** (necesario para geolocalización) |
| `serial` | string | `"AP_ea4f8dd0b2e0"` | **Serial anonimizado** - Identificador único persistente del hardware del AP |
| `macaddr` | string | `"AP_ea4f8dd0b2e0"` | **MAC anonimizada** - Dirección MAC del AP (mismo hash que serial) |
| `ip_address` | string | `"IP_4a767db8d4a7"` | **IP anonimizada** - Dirección IP del AP en la red de gestión |
| `public_ip_address` | string | `"158.109.XXX.XXX"` | **IP pública parcial** - Enmascarada para privacidad |

#### Estado y Conectividad

| Campo | Tipo | Valores/Ejemplo | Descripción |
|-------|------|-----------------|-------------|
| `status` | string | `"Up"`, `"Down"` | **Estado del AP** - Indica si está operativo |
| `down_reason` | string | `"Access Point disconnected from Aruba Central"` | **Motivo de caída** - Solo presente si `status == "Down"` |
| `client_count` | integer | `4` | **Dispositivos conectados** - Número de clientes activos en este AP |
| `uptime` | integer | `3867941` | **Tiempo activo** - Segundos desde el último reinicio |
| `last_modified` | integer | `1747356419` | **Timestamp** - Última modificación (Unix timestamp en segundos) |

#### Rendimiento del AP

| Campo | Tipo | Rango | Descripción |
|-------|------|-------|-------------|
| `cpu_utilization` | integer | 0-100 | **Uso de CPU** - Porcentaje de utilización del procesador |
| `mem_free` | integer | bytes | **Memoria libre** - RAM disponible en bytes |
| `mem_total` | integer | bytes | **Memoria total** - RAM total del dispositivo |

#### Hardware y Firmware

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `model` | string | `"314"` | **Modelo** - Código del modelo de hardware Aruba |
| `firmware_version` | string | `"10.6.0.3_90581"` | **Versión firmware** - Software instalado en el AP |
| `labels` | array | `["UAB-7240XM"]` | **Etiquetas** - Tags de clasificación del AP |

#### Ubicación y Organización

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `site` | string | `"UAB"` | **Sitio** - Siempre "UAB" en este dataset |
| `group_name` | string | `"Bellaterra"` | **Grupo** - Campus o zona geográfica |

#### Configuración de Red

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `ap_deployment_mode` | string | `"IAP"` | **Modo de despliegue** - "IAP" = Instant AP (autónomo) |
| `subnet_mask` | string | `"255.255.248.0"` | **Máscara de subred** - Configuración de red del AP |
| `mesh_role` | string | `"Unknown"`, `"Point"` | **Rol mesh** - Si participa en red mallada |
| `swarm_master` | boolean | `false` | **Maestro de enjambre** - Si coordina otros APs en modo IAP |
| `swarm_name` | string | `"AP-VET71"` | **Nombre del enjambre** - Grupo de coordinación IAP |

#### Clusters y Gateways

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `gateway_cluster_id` | integer | `82` | **ID de cluster gateway** - Grupo de gateways asociados |
| `gateway_cluster_name` | string | `"auto_group_229"` | **Nombre cluster** - Identificador del grupo |

---

### Radios (Antenas WiFi)

Cada AP tiene un array `radios[]` con 2-3 elementos (bandas 2.4GHz, 5GHz, 6GHz):

```json
{
  "radios": [
    {
      "band": 1,
      "channel": "112",
      "macaddr": "RADIO_31814ada5fa1",
      "status": "Up",
      "tx_power": 17,
      "utilization": 3,
      ...
    }
  ]
}
```

#### Campos de Radio

| Campo | Tipo | Valores/Ejemplo | Descripción |
|-------|------|-----------------|-------------|
| `band` | integer | `0`, `1`, `3` | **Banda de frecuencia** - `0`=2.4GHz, `1`=5GHz, `3`=6GHz |
| `channel` | string | `"112"`, `"11"` | **Canal WiFi** - Número de canal usado |
| `macaddr` | string | `"RADIO_31814ada5fa1"` | **MAC del radio** - Identificador anonimizado de la antena física. **IMPORTANTE:** Este ID se usa en los datos de clientes (`radio_mac`) |
| `status` | string | `"Up"`, `"Down"` | **Estado del radio** - Si está transmitiendo |
| `tx_power` | integer | dBm | **Potencia de transmisión** - Potencia en dBm (típico: 10-21) |
| `utilization` | integer | 0-100 | **Utilización del canal** - Porcentaje de tiempo ocupado |
| `radio_name` | string | `"Radio 5 GHz"` | **Nombre descriptivo** - Identificación legible |
| `radio_type` | string | `"802.11ac"`, `"802.11n"` | **Estándar WiFi** - Tecnología del radio |
| `spatial_stream` | string | `"4x4:4"`, `"2x2:2"` | **Configuración MIMO** - Antenas Tx x Rx : Streams |
| `index` | integer | `0`, `1` | **Índice del radio** - Orden en el array |
| `mode` | integer | `0` | **Modo operativo** - Tipo de operación (sin documentar) |

---

## Datos de Clientes/Dispositivos

### Estructura General

Cada archivo contiene un array JSON con objetos que representan dispositivos conectados en ese momento.

```json
{
  "macaddr": "CLIENT_87e3ddea248c",
  "associated_device_name": "AP-CEDU26",
  "signal_db": -55,
  "health": 100,
  ...
}
```

### Campos Principales

#### Identificación del Cliente

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `macaddr` | string | `"CLIENT_87e3ddea248c"` | **MAC anonimizada** - Identificador único persistente del dispositivo. **Consistente en el tiempo** |
| `ip_address` | string | `"IP_b8b8ae24ea0e"` | **IP anonimizada** - Dirección IP asignada al dispositivo |
| `hostname` | string | `"HOST_87e3ddea248c"` | **Hostname anonimizado** - Nombre del dispositivo en la red |
| `username` | string | `"USER_87e3ddea248c"` | **Username anonimizado** - Usuario autenticado (si aplica) |
| `name` | string | `"NAME_87e3ddea248c"` | **Name anonimizado** - Nombre amigable del dispositivo |

#### Asociación con Access Point

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `associated_device` | string | `"AP_8e2d9933ec92"` | **Serial del AP** - Coincide con `serial` en datos de APs. **CLAVE para joins** |
| `associated_device_mac` | string | `"AP_5cdc80c05afc"` | **MAC del AP** - Coincide con `macaddr` en datos de APs |
| `associated_device_name` | string | `"AP-CEDU26"` | **Nombre del AP** - Identificación legible de ubicación |
| `radio_mac` | string | `"RADIO_6fad7568e4d9"` | **MAC del radio** - Coincide con `radios[].macaddr` en APs. Identifica la banda específica |
| `radio_number` | integer | `0`, `1` | **Número de radio** - `0`=primer radio (5GHz), `1`=segundo (2.4GHz) |
| `gateway_serial` | string | `"GW_5c870ce8653f"` | **Serial del gateway** - Gateway de red asociado |

#### Red y Autenticación

| Campo | Tipo | Valores | Descripción |
|-------|------|---------|-------------|
| `network` | string | `"UAB"`, `"eduroam"` | **Red WiFi** - SSID generalizado (UAB o eduroam) |
| `vlan` | string | `"VLAN_A"`, `"VLAN_B"`, ... | **VLAN pseudonimizada** - Segmento de red. `VLAN_A` es mayoritario (~80%) |
| `authentication_type` | string | `"MAC Authentication"`, `"DOT1X"` | **Tipo de autenticación** - Método usado para conectar |
| `encryption_method` | string | `"OPEN"`, `"WPA2"`, `"WPA3"` | **Método de cifrado** - Seguridad de la conexión |
| `user_role` | string | `"conv_authenticad"` | **Rol de usuario** - Perfil asignado en la red |

#### Calidad de Señal

| Campo | Tipo | Rango/Ejemplo | Descripción |
|-------|------|---------------|-------------|
| `signal_db` | integer | -90 a -20 | **Potencia de señal** - RSSI en dBm. `-50` es excelente, `-70` es débil, `-80` muy pobre |
| `signal_strength` | integer | 1-5 | **Fuerza de señal simplificada** - Escala 1-5 (1=pésima, 5=excelente) |
| `snr` | integer | 0-100+ | **Signal-to-Noise Ratio** - Relación señal/ruido en dB. >40 es bueno, >25 aceptable |
| `health` | integer | 0-100 | **Health score** - Métrica agregada de calidad de conexión. 100 es perfecto |

#### Velocidad y Rendimiento

| Campo | Tipo | Unidad | Descripción |
|-------|------|--------|-------------|
| `speed` | integer | Mbps | **Velocidad actual** - Tasa de transmisión actual en Mbps |
| `maxspeed` | integer | Mbps | **Velocidad máxima** - Tasa máxima negociada según estándar WiFi |

#### Configuración del Canal

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `band` | float | `5.0`, `2.4` | **Banda de frecuencia** - GHz (2.4 o 5) |
| `channel` | string | `"100 (20 MHz)"`, `"1 (20 MHz)"` | **Canal y ancho** - Número de canal + ancho de banda |
| `ht_type` | integer | `3`, `1` | **Tipo HT/VHT** - Código de tecnología (sin documentar) |
| `phy_type` | integer | `1`, `0` | **Tipo PHY** - Capa física (sin documentar) |

#### Estándares WiFi

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `connection` | string | `"802.11ac, 802.11k, 802.11v"` | **Capacidades** - Estándares soportados por la conexión actual |

#### Información del Dispositivo

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `manufacturer` | string | `"Apple, Inc."`, `"Samsung Electronics"` | **Fabricante** - Según OUI de la MAC. **NO anonimizado** |
| `os_type` | string | `"Android"`, `"iOS"`, `"Windows"`, `"Mac"` | **Sistema operativo** - Detectado por fingerprinting. **NO anonimizado** |
| `client_category` | string | `"Computer"`, `"SmartDevice"`, `"Phone"` | **Categoría** - Tipo de dispositivo clasificado |
| `client_type` | string | `"WIRELESS"` | **Tipo de cliente** - Siempre "WIRELESS" en este dataset |
| `connected_device_type` | string | `"AP"` | **Tipo de conexión** - Siempre "AP" (conectado a Access Point) |

#### Ubicación y Organización

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `site` | string | `"UAB"` | **Sitio** - Siempre "UAB" en este dataset |
| `group_name` | string | `"Bellaterra"` | **Grupo** - Campus o zona geográfica |
| `group_id` | integer | `97` | **ID de grupo** - Identificador numérico del grupo |

#### Timestamps

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `last_connection_time` | integer | `1743587787000` | **Última conexión** - Unix timestamp en **milisegundos** (¡diferente de APs!) |

#### Etiquetas

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `labels` | array | `["UAB-7240XM"]` | **Etiquetas del AP** - Tags del AP al que está conectado |
| `label_id` | array | `[2]` | **IDs de etiquetas** - Identificadores numéricos |

#### Estado de Fallos

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `failure_stage` | string | `""`, `"DHCP"`, `"Auth"` | **Etapa de fallo** - Vacío si está OK, indica etapa si falló |

#### Configuración Mesh/Swarm

| Campo | Tipo | Ejemplo | Descripción |
|-------|------|---------|-------------|
| `swarm_id` | string | `""` | **ID de enjambre** - Grupo IAP al que pertenece el AP |

---

## Anonimización y Privacidad

### Método Utilizado

**HMAC-SHA256 con clave secreta (pepper)**

- Imposible de revertir sin la clave
- Consistente en el tiempo: mismo dispositivo = mismo hash
- Truncado a 12 caracteres (48 bits) para k-anonymity
- Tasa de colisión <1%

### Campos Anonimizados

| Prefijo | Tipo de Dato | Ejemplo |
|---------|--------------|---------|
| `CLIENT_` | MAC de dispositivo cliente | `CLIENT_87e3ddea248c` |
| `AP_` | MAC/Serial de Access Point | `AP_ea4f8dd0b2e0` |
| `RADIO_` | MAC de radio/antena | `RADIO_31814ada5fa1` |
| `IP_` | Dirección IP | `IP_b8b8ae24ea0e` |
| `HOST_` | Hostname | `HOST_87e3ddea248c` |
| `USER_` | Username | `USER_87e3ddea248c` |
| `NAME_` | Name | `NAME_87e3ddea248c` |
| `GW_` | Serial de Gateway | `GW_5c870ce8653f` |
| `VLAN_` | VLAN ID | `VLAN_A`, `VLAN_B` |

### Campos NO Anonimizados (Por Diseño)

- `name` (APs): Necesario para ubicación geográfica (ej: "AP-VET71" → Edificio Veterinaria)
- `manufacturer`: No identifica individuos
- `os_type`: No identifica individuos
- `network`: Nombre genérico ("UAB", "eduroam")

### Consistencia de Hashes

**Importante para análisis temporal:**

- Un dispositivo con MAC `CLIENT_87e3ddea248c` tendrá ese mismo hash en TODOS los archivos
- Permite seguir movilidad de dispositivos a lo largo del tiempo
- Un AP con serial `AP_ea4f8dd0b2e0` es el mismo en todos los snapshots

---

## Relaciones entre Datos

### Join AP ↔ Cliente

**Por serial del AP:**
```python
# Cliente conectado a AP
client['associated_device'] == ap['serial']
client['associated_device_mac'] == ap['macaddr']
```

**Por MAC del radio:**
```python
# Cliente conectado a radio específico del AP
client['radio_mac'] == ap['radios'][i]['macaddr']
```

### Ejemplos de Relaciones

#### 1. Encontrar el AP de un cliente

```python
client = {
  "macaddr": "CLIENT_87e3ddea248c",
  "associated_device": "AP_8e2d9933ec92",
  "associated_device_name": "AP-CEDU26",
  ...
}

# Buscar en datos de APs:
ap = find_ap_by_serial("AP_8e2d9933ec92")
# → ap['name'] == "AP-CEDU26"
```

#### 2. Contar dispositivos por AP

```python
# Método 1: Desde datos de clientes
devices_per_ap = clients.groupby('associated_device').size()

# Método 2: Desde datos de APs (más rápido)
ap['client_count']  # Número directo
```

#### 3. Análisis de movilidad temporal

```python
# Seguir un dispositivo a lo largo del tiempo
device_mac = "CLIENT_87e3ddea248c"

# En archivo timestamp1:
client1['associated_device_name'] == "AP-CEDU26"

# En archivo timestamp2:
client2['associated_device_name'] == "AP-VET71"

# → El dispositivo se movió de CEDU a VET
```

---

## Casos de Uso Frecuentes

### 1. Hotspot Analysis (Zonas Calientes)

**Campos relevantes:**
- `ap['name']` - Ubicación del AP
- `ap['client_count']` - Dispositivos conectados
- `client['associated_device_name']` - Agrupar por ubicación

**Pregunta:** ¿Qué edificios tienen más dispositivos?

```python
# Extraer edificio del nombre del AP
ap['building'] = ap['name'].str.extract(r'AP-([A-Z]+)\d+')
density = ap.groupby('building')['client_count'].sum()
```

### 2. Calidad de Señal

**Campos relevantes:**
- `client['signal_db']` - RSSI
- `client['snr']` - Signal-to-Noise
- `client['health']` - Health score
- `client['signal_strength']` - 1-5

**Pregunta:** ¿Qué APs tienen peor calidad?

```python
poor_signal = clients[clients['signal_db'] < -70]
problematic_aps = poor_signal.groupby('associated_device_name').size()
```

### 3. Análisis de Velocidad

**Campos relevantes:**
- `client['speed']` - Velocidad actual
- `client['maxspeed']` - Velocidad máxima
- `client['band']` - 2.4 vs 5 GHz

**Pregunta:** ¿Qué dispositivos no alcanzan su velocidad máxima?

```python
clients['speed_ratio'] = clients['speed'] / clients['maxspeed']
underperforming = clients[clients['speed_ratio'] < 0.5]
```

### 4. Distribución de Bandas

**Campos relevantes:**
- `client['band']` - 2.4 o 5 GHz
- `client['channel']` - Canal usado

**Pregunta:** ¿Cuántos dispositivos usan 2.4GHz vs 5GHz?

```python
band_distribution = clients['band'].value_counts()
```

### 5. Carga por Hora del Día

**Campos relevantes:**
- `ap['last_modified']` - Timestamp del snapshot
- `ap['client_count']` - Dispositivos conectados

**Pregunta:** ¿Cuáles son las horas pico?

```python
from datetime import datetime
ap['hour'] = pd.to_datetime(ap['last_modified'], unit='s').dt.hour
hourly_load = ap.groupby('hour')['client_count'].mean()
```

### 6. Movilidad de Dispositivos

**Campos relevantes:**
- `client['macaddr']` - Identificador del dispositivo
- `client['associated_device_name']` - AP actual
- Archivos de diferentes timestamps

**Pregunta:** ¿Cómo se mueven los dispositivos entre edificios?

```python
# Cargar dos snapshots temporales
t1_clients = load_clients('file_t1.json')
t2_clients = load_clients('file_t2.json')

# Merge por MAC del dispositivo
movements = t1_clients.merge(t2_clients, on='macaddr', suffixes=('_t1', '_t2'))

# Filtrar los que cambiaron de AP
moved = movements[
    movements['associated_device_name_t1'] != movements['associated_device_name_t2']
]
```

### 7. Tipos de Dispositivos

**Campos relevantes:**
- `client['manufacturer']` - Fabricante
- `client['os_type']` - Sistema operativo
- `client['client_category']` - Categoría

**Pregunta:** ¿Qué tipos de dispositivos se conectan más?

```python
device_types = clients.groupby(['os_type', 'client_category']).size()
```

### 8. Red UAB vs eduroam

**Campos relevantes:**
- `client['network']` - "UAB" o "eduroam"
- `client['vlan']` - Segmento de red

**Pregunta:** ¿Cómo se distribuyen los usuarios entre redes?

```python
network_distribution = clients.groupby(['network', 'vlan']).size()
```

### 9. Rendimiento de APs

**Campos relevantes:**
- `ap['cpu_utilization']` - Uso de CPU
- `ap['mem_free']` / `ap['mem_total']` - Memoria
- `ap['client_count']` - Carga de clientes

**Pregunta:** ¿Qué APs están sobrecargados?

```python
ap['mem_usage_pct'] = 100 * (1 - ap['mem_free'] / ap['mem_total'])
overloaded = ap[
    (ap['cpu_utilization'] > 80) |
    (ap['mem_usage_pct'] > 80) |
    (ap['client_count'] > 50)
]
```

### 10. Canales WiFi Congestionados

**Campos relevantes:**
- `ap['radios'][]['channel']` - Canal usado
- `ap['radios'][]['utilization']` - % de uso del canal
- `ap['radios'][]['band']` - Banda (2.4 o 5 GHz)

**Pregunta:** ¿Qué canales tienen más interferencia?

```python
# Explotar array de radios
radios = []
for ap in aps:
    for radio in ap['radios']:
        radios.append({
            'ap_name': ap['name'],
            'channel': radio['channel'],
            'utilization': radio['utilization'],
            'band': radio['band']
        })

radios_df = pd.DataFrame(radios)
congested_channels = radios_df.groupby('channel')['utilization'].mean().sort_values(ascending=False)
```

---

## Conversiones y Fórmulas Útiles

### Timestamps

```python
import pandas as pd
from datetime import datetime

# Access Points (segundos)
ap['datetime'] = pd.to_datetime(ap['last_modified'], unit='s')

# Clientes (milisegundos)
client['datetime'] = pd.to_datetime(client['last_connection_time'], unit='ms')
```

### Memoria

```python
# Convertir bytes a MB
ap['mem_free_mb'] = ap['mem_free'] / (1024 * 1024)
ap['mem_total_mb'] = ap['mem_total'] / (1024 * 1024)
```

### Calidad de Señal (Interpretación)

```python
def signal_quality(rssi):
    if rssi >= -50:
        return "Excelente"
    elif rssi >= -60:
        return "Buena"
    elif rssi >= -70:
        return "Aceptable"
    else:
        return "Pobre"

client['signal_quality'] = client['signal_db'].apply(signal_quality)
```

### Extraer Edificio del Nombre del AP

```python
# Patrón: AP-[EDIFICIO][NUMERO]
# Ejemplos: AP-VET71, AP-CEDU26, AP-LLET40

ap['building'] = ap['name'].str.extract(r'AP-([A-Z]+)\d+')[0]
```

---

## Limitaciones y Consideraciones

### Datos Faltantes

- Algunos campos pueden ser `null` o `""` (vacíos)
- `down_reason` solo aparece cuando `status == "Down"`
- `failure_stage` está vacío si la conexión es exitosa

### Precisión de Timestamps

- **APs:** `last_modified` en segundos (Unix timestamp)
- **Clientes:** `last_connection_time` en milisegundos
- No todos los snapshots tienen la misma frecuencia temporal

### Granularidad Geográfica

- **Ubicación:** Solo disponible a nivel de AP (nombre del edificio)
- **Pendiente:** Coordenadas GPS de APs (en proceso desde GIS)

### Colisiones de Hash

- Tasa esperada: <1%
- Puede afectar análisis de movilidad de dispositivos individuales
- Análisis agregados no se ven afectados

### Sesgo Temporal

- Mayor frecuencia de snapshots durante horas lectivas
- Menor cobertura en fines de semana y horario nocturno

---

## Recursos Adicionales

### Documentación de Referencia

- **Aruba Central API**: https://developer.arubanetworks.com/
- **802.11 Standards**: https://en.wikipedia.org/wiki/IEEE_802.11
- **WiFi Signal Strength Guide**: https://www.metageek.com/training/resources/wifi-signal-strength-basics/

### Archivos Relacionados

- `README.md` - Visión general del challenge
- `USAGE_GUIDE.md` - Guía de uso paso a paso
- `ANONYMIZATION_STRATEGY.md` - Estrategia de privacidad
- `starter_kits/` - Notebooks con ejemplos de código

---

## Contacto

**Soporte durante el hackathon:**
albert.gil.lopez@uab.cat

---

**Última revisión:** 8 de noviembre de 2025
**Versión:** 1.0
**Licencia:** Documentación bajo CC BY 4.0 - Datos solo para uso educativo

