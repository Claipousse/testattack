#!/usr/bin/env python3

import csv

def fusionner_csvs(csv_ollama, csv_proprietaires, csv_final):
    """fusionne les resultats ollama et proprietaires dans un seul csv"""
    
    # lire ollama
    try:
        with open(csv_ollama, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            resultats_ollama = list(reader)
        print(f"  - ollama: {len(resultats_ollama)} lignes")
    except FileNotFoundError:
        print(f"warning: {csv_ollama} introuvable, on continue sans")
        resultats_ollama = []
    
    # lire proprietaires
    try:
        with open(csv_proprietaires, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            resultats_proprietaires = list(reader)
        print(f"  - proprietaires: {len(resultats_proprietaires)} lignes")
    except FileNotFoundError:
        print(f"erreur: {csv_proprietaires} introuvable")
        print("lance d'abord text_to_csv.py")
        return False
    
    # fusionner
    tous_resultats = resultats_ollama + resultats_proprietaires
    
    # trier par prompt_id puis par modele
    tous_resultats.sort(key=lambda x: (x['prompt_id'], x['modele']))
    
    # ecrire
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
    
    with open(csv_final, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tous_resultats)
    
    print(f"  - total: {len(tous_resultats)} lignes")
    return True


def main():
    """fonction principale"""
    
    print("=" * 70)
    print("fusion resultats ollama + proprietaires")
    print("=" * 70)
    print()
    
    csv_ollama = '../resultats/resultats_ollama.csv'
    csv_proprietaires = '../resultats/resultats_proprietaires.csv'
    csv_final = '../resultats/resultats_complets.csv'
    
    print("fusion en cours...")
    succes = fusionner_csvs(csv_ollama, csv_proprietaires, csv_final)
    
    if succes:
        print()
        print(f"fichier cree: {csv_final}")
        print()
        print("=" * 70)
        print("termine !")
        print("=" * 70)
    else:
        print()
        print("echec de la fusion")


if __name__ == "__main__":
    main()