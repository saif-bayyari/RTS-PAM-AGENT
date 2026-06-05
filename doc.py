import time

from pynput import keyboard as kb
from pynput.keyboard import Controller, Key

SNIPPETS = {
    "/greeting": "Hi there,\n\nThank you for reaching out.\n\nBest regards,\nSaif",
    "/closing": "Please let me know if you have any questions. Happy to help!\n\n— Saif",
    "/sig": "Saif | L1 Engineer @ Resolve Tech Solutions\nsaif@example.com",
    "/tix": "Ticket acknowledged. I'm looking into this now and will update you within 1 business hour.",
    "/tyvm": "Thank you very much — really appreciate it!",
}

buffer = []
MAX_BUFFER = 30
controller = Controller()


def delete_command(command: str):
    for _ in command:
        controller.tap(Key.backspace)
    time.sleep(0.02)


def type_expansion(text: str):
    for line in text.split("\n"):
        if line:
            controller.type(line)
            time.sleep(0.005)
        controller.tap(Key.enter)
    controller.tap(Key.backspace)  # remove trailing newline


def on_press(key):
    global buffer

    # Reset on trigger keys
    if key in (Key.space, Key.enter, Key.esc, Key.tab):
        buffer = []
        return

    # Backspace
    if key == Key.backspace:
        if buffer:
            buffer.pop()
        return

    # Printable characters only
    try:
        char = key.char
        if char:
            buffer.append(char)
    except AttributeError:
        buffer = []  # special key, reset
        return

    # Cap buffer
    if len(buffer) > MAX_BUFFER:
        buffer = buffer[-MAX_BUFFER:]

    current = "".join(buffer)

    for command, template in SNIPPETS.items():
        if current.endswith(command):
            time.sleep(0.05)
            delete_command(command)
            type_expansion(template)
            buffer = []
            return


def run():
    print("✓ Text expander running.")
    print("  Commands:", ", ".join(SNIPPETS.keys()))
    print("  Press Ctrl+C to stop.\n")

    listener = kb.Listener(on_press=on_press)
    listener.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()
        print("\n✗ Text expander stopped.")


run()
