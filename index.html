<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#1a1a2e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<title>⛽ Essence Saguenay</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f0f1a;
    color: #e0e0e0;
    min-height: 100vh;
  }

  header {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    padding: 20px 16px 16px;
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid #2a2a4a;
    box-shadow: 0 2px 20px rgba(0,0,0,0.5);
  }

  h1 {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .subtitle {
    font-size: 12px;
    color: #888;
    margin-top: 4px;
  }

  .maj {
    font-size: 11px;
    color: #4fc3f7;
    margin-top: 6px;
  }

  .filtre {
    display: flex;
    gap: 8px;
    margin-top: 12px;
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .filtre button {
    background: #1e1e3a;
    border: 1px solid #333;
    color: #aaa;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
  }

  .filtre button.actif {
    background: #4fc3f7;
    color: #000;
    border-color: #4fc3f7;
    font-weight: 600;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 12px 16px;
    background: #12122a;
    border-bottom: 1px solid #2a2a4a;
  }

  .stat-card {
    background: #1e1e3a;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
  }

  .stat-label {
    font-size: 10px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .stat-value {
    font-size: 18px;
    font-weight: 700;
    margin-top: 4px;
  }

  .stat-value.bas { color: #4caf50; }
  .stat-value.moyen { color: #ffb74d; }
  .stat-value.haut { color: #ef5350; }

  .liste {
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .station {
    background: #1e1e3a;
    border-radius: 12px;
    padding: 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    border: 1px solid #2a2a4a;
    transition: transform 0.15s;
    position: relative;
    overflow: hidden;
  }

  .station:active { transform: scale(0.98); }

  .station.top1 { border-color: #4caf50; }
  .station.top2 { border-color: #8bc34a; }
  .station.top3 { border-color: #cddc39; }

  .rang {
    font-size: 13px;
    font-weight: 700;
    color: #666;
    min-width: 24px;
    text-align: center;
  }

  .station.top1 .rang { color: #4caf50; font-size: 18px; }
  .station.top2 .rang { color: #8bc34a; }
  .station.top3 .rang { color: #cddc39; }

  .info {
    flex: 1;
    min-width: 0;
  }

  .banniere {
    font-size: 15px;
    font-weight: 600;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .adresse {
    font-size: 12px;
    color: #888;
    margin-top: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .prix-box {
    text-align: right;
    flex-shrink: 0;
  }

  .prix {
    font-size: 24px;
    font-weight: 800;
    line-height: 1;
  }

  .prix-unit {
    font-size: 11px;
    color: #888;
    margin-top: 2px;
  }

  .economie {
    font-size: 11px;
    color: #4caf50;
    margin-top: 3px;
  }

  .loading {
    text-align: center;
    padding: 60px 20px;
    color: #666;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #333;
    border-top-color: #4fc3f7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .erreur {
    text-align: center;
    padding: 40px 20px;
    color: #ef5350;
  }

  .btn-refresh {
    background: #4fc3f7;
    color: #000;
    border: none;
    padding: 10px 24px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 12px;
  }

  .vide {
    text-align: center;
    padding: 40px;
    color: #555;
  }
</style>
</head>
<body>

<header>
  <h1>⛽ Essence Saguenay</h1>
  <div class="subtitle">Jonquière • Chicoutimi</div>
  <div class="maj" id="maj">Chargement...</div>
  <div class="filtre">
    <button class="actif" onclick="filtrer('tous')">Tous</button>
    <button onclick="filtrer('jonquiere')">Jonquière</button>
    <button onclick="filtrer('chicoutimi')">Chicoutimi</button>
  </div>
</header>

<div class="stats" id="stats" style="display:none">
  <div class="stat-card">
    <div class="stat-label">Plus bas</div>
    <div class="stat-value bas" id="stat-bas">—</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Moyen</div>
    <div class="stat-value moyen" id="stat-moy">—</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Plus haut</div>
    <div class="stat-value haut" id="stat-haut">—</div>
  </div>
</div>

<div id="contenu">
  <div class="loading">
    <div class="spinner"></div>
    <div>Chargement des prix...</div>
  </div>
</div>

<script>
let toutesStations = [];
let filtreActuel = 'tous';

async function charger() {
  try {
    const r = await fetch('data.json?t=' + Date.now());
    if (!r.ok) throw new Error('Fichier introuvable');
    const data = await r.json();
    
    toutesStations = data.stations;
    document.getElementById('maj').textContent = '🕐 Mis à jour: ' + data.mise_a_jour;
    
    afficher(toutesStations);
  } catch(e) {
    document.getElementById('contenu').innerHTML = `
      <div class="erreur">
        ❌ Données non disponibles<br>
        <small>${e.message}</small><br>
        <button class="btn-refresh" onclick="charger()">🔄 Réessayer</button>
      </div>`;
  }
}

function filtrer(zone) {
  filtreActuel = zone;
  
  // Met à jour les boutons
  document.querySelectorAll('.filtre button').forEach(b => b.classList.remove('actif'));
  event.target.classList.add('actif');
  
  let stations = toutesStations;
  
  if (zone === 'jonquiere') {
    stations = toutesStations.filter(s => 
      s.adresse.toLowerCase().includes('jonquière') || 
      s.adresse.toLowerCase().includes('jonquiere'));
  } else if (zone === 'chicoutimi') {
    stations = toutesStations.filter(s => 
      s.adresse.toLowerCase().includes('chicoutimi'));
  }
  
  afficher(stations);
}

function afficher(stations) {
  if (stations.length === 0) {
    document.getElementById('stats').style.display = 'none';
    document.getElementById('contenu').innerHTML = '<div class="vide">Aucune station trouvée</div>';
    return;
  }
  
  // Stats
  const prix = stations.map(s => s.prix).filter(p => p > 0).sort((a,b) => a-b);
  const moyen = prix.reduce((a,b) => a+b, 0) / prix.length;
  const prixMin = prix[0];
  
  document.getElementById('stat-bas').textContent = prix[0] + '¢';
  document.getElementById('stat-moy').textContent = Math.round(moyen) + '¢';
  document.getElementById('stat-haut').textContent = prix[prix.length-1] + '¢';
  document.getElementById('stats').style.display = 'grid';
  
  // Liste
  let html = '<div class="liste">';
  
  stations.forEach((s, i) => {
    const rang = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i+1);
    const classe = i === 0 ? 'top1' : i === 1 ? 'top2' : i === 2 ? 'top3' : '';
    const eco = i > 0 && s.prix > 0 ? `Économie: ${(s.prix - prixMin).toFixed(1)}¢/L` : '';
    
    const couleur = i === 0 ? '#4caf50' : 
                    i < 3 ? '#8bc34a' :
                    s.prix > moyen + 5 ? '#ef5350' : '#e0e0e0';
    
    html += `
      <div class="station ${classe}">
        <div class="rang">${rang}</div>
        <div class="info">
          <div class="banniere">${s.banniere}</div>
          <div class="adresse">📍 ${s.adresse}</div>
          ${eco ? `<div class="economie">💰 ${eco}</div>` : ''}
        </div>
        <div class="prix-box">
          <div class="prix" style="color:${couleur}">${s.prix}</div>
          <div class="prix-unit">¢/litre</div>
        </div>
      </div>`;
  });
  
  html += '</div>';
  document.getElementById('contenu').innerHTML = html;
}

// Charge au démarrage
charger();

// Rafraîchit toutes les 30 minutes
setInterval(charger, 30 * 60 * 1000);
</script>

</body>
</html>
