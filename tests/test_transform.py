import pandas as pd
import pytest

# Fonction fictive simulant ton nettoyage Silver
def clean_financial_data(df):
    # Supprimer les doublons
    df_clean = df.drop_duplicates()
    # Filtrer les prix aberrants (négatifs ou nuls)
    df_clean = df_clean[df_clean['close_price'] > 0]
    return df_clean

def test_remove_duplicates():
    """Test pour vérifier que les lignes dupliquées sont bien supprimées."""
    data = {
        'ticker': ['ATW', 'ATW', 'BCP'],
        'date_key': ['2023-01-01', '2023-01-01', '2023-01-01'],
        'close_price': [450.0, 450.0, 280.0]
    }
    df_raw = pd.DataFrame(data)
    df_clean = clean_financial_data(df_raw)
    
    # On s'attend à ce qu'il ne reste que 2 lignes au lieu de 3
    assert len(df_clean) == 2

def test_no_negative_prices():
    """Test pour vérifier que les prix négatifs sont rejetés."""
    data = {
        'ticker': ['ATW', 'BCP'],
        'close_price': [450.0, -10.0]
    }
    df_raw = pd.DataFrame(data)
    df_clean = clean_financial_data(df_raw)
    
    # On s'attend à ce que la ligne avec le prix négatif soit supprimée
    assert len(df_clean) == 1
    assert df_clean.iloc[0]['ticker'] == 'ATW'