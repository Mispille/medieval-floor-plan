# Générateur de plans de maisons médiévales aléatoires

Génère aléatoirement des plans de maisons médiévales pour vos parties de jeu de rôle
Accessible depuis un navigateur web, sans installation complexe

---

## Utilisation

1. Lancez l'application (voir Installation ci-dessous)
2. Ouvrez [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. Ajustez les curseurs selon vos besoins :
   - **Largeur / Hauteur** — dimensions du plan
   - **Taille min pièce** — taille minimale de chaque pièce
   - **Profondeur** — nombre de pièces générées
   - **Marge des murs** — espace entre les pièces
4. Cliquez sur **Appliquer** pour générer, **Reroll** pour un nouveau plan aléatoire
5. Le champ **Seed** permet de retrouver un plan déjà généré en réutilisant le même numéro
6. Cliquez sur **Exporter en PNG** pour télécharger le plan

---

## Installation

**Prérequis :** Python 3.11 ou supérieur

```bash
# Cloner le projet
git clone https://github.com/Mispille/medieval-floor-plan.git
cd medieval-floor-plan

# Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

---

## Structure du projet

| Fichier        | Rôle                               |
| -------------- | ---------------------------------- |
| `main.py`      | Point d'entrée — lance le serveur  |
| `app.py`       | Serveur web — gère les requêtes    |
| `generator.py` | Algorithme BSP — génère les pièces |
| `renderer.py`  | Produit le SVG à partir du plan    |
| `config.toml`  | Valeurs par défaut des paramètres  |
