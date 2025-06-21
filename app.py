import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Relación entre Rating y Precio con Descuento")

# Cargar datos
df = pd.read_csv("amazon.csv")

# Forzar tipos numéricos
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Eliminar filas con datos faltantes
df = df.dropna(subset=['discounted_price', 'rating'])

# Verificar valores válidos
if df.empty or df['discounted_price'].nunique() < 2:
    st.error("No hay suficientes datos válidos para graficar.")
else:
    # Definir automáticamente los bins con pandas cut (7 segmentos)
    df['price_range'] = pd.cut(df['discounted_price'], bins=7)

    # Agrupar rating redondeado para simplificar
    df['rating_int'] = df['rating'].round().astype(int)

    # Agrupar por rango de precio y rating
    counts = df.groupby(['price_range', 'rating_int']).size().reset_index(name='count')

    # Crear histograma de barras apiladas
    fig = px.bar(counts, x='price_range', y='count', color='rating_int',
                 labels={'price_range': 'Rango de Precio con Descuento', 'count': 'Cantidad de Productos', 'rating_int': 'Rating'},
                 title='Distribución de Rating por Precio con Descuento',
                 barmode='stack')

    fig.update_layout(xaxis_title="Rango de Precio con Descuento", yaxis_title="Cantidad de Productos")
    st.plotly_chart(fig)
