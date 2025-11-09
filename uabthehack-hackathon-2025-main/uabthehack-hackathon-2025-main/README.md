# UAB WiFi Dataset Analysis - UAB THE HACK! 2025

**Reto propuesto por:** DTIC (Serveis d'Informàtica UAB)

**Evento:** UAB THE HACK! - 8 y 9 de noviembre de 2025

**Categoría:** Análisis de Datos + IA/ML

---

## Descripción del Reto

Analiza los datos de la red WiFi del campus de la UAB para descubrir patrones de uso, identificar problemas de conectividad y proponer mejoras basadas en datos reales.

El dataset incluye información de **más de 1.000 Access Points** distribuidos por todo el campus y **miles de dispositivos** conectados durante el período abril-julio 2025.

---

## Dataset

### Estructura

- **Datos de Access Points (7.229 archivos JSON)**
  - Snapshots temporales de todos los APs del campus
  - Frecuencia: mayor durante horas lectivas
  - Tamaño: ~1.4MB por archivo (~10GB total)

- **Datos de Clientes/Dispositivos (3.205 archivos JSON)**
  - Información detallada de dispositivos conectados
  - ~10.000 dispositivos por snapshot
  - Tamaño variable

### Período de Datos

**3 de abril - 10 de julio de 2025**

### Anonimización

**Todos los datos personales han sido anonimizados** usando HMAC-SHA256 con clave secreta:
- MACs de dispositivos → `CLIENT_8f3a2b1c4d5e`
- IPs → `IP_a1b2c3d4e5f6`
- Serials de APs → `AP_4d3c2b1a0f9e`
- Usernames → `USER_9e8d7c6b5a4f`
- VLANs → `VLAN_A`, `VLAN_B`, etc.

**La anonimización es consistente:** un mismo dispositivo tendrá el mismo hash en todos los archivos, permitiendo análisis de movilidad temporal.

---

## Niveles del Reto

### Nivel 1: ROOKIE (Análisis Básico)

**Objetivo:** Explorar y visualizar el dataset

**Tareas sugeridas:**
- Identificar zonas "hotspot" con alta densidad de dispositivos
- Analizar patrones temporales (horas pico, días de la semana)
- Visualizar distribución de dispositivos por edificio
- Estadísticas básicas: número de APs, dispositivos únicos, etc.

**Herramientas recomendadas:** Python, Pandas, Matplotlib, Seaborn

**Entregable:** Notebook con visualizaciones y conclusiones

---

### Nivel 2: INTERMEDIO (Análisis Avanzado)

**Objetivo:** Descubrir patrones y problemas de conectividad

**Tareas sugeridas:**
- **Análisis de movilidad:** flujos de dispositivos entre edificios
- **Calidad de servicio:** zonas con señal débil o problemas de conexión
- **Mapas de calor:** densidad + calidad de señal sobre mapa del campus
- **Anomalías:** APs con comportamiento inusual
- **Segmentación:** análisis por tipo de red (UAB vs eduroam), tipo de dispositivo

**Herramientas recomendadas:** Python, NetworkX, Plotly, Folium (mapas), scikit-learn

**Entregable:** Dashboard interactivo + informe técnico

---

### Nivel 3: AVANZADO (IA/ML/LLMs)

**Objetivo:** Sistemas inteligentes para optimización y recomendaciones

**Tareas sugeridas:**
- **Predicción de demanda:** ML para anticipar saturación de APs
- **Sistema de recomendaciones con LLM:** chatbot que responde preguntas sobre la infraestructura usando RAG
- **Detección de anomalías:** ML no supervisado para identificar problemas
- **Optimización:** algoritmos para redistribución de canales WiFi
- **Agentes IA:** sistema multi-agente para diagnóstico y resolución
- **Digital Twin:** simulador del campus WiFi en tiempo real

**Herramientas recomendadas:** PyTorch/TensorFlow, LangChain, Claude/GPT APIs, FastAPI

**Entregable:** Sistema funcional + demo + documentación técnica

---

## Datos Disponibles

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

## Geolocalización de APs

**Estado:** En proceso (pendiente de recibir desde GIS)

Se proporcionarán coordenadas geográficas de los APs para permitir visualizaciones en mapas del campus.

---

## Starter Kit

En la carpeta `starter_kits/` encontrarás:

- `01_rookie_basic_analysis.ipynb`: Notebook con carga de datos y visualizaciones básicas
- `utils/`: Funciones auxiliares para cargar y procesar datos

---

## Instalación y Uso

### Requisitos

```bash
python >= 3.8
pandas
matplotlib
seaborn
jupyter
```

### Instalación

```bash
# Clonar o descargar el repositorio
git clone <repo-url>
cd dtic-wifi-analysis

# Instalar dependencias
pip install -r requirements.txt

# Lanzar Jupyter
jupyter notebook starter_kits/
```

---

## Criterios de Evaluación

### Nivel Rookie (30%)
- **Corrección técnica (40%):** Análisis correcto de los datos
- **Visualizaciones (30%):** Claridad y efectividad de gráficos
- **Insights (20%):** Descubrimientos interesantes
- **Presentación (10%):** Comunicación de resultados

### Nivel Intermedio (35%)
- **Profundidad técnica (35%):** Complejidad del análisis
- **Innovación (25%):** Enfoques originales
- **Aplicabilidad (25%):** Utilidad para DTIC
- **Visualizaciones (15%):** Dashboards interactivos

### Nivel Avanzado (35%)
- **Innovación técnica (30%):** Uso no trivial de ML/LLMs/Agents
- **Aplicabilidad real (25%):** ¿Lo usaría DTIC en producción?
- **Complejidad (20%):** Integración de múltiples componentes
- **Escalabilidad (15%):** ¿Funciona con el dataset completo?
- **Demo (10%):** Presentación convincente

---

## Restricciones de Uso

- **Solo para fines educativos e investigación** durante el hackathon
- **No redistribuir** el dataset fuera del evento
- **No intentar** revertir la anonimización (violación de privacidad)
- Los datos se **eliminarán después del hackathon** (puedes conservar agregados anonimizados)

---

## Recursos Adicionales

### Documentación WiFi
- [Aruba Central API](https://developer.arubanetworks.com/)
- [802.11 Standards](https://en.wikipedia.org/wiki/IEEE_802.11)
- [WiFi Signal Strength Guide](https://www.metageek.com/training/resources/wifi-signal-strength-basics/)

### Análisis de Datos
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NetworkX](https://networkx.org/) - Para análisis de grafos/movilidad
- [Folium](https://python-visualization.github.io/folium/) - Mapas interactivos

### Machine Learning
- [scikit-learn](https://scikit-learn.org/)
- [LangChain](https://www.langchain.com/) - Para integración con LLMs
- [Anthropic Claude API](https://docs.anthropic.com/)

---

## Contacto y Soporte

**Durante el hackathon:**
- Busca a los mentores de DTIC en el evento
- Preguntas técnicas: albert.gil.lopez@uab.cat

---

## Licencia

El código de los scripts de procesamiento está bajo licencia MIT.
Los datos son propiedad de la UAB y solo para uso educativo durante el evento.

