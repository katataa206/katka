import time
import random
import json

start_time = None

def load_texts():
    with open("texts.json", "r", encoding="utf-8") as f:
        return json.load(f)


def on_word(typed, text):

    global start_time

    if typed == "":
        start_time = time.time()
        return None

    errors = 0

    for i in range(len(typed)):

        if i >= len(text):

            errors += 1

        elif typed[i] != text[i]:

            errors += 1

    if len(typed) >= len(text):

        elapsed = time.time() - start_time

        correct = len(text) - errors

        accuracy = (correct / len(text)) * 100

        wpm = round((len(text) / 5) / (elapsed / 60))

        start_time = None

        return {
            "time": elapsed,
            "accuracy": accuracy,
            "wpm": wpm,
            "errors": errors,
            "finished": True
        }

    return {
        "errors": errors,
        "finished": False
    }


def get_random_text_by_level(level):
    texts=load_texts()
    level_texts =texts[level - 1]
    return random.choice(level_texts)


def write_scoreboard(name, result, level):

    with open("scoreboard.json", "r", encoding="utf-8") as f:

        scoreboard = json.load(f)

    entry = {
        "name": name,
        "time": result.get("time", 0),
        "accuracy": result.get("accuracy", 0),
        "wpm": result.get("wpm", 0),
        "errors": result.get("errors", 0)
    }

    index = level - 1

    scoreboard[index].append(entry)
    scoreboard[index].sort(key=lambda x: float(x.get("time", 0)))
    scoreboard[index] = scoreboard[index][:10]

    with open("scoreboard.json", "w", encoding="utf-8") as f:
        json.dump(scoreboard, f, indent=2)


def read_sorted_scoreboard(level):

    with open("scoreboard.json", "r", encoding="utf-8") as f:
        scoreboard = json.load(f)

    return scoreboard[level - 1]