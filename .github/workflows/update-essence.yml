name: Update Essence Data

on:
  schedule:
    - cron: '0 10 * * *'
    - cron: '0 12 * * *'
    - cron: '0 14 * * *'
    - cron: '0 16 * * *'
    - cron: '0 18 * * *'
    - cron: '0 20 * * *'
    - cron: '0 22 * * *'
    - cron: '0 0 * * *'
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests pandas openpyxl

      - name: Find Excel URL
        run: |
          python3 - <<'EOF'
          import requests
          from datetime import datetime, timedelta
          import time

          headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
          base = "https://regieessencequebec.ca/data/stations-"
          found = None
          now = datetime.utcnow()

          print(f"Recherche autour de {now.strftime('%Y-%m-%d %H:%M')} UTC")
          
          # Teste seulement les minutes des 4 dernières heures (240 requetes max)
          for delta_min in range(0, 241):
              dt = now - timedelta(minutes=delta_min)
              # Teste avec secondes 00, 30 seulement pour réduire les requêtes
              for sec in [0, 30]:
                  ts = dt.strftime(f"%Y%m%d%H%M{sec:02d}")
                  url = f"{base}{ts}.xlsx"
                  try:
                      r = requests.head(url, headers=headers, timeout=3)
                      if r.status_code == 200:
                          found = url
                          print(f"Trouve: {url}")
                          break
                  except:
                      pass
              if found:
                  break
              # Petite pause toutes les 50 requetes pour eviter le blocage
              if delta_min % 50 == 0 and delta_min > 0:
                  time.sleep(1)

          if found:
              with open("excel_url.txt", "w") as f:
                  f.write(found)
              print(f"URL sauvegardee: {found}")
          else:
              print("Aucune URL trouvee dans les 4 dernieres heures")
              with open("excel_url.txt", "w") as f:
                  f.write("")
          EOF

      - name: Run scraper
        run: |
          URL=$(cat excel_url.txt)
          echo "URL: $URL"
          python essence_saguenay.py "$URL"

      - name: Commit data
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data.json
          git diff --staged --quiet || git commit -m "Update essence data"
          git push
