import customtkinter as ctk
from tkinter import ttk
from database import get_all_songs

class SongList:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn
        self.frame = ctk.CTkFrame(parent)
        self.create_song_list()

    def create_song_list(self):
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.frame, columns=("name", "gesang", "gitarre", "zusammenspiel", "overall"), show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize(), command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree.column(col, anchor="center", width=100)
        self.tree.column("name", anchor="w", width=200)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.update_song_list()

    def update_song_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        songs = get_all_songs(self.conn)
        print(f"Aktualisiere Songliste mit {len(songs)} Songs")  # Debug-Ausgabe
        for song in songs:
            song_id, name, gesang, gitarre, zusammenspiel, overall_rating = song
            
            self.tree.insert("", "end", values=(
                name,
                f"{gesang:.1f}%" if gesang is not None else "N/A",
                f"{gitarre:.1f}%" if gitarre is not None else "N/A",
                f"{zusammenspiel:.1f}%" if zusammenspiel is not None else "N/A",
                f"{overall_rating:.1f}%" if overall_rating is not None else "N/A"
            ))
            print(f"Füge Song hinzu: {name}")  # Debug-Ausgabe

    def sort_treeview(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(key=lambda t: float(t[0].rstrip('%')) if t[0] != "N/A" else -1, reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))