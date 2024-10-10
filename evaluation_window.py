import customtkinter as ctk
from database import update_song_rating, get_song_ratings

class EvaluationWindow(ctk.CTkToplevel):
    def __init__(self, parent, song_name, conn, callback):
        super().__init__(parent)

        self.parent = parent
        self.song_name = song_name
        self.conn = conn
        self.callback = callback

        self.title(f"Bewertung: {self.song_name}")
        self.geometry("1100x600")
        self.minsize(1100, 600)  # Setze minimale Fenstergröße

        self.ratings = {}
        self.create_widgets()
        self.load_existing_ratings()

        # Fenster initial verstecken
        self.withdraw()

        # Zentrieren und Anzeigen des Fensters nach einem kurzen Delay
        self.after(100, self.show)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text=f"Bewertung für: {self.song_name}", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(20, 10))

        categories = {
            "Gesang": ["Textsicherheit", "Timing", "Intonation", "Ausdruck"],
            "Gitarre": ["Arrangement", "Technik", "Timing", "Ausdruck"],
            "Zusammenspiel": ["Timing", "Dynamik", "Buehnenpraesenz", "Performance"]
        }

        for col, (category, subcategories) in enumerate(categories.items()):
            frame = ctk.CTkFrame(self)
            frame.grid(row=1, column=col, padx=10, pady=10, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(len(subcategories) + 1, weight=1)  # Extra Zeile für Abstand unten

            ctk.CTkLabel(frame, text=category, font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 10))

            category_ratings = {}
            for i, subcategory in enumerate(subcategories):
                subframe = ctk.CTkFrame(frame)
                subframe.grid(row=i+1, column=0, pady=5, sticky="ew")
                subframe.grid_columnconfigure(1, weight=1)

                ctk.CTkLabel(subframe, text=subcategory, width=100).grid(row=0, column=0, padx=(0, 10))

                slider = ctk.CTkSlider(subframe, from_=0, to=100, number_of_steps=100, width=200)
                slider.grid(row=0, column=1, sticky="ew")
                
                value_label = ctk.CTkLabel(subframe, text="0", width=30)
                value_label.grid(row=0, column=2, padx=(10, 0))

                slider.configure(command=lambda value, label=value_label: label.configure(text=f"{int(value)}"))
                
                category_ratings[subcategory] = slider

            self.ratings[category] = category_ratings

        save_button = ctk.CTkButton(self, text="Bewertung speichern", command=self.save_evaluation)
        save_button.grid(row=2, column=0, columnspan=3, pady=20)

    def load_existing_ratings(self):
        existing_ratings = get_song_ratings(self.conn, self.song_name)
        for category, subcategories in self.ratings.items():
            for subcategory, slider in subcategories.items():
                rating_key = f"{category}_{subcategory}".replace(" ", "_")
                if rating_key in existing_ratings:
                    slider.set(existing_ratings[rating_key])
                    # Update the value label
                    for child in slider.master.winfo_children():
                        if isinstance(child, ctk.CTkLabel) and child.cget("width") == 30:
                            child.configure(text=f"{int(existing_ratings[rating_key])}")
                            break

    def save_evaluation(self):
        ratings_dict = {f"{category}_{subcategory}".replace(" ", "_"): slider.get() 
                        for category, subcategories in self.ratings.items() 
                        for subcategory, slider in subcategories.items()}
        overall_rating = sum(ratings_dict.values()) / len(ratings_dict)
        
        update_song_rating(self.conn, self.song_name, overall_rating, ratings_dict)
        
        self.callback()
        self.destroy()

    def show(self):
        self.center_window()
        self.deiconify()
        self.lift()
        self.focus_force()
        self.grab_set()

if __name__ == "__main__":
    # Nur für Testzwecke
    root = ctk.CTk()
    app = EvaluationWindow(root, "Test Song", None, lambda: print("Callback"))
    root.mainloop()