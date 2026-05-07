import tkinter as tk
import tkinter.ttk as ttk
import json
import os
import game_logic as logic

lives = 3
last_errors = 0
current_level = 1

root = tk.Tk()
root.title("Typing Game")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Score.Treeview",
    background="#2e2e2e",
    fieldbackground="#2e2e2e",
    foreground="white",
    rowheight=22
)
style.configure(
    "Score.Treeview.Heading",
    background="#333333",
    foreground="white"
)

# farby
BG = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#ff69b4"

text_var = tk.StringVar(value="Zadaj meno a stlač Start")
info_var = tk.StringVar(value="")


def load_levels():

    path = os.path.join(os.path.dirname(__file__), "texts.json")

    with open(path, "r", encoding="utf-8") as f:

        texts = json.load(f)

    return [str(i + 1) for i in range(len(texts))]


level_options = load_levels()

if not level_options:

    level_options = ["1"]

selected_level = tk.IntVar(value=int(level_options[0]))
level_buttons = []
LEVEL_BTN_BG = "#ff69b4"
LEVEL_BTN_BG_SELECTED = "#ff85c2"

# scoreboard
def update_scores():

    for item in score_table.get_children():

        score_table.delete(item)

    scores = logic.read_sorted_scoreboard(selected_level.get())

    for i, entry in enumerate(scores, start=1):

        score_table.insert(
            "",
            tk.END,
            values=(
                i,
                entry["name"],
                f"{entry['time']:.2f}",
                f"{entry['accuracy']:.1f}",
                entry["wpm"],
                entry["errors"]
            )
        )


# štart hry
def start():

    global lives
    global last_errors
    global current_level

    lives = 3
    last_errors = 0

    name = name_entry.get().strip()

    if name == "":

        info_var.set("Zadaj meno")

        return

    current_level = selected_level.get()

    # LEVELY
    text = logic.get_random_text_by_level(current_level)

    text_var.set(f"LEVEL {current_level}\n\n{text}")

    info_var.set("Životy: 3")

    entry.config(state="normal")

    entry.delete(0, tk.END)

    logic.on_word("", text)

    entry.focus()


# písanie
def typing(event=None):

    global lives
    global last_errors
    global current_level

    typed = entry.get()

    text = text_var.get().split("\n\n")[1]

    result = logic.on_word(typed, text)

    if result is None:

        return

    errors = result["errors"]

    # život sa odčíta iba pri novej chybe
    if errors > last_errors:

        lives -= 1

        last_errors = errors

    if lives <= 0:

        info_var.set("GAME OVER")

        entry.config(state="disabled")

        return

    # koniec hry
    if result["finished"]:

        name = name_entry.get().strip()

        logic.write_scoreboard(name, result, current_level)

        info_var.set(
            f"LEVEL {current_level} | "
            f"Čas: {result['time']:.2f}s | "
            f"Presnosť: {result['accuracy']:.1f}% | "
            f"Slová/min: {result['wpm']}"
        )

        entry.config(state="disabled")

        update_scores()

        return

    info_var.set(f"Životy: {lives}")


# názov
title = tk.Label(
    root,
    text="TYPING GAME",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg="#ff69b4"
)

title.pack(pady=15)


# meno
name_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30,
    bg="#2e2e2e",
    fg="white",
    insertbackground="#ff69b4",
    highlightthickness=2,
    highlightbackground="#333333",
    highlightcolor="#ff69b4"
)

name_entry.pack(pady=10)


level_frame = tk.Frame(root, bg=BG)
level_frame.pack(pady=5)

level_label = tk.Label(
    level_frame,
    text="Level",
    font=("Arial", 12),
    bg=BG,
    fg=FG
)
level_label.pack(side="left", padx=6)


def set_level(level):

    global current_level

    current_level = level
    selected_level.set(level)

    for button, btn_level in level_buttons:

        is_selected = btn_level == level
        button.configure(
            bg=LEVEL_BTN_BG if is_selected else LEVEL_BTN_BG_SELECTED,
           
        )

    update_scores()


for option in level_options:

    level_value = int(option)

    button = tk.Button(
        level_frame,
        text="level "+ option,
        font=("Arial", 11, "bold"),
        bg=LEVEL_BTN_BG,
        fg=BG,
        activebackground=LEVEL_BTN_BG_SELECTED,
        activeforeground=BG,
        width=3,
        command=lambda value=level_value: set_level(value)
    )
    button.pack(side="left", padx=4)
    level_buttons.append((button, level_value))


# START BUTTON
start_btn = tk.Button(
    root,
    text="Start",
    font=("Arial", 14, "bold"),
    bg="#ff69b4",
    fg="black",
    width=10,
    command=start
)

start_btn.pack(pady=10)


# text
text_label = tk.Label(
    root,
    textvariable=text_var,
    font=("Arial", 16),
    wraplength=600,
    bg=BG,
    fg=FG,
    justify="center"
)

text_label.pack(pady=20)


# input
entry = tk.Entry(
    root,
    font=("Arial", 16),
    width=40,
    state="disabled",
    bg="#2e2e2e",
    fg="white",
    insertbackground="#ff69b4",
    highlightthickness=2,
    highlightbackground="#333333",
    highlightcolor="#ff69b4"
)

entry.pack(pady=10)

entry.bind("<KeyRelease>", typing)


# info
result_label = tk.Label(
    root,
    textvariable=info_var,
    font=("Arial", 14),
    bg=BG,
    fg=ACCENT
)

result_label.pack(pady=15)


# scoreboard
columns = ("rank", "name", "time", "accuracy", "wpm", "errors")

score_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=8,
    style="Score.Treeview"
)

score_table.heading("rank", text="#")
score_table.heading("name", text="Meno")
score_table.heading("time", text="Cas (s)")
score_table.heading("accuracy", text="Presnost %")
score_table.heading("wpm", text="Slov/min")
score_table.heading("errors", text="Chyby")

score_table.column("rank", width=40, anchor="center", stretch=False)
score_table.column("name", width=120, anchor="w")
score_table.column("time", width=80, anchor="center")
score_table.column("accuracy", width=90, anchor="center")
score_table.column("wpm", width=80, anchor="center")
score_table.column("errors", width=70, anchor="center")

score_table.pack(pady=10)

set_level(selected_level.get())

update_scores()

root.mainloop()