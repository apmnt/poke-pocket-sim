class Match:
    def __init__(self, starting_player, second_player):
        starting_player.set_opponent(second_player)
        second_player.set_opponent(starting_player)
        self.starting_player = starting_player
        self.second_player = second_player

        self.turn = 0
        self.game_over = False

    def start_turn(self):
        self.turn += 1
        if self.turn % 2 == 0:
            active_player = self.second_player
            non_active_player = self.starting_player
        else:
            active_player = self.starting_player
            non_active_player = self.second_player
        print(
            f"Turn {self.turn}, {active_player.name}'s turn, {self.starting_player.points} - {self.second_player.points}"
        )
        self.game_over = active_player.start_turn(self)
        if self.game_over:
            print(0)
            print("------ GAME OVER -------")
            print(
                f"{active_player.name} won {active_player.points}-{non_active_player.points}"
            )
            print(f"after {self.turn} turns")
        return self.game_over

    def __repr__(self):
        return f"Match(Players: {self.players}, Deck: {self.deck})"
