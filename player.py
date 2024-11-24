import random
from action import Action, ActionType
from card import Card
from item import Item
from supporter import Supporter


class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck

        self.hand = [self.deck.draw_card() for _ in range(min(5, len(self.deck.cards)))]
        self.bench = []
        self.active_card = None
        self.points = 0
        self.opponent = None
        self.current_energy = None
        self.has_used_trainer = False
        self.has_added_energy = False

    def set_opponent(self, opponent):
        self.opponent = opponent

    def start_turn(self, match):
        self.reset_for_turn()

        if self.active_card:
            self.active_card.update_conditions()
        elif match.turn > 2:
            if len(self.bench) == 0:
                return True
            else:
                self.set_active_card_from_bench(random.choice(self.bench))

        drawn_card = self.deck.draw_card()
        if drawn_card is not None:
            self.hand.append(drawn_card)

        self.current_energy = self.deck.draw_energy()

        print(f"{self.name} hand: ", [c for c in self.hand])

        # Gather actions
        actions = self.gather_actions()

        # Do random action
        if len(actions) > 0:
            # Print
            print("Possible actions:")
            for action in actions:
                print("\t", action)
            random_action = actions.pop(random.randint(0, len(actions) - 1))
            can_continue = True
        else:
            can_continue = False

        while can_continue is True:
            can_continue = random_action.act(self)
            if random_action.action_type == ActionType.SET_ACTIVE_CARD:
                actions = [
                    action
                    for action in actions
                    if action.action_type != ActionType.SET_ACTIVE_CARD
                ]
                if match.turn > 2:
                    actions = self.gather_actions()
            else:
                if random_action.action_type == ActionType.ADD_ENERGY:
                    self.has_added_energy = True
                if random_action.action_type == ActionType.SUPPORTER:
                    self.has_used_trainer = True
                if random_action.action_type == ActionType.ITEM:
                    self.hand.remove(
                        next(
                            card
                            for card in self.hand
                            if isinstance(card, random_action.item_class)
                        )
                    )
                actions = self.gather_actions()

            if len(actions) > 0:
                random_action = actions.pop(random.randint(0, len(actions) - 1))
            else:
                can_continue = False

        print(f"Current active card of {self.name} is {self.active_card}")
        if self.opponent.active_card is not None and self.opponent.active_card.hp <= 0:
            print(
                f"{self.opponent.name}'s {self.opponent.active_card.name} knocked out!"
            )

            if self.opponent.active_card.is_ex:
                self.points += 2
            else:
                self.points += 1

            self.opponent.active_card = None

            if self.points >= 3:
                return True
        else:
            print(
                f"Current active card of {self.opponent.name} is {self.opponent.active_card}"
            )
        print()
        return False

    def gather_actions(self):
        actions = []
        if self.active_card is not None:

            # ITEM
            for card in self.hand:
                if type(card) == Item.Potion:
                    for pokemon in self.bench + [self.active_card]:
                        if Item.Potion.card_able_to_use(pokemon):
                            actions.append(
                                Action(
                                    f"Use potion on ({pokemon})",
                                    lambda pokemon=pokemon: Item.Potion.use(pokemon),
                                    ActionType.ITEM,
                                    item_class=Item.Potion,
                                )
                            )

                # Break if trainer has already been used this turn
                if self.has_used_trainer:
                    break

                if type(card) == Supporter.Erika:
                    for pokemon in self.bench + [self.active_card]:
                        if Supporter.Erika.card_able_to_use(pokemon):
                            actions.append(
                                Action(
                                    f"Use Erika on ({pokemon})",
                                    lambda pokemon=pokemon: Supporter.Erika.use(
                                        pokemon
                                    ),
                                    ActionType.ITEM,
                                    item_class=Supporter.Erika,
                                )
                            )

            # RETREAT
            actions.extend(self.active_card.gather_actions())
            if (
                self.active_card.get_total_energy() >= self.active_card.retreat_cost
                and len(self.bench) > 0
            ):
                actions.append(
                    Action(
                        f"Retreat active card ({self.active_card})",
                        self.retreat,
                        ActionType.FUNCTION,
                    )
                )

            # ADD CARD TO BENCH
            for card in self.hand:
                if type(card) == Card and card.is_basic:
                    actions.append(
                        Action(
                            f"Add {card.name} to bench",
                            lambda card=card: self.add_card_to_bench(card),
                            ActionType.ADD_CARD_TO_BENCH,
                        )
                    )

            # ADD ENERGY
            if self.has_added_energy is False:
                actions.append(
                    Action(
                        f"Add {self.current_energy} energy to {self.active_card}",
                        lambda card=self.active_card: card.add_energy(
                            self.current_energy
                        ),
                        ActionType.ADD_ENERGY,
                    )
                )
                for card in self.bench:
                    actions.append(
                        Action(
                            f"Add {self.current_energy} energy to {card}",
                            lambda card=card: card.add_energy(self.current_energy),
                            ActionType.ADD_ENERGY,
                        )
                    )

        # SET AN ACTIVE CARD
        else:
            for card in self.hand:
                if type(card) == Card and card.is_basic:
                    actions.append(
                        Action(
                            f"Set {card.name} as active card",
                            lambda card=card: self.set_active_card_from_hand(card),
                            ActionType.SET_ACTIVE_CARD,
                        )
                    )
        return actions

    def retreat(self):
        if self.active_card.get_total_energy() < self.active_card.retreat_cost:
            raise Exception(f"Not enough energy to retreat {self.active_card.name}")

        self.active_card.remove_retreat_cost_energy()

        old_active_card = self.active_card
        self.active_card = random.choice(self.bench)
        self.bench.remove(self.active_card)
        self.bench.append(old_active_card)
        print(
            f"{old_active_card.name} retreated, {self.active_card.name} set as active"
        )

    def set_active_card_from_hand(self, card):
        print(f"Setting active card from hand to {card.name}")
        self.active_card = card
        self.hand.remove(card)

    def set_active_card_from_bench(self, card):
        print(f"Setting active card from bench to {card.name}")
        self.active_card = card
        self.bench.remove(card)

    def add_card_to_bench(self, card):
        if card not in self.hand:
            raise Exception(f"Card {card.name} not in hand")
        if len(self.bench) < 3:
            self.bench.append(card)
            self.hand.remove(card)

    def reset_for_turn(self):
        self.has_added_energy = False
        self.has_used_trainer = False

    def __repr__(self):
        return f"Player({self.name}, Hand: {self.hand}, Active Card: {self.active_card}, Bench: {self.bench}, Deck: {self.deck}, Energy Queue: {self.energy_queue}, Points: {self.points}, Has Used Trainer This Turn: {self.has_used_trainer})"
