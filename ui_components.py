import tkinter as tk
from tkinter import ttk

def create_tree(parent):
    columns = ("name", "gesang", "gitarre", "zusammenspiel", "overall")
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    
    tree.heading("name", text="Songname", command=lambda: sort_column(tree, "name", False))
    tree.heading("gesang", text="Gesang", command=lambda: sort_column(tree, "gesang", True))
    tree.heading("gitarre", text="Gitarre", command=lambda: sort_column(tree, "gitarre", True))
    tree.heading("zusammenspiel", text="Zusammenspiel", command=lambda: sort_column(tree, "zusammenspiel", True))
    tree.heading("overall", text="Gesamt", command=lambda: sort_column(tree, "overall", False))
    
    tree.column("name", width=200, anchor="w")
    tree.column("gesang", width=100, anchor="center")
    tree.column("gitarre", width=100, anchor="center")
    tree.column("zusammenspiel", width=100, anchor="center")
    tree.column("overall", width=100, anchor="center")

    return tree

def create_progress_bar(parent, category):
    frame = ttk.Frame(parent)
    frame.pack(fill='x', pady=10)
    ttk.Label(frame, text=f"{category}:", width=15).pack(side='left')
    progress = ttk.Progressbar(frame, length=300, mode='determinate', style="TProgressbar")
    progress.pack(side='left', padx=(0, 10))
    value_label = ttk.Label(frame, text="0%")
    value_label.pack(side='left')
    return (progress, value_label)

def update_progress_color(progress_bar, value):
    if value < 30:
        progress_bar.config(style="red.Horizontal.TProgressbar")
    elif value < 80:
        progress_bar.config(style="yellow.Horizontal.TProgressbar")
    else:
        progress_bar.config(style="green.Horizontal.TProgressbar")

def sort_column(tree, col, reverse):
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    
    if col != "name":
        l.sort(reverse=reverse, key=lambda x: float(x[0].rstrip('%')) if x[0].strip() != "N/A" else -1)
    else:
        l.sort(reverse=reverse, key=lambda x: x[0].lower())

    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))