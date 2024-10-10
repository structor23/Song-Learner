import customtkinter as ctk
from database import get_song_ratings

class ProgressDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.frame, text="Song Fortschritt", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        categories = ["Gesang", "Gitarre", "Zusammenspiel", "Gesamt"]
        self.progress_bars = {}

        for i, category in enumerate(categories):
            label = ctk.CTkLabel(self.frame, text=category)
            label.grid(row=i+1, column=0, sticky="e", padx=(0, 10))

            progress_bar = ctk.CTkProgressBar(self.frame, width=200)
            progress_bar.grid(row=i+1, column=1, sticky="w")
            progress_bar.set(0)

            self.progress_bars[category] = progress_bar

    def update_progress_display(self, conn, song_name):
        ratings = get_song_ratings(conn, song_name)
        
        if ratings:
            gesang = (ratings["Gesang_Textsicherheit"] + ratings["Gesang_Timing"] + 
                      ratings["Gesang_Intonation"] + ratings["Gesang_Ausdruck"]) / 4
            gitarre = (ratings["Gitarre_Arrangement"] + ratings["Gitarre_Technik"] + 
                       ratings["Gitarre_Timing"] + ratings["Gitarre_Ausdruck"]) / 4
            zusammenspiel = (ratings["Zusammenspiel_Timing"] + ratings["Zusammenspiel_Dynamik"] + 
                             ratings["Zusammenspiel_Buehnenpraesenz"] + ratings["Zusammenspiel_Performance"]) / 4
            gesamt = ratings["Overall"]

            self.progress_bars["Gesang"].set(gesang / 100)
            self.progress_bars["Gitarre"].set(gitarre / 100)
            self.progress_bars["Zusammenspiel"].set(zusammenspiel / 100)
            self.progress_bars["Gesamt"].set(gesamt / 100)
        else:
            self.reset_display()

    def reset_display(self):
        for progress_bar in self.progress_bars.values():
            progress_bar.set(0)