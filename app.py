import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard de Productos por Categoría")

# Cargar archivo CSV
df = pd.read_csv("amazon.csv")

# Forzar columnas numéricas
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Limpiar datos con valores faltantes en columnas importantes
df = df.dropna(subset=['category', 'rating_count', 'actual_price', 'discounted_price', 'discount_percentage', 'rating'])

df['category'] = df['category'].str.lower()

categorias = df['category'].unique()

for categoria in categorias:
    st.header(f"Categoría: {categoria.capitalize()}")

    df_cat = df[df['category'] == categoria]

    # Métricas clave
    total_productos = df_cat['product_id'].nunique()
    avg_actual_price = df_cat['actual_price'].mean()
    avg_discounted_price = df_cat['discounted_price'].mean()
    avg_discount = df_cat['discount_percentage'].mean()
    avg_rating = df_cat['rating'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Productos únicos", total_productos)
    col2.metric("Precio promedio (actual)", f"${avg_actual_price:.2f}")
    col3.metric("Precio promedio (con descuento)", f"${avg_discounted_price:.2f}")
    col4.metric("Descuento promedio (%)", f"{avg_discount:.2f}%")
    col5.metric("Rating promedio", f"{avg_rating:.2f} ⭐")

    # Top 5 productos más vendidos (rating_count)
    top5 = df_cat.sort_values(by='rating_count', ascending=False).head(5)
    st.subheader("Top 5 Productos Más Vendidos")
    fig = px.bar(top5, x='product_name', y='rating_count',
                 labels={'rating_count': 'Cantidad de Reseñas'},
                 text='rating_count')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Distribución de descuentos
    st.subheader("Distribución de Descuentos")
    fig2 = px.histogram(df_cat, x='discount_percentage',
                        nbins=20,
                        labels={'discount_percentage': 'Porcentaje de Descuento (%)'},
                        title="Frecuencia de Descuentos")
    st.plotly_chart(fig2, use_container_width=True)

    # Rating vs cantidad de reseñas
    st.subheader("Rating vs Cantidad de Reseñas")
    fig3 = px.scatter(df_cat, x='rating_count', y='rating',
                      hover_data=['product_name'],
                      labels={'rating_count': 'Cantidad de Reseñas', 'rating': 'Rating'},
                      title="Rating y Cantidad de Reseñas por Producto")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
