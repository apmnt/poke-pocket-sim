import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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

        for i in range(3):
            card = self.create_empty_bench_slot(opponent_bench_slots, f"Opponent Bench {i+1}")
            card.pack(side='left', padx=3)

        # Opponent's active Pokémon
        opponent_active_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        opponent_active_frame.pack(fill='x', padx=20)

        self.opponent_active_card = self.create_card_placeholder(
            opponent_active_frame, 
            "Blastoise", 
            "130 HP", 
            self.colors['empty_slot_bg'],
            "Opponent Active"
        )
        self.opponent_active_card.pack()

        # Battle center divider
        center_frame = tk.Frame(battle_frame, bg=self.colors['accent'], height=2)
        center_frame.pack(fill='x', padx=40, pady=10)
        center_frame.pack_propagate(False)

        # Player's active Pokémon
        player_active_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_active_frame.pack(fill='x', padx=20, pady=5)

        self.player_active_card = self.create_card_placeholder(
            player_active_frame, 
            "Blastoise", 
            "130 HP", 
            self.colors['empty_slot_bg'],
            "Your Active"
        )
        self.player_active_card.pack()

        # Player's bench
        player_bench_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_bench_frame.pack(fill='x', padx=20, pady=5)
        
        # Player's bench slots (3 slots)
        self.player_bench_slots = tk.Frame(player_bench_frame, bg=self.colors['bg_light'])
        self.player_bench_slots.pack()

        for i in range(3):
            card = self.create_empty_bench_slot(self.player_bench_slots, f"Player Bench {i+1}")
            card.pack(side='left', padx=3)

        tk.Label(
            player_bench_frame,
            text="Your Bench",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_light']
        ).pack()

    def create_empty_bench_slot(self, parent, slot_name):
        slot = tk.Frame(
            parent,
            bg=self.colors['empty_slot_bg'],
            relief='raised',
            bd=1,
            width=100,
            height=125
        )
        slot.pack_propagate(False)
        
        # Plus icon for empty slot
        plus_label = tk.Label(
            slot,
            text="+",
            font=('Arial', 20, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['empty_slot_bg']
        )
        plus_label.pack(expand=True)
        
        # Bind click event for empty slot
        # slot.bind('<Button-1>', lambda e, s=slot_name: self.empty_slot_clicked(s))
        # plus_label.bind('<Button-1>', lambda e, s=slot_name: self.empty_slot_clicked(s))
        
        return slot
    
    def create_card_placeholder(self, parent, name, hp, energy_color, slot_type):
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
        
        card.plus_label.pack(expand=True)
        # card.name_label.pack(pady=(8, 0))
        # card.hp_label.pack()
        
        # Energy type indicator
        # energy_indicator = tk.Frame(
        #     card,
        #     bg=energy_color,
        #     width=35,
        #     height=15
        # )
        # energy_indicator.pack(pady=5)
        # energy_indicator.pack_propagate(False)
        
        # Bind click event
        # card.bind('<Button-1>', lambda e, c=name, t=slot_type: self.card_clicked(c, t))
        # for child in card.winfo_children():
        #     child.bind('<Button-1>', lambda e, c=name, t=slot_type: self.card_clicked(c, t))
        
        return card
    
    def update_gui(self, starting_player: Player, second_player: Player) -> None: 
        # Update p1 active
        if self.starting_player.active_card == None:
            self.player_active_card.plus_label.pack(expand=True)
            self.player_active_card.name_label.pack_forget()
            self.player_active_card.hp_label.pack_forget()
        else:
            self.player_active_card.plus_label.pack_forget()
            self.player_active_card.name_label.pack(pady=(8, 0))
            self.player_active_card.hp_label.pack()
            self.player_active_card.name_label['text'] = self.starting_player.active_card.name
            self.player_active_card.hp_label['text'] = str(self.starting_player.active_card.hp) + " HP"
            self.player_active_card['bg'] = self.colors[self.starting_player.active_card.type.name]

        # Update p2
        if self.second_player.active_card == None:
            self.opponent_active_card.plus_label.pack(expand=True)
            self.opponent_active_card.name_label.pack_forget()
            self.opponent_active_card.hp_label.pack_forget()
        else:
            self.opponent_active_card.plus_label.pack_forget()
            self.opponent_active_card.name_label.pack(pady=(8, 0))
            self.opponent_active_card.hp_label.pack()
            self.opponent_active_card.name_label['text'] = self.second_player.active_card.name
            self.opponent_active_card.hp_label['text'] = str(self.second_player.active_card.hp) + " HP"
            self.opponent_active_card['bg'] = self.colors[self.second_player.active_card.type.name]