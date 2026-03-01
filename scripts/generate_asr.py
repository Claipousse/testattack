#!/usr/bin/env python3

import csv
from collections import defaultdict

def calculer_asr(fichier_annote):
    """calcule l'attack success rate a partir des resultats annotes"""
    
    print("=" * 70)
    print("CALCUL DE L'ATTACK SUCCESS RATE (ASR)")
    print("=" * 70)
    print()
    
    # lire les resultats annotes
    print(f"lecture de {fichier_annote}...")
    with open(fichier_annote, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        resultats = list(reader)
    
    print(f"{len(resultats)} resultats annotes charges")
    print()
    
    # initialiser les compteurs
    stats_globales = {'total': 0, 'jailbreak': 0, 'refus': 0}
    stats_par_modele = defaultdict(lambda: {'total': 0, 'jailbreak': 0, 'refus': 0})
    stats_par_technique = defaultdict(lambda: {'total': 0, 'jailbreak': 0, 'refus': 0})
    stats_croisees = defaultdict(lambda: defaultdict(lambda: {'total': 0, 'jailbreak': 0, 'refus': 0}))
    
    # parcourir les resultats
    for resultat in resultats:
        modele = resultat['modele']
        technique = resultat['technique']
        classification = resultat['classification']
        
        # stats globales
        stats_globales['total'] += 1
        if classification == 'JAILBREAK':
            stats_globales['jailbreak'] += 1
        else:
            stats_globales['refus'] += 1
        
        # stats par modele
        stats_par_modele[modele]['total'] += 1
        if classification == 'JAILBREAK':
            stats_par_modele[modele]['jailbreak'] += 1
        else:
            stats_par_modele[modele]['refus'] += 1
        
        # stats par technique
        stats_par_technique[technique]['total'] += 1
        if classification == 'JAILBREAK':
            stats_par_technique[technique]['jailbreak'] += 1
        else:
            stats_par_technique[technique]['refus'] += 1
        
        # stats croisees (modele x technique)
        stats_croisees[modele][technique]['total'] += 1
        if classification == 'JAILBREAK':
            stats_croisees[modele][technique]['jailbreak'] += 1
        else:
            stats_croisees[modele][technique]['refus'] += 1
    
    # calculer les asr
    def calculer_taux(stats):
        if stats['total'] == 0:
            return 0.0
        return (stats['jailbreak'] / stats['total']) * 100
    
    # afficher les resultats
    print("=" * 70)
    print("RESULTATS GLOBAUX")
    print("=" * 70)
    print()
    print(f"total de tests : {stats_globales['total']}")
    print(f"jailbreaks reussis : {stats_globales['jailbreak']} ({calculer_taux(stats_globales):.1f}%)")
    print(f"refus : {stats_globales['refus']} ({stats_globales['refus']/stats_globales['total']*100:.1f}%)")
    print()
    
    print("=" * 70)
    print("ASR PAR MODELE")
    print("=" * 70)
    print()
    print(f"{'Modele':<25} {'Tests':<10} {'Jailbreaks':<15} {'ASR':<10}")
    print("-" * 70)
    
    # trier par asr decroissant
    modeles_tries = sorted(stats_par_modele.items(), key=lambda x: calculer_taux(x[1]), reverse=True)
    
    for modele, stats in modeles_tries:
        asr = calculer_taux(stats)
        print(f"{modele:<25} {stats['total']:<10} {stats['jailbreak']:<15} {asr:>6.1f}%")
    
    print()
    
    print("=" * 70)
    print("ASR PAR TECHNIQUE")
    print("=" * 70)
    print()
    print(f"{'Technique':<25} {'Tests':<10} {'Jailbreaks':<15} {'ASR':<10}")
    print("-" * 70)
    
    techniques_triees = sorted(stats_par_technique.items(), key=lambda x: calculer_taux(x[1]), reverse=True)
    
    for technique, stats in techniques_triees:
        asr = calculer_taux(stats)
        print(f"{technique:<25} {stats['total']:<10} {stats['jailbreak']:<15} {asr:>6.1f}%")
    
    print()
    
    print("=" * 70)
    print("ASR CROISE (MODELE × TECHNIQUE)")
    print("=" * 70)
    print()
    
    # tableau croise
    techniques = sorted(stats_par_technique.keys())
    modeles = sorted(stats_par_modele.keys())
    
    # en-tete
    print(f"{'Modele':<25}", end="")
    for technique in techniques:
        print(f"{technique:<15}", end="")
    print()
    print("-" * (25 + 15 * len(techniques)))
    
    # lignes
    for modele in modeles:
        print(f"{modele:<25}", end="")
        for technique in techniques:
            stats = stats_croisees[modele][technique]
            asr = calculer_taux(stats)
            print(f"{asr:>6.1f}%        ", end="")
        print()
    
    print()
    
    # generer le fichier csv des stats
    print("generation du fichier stats_asr.csv...")
    
    with open('../resultats/stats_asr.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # stats par modele
        writer.writerow(['# ASR PAR MODELE'])
        writer.writerow(['Modele', 'Total tests', 'Jailbreaks', 'Refus', 'ASR (%)'])
        for modele, stats in modeles_tries:
            asr = calculer_taux(stats)
            writer.writerow([modele, stats['total'], stats['jailbreak'], stats['refus'], f"{asr:.1f}"])
        
        writer.writerow([])
        
        # stats par technique
        writer.writerow(['# ASR PAR TECHNIQUE'])
        writer.writerow(['Technique', 'Total tests', 'Jailbreaks', 'Refus', 'ASR (%)'])
        for technique, stats in techniques_triees:
            asr = calculer_taux(stats)
            writer.writerow([technique, stats['total'], stats['jailbreak'], stats['refus'], f"{asr:.1f}"])
        
        writer.writerow([])
        
        # tableau croise
        writer.writerow(['# TABLEAU CROISE (MODELE × TECHNIQUE)'])
        header = ['Modele'] + techniques
        writer.writerow(header)
        for modele in modeles:
            row = [modele]
            for technique in techniques:
                asr = calculer_taux(stats_croisees[modele][technique])
                row.append(f"{asr:.1f}")
            writer.writerow(row)
    
    print("✓ fichier genere : ../resultats/stats_asr.csv")
    print()
    
    print("=" * 70)
    print("TERMINÉ")
    print("=" * 70)
    print()
    print("fichiers generes :")
    print("  - ../resultats/resultats_annotes.csv (resultats avec annotations)")
    print("  - ../resultats/stats_asr.csv (tableaux asr pour le rapport)")
    print()
    print("tu peux maintenant :")
    print("  1. copier les tableaux dans ton rapport")
    print("  2. analyser les resultats dans la section iv")
    print("  3. rediger la conclusion")


if __name__ == "__main__":
    calculer_asr("../resultats/resultats_annotes.csv")
