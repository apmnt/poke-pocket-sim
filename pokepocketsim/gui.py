import tkinter as tk
from tkinter import ttk
from .player import Player

class GUI:
    def __init__(self, root, starting_player: Player, second_player: Player) -> None:
        self.root = root
        self.root.title("Pokemon TCG Pocket Simulator")
        self.root.geometry("400x800")
        self.root.configure(bg='#1a1a2e')

        self.starting_player = starting_player
        self.second_player = second_player

        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#e94560',
            'card_bg': '#0f3460',
            'empty_slot_bg': '#2a2a4a',
            'text_light': '#ffffff',
            'text_dark': '#b8b8b8',
            'FIRE': '#ff7f00',
            'WATER': '#0077be',
            'GRASS': '#4caf50',
            'ELECTRIC': '#ffd700',
            'PSYCHIC': "#661970"
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container with gradient-like appearance
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header with logo
        self.create_header()

        # Battle field
        self.create_battle_field()

    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Logo/text
        logo_label = tk.Label(
            header_frame,
            text="POKÉMON TCG POCKET Simulator",
            font=('Arial', 16, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        logo_label.pack()
        
        # Turn indicator
        self.turn_label = tk.Label(
            header_frame,
            text="Your Turn",
            font=('Arial', 10, 'bold'),
            fg=self.colors['text_light'],
            bg=self.colors['accent'],
            padx=10,
            pady=2
        )
        self.turn_label.pack(pady=5)

    def create_battle_field(self):
        battle_frame = tk.Frame(self.main_frame, bg=self.colors['bg_light'], relief='sunken', bd=2)
        battle_frame.pack(fill='x', pady=10, ipady=10)
        
        # Opponent's bench
        opponent_bench_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        opponent_bench_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            opponent_bench_frame,
            text="Opponent's Bench",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_light']
        ).pack()
        
        # Opponent's bench slots (3 slots)
        opponent_bench_slots = tk.Frame(opponent_bench_frame, bg=self.colors['bg_light'])
        opponent_bench_slots.pack(pady=5)
        self.opp_bench_arr = []
        for i in range(3):
            card = self.create_card_placeholder(opponent_bench_slots)
            card.pack(side='left', padx=3)
            self.opp_bench_arr.append(card)

        # Opponent's active Pokémon
        opponent_active_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        opponent_active_frame.pack(fill='x', padx=20)
        self.opp_active_card = self.create_card_placeholder(opponent_active_frame)
        self.opp_active_card.pack()

        # Battle center divider
        center_frame = tk.Frame(battle_frame, bg=self.colors['accent'], height=2)
        center_frame.pack(fill='x', padx=40, pady=10)
        center_frame.pack_propagate(False)

        # Player's active Pokémon
        player_active_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_active_frame.pack(fill='x', padx=20, pady=5)
        self.player_active_card = self.create_card_placeholder(player_active_frame)
        self.player_active_card.pack()

        # Player's bench
        player_bench_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_bench_frame.pack(fill='x', padx=20, pady=5)
        
        # Player's bench slots (3 slots)
        player_bench_slots = tk.Frame(player_bench_frame, bg=self.colors['bg_light'])
        player_bench_slots.pack()
        self.player_bench_arr = []
        for i in range(3):
            card = self.create_card_placeholder(player_bench_slots)
            card.pack(side='left', padx=3)
            self.player_bench_arr.append(card)

        tk.Label(
            player_bench_frame,
            text="Your Bench",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_light']
        ).pack()
    
    def create_card_placeholder(self, parent, name="Placeholder", hp="100 HP", energy=""):
        card = tk.Frame(
            parent,
            bg=self.colors['empty_slot_bg'],
            relief='raised',
            bd=2,
            width=100,
            height=125
        )
        card.pack_propagate(False)

        # Plus icon for empty slot
        card.plus_label = tk.Label(card, text="+", font=('Arial', 20, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['empty_slot_bg']
        )
        
        # Pokémon name
        card.name_label = tk.Label(card, text=name, font=('Arial', 9, 'bold'),
            fg=self.colors['text_light'],
            bg = card.cget('bg'),
            wraplength=80
        )
        
        # HP
        card.hp_label = tk.Label(card, text=hp, font=('Arial', 8),
            fg=self.colors['text_light'],
            bg = card.cget('bg'),
        )

        # Energy
        card.energy_label = tk.Label(card, text=energy, font=('Arial', 8),
            fg=self.colors['text_light'],
            bg = card.cget('bg'),
        )
        
        card.plus_label.pack(expand=True)
        # card.name_label.pack(pady=(8, 0))
        # card.hp_label.pack()
        # card.energy_label.pack()
        
        # Bind click event
        # card.bind('<Button-1>', lambda e, c=name, t=slot_type: self.card_clicked(c, t))
        # for child in card.winfo_children():
        #     child.bind('<Button-1>', lambda e, c=name, t=slot_type: self.card_clicked(c, t))
        
        return card

    def _update_active_placeholder(self, placeholder, card) -> None:

        if card is None:
            placeholder.plus_label.pack(expand=True)
            placeholder.name_label.pack_forget()
            placeholder.hp_label.pack_forget()
            placeholder.energy_label.pack_forget()
            placeholder['bg'] = self.colors['empty_slot_bg']
        else:
            placeholder.plus_label.pack_forget()
            placeholder.name_label.pack(pady=(8, 0))
            placeholder.hp_label.pack()
            placeholder.energy_label.pack()
            placeholder.name_label['text'] = card.name
            placeholder.hp_label['text'] = str(card.hp) + " HP"
            placeholder.energy_label['text'] = card.energies
            placeholder['bg'] = self.colors[card.energy_type.name]

    def _update_bench_placeholders(self, bench_arr, bench_cards) -> None:

        # Reset all bench slots to empty
        for i in range(3):
            bench_arr[i].plus_label.pack(expand=True)
            bench_arr[i].name_label.pack_forget()
            bench_arr[i].hp_label.pack_forget()
            bench_arr[i].energy_label.pack_forget()
            bench_arr[i]['bg'] = self.colors['empty_slot_bg']

        # Fill in present bench cards
        for i, card in enumerate(bench_cards):
            bench_arr[i].plus_label.pack_forget()
            bench_arr[i].name_label.pack(pady=(8, 0))
            bench_arr[i].hp_label.pack()
            bench_arr[i].energy_label.pack()
            bench_arr[i].name_label['text'] = card.name
            bench_arr[i].hp_label['text'] = str(card.hp) + " HP"
            bench_arr[i].energy_label['text'] = card.energies
            bench_arr[i]['bg'] = self.colors[card.energy_type.name]
    
    def update_gui(self, starting_player: Player, second_player: Player) -> None: 

        # Update p1
        self._update_active_placeholder(self.player_active_card, starting_player.active_card)
        self._update_bench_placeholders(self.player_bench_arr, starting_player.bench)

        # Update p2
        self._update_active_placeholder(self.opp_active_card, second_player.active_card)
        self._update_bench_placeholders(self.opp_bench_arr, second_player.bench)