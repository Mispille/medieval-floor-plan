import cairosvg
from flask import Flask, render_template, send_file

import tomllib
import io

from generator import generate, GeneratorConfig
from renderer import render_svg

app = Flask(__name__)

current_svg: str = ""


@app.route("/")
def index():
    global current_svg

    # Import de la configuration
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

    gen_config = app_config["generator"]
    rend_config = app_config["renderer"]

    config = GeneratorConfig(
        width=gen_config["width"],
        height=gen_config["height"],
        min_room_size=gen_config["min_room_size"],
        max_depth=gen_config["max_depth"],
        room_margin=gen_config["room_margin"],
    )

    plan = generate(config)

    svg: str = render_svg(plan=plan, title="Maison medievale", cfg=rend_config)
    current_svg = svg

    return render_template("index.html", svg=svg)


@app.route("/export")
def export_png():
    buffer = io.BytesIO()
    cairosvg.svg2png(bytestring=current_svg.encode("utf-8"), write_to=buffer)
    buffer.seek(0)
    return send_file(
        path_or_file=buffer,
        as_attachment=True,
        mimetype="image/png",
        download_name="maison.png",
    )


if __name__ == "__main__":
    app.run(debug=True)
