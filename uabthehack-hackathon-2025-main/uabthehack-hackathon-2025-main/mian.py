from pathlib import Path
import json
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter
from tqdm import tqdm
import matplotlib.cm as cm

# =========================================================
# Función para mapear el nombre de un punto de acceso (AP)
# a su edificio correspondiente
# =========================================================
def ap_to_building(ap_name):
    match = re.match(r'AP-([A-Z]+)', ap_name)
    if match:
        return match.group(1)
    return ap_name

# =========================================================
# Funciones auxiliares para cargar los JSON de clientes
# =========================================================
def extract_timestamp_from_filename(filename):
    # Extrae la marca de tiempo (timestamp) del nombre del archivo
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\+\d{2}_\d{2})', filename)
    if match:
        return match.group(1).replace('_', ':')
    return None

def load_all_json_files(directory, pattern):
    # Carga todos los archivos JSON de un directorio siguiendo un patrón
    files = list(Path(directory).glob(pattern))
    print(f"Encontrados {len(files)} archivos")
    all_data = []
    for file in tqdm(files):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                timestamp = extract_timestamp_from_filename(file.name)
                for record in data:
                    record['_file_timestamp'] = timestamp
                all_data.extend(data)
        except Exception as e:
            print(f"Error cargando {file}: {e}")
    return pd.DataFrame(all_data)

# =========================================================
# Cargar y ordenar los datos
# =========================================================
base_dir = Path(__file__).parent / "data"
df_clients_all = load_all_json_files(base_dir, 'client-info-*.json')

df_clients_all['_file_timestamp'] = pd.to_datetime(df_clients_all['_file_timestamp'])
df_clients_all = df_clients_all.sort_values('_file_timestamp')

df_clients_all['hour'] = df_clients_all['_file_timestamp'].dt.hour
df_clients_all['weekday'] = df_clients_all['_file_timestamp'].dt.weekday

# =========================================================
# Detección de movimientos entre timestamps consecutivos
# =========================================================
timestamps = sorted(df_clients_all['_file_timestamp'].unique())
all_movements = []

for i in range(len(timestamps)-1):
    t1, t2 = timestamps[i], timestamps[i+1]
    
    # Filtramos los clientes conectados en ambos instantes
    t1_clients = df_clients_all[df_clients_all['_file_timestamp'] == t1]
    t2_clients = df_clients_all[df_clients_all['_file_timestamp'] == t2]
    
    # Combinamos los datos por dirección MAC
    movements = t1_clients.merge(
        t2_clients,
        on='macaddr',
        suffixes=('_t1', '_t2')
    )
    
    # Nos quedamos solo con los que cambiaron de AP (movimiento real)
    moved = movements[movements['associated_device_name_t1'] != movements['associated_device_name_t2']]
    
    # Registramos cada movimiento
    for _, row in moved.iterrows():
        all_movements.append({
            'macaddr': row['macaddr'],
            'timestamp_origen': t1,
            'ap_origen': row['associated_device_name_t1'],
            'timestamp_destino': t2,
            'ap_destino': row['associated_device_name_t2']
        })

df_movements = pd.DataFrame(all_movements)

# =========================================================
# Agrupar los APs por edificio (usando la función anterior)
# =========================================================
df_movements['ap_origen_group'] = df_movements['ap_origen'].apply(ap_to_building)
df_movements['ap_destino_group'] = df_movements['ap_destino'].apply(ap_to_building)

# =========================================================
# Filtrar edificios de interés
# =========================================================
top_buildings = ['CIEN', 'VET', 'ETSE', 'LLET', 'POL',
                 'ECON', 'MED', 'CEDU', 'CCOM', 'FTI', 'DRET']

df_movements_subset = df_movements[
    df_movements['ap_origen_group'].isin(top_buildings) &
    df_movements['ap_destino_group'].isin(top_buildings) &
    (df_movements['ap_origen_group'] != df_movements['ap_destino_group'])
]

# =========================================================
# Precalcular los costes de aristas y conteos por nodo
# =========================================================
timestamps_subset = sorted(df_movements_subset['timestamp_destino'].unique())
nodes = list(set(df_movements_subset['ap_origen_group']) | set(df_movements_subset['ap_destino_group']))

edge_data_dict = {}
node_counts_dict = {}

for t_idx in range(len(timestamps_subset)-1):
    t1, t2 = timestamps_subset[t_idx], timestamps_subset[t_idx+1]
    
    # Movimientos entre dos timestamps consecutivos
    df_frame = df_movements_subset[
        (df_movements_subset['timestamp_origen'] == t1) &
        (df_movements_subset['timestamp_destino'] == t2)
    ]
    
    # Coste por arista = nº de personas que se mueven de un edificio a otro
    edge_costs = df_frame.groupby(['ap_origen_group', 'ap_destino_group'])['macaddr'].nunique().to_dict()
    edge_data_dict[(t1, t2)] = edge_costs
    
    # Nº de personas en cada edificio en el segundo timestamp
    df_t2 = df_movements_subset[df_movements_subset['timestamp_destino'] == t2]
    node_counts_dict[t2] = df_t2.groupby('ap_destino_group')['macaddr'].nunique().to_dict()

# =========================================================
# Visualización interactiva con slider temporal
# =========================================================
pos = nx.spring_layout(nodes, seed=42)
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.15)

# Slider inferior para moverse entre frames
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Frame', 0, len(timestamps_subset)-2, valinit=0, valstep=1)

def update(frame):
    ax.clear()
    if frame >= len(timestamps_subset) - 1:
        return
    
    t1, t2 = timestamps_subset[frame], timestamps_subset[frame+1]
    edge_costs = edge_data_dict.get((t1, t2), {})
    node_counts = node_counts_dict.get(t2, {})
    total_personas = sum(node_counts.values())
    
    # Construcción del grafo dirigido
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    for (u, v), cost in edge_costs.items():
        G.add_edge(u, v, cost=cost)
    
    # Tamaño de nodo proporcional al número de personas
    node_sizes = [800 + node_counts.get(n, 0) * 50 for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='skyblue', node_size=node_sizes)
    
    # Normalizar colores según intensidad del flujo
    max_cost = max((d['cost'] for _, _, d in G.edges(data=True)), default=1)
    
    for u, v, d in G.edges(data=True):
        rad = 0.2 if (v, u) in G.edges() else 0.0
        width = max(1, d['cost'] / 3.5)
        color = cm.Reds(d['cost'] / max_cost)
        
        # Aristas muy gruesas se dibujan en negro
        if width >= 13:
            width = 13
            color = 'black'
        
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)], ax=ax,
            width=width, edge_color=color,
            arrowstyle='-|>', arrowsize=40,
            connectionstyle=f'arc3,rad={rad}'
        )
    
    # Etiquetas de nodos: edificio + nº de personas
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels={n: f"{n}\n{node_counts.get(n, 0)}" for n in G.nodes()},
        font_size=10
    )
    
    # Etiquetas de aristas: nº de personas que se mueven (coste)
    for u, v, d in G.edges(data=True):
        label_pos = 0.6 if (v, u) in G.edges() else 0.5
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax,
            edge_labels={(u, v): f"{d['cost']}"},
            font_size=8, label_pos=label_pos
        )
    
    # Título con intervalo temporal y total de personas
    ax.set_title(f"Movimientos entre edificios ({t1} → {t2}) | Total: {total_personas} personas")
    ax.axis('off')
    fig.canvas.draw_idle()

# Inicializar gráfico
slider.on_changed(update)
update(0)
plt.show()
