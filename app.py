from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Dashboard de Ventas - Cafetería",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --coffee-green: #174b3b;
        --coffee-leaf: #4f8b63;
        --coffee-citrus: #d89b32;
        --coffee-coral: #cb684d;
        --coffee-ink: #26352f;
        --coffee-muted: #65736c;
        --coffee-paper: #f4f7f3;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stAppDeployButton"] {
        display: none;
    }

    .dashboard-hero {
        position: relative;
        overflow: hidden;
        margin: 0 0 1.5rem;
        padding: 2rem 2.25rem;
        border-radius: 8px;
        border-left: 7px solid var(--coffee-citrus);
        color: #fff;
        background: var(--coffee-green);
    }

    .dashboard-hero::after {
        content: "";
        position: absolute;
        top: -3.5rem;
        right: 2.5rem;
        width: 11rem;
        height: 11rem;
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 50%;
        box-shadow: 0 0 0 1.5rem rgba(255, 255, 255, 0.04), 0 0 0 3rem rgba(255, 255, 255, 0.025);
    }

    .hero-kicker {
        margin-bottom: 0.55rem;
        color: #d8bd78;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .dashboard-hero h1 {
        position: relative;
        z-index: 1;
        margin: 0;
        color: #fff;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2rem;
        font-weight: 600;
        line-height: 1.2;
    }

    .dashboard-hero p {
        position: relative;
        z-index: 1;
        max-width: 44rem;
        margin: 0.65rem 0 0;
        color: #dce9e1;
        font-size: 0.98rem;
        line-height: 1.55;
    }

    div[data-testid="column"] [data-testid="stMetric"] {
        min-height: 7rem;
        padding: 1rem 1.15rem;
        border: 1px solid #e2e9e3;
        border-top: 4px solid var(--coffee-leaf);
        border-radius: 7px;
        background: #fff;
        box-shadow: 0 3px 12px rgba(23, 75, 59, 0.055);
    }

    div[data-testid="column"]:nth-child(2) [data-testid="stMetric"] {
        border-top-color: var(--coffee-citrus);
    }

    div[data-testid="column"]:nth-child(3) [data-testid="stMetric"] {
        border-top-color: #4c91a0;
    }

    div[data-testid="column"]:nth-child(4) [data-testid="stMetric"] {
        border-top-color: var(--coffee-coral);
    }

    [data-testid="stMetricLabel"] p {
        color: var(--coffee-muted);
        font-size: 0.82rem;
        font-weight: 650;
    }

    [data-testid="stMetricValue"] {
        color: var(--coffee-ink);
        font-size: 1.55rem;
        font-weight: 700;
    }

    [data-baseweb="tab-list"] {
        gap: 0.4rem;
        border-bottom: 1px solid #dfe7e0;
    }

    [data-baseweb="tab"] {
        min-height: 3rem;
        padding: 0.65rem 1rem;
        border-radius: 6px 6px 0 0;
        color: var(--coffee-muted);
        font-weight: 650;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        color: var(--coffee-green);
        background: #eaf1eb;
    }

    [data-testid="stSidebar"] {
        background: var(--coffee-paper);
    }

    [data-testid="stSidebar"] h1 {
        color: var(--coffee-green);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.55rem;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: var(--coffee-ink);
        font-weight: 650;
    }

    .record-count {
        margin-top: 1.25rem;
        padding: 1rem 1.1rem;
        border: 1px solid #dce7dd;
        border-left: 4px solid var(--coffee-leaf);
        border-radius: 6px;
        background: #fff;
    }

    .record-count-label,
    .record-count-detail {
        display: block;
        color: var(--coffee-muted);
        font-size: 0.78rem;
    }

    .record-count-value {
        display: block;
        margin: 0.2rem 0;
        color: var(--coffee-green);
        font-size: 1.5rem;
        font-weight: 750;
        line-height: 1.2;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-top: 1rem;
        }

        .dashboard-hero {
            padding: 1.5rem 1.25rem;
        }

        .dashboard-hero h1 {
            font-size: 1.6rem;
        }

        [data-baseweb="tab-list"] {
            gap: 0.15rem;
        }

        [data-baseweb="tab"] {
            padding: 0.55rem 0.5rem;
            font-size: 0.78rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Estilos visuales para Seaborn/Matplotlib
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'figure.autolayout': True})


def etiquetar_barras(ax, formato="{:,.0f}", rotacion=0, tamano=8):
    for contenedor in ax.containers:
        ax.bar_label(
            contenedor,
            fmt=formato,
            padding=3,
            fontsize=tamano,
            rotation=rotacion
        )


# -------------------------------------------------------------
# 1. CARGA Y LIMPIEZA DE DATOS CON CACHÉ
# -------------------------------------------------------------
@st.cache_data
def cargar_y_limpiar_datos():
    archivo_csv = Path(__file__).resolve().parent / 'data' / 'ventas_cafeteria.csv'
    if not archivo_csv.is_file():
        return None, None

    ventas_original = pd.read_csv(archivo_csv)
    ventas = ventas_original.copy()

    # Eliminación de filas completamente vacías
    ventas = ventas.dropna(axis=0, how='all')

    # Conversión a tipos de datos numéricos
    ventas['Total_Gastado'] = pd.to_numeric(ventas['Total_Gastado'], errors='coerce')
    ventas['Cantidad'] = pd.to_numeric(ventas['Cantidad'], errors='coerce')
    ventas['Precio_Unitario'] = pd.to_numeric(ventas['Precio_Unitario'], errors='coerce')

    # Conversión de Fecha a datetime
    ventas['Fecha_Transaccion'] = pd.to_datetime(ventas['Fecha_Transaccion'], errors='coerce')

    # Estandarización de errores a NaN
    valores_sucios = ['ERROR', 'DESCONOCIDO', 'N/A', 'none']
    ventas.replace(valores_sucios, np.nan, inplace=True)

    # Imputación de Metodo_Pago
    ventas['Metodo_Pago'] = ventas['Metodo_Pago'].fillna('Desconocido')

    # Imputación cruzada calculada de nulos:
    # 1. Total_Gastado = Cantidad * Precio_Unitario
    cond_total = ventas['Total_Gastado'].isna() & ventas['Cantidad'].notna() & ventas['Precio_Unitario'].notna()
    ventas.loc[cond_total, 'Total_Gastado'] = ventas['Cantidad'] * ventas['Precio_Unitario']

    # 2. Cantidad = Total_Gastado / Precio_Unitario
    cond_cant = ventas['Cantidad'].isna() & ventas['Total_Gastado'].notna() & ventas['Precio_Unitario'].notna() & (ventas['Precio_Unitario'] != 0)
    ventas.loc[cond_cant, 'Cantidad'] = ventas['Total_Gastado'] / ventas['Precio_Unitario']

    # 3. Precio_Unitario = Total_Gastado / Cantidad
    cond_precio = ventas['Precio_Unitario'].isna() & ventas['Total_Gastado'].notna() & ventas['Cantidad'].notna() & (ventas['Cantidad'] != 0)
    ventas.loc[cond_precio, 'Precio_Unitario'] = ventas['Total_Gastado'] / ventas['Cantidad']

    # Creación de columnas temporales
    ventas['Anio'] = ventas['Fecha_Transaccion'].dt.year
    ventas['Mes'] = ventas['Fecha_Transaccion'].dt.month
    ventas['Dia'] = ventas['Fecha_Transaccion'].dt.day
    ventas['Trimestre'] = ventas['Fecha_Transaccion'].dt.quarter
    ventas['Hora'] = ventas['Fecha_Transaccion'].dt.hour
    ventas['Pais'] = 'Colombia'

    return ventas_original, ventas

# Cargar datos
ventas_original, ventas = cargar_y_limpiar_datos()

if ventas is None:
    st.error("⚠️ No se encontró el archivo CSV en el directorio del proyecto.")
    st.stop()

# -------------------------------------------------------------
# 2. SIDEBAR - FILTROS DINÁMICOS
# -------------------------------------------------------------
st.sidebar.markdown("<h1>☕ Filtros de Análisis</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Personaliza las métricas y gráficos del panel:")

# Filtro de Ubicación
ubicaciones_disp = ['Todas'] + sorted([u for u in ventas['Ubicacion'].dropna().unique() if str(u).strip() != ''])
ubicacion_seleccionada = st.sidebar.selectbox("Ubicación:", ubicaciones_disp)

# Filtro de Método de Pago
metodos_disp = ['Todos'] + sorted(list(ventas['Metodo_Pago'].unique()))
metodo_seleccionado = st.sidebar.selectbox("Método de Pago:", metodos_disp)

# Aplicación de filtros
datos_filtrados = ventas.copy()
if ubicacion_seleccionada != 'Todas':
    datos_filtrados = datos_filtrados[datos_filtrados['Ubicacion'] == ubicacion_seleccionada]

if metodo_seleccionado != 'Todos':
    datos_filtrados = datos_filtrados[datos_filtrados['Metodo_Pago'] == metodo_seleccionado]

st.sidebar.divider()
st.sidebar.markdown(
    f"""
    <div class="record-count">
        <span class="record-count-label">Registros analizados</span>
        <strong class="record-count-value">{len(datos_filtrados):,}</strong>
        <span class="record-count-detail">de {len(ventas):,} registros totales</span>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# 3. ENCABEZADO Y KPIS PRINCIPALES
# -------------------------------------------------------------
st.markdown(
    """
    <header class="dashboard-hero">
        <div class="hero-kicker">Cafetería · Resumen comercial</div>
        <h1>📊 Analítica de Ventas</h1>
        <p>Transacciones, comportamiento de consumo y métricas clave del negocio.</p>
    </header>
    """,
    unsafe_allow_html=True
)

total_ventas = datos_filtrados['Total_Gastado'].sum()
ticket_promedio = datos_filtrados['Total_Gastado'].mean()
total_transacciones = len(datos_filtrados)
producto_top = datos_filtrados['Producto'].value_counts().idxmax() if not datos_filtrados['Producto'].dropna().empty else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Ventas Totales", f"${total_ventas:,.2f}")
kpi2.metric("💳 Ticket Promedio", f"${ticket_promedio:.2f}")
kpi3.metric("🧾 Total Transacciones", f"{total_transacciones:,}")
kpi4.metric("⭐ Producto Más Popular", str(producto_top))

st.divider()

# -------------------------------------------------------------
# 4. PESTAÑAS PRINCIPALES DEL DASHBOARD
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Tendencia Temporal",
    "🥐 Productos y Ubicación",
    "💳 Métodos de Pago y Canales",
    "🔍 Limpieza y Correlación"
])

# =============================================================
# PESTAÑA 1: TENDENCIA TEMPORAL
# =============================================================
with tab1:
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.subheader("Ventas Totales por Año")
        ventas_por_anio = datos_filtrados.groupby('Anio')['Total_Gastado'].sum().reset_index()
        fig_anio, ax_anio = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Anio', y='Total_Gastado', hue='Anio', data=ventas_por_anio, palette='viridis', legend=False, ax=ax_anio)
        ax_anio.set_title("Ventas por Año")
        ax_anio.set_xlabel("Año")
        ax_anio.set_ylabel("Total Gastado ($)")
        etiquetar_barras(ax_anio, formato="${:,.0f}")
        st.pyplot(fig_anio)
        plt.close(fig_anio)

    with col_t2:
        st.subheader("Ventas Totales por Trimestre")
        ventas_trimestre = datos_filtrados.groupby('Trimestre')['Total_Gastado'].sum().reset_index()
        fig_trim, ax_trim = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Trimestre', y='Total_Gastado', hue='Trimestre', data=ventas_trimestre, palette='coolwarm', legend=False, ax=ax_trim)
        ax_trim.set_title("Ventas por Trimestre")
        ax_trim.set_xlabel("Trimestre (Q)")
        ax_trim.set_ylabel("Total Gastado ($)")
        etiquetar_barras(ax_trim, formato="${:,.0f}")
        st.pyplot(fig_trim)
        plt.close(fig_trim)

    st.subheader("Evolución de Ventas Mensuales (2023)")
    ventas_anuales_mensuales = datos_filtrados.groupby(['Anio', 'Mes'])['Total_Gastado'].sum().reset_index()
    ventas_2023 = ventas_anuales_mensuales[ventas_anuales_mensuales['Anio'] == 2023.0]
    fig_mes, ax_mes = plt.subplots(figsize=(13, 3.6))
    sns.lineplot(x='Mes', y='Total_Gastado', data=ventas_2023, marker='o', color='#2b5c8f', linewidth=2.2, ax=ax_mes)
    ax_mes.set_title("Ventas Mes a Mes (Año 2023)")
    ax_mes.set_xlabel("Mes")
    ax_mes.set_ylabel("Total Gastado ($)")
    ax_mes.set_xticks(range(1, 13))
    ax_mes.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    for _, fila in ventas_2023.iterrows():
        ax_mes.annotate(
            f"${fila['Total_Gastado']:,.0f}",
            (fila['Mes'], fila['Total_Gastado']),
            xytext=(0, 7),
            textcoords='offset points',
            ha='center',
            fontsize=10,
            color="#0c0c0c"
        )
    st.pyplot(fig_mes)
    plt.close(fig_mes)

    st.subheader("📅 Ventas por Día del Mes")
    ventas_por_dia = datos_filtrados.groupby('Dia')['Total_Gastado'].sum().reset_index().dropna()
    if not ventas_por_dia.empty:
        ventas_por_dia['Dia'] = ventas_por_dia['Dia'].astype(int)
        ventas_por_dia = ventas_por_dia.sort_values('Dia')

        fig_dia, ax_dia = plt.subplots(figsize=(14, 4.8))
        sns.barplot(
            x='Dia', 
            y='Total_Gastado', 
            data=ventas_por_dia, 
            color='#3470a3',
            edgecolor='#1d456b',
            linewidth=0.8,
            ax=ax_dia
        )
        ax_dia.set_title("Ventas Totales Registradas por Día del Mes (1 al 31)", fontsize=13, fontweight='bold', pad=12)
        ax_dia.set_xlabel("Día del Mes", fontsize=11, fontweight='semibold')
        ax_dia.set_ylabel("Total Gastado ($)", fontsize=11, fontweight='semibold')
        ax_dia.set_ylim(0, ventas_por_dia['Total_Gastado'].max() * 1.2)
        ax_dia.tick_params(axis='x', rotation=0, labelsize=10)
        ax_dia.grid(axis='y', linestyle='--', alpha=0.5)

        etiquetar_barras(ax_dia, formato="${:,.0f}", rotacion=90, tamano=8)
        st.pyplot(fig_dia)
        plt.close(fig_dia)

# =============================================================
# PESTAÑA 2: PRODUCTOS Y UBICACIÓN
# =============================================================
with tab2:
    st.subheader("Top 10 Productos Más Vendidos por Ubicación")
    prod_ubi = datos_filtrados.groupby(['Producto', 'Ubicacion'])['Cantidad'].sum().reset_index()
    prod_ubi_top = prod_ubi.sort_values(by='Cantidad', ascending=False).head(10)

    fig_pu, ax_pu = plt.subplots(figsize=(10, 4.5))
    sns.barplot(x='Cantidad', y='Producto', hue='Ubicacion', data=prod_ubi_top, palette='muted', ax=ax_pu)
    ax_pu.set_title("Top 10 Productos por Cantidad y Ubicación")
    ax_pu.set_xlabel("Cantidad Vendida")
    ax_pu.set_ylabel("Producto")
    etiquetar_barras(ax_pu, tamano=7)
    st.pyplot(fig_pu)
    plt.close(fig_pu)

    col_p1, col_p2 = st.columns(2)
    productos_vendidos = datos_filtrados['Producto'].value_counts().reset_index()
    productos_vendidos.columns = ['Producto', 'Cantidad_Vendida']

    with col_p1:
        st.subheader("Top 5 Productos Más Vendidos")
        top_5 = productos_vendidos.head(5)
        fig_t5, ax_t5 = plt.subplots(figsize=(6, 3.8))
        sns.barplot(x='Cantidad_Vendida', y='Producto', hue='Producto', data=top_5, palette='cubehelix', legend=False, ax=ax_t5)
        ax_t5.set_xlabel("Unidades Vendidas")
        etiquetar_barras(ax_t5)
        st.pyplot(fig_t5)
        plt.close(fig_t5)

    with col_p2:
        st.subheader("Productos Menos Vendidos")
        least_prod = productos_vendidos.tail(5)
        fig_lp, ax_lp = plt.subplots(figsize=(6, 3.8))
        sns.barplot(x='Cantidad_Vendida', y='Producto', hue='Producto', data=least_prod, palette='viridis', legend=False, ax=ax_lp)
        ax_lp.set_xlabel("Unidades Vendidas")
        etiquetar_barras(ax_lp)
        st.pyplot(fig_lp)
        plt.close(fig_lp)

# =============================================================
# PESTAÑA 3: MÉTODOS DE PAGO Y CANALES
# =============================================================
with tab3:
    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.subheader("Distribución de Ventas por Método de Pago")
        ventas_metodo = datos_filtrados.groupby('Metodo_Pago')['Total_Gastado'].sum().reset_index()
        fig_mp, ax_mp = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Metodo_Pago', y='Total_Gastado', hue='Metodo_Pago', data=ventas_metodo, palette='viridis', legend=False, ax=ax_mp)
        ax_mp.set_title("Ventas por Método de Pago")
        ax_mp.set_xlabel("Método de Pago")
        ax_mp.set_ylabel("Total Gastado ($)")
        ax_mp.tick_params(axis='x', rotation=30)
        etiquetar_barras(ax_mp, formato="${:,.0f}")
        st.pyplot(fig_mp)
        plt.close(fig_mp)

    with col_m2:
        st.subheader("Distribución de Ventas por Ubicación")
        ventas_ubi = datos_filtrados.groupby('Ubicacion')['Total_Gastado'].sum().reset_index()
        fig_ub, ax_ub = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Ubicacion', y='Total_Gastado', hue='Ubicacion', data=ventas_ubi, palette='crest', legend=False, ax=ax_ub)
        ax_ub.set_title("Ventas por Ubicación")
        ax_ub.set_xlabel("Ubicación")
        ax_ub.set_ylabel("Total Gastado ($)")
        ax_ub.tick_params(axis='x', rotation=30)
        etiquetar_barras(ax_ub, formato="${:,.0f}")
        st.pyplot(fig_ub)
        plt.close(fig_ub)

# =============================================================
# PESTAÑA 4: LIMPIEZA Y CORRELACIÓN
# =============================================================
with tab4:
    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.subheader("Matriz de Correlación Numérica")
        columnas_numericas = datos_filtrados.select_dtypes(include=[np.number])
        matriz_corr = columnas_numericas.corr()
        fig_corr, ax_corr = plt.subplots(figsize=(6.5, 5))
        sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5, ax=ax_corr)
        ax_corr.tick_params(axis='x', rotation=45)
        ax_corr.tick_params(axis='y', rotation=0)
        st.pyplot(fig_corr)
        plt.close(fig_corr)

    with col_c2:
        st.subheader("Resumen de Calidad del Dataset")
        st.write("**Valores nulos en datos originales vs limpios:**")
        comp_df = pd.DataFrame({
            "Originales": ventas_original.isnull().sum(),
            "Tras Limpieza/Imputación": datos_filtrados[ventas_original.columns].isnull().sum()
        })
        st.dataframe(comp_df, use_container_width=True)

    st.subheader("Vista Previa de los Datos Procesados")
    st.dataframe(datos_filtrados.head(100), use_container_width=True)