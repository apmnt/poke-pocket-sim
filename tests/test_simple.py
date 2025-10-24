import pytest

from pokepocketsim import Card, Deck, Item, Match, Player


class TestMatch:
    """
    TestMatch:
        This test class verifies the behavior of the Match class in a simulated game environment.
        To setup games/tests, you can use a file like testmatch_psychic_gardevoir_mewtwo to
        record inputs, and then pass them into the inputs array. You can also just continuously
        run the test before the inputs array, and when it fails due to runtime error when it runs
        out of inputs, you can add the desired action int to the array.

        This testing setup needs some work as it is only able to catch exceptions in the code,
        but checking the game states is not possible.

        Setup:
            - Initializes two decks with predetermined sets of cards and items.
            - Constructs two players, each with a unique deck and player identity.
            - Instantiates a Match object using the two configured players.

        Test Method - test_attack_and_win:
            - Simulates user input using monkeypatch to replicate in-game decisions.
            - Executes a full match play sequence by invoking play_one_match.
            - Ensures that the match logic processes the actions correctly without runtime errors.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_deck1 = Deck(energy_types=["psychic"])
        self.test_deck1.add(Card.create_card("Ralts"))
        self.test_deck1.add(Card.create_card("Kirlia"))
        self.test_deck1.add(Card.create_card("Gardevoir"))
        self.test_deck1.add(Card.create_card("Mewtwo EX"))
        self.test_deck1.add(Item.Potion)
        self.test_deck1.add(Item.Potion)

        self.test_deck2 = Deck(energy_types=["psychic"])
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))
        self.test_deck2.add(Card.create_card("Ralts"))

        self.test_player1 = Player("p1", self.test_deck1, is_bot=False)
        self.test_player2 = Player("p2", self.test_deck2, is_bot=False)

        self.test_match = Match(self.test_player1, self.test_player2)

    def test_1(self):
        # TODO: Add tests after action refactoring
        assert True


if __name__ == "__main__":
    pytest.main()
