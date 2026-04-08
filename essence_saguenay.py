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
    if not url or url.strip() == "":
        print("Aucune URL fournie")
        return None

    print(f"Telechargement: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

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

def convertir_prix(val):
    try:
        s = str(val).replace(',', '.').replace('¢', '').replace('$', '').replace(' ', '').strip()
        p = float(s)
        if p <= 0:
            return 0
        if p >= 100:
            return round(p, 1)
        if p < 10:
            return round(p * 100, 1)
        return round(p, 1)
    except:
        return 0

def filtrer_saguenay(filepath):
    try:
        df = pd.read_excel(filepath)
        print(f"Total stations au Quebec: {len(df)}")
        print(f"Colonnes disponibles: {df.columns.tolist()}")

        col_banniere = col_adresse = col_prix = col_region = col_cp = None
        col_lat = col_lon = None

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
            if 'postal' in col_lower:
                col_cp = col
            if 'latitude' in col_lower or col_lower == 'lat':
                col_lat = col
            if 'longitude' in col_lower or col_lower == 'lon' or col_lower == 'lng':
                col_lon = col

        print(f"Colonnes: banniere={col_banniere}, adresse={col_adresse}, prix={col_prix}, region={col_region}, cp={col_cp}, lat={col_lat}, lon={col_lon}")

        masque = pd.Series([False] * len(df))
        if col_region:
            masque = masque | df[col_region].astype(str).str.contains('Saguenay', case=False, na=False)
        if col_adresse:
            masque = masque | df[col_adresse].astype(str).str.contains('Saguenay', case=False, na=False)

        df_saguenay = df[masque].copy()
        print(f"Stations Saguenay trouvees: {len(df_saguenay)}")

        colonnes = [col_banniere, col_adresse, col_prix]
        noms = ['Banniere', 'Adresse', 'Prix']

        if col_cp:
            colonnes.append(col_cp)
            noms.append('CodePostal')
        if col_lat:
            colonnes.append(col_lat)
            noms.append('Lat')
        if col_lon:
            colonnes.append(col_lon)
            noms.append('Lon')

        df_final = df_saguenay[colonnes].copy()
        df_final.columns = noms

        print(f"Exemple prix bruts: {df_final['Prix'].head(5).tolist()}")

        df_final['Prix'] = df_final['Prix'].apply(convertir_prix)
        df_final = df_final[df_final['Prix'] > 0]
        df_final = df_final.sort_values('Prix')

        print(f"Stations avec prix valides: {len(df_final)}")
        if len(df_final) > 0:
            print(f"Prix min: {df_final['Prix'].min()}, max: {df_final['Prix'].max()}")
        return df_final

    except Exception as e:
        import traceback
        print(f"Erreur: {e}")
        traceback.print_exc()
        return None

def determiner_ville(row):
    if 'CodePostal' in row.index and pd.notna(row.get('CodePostal')):
        cp = str(row['CodePostal']).upper().strip()
        if cp.startswith(('G7H', 'G7B', 'G7G')):
            return "Chicoutimi"
        elif cp.startswith(('G7J', 'G7K', 'G7X', 'G7S')):
            return "Jonquiere"
    return "Saguenay"

def sauvegarder_json(df, url_source=""):
    stations = []
    for _, row in df.iterrows():
        try:
            prix_num = float(row['Prix'])
        except:
            prix_num = 0

        # Coordonnees GPS
        lat = None
        lon = None
        if 'Lat' in row.index and pd.notna(row.get('Lat')):
            try:
                lat = round(float(row['Lat']), 6)
            except:
                pass
        if 'Lon' in row.index and pd.notna(row.get('Lon')):
            try:
                lon = round(float(row['Lon']), 6)
            except:
                pass

        stations.append({
            "banniere": str(row['Banniere']) if pd.notna(row['Banniere']) else "Inconnue",
            "adresse": str(row['Adresse']),
            "ville": determiner_ville(row),
            "prix": round(prix_num, 1),
            "lat": lat,
            "lon": lon
        })

    nom_fichier = ""
    if url_source:
        match = re.search(r'stations-[\d]+\.xlsx', url_source)
        if match:
            nom_fichier = match.group(0)

    data = {
        "mise_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fichier_source": nom_fichier,
        "total": len(stations),
        "stations": stations
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON sauvegarde: {OUTPUT_JSON}")
    if stations:
        print(f"Meilleur prix: {stations[0]['banniere']} - {stations[0]['adresse']} - {stations[0]['prix']}c")
        if stations[0]['lat']:
            print(f"Coordonnees: {stations[0]['lat']}, {stations[0]['lon']}")
    return True

def main():
    print("=" * 50)
    print("Regie Essence Quebec - Saguenay")
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)

    url = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if url:
        print(f"URL: {url}")

    filepath = telecharger_excel(url)
    if not filepath:
        data = {
            "mise_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "fichier_source": "",
            "total": 0,
            "stations": [],
            "erreur": "Fichier Excel non disponible"
        }
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return False

    df = filtrer_saguenay(filepath)
    if df is None or len(df) == 0:
        print("Aucune station trouvee")
        return False

    sauvegarder_json(df, url or "")
    os.remove(filepath)
    print("Termine!")
    return True

if __name__ == "__main__":
    main()
