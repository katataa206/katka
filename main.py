import tkinter as tk
import game_logic as logic

lives = 3
last_errors = 0

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

# scoreboard
def update_scores():

    listbox.delete(0, tk.END)

    scores = logic.read_sorted_scoreboard()

    for i in range(len(scores)):

        listbox.insert(tk.END, f"{i + 1}. {scores[i]}")


# štart hry
def start():

    global lives
    global last_errors

    lives = 3
    last_errors = 0

    name = name_entry.get().strip()

    if name == "":

        info_var.set("Zadaj meno")

        return

    # LEVELY
    text = logic.get_text_by_level()

    text_var.set(f"LEVEL {logic.current_level}\n\n{text}")

    info_var.set("Životy: 3")

    entry.config(state="normal")

    entry.delete(0, tk.END)

    logic.on_word("", text)

    entry.focus()


# písanie
def typing(event=None):

    global lives
    global last_errors

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

        logic.write_scoreboard(name, result)

        info_var.set(
            f"LEVEL {logic.current_level} | "
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
listbox = tk.Listbox(
    root,
    font=("Arial", 12),
    width=50,
    height=8,
    bg="#2e2e2e",
    fg="white"
)

listbox.pack(pady=10)

update_scores()

root.mainloop()