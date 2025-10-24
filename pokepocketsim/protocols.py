from typing import TYPE_CHECKING, List, Protocol

from .mechanics.condition import ConditionBase

if TYPE_CHECKING:
    from .mechanics.attack_common import EnergyType


class ICard(Protocol):
    energy_type: "EnergyType"
    hp: int
    max_hp: int
    name: str

    def add_condition(self, condition: ConditionBase) -> None: ...


class IPlayer(Protocol):
    active_card: ICard
    bench: List[ICard]
    opponent: "IPlayer"

    def move_active_card_to_bench(self) -> None: ...


class ISupporter(Protocol):
    name: str

    def card_able_to_use(self, card: ICard) -> bool: ...
