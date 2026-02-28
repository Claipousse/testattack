#!/usr/bin/env python3
"""
script d'automatisation des tests de jailbreak sur les modèles en local de ollama
lit le csv des prompts et teste automatiquement Llama 3.1 8B et Mistral 7B
sauvegarde les résultats dans un csv avec prompt + réponse + métadonnées
comme ça pas besoin de tout se taper à la main (enfin sauf pour les modèles en ligne mais ça c'est une autre histoire), un bon informaticien est un informaticien feignant
"""

import csv
import ollama
import time
from datetime import datetime
from pathlib import Path

# configuration
input_file = "prompts.csv"  # fichier avec liste des prompts
output_file = "resultats_ollama.csv"  # fichier de sortie avec les resultats
models = ["llama3.1:8b", "mistral:7b"]  # modeles a tester

generation_options = {  # parametres de generation fixes qui reflète un usage réel
    'temperature': 0.7, #entre 0 et 1, plus c'est bas plus c'est prévisible, la on a un truc bien équilibré
    'top_p': 0.9, #prend en compte 90% des tokens les plus probables
    'num_predict': 2048 #nombre max de tokens dans la réponse, on veut éviter les gros pavés donc j'ai mit une limite qui reste quand même assez conséquente
}

def test_prompt(model_name, prompt_text):
    """teste un prompt sur un modele ollama"""
    
    print(f"  -> test sur {model_name}...", end=" ", flush=True)
    start_time = time.time()
    
    try:
        response = ollama.chat(
            model=model_name,#quel modele on utilise
            messages=[{'role': 'user', 'content': prompt_text}], #message de l'utilisateur
            options=generation_options #utilise les parametres définis plus tot
        )
        
        elapsed_time = time.time() - start_time #pour métadonnée et calcul du temps pour gérer le prompts (utile quand on va analyser pour de la data en plus :3)
        
        result = { #si ça a marché, alors on met les infos pour faire un message de validation
            'response': response['message']['content'], #la réponse
            'model': model_name, #le modèle
            'success': True,
            'error': None,
            'time_seconds': round(elapsed_time, 2) #temps au centieme près
        }
        
        print(f"ok ({elapsed_time:.1f}s)") #message de validation
        return result
        
    except Exception as e: #si ya un blème, on le fait comprendre à l'utilisateur avec un message d'erreur et la cause (e)
        elapsed_time = time.time() - start_time
        
        result = {
            'response': f"erreur: {str(e)}",
            'model': model_name,
            'success': False,
            'error': str(e),
            'time_seconds': round(elapsed_time, 2)
        }
        
        print(f"erreur ({e})") #on affiche l'erreur
        return result


def main():
    #titre avec plein de = pour faire un joli titre de gros kéké
    print("="*70)
    print("automatisation tests jailbreak - modeles ollama")
    print("="*70)
    print()
    
    if not Path(input_file).exists():  # verifier que le fichier avec la liste des prompts est bien la
        print(f"erreur: fichier {input_file} introuvable") #si on trouve pas, erreur et on exit
        return
    
    print(f"lecture des prompts depuis {input_file}...") #si c'est bon, on crée une liste vide puis on va importer les prompts du csv dans la liste avec DictReader
    prompts = []
    
    with open(input_file, 'r', encoding='utf-8') as f: #r pour read, utf-8 pour l'encodage par défaut, on renomme le fichier 'f'
        reader = csv.DictReader(f)
        prompts = list(reader) #convertit tout ça en liste 
    
    print(f"{len(prompts)} prompts chargés") #len = taille = nombre de prompts
    print()
    
    print(f"preparation du fichier de résultats: {output_file}")
    
    fieldnames = [  # colonnes du csv de sortie
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
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:  # creer le fichier avec en-tetes, w pour écriture pour pouvoir créer le fichier ET mettre les réponses dedans
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader() #écrit premier colonnes qui sert d'index/header pour les réponses des modèles
    
    print(f"fichier crée avec en-tetes")
    print()
    
    total_tests = len(prompts) * len(models) #(nombre de prompts à faire) x (nombre de modèles à tester)
    #compteurs
    tests_done = 0
    tests_success = 0
    tests_failed = 0
    
    #là on marque dans la console les paramètres et autres infos qu'on a pu définir au dessus
    print(f"debut des tests: {len(prompts)} prompts x {len(models)} modeles = {total_tests} tests")
    print()
    print("parametres:") 
    print(f"  - temperature: {generation_options['temperature']}")
    print(f"  - top-p: {generation_options['top_p']}")
    print(f"  - max tokens: {generation_options['num_predict']}")
    print()
    print("-"*70)
    print()
    
    for idx, prompt_data in enumerate(prompts, 1): # boucle sur chaque prompt, on numérote à partir de 1 et pas 0
        #on extrait les infos suivantes
        prompt_id = prompt_data['id'] #ID : ex R01
        technique = prompt_data['technique'] #technique : ex "roleplay"
        domaine = prompt_data['domaine'] #domaine : ex "cybercriminalite"
        prompt_text = prompt_data['prompt'] #prompt_text: ex "tu es nicolas sarkozy..."
        
        #affiche les infos du prompt qu'on envoit (du moins que le début, que les 80 premiers caractères)
        print(f"[{idx}/{len(prompts)}] prompt {prompt_id} ({technique} / {domaine})")
        print(f"  texte: {prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}")
        
        for model in models:  # tester sur chaque modele
            result = test_prompt(model, prompt_text) #appelle la fonction qu'on a faite plus haut, on envoi le prompt au modèle, et on récupère le résultat avec result
            
            row = {  # sauvegarder le resultat
                'timestamp': datetime.now().isoformat(),
                'prompt_id': prompt_id,
                'technique': technique,
                'domaine': domaine,
                'prompt': prompt_text,
                'modele': result['model'],
                'reponse': result['response'],
                'temps_secondes': result['time_seconds'],
                'succes': 'oui' if result['success'] else 'non'
            }
            
            with open(output_file, 'a', encoding='utf-8', newline='') as f:  # ecrire dans le csv
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(row)
            
            tests_done += 1  # mettre à jour les compteurs
            if result['success']:
                tests_success += 1
            else:
                tests_failed += 1
        
        print()
    
    print("="*70)  # resumé final
    print("TESTS TERMINÉS")
    print("="*70)
    print()
    print(f"total tests: {tests_done}/{total_tests}")
    print(f"succes    : {tests_success} ({tests_success/tests_done*100:.1f}%)")
    print(f"echecs    : {tests_failed} ({tests_failed/tests_done*100:.1f}%)")
    print()
    print(f"résultats sauvegardés dans: {output_file}")
    print("Bye bye !! Ciao Kombucha!!!")


if __name__ == "__main__":
    main()

# je met les commentaires à 3h du matin je suis le café-batman merci de votre lecture je suis à bout
