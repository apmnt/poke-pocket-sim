import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import os

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon TCG Pocket Simulator")
        self.root.geometry("400x700")
        self.root.configure(bg='#1a1a2e')
        
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#e94560',
            'card_bg': '#0f3460',
            'empty_slot_bg': '#2a2a4a',
            'text_light': '#ffffff',
            'text_dark': '#b8b8b8',
            'energy_fire': '#ff7f00',
            'energy_water': '#0077be',
            'energy_grass': '#4caf50',
            'energy_electric': '#ffd700',
            'energy_psychic': '#9c27b0'
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
        opponent_active_frame.pack(fill='x', padx=20, pady=5)

        opponent_active_card = self.create_empty_bench_slot(opponent_active_frame, f"Opponent Active")
        opponent_active_card.pack(padx=3)

        # Battle center divider
        center_frame = tk.Frame(battle_frame, bg=self.colors['accent'], height=2)
        center_frame.pack(fill='x', padx=40, pady=10)
        center_frame.pack_propagate(False)

        # Player's active Pokémon
        player_active_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_active_frame.pack(fill='x', padx=20, pady=5)

        player_active_card = self.create_empty_bench_slot(player_active_frame, f"Player Active")
        player_active_card.pack(padx=3)

        # Player's bench
        player_bench_frame = tk.Frame(battle_frame, bg=self.colors['bg_light'])
        player_bench_frame.pack(fill='x', padx=20, pady=5)
        
        # Player's bench slots (3 slots)
        player_bench_slots = tk.Frame(player_bench_frame, bg=self.colors['bg_light'])
        player_bench_slots.pack(pady=5)

        for i in range(3):
            card = self.create_empty_bench_slot(player_bench_slots, f"Player Bench {i+1}")
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
            height=70
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