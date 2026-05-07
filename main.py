import tkinter as tk
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

    score_list.delete(0, tk.END)

    scores = logic.read_sorted_scoreboard(selected_level.get())

    if not scores:

        score_list.insert(tk.END, "Ziadne skore")
        return

    for i, entry in enumerate(scores, start=1):

        score_list.insert(
            tk.END,
            f"{i}. name:{entry['name']} time:{entry['time']:.2f}s "
            f"accuracy:{entry['accuracy']:.1f}% wpm:{entry['wpm']} "
            f"errors:{entry['errors']}"
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
score_list = tk.Listbox(
    root,
    font=("Arial", 11),
    width=80,
    height=8,
    bg="#2e2e2e",
    fg="white",
    highlightthickness=1,
    highlightbackground="#333333",
    selectbackground="#444444",
    activestyle="none"
)

score_list.pack(pady=10)

set_level(selected_level.get())

update_scores()

root.mainloop()