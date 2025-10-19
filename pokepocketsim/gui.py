import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import os

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon TCG Pocket")
        self.root.geometry("400x700")
        self.root.configure(bg='#1a1a2e')
        
        # Colors inspired by Pokemon TCG Pocket
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#e94560',
            'card_bg': '#0f3460',
            'text_light': '#ffffff',
            'text_dark': '#b8b8b8',
            'energy_fire': '#ff7f00',
            'energy_water': '#0077be',
            'energy_grass': '#4caf50'
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main container with gradient-like appearance
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)