#!/usr/bin/env python3
"""
Regie Essence Quebec - Scraper Saguenay
Telecharge les donnees et filtre Jonquiere/Chicoutimi
"""

import requests
import pandas as pd
import json
import os
import re
import sys
from datetime import datetime

OUTPUT_JSON = "data.json"

def telecharger_excel(url=None):
    """Telecharge le fichier Excel"""
    if not url or url.strip() == "":
        print("Aucune URL fournie")
        return None

    print(f"Telechargement: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            filepath = "/tmp/stations_essence.xlsx"
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Fichier telecharge: {len(response.content)} bytes")
            return filepath
        else:
            print(f"Erreur HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def filtrer_saguenay(filepath):
    """Lit le Excel et filtre la region Saguenay"""
    try:
        df = pd.read_excel(filepath)
        print(f"Total stations au Quebec: {len(df)}")
        print(f"Colonnes: {df.columns.tolist()}")
        
        # Affiche quelques lignes pour debug
        print("Exemple de donnees:")
        print(df.head(3).to_string())

        # Detecte les colonnes
        col_banniere = None
        col_adresse = None
        col_prix = None
        col_region = None
        col_cp = None

        for col in df.columns:
            col_lower = col.lower()
            if 'banni' in col_lower:
                col_banniere = col
            if 'adresse' in col_lower:
                col_adresse = col
            if 'regulier' in col_lower or 'régulier' in col_lower:
                col_prix = col
            if 'region' in col_lower or 'région' in col_lower:
                col_region = col
            if 'postal' in col_lower or 'code' in col_lower:
                col_cp = col

        print(f"Colonnes detectees: banniere={col_banniere}, adresse={col_adresse}, prix={col_prix}, region={col_region}")

        # Filtre par region Saguenay
        masque = pd.Series([False] * len(df))
        
        if col_region:
            masque = masque | df[col_region].astype(str).str.contains('Saguenay', case=False, na=False)
        
        if col_adresse:
            masque = masque | df[col_adresse].astype(str).str.contains('Saguenay', case=False, na=False)
            masque = masque | df[col_adresse].astype(str).str.contains('Jonquiere', case=False, na=False)
            masque = masque | df[col_adresse].astype(str).str.contains('Chicoutimi', case=False, na=False)

        df_saguenay = df[masque].copy()
        print(f"Stations Saguenay trouvees: {len(df_saguenay)}")

        # Garde les colonnes utiles
        colonnes_garder = [col_banniere, col_adresse, col_prix]
        if col_region:
            colonnes_garder.append(col_region)
        if col_cp:
            colonnes_garder.append(col_cp)

        df_final = df_saguenay[colonnes_garder].copy()

        # Renomme les colonnes
        new_names = ['Banniere', 'Adresse', 'Prix']
        if col_region:
            new_names.append('Region')
        if col_cp:
            new_names.append('CodePostal')
        df_final.columns = new_names

        # Retire les stations sans prix
        df_final = df_final.dropna(subset=['Prix'])
        
        # Debug prix
        print(f"Exemple de prix bruts: {df_final['Prix'].head(5).tolist()}")
        
        # Convertit les prix
        def convertir_prix(val):
            try:
                p = float(str(val).replace(',', '.').strip())
                # Si prix < 10, c'est en dollars (ex: 1.879) -> convertir en cents (187.9)
                if p > 0 and p < 10:
                    p = round(p * 100, 1)
                # Si prix entre 10 et 100, probablement en cents deja (ex: 87.9)
                elif p >= 100 and p < 300:
                    pass  # OK deja en cents
                elif p > 0:
                    p = round(p, 1)
                return p
            except:
                return 0

        df_final['Prix'] = df_final['Prix'].apply(convertir_prix)
        
        # Retire les prix a 0
        df_final = df_final[df_final['Prix'] > 0]
        
        # Trie par prix croissant
        df_final = df_final.sort_values('Prix')

        print(f"Stations avec prix valides: {len(df_final)}")
        print(f"Prix min: {df_final['Prix'].min()}, Prix max: {df_final['Prix'].max()}")
        return df_final

    except Exception as e:
        import traceback
        print(f"Erreur lecture Excel: {e}")
        traceback.print_exc()
        return None

def sauvegarder_json(df):
    """Sauvegarde en JSON"""
    stations = []
    for _, row in df.iterrows():
        try:
            prix_num = float(row['Prix'])
        except:
            prix_num = 0

        # Determine la ville depuis le code postal ou la region
        ville = "Saguenay"
        adresse = str(row['Adresse'])
        
        # Codes postaux: G7H = Chicoutimi, G7J/G7K = Jonquiere
        if 'CodePostal' in df.columns and pd.notna(row.get('CodePostal')):
            cp = str(row['CodePostal']).upper().strip()
            if cp.startswith('G7H') or cp.startswith('G7B') or cp.startswith('G7G'):
                ville = "Chicoutimi"
            elif cp.startswith('G7J') or cp.startswith('G7K') or cp.startswith('G7X') or cp.startswith('G7S'):
                ville = "Jonquiere"
        
        stations.append({
            "banniere": str(row['Banniere']) if pd.notna(row['Banniere']) else "Inconnue",
            "adresse": adresse,
            "ville": ville,
            "prix": round(prix_num, 1)
        })

    data = {
        "mise_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total": len(stations),
        "stations": stations
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON sauvegarde: {OUTPUT_JSON}")
    if stations:
        print(f"Meilleur prix: {stations[0]['banniere']} - {stations[0]['adresse']} - {stations[0]['prix']}c")
    return True

def main():
    print("=" * 50)
    print("Regie Essence Quebec - Saguenay")
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    url = sys.argv[1] if len(sys.argv) > 1 else None
    if url:
        url = url.strip()
    if url:
        print(f"URL fournie en argument: {url}")

    filepath = telecharger_excel(url)
    if not filepath:
        data = {
            "mise_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "total": 0,
            "stations": [],
            "erreur": "Fichier Excel non disponible"
        }
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("data.json vide cree")
        return False

    df = filtrer_saguenay(filepath)
    if df is None or len(df) == 0:
        print("Aucune station trouvee")
        return False

    sauvegarder_json(df)
    os.remove(filepath)
    print("Termine!")
    return True

if __name__ == "__main__":
    main()
