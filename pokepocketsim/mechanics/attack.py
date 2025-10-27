# Dynamically created attack methods and their source code:
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    TypeVar,
    cast,
)

from .attack_common import EnergyType

if TYPE_CHECKING:
    from ..core.card import Card
    from ..core.player import Player


# Type for attack functions
AttackFunc = Callable[["Player"], None]
F = TypeVar("F", bound=AttackFunc)


def apply_damage(func: F) -> F:
    """
    Decorator that wraps attack functions to apply damage to the opponent.

    Args:
        func: The attack function to wrap

    Returns:
        The wrapped function that handles the damage application
    """

    @wraps(func)
    def wrapper(player: "Player", *args: Any, **kwargs: Any) -> None:
        # Get the attack metadata from the card's attack info
        attack_name = func.__name__
        if player.active_card is None:
            return None

        # Find the attack info in the card's attacks list
        attack_info = None
        for attack in player.active_card.attacks:
            if attack["title"].lower().replace(" ", "_") == attack_name:
                attack_info = attack
                break

        if not attack_info:
            return None

        # Call the attack function (which may have additional side effects)
        func(player, *args, **kwargs)

        if player.opponent is None or player.opponent.active_card is None:
            return None

        # Get fixed damage from attack info
        damage = attack_info.get("fixed_damage", 0)
        if damage == 0:
            return None

        # Type effectiveness
        if player.active_card and player.opponent.active_card:
            player_card_type = str(player.active_card.energy_type)
            opponent_card_type = str(player.opponent.active_card.energy_type)

            # Apply weakness and resistance adjustments
            damage = apply_type_effects(damage, player_card_type, opponent_card_type)

        # Apply conditions
        if player.active_card and "Plus10DamageDealed" in player.active_card.conditions:
            damage += 10
        if player.active_card and "Plus30DamageDealed" in player.active_card.conditions:
            damage += 30
        if (
            player.opponent.active_card
            and "Minus20DamageReceived" in player.opponent.active_card.conditions
        ):
            damage = max(0, damage - 20)

        # Apply damage
        if player.opponent.active_card:
            player.opponent.active_card.hp -= damage
            if player.print_actions:
                print(
                    f"{player.active_card.name} attacks {player.opponent.active_card.name} for {damage} damage!"
                )

    return cast(F, wrapper)


def apply_type_effects(damage: int, attacker_type: str, defender_type: str) -> int:
    """
    Apply type effectiveness to damage calculation.

    Args:
        damage: Base damage value
        attacker_type: Type of the attacking card
        defender_type: Type of the defending card

    Returns:
        Modified damage value based on type effectiveness
    """
    # Simplify to lowercase for comparison
    attacker_type = attacker_type.lower()
    defender_type = defender_type.lower()

    # Type effectiveness logic
    multiplier = 1.0

    # Add type effectiveness rules here as needed
    if attacker_type == "water" and defender_type == "fire":
        multiplier = 2.0
    elif attacker_type == "fire" and defender_type == "grass":
        multiplier = 2.0
    elif attacker_type == "grass" and defender_type == "water":
        multiplier = 2.0
    elif attacker_type == "electric" and defender_type == "water":
        multiplier = 2.0

    # Apply the multiplier and return as int
    return int(damage * multiplier)


class Attack:
    """Class containing attack methods and utilities."""

    @staticmethod
    def can_use_attack(card: "Card", attack_func: AttackFunc) -> bool:
        """
        Check if a card can use the specified attack based on energy requirements.

        Args:
            card: The card attempting to use the attack
            attack_func: The attack function to check

        Returns:
            Boolean indicating if the attack can be used
        """
        # attack_func may be either a callable (Attack.<name>) or an attack
        # metadata dict (from Card.attacks). Normalize to attack_name.
        if isinstance(attack_func, dict):
            attack_name = attack_func.get("title", "").lower().replace(" ", "_")
        else:
            attack_name = getattr(attack_func, "__name__", "")

        # Find the corresponding attack info in the card's attack metadata
        attack_info = None
        for attack in card.attacks:
            title_as_func = attack.get("title", "").lower().replace(" ", "_")
            if title_as_func == attack_name:
                attack_info = attack
                break
                
        if not attack_info:
            return False

        required_energy = attack_info.get("energy_required", [])
        colorless_count = sum(1 for e in required_energy if e == "Colorless")
        typed_energy = [e for e in required_energy if e != "Colorless"]

        # Check each required typed energy
        for energy in typed_energy:
            energy_type = energy.lower()
            if card.energies.get(energy_type, 0) < 1:
                return False

        # Check if we have enough total energy for colorless cost
        remaining_energy = card.get_total_energy() - len(typed_energy)
        if remaining_energy < colorless_count:
            return False

        return True

    @staticmethod
    def attack_repr(name: str, damage: int, energy_cost: Dict[str, int]) -> str:
        """
        Create a string representation of an attack.

        Args:
            name: Name of the attack
            damage: Damage value of the attack
            energy_cost: Dictionary of energy costs by type

        Returns:
            String representation of the attack
        """
        energy_str = ", ".join(
            f"{count} {energy_type}" for energy_type, count in energy_cost.items()
        )
        return f"{name} ({damage} damage, {energy_str})"

    @staticmethod
    @apply_damage
    def psychic_sphere(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def psydrive(player: "Player") -> None:
        if player.active_card and player.active_card.energies.get("psychic", 0) < 2:
            if player.print_actions:
                print(
                    f"Not enough energy, only {player.active_card.energies.get('psychic', 0)} psychic energy"
                )
            return

        if player.active_card:
            player.active_card.remove_energy(EnergyType.Psychic)
            player.active_card.remove_energy(EnergyType.Psychic)

    @staticmethod
    @apply_damage
    def circle_circuit(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def slash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def crimson_storm(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def psy_report(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ice_wing(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def blizzard(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def sleepy_song(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def mega_punch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bonemerang(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def spooky_shot(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def peck(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def thundering_hurricane(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def inferno_dance(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def heat_blast(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def surf(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def hydro_bazooka(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def hydro_splash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def inferno_onrush(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tropical_swing(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def razor_leaf(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def giant_bloom(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tail_whap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def power_blast(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def gnaw(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def mega_drain(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def copy_anything(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tackle(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def rollout(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def pay_day(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sharpen(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def draco_meteor(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def wing_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def lovestrike(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def poison_horn(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def growl(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def mud_slap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def psychic(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def electro_ball(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def hydro_pump(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def fire_mane(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def hyper_beam(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def water_gun(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ember(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def double_horn(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def drool(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def vine_whip(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bubble_drain(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def gentle_slap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def lightning_ball(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def mist_slash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def gust(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def primal_wingbeat(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def dizzy_punch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def heavy_impact(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def venoshock(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def leech_life(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def double_edge(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def seismic_toss(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def psyshot(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def psypunch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bother(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def thunder_fang(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def raging_thunder(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def pin_missile(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def spinning_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def thunderbolt(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def fire_spin(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ice_beam(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ancient_whirlpool(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sky_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def flamethrower(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def heat_tackle(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def stomp(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def soothing_scent(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sharp_sting(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def second_strike(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def do_the_wave(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def horn_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def continuous_lick(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def drill_peck(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def shadow_claw(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tail_smack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def metal_claw(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bite(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def corner(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def knock_back(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def spiral_kick(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def shell_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def horn_drill(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bone_beatdown(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def land_crush(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def strength(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def fight_back(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def dig(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def double_lariat(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def smack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def barrier_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def will_o_wisp(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def super_psy_bolt(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def magical_shot(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def thunder_shock(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def head_bolt(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def thunder_spear(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def powder_snow(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def water_drip(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def leaf_supply(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def wave_splash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def water_arrow(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ko_crab(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def poison_tentacles(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def knuckle_punch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def aqua_edge(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def fire_blast(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def fire_claws(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def rolling_tackle(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def poison_powder(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sing(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def surprise_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def reckless_charge(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def slap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def scratch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def leek_slap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def pound(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def hyper_voice(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def drill_run(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def ram(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def amass(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def pierce(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def crunch(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def suffocating_gas(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def poison_gas(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def glide(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def call_for_family(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def stretch_kick(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def jab(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def flop(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def low_kick(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def heart_stamp(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def mumble(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def teleport(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def quick_attack(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tiny_charge(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def zap_kick(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def thunder_punch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def rain_splash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def flap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def splash(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def horn_hazard(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def vise_grip(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tongue_slap(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def headbutt(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def razor_fin(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def headache(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def combustion(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def magma_punch(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def flare(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def tail_whip(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def blot(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def attach(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sharp_scythe(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def absorb(player: "Player") -> None:
        # TODO ATTACK
        pass

    @staticmethod
    @apply_damage
    def seed_bomb(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def sting(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def bug_bite(player: "Player") -> None:
        pass

    @staticmethod
    @apply_damage
    def find_a_friend(player: "Player") -> None:
        pass
