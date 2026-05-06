import time
import random
import os

start_time = None

# LEVELY
current_level = 1
used_texts = []


def on_word(typed, text):

    global start_time

    # začiatok písania
    if typed == "":

        start_time = time.time()

        return None

    # chyby
    errors = 0

    for i in range(len(typed)):

        if i >= len(text):

            errors += 1

        elif typed[i] != text[i]:

            errors += 1

    # hra skončí keď dopíšeš celý text
    if len(typed) >= len(text):

        elapsed = time.time() - start_time

        # ochrana proti 0 sekundám
        if elapsed <= 0:
            elapsed = 1

        correct = len(text) - errors

        accuracy = (correct / len(text)) * 100

        if accuracy < 0:
            accuracy = 0

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


# LEVELY A TEXTY
def get_text_by_level():

    global current_level
    global used_texts

    path = os.path.join(os.path.dirname(__file__), "texts.txt")

    with open(path, "r", encoding="utf-8") as f:

        lines = [line.strip() for line in f.readlines() if line.strip()]

    # LEVEL 1
    if current_level == 1:

        level_texts = [t for t in lines if len(t) < 25]

    # LEVEL 2
    elif current_level == 2:

        level_texts = [t for t in lines if len(t) >= 25 and len(t) < 45]

    # LEVEL 3
    else:

        level_texts = [t for t in lines if len(t) >= 45]

    # odstránenie použitých viet
    available = [t for t in level_texts if t not in used_texts]

    # ďalší level
    if len(available) == 0:

        current_level += 1

        used_texts = []

        return get_text_by_level()

    # náhodná veta
    text = random.choice(available)

    used_texts.append(text)

    return text


# uloženie skóre
def write_scoreboard(name, result):

    path = os.path.join(os.path.dirname(__file__), "scoreboard.txt")

    with open(path, "a", encoding="utf-8") as f:

        f.write(
            f"{name}: "
            f"LEVEL {current_level} | "
            f"{result['time']:.2f}s | "
            f"{result['accuracy']:.1f}% | "
            f"{result['wpm']} slov/min | "
            f"chyby: {result['errors']}\n"
        )


# TOP 10 výsledkov
def read_sorted_scoreboard():

    path = os.path.join(os.path.dirname(__file__), "scoreboard.txt")

    try:

        with open(path, "r", encoding="utf-8") as f:

            lines = [line for line in f.read().splitlines() if line.strip()]

    except FileNotFoundError:

        return []

    # zoradenie podľa času
    lines.sort(key=lambda x: float(x.split("|")[1].replace("s", "").replace("LEVEL 1", "").replace("LEVEL 2", "").replace("LEVEL 3", "").strip()))

    return lines[:10]