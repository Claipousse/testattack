#!/usr/bin/env python3

import csv
import html  # pour echapper les caracteres speciaux HTML

def generer_html(fichier_csv, fichier_html):
    """genere une page html pour visualiser les resultats"""
    
    with open(fichier_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        resultats = list(reader)
    
    # detecter automatiquement tous les modeles presents
    modeles_presents = sorted(set(r['modele'] for r in resultats))
    
    # mapper les noms de modeles vers des noms courts pour affichage
    modele_display_names = {
        'llama3.1:8b': 'Llama 3.1',
        'mistral:7b': 'Mistral 7B',
        'gpt-4': 'GPT-4',
        'claude-sonnet-4.5': 'Claude Sonnet 4.5',
        'deepseek-v3': 'DeepSeek-V3'
    }
    
    # generer les stats pour chaque modele
    stats_html = f'<span>Total : {len(resultats)} tests</span>'
    for modele in modeles_presents:
        count = sum(1 for r in resultats if r['modele'] == modele)
        display_name = modele_display_names.get(modele, modele)
        stats_html += f'<span>{display_name} : {count}</span>'
    
    # generer les options de filtre pour les modeles
    options_modeles = '<option value="">Tous les modèles</option>'
    for modele in modeles_presents:
        display_name = modele_display_names.get(modele, modele)
        options_modeles += f'<option value="{modele}">{display_name}</option>'
    
    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Résultats Jailbreak Tests</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .filters {
            background: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .filters label {
            margin-right: 10px;
            font-weight: bold;
        }
        .filters select {
            margin-right: 20px;
            padding: 5px;
        }
        .result {
            background: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .result-header {
            background: #e8f4f8;
            padding: 10px;
            margin: -20px -20px 15px -20px;
            border-radius: 5px 5px 0 0;
            border-left: 4px solid #2196F3;
        }
        .result-meta {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }
        .prompt {
            background: #fff9e6;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #ffc107;
            border-radius: 3px;
        }
        .reponse {
            background: #f0f0f0;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #4CAF50;
            border-radius: 3px;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
        }
        .tag {
            display: inline-block;
            padding: 3px 8px;
            margin: 2px;
            background: #2196F3;
            color: white;
            border-radius: 3px;
            font-size: 0.85em;
        }
        /* Tags techniques */
        .tag.roleplay { background: #e91e63; }
        .tag.educatif { background: #9c27b0; }
        .tag.encodage { background: #ff9800; }
        
        /* Tags modeles */
        .tag.llama { background: #4CAF50; }
        .tag.mistral { background: #f44336; }
        .tag.gpt { background: #00bcd4; }
        .tag.claude { background: #673ab7; }
        .tag.deepseek { background: #ff5722; }
        
        .stats {
            background: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stats span {
            margin: 0 15px;
            font-weight: bold;
        }
        .search-input {
            padding: 5px;
            width: 300px;
        }
    </style>
</head>
<body>
    <h1>Résultats Tests Jailbreak</h1>
    
    <div class="stats">
        """ + stats_html + """
    </div>
    
    <div class="filters">
        <label>Filtrer par :</label>
        <select id="filter-modele" onchange="filtrer()">
            """ + options_modeles + """
        </select>
        
        <select id="filter-technique" onchange="filtrer()">
            <option value="">Toutes les techniques</option>
            <option value="roleplay">Roleplay</option>
            <option value="educatif">Éducatif</option>
            <option value="encodage">Encodage</option>
        </select>
        
        <input type="text" id="search" class="search-input" placeholder="Rechercher..." onkeyup="filtrer()">
    </div>
    
    <div id="results">
"""
    
    for idx, r in enumerate(resultats):
        # determiner la classe css pour le modele
        if 'llama' in r['modele']:
            modele_class = 'llama'
            modele_display = modele_display_names.get(r['modele'], r['modele'])
        elif 'mistral' in r['modele']:
            modele_class = 'mistral'
            modele_display = modele_display_names.get(r['modele'], r['modele'])
        elif 'gpt' in r['modele']:
            modele_class = 'gpt'
            modele_display = modele_display_names.get(r['modele'], r['modele'])
        elif 'claude' in r['modele']:
            modele_class = 'claude'
            modele_display = modele_display_names.get(r['modele'], r['modele'])
        elif 'deepseek' in r['modele']:
            modele_class = 'deepseek'
            modele_display = modele_display_names.get(r['modele'], r['modele'])
        else:
            modele_class = 'unknown'
            modele_display = r['modele']
        
        # echapper les caracteres speciaux pour eviter les bugs d'affichage
        prompt_escaped = html.escape(r['prompt'])
        reponse_escaped = html.escape(r['reponse'])
        # pour data-content, on echappe et on remplace les guillemets par des apostrophes
        search_content = html.escape(r['prompt'].lower() + ' ' + r['reponse'].lower()).replace('"', '&quot;')
        
        html_content += f"""
        <div class="result" data-modele="{r['modele']}" data-technique="{r['technique']}" data-content="{search_content}">
            <div class="result-header">
                <strong>#{idx + 1} - {r['prompt_id']}</strong>
                <span class="tag {r['technique']}">{r['technique']}</span>
                <span class="tag {modele_class}">{modele_display}</span>
                <span class="tag">{r['domaine']}</span>
            </div>
            
            <div class="result-meta">
                Temps : {r['temps_secondes']}s | {r['timestamp']}
            </div>
            
            <div class="prompt">
                <strong>Prompt :</strong><br>
                {prompt_escaped}
            </div>
            
            <div class="reponse">
                <strong>Réponse :</strong><br>
                {reponse_escaped}
            </div>
        </div>
"""
    
    html_content += """
    </div>
    
    <script>
        function filtrer() {
            const modeleFilter = document.getElementById('filter-modele').value;
            const techniqueFilter = document.getElementById('filter-technique').value;
            const searchText = document.getElementById('search').value.toLowerCase();
            
            const results = document.querySelectorAll('.result');
            let count = 0;
            
            results.forEach(result => {
                let show = true;
                
                if (modeleFilter && result.dataset.modele !== modeleFilter) {
                    show = false;
                }
                
                if (techniqueFilter && result.dataset.technique !== techniqueFilter) {
                    show = false;
                }
                
                if (searchText && !result.dataset.content.includes(searchText)) {
                    show = false;
                }
                
                result.style.display = show ? 'block' : 'none';
                if (show) count++;
            });
            
            console.log(count + ' resultats affiches');
        }
    </script>
</body>
</html>
"""
    
    with open(fichier_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"page html generee: {fichier_html}")
    print(f"ouverture dans le navigateur par defaut...")
    
    # ouvrir automatiquement dans le navigateur par defaut (windows + linux)
    import webbrowser
    import os
    
    fichier_complet = os.path.abspath(fichier_html)
    webbrowser.open('file://' + fichier_complet)
    
    print(f"si le navigateur ne s'ouvre pas automatiquement:")
    print(f"ouvre manuellement: {fichier_complet}")


if __name__ == "__main__":
    generer_html("resultats_complets.csv", "resultats.html")
