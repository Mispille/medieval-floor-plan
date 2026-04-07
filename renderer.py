"""
Rendu SVG du FloorPlan medieval généré avec generator.py

API publique :
    render_svg(plan, title=None, seed=None) -> str
    save_svg(svg_str, path)
    save_png(svg_str, path)
"""

import cairosvg  # pyright: ignore[reportMissingTypeStubs]
from typing import Optional
from generator import FloorPlan, Room, Corridor

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

SCALE = 12  # px par cellule de grille
BG_COLOR = "#f5f0e8"  # fond parchemin
WALL_COLOR = "#1a1a1a"  # murs
CORRIDOR_COLOR = "#c4a882"  # couloirs (beige-brun)
WALL_W = 2  # px epaisseur mur
CORRIDOR_W = 8  # px largeur couloir


# ---------------------------------------------------------------------------
# Elements SVG internes
# ---------------------------------------------------------------------------


def _svg_background(w: int, h: int) -> str:
    return f'<rect width="{w}" height="{h}" fill="{BG_COLOR}"/>'


def _svg_corridor(c: Corridor) -> str:
    """Couloir en L : horizontal a y1, puis vertical a x2 (meme logique que ASCII)"""
    s = SCALE
    points = f"{c.x1 * s},{c.y1 * s} {c.x2 * s},{c.y1 * s} {c.x2 * s},{c.y2 * s}"
    return (
        f'<polyline points="{points}" fill="none" '
        f'stroke="{CORRIDOR_COLOR}" stroke-width="{CORRIDOR_W}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )


def _svg_room(room: Room) -> str:
    """Rectangle de la piece + label centre"""
    r = room.rect
    s = SCALE
    x, y, w, h = r.x * s, r.y * s, r.w * s, r.h * s
    cx, cy = x + w // 2, y + h // 2

    # Taille police adaptee a la largeur interieure de la piece
    inner_px = (r.w - 2) * s
    font_size = min(10, max(6, int(inner_px / max(len(room.room_type), 1) / 0.6)))

    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{BG_COLOR}" stroke="{WALL_COLOR}" stroke-width="{WALL_W}"/>',
            f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
            f'font-family="serif" font-size="{font_size}" fill="{WALL_COLOR}">'
            f"{room.room_type}</text>",
        ]
    )


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


def render_svg(plan: FloorPlan, title: Optional[str] = None) -> str:
    """Retourne une chaine SVG complete representant le plan"""
    W = plan.width * SCALE
    H = plan.height * SCALE
    margin_top = 24 if title else 4
    total_h = H + margin_top

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">',
        _svg_background(W, total_h),
    ]

    if title:
        parts.append(
            f'<text x="{W // 2}" y="16" text-anchor="middle" '
            f'font-family="serif" font-size="14" font-style="italic" '
            f'fill="{WALL_COLOR}">{title}</text>'
        )

    parts.append(f'<g transform="translate(0,{margin_top})">')

    # Couloirs d'abord — les pieces seront dessinees par-dessus
    # ce qui cache automatiquement la partie des couloirs a l'interieur des pieces
    for corridor in plan.corridors:
        parts.append(_svg_corridor(corridor))

    for room in plan.rooms:
        parts.append(_svg_room(room))

    parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)


def save_svg(svg_str: str, path: str) -> None:
    """Sauvegarde le SVG dans un fichier"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_str)


def save_png(svg_str: str, path: str) -> None:
    """Exporte le SVG en PNG via cairosvg"""
    cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to=path)  # pyright: ignore[reportUnknownMemberType]
