# Dashboard de ventas de cafetería

Dashboard interactivo para explorar transacciones de una cafetería, resumir indicadores comerciales y analizar tendencias de venta a partir de un archivo CSV.

## Funcionalidades

- Filtrado por ubicación y método de pago.
- Indicadores de ventas totales, ticket promedio, transacciones y producto popular.
- Análisis temporal por año, trimestre, mes y día.
- Comparación de productos, ubicaciones y métodos de pago.
- Limpieza de datos, tratamiento de valores faltantes e inspección de correlaciones.

## Tecnologías

Python, Streamlit, Pandas, NumPy, Matplotlib y Seaborn.

## Estructura

```text
.
├── app.py
├── data/
│   └── ventas_cafeteria.csv
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`.

## Despliegue en Streamlit Community Cloud

1. Sube este proyecto a un repositorio de GitHub.
2. En Streamlit Community Cloud, crea una aplicación y selecciona ese repositorio y la rama que usarás.
3. Indica `app.py` como archivo principal y despliega.

Las dependencias se instalan desde `requirements.txt`; el dataset incluido se carga desde `data/ventas_cafeteria.csv`. Antes de hacer público el repositorio, confirma que tienes permiso para compartir el contenido del CSV.