import tkinter as tk
from tkinter import messagebox

import handlers as h


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Typing Game")
    root.geometry("700x500")
    root.resizable(False, False)

    texts = h.load_texts()
    current_text = tk.StringVar(value="Klikni na Start game.")
    result_text = tk.StringVar(value="")

    def refresh_scoreboard():
        scoreboard_list.delete(0, tk.END)
        for score in h.read_sorted_scoreboard():
            scoreboard_list.insert(tk.END, score)

    def start_game():
        player_name = name_entry.get().strip()
        if not player_name:
            messagebox.showwarning("Missing name", "Najprv zadaj meno.")
            return

        selected_text = h.get_random_text(texts)
        current_text.set(selected_text)
        result_text.set("")
        input_entry.config(state="normal")
        input_entry.delete(0, tk.END)
        h.on_word("", selected_text)
        input_entry.focus_set()

    def handle_typing(_event=None):
        typed_text = input_entry.get()
        elapsed_time = h.on_word(typed_text, current_text.get())

        if elapsed_time is None:
            return

        player_name = name_entry.get().strip()
        h.write_scoreboard(player_name, elapsed_time)
        result_text.set(f"Hotovo za {elapsed_time:.2f} sekundy")
        input_entry.config(state="disabled")
        refresh_scoreboard()

    title_label = tk.Label(root, text="Typing Game", font=("Arial", 20, "bold"))
    title_label.pack(pady=(20, 10))

    name_label = tk.Label(root, text="Meno")
    name_label.pack()

    name_entry = tk.Entry(root, width=40)
    name_entry.pack(pady=(0, 10))

    start_button = tk.Button(root, text="Start game", command=start_game)
    start_button.pack(pady=(0, 15))

    text_label = tk.Label(root, textvariable=current_text, wraplength=620, justify="left")
    text_label.pack(padx=20, pady=(0, 10))

    input_label = tk.Label(root, text="Sem prepíš text")
    input_label.pack()

    input_entry = tk.Entry(root, width=60, state="disabled")
    input_entry.pack(pady=(0, 10))
    input_entry.bind("<KeyRelease>", handle_typing)

    result_label = tk.Label(root, textvariable=result_text, fg="green")
    result_label.pack(pady=(0, 15))

    scoreboard_label = tk.Label(root, text="Scoreboard")
    scoreboard_label.pack()

    scoreboard_list = tk.Listbox(root, width=50, height=10)
    scoreboard_list.pack(pady=(0, 20))

    refresh_scoreboard()
    root.mainloop()