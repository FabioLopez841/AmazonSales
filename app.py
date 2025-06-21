import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("amazon.csv")  # Cambia esto al nombre real del archivo

st.title("Análisis de Productos y Descuentos")

# Limpiar datos
df = df.dropna(subset=['category', 'rating_count', 'discount_percentage'])

# Convertir texto a minúsculas para evitar problemas de coincidencia
df['category'] = df['category'].str.lower()

# --- 1. TOP 10 Productos Más Vendidos en Hogar y Tecnología ---
st.header("Top 10 Productos Más Vendidos - Hogar y Tecnología")

# Filtrar categorías
mask = df['category'].str.contains('hogar') | df['category'].str.contains('tecnolog')
top_cat = df[mask]

# Ordenar por rating_count (suponiendo que representa ventas)
top_cat_sorted = top_cat.sort_values(by='rating_count', ascending=False)

# Tomar top 10
top10_cat = top_cat_sorted.head(10)

# Gráfica
fig1 = px.bar(top10_cat, x='product_name', y='rating_count',
              color='category',
              title="Top 10 Productos Más Vendidos (Hogar y Tecnología)",
              labels={'rating_count': 'Cantidad de Reseñas'},
              text='rating_count')
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1)


# --- 2. TOP 10 Productos Más Vendidos con Descuento ---
st.header("Top 10 Productos Más Vendidos con Descuento")

# Considerar solo productos con algún descuento (> 0%)
discounted_df = df[df['discount_percentage'] > 0]

# Ordenar por rating_count
top_discounted = discounted_df.sort_values(by='rating_count', ascending=False).head(10)

# Gráfica
fig2 = px.bar(top_discounted, x='product_name', y='rating_count',
              color='discount_percentage',
              title="Top 10 Productos Más Vendidos con Descuento",
              labels={'rating_count': 'Cantidad de Reseñas', 'discount_percentage': '% Descuento'},
              text='discount_percentage')
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2)
