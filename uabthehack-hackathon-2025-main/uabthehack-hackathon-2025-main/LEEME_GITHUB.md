# UAB WiFi Dataset Analysis - Repositorio GitHub

Este es el repositorio oficial del reto **UAB WiFi Dataset Analysis** para el evento **UAB THE HACK! 2025**.

## Contenido del Repositorio

### Archivos Principales
- **README.md** - Descripción completa del reto, niveles y criterios de evaluación
- **USAGE_GUIDE.md** - Guía de uso detallada del dataset
- **requirements.txt** - Dependencias de Python necesarias

### Carpetas

#### `starter_kits/`
Notebooks de Jupyter para comenzar rápidamente en cada nivel:
- `01_rookie_basic_analysis.ipynb` - Análisis básico para nivel ROOKIE
- `utils/` - Funciones auxiliares de carga y procesamiento

#### `anonymized_data/`
Dataset completo anonimizado:
- `aps/` - ~2,300 archivos JSON con snapshots de Access Points
- `clients/` - ~3,200 archivos JSON con datos de dispositivos conectados

#### `samples/`
Archivos de ejemplo para exploración rápida sin cargar el dataset completo

#### `docs/`
Documentación técnica:
- `DATA_DICTIONARY.md` - Diccionario completo de campos y estructuras
- Guías de optimización y análisis

### Imágenes
- `logo-uab.png` - Logo de la UAB
- `logo-uab-the-hack.png` - Logo del evento
- `criteris-repte-dtic.jpg` - Criterios de evaluación del reto

## Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd [nombre-del-repositorio]
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Explorar los notebooks
```bash
jupyter notebook starter_kits/
```

## Datos del Evento

**Fecha:** 8-9 de noviembre de 2025
**Organizador:** Consell d'Estudiants d'Enginyeria - UAB
**Propuesto por:** DTIC (Serveis d'Informàtica UAB)

## Restricciones de Uso

⚠️ **IMPORTANTE:**
- Solo para fines educativos durante el hackathon
- NO redistribuir el dataset fuera del evento
- NO intentar revertir la anonimización
- Los datos deben eliminarse después del hackathon

## Soporte

Durante el hackathon, busca a los mentores de DTIC en el evento o contacta:
- **Soporte técnico:** albert.gil.lopez@uab.cat
