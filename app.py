import customtkinter as ctk
from tkinter import ttk, messagebox
import json
from evaluation_window import EvaluationWindow
from database import create_connection, create_tables, check_database_values
from song_operations import add_song as db_add_song, delete_song as db_delete_song, get_all_songs
from progress_display import ProgressDisplay

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SongList(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self["columns"] = ("name", "overall_rating", "gesang", "gitarre", "zusammenspiel")
        self["show"] = "headings"
        
        self.heading("name", text="Songname", command=lambda: self.master.master.on_sort_column("name"))
        self.heading("overall_rating", text="Gesamtbewertung", command=lambda: self.master.master.on_sort_column("overall_rating"))
        self.heading("gesang", text="Gesang", command=lambda: self.master.master.on_sort_column("gesang"))
        self.heading("gitarre", text="Gitarre", command=lambda: self.master.master.on_sort_column("gitarre"))
        self.heading("zusammenspiel", text="Zusammenspiel", command=lambda: self.master.master.on_sort_column("zusammenspiel"))
        
        self.column("name", width=200, anchor="w")
        self.column("overall_rating", width=100, anchor="center")
        self.column("gesang", width=100, anchor="center")
        self.column("gitarre", width=100, anchor="center")
        self.column("zusammenspiel", width=100, anchor="center")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Song Lernstatus")
        self.geometry("1200x680")
        
        self.conn = create_connection()
        create_tables(self.conn)
        check_database_values(self.conn)

        self.current_sort = {"column": "name", "order": "ascending"}
        self.load_sort_settings()

        self.create_widgets()
        self.update_song_list()
        
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)

        logo_label = ctk.CTkLabel(sidebar_frame, text="Song Learner", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        ctk.CTkButton(sidebar_frame, text="Song hinzufügen", command=self.add_song).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(sidebar_frame, text="Song bewerten", command=self.open_evaluation_window).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(sidebar_frame, text="Song löschen", command=self.delete_song).grid(row=3, column=0, padx=20, pady=10)

        # Main area
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.song_list = SongList(main_frame)
        self.song_list.grid(row=0, column=0, sticky="nsew")
        self.song_list.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.progress_display = ProgressDisplay(main_frame)
        self.progress_display.frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

    def add_song(self):
        song_name = ctk.CTkInputDialog(text="Geben Sie den Namen des Songs ein:", title="Song hinzufügen").get_input()
        if song_name:
            db_add_song(self.conn, song_name)
            self.update_song_list()

    def open_evaluation_window(self):
        selected_items = self.song_list.selection()
        if not selected_items:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Song aus der Liste aus.")
            return

        song_name = self.song_list.item(selected_items[0])['values'][0]
        EvaluationWindow(self, song_name, self.conn, self.update_after_evaluation)

    def delete_song(self):
        selected_items = self.song_list.selection()
        if not selected_items:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Song aus der Liste aus.")
            return

        song_name = self.song_list.item(selected_items[0])['values'][0]
        if messagebox.askyesno("Löschen bestätigen", f"Möchten Sie '{song_name}' wirklich löschen?"):
            db_delete_song(self.conn, song_name)
            self.update_song_list()
            self.progress_display.reset_display()

    def update_song_list(self):
        self.song_list.delete(*self.song_list.get_children())
        songs = get_all_songs(self.conn)
        for song in songs:
            name, overall, gesang, gitarre, zusammenspiel, _ = song
            formatted_song = (
                name,
                f"{float(overall):.2f}%" if overall is not None else "N/A",
                f"{float(gesang):.2f}%" if gesang is not None else "N/A",
                f"{float(gitarre):.2f}%" if gitarre is not None else "N/A",
                f"{float(zusammenspiel):.2f}%" if zusammenspiel is not None else "N/A"
            )
            self.song_list.insert("", "end", values=formatted_song)
        self.sort_song_list()

    def sort_song_list(self):
        column = self.current_sort["column"]
        reverse = self.current_sort["order"] == "descending"
        items = [(self.song_list.set(k, column), k) for k in self.song_list.get_children('')]
        
        def sort_key(item):
            value = item[0].rstrip('%')
            return float(value) if value.replace('.', '', 1).isdigit() else item[0]

        items.sort(reverse=reverse, key=sort_key)
        for index, (val, k) in enumerate(items):
            self.song_list.move(k, '', index)

    def on_sort_column(self, column):
        if self.current_sort["column"] == column:
            self.current_sort["order"] = "descending" if self.current_sort["order"] == "ascending" else "ascending"
        else:
            self.current_sort["column"] = column
            self.current_sort["order"] = "ascending"
        self.sort_song_list()
        self.save_sort_settings()

    def on_tree_select(self, event):
        selected_items = self.song_list.selection()
        if selected_items:
            song_name = self.song_list.item(selected_items[0])['values'][0]
            self.progress_display.update_progress_display(self.conn, song_name)

    def update_after_evaluation(self):
        self.update_song_list()
        selected_items = self.song_list.selection()
        if selected_items:
            song_name = self.song_list.item(selected_items[0])['values'][0]
            self.progress_display.update_progress_display(self.conn, song_name)

    def load_sort_settings(self):
        try:
            with open("sort_settings.json", "r") as f:
                self.current_sort = json.load(f)
        except FileNotFoundError:
            pass

    def save_sort_settings(self):
        with open("sort_settings.json", "w") as f:
            json.dump(self.current_sort, f)

if __name__ == "__main__":
    app = App()
    app.mainloop()