from generator import generate, GeneratorConfig
from renderer import render_svg, save_svg  # , save_png

import tomllib
import sys


if __name__ == "__main__":
    # Chargement de la configuration
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

    gen_config = app_config["generator"]
    rend_config = app_config["renderer"]

    # Generation du plan avec 1 argument pour la profondeur
    if len(sys.argv) > 1:
        try:
            depth = int(sys.argv[1])
        except ValueError:
            print("Profondeur invalide, retour a la valeur par defaut")
            depth = gen_config["max_depth"]

        config = GeneratorConfig(
            width=gen_config["width"],
            height=gen_config["height"],
            min_room_size=gen_config["min_room_size"],
            max_depth=depth,
            room_margin=gen_config["room_margin"],
        )

        plan = generate(config)

        # Creation du SVG et options de sauvegarde en SVG
        chemin: str = "plan.svg"
        svg = render_svg(plan=plan, title="Maison medievale", cfg=rend_config)
        save_svg(svg_str=svg, path=chemin)
        print(f"Fichier SVG cree sous {chemin}")
    else:
        print("Argument manquant pour la profondeur")
