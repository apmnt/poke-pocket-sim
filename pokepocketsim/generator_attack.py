from enum import Enum
from functools import wraps
import inspect
from pprint import pformat
from typing import Dict, Any, Callable, List, Optional, cast, Union


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


ATTACKS = {
    "psychic-sphere": {
        "energy": {
            "psychic": 1,
            "colorless": 1,
        },
        "damage": 50,
        "has_side_effect": False,
    },
    "psydrive": {
        "energy": {
            "psychic": 2,
            "colorless": 2,
        },
        "damage": 150,
        "has_side_effect": True,
    },
    "circle-circuit": {
        "energy": {
            "lightning": 2,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "slash": {
        "energy": {
            "grass": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": False,
    },
    "crimson-storm": {
        "energy": {
            "fire": 2,
            "colorless": 2,
        },
        "damage": 200,
        "has_side_effect": True,
    },
    "psy-report": {
        "energy": {
            "psychic": 1,
        },
        "damage": 20,
        "has_side_effect": True,
    },
    "ice-wing": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "blizzard": {
        "energy": {
            "water": 3,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "sleepy-song": {
        "energy": {
            "colorless": 3,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "mega-punch": {
        "energy": {
            "psychic": 1,
            "colorless": 2,
        },
        "damage": 50,
        "has_side_effect": False,
    },
    "bonemerang": {
        "energy": {
            "fighting": 2,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "spooky-shot": {
        "energy": {
            "psychic": 3,
        },
        "damage": 100,
        "has_side_effect": False,
    },
    "peck": {
        "energy": {
            "darkness": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "thundering-hurricane": {
        "energy": {
            "lightning": 3,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "inferno-dance": {
        "energy": {
            "fire": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "heat-blast": {
        "energy": {
            "fire": 1,
            "colorless": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "surf": {
        "energy": {
            "water": 3,
        },
        "damage": 90,
        "has_side_effect": False,
    },
    "hydro-bazooka": {
        "energy": {
            "water": 2,
            "colorless": 1,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "hydro-splash": {
        "energy": {
            "water": 2,
        },
        "damage": 90,
        "has_side_effect": False,
    },
    "inferno-onrush": {
        "energy": {
            "fire": 2,
            "colorless": 1,
        },
        "damage": 120,
        "has_side_effect": True,
    },
    "tropical-swing": {
        "energy": {
            "grass": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "razor-leaf": {
        "energy": {
            "grass": 1,
            "colorless": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "giant-bloom": {
        "energy": {
            "grass": 2,
            "colorless": 2,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "tail-whap": {
        "energy": {
            "lightning": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "power-blast": {
        "energy": {
            "psychic": 2,
            "colorless": 2,
        },
        "damage": 120,
        "has_side_effect": True,
    },
    "gnaw": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "mega-drain": {
        "energy": {
            "grass": 2,
            "colorless": 2,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "copy-anything": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "tackle": {
        "energy": {
            "grass": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "rollout": {
        "energy": {
            "fighting": 1,
            "colorless": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "pay-day": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": True,
    },
    "sharpen": {
        "energy": {
            "colorless": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "draco-meteor": {
        "energy": {
            "water": 1,
            "lightning": 1,
            "colorless": 2,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "wing-attack": {
        "energy": {
            "colorless": 3,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "lovestrike": {
        "energy": {
            "darkness": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "poison-horn": {
        "energy": {
            "darkness": 2,
            "colorless": 1,
        },
        "damage": 90,
        "has_side_effect": True,
    },
    "growl": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "mud-slap": {
        "energy": {
            "fighting": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "psychic": {
        "energy": {
            "psychic": 1,
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "electro-ball": {
        "energy": {
            "lightning": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "hydro-pump": {
        "energy": {
            "water": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "fire-mane": {
        "energy": {
            "fire": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "hyper-beam": {
        "energy": {
            "water": 4,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "water-gun": {
        "energy": {
            "water": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "ember": {
        "energy": {
            "fire": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "double-horn": {
        "energy": {
            "grass": 2,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "drool": {
        "energy": {
            "grass": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "vine-whip": {
        "energy": {
            "grass": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "bubble-drain": {
        "energy": {
            "water": 1,
            "colorless": 2,
        },
        "damage": 60,
        "has_side_effect": True,
    },
    "gentle-slap": {
        "energy": {
            "water": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "lightning-ball": {
        "energy": {
            "lightning": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "mist-slash": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "gust": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "primal-wingbeat": {
        "energy": {
            "colorless": 2,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "dizzy-punch": {
        "energy": {
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "heavy-impact": {
        "energy": {
            "metal": 3,
            "colorless": 1,
        },
        "damage": 120,
        "has_side_effect": False,
    },
    "venoshock": {
        "energy": {
            "darkness": 2,
            "colorless": 1,
        },
        "damage": 70,
        "has_side_effect": True,
    },
    "leech-life": {
        "energy": {
            "fighting": 1,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "double-edge": {
        "energy": {
            "fighting": 1,
            "colorless": 3,
        },
        "damage": 150,
        "has_side_effect": True,
    },
    "seismic-toss": {
        "energy": {
            "fighting": 3,
        },
        "damage": 100,
        "has_side_effect": False,
    },
    "psyshot": {
        "energy": {
            "psychic": 2,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "psypunch": {
        "energy": {
            "psychic": 2,
            "colorless": 1,
        },
        "damage": 50,
        "has_side_effect": False,
    },
    "bother": {
        "energy": {
            "psychic": 1,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "thunder-fang": {
        "energy": {
            "lightning": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "raging-thunder": {
        "energy": {
            "lightning": 2,
            "colorless": 1,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "pin-missile": {
        "energy": {
            "lightning": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "spinning-attack": {
        "energy": {
            "lightning": 1,
            "colorless": 3,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "thunderbolt": {
        "energy": {
            "lightning": 3,
        },
        "damage": 140,
        "has_side_effect": True,
    },
    "fire-spin": {
        "energy": {
            "fire": 2,
            "colorless": 2,
        },
        "damage": 150,
        "has_side_effect": True,
    },
    "ice-beam": {
        "energy": {
            "water": 2,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": True,
    },
    "ancient-whirlpool": {
        "energy": {
            "water": 1,
            "colorless": 2,
        },
        "damage": 70,
        "has_side_effect": True,
    },
    "sky-attack": {
        "energy": {
            "fire": 1,
            "colorless": 2,
        },
        "damage": 130,
        "has_side_effect": True,
    },
    "flamethrower": {
        "energy": {
            "fire": 2,
        },
        "damage": 90,
        "has_side_effect": True,
    },
    "heat-tackle": {
        "energy": {
            "fire": 2,
            "colorless": 1,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "stomp": {
        "energy": {
            "grass": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "soothing-scent": {
        "energy": {
            "grass": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "sharp-sting": {
        "energy": {
            "grass": 1,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "second-strike": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": True,
    },
    "do-the-wave": {
        "energy": {
            "colorless": 3,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "horn-attack": {
        "energy": {
            "darkness": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "continuous-lick": {
        "energy": {
            "colorless": 3,
        },
        "damage": 60,
        "has_side_effect": True,
    },
    "drill-peck": {
        "energy": {
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "shadow-claw": {
        "energy": {
            "colorless": 2,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "tail-smack": {
        "energy": {
            "colorless": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "metal-claw": {
        "energy": {
            "metal": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "bite": {
        "energy": {
            "colorless": 2,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "corner": {
        "energy": {
            "darkness": 1,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": True,
    },
    "knock-back": {
        "energy": {
            "fighting": 2,
            "colorless": 1,
        },
        "damage": 70,
        "has_side_effect": True,
    },
    "spiral-kick": {
        "energy": {
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "shell-attack": {
        "energy": {
            "fighting": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "horn-drill": {
        "energy": {
            "fighting": 3,
            "colorless": 1,
        },
        "damage": 100,
        "has_side_effect": False,
    },
    "bone-beatdown": {
        "energy": {
            "fighting": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "land-crush": {
        "energy": {
            "fighting": 3,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "strength": {
        "energy": {
            "fighting": 2,
        },
        "damage": 50,
        "has_side_effect": False,
    },
    "fight-back": {
        "energy": {
            "fighting": 2,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "dig": {
        "energy": {
            "fighting": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "double-lariat": {
        "energy": {
            "psychic": 2,
            "colorless": 2,
        },
        "damage": 100,
        "has_side_effect": True,
    },
    "smack": {
        "energy": {
            "water": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "barrier-attack": {
        "energy": {
            "psychic": 1,
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "will-o-wisp": {
        "energy": {
            "psychic": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "super-psy-bolt": {
        "energy": {
            "psychic": 1,
            "colorless": 2,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "magical-shot": {
        "energy": {
            "psychic": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "thunder-shock": {
        "energy": {
            "lightning": 2,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "head-bolt": {
        "energy": {
            "lightning": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "thunder-spear": {
        "energy": {
            "lightning": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "powder-snow": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "water-drip": {
        "energy": {
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "leaf-supply": {
        "energy": {
            "grass": 2,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "wave-splash": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "water-arrow": {
        "energy": {
            "water": 3,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "ko-crab": {
        "energy": {
            "water": 2,
            "colorless": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "poison-tentacles": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "knuckle-punch": {
        "energy": {
            "fighting": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "aqua-edge": {
        "energy": {
            "water": 2,
        },
        "damage": 70,
        "has_side_effect": False,
    },
    "fire-blast": {
        "energy": {
            "fire": 1,
            "colorless": 3,
        },
        "damage": 130,
        "has_side_effect": True,
    },
    "fire-claws": {
        "energy": {
            "fire": 1,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "rolling-tackle": {
        "energy": {
            "colorless": 3,
        },
        "damage": 80,
        "has_side_effect": False,
    },
    "poison-powder": {
        "energy": {
            "grass": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "sing": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "surprise-attack": {
        "energy": {
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "reckless-charge": {
        "energy": {
            "fighting": 1,
        },
        "damage": 30,
        "has_side_effect": True,
    },
    "slap": {
        "energy": {
            "psychic": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "scratch": {
        "energy": {
            "grass": 1,
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "leek-slap": {
        "energy": {
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "pound": {
        "energy": {
            "colorless": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "hyper-voice": {
        "energy": {
            "colorless": 2,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "drill-run": {
        "energy": {
            "colorless": 2,
        },
        "damage": 50,
        "has_side_effect": True,
    },
    "ram": {
        "energy": {
            "grass": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "amass": {
        "energy": {
            "metal": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "pierce": {
        "energy": {
            "metal": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "crunch": {
        "energy": {
            "metal": 1,
        },
        "damage": 20,
        "has_side_effect": True,
    },
    "suffocating-gas": {
        "energy": {
            "psychic": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "poison-gas": {
        "energy": {
            "darkness": 1,
        },
        "damage": 10,
        "has_side_effect": True,
    },
    "glide": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "call-for-family": {
        "energy": {
            "darkness": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "stretch-kick": {
        "energy": {
            "fighting": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "jab": {
        "energy": {
            "fighting": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "flop": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "low-kick": {
        "energy": {
            "fighting": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "heart-stamp": {
        "energy": {
            "psychic": 1,
            "colorless": 1,
        },
        "damage": 60,
        "has_side_effect": False,
    },
    "mumble": {
        "energy": {
            "psychic": 1,
            "colorless": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "teleport": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "quick-attack": {
        "energy": {
            "colorless": 2,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "tiny-charge": {
        "energy": {
            "lightning": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "zap-kick": {
        "energy": {
            "lightning": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "thunder-punch": {
        "energy": {
            "lightning": 2,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "rain-splash": {
        "energy": {
            "water": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "flap": {
        "energy": {
            "colorless": 2,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "splash": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "horn-hazard": {
        "energy": {
            "water": 1,
        },
        "damage": 80,
        "has_side_effect": True,
    },
    "vise-grip": {
        "energy": {
            "water": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": False,
    },
    "tongue-slap": {
        "energy": {
            "water": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "headbutt": {
        "energy": {
            "colorless": 2,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "razor-fin": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "headache": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": True,
    },
    "combustion": {
        "energy": {
            "fire": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "magma-punch": {
        "energy": {
            "fire": 2,
        },
        "damage": 50,
        "has_side_effect": False,
    },
    "flare": {
        "energy": {
            "fire": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "tail-whip": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
    "blot": {
        "energy": {
            "grass": 1,
        },
        "damage": 10,
        "has_side_effect": True,
    },
    "attach": {
        "energy": {
            "colorless": 1,
        },
        "damage": 10,
        "has_side_effect": False,
    },
    "sharp-scythe": {
        "energy": {
            "grass": 1,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "absorb": {
        "energy": {
            "grass": 1,
            "colorless": 1,
        },
        "damage": 40,
        "has_side_effect": True,
    },
    "seed-bomb": {
        "energy": {
            "grass": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "sting": {
        "energy": {
            "grass": 1,
        },
        "damage": 20,
        "has_side_effect": False,
    },
    "bug-bite": {
        "energy": {
            "colorless": 2,
        },
        "damage": 30,
        "has_side_effect": False,
    },
    "find-a-friend": {
        "energy": {
            "colorless": 1,
        },
        "damage": 0,
        "has_side_effect": True,
    },
}


def apply_damage(func: Callable) -> Callable:
    """Decorator that applies damage to the opponent's active card based on the attack used."""

    @wraps(func)
    def wrapper(player: Any, *args: Any, **kwargs: Any) -> None:
        """Wrapper function to apply damage after the attack function is called."""
        func(player, *args, **kwargs)

        # Find the attack name by converting function name to a valid format
        attack_name = func.__name__.replace("_", "-")

        # If we have valid attacks data
        if attack_name in ATTACKS:
            damage = cast(int, ATTACKS[attack_name]["damage"])

            # Apply weakness bonus
            if (
                player.opponent
                and player.opponent.active_card
                and player.active_card
                and hasattr(player.opponent.active_card, "weakness")
                and player.opponent.active_card.weakness == player.active_card.energy_type
            ):
                damage += 20

            # Apply damage
            if player.opponent and player.opponent.active_card:
                player.opponent.active_card.hp -= damage

    return cast(Callable, wrapper)


class Attack:
    """Class containing attack methods and utilities."""

    @staticmethod
    def can_use_attack(card: Any, attack_func: Callable) -> bool:
        """
        Check if a card can use the specified attack based on energy requirements.

        Args:
            card: The card attempting to use the attack
            attack_func: The attack function to check

        Returns:
            Boolean indicating if the attack can be used
        """
        # Check if the attack exists in the ATTACKS dictionary
        attack_name = attack_func.__name__.replace("_", "-")
        if attack_name not in ATTACKS:
            # Return False instead of raising an exception for safer operation
            return False

        # Ensure we have energies to check
        if not hasattr(card, "energies") or not card.energies:
            return False

        # Make a copy to avoid modifying the original
        energies = card.energies.copy()
        attack_cost: Dict[str, int] = cast(
            Dict[str, int], ATTACKS[attack_name].get("energy", {})
        )
        if not attack_cost:
            # If no energy cost defined, can always use attack
            return True

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

        # Return explicit boolean
        return bool(total_remaining_energy >= colorless_cost)

    @staticmethod
    def attack_repr(name: str, damage: int, energy_cost: Dict[str, int]) -> str:
        """
        Create a string representation of an attack.

        Args:
            name: The name of the attack
            damage: The damage value of the attack
            energy_cost: The energy cost of the attack

        Returns:
            A string representation of the attack
        """
        return f"Attack(Name: {name}, Damage: {damage}, Energy Cost: {energy_cost})"


# ------------------- SIDE EFFECTS ---------------------------------


@apply_damage
def psydrive(player: Any) -> None:
    """
    Implementation of the Psydrive attack.
    Requires removing 2 psychic energy from the active card.
    """
    if hasattr(player, "active_card") and player.active_card:
        player.active_card.remove_energy(EnergyType.PSYCHIC)
        player.active_card.remove_energy(EnergyType.PSYCHIC)


# ------------------- GENERATOR FUNCTIONS ---------------------------------


def generate_todo_attack_function(function_name: str) -> str:
    """
    Generate a TODO attack function.

    Args:
        function_name: The name of the attack function

    Returns:
        A string containing the attack function code
    """
    return f"""
    @apply_damage
    def {function_name}(player):
        # TODO ATTACK
        pass
    """


def generate_general_attack_function(function_name: str) -> str:
    """
    Generate a general attack function.

    Args:
        function_name: The name of the attack function

    Returns:
        A string containing the attack function code
    """
    return f"""
    @apply_damage
    def {function_name}(player):
        pass
    """


def add_tab_to_lines(text: str) -> str:
    """
    Add a tab (4 spaces) to the beginning of each line in the text.

    Args:
        text: The text to add tabs to

    Returns:
        The text with tabs added
    """
    return "\n".join("    " + line for line in text.splitlines())


# Collect all the attacks that have a side effect
specific_attack_methods = {}
for attack_name, attack_info in ATTACKS.items():
    if attack_info["has_side_effect"]:
        function_name = attack_name.replace("-", "_")
        specific_attack_methods[attack_name] = globals().get(function_name, None)


# Dynamically create static methods for each attack
for attack_name, attack_info in ATTACKS.items():
    attack_name = attack_name.replace("-", "_")
    if attack_name in specific_attack_methods:
        setattr(
            Attack,
            attack_name,
            staticmethod(specific_attack_methods[attack_name]),
        )
    else:
        generate_todo_attack_function(attack_name)

output_content = "# Dynamically created attack methods and their source code:\n"
output_content += "from enum import Enum" + "\n"
output_content += "from functools import wraps" + "\n\n"
output_content += inspect.getsource(AttackName) + "\n"
output_content += inspect.getsource(EnergyType) + "\n"
output_content += f"ATTACKS = {pformat(ATTACKS)}\n\n"
output_content += inspect.getsource(apply_damage) + "\n"
output_content += inspect.getsource(Attack) + "\n"

for attack_name in ATTACKS.keys():
    attack_name = attack_name.replace("-", "_")
    try:
        method = getattr(Attack, attack_name)
        try:
            output_content += add_tab_to_lines(inspect.getsource(method)) + "\n"
        except TypeError:
            output_content += generate_todo_attack_function(attack_name) + "\n"
        except OSError:
            output_content += (
                f"# Source code for {attack_name} could not be retrieved\n"
            )
    except AttributeError:
        output_content += generate_general_attack_function(attack_name) + "\n"


# Save the content to attack.py
with open("attack.py", "w") as file:
    file.write(output_content)

print("Dynamically created methods have been saved to attack.py")
