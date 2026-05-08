import tkinter as tk
import game_logic as logic

lives = 3
last_errors = 0
current_level = 1

root = tk.Tk()
root.title("Typing Game")
root.geometry("700x500")
root.configure(bg="#1e1e1e")


BG = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#ff69b4"

text_var = tk.StringVar(value="Zadaj meno a stlač Start")
info_var = tk.StringVar(value="")

level_count = len(logic.load_texts())

selected_level = tk.IntVar(value=1)
level_buttons = []
LEVEL_BTN_BG = "#ff69b4"
LEVEL_BTN_BG_SELECTED = "#ff85c2"


def update_scores():

    score_list.delete(0, tk.END)
    scores = logic.read_sorted_scoreboard(selected_level.get())

    for i, entry in enumerate(scores, start=1):
        score_list.insert(
            tk.END,
            f"{i}. Meno: {entry['name']} | Čas: {entry['time']:.2f}s "
            f"| Presnosť: {entry['accuracy']:.1f}% | Slová/min: {entry['wpm']} "
            f"| Chyby: {entry['errors']}"
        )

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

    text = logic.get_random_text_by_level(current_level)
    text_var.set(f"LEVEL {current_level}\n\n{text}")
    info_var.set("Životy: 3")
    entry.config(state="normal")
    entry.delete(0, tk.END)
    logic.on_word("", text)
    entry.focus()

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

    if errors > last_errors:
        lives -= 1
        last_errors = errors

    if lives <= 0:
        info_var.set("GAME OVER")
        entry.config(state="disabled")
        return

    
    if result["finished"]:
        name = name_entry.get().strip()

        logic.write_scoreboard(name, result, current_level)

        info_var.set(
            f"LEVEL {current_level} | "
            f"Čas: {result['time']:.2f}s | "
            f"Presnosť: {result['accuracy']:.1f}% | "
            f"Slová/min: {result['wpm']} | "
            f"Chyby: {result['errors']}"
        )

        entry.config(state="disabled")
        update_scores()
        return

    info_var.set(f"Životy: {lives}")

title = tk.Label(
    root,
    text="TYPING GAME",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg="#ff69b4"
)

title.pack(pady=15)

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
    update_scores()

for level_value in range(1, level_count + 1):

    button = tk.Button(
        level_frame,
        text=f"level {level_value}",
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

result_label = tk.Label(
    root,
    textvariable=info_var,
    font=("Arial", 14),
    bg=BG,
    fg=ACCENT
)

result_label.pack(pady=15)

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