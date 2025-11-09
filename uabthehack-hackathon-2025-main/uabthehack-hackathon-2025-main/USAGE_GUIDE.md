# Usage Guide - UAB WiFi Dataset

**Evento:** UAB THE HACK! 2025 (8-9 de noviembre)
**Challenge:** DTIC WiFi Network Analysis
**Nivel:** Todos los niveles (Rookie → Advanced)

---

## Tabla de Contenidos

1. [Quick Start](#quick-start)
2. [Estructura del Dataset](#estructura-del-dataset)
3. [Carga de Datos](#carga-de-datos)
4. [Análisis Básico (Nivel Rookie)](#análisis-básico-nivel-rookie)
5. [Tips y Trucos](#tips-y-trucos)
6. [Problemas Comunes](#problemas-comunes)
7. [Recursos](#recursos)

---

## Quick Start

### Instalación Rápida

```bash
# Clonar o descargar el dataset
cd dtic-wifi-analysis

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias básicas
pip install pandas matplotlib seaborn jupyter

# O instalar todo desde requirements.txt
pip install -r requirements.txt

# Lanzar Jupyter
jupyter notebook
```

### Primeros Pasos en 5 Minutos

```python
import json
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar un archivo de APs
with open('anonymized_data/AP-info-v2-2025-06-13T14_45_01+02_00-ANON.json', 'r') as f:
    aps = json.load(f)

# 2. Convertir a DataFrame
df_aps = pd.DataFrame(aps)

# 3. Ver las primeras filas
print(df_aps.head())

# 4. Estadísticas básicas
print(f"Total APs: {len(df_aps)}")
print(f"APs activos: {(df_aps['status'] == 'Up').sum()}")
print(f"Total dispositivos: {df_aps['client_count'].sum()}")

# 5. Visualización rápida
df_aps['client_count'].hist(bins=50)
plt.xlabel('Dispositivos por AP')
plt.ylabel('Frecuencia')
plt.title('Distribución de Carga en Access Points')
plt.show()
```

---

## Estructura del Dataset

### Archivos Disponibles

```
dtic-wifi-analysis/
├── README.md                      # Descripción general del challenge
├── DATA_DICTIONARY.md             # Diccionario de datos (este archivo es tu biblia!)
├── USAGE_GUIDE.md                 # Esta guía
├── requirements.txt               # Dependencias Python
│
├── anonymized_data/               # DATOS PRINCIPALES (copiar aquí desde Google Drive)
│   ├── AP-info-v2-[timestamp]-ANON.json       # 7.229 archivos (~10GB)
│   └── client-info-[timestamp]-ANON.json      # 3.205 archivos
│
├── anonymized_samples/            # Muestras para desarrollo rápido
│   ├── AP-info-v2-2025-06-13T14_45_01+02_00-ANON.json
│   └── client-info-2025-04-09T11_47_24+02_00-10487-ANON.json
│
├── starter_kits/                  # Notebooks de ejemplo
│   ├── 01_rookie_basic_analysis.ipynb
│   
│
└── utils/                         # Funciones auxiliares
    ├── data_loader.py             # Funciones para cargar datos eficientemente
```

### Nomenclatura de Archivos

#### Access Points
```
AP-info-v2-[TIMESTAMP].json

Ejemplos:
AP-info-v2-2025-04-05T10_00_01+02_00-ANON.json
             ↑                ↑
             fecha/hora       zona horaria
```

#### Clientes
```
client-info-[TIMESTAMP]-[COUNT].json

Ejemplos:
client-info-2025-04-09T11_47_24+02_00-10487-ANON.json
                                             ↑
                                             número de dispositivos
```

### Tamaño de Datos

| Tipo | Cantidad | Tamaño Total | Tamaño Promedio |
|------|----------|--------------|-----------------|
| APs | 7.229 archivos | ~10 GB | ~1.4 MB/archivo |
| Clientes | 3.205 archivos | ~15 GB | ~5 MB/archivo |
| **Total** | **10.434 archivos** | **~25 GB** | - |

---

## Carga de Datos

### Opción 1: Cargar un Solo Archivo (Desarrollo)

```python
import json
import pandas as pd

# Cargar APs
with open('anonymized_samples/AP-info-v2-2025-06-13T14_45_01+02_00-ANON.json', 'r', encoding='utf-8') as f:
    aps_data = json.load(f)

df_aps = pd.DataFrame(aps_data)

# Cargar Clientes
with open('anonymized_samples/client-info-2025-04-09T11_47_24+02_00-10487-ANON.json', 'r', encoding='utf-8') as f:
    clients_data = json.load(f)

df_clients = pd.DataFrame(clients_data)
```

### Opción 2: Cargar Múltiples Archivos (Análisis Completo)

```python
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm  # Para barra de progreso

def load_all_json_files(directory, pattern):
    """
    Carga todos los archivos JSON que coinciden con un patrón.

    Args:
        directory: Ruta al directorio
        pattern: Patrón glob (ej: "AP-info-v2-*.json")

    Returns:
        DataFrame combinado
    """
    files = list(Path(directory).glob(pattern))
    print(f"Encontrados {len(files)} archivos")

    all_data = []

    for file in tqdm(files):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Añadir timestamp del nombre del archivo
                timestamp = extract_timestamp_from_filename(file.name)

                for record in data:
                    record['_file_timestamp'] = timestamp

                all_data.extend(data)
        except Exception as e:
            print(f"Error cargando {file}: {e}")

    return pd.DataFrame(all_data)

def extract_timestamp_from_filename(filename):
    """
    Extrae el timestamp del nombre del archivo.

    Ejemplo:
    'AP-info-v2-2025-04-05T10_00_01+02_00-ANON.json'
    → '2025-04-05T10:00:01+02:00'
    """
    import re
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\+\d{2}_\d{2})', filename)
    if match:
        return match.group(1).replace('_', ':')
    return None

# Usar la función
df_aps_all = load_all_json_files('anonymized_data/', 'AP-info-v2-*-ANON.json')
df_clients_all = load_all_json_files('anonymized_data/', 'client-info-*-ANON.json')
```

### Opción 3: Cargar Selectivamente por Fecha/Hora

```python
from datetime import datetime, timedelta

def load_files_in_range(directory, pattern, start_date, end_date):
    """
    Carga archivos en un rango de fechas específico.

    Args:
        start_date: datetime object
        end_date: datetime object
    """
    files = Path(directory).glob(pattern)
    selected_files = []

    for file in files:
        timestamp_str = extract_timestamp_from_filename(file.name)
        if timestamp_str:
            file_date = datetime.fromisoformat(timestamp_str)
            if start_date <= file_date <= end_date:
                selected_files.append(file)

    print(f"Cargando {len(selected_files)} archivos entre {start_date} y {end_date}")

    # Cargar igual que antes...
    # (código similar a load_all_json_files)

# Ejemplo: Solo cargar datos de una semana
start = datetime(2025, 4, 10)
end = datetime(2025, 4, 17)
df_week = load_files_in_range('anonymized_data/', 'client-info-*.json', start, end)
```

### Opción 4: Sampling Aleatorio (Para Prototipado Rápido)

```python
import random

def load_random_sample(directory, pattern, n_files=10):
    """Carga N archivos aleatorios para desarrollo rápido."""
    files = list(Path(directory).glob(pattern))
    sample_files = random.sample(files, min(n_files, len(files)))

    print(f"Cargando muestra de {len(sample_files)} archivos")

    # Cargar igual que antes...

# Ejemplo: Cargar 20 archivos aleatorios
df_sample = load_random_sample('anonymized_data/', 'client-info-*.json', n_files=20)
```

---

## Análisis Básico (Nivel Rookie)

### 1. Exploración Inicial de Datos

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Cargar datos (usar Opción 1 para empezar)
df_aps = pd.read_json('anonymized_samples/AP-info-v2-2025-06-13T14_45_01+02_00-ANON.json')
df_clients = pd.read_json('anonymized_samples/client-info-2025-04-09T11_47_24+02_00-10487-ANON.json')

# Información general
print("=== ACCESS POINTS ===")
print(f"Total APs: {len(df_aps)}")
print(f"Columnas: {df_aps.columns.tolist()}")
print(df_aps.info())

print("\n=== CLIENTES ===")
print(f"Total clientes: {len(df_clients)}")
print(f"Columnas: {df_clients.columns.tolist()}")
print(df_clients.info())
```

### 2. Estadísticas Descriptivas

```python
# APs
print("=== Estadísticas de Access Points ===")
print(df_aps[['client_count', 'cpu_utilization', 'mem_free']].describe())

# Clientes
print("\n=== Estadísticas de Clientes ===")
print(df_clients[['signal_db', 'snr', 'speed', 'health']].describe())
```

### 3. Identificar Zonas Hotspot

```python
# Extraer edificio del nombre del AP
df_aps['building'] = df_aps['name'].str.extract(r'AP-([A-Z]+)\d+')[0]

# Agrupar por edificio
hotspots = df_aps.groupby('building').agg({
    'client_count': 'sum',
    'name': 'count'  # Número de APs por edificio
}).rename(columns={'name': 'num_aps'})

hotspots['avg_clients_per_ap'] = hotspots['client_count'] / hotspots['num_aps']
hotspots = hotspots.sort_values('client_count', ascending=False)

print("=== Top 10 Edificios con Más Dispositivos ===")
print(hotspots.head(10))

# Visualización
plt.figure(figsize=(14, 6))
hotspots.head(15)['client_count'].plot(kind='bar')
plt.title('Top 15 Edificios por Densidad de Dispositivos')
plt.xlabel('Edificio')
plt.ylabel('Total Dispositivos Conectados')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 4. Distribución de Calidad de Señal

```python
# Histograma de RSSI
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
df_clients['signal_db'].hist(bins=50, edgecolor='black')
plt.xlabel('RSSI (dBm)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Potencia de Señal')
plt.axvline(-70, color='red', linestyle='--', label='Umbral "débil"')
plt.axvline(-50, color='green', linestyle='--', label='Umbral "excelente"')
plt.legend()

plt.subplot(1, 2, 2)
df_clients['signal_strength'].value_counts().sort_index().plot(kind='bar')
plt.xlabel('Signal Strength (1-5)')
plt.ylabel('Número de Clientes')
plt.title('Distribución de Fuerza de Señal Simplificada')

plt.tight_layout()
plt.show()

# Porcentaje con señal pobre
poor_signal_pct = (df_clients['signal_db'] < -70).mean() * 100
print(f"Porcentaje de clientes con señal pobre (<-70 dBm): {poor_signal_pct:.1f}%")
```

### 5. Análisis de Bandas (2.4 GHz vs 5 GHz)

```python
# Distribución de clientes por banda
band_distribution = df_clients['band'].value_counts()

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
band_distribution.plot(kind='pie', autopct='%1.1f%%', labels=['5 GHz', '2.4 GHz'])
plt.title('Distribución de Clientes por Banda')
plt.ylabel('')

plt.subplot(1, 2, 2)
df_clients.boxplot(column='speed', by='band')
plt.xlabel('Banda (GHz)')
plt.ylabel('Velocidad (Mbps)')
plt.title('Velocidad por Banda')
plt.suptitle('')  # Quitar título automático

plt.tight_layout()
plt.show()

# Comparación de velocidad promedio
print("=== Velocidad Promedio por Banda ===")
print(df_clients.groupby('band')['speed'].agg(['mean', 'median', 'max']))
```

### 6. Tipos de Dispositivos

```python
# Top 10 fabricantes
top_manufacturers = df_clients['manufacturer'].value_counts().head(10)

plt.figure(figsize=(12, 6))
top_manufacturers.plot(kind='barh')
plt.title('Top 10 Fabricantes de Dispositivos')
plt.xlabel('Número de Dispositivos')
plt.ylabel('Fabricante')
plt.tight_layout()
plt.show()

# Sistemas operativos
os_distribution = df_clients['os_type'].value_counts()
print("=== Distribución de Sistemas Operativos ===")
print(os_distribution)

# Categorías de dispositivos
category_distribution = df_clients['client_category'].value_counts()
print("\n=== Categorías de Dispositivos ===")
print(category_distribution)
```

### 7. Red UAB vs eduroam

```python
network_stats = df_clients.groupby('network').agg({
    'macaddr': 'count',
    'signal_db': 'mean',
    'speed': 'mean',
    'health': 'mean'
}).rename(columns={'macaddr': 'num_clients'})

print("=== Comparación UAB vs eduroam ===")
print(network_stats)

# Visualización
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

network_stats['num_clients'].plot(kind='bar', ax=axes[0])
axes[0].set_title('Número de Clientes')
axes[0].set_ylabel('Clientes')

network_stats['signal_db'].plot(kind='bar', ax=axes[1])
axes[1].set_title('RSSI Promedio')
axes[1].set_ylabel('dBm')

network_stats['speed'].plot(kind='bar', ax=axes[2])
axes[2].set_title('Velocidad Promedio')
axes[2].set_ylabel('Mbps')

plt.tight_layout()
plt.show()
```

### 8. Rendimiento de Access Points

```python
# Top 10 APs con más clientes
top_aps = df_aps.nlargest(10, 'client_count')[['name', 'client_count', 'cpu_utilization', 'status']]
print("=== Top 10 APs con Más Clientes ===")
print(top_aps)

# APs con problemas
problematic_aps = df_aps[
    (df_aps['status'] == 'Down') |
    (df_aps['cpu_utilization'] > 80)
][['name', 'status', 'client_count', 'cpu_utilization']]

print("\n=== APs con Posibles Problemas ===")
print(problematic_aps)

# Scatter plot: carga vs CPU
plt.figure(figsize=(10, 6))
plt.scatter(df_aps['client_count'], df_aps['cpu_utilization'], alpha=0.5)
plt.xlabel('Número de Clientes')
plt.ylabel('CPU Utilization (%)')
plt.title('Relación entre Carga de Clientes y Uso de CPU')
plt.axhline(80, color='red', linestyle='--', label='Umbral crítico (80%)')
plt.legend()
plt.tight_layout()
plt.show()
```
---

## Tips y Trucos

### Optimización de Memoria

```python
# Cargar solo columnas necesarias
import json

def load_json_columns(file_path, columns):
    """Carga solo columnas específicas de un JSON."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Filtrar solo columnas requeridas
    filtered = []
    for record in data:
        filtered.append({k: record.get(k) for k in columns})

    return pd.DataFrame(filtered)

# Ejemplo
df_clients_light = load_json_columns(
    'anonymized_data/client-info-XXX.json',
    columns=['macaddr', 'associated_device_name', 'signal_db', 'speed']
)
```

### Procesamiento Paralelo

```python
from multiprocessing import Pool
from functools import partial

def process_file(file_path):
    """Procesa un archivo individual."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    # ... procesamiento ...
    return result

def parallel_load(directory, pattern, n_workers=4):
    """Carga archivos en paralelo."""
    files = list(Path(directory).glob(pattern))

    with Pool(processes=n_workers) as pool:
        results = pool.map(process_file, files)

    return pd.concat(results)

# Usar
df = parallel_load('anonymized_data/', 'client-info-*.json', n_workers=8)
```

### Exportar Resultados

```python
# CSV
df_results.to_csv('results/hotspots_analysis.csv', index=False)

# Excel con múltiples hojas
with pd.ExcelWriter('results/wifi_analysis.xlsx') as writer:
    hotspots.to_excel(writer, sheet_name='Hotspots')
    ap_quality.to_excel(writer, sheet_name='Quality')
    building_quality.to_excel(writer, sheet_name='Building Stats')

# JSON
df_results.to_json('results/analysis.json', orient='records', indent=2)

# Pickle (para guardar DataFrames grandes rápidamente)
df.to_pickle('processed_data/clients_all.pkl')
# Cargar: df = pd.read_pickle('processed_data/clients_all.pkl')
```

---

## Problemas Comunes

### 1. "FileNotFoundError: No such file or directory"

**Solución:**
```python
from pathlib import Path

# Verificar que el archivo existe
file_path = Path('anonymized_data/AP-info-v2-XXX.json')
if not file_path.exists():
    print(f"Archivo no encontrado: {file_path}")
    print("Archivos disponibles:")
    for f in Path('anonymized_data/').glob('*.json'):
        print(f" - {f.name}")
```

### 2. "JSONDecodeError: Expecting value"

**Solución:** Archivo JSON corrupto o vacío
```python
import json

try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error parseando {file_path}: {e}")
    # Intentar leer línea por línea para identificar el problema
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            try:
                json.loads(line)
            except:
                print(f"Error en línea {i}: {line[:100]}")
```

### 3. "MemoryError" al cargar todos los archivos

**Solución:** Cargar en chunks o usar Dask
```python
import dask.dataframe as dd

# Opción 1: Cargar solo muestra aleatoria
df_sample = load_random_sample('anonymized_data/', 'client-info-*.json', n_files=50)

# Opción 2: Usar Dask para procesamiento lazy
# (Requiere: pip install dask)
# ddf = dd.read_json('anonymized_data/client-info-*.json')
# result = ddf.groupby('associated_device_name').size().compute()
```

### 4. KeyError al acceder a campos

**Solución:** Algunos registros pueden no tener todos los campos
```python
# Opción 1: Usar .get() con default
ap_name = record.get('name', 'UNKNOWN')

# Opción 2: Verificar existencia
if 'down_reason' in record:
    print(f"AP caído: {record['down_reason']}")

# Opción 3: Usar fillna en DataFrame
df['down_reason'] = df['down_reason'].fillna('N/A')
```

### 5. Timestamps no se convierten correctamente

**Solución:** APs usan segundos, Clientes usan milisegundos
```python
# APs (segundos)
df_aps['datetime'] = pd.to_datetime(df_aps['last_modified'], unit='s')

# Clientes (milisegundos)
df_clients['datetime'] = pd.to_datetime(df_clients['last_connection_time'], unit='ms')
```

---

## Recursos

### Documentación del Proyecto

- `README.md` - Visión general y niveles del challenge
- `DATA_DICTIONARY.md` - Referencia completa de campos

### Bibliotecas Recomendadas

**Análisis Básico:**
- pandas: https://pandas.pydata.org/docs/
- matplotlib: https://matplotlib.org/stable/contents.html
- seaborn: https://seaborn.pydata.org/

**Análisis Avanzado:**
- NetworkX: https://networkx.org/ (grafos de movilidad)
- Plotly: https://plotly.com/python/ (dashboards interactivos)
- Folium: https://python-visualization.github.io/folium/ (mapas)

**Machine Learning:**
- scikit-learn: https://scikit-learn.org/stable/
- PyTorch: https://pytorch.org/docs/stable/index.html
- TensorFlow: https://www.tensorflow.org/api_docs

**LLMs y RAG:**
- LangChain: https://python.langchain.com/
- Anthropic Claude API: https://docs.anthropic.com/
- OpenAI API: https://platform.openai.com/docs/

### Tutoriales Externos

- **WiFi Signal Strength**: https://www.metageek.com/training/resources/wifi-signal-strength-basics/
- **NetworkX Tutorial**: https://networkx.org/documentation/stable/tutorial.html
- **Time Series con Pandas**: https://pandas.pydata.org/docs/user_guide/timeseries.html
- **RAG con LangChain**: https://python.langchain.com/docs/use_cases/question_answering/

### Contacto

**Durante el hackathon:**
- Busca a los mentores de DTIC en el stand
- Preguntas técnicas: albert.gil.lopez@uab.cat

**Responsable técnico:**
- Gonçal Badenes Guia (goncal.badenes@uab.cat)

---

## Checklist para Empezar

- [ ] Instalar Python >= 3.8
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Descargar dataset completo desde One Drive
- [ ] Verificar que puedes cargar un archivo de muestra
- [ ] Leer `DATA_DICTIONARY.md` completo
- [ ] Explorar un notebook de `starter_kits/`
- [ ] Elegir tu nivel (Rookie / Intermedio / Avanzado)
- [ ] Formar equipo y definir objetivo
- [ ] Enjoy!

---

**Última actualización:** 8 de noviembre de 2025
**Versión:** 1.0

