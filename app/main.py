import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("../.env") # Ajuste le chemin si besoin

# Configuration de la page
st.set_page_config(page_title="Bourse de Casablanca", page_icon="📈", layout="wide")
st.title("📈 Tableau de Bord Boursier - Casablanca")
st.markdown("Projet Data Lakehouse de bout en bout (MinIO, PostgreSQL, dbt, Airflow)")

# Connexion à PostgreSQL (en lecture depuis la couche Gold)
@st.cache_resource
def init_connection():
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', 'admin123')
    host = '127.0.0.1'
    port = '5434' # Ton port PostgreSQL modifié
    db = os.getenv('POSTGRES_DB', 'market_data')
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

engine = init_connection()

# Récupération des données via une jointure entre les faits et la dimension
@st.cache_data
def load_data():
    query = """
    SELECT 
        dp.date_key, 
        ds.ticker, 
        dp.close_price, 
        dp.volume_titres
    FROM fact_daily_prices dp
    JOIN dim_stock ds ON dp.stock_key = ds.stock_key
    ORDER BY dp.date_key
    """
    return pd.read_sql(query, engine)

try:
    df = load_data()
    
    # Filtre interactif
    tickers = df['ticker'].unique()
    selected_ticker = st.selectbox("Sélectionnez une action :", tickers)
    
    # Filtrer les données selon le choix
    df_filtered = df[df['ticker'] == selected_ticker]
    
    # Affichage du graphique
    st.subheader(f"Évolution du prix de clôture : {selected_ticker}")
    st.line_chart(data=df_filtered, x='date_key', y='close_price')
    
    # Affichage des données brutes
    st.subheader("Aperçu des données")
    st.dataframe(df_filtered.tail(10))

except Exception as e:
    st.error(f"Erreur de connexion à la base de données : {e}")