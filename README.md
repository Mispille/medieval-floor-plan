# Générateur de plans de maisons médiévales aléatoires

Génère aléatoirement des plans de maisons médiévales pour vos parties de jeu de rôle

Accessible depuis un navigateur web, sans installation complexe

---

## Utilisation

1. Lancez l'application (voir Installation ci-dessous)
2. Ouvrez [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. Ajustez les curseurs selon vos besoins :
   - **Largeur / Hauteur** — dimensions
   - **Taille min pièce** — taille min de chaque pièce
   - **Profondeur** — nombre pièces générées
   - **Marge des murs** — espace entre pièces
4. Cliquez sur **Appliquer** pour générer avec le même seed, **Reroll** pour un nouveau plan aléatoire
5. Le champ **Seed** permet de retrouver un plan déjà généré en réutilisant la même valeur
6. Cliquez sur **Exporter en PNG** pour télécharger le plan

---

## Installation

**Prérequis :**
* Python 3.11 ou supérieur
* Git *(sauf si vous téléchargez manuellement le code source)*

```bash
# Clonez le projet
git clone https://github.com/Mispille/medieval-floor-plan.git
cd medieval-floor-plan

# Créez et activez l'environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows (ajoutez .ps1 si Powershell)

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

---

## Structure

| Fichier        | Rôle                               |
| -------------- | ---------------------------------- |
| `main.py`      | Point d'entrée — lance le serveur  |
| `app.py`       | Serveur web — gère les requêtes    |
| `generator.py` | Algorithme BSP — génère les pièces |
| `renderer.py`  | Produit le SVG à partir du plan    |
| `config.toml`  | Valeurs par défaut des paramètres  |
