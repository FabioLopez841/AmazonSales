import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Relación entre Rating y Precio con Descuento")

# Cargar datos
df = pd.read_csv("amazon.csv")

# Limpiar y convertir a numérico
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df = df.dropna(subset=['discounted_price', 'rating'])

# Crear bins para precio con descuento
bins = [0, 50, 100, 200, 300, 500, 1000, df['discounted_price'].max()]
labels = ['0-50', '51-100', '101-200', '201-300', '301-500', '501-1000', '1000+']
df['price_range'] = pd.cut(df['discounted_price'], bins=bins, labels=labels, include_lowest=True)

# Para facilitar, redondeamos rating a entero para agrupar
df['rating_int'] = df['rating'].round(0).astype(int)

# Contar cantidad de productos por rango de precio y rating
counts = df.groupby(['price_range', 'rating_int']).size().reset_index(name='count')

# Graficar histograma apilado de rating por rango de precio
fig = px.bar(counts, x='price_range', y='count', color='rating_int',
             labels={'price_range': 'Rango Precio con Descuento', 'count': 'Cantidad de Productos', 'rating_int': 'Rating'},
             title='Distribución de Rating según Precio con Descuento',
             barmode='stack')

fig.update_layout(xaxis_title="Rango de Precio con Descuento", yaxis_title="Cantidad de Productos")

st.plotly_chart(fig)
