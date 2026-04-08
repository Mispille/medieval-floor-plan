from generator import generate, GeneratorConfig
from renderer import render_svg, save_svg  # , save_png

import sys


if __name__ == "__main__":
    # Generation du plan avec 1 argument pour la profondeur (3 par defaut)
    if len(sys.argv) > 1:
        try:
            depth = int(sys.argv[1])
        except ValueError:
            print("Profondeur invalide, 3 par defaut")
            depth = 3

        config = GeneratorConfig(max_depth=depth)
        plan = generate(config)

        # Creation du SVG et options de sauvegarde en SVG ou PNG
        chemin: str = "plan.svg"
        svg = render_svg(plan=plan, title="Maison medievale")
        save_svg(svg_str=svg, path=chemin)
        print(f"Fichier SVG cree sous {chemin}")
    else:
        print("Argument manquant pour la profondeur")
