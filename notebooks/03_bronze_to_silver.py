import os
import pandas as pd
from dotenv import load_dotenv

# 1. Charger les variables d'environnement
load_dotenv(dotenv_path=".env")

bucket_name = "attijari-data" # Ton bucket MinIO

# 2. Configurer Pandas pour qu'il utilise ton MinIO local au lieu du vrai AWS S3
storage_options = {
    "key": os.getenv('AWS_ACCESS_KEY_ID'),
    "secret": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "client_kwargs": {
        "endpoint_url": os.getenv('S3_ENDPOINT_URL'),
        "region_name": os.getenv('AWS_REGION')
    }
}

# 3. Lire le fichier directement depuis la couche Bronze sur MinIO
# Attention : adapte le sep=';' si c'est le CSV déguisé en .xlsx que l'on a vu tout à l'heure
chemin_bronze = f"s3://{bucket_name}/bronze/stocks/attijari_3ans.xlsx"
print(f"📥 Lecture depuis {chemin_bronze}...")

df = pd.read_csv(chemin_bronze, sep=';', storage_options=storage_options)

# 4. Transformations (Nettoyage de la donnée)
print("⚙️ Transformation des données...")
df_silver = df.rename(columns={
    'Séance': 'date_seance',
    'Ticker': 'ticker',
    'Instrument': 'company_name',
    'Ouverture': 'open_price',
    'Dernier Cours': 'close_price',
    'Plus Haut': 'high_price',
    'Plus Bas': 'low_price',
    'Volume (MAD)': 'volume_mad',
    'Titres Échangés': 'volume_titres',
    'Nb Transactions': 'transactions',
    'Capitalisation': 'capitalisation'
})

# Nettoyage des espaces et conversion de la date
df_silver['ticker'] = df_silver['ticker'].str.strip()
df_silver['date_seance'] = pd.to_datetime(df_silver['date_seance'], format='%d/%m/%Y')

# Tri chronologique des données boursières
df_silver = df_silver.sort_values('date_seance').reset_index(drop=True)

# 5. Sauvegarde au format Parquet directement dans la couche Silver sur MinIO
chemin_silver = f"s3://{bucket_name}/silver/stocks/attijari_3ans_clean.parquet"

print(f"📤 Sauvegarde vers {chemin_silver}...")
df_silver.to_parquet(
    chemin_silver, 
    index=False, 
    storage_options=storage_options
)

print("✅ Traitement Bronze vers Silver terminé avec succès !")
# Remplacer ceci :
# display(df_silver.head())

# Par cela :
print(df_silver.head())