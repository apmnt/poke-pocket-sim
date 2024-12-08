# Dynamically created attack methods and their source code:
from enum import Enum
from functools import wraps
from condition import Condition

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class AttackName(Enum):
    SING = "sing"
    RECKLESS_CHARGE = "reckless-charge"
    PSY_REPORT = "psy-report"
    GROWL = "growl"
    DO_THE_WAVE = "do-the-wave"
    PRIMAL_WINGBEAT = "primal-wingbeat"
    SHARPEN = "sharpen"
    COPY_ANYTHING = "copy-anything"
    DIZZY_PUNCH = "dizzy-punch"
    CONTINUOUS_LICK = "continuous-lick"
    DRILL_PECK = "drill-peck"
    SHADOW_CLAW = "shadow-claw"
    LEEK_SLAP = "leek-slap"
    PAY_DAY = "pay-day"
    SLEEPY_SONG = "sleepy-song"
    HYPER_VOICE = "hyper-voice"
    DRILL_RUN = "drill-run"
    DRACO_METEOR = "draco-meteor"
    TAIL_SMACK = "tail-smack"
    HEAVY_IMPACT = "heavy-impact"
    AMASS = "amass"
    METAL_CLAW = "metal-claw"
    PIERCE = "pierce"
    CRUNCH = "crunch"
    VENOSHOCK = "venoshock"
    POISON_GAS = "poison-gas"
    GLIDE = "glide"
    POISON_HORN = "poison-horn"
    HORN_ATTACK = "horn-attack"
    LOVESTRIKE = "lovestrike"
    CALL_FOR_FAMILY = "call-for-family"
    CORNER = "corner"
    KNOCK_BACK = "knock-back"
    POUND = "pound"
    SPIRAL_KICK = "spiral-kick"
    LEECH_LIFE = "leech-life"
    SHELL_ATTACK = "shell-attack"
    HORN_DRILL = "horn-drill"
    JAB = "jab"
    STRETCH_KICK = "stretch-kick"
    BONEMERANG = "bonemerang"
    BONE_BEATDOWN = "bone-beatdown"
    LAND_CRUSH = "land-crush"
    DOUBLE_EDGE = "double-edge"
    ROLLOUT = "rollout"
    SEISMIC_TOSS = "seismic-toss"
    STRENGTH = "strength"
    FIGHT_BACK = "fight-back"
    LOW_KICK = "low-kick"
    DIG = "dig"
    MUD_SLAP = "mud-slap"
    DOUBLE_LARIAT = "double-lariat"
    HEART_STAMP = "heart-stamp"
    PSYSHOT = "psyshot"
    PSYDRIVE = "psydrive"
    PSYCHIC_SPHERE = "psychic-sphere"
    POWER_BLAST = "power-blast"
    BARRIER_ATTACK = "barrier-attack"
    PSYPUNCH = "psypunch"
    MUMBLE = "mumble"
    SPOOKY_SHOT = "spooky-shot"
    BOTHER = "bother"
    WILL_O_WISP = "will-o-wisp"
    SUFFOCATING_GAS = "suffocating-gas"
    PSYCHIC = "psychic"
    SUPER_PSY_BOLT = "super-psy-bolt"
    TELEPORT = "teleport"
    MAGICAL_SHOT = "magical-shot"
    SLAP = "slap"
    THUNDER_SHOCK = "thunder-shock"
    QUICK_ATTACK = "quick-attack"
    TAIL_WHAP = "tail-whap"
    THUNDER_FANG = "thunder-fang"
    HEAD_BOLT = "head-bolt"
    TINY_CHARGE = "tiny-charge"
    THUNDER_SPEAR = "thunder-spear"
    ZAP_KICK = "zap-kick"
    RAGING_THUNDER = "raging-thunder"
    PECK = "peck"
    THUNDERING_HURRICANE = "thundering-hurricane"
    PIN_MISSILE = "pin-missile"
    THUNDER_PUNCH = "thunder-punch"
    ELECTRO_BALL = "electro-ball"
    SPINNING_ATTACK = "spinning-attack"
    LIGHTNING_BALL = "lightning-ball"
    CIRCLE_CIRCUIT = "circle-circuit"
    THUNDERBOLT = "thunderbolt"
    POWDER_SNOW = "powder-snow"
    SECOND_STRIKE = "second-strike"
    RAIN_SPLASH = "rain-splash"
    MIST_SLASH = "mist-slash"
    WATER_DRIP = "water-drip"
    WING_ATTACK = "wing-attack"
    FLAP = "flap"
    BLIZZARD = "blizzard"
    ICE_WING = "ice-wing"
    ICE_BEAM = "ice-beam"
    ANCIENT_WHIRLPOOL = "ancient-whirlpool"
    BUBBLE_DRAIN = "bubble-drain"
    HYPER_BEAM = "hyper-beam"
    SPLASH = "splash"
    HYDRO_SPLASH = "hydro-splash"
    SMACK = "smack"
    HORN_HAZARD = "horn-hazard"
    FLOP = "flop"
    WATER_ARROW = "water-arrow"
    KO_CRAB = "ko-crab"
    VISE_GRIP = "vise-grip"
    TONGUE_SLAP = "tongue-slap"
    HEADBUTT = "headbutt"
    POISON_TENTACLES = "poison-tentacles"
    GENTLE_SLAP = "gentle-slap"
    MEGA_PUNCH = "mega-punch"
    KNUCKLE_PUNCH = "knuckle-punch"
    RAZOR_FIN = "razor-fin"
    AQUA_EDGE = "aqua-edge"
    HEADACHE = "headache"
    SURF = "surf"
    HYDRO_BAZOOKA = "hydro-bazooka"
    HYDRO_PUMP = "hydro-pump"
    WAVE_SPLASH = "wave-splash"
    WATER_GUN = "water-gun"
    FIRE_BLAST = "fire-blast"
    GNAW = "gnaw"
    COMBUSTION = "combustion"
    HEAT_BLAST = "heat-blast"
    INFERNO_DANCE = "inferno-dance"
    SKY_ATTACK = "sky-attack"
    MAGMA_PUNCH = "magma-punch"
    FIRE_MANE = "fire-mane"
    FLARE = "flare"
    INFERNO_ONRUSH = "inferno-onrush"
    HEAT_TACKLE = "heat-tackle"
    BITE = "bite"
    FLAMETHROWER = "flamethrower"
    TAIL_WHIP = "tail-whip"
    FIRE_SPIN = "fire-spin"
    CRIMSON_STORM = "crimson-storm"
    FIRE_CLAWS = "fire-claws"
    EMBER = "ember"
    SURPRISE_ATTACK = "surprise-attack"
    LEAF_SUPPLY = "leaf-supply"
    ROLLING_TACKLE = "rolling-tackle"
    BLOT = "blot"
    ATTACH = "attach"
    DOUBLE_HORN = "double-horn"
    SHARP_SCYTHE = "sharp-scythe"
    ABSORB = "absorb"
    TROPICAL_SWING = "tropical-swing"
    STOMP = "stomp"
    SEED_BOMB = "seed-bomb"
    POISON_POWDER = "poison-powder"
    TACKLE = "tackle"
    SLASH = "slash"
    SCRATCH = "scratch"
    SOOTHING_SCENT = "soothing-scent"
    DROOL = "drool"
    RAM = "ram"
    SHARP_STING = "sharp-sting"
    STING = "sting"
    GUST = "gust"
    BUG_BITE = "bug-bite"
    FIND_A_FRIEND = "find-a-friend"
    GIANT_BLOOM = "giant-bloom"
    MEGA_DRAIN = "mega-drain"
    RAZOR_LEAF = "razor-leaf"
    VINE_WHIP = "vine-whip"


class EnergyType(Enum):
    WATER = "water"
    FIRE = "fire"
    GRASS = "grass"
    ELECTRIC = "electric"
    PSYCHIC = "psychic"
    FIGHTING = "fighting"
    DARKNESS = "darkness"
    METAL = "metal"
    ANY = "any"


ATTACKS = {
    "absorb": {
        "damage": 40,
        "energy": {"colorless": 1, "grass": 1},
        "has_side_effect": True,
    },
    "amass": {"damage": 0, "energy": {"metal": 1}, "has_side_effect": True},
    "ancient-whirlpool": {
        "damage": 70,
        "energy": {"colorless": 2, "water": 1},
        "has_side_effect": True,
    },
    "aqua-edge": {"damage": 70, "energy": {"water": 2}, "has_side_effect": False},
    "attach": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "barrier-attack": {
        "damage": 30,
        "energy": {"colorless": 1, "psychic": 1},
        "has_side_effect": True,
    },
    "bite": {"damage": 20, "energy": {"colorless": 2}, "has_side_effect": False},
    "blizzard": {"damage": 80, "energy": {"water": 3}, "has_side_effect": True},
    "blot": {"damage": 10, "energy": {"grass": 1}, "has_side_effect": True},
    "bone-beatdown": {
        "damage": 40,
        "energy": {"fighting": 1},
        "has_side_effect": False,
    },
    "bonemerang": {"damage": 80, "energy": {"fighting": 2}, "has_side_effect": True},
    "bother": {"damage": 50, "energy": {"psychic": 1}, "has_side_effect": True},
    "bubble-drain": {
        "damage": 60,
        "energy": {"colorless": 2, "water": 1},
        "has_side_effect": True,
    },
    "bug-bite": {"damage": 30, "energy": {"colorless": 2}, "has_side_effect": False},
    "call-for-family": {
        "damage": 0,
        "energy": {"darkness": 1},
        "has_side_effect": True,
    },
    "circle-circuit": {
        "damage": 30,
        "energy": {"lightning": 2},
        "has_side_effect": True,
    },
    "combustion": {"damage": 30, "energy": {"fire": 1}, "has_side_effect": False},
    "continuous-lick": {
        "damage": 60,
        "energy": {"colorless": 3},
        "has_side_effect": True,
    },
    "copy-anything": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "corner": {
        "damage": 60,
        "energy": {"colorless": 1, "darkness": 1},
        "has_side_effect": True,
    },
    "crimson-storm": {
        "damage": 200,
        "energy": {"colorless": 2, "fire": 2},
        "has_side_effect": True,
    },
    "crunch": {"damage": 20, "energy": {"metal": 1}, "has_side_effect": True},
    "dig": {"damage": 40, "energy": {"fighting": 1}, "has_side_effect": True},
    "dizzy-punch": {"damage": 30, "energy": {"colorless": 1}, "has_side_effect": True},
    "do-the-wave": {"damage": 30, "energy": {"colorless": 3}, "has_side_effect": True},
    "double-edge": {
        "damage": 150,
        "energy": {"colorless": 3, "fighting": 1},
        "has_side_effect": True,
    },
    "double-horn": {"damage": 50, "energy": {"grass": 2}, "has_side_effect": True},
    "double-lariat": {
        "damage": 100,
        "energy": {"colorless": 2, "psychic": 2},
        "has_side_effect": True,
    },
    "draco-meteor": {
        "damage": 0,
        "energy": {"colorless": 2, "lightning": 1, "water": 1},
        "has_side_effect": True,
    },
    "drill-peck": {"damage": 40, "energy": {"colorless": 1}, "has_side_effect": False},
    "drill-run": {"damage": 50, "energy": {"colorless": 2}, "has_side_effect": True},
    "drool": {
        "damage": 40,
        "energy": {"colorless": 1, "grass": 1},
        "has_side_effect": False,
    },
    "electro-ball": {
        "damage": 70,
        "energy": {"lightning": 2},
        "has_side_effect": False,
    },
    "ember": {"damage": 30, "energy": {"fire": 1}, "has_side_effect": True},
    "fight-back": {"damage": 40, "energy": {"fighting": 2}, "has_side_effect": True},
    "find-a-friend": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "fire-blast": {
        "damage": 130,
        "energy": {"colorless": 3, "fire": 1},
        "has_side_effect": True,
    },
    "fire-claws": {
        "damage": 60,
        "energy": {"colorless": 1, "fire": 1},
        "has_side_effect": False,
    },
    "fire-mane": {"damage": 40, "energy": {"fire": 1}, "has_side_effect": False},
    "fire-spin": {
        "damage": 150,
        "energy": {"colorless": 2, "fire": 2},
        "has_side_effect": True,
    },
    "flamethrower": {"damage": 90, "energy": {"fire": 2}, "has_side_effect": True},
    "flap": {"damage": 30, "energy": {"colorless": 2}, "has_side_effect": False},
    "flare": {"damage": 20, "energy": {"fire": 1}, "has_side_effect": False},
    "flop": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "gentle-slap": {"damage": 20, "energy": {"water": 1}, "has_side_effect": False},
    "giant-bloom": {
        "damage": 100,
        "energy": {"colorless": 2, "grass": 2},
        "has_side_effect": True,
    },
    "glide": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "gnaw": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "growl": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "gust": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "head-bolt": {"damage": 40, "energy": {"lightning": 1}, "has_side_effect": False},
    "headache": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": True},
    "headbutt": {"damage": 30, "energy": {"colorless": 2}, "has_side_effect": False},
    "heart-stamp": {
        "damage": 60,
        "energy": {"colorless": 1, "psychic": 1},
        "has_side_effect": False,
    },
    "heat-blast": {
        "damage": 70,
        "energy": {"colorless": 2, "fire": 1},
        "has_side_effect": False,
    },
    "heat-tackle": {
        "damage": 100,
        "energy": {"colorless": 1, "fire": 2},
        "has_side_effect": True,
    },
    "heavy-impact": {
        "damage": 120,
        "energy": {"colorless": 1, "metal": 3},
        "has_side_effect": False,
    },
    "horn-attack": {
        "damage": 40,
        "energy": {"colorless": 1, "darkness": 1},
        "has_side_effect": False,
    },
    "horn-drill": {
        "damage": 100,
        "energy": {"colorless": 1, "fighting": 3},
        "has_side_effect": False,
    },
    "horn-hazard": {"damage": 80, "energy": {"water": 1}, "has_side_effect": True},
    "hydro-bazooka": {
        "damage": 100,
        "energy": {"colorless": 1, "water": 2},
        "has_side_effect": True,
    },
    "hydro-pump": {
        "damage": 80,
        "energy": {"colorless": 1, "water": 2},
        "has_side_effect": True,
    },
    "hydro-splash": {"damage": 90, "energy": {"water": 2}, "has_side_effect": False},
    "hyper-beam": {"damage": 100, "energy": {"water": 4}, "has_side_effect": True},
    "hyper-voice": {"damage": 60, "energy": {"colorless": 2}, "has_side_effect": False},
    "ice-beam": {
        "damage": 60,
        "energy": {"colorless": 1, "water": 2},
        "has_side_effect": True,
    },
    "ice-wing": {
        "damage": 40,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": False,
    },
    "inferno-dance": {"damage": 0, "energy": {"fire": 1}, "has_side_effect": True},
    "inferno-onrush": {
        "damage": 120,
        "energy": {"colorless": 1, "fire": 2},
        "has_side_effect": True,
    },
    "jab": {"damage": 30, "energy": {"fighting": 1}, "has_side_effect": False},
    "knock-back": {
        "damage": 70,
        "energy": {"colorless": 1, "fighting": 2},
        "has_side_effect": True,
    },
    "knuckle-punch": {
        "damage": 20,
        "energy": {"fighting": 1},
        "has_side_effect": False,
    },
    "ko-crab": {
        "damage": 80,
        "energy": {"colorless": 1, "water": 2},
        "has_side_effect": True,
    },
    "land-crush": {"damage": 70, "energy": {"fighting": 3}, "has_side_effect": False},
    "leaf-supply": {"damage": 50, "energy": {"grass": 2}, "has_side_effect": True},
    "leech-life": {"damage": 50, "energy": {"fighting": 1}, "has_side_effect": True},
    "leek-slap": {"damage": 40, "energy": {"colorless": 1}, "has_side_effect": False},
    "lightning-ball": {
        "damage": 20,
        "energy": {"lightning": 1},
        "has_side_effect": False,
    },
    "lovestrike": {
        "damage": 80,
        "energy": {"colorless": 1, "darkness": 2},
        "has_side_effect": True,
    },
    "low-kick": {"damage": 20, "energy": {"fighting": 1}, "has_side_effect": False},
    "magical-shot": {"damage": 40, "energy": {"psychic": 1}, "has_side_effect": False},
    "magma-punch": {"damage": 50, "energy": {"fire": 2}, "has_side_effect": False},
    "mega-drain": {
        "damage": 80,
        "energy": {"colorless": 2, "grass": 2},
        "has_side_effect": True,
    },
    "mega-punch": {
        "damage": 50,
        "energy": {"colorless": 2, "psychic": 1},
        "has_side_effect": False,
    },
    "metal-claw": {"damage": 70, "energy": {"metal": 2}, "has_side_effect": False},
    "mist-slash": {
        "damage": 60,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": False,
    },
    "mud-slap": {"damage": 20, "energy": {"fighting": 1}, "has_side_effect": False},
    "mumble": {
        "damage": 30,
        "energy": {"colorless": 1, "psychic": 1},
        "has_side_effect": False,
    },
    "pay-day": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": True},
    "peck": {"damage": 20, "energy": {"darkness": 1}, "has_side_effect": False},
    "pierce": {"damage": 30, "energy": {"metal": 1}, "has_side_effect": False},
    "pin-missile": {
        "damage": 40,
        "energy": {"colorless": 1, "lightning": 1},
        "has_side_effect": True,
    },
    "poison-gas": {"damage": 10, "energy": {"darkness": 1}, "has_side_effect": True},
    "poison-horn": {
        "damage": 90,
        "energy": {"colorless": 1, "darkness": 2},
        "has_side_effect": True,
    },
    "poison-powder": {"damage": 30, "energy": {"grass": 1}, "has_side_effect": True},
    "poison-tentacles": {
        "damage": 50,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": True,
    },
    "pound": {"damage": 20, "energy": {"colorless": 1}, "has_side_effect": False},
    "powder-snow": {
        "damage": 40,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": True,
    },
    "power-blast": {
        "damage": 120,
        "energy": {"colorless": 2, "psychic": 2},
        "has_side_effect": True,
    },
    "primal-wingbeat": {
        "damage": 0,
        "energy": {"colorless": 2},
        "has_side_effect": True,
    },
    "psy-report": {"damage": 20, "energy": {"psychic": 1}, "has_side_effect": True},
    "psychic": {
        "damage": 30,
        "energy": {"colorless": 1, "psychic": 1},
        "has_side_effect": True,
    },
    "psychic-sphere": {
        "damage": 50,
        "energy": {"colorless": 1, "psychic": 1},
        "has_side_effect": False,
    },
    "psydrive": {
        "damage": 150,
        "energy": {"colorless": 2, "psychic": 2},
        "has_side_effect": True,
    },
    "psypunch": {
        "damage": 50,
        "energy": {"colorless": 1, "psychic": 2},
        "has_side_effect": False,
    },
    "psyshot": {
        "damage": 60,
        "energy": {"colorless": 1, "psychic": 2},
        "has_side_effect": False,
    },
    "quick-attack": {"damage": 40, "energy": {"colorless": 2}, "has_side_effect": True},
    "raging-thunder": {
        "damage": 100,
        "energy": {"colorless": 1, "lightning": 2},
        "has_side_effect": True,
    },
    "rain-splash": {"damage": 30, "energy": {"water": 1}, "has_side_effect": False},
    "ram": {"damage": 20, "energy": {"grass": 1}, "has_side_effect": False},
    "razor-fin": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "razor-leaf": {
        "damage": 70,
        "energy": {"colorless": 2, "grass": 1},
        "has_side_effect": False,
    },
    "reckless-charge": {
        "damage": 30,
        "energy": {"fighting": 1},
        "has_side_effect": True,
    },
    "rolling-tackle": {
        "damage": 80,
        "energy": {"colorless": 3},
        "has_side_effect": False,
    },
    "rollout": {
        "damage": 70,
        "energy": {"colorless": 2, "fighting": 1},
        "has_side_effect": False,
    },
    "scratch": {
        "damage": 30,
        "energy": {"colorless": 1, "grass": 1},
        "has_side_effect": False,
    },
    "second-strike": {
        "damage": 10,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": True,
    },
    "seed-bomb": {"damage": 20, "energy": {"grass": 1}, "has_side_effect": False},
    "seismic-toss": {
        "damage": 100,
        "energy": {"fighting": 3},
        "has_side_effect": False,
    },
    "shadow-claw": {"damage": 40, "energy": {"colorless": 2}, "has_side_effect": True},
    "sharp-scythe": {"damage": 30, "energy": {"grass": 1}, "has_side_effect": False},
    "sharp-sting": {"damage": 70, "energy": {"grass": 1}, "has_side_effect": False},
    "sharpen": {"damage": 20, "energy": {"colorless": 1}, "has_side_effect": False},
    "shell-attack": {"damage": 40, "energy": {"fighting": 1}, "has_side_effect": False},
    "sing": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "sky-attack": {
        "damage": 130,
        "energy": {"colorless": 2, "fire": 1},
        "has_side_effect": True,
    },
    "slap": {"damage": 20, "energy": {"psychic": 1}, "has_side_effect": False},
    "slash": {
        "damage": 80,
        "energy": {"colorless": 1, "grass": 2},
        "has_side_effect": False,
    },
    "sleepy-song": {"damage": 80, "energy": {"colorless": 3}, "has_side_effect": True},
    "smack": {"damage": 20, "energy": {"water": 1}, "has_side_effect": False},
    "soothing-scent": {
        "damage": 80,
        "energy": {"colorless": 1, "grass": 2},
        "has_side_effect": True,
    },
    "spinning-attack": {
        "damage": 60,
        "energy": {"colorless": 3, "lightning": 1},
        "has_side_effect": False,
    },
    "spiral-kick": {"damage": 40, "energy": {"colorless": 1}, "has_side_effect": False},
    "splash": {"damage": 10, "energy": {"colorless": 1}, "has_side_effect": False},
    "spooky-shot": {"damage": 100, "energy": {"psychic": 3}, "has_side_effect": False},
    "sting": {"damage": 20, "energy": {"grass": 1}, "has_side_effect": False},
    "stomp": {"damage": 30, "energy": {"grass": 1}, "has_side_effect": True},
    "strength": {"damage": 50, "energy": {"fighting": 2}, "has_side_effect": False},
    "stretch-kick": {"damage": 0, "energy": {"fighting": 1}, "has_side_effect": True},
    "suffocating-gas": {
        "damage": 20,
        "energy": {"psychic": 1},
        "has_side_effect": False,
    },
    "super-psy-bolt": {
        "damage": 60,
        "energy": {"colorless": 2, "psychic": 1},
        "has_side_effect": False,
    },
    "surf": {"damage": 90, "energy": {"water": 3}, "has_side_effect": False},
    "surprise-attack": {
        "damage": 40,
        "energy": {"colorless": 1},
        "has_side_effect": True,
    },
    "tackle": {"damage": 20, "energy": {"grass": 1}, "has_side_effect": False},
    "tail-smack": {"damage": 20, "energy": {"colorless": 1}, "has_side_effect": False},
    "tail-whap": {"damage": 20, "energy": {"lightning": 1}, "has_side_effect": False},
    "tail-whip": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "teleport": {"damage": 0, "energy": {"colorless": 1}, "has_side_effect": True},
    "thunder-fang": {
        "damage": 80,
        "energy": {"colorless": 1, "lightning": 2},
        "has_side_effect": True,
    },
    "thunder-punch": {
        "damage": 40,
        "energy": {"lightning": 2},
        "has_side_effect": True,
    },
    "thunder-shock": {
        "damage": 30,
        "energy": {"lightning": 2},
        "has_side_effect": True,
    },
    "thunder-spear": {"damage": 0, "energy": {"lightning": 1}, "has_side_effect": True},
    "thunderbolt": {"damage": 140, "energy": {"lightning": 3}, "has_side_effect": True},
    "thundering-hurricane": {
        "damage": 50,
        "energy": {"lightning": 3},
        "has_side_effect": True,
    },
    "tiny-charge": {"damage": 30, "energy": {"lightning": 1}, "has_side_effect": False},
    "tongue-slap": {"damage": 20, "energy": {"water": 1}, "has_side_effect": False},
    "tropical-swing": {"damage": 40, "energy": {"grass": 1}, "has_side_effect": True},
    "venoshock": {
        "damage": 70,
        "energy": {"colorless": 1, "darkness": 2},
        "has_side_effect": True,
    },
    "vine-whip": {"damage": 20, "energy": {"grass": 1}, "has_side_effect": False},
    "vise-grip": {
        "damage": 40,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": False,
    },
    "water-arrow": {"damage": 0, "energy": {"water": 3}, "has_side_effect": True},
    "water-drip": {"damage": 30, "energy": {"colorless": 1}, "has_side_effect": False},
    "water-gun": {"damage": 40, "energy": {"water": 1}, "has_side_effect": False},
    "wave-splash": {
        "damage": 40,
        "energy": {"colorless": 1, "water": 1},
        "has_side_effect": False,
    },
    "will-o-wisp": {"damage": 30, "energy": {"psychic": 1}, "has_side_effect": False},
    "wing-attack": {"damage": 70, "energy": {"colorless": 3}, "has_side_effect": False},
    "zap-kick": {"damage": 20, "energy": {"lightning": 1}, "has_side_effect": False},
}


def apply_damage(func):
    @wraps(func)
    def wrapper(player: "Player", *args, **kwargs):
        func(player, *args, **kwargs)
        attack_name = AttackName[func.__name__.upper()].value
        damage = ATTACKS[attack_name]["damage"]
        if (
            damage != 0
            and player.opponent.active_card.weakness == player.active_card.type
        ):
            damage += 20
        if player.active_card.conditions is not []:
            for condition in player.active_card.conditions:
                if type(condition) is Condition.Plus10DamageDealed and damage != 0:
                    damage += 10

        if player.print_actions:
            print(f"Dealing {damage} to {player.opponent.active_card.name}")
        player.opponent.active_card.hp -= damage

    return wrapper


class Attack:

    @staticmethod
    def can_use_attack(card, attack_func):
        attack_name = attack_func.__name__.replace("_", "-")
        if attack_name not in ATTACKS:
            raise ValueError(f"Attack {attack_name} does not exist")

        energies = card.energies.copy()
        attack_cost = ATTACKS[attack_name]["energy"]

        # Check specific energy requirements
        for energy_type, cost in attack_cost.items():
            if energy_type == "colorless":
                continue  # Skip colorless
            if energies.get(energy_type, 0) < cost:
                return False  # Not enough specific energy
            energies[energy_type] -= cost  # Deduct the used energy

        # Check colorless energy requirement
        colorless_cost = attack_cost.get("colorless", 0)
        total_remaining_energy = sum(energies.values())
        return total_remaining_energy >= colorless_cost

    @staticmethod
    def attack_repr(name, damage, energy_cost):
        return f"Attack(Name: {name}, Damage: {damage}, Energy Cost: {energy_cost})"

    @apply_damage
    def psychic_sphere(player):
        pass

    @apply_damage
    def psydrive(player):
        if player.active_card.energies["psychic"] < 2:
            raise Exception(
                f'Not enough energy, only {player.active_card.energies["psychic"]} psychic energy'
            )
        player.active_card.remove_energy(EnergyType.PSYCHIC)
        player.active_card.remove_energy(EnergyType.PSYCHIC)

    @apply_damage
    def circle_circuit(player):
        pass

    @apply_damage
    def slash(player):
        pass

    @apply_damage
    def crimson_storm(player):
        pass

    @apply_damage
    def psy_report(player):
        pass

    @apply_damage
    def ice_wing(player):
        pass

    @apply_damage
    def blizzard(player):
        # TODO ATTACK
        pass

    @apply_damage
    def sleepy_song(player):
        pass

    @apply_damage
    def mega_punch(player):
        pass

    @apply_damage
    def bonemerang(player):
        # TODO ATTACK
        pass

    @apply_damage
    def spooky_shot(player):
        pass

    @apply_damage
    def peck(player):
        pass

    @apply_damage
    def thundering_hurricane(player):
        pass

    @apply_damage
    def inferno_dance(player):
        pass

    @apply_damage
    def heat_blast(player):
        pass

    @apply_damage
    def surf(player):
        pass

    @apply_damage
    def hydro_bazooka(player):
        pass

    @apply_damage
    def hydro_splash(player):
        pass

    @apply_damage
    def inferno_onrush(player):
        pass

    @apply_damage
    def tropical_swing(player):
        pass

    @apply_damage
    def razor_leaf(player):
        pass

    @apply_damage
    def giant_bloom(player):
        pass

    @apply_damage
    def tail_whap(player):
        pass

    @apply_damage
    def power_blast(player):
        pass

    @apply_damage
    def gnaw(player):
        pass

    @apply_damage
    def mega_drain(player):
        pass

    @apply_damage
    def copy_anything(player):
        pass

    @apply_damage
    def tackle(player):
        pass

    @apply_damage
    def rollout(player):
        pass

    @apply_damage
    def pay_day(player):
        pass

    @apply_damage
    def sharpen(player):
        pass

    @apply_damage
    def draco_meteor(player):
        pass

    @apply_damage
    def wing_attack(player):
        pass

    @apply_damage
    def lovestrike(player):
        # TODO ATTACK
        pass

    @apply_damage
    def poison_horn(player):
        pass

    @apply_damage
    def growl(player):
        # TODO ATTACK
        pass

    @apply_damage
    def mud_slap(player):
        pass

    @apply_damage
    def psychic(player):
        # TODO ATTACK
        pass

    @apply_damage
    def electro_ball(player):
        pass

    @apply_damage
    def hydro_pump(player):
        pass

    @apply_damage
    def fire_mane(player):
        pass

    @apply_damage
    def hyper_beam(player):
        pass

    @apply_damage
    def water_gun(player):
        pass

    @apply_damage
    def ember(player):
        # TODO ATTACK
        pass

    @apply_damage
    def double_horn(player):
        pass

    @apply_damage
    def drool(player):
        pass

    @apply_damage
    def vine_whip(player):
        pass

    @apply_damage
    def bubble_drain(player):
        pass

    @apply_damage
    def gentle_slap(player):
        pass

    @apply_damage
    def lightning_ball(player):
        pass

    @apply_damage
    def mist_slash(player):
        pass

    @apply_damage
    def gust(player):
        pass

    @apply_damage
    def primal_wingbeat(player):
        pass

    @apply_damage
    def dizzy_punch(player):
        pass

    @apply_damage
    def heavy_impact(player):
        pass

    @apply_damage
    def venoshock(player):
        # TODO ATTACK
        pass

    @apply_damage
    def leech_life(player):
        pass

    @apply_damage
    def double_edge(player):
        pass

    @apply_damage
    def seismic_toss(player):
        pass

    @apply_damage
    def psyshot(player):
        pass

    @apply_damage
    def psypunch(player):
        pass

    @apply_damage
    def bother(player):
        # TODO ATTACK
        pass

    @apply_damage
    def thunder_fang(player):
        pass

    @apply_damage
    def raging_thunder(player):
        pass

    @apply_damage
    def pin_missile(player):
        pass

    @apply_damage
    def spinning_attack(player):
        pass

    @apply_damage
    def thunderbolt(player):
        # TODO ATTACK
        pass

    @apply_damage
    def fire_spin(player):
        pass

    @apply_damage
    def ice_beam(player):
        pass

    @apply_damage
    def ancient_whirlpool(player):
        pass

    @apply_damage
    def sky_attack(player):
        pass

    @apply_damage
    def flamethrower(player):
        # TODO ATTACK
        pass

    @apply_damage
    def heat_tackle(player):
        pass

    @apply_damage
    def stomp(player):
        # TODO ATTACK
        pass

    @apply_damage
    def soothing_scent(player):
        pass

    @apply_damage
    def sharp_sting(player):
        pass

    @apply_damage
    def second_strike(player):
        pass

    @apply_damage
    def do_the_wave(player):
        pass

    @apply_damage
    def horn_attack(player):
        pass

    @apply_damage
    def continuous_lick(player):
        pass

    @apply_damage
    def drill_peck(player):
        pass

    @apply_damage
    def shadow_claw(player):
        pass

    @apply_damage
    def tail_smack(player):
        pass

    @apply_damage
    def metal_claw(player):
        pass

    @apply_damage
    def bite(player):
        pass

    @apply_damage
    def corner(player):
        # TODO ATTACK
        pass

    @apply_damage
    def knock_back(player):
        pass

    @apply_damage
    def spiral_kick(player):
        pass

    @apply_damage
    def shell_attack(player):
        pass

    @apply_damage
    def horn_drill(player):
        pass

    @apply_damage
    def bone_beatdown(player):
        pass

    @apply_damage
    def land_crush(player):
        pass

    @apply_damage
    def strength(player):
        pass

    @apply_damage
    def fight_back(player):
        pass

    @apply_damage
    def dig(player):
        # TODO ATTACK
        pass

    @apply_damage
    def double_lariat(player):
        pass

    @apply_damage
    def smack(player):
        pass

    @apply_damage
    def barrier_attack(player):
        pass

    @apply_damage
    def will_o_wisp(player):
        pass

    @apply_damage
    def super_psy_bolt(player):
        pass

    @apply_damage
    def magical_shot(player):
        pass

    @apply_damage
    def thunder_shock(player):
        pass

    @apply_damage
    def head_bolt(player):
        pass

    @apply_damage
    def thunder_spear(player):
        pass

    @apply_damage
    def powder_snow(player):
        pass

    @apply_damage
    def water_drip(player):
        pass

    @apply_damage
    def leaf_supply(player):
        pass

    @apply_damage
    def wave_splash(player):
        pass

    @apply_damage
    def water_arrow(player):
        pass

    @apply_damage
    def ko_crab(player):
        pass

    @apply_damage
    def poison_tentacles(player):
        pass

    @apply_damage
    def knuckle_punch(player):
        pass

    @apply_damage
    def aqua_edge(player):
        pass

    @apply_damage
    def fire_blast(player):
        pass

    @apply_damage
    def fire_claws(player):
        pass

    @apply_damage
    def rolling_tackle(player):
        pass

    @apply_damage
    def poison_powder(player):
        pass

    @apply_damage
    def sing(player):
        # TODO ATTACK
        pass

    @apply_damage
    def surprise_attack(player):
        pass

    @apply_damage
    def reckless_charge(player):
        pass

    @apply_damage
    def slap(player):
        pass

    @apply_damage
    def scratch(player):
        pass

    @apply_damage
    def leek_slap(player):
        pass

    @apply_damage
    def pound(player):
        pass

    @apply_damage
    def hyper_voice(player):
        pass

    @apply_damage
    def drill_run(player):
        pass

    @apply_damage
    def ram(player):
        pass

    @apply_damage
    def amass(player):
        # TODO ATTACK
        pass

    @apply_damage
    def pierce(player):
        pass

    @apply_damage
    def crunch(player):
        # TODO ATTACK
        pass

    @apply_damage
    def suffocating_gas(player):
        pass

    @apply_damage
    def poison_gas(player):
        pass

    @apply_damage
    def glide(player):
        pass

    @apply_damage
    def call_for_family(player):
        pass

    @apply_damage
    def stretch_kick(player):
        pass

    @apply_damage
    def jab(player):
        pass

    @apply_damage
    def flop(player):
        pass

    @apply_damage
    def low_kick(player):
        pass

    @apply_damage
    def heart_stamp(player):
        pass

    @apply_damage
    def mumble(player):
        pass

    @apply_damage
    def teleport(player):
        # TODO ATTACK
        pass

    @apply_damage
    def quick_attack(player):
        pass

    @apply_damage
    def tiny_charge(player):
        pass

    @apply_damage
    def zap_kick(player):
        pass

    @apply_damage
    def thunder_punch(player):
        pass

    @apply_damage
    def rain_splash(player):
        pass

    @apply_damage
    def flap(player):
        pass

    @apply_damage
    def splash(player):
        pass

    @apply_damage
    def horn_hazard(player):
        pass

    @apply_damage
    def vise_grip(player):
        pass

    @apply_damage
    def tongue_slap(player):
        pass

    @apply_damage
    def headbutt(player):
        pass

    @apply_damage
    def razor_fin(player):
        pass

    @apply_damage
    def headache(player):
        # TODO ATTACK
        pass

    @apply_damage
    def combustion(player):
        pass

    @apply_damage
    def magma_punch(player):
        pass

    @apply_damage
    def flare(player):
        pass

    @apply_damage
    def tail_whip(player):
        pass

    @apply_damage
    def blot(player):
        # TODO ATTACK
        pass

    @apply_damage
    def attach(player):
        pass

    @apply_damage
    def sharp_scythe(player):
        pass

    @apply_damage
    def absorb(player):
        # TODO ATTACK
        pass

    @apply_damage
    def seed_bomb(player):
        pass

    @apply_damage
    def sting(player):
        pass

    @apply_damage
    def bug_bite(player):
        pass

    @apply_damage
    def find_a_friend(player):
        pass
