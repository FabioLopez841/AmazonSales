import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Dashboard de Productos", layout="wide")

# Cargar datos
df = pd.read_csv("amazon.csv")

# Título
st.title("📊 Dashboard de Visualización de Productos y Reseñas")

# Filtro por categoría
categorias = df["category"].dropna().unique()
categoria_seleccionada = st.sidebar.multiselect("Seleccionar categoría:", categorias, default=categorias)
df_filtrado = df[df["category"].isin(categoria_seleccionada)]

# 1. Precio real vs Precio con descuento
st.subheader("1️⃣ Comparación de Precio Real vs. Precio con Descuento")
fig1 = px.box(df_filtrado, x="category", y="actual_price", points="all", title="Precio Real por Categoría")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.box(df_filtrado, x="category", y="discounted_price", points="all", title="Precio con Descuento por Categoría")
st.plotly_chart(fig2, use_container_width=True)

# 2. Porcentaje de descuento por categoría
st.subheader("2️⃣ Porcentaje de Descuento por Categoría")
fig3 = px.bar(df_filtrado.groupby("category")["discount_percentage"].mean().reset_index(),
              x="category", y="discount_percentage", title="Promedio de Descuento (%)")
st.plotly_chart(fig3, use_container_width=True)

# 3. Promedio de rating por categoría
st.subheader("3️⃣ Rating Promedio por Categoría")
fig4 = px.bar(df_filtrado.groupby("category")["rating"].mean().reset_index(),
              x="category", y="rating", title="Calificación Promedio")
st.plotly_chart(fig4, use_container_width=True)

# 4. Distribución de calificaciones
st.subheader("4️⃣ Distribución de Calificaciones")
fig5 = px.histogram(df_filtrado, x="rating", nbins=20, title="Histograma de Calificaciones")
st.plotly_chart(fig5, use_container_width=True)

# 5. Número de reseñas por producto
st.subheader("5️⃣ Top Productos con Más Reseñas")
top_reviews = df_filtrado["product_name"].value_counts().nlargest(10).reset_index()
top_reviews.columns = ["product_name", "review_count"]
fig6 = px.bar(top_reviews, x="product_name", y="review_count", title="Top 10 Productos con Más Reseñas")
st.plotly_chart(fig6, use_container_width=True)

# 6. Usuarios más activos (por reseñas)
st.subheader("6️⃣ Usuarios Más Activos (reseñas)")
top_users = df_filtrado["user_name"].value_counts().nlargest(10).reset_index()
top_users.columns = ["user_name", "review_count"]
fig7 = px.bar(top_users, x="user_name", y="review_count", title="Top 10 Usuarios Más Activos")
st.plotly_chart(fig7, use_container_width=True)

# 7. Productos mejor calificados (mínimo 5 reseñas)
st.subheader("7️⃣ Productos Mejor Calificados")
min_reviews = df_filtrado.groupby("product_name")["rating_count"].count()
valid_products = min_reviews[min_reviews >= 5].index
top_rated = df_filtrado[df_filtrado["product_name"].isin(valid_products)]
avg_rating = top_rated.groupby("product_name")["rating"].mean().nlargest(10).reset_index()
fig8 = px.bar(avg_rating, x="product_name", y="rating", title="Top 10 Productos Mejor Calificados")
st.plotly_chart(fig8, use_container_width=True)

# 8. Nube de palabras de títulos de reseñas
st.subheader("8️⃣ Nube de Palabras de Títulos de Reseñas")
text = " ".join(str(t) for t in df_filtrado["review_title"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
fig9, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig9)

# 9. Histograma del número de calificaciones
st.subheader("9️⃣ Histograma del Número de Calificaciones")
fig10 = px.histogram(df_filtrado, x="rating_count", nbins=30, title="Distribución del Número de Calificaciones")
st.plotly_chart(fig10, use_container_width=True)

# 10. Relación entre rating y descuento
st.subheader("🔟 Relación entre Calificación y Descuento")
fig11 = px.scatter(df_filtrado, x="discount_percentage", y="rating",
                   size="rating_count", color="category",
                   title="Rating vs. Porcentaje de Descuento")
st.plotly_chart(fig11, use_container_width=True)
