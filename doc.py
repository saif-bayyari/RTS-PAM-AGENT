"""
text_expander.py — TextBlaze-style background snippet expander
Detects /commands as you type anywhere on your computer and replaces them.

Requirements:
    pip install keyboard jinja2

Run:
    python text_expander.py

On Linux you may need to run with sudo, or add yourself to the 'input' group:
    sudo python text_expander.py
"""

import time

import keyboard
from jinja2 import Environment

# ─────────────────────────────────────────
#  Your snippets — edit these freely
#  Supports Jinja2 {{ variable }} syntax
# ─────────────────────────────────────────
SNIPPETS = {
    "/greeting": """Hi there,

    Thank you for reaching out.

    Best regards,
    Saif""",
    "/closing": "Please let me know if you have any questions. Happy to help!\n\n— Saif",
    "/ooo": "I'm currently out of office. For urgent matters, please contact support@example.com.",
    "/sig": "Saif | L1 Engineer @ Resolve Tech Solutions\nsaif@example.com",
    "/tix": "Ticket acknowledged. I'm looking into this now and will update you within 1 business hour.",
    "/tyvm": "Thank you very much — really appreciate it!",
    "/mtg": "Does this time work for you?\n[ ] Monday\n[ ] Tuesday\n[ ] Wednesday",
}

# ─────────────────────────────────────────
#  Engine
# ─────────────────────────────────────────
env = Environment()
buffer = []  # tracks characters typed since last reset
MAX_BUFFER = 30  # ignore anything longer than this (perf guard)


def expand(template_str: str) -> str:
    """Render a Jinja2 template. No variables needed for most snippets."""
    return env.from_string(template_str).render()


def delete_command(command: str):
    """Backspace over the typed command so we can replace it."""
    for _ in command:
        keyboard.send("backspace")
    time.sleep(0.02)  # tiny pause so the app registers all backspaces


def type_expansion(text: str):
    """Type the expanded text, handling newlines correctly."""
    for line in text.split("\n"):
        if line:
            keyboard.write(line, delay=0.005)
        keyboard.send("enter")
    # Remove the trailing newline we just added
    keyboard.send("backspace")


def on_key(event):
    global buffer

    if event.event_type != keyboard.KEY_DOWN:
        return

    key = event.name

    # Reset buffer on space, enter, or escape
    if key in ("space", "enter", "esc", "tab"):
        buffer = []
        return

    # Handle backspace — remove last char from buffer
    if key == "backspace":
        if buffer:
            buffer.pop()
        return

    # Only track printable single chars
    if len(key) == 1:
        buffer.append(key)
    else:
        # Arrow keys, function keys etc → reset
        buffer = []
        return

    # Cap buffer length
    if len(buffer) > MAX_BUFFER:
        buffer = buffer[-MAX_BUFFER:]

    # Build current word from buffer
    current = "".join(buffer)

    # Check if the current buffer ends with any registered command
    for command, template in SNIPPETS.items():
        if current.endswith(command):
            expanded = expand(template)
            # Small delay so the last typed char registers
            time.sleep(0.05)
            delete_command(command)
            type_expansion(expanded)
            buffer = []  # reset after expansion
            return


# ─────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("✓ Text expander running. Type any /command to expand it.")
    print("  Registered commands:", ", ".join(SNIPPETS.keys()))
    print("  Press Ctrl+C to stop.\n")

    keyboard.hook(on_key)
    keyboard.wait()  # blocks forever, runs in background
