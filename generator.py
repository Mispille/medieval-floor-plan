"""
Generateur de plan de maison medievale en Binary Space Partitioning (BSP)

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
    room_type: str  # Nom de la piece
    id: int


@dataclass
class Corridor:
    """Couloir entre deux pieces"""

    x1: int  # Debut du couloir
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
    min_room_size: int = 8  # Taille minimale d'une piece
    max_depth: int = 5  # Profondeur recursion du BSP recursion -> Gere nb pieces
    room_margin: int = 1  # Gap entre murs et rectangles
    seed: Optional[int] = None


# ---------------------------------------------------------------------------
# Algos internes au BSP (en cours d'apprentissage, va evoluer pour optimisation)
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
    """Separation recursive de chaque node jusqu'a max_depth ou taille mini atteinte"""
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
    """Assigne une piece a chaque node feuille"""
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
    """Retourne toute piece atteignable depuis un node"""
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
        corridors.append(
            Corridor(lc[0], lc[1], rc[0], rc[1], left_room.id, right_room.id)
        )


# ---------------------------------------------------------------------------
# API accessible publiquement
# ---------------------------------------------------------------------------


def generate(config: Optional[GeneratorConfig] = None) -> FloorPlan:
    """Retourne un "FloorPlan" d'une maison medievale aleatoire"""
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
