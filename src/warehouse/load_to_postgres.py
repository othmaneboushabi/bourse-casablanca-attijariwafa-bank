import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Charger les variables d'environnement
load_dotenv(".env")

bucket_name = "attijari-data"

# 2. Configurer l'accès à MinIO
storage_options = {
    "key": os.getenv('AWS_ACCESS_KEY_ID'),
    "secret": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "client_kwargs": {
        "endpoint_url": os.getenv('S3_ENDPOINT_URL'),
        "region_name": os.getenv('AWS_REGION')
    }
}

print("📥 Lecture de la donnée Silver depuis MinIO...")
chemin_silver = f"s3://{bucket_name}/silver/stocks/attijari_3ans_clean.parquet"
df_silver = pd.read_parquet(chemin_silver, storage_options=storage_options)

# 3. Créer la connexion à PostgreSQL
print("🔌 Connexion au Data Warehouse PostgreSQL...")
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
db = os.getenv('POSTGRES_DB')

# Utilisation explicite du moteur psycopg2
chaine_connexion = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(chaine_connexion)

# 4. Charger les données dans PostgreSQL
nom_table = "stg_stock_prices"
print(f"📤 Injection des données dans la table '{nom_table}'...")

df_silver.to_sql(nom_table, engine, if_exists='replace', index=False)

print(f"✅ Succès ! {len(df_silver)} lignes ont été insérées dans la base PostgreSQL.")