# Structure du projet

## Prompts

Liste des prompts de base utilisés pour les tests.

Ce fichier contient l’ensemble des prompts adversariaux utilisés dans l’expérience.

---

## Résultats

Contient les résultats des expériences réalisées sur les différents modèles.

Les fichiers principaux sont :

- `resultats-proprietaires.csv`  
  Résultats obtenus sur les modèles propriétaires :
  - GPT-4
  - Claude Sonnet 4.5
  - DeepSeek v3

- `resultats_ollama.csv`  
  Résultats obtenus sur les modèles open source exécutés localement :
  - Llama
  - Mistral

- `resultats_complets.csv`  
  Fusion des deux fichiers précédents.

Ce fichier contient l'ensemble des résultats utilisés pour l'analyse.

---

# Scripts

Le dossier `scripts` contient plusieurs scripts permettant d'automatiser le pipeline expérimental.

## parse-to-csv

Convertit le document Word contenant les résultats des modèles propriétaires en fichier CSV.

Lors de l’expérimentation, les réponses des modèles propriétaires ont été copiées dans un document Word d'environ **260 pages**.

Ce script permet de :

- parser ce document
- extraire les réponses
- convertir les données dans un **CSV structuré exploitable**

---

## test_ollama

Ce script envoie automatiquement les prompts aux modèles open-source installés localement via **Ollama**.

Modèles utilisés :

- Llama
- Mistral

Le script :

1. lit les prompts dans `prompts.csv`
2. les envoie aux modèles
3. récupère les réponses
4. les stocke dans un CSV de résultats

Le fichier généré est : ```resultats_ollama.csv```

---

## generer_html

Ce script génère une interface HTML permettant de consulter facilement les résultats.

Il lit le fichier : ```resultats_complets.csv```

et génère une page : ```resultats.html```


Cette page permet :

- d’explorer les résultats
- de trier les réponses
- de comparer les modèles

Lire directement les résultats dans un CSV étant peu pratique, cette interface facilite l'analyse.

---

# Pipeline expérimental

Le pipeline du projet est le suivant :

1. Création du corpus de prompts (`prompts.csv`)
2. Test automatique sur les modèles open-source via `test_ollama`
3. Collecte manuelle des réponses des modèles propriétaires
4. Conversion du document Word via `parse-to-csv`
5. Fusion des résultats dans `resultats_complets.csv`
6. Visualisation via `generer_html`

---

# Modèles évalués

Le benchmark compare cinq modèles :

| Type | Modèle |
|-----|------|
| Propriétaire | GPT-4 |
| Propriétaire | Claude Sonnet 4.5 |
| Propriétaire | DeepSeek v3 |
| Open-source | Llama |
| Open-source | Mistral |


---

# Objectif

Le projet vise à :

- analyser la robustesse des LLM face aux attaques de jailbreak
- comparer les modèles propriétaires et open-source
- identifier les techniques d'attaque les plus efficaces
- proposer un benchmark reproductible pour la recherche en sécurité des LLM

---

# Auteurs

Projet réalisé dans le cadre d'un hackathon sur la sécurité des modèles de langage.

- Clément CONRIÉ  
- Thomas SCHAMING  
- Yanis LIU  
- Christ DIATHA  

---

# Licence

Projet open-source destiné à la recherche sur la sécurité des LLM.
