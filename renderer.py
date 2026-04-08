"""
Rendu SVG du FloorPlan medieval généré avec generator.py

API publique :
    render_svg(plan, title=None, cfg=None) -> str
"""

from typing import Optional

from generator import Corridor, FloorPlan, Room

# ---------------------------------------------------------------------------
# Elements SVG internes
# ---------------------------------------------------------------------------


def _svg_background(w: int, h: int, bg) -> str:
    return f'<rect width="{w}" height="{h}" fill="{bg}"/>'


def _svg_corridor(c: Corridor, scale: int, corr_col, corr_w: int) -> str:
    """Couloir en L : horizontal a y1, puis vertical a x2 (meme logique que ASCII)"""
    s = scale
    points = f"{c.x1 * s},{c.y1 * s} {c.x2 * s},{c.y1 * s} {c.x2 * s},{c.y2 * s}"
    return (
        f'<polyline points="{points}" fill="none" '
        f'stroke="{corr_col}" stroke-width="{corr_w}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )


def _svg_room(room: Room, scale: int, bg, wall_col, wall_w) -> str:
    """Rectangle de la piece + label centre"""
    r = room.rect
    s = scale
    x, y, w, h = r.x * s, r.y * s, r.w * s, r.h * s
    cx, cy = x + w // 2, y + h // 2

    # Taille police adaptee a la largeur interieure de la piece
    inner_px = (r.w - 2) * s
    font_size = min(10, max(6, int(inner_px / max(len(room.room_type), 1) / 0.6)))

    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{bg}" stroke="{wall_col}" stroke-width="{wall_w}"/>',
            f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
            f'font-family="serif" font-size="{font_size}" fill="{wall_col}">'
            f"{room.room_type}</text>",
        ]
    )


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


def render_svg(
    plan: FloorPlan, title: Optional[str] = None, cfg: Optional[dict] = None
) -> str:
    """Retourne une chaine SVG complete representant le plan"""

    # Chargement configuration
    SCALE = cfg["SCALE"] if cfg else 12
    BG_COLOR = cfg["BG_COLOR"] if cfg else "#f5f0e8"
    WALL_COLOR = cfg["WALL_COLOR"] if cfg else "#1a1a1a"
    CORRIDOR_COLOR = cfg["CORRIDOR_COLOR"] if cfg else "#c4a882"
    WALL_W = cfg["WALL_W"] if cfg else 2
    CORRIDOR_W = cfg["CORRIDOR_W"] if cfg else 8

    W = plan.width * SCALE
    H = plan.height * SCALE
    margin_top = 24 if title else 4
    total_h = H + margin_top

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">',
        _svg_background(W, total_h, bg=BG_COLOR),
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
        parts.append(
            _svg_corridor(
                corridor, scale=SCALE, corr_col=CORRIDOR_COLOR, corr_w=CORRIDOR_W
            )
        )

    for room in plan.rooms:
        parts.append(
            _svg_room(
                room, scale=SCALE, bg=BG_COLOR, wall_col=WALL_COLOR, wall_w=WALL_W
            )
        )

    parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)
