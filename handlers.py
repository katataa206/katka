import time
import random

_start_time = None


def on_word(input: str, text: str):
    global _start_time

    if not input:
        _start_time = None
        return None

    if _start_time is None:
        _start_time = time.time()

    if input == text:
        end_time = time.time()
        elapsed_time = end_time - _start_time
        _start_time = None
        return elapsed_time

    return None


def get_random_text():
    with open("texts.txt", "r") as file:
        texts = [line for line in file.read().splitlines() if line.strip()]
    return random.choice(texts)


def write_scoreboard(name, elapsed_time):
    with open("scoreboard.txt", "a") as file:
        file.write(f"{name}: {elapsed_time:.2f} seconds\n")

def read_sorted_scoreboard():
    try:
        with open("scoreboard.txt", "r") as file:
            scores = [line for line in file.read().splitlines() if line.strip()]
    except FileNotFoundError:
        return []

    sorted_scores = sorted(
        scores,
        key=lambda x: float(x.split(": ")[1].split()[0])
    )
    return sorted_scores