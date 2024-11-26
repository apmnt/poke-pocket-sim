class Match:
    """
    A class to represent a match between two players.

    Attributes:
        starting_player (Player): The player who will start the match.
        second_player (Player): The player who will play second.
        turn (int): The current turn number, starting at 0.
        game_over (bool): A flag indicating whether the game is over.

    Methods:
    -------
    start_turn():
        Advances the match by one turn, alternating between players.
        Checks if the game is over after each turn.
    __repr__():
        Returns a string representation of the match.
    """

    def __init__(self, starting_player, second_player):
        """
        Initializes a match between two players.

        Args:
            starting_player (Player): The player who will start the match.
            second_player (Player): The player who will play second.
        """
        starting_player.set_opponent(second_player)
        second_player.set_opponent(starting_player)
        self.starting_player = starting_player
        self.second_player = second_player

        self.turn = 0
        self.game_over = False


    def start_turn(self):
        """
        Starts a new turn in the match.

        This method increments the turn counter and determines which player goes first.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        self.turn += 1
        if self.turn % 2 == 0:
            active_player = self.second_player
            non_active_player = self.starting_player
        else:
            active_player = self.starting_player
            non_active_player = self.second_player
        print(
            f"Turn {self.turn}, {active_player.name}'s turn, {self.starting_player.name} {self.starting_player.points} - {self.second_player.name} {self.second_player.points}"
        )
        self.game_over = active_player.start_turn(self)
        if self.game_over:
            print()
            print("------ GAME OVER -------")
            print(
                f"{active_player.name} won {active_player.points}-{non_active_player.points}"
            )
            print(f"after {self.turn} turns")
        return self.game_over

    def __repr__(self):
        return f"Match(Players: {self.players}, Deck: {self.deck})"
