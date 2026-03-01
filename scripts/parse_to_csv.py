#!/usr/bin/env python3

import csv
import re
from datetime import datetime

def parser_fichier_word(fichier_txt):
    """parse le fichier texte (qui lui meme vient d'un word) vers un csv et extrait les reponses"""
    
    with open(fichier_txt, 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # nettoyer les espaces en trop
    # remplacer les espaces multiples par un seul espace
    contenu = re.sub(r' +', ' ', contenu)
    # nettoyer les sauts de ligne multiples mais garder au moins un
    contenu = re.sub(r'\n{4,}', '\n\n\n', contenu)
    
    resultats = []
    
    # pattern plus flexible pour trouver chaque bloc de prompt
    # accepte n'importe quel nombre de = (minimum 10) et des espaces variables
    pattern_bloc = r'={10,}\s*PROMPT\s+([A-Z]+\d+)\s+-\s+(\w+)\s+-\s+(\w+)\s*={10,}\s*(.*?)(?=={10,}\s*PROMPT|\Z)'
    
    blocs = re.finditer(pattern_bloc, contenu, re.DOTALL)
    
    compteur = 0
    for match in blocs:
        prompt_id = match.group(1)
        technique = match.group(2)
        domaine = match.group(3)
        bloc_contenu = match.group(4)
        
        compteur += 1
        print(f"[{compteur}/60] traitement prompt {prompt_id}...", end=" ", flush=True)
        
        # extraire le texte du prompt (entre le header et "--- REPONSE")
        # pattern flexible qui accepte des espaces variables
        match_prompt = re.search(r'^(.*?)(?=\s*-{2,}\s*REPONSE)', bloc_contenu, re.DOTALL)
        if not match_prompt:
            print(f"warning: prompt non trouve")
            continue
        
        prompt_text = match_prompt.group(1).strip()
        
        # extraire les 3 reponses avec patterns flexibles
        # GPT-4 (accepte "GPT-4", "GPT 4", "gpt-4", etc.)
        match_gpt = re.search(r'-{2,}\s*REPONSE\s+GPT[-\s]?4\s*-{2,}\s*(.*?)(?=\s*-{2,}\s*REPONSE\s+CLAUDE|\Z)', bloc_contenu, re.DOTALL | re.IGNORECASE)
        # Claude (accepte "CLAUDE", "claude", etc.)
        match_claude = re.search(r'-{2,}\s*REPONSE\s+CLAUDE\s*-{2,}\s*(.*?)(?=\s*-{2,}\s*REPONSE\s+DEEPSEEK|\Z)', bloc_contenu, re.DOTALL | re.IGNORECASE)
        # DeepSeek (accepte "DEEPSEEK", "deepseek", "DeepSeek", etc.)
        match_deepseek = re.search(r'-{2,}\s*REPONSE\s+DEEPSEEK\s*-{2,}\s*(.*?)(?=\s*={10,}|\Z)', bloc_contenu, re.DOTALL | re.IGNORECASE)
        
        reponse_gpt = match_gpt.group(1).strip() if match_gpt else ""
        reponse_claude = match_claude.group(1).strip() if match_claude else ""
        reponse_deepseek = match_deepseek.group(1).strip() if match_deepseek else ""
        
        # verifier que les reponses ne sont pas vides
        if not reponse_gpt:
            print(f"warning gpt vide", end=" ")
        if not reponse_claude:
            print(f"warning claude vide", end=" ")
        if not reponse_deepseek:
            print(f"warning deepseek vide", end=" ")
        
        # ajouter les 3 lignes (une par modele)
        timestamp = datetime.now().isoformat()
        
        if reponse_gpt:
            resultats.append({
                'timestamp': timestamp,
                'prompt_id': prompt_id,
                'technique': technique,
                'domaine': domaine,
                'prompt': prompt_text,
                'modele': 'gpt-4',
                'reponse': reponse_gpt,
                'temps_secondes': 0,
                'succes': 'oui'
            })
        
        if reponse_claude:
            resultats.append({
                'timestamp': timestamp,
                'prompt_id': prompt_id,
                'technique': technique,
                'domaine': domaine,
                'prompt': prompt_text,
                'modele': 'claude-sonnet-4.5',
                'reponse': reponse_claude,
                'temps_secondes': 0,
                'succes': 'oui'
            })
        
        if reponse_deepseek:
            resultats.append({
                'timestamp': timestamp,
                'prompt_id': prompt_id,
                'technique': technique,
                'domaine': domaine,
                'prompt': prompt_text,
                'modele': 'deepseek-v3',
                'reponse': reponse_deepseek,
                'temps_secondes': 0,
                'succes': 'oui'
            })
        
        print("ok")
    
    return resultats


def ecrire_csv(resultats, fichier_csv):
    """ecrit les resultats dans un csv"""
    
    fieldnames = [
        'timestamp',
        'prompt_id',
        'technique',
        'domaine',
        'prompt',
        'modele',
        'reponse',
        'temps_secondes',
        'succes'
    ]
    
    with open(fichier_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resultats)


def fusionner_csvs(csv_ollama, csv_proprietaires, csv_final):
    """fusionne les resultats ollama et proprietaires dans un seul csv"""
    
    # lire ollama
    try:
        with open(csv_ollama, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            resultats_ollama = list(reader)
    except FileNotFoundError:
        print(f"warning: {csv_ollama} introuvable, on continue sans")
        resultats_ollama = []
    
    # lire proprietaires
    with open(csv_proprietaires, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        resultats_proprietaires = list(reader)
    
    # fusionner
    tous_resultats = resultats_ollama + resultats_proprietaires
    
    # trier par prompt_id puis par modele
    tous_resultats.sort(key=lambda x: (x['prompt_id'], x['modele']))
    
    # ecrire
    ecrire_csv(tous_resultats, csv_final)


def main():
    """fonction principale"""
    
    print("=" * 70)
    print("conversion fichier word -> csv")
    print("=" * 70)
    print()
    
    fichier_input = "../tests_online.txt"  # nom du fichier txt converti
    
    # parser le fichier txt
    print(f"lecture de {fichier_input}...")
    print()
    
    try:
        resultats = parser_fichier_word(fichier_input)
    except FileNotFoundError:
        print(f"erreur: fichier {fichier_input} introuvable")
        print()
        print("il faut d'abord convertir ton fichier word en .txt :")
        print("1. ouvre ton fichier word dans libreoffice")
        print("2. fichier -> enregistrer sous")
        print("3. format: texte (.txt)")
        print("4. renomme en 'tests_online.txt'")
        print("5. place-le dans le dossier ~/jailbreak_tests/")
        return
    
    print()
    print(f"trouve {len(resultats)} reponses")
    print(f"  - gpt-4: {sum(1 for r in resultats if r['modele'] == 'gpt-4')}")
    print(f"  - claude: {sum(1 for r in resultats if 'claude' in r['modele'])}")
    print(f"  - deepseek: {sum(1 for r in resultats if 'deepseek' in r['modele'])}")
    print()
    
    # ecrire le csv des tests proprietaires
    print("ecriture de resultats_proprietaires.csv...")
    ecrire_csv(resultats, '../resultats/resultats_proprietaires.csv')
    print("ok")
    print()
    
    # fusionner avec ollama si disponible
    try:
        print("fusion avec resultats_ollama.csv...")
        fusionner_csvs('../resultats/resultats_ollama.csv', '../resultats/resultats_proprietaires.csv', '../resultats/resultats_complets.csv')
        print("ok")
        print()
        print("fichiers crees:")
        print("  - resultats_proprietaires.csv (180 lignes - gpt/claude/deepseek)")
        print("  - resultats_complets.csv (300 lignes - tous les modeles)")
    except FileNotFoundError:
        print("resultats_ollama.csv introuvable")
        print("seul resultats_proprietaires.csv a ete cree")
    
    print()
    print("=" * 70)
    print("termine !")
    print("=" * 70)


if __name__ == "__main__":
    main()
