#!/usr/bin/env python3
"""
Régie Essence Québec - Scraper Saguenay
Télécharge les données et filtre Jonquière/Chicoutimi
"""

import requests
import pandas as pd
import json
import os
import glob
from datetime import datetime

# Configuration
OUTPUT_JSON = "data.json"
REGIONS_CIBLES = ["Saguenay", "Jonquière", "Chicoutimi", "Saguenay–Lac-Saint-Jean"]
VILLES_CIBLES = ["Saguenay", "Jonquière", "Chicoutimi"]

def trouver_dernier_fichier():
    """Trouve l'URL du dernier fichier Excel sur le site"""
    try:
        response = requests.get("https://regieessencequebec.ca/", timeout=10)
        import re
        # Cherche le pattern de fichier Excel dans la page
        matches = re.findall(r'data/stations-\d+\.xlsx', response.text)
        if matches:
            return f"https://regieessencequebec.ca/{matches[-1]}"
    except:
        pass
    return None

def telecharger_excel(url=None):
    """Télécharge le fichier Excel"""
    if not url:
        url = trouver_dernier_fichier()
    
    if not url:
        print("❌ Impossible de trouver l'URL du fichier Excel")
        return None
    
    print(f"📥 Téléchargement: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            filepath = "/tmp/stations_essence.xlsx"
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Fichier téléchargé: {len(response.content)} bytes")
            return filepath
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def filtrer_saguenay(filepath):
    """Lit le Excel et filtre Jonquière/Chicoutimi"""
    try:
        df = pd.read_excel(filepath)
        print(f"📊 Total stations au Québec: {len(df)}")
        
        # Filtre par région ou adresse contenant Saguenay/Jonquière/Chicoutimi
        masque = (
            df['Région'].str.contains('Saguenay', case=False, na=False) |
            df['Adresse'].str.contains('Jonquière', case=False, na=False) |
            df['Adresse'].str.contains('Chicoutimi', case=False, na=False) |
            df['Adresse'].str.contains('Saguenay', case=False, na=False)
        )
        
        df_saguenay = df[masque].copy()
        print(f"📍 Stations Saguenay trouvées: {len(df_saguenay)}")
        
        # Garde seulement les colonnes utiles
        colonnes = ['Bannière', 'Adresse', 'Prix Régulier']
        df_final = df_saguenay[colonnes].copy()
        
        # Retire les stations sans prix
        df_final = df_final.dropna(subset=['Prix Régulier'])
        
        # Trie par prix croissant
        df_final = df_final.sort_values('Prix Régulier')
        
        print(f"✅ Stations avec prix: {len(df_final)}")
        return df_final
        
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return None

def sauvegarder_json(df):
    """Sauvegarde en JSON"""
    stations = []
    for _, row in df.iterrows():
        prix = row['Prix Régulier']
        try:
            prix_num = float(prix)
        except:
            prix_num = 0
            
        stations.append({
            "banniere": str(row['Bannière']) if pd.notna(row['Bannière']) else "Inconnue",
            "adresse": str(row['Adresse']),
            "prix": round(prix_num, 1)
        })
    
    data = {
        "mise_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total": len(stations),
        "stations": stations
    }
    


    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON sauvegardé: {OUTPUT_JSON}")
    print(f"🏆 Meilleur prix: {stations[0]['banniere']} - {stations[0]['adresse']} - {stations[0]['prix']}¢")
    return True

def main():
    print("=" * 50)
    print("🔥 Régie Essence Québec - Saguenay")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)
    
    # Télécharge
    filepath = telecharger_excel()
    if not filepath:
        return False
    
    # Filtre
    df = filtrer_saguenay(filepath)
    if df is None or len(df) == 0:
        print("❌ Aucune station trouvée")
        return False
    
    # Sauvegarde
    sauvegarder_json(df)
    
    # Nettoie
    os.remove(filepath)
    print("✅ Terminé!")
    return True

if __name__ == "__main__":
    main()
