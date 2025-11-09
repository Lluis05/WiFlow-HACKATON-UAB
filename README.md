# UAB WiFi Dataset Analysis - UAB THE HACK! 2025

**Reto propuesto por:** DTIC (Serveis d'Informàtica UAB)

**Evento:** UAB THE HACK! - 8 y 9 de noviembre de 2025

**Categoría:** Análisis de Datos + IA/ML

---

# 📊 Análisis de Afluencia entre Edificios de la UAB

Este proyecto realiza un análisis de movilidad entre los edificios principales de la Universitat Autònoma de Barcelona (UAB) a partir de logs de conexión Wi-Fi.  
A partir de los registros de clientes conectados a distintos puntos de acceso (APs), se detectan cambios de ubicación y se visualizan como un grafo dinámico que muestra el flujo de personas entre edificios a lo largo del tiempo.

---

## 🧠 Funcionalidad

1. **Carga múltiples archivos JSON** con datos de dispositivos conectados.
2. **Extrae timestamps** desde los nombres de los archivos.
3. **Identifica cambios de localización** de cada MAC entre instantes consecutivos.
4. **Agrupa puntos de acceso por edificio** mediante regla de nombre (ej. `AP-CIEN-*` → `CIEN`).
5. **Filtra edificios relevantes**.
6. **Construye un grafo dirigido temporal** representando flujos entre edificios.
7. **Genera una animación** que muestra cómo evoluciona el movimiento en el tiempo.

---

## 📁 Estructura de datos esperada

Los archivos deben estar en un directorio `data/` junto al script:

---

### Campos en Access Points

```json
{
  "name": "AP-VET71",                    // Nombre del AP (identifica edificio)
  "serial": "AP_ea4f8dd0b2e0",           // Serial anonimizado
  "macaddr": "AP_ea4f8dd0b2e0",          // MAC anonimizada
  "ip_address": "IP_4a767db8d4a7",      // IP anonimizada
  "site": "UAB",
  "group_name": "Bellaterra",
  "status": "Up" / "Down",
  "client_count": 4,                     // Dispositivos conectados
  "cpu_utilization": 8,                  // Porcentaje CPU
  "mem_free": 158683136,
  "model": "314",
  "firmware_version": "10.6.0.3_90581",
  "radios": [                            // 2.4GHz, 5GHz, 6GHz
    {
      "band": 1,                         // 0=2.4GHz, 1=5GHz, 3=6GHz
      "channel": "112",
      "macaddr": "RADIO_31814ada5fa1",
      "radio_type": "802.11ac",
      "status": "Up",
      "tx_power": 17,                    // Potencia transmisión (dBm)
      "utilization": 3                   // Porcentaje uso del canal
    }
  ],
  "last_modified": 1747356419,           // Timestamp
  "uptime": 3867941                      // Segundos de uptime
}
```

### Campos en Clientes

```json
{
  "macaddr": "CLIENT_87e3ddea248c",              // MAC anonimizada
  "ip_address": "IP_b8b8ae24ea0e",              // IP anonimizada
  "hostname": "HOST_87e3ddea248c",              // Hostname anonimizado
  "username": "USER_87e3ddea248c",              // Username anonimizado
  "name": "NAME_87e3ddea248c",                  // Name anonimizado
  "associated_device": "AP_8e2d9933ec92",       // Serial del AP (match con APs)
  "associated_device_name": "AP-CEDU26",        // Nombre del AP
  "associated_device_mac": "AP_5cdc80c05afc",
  "radio_mac": "RADIO_6fad7568e4d9",            // MAC del radio (match con AP)
  "gateway_serial": "GW_5c870ce8653f",
  "vlan": "VLAN_A",                             // VLAN pseudonimizada
  "network": "UAB" / "eduroam",
  "authentication_type": "MAC Authentication" / "DOT1X",
  "band": 5,                                    // 2.4 o 5 GHz
  "channel": "100 (20 MHz)",
  "signal_db": -55,                             // Potencia señal (dBm)
  "signal_strength": 5,                         // 1-5 (1=peor, 5=mejor)
  "snr": 41,                                    // Signal-to-Noise Ratio
  "speed": 96,                                  // Velocidad actual (Mbps)
  "maxspeed": 192,                              // Velocidad máxima (Mbps)
  "health": 100,                                // Health score 0-100
  "manufacturer": "SMART Technologies, Inc.",
  "os_type": "Android" / "iOS" / "Windows" / ...,
  "client_category": "SmartDevice" / "Computer" / ...,
  "last_connection_time": 1743587787000,        // Timestamp
  "site": "UAB",
  "group_name": "Bellaterra"
}
```

---

## Restricciones de Uso

- **Solo para fines educativos e investigación** durante el hackathon
- **No redistribuir** el dataset fuera del evento
- **No intentar** revertir la anonimización (violación de privacidad)
- Los datos se **eliminarán después del hackathon** (puedes conservar agregados anonimizados)

---

## Licencia

El código de los scripts de procesamiento está bajo licencia MIT.
Los datos son propiedad de la UAB y solo para uso educativo durante el evento.
