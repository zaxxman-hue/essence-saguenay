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
from datetime import datetime
 
# Configuration
OUTPUT_JSON = "data.json"
 
def trouver_dernier_fichier():
    """Trouve l'URL du dernier fichier Excel sur le site"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get("https://regieessencequebec.ca/", headers=headers, timeout=15)
        matches = re.findall(r'data/stations-\d+\.xlsx', response.text)
        if matches:
            url = f"https://regieessencequebec.ca/{matches[-1]}"
            print(f"URL trouvee: {url}")
            return url
    except Exception as e:
        print(f"Erreur recherche URL: {e}")
 
    # Cherche dans les assets JS aussi
    try:
        r2 = requests.get("https://regieessencequebec.ca/", headers=headers, timeout=15)
        # Cherche pattern alternatif
        matches2 = re.findall(r'stations-[\d]+\.xlsx', r2.text)
        if matches2:
            return f"https://regieessencequebec.ca/data/{matches2[-1]}"
    except:
        pass
 
    # Genere URL basee sur date/heure actuelle comme fallback
    now = datetime.now()
    for hour in range(now.hour, max(now.hour-12, -1), -1):
        for minute in [0, 30]:
            timestamp = now.strftime(f"%Y%m%d{hour:02d}{minute:02d}00")
            url = f"https://regieessencequebec.ca/data/stations-{timestamp}.xlsx"
            try:
                r = requests.head(url, headers=headers, timeout=5)
                if r.status_code == 200:
                    print(f"URL trouvee par bruteforce: {url}")
                    return url
            except:
                pass
    return None
 
def telecharger_excel(url=None):
    """Telecharge le fichier Excel"""
    if not url:
        url = trouver_dernier_fichier()
 
    if not url:
        print("Impossible de trouver l'URL du fichier Excel")
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
    """Lit le Excel et filtre Jonquiere/Chicoutimi"""
    try:
        df = pd.read_excel(filepath)
        print(f"Total stations au Quebec: {len(df)}")
        print(f"Colonnes: {df.columns.tolist()}")
 
        masque = (
            df['Region'].str.contains('Saguenay', case=False, na=False) |
            df['Adresse'].str.contains('Jonquiere', case=False, na=False) |
            df['Adresse'].str.contains('Chicoutimi', case=False, na=False) |
            df['Adresse'].str.contains('Saguenay', case=False, na=False)
        )
 
        # Essaie aussi avec accents
        try:
            masque2 = (
                df['Région'].str.contains('Saguenay', case=False, na=False) |
                df['Adresse'].str.contains('Jonquière', case=False, na=False) |
                df['Adresse'].str.contains('Chicoutimi', case=False, na=False)
            )
            masque = masque | masque2
        except:
            pass
 
        df_saguenay = df[masque].copy()
        print(f"Stations Saguenay trouvees: {len(df_saguenay)}")
 
        # Detecte les colonnes avec ou sans accents
        col_banniere = 'Bannière' if 'Bannière' in df.columns else 'Banniere'
        col_prix = 'Prix Régulier' if 'Prix Régulier' in df.columns else 'Prix Regulier'
 
        colonnes = [col_banniere, 'Adresse', col_prix]
        df_final = df_saguenay[colonnes].copy()
        df_final.columns = ['Banniere', 'Adresse', 'Prix']
 
        df_final = df_final.dropna(subset=['Prix'])
        df_final = df_final.sort_values('Prix')
 
        print(f"Stations avec prix: {len(df_final)}")
        return df_final
 
    except Exception as e:
        print(f"Erreur lecture Excel: {e}")
        return None
 
def sauvegarder_json(df):
    """Sauvegarde en JSON"""
    stations = []
    for _, row in df.iterrows():
        try:
            prix_num = float(row['Prix'])
        except:
            prix_num = 0
 
        stations.append({
            "banniere": str(row['Banniere']) if pd.notna(row['Banniere']) else "Inconnue",
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
 
    print(f"JSON sauvegarde: {OUTPUT_JSON}")
    if stations:
        print(f"Meilleur prix: {stations[0]['banniere']} - {stations[0]['adresse']} - {stations[0]['prix']}c")
    return True
 
def main():
    print("=" * 50)
    print("Regie Essence Quebec - Saguenay")
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)
 
    filepath = telecharger_excel()
    if not filepath:
        # Cree un data.json vide pour eviter l'erreur git
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
