def log(text):
    print(text)
    with open("session_log", "a") as file:
        file.write(f"{text}\n")


def clear_log():
    with open("session_log", "w") as file:
        pass
