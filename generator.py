"""
Générateur de plan de maison médiévale en Binary Space Partitioning (BSP)

API publique :
    generate(config) -> FloorPlan
    FloorPlan.rooms   : list[Room]
    FloorPlan.corridors : list[Corridor]
"""

import random
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

ROOM_TYPES = [
    "Grande Salle",
    "Chambre",
    "Cuisine",
    "Cellier",
    "Chapelle",
    "Bibliothèque",
    "Armurerie",
    "Atelier",
    "Garde-manger",
    "Écurie",
    "Cave",
    "Forge",
]


@dataclass
class Rect:
    x: int  # Position du rectangle
    y: int
    w: int  # Largeur et hauteur du rectangle
    h: int

    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def area(self) -> int:
        return self.w * self.h


@dataclass
class Room:
    rect: Rect
    room_type: str  # Nom de la pièce
    id: int


@dataclass
class Corridor:
    """Couloir entre deux pièces"""

    x1: int  # Début du couloir
    y1: int
    x2: int  # Fin du couloir
    y2: int
    room_id_a: int = 0
    room_id_b: int = 0


@dataclass
class FloorPlan:
    rooms: list[Room]
    corridors: list[Corridor]
    width: int
    height: int


@dataclass
class GeneratorConfig:
    width: int = 72  # Largeur grille ASCII - 72 en v1
    height: int = 48  # Hauteur grille ASCII - 48 en v1
    min_room_size: int = 8  # Taille minimale d'une pièce
    max_depth: int = 5  # Profondeur récursion du BSP recursion → Gère nb pièces
    room_margin: int = 1  # Gap entre murs et rectangles
    seed: Optional[int] = None


# ---------------------------------------------------------------------------
# Algos internes au BSP (en cours d'apprentissage, va évoluer pour optimisation)
# ---------------------------------------------------------------------------


class _BSPNode:
    __slots__ = ("rect", "left", "right", "room")

    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.left: Optional["_BSPNode"] = None
        self.right: Optional["_BSPNode"] = None
        self.room: Optional[Room] = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def _split(node: _BSPNode, depth: int, min_size: int, max_depth: int) -> None:
    """Séparation récursive de chaque node jusqu'à max_depth ou taille mini atteinte"""
    if depth >= max_depth:
        return

    rect = node.rect
    can_h = rect.h >= min_size * 2  # coupe horizontale (split la hauteur)
    can_v = rect.w >= min_size * 2  # coupe verticale   (split la largeur)

    if not can_h and not can_v:
        return

    if can_h and can_v:
        horizontal = random.random() < 0.5
    else:
        horizontal = can_h

    if horizontal:
        cut = random.randint(min_size, rect.h - min_size)
        node.left = _BSPNode(Rect(rect.x, rect.y, rect.w, cut))
        node.right = _BSPNode(Rect(rect.x, rect.y + cut, rect.w, rect.h - cut))
    else:
        cut = random.randint(min_size, rect.w - min_size)
        node.left = _BSPNode(Rect(rect.x, rect.y, cut, rect.h))
        node.right = _BSPNode(Rect(rect.x + cut, rect.y, rect.w - cut, rect.h))

    _split(node.left, depth + 1, min_size, max_depth)
    _split(node.right, depth + 1, min_size, max_depth)


def _place_rooms(
    node: _BSPNode, margin: int, rooms: list[Room], counter: list[int]
) -> None:
    """Assigne une pièce à chaque node feuille"""
    if node.is_leaf:
        r = node.rect
        rx = r.x + margin
        ry = r.y + margin
        rw = r.w - margin * 2
        rh = r.h - margin * 2
        if rw >= 3 and rh >= 3:
            room = Room(
                rect=Rect(rx, ry, rw, rh),
                room_type=random.choice(ROOM_TYPES),
                id=counter[0],
            )
            counter[0] += 1
            node.room = room
            rooms.append(room)
        return

    if node.left:
        _place_rooms(node.left, margin, rooms, counter)
    if node.right:
        _place_rooms(node.right, margin, rooms, counter)


def _nearest_room(node: _BSPNode) -> Optional[Room]:
    """Retourne toute pièce atteignable depuis un node"""
    if node.is_leaf:
        return node.room
    left = _nearest_room(node.left) if node.left else None
    right = _nearest_room(node.right) if node.right else None
    return left or right


def _connect(node: _BSPNode, corridors: list[Corridor]) -> None:
    """Connecte les sous-nodes avec un "Corridor" (couloir)"""
    if node.is_leaf:
        return
    if node.left:
        _connect(node.left, corridors)
    if node.right:
        _connect(node.right, corridors)

    left_room = _nearest_room(node.left) if node.left else None
    right_room = _nearest_room(node.right) if node.right else None

    if left_room and right_room:
        lc = left_room.rect.center()
        rc = right_room.rect.center()
        corridors.append(Corridor(lc[0], lc[1], rc[0], rc[1], left_room.id, right_room.id))


# ---------------------------------------------------------------------------
# API accessible publiquement
# ---------------------------------------------------------------------------


def generate(config: Optional[GeneratorConfig] = None) -> FloorPlan:
    """Retourne un "FloorPlan" d'une maison médiévale aléatoire"""
    if config is None:
        config = GeneratorConfig()

    rng_seed = config.seed if config.seed is not None else random.randint(0, 2**32)
    random.seed(rng_seed)

    root = _BSPNode(Rect(0, 0, config.width, config.height))
    _split(root, 0, config.min_room_size, config.max_depth)

    rooms: list[Room] = []
    counter = [0]
    _place_rooms(root, config.room_margin, rooms, counter)

    corridors: list[Corridor] = []
    _connect(root, corridors)

    return FloorPlan(
        rooms=rooms, corridors=corridors, width=config.width, height=config.height
    )


# ---------------------------------------------------------------------------
# Rendu ASCII - Test visuel pour validation BSP: Terminal seulement - sera supprimé!
# ---------------------------------------------------------------------------

_WALL = "#"  # Murs
_FLOOR = " "  # Sol (reste vide)
_EMPTY = "·"  # En dehors de toute pièce
_PATH = "░"  # Corridor (couloir)


def render_ascii(plan: FloorPlan, show_labels: bool = True) -> str:
    W, H = plan.width, plan.height
    grid = [[_EMPTY] * W for _ in range(H)]

    # 1. Dessine les corridors/couloirs
    for c in plan.corridors:
        # Segment horizontal à y1, puis segment vertical à x2
        x_range = range(min(c.x1, c.x2), max(c.x1, c.x2) + 1)
        y_range = range(min(c.y1, c.y2), max(c.y1, c.y2) + 1)
        for x in x_range:
            if 0 <= c.y1 < H and 0 <= x < W and grid[c.y1][x] == _EMPTY:
                grid[c.y1][x] = _PATH
        for y in y_range:
            if 0 <= y < H and 0 <= c.x2 < W and grid[y][c.x2] == _EMPTY:
                grid[y][c.x2] = _PATH

    # 2. Déssine les pièces
    for room in plan.rooms:
        r = room.rect
        for dy in range(r.h):
            for dx in range(r.w):
                gy, gx = r.y + dy, r.x + dx
                if not (0 <= gy < H and 0 <= gx < W):
                    continue
                is_wall = dy == 0 or dy == r.h - 1 or dx == 0 or dx == r.w - 1
                grid[gy][gx] = _WALL if is_wall else _FLOOR

    # 3. Ecris le nom de chaque pièce
    if show_labels:
        for room in plan.rooms:
            r = room.rect
            inner_w = r.w - 2
            inner_h = r.h - 2
            if inner_w < 1 or inner_h < 1:
                continue
            label = room.room_type[:inner_w]
            lx = r.x + 1 + (inner_w - len(label)) // 2
            ly = r.y + 1 + inner_h // 2
            for i, ch in enumerate(label):
                gx = lx + i
                if 0 <= ly < H and 0 <= gx < W:
                    grid[ly][gx] = ch

    return "\n".join("".join(row) for row in grid)


# ---------------------------------------------------------------------------
# Point d'entrée CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    config = GeneratorConfig(max_depth=depth)
    plan = generate(config)

    print(render_ascii(plan))
    print()
    print(f"Pièces : {len(plan.rooms)}  |  Couloirs : {len(plan.corridors)}")
    print("Types  :", ", ".join(r.room_type for r in plan.rooms))
