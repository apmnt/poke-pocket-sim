import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

from match import Match
from player import Player
from deck import Deck
from card import Card, Cards
from item import Item
from action import ActionType


class PokePocketSelfPlayEnv(gym.Env):
    """
    A Gym environment wrapping the simulator in self-play mode.
    On each turn, the active player (determined by turn number) selects an action.
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(PokePocketSelfPlayEnv, self).__init__()

        # Action space.
        self.max_actions = 5
        self.action_space = spaces.Discrete(self.max_actions)

        # Observation space. (needs a lot work)
        # [Player1 points, Player2 points, turn, Player1 active hp, Player1 active max hp, Player2 active hp, Player2 active max hp]
        low = np.array([0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([10, 10, 100, 200, 300, 300, 300], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        self._setup_game()

    def _setup_game(self):
        """
        Sets up a match for self-play between two RL-controlled players.
        This method instantiates decks, players, and a match.
        """
        # Create deck for Player1.
        deck1 = Deck(energy_types=["psychic"])
        deck1.add_card(Card.create_card(Cards.RALTS))
        deck1.add_card(Card.create_card(Cards.KIRLIA))
        deck1.add_card(Card.create_card(Cards.GARDEVOIR))
        deck1.add_card(Card.create_card(Cards.MEWTWO_EX))
        deck1.add_card(Item.Potion)
        deck1.add_card(Item.Potion)

        # Create deck for Player2.
        deck2 = Deck(energy_types=["psychic"])
        deck2.add_card(Card.create_card(Cards.RALTS))
        deck2.add_card(Card.create_card(Cards.KIRLIA))
        deck2.add_card(Card.create_card(Cards.GARDEVOIR))
        deck2.add_card(Card.create_card(Cards.MEWTWO_EX))

        # Both players are RL-controlled (self-play).
        self.player1 = Player("Player1", deck1, is_bot=False)
        self.player2 = Player("Player2", deck2, is_bot=False)

        self.player1.print_actions = False
        self.player2.print_actions = False

        # Create a match with player1 as the starting player.
        self.match = Match(self.player1, self.player2)
        self.match.turn = 1

        # Determine the active player and gather its available actions.
        self.active_player = self._current_active_player()

    def _current_active_player(self):
        """
        Returns the active player based on the match turn.
        If the turn is odd, player1 is active; if even, player2 is active.
        """
        if self.match.turn % 2 == 1:
            return self.player1
        else:
            return self.player2

    def reset(self):
        """
        Resets the environment for a new episode.
        Returns:
            observation (np.array): The initial observation vector.
        """
        self._setup_game()
        return self._get_observation()

    def step(self, action):
        """
        Executes one action chosen by the RL agent for the active player.

        Args:
            action (int): An index corresponding to one of the available actions.

        Returns:
            observation (np.array): The next state representation.
            reward (float): The reward received after taking the action.
            done (bool): Whether the episode (match) is finished.
            info (dict): Additional information (empty here).
        """
        info = {}
        reward = 0
        can_continue = False

        self.available_actions = self.active_player.gather_actions()

        # if self.match.turn < 3 and any(action.action_type == ActionType.ATTACK for action in self.available_actions):
        #     print("Attack actions are not allowed in self-play mode.")

        # self.available_actions = self.active_player.gather_actions()

        # Check if the provided action index is valid.
        if action >= len(self.available_actions):
            # If the chosen action is invalid, add penalty.
            reward = -1
            return self._get_observation(), reward, can_continue, info

        # Execute the action.
        self.available_actions = self.active_player.process_rl_actions(
            self.match, self.available_actions, action_to_take=action
        )

        # Check if the game is over
        self.match.game_over = self.active_player.handle_knockout_points()

        # If the active player's turn is over (e.g. no further actions or an "End turn" was chosen),
        # then advance the match turn.
        if not self.active_player.can_continue:
            self.match.turn += 1
            # Reset the new active player's turn.
            self.active_player = self._current_active_player()
            self.active_player.setup_turn(self.match)
            self.available_actions = self.active_player.gather_actions()

        observation = self._get_observation()
        return observation, reward, can_continue, info

    def _get_observation(self):
        """
        Constructs an observation vector based on the current game state.
        Returns:
            np.array: [Player1 points, Player2 points, turn, Player1 active hp, Player1 active max hp,
                       Player2 active hp, Player2 active max hp]
        """
        # For each player, if no active card is present, use 0 values.
        p1_active_hp = self.player1.active_card.hp if self.player1.active_card else 0
        p1_active_max = (
            self.player1.active_card.max_hp if self.player1.active_card else 0
        )
        p2_active_hp = self.player2.active_card.hp if self.player2.active_card else 0
        p2_active_max = (
            self.player2.active_card.max_hp if self.player2.active_card else 0
        )

        obs = np.array(
            [
                self.player1.points,
                self.player2.points,
                self.match.turn,
                p1_active_hp,
                p1_active_max,
                p2_active_hp,
                p2_active_max,
            ],
            dtype=np.float32,
        )
        return obs

    def render(self, mode="human"):
        """
        Renders a text-based view of the game state.
        """
        print("Turn:", self.match.turn)
        print(
            "Player1 Points:",
            self.player1.points,
            "Player1 Active Card:",
            self.player1.active_card,
            "Bench:",
            self.player1.bench,
        )
        print(
            "Player2 Points:",
            self.player2.points,
            "Player2 Active Card:",
            self.player2.active_card,
            "Bench:",
            self.player2.bench,
        )

    def close(self):
        pass

    def act(self, obs, epsilon=0.1):
        if np.random.rand() < epsilon:
            return random.randint(0, self.env.max_actions - 1)
        else:
            q_values = self.network.predict(obs)
            return np.argmax(q_values)


if __name__ == "__main__":
    env = PokePocketSelfPlayEnv()
    obs = env.reset()
    match_over = False
    actions_taken = []
    reward_total = 0

    while not match_over:

        # Just a random selection for now
        env.active_player.setup_turn(env.match)

        action = random.randint(0, env.max_actions - 1)
        obs, reward, match_over, info = env.step(action)
        reward_total += reward
        actions_taken.append(action)
        if not env.active_player.can_continue:
            env.render()
            print(
                env.active_player.name,
                "- Action taken:",
                actions_taken,
                "Reward total:",
                reward_total,
            )
            actions_taken = []
            reward_total = 0
            match_over = env.match.game_over

    env.close()
