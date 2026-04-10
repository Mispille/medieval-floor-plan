import tomllib
from flask import Flask, render_template, request

from generator import GeneratorConfig, generate
from renderer import render_svg

app = Flask(__name__)


@app.route("/")
def index():
    # Import de la configuration
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

    gen_config = app_config["generator"]
    rend_config = app_config["renderer"]

    seed_param = request.args.get("seed")
    seed = int(seed_param) if seed_param is not None else None

    config = GeneratorConfig(
        width=int(request.args.get("width", gen_config["width"])),
        height=int(request.args.get("height", gen_config["height"])),
        min_room_size=int(
            request.args.get("min_room_size", gen_config["min_room_size"])
        ),
        max_depth=int(request.args.get("max_depth", gen_config["max_depth"])),
        room_margin=int(request.args.get("room_margin", gen_config["room_margin"])),
        seed=seed,
    )

    plan = generate(config)

    svg: str = render_svg(plan=plan, title="Maison medievale", cfg=rend_config)

    return render_template(
        "index.html",
        svg=svg,
        seed=plan.seed,
        width=config.width,
        height=config.height,
        min_room_size=config.min_room_size,
        max_depth=config.max_depth,
        room_margin=config.room_margin,
    )
