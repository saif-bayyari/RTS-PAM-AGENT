import csv
import os
import re
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

CSV_FILE = os.path.join(os.path.dirname(__file__), "entries.csv")


all_entries = {}


def normalize(text):
    text = text.strip()  # remove leading/trailing whitespace
    text = re.sub(
        r"\s+", " ", text
    )  # collapse all internal whitespace/newlines to single space
    text = text.encode("ascii", "ignore").decode()  # strip non-ascii characters
    return text


def save_to_csv(source, text):
    all_entries.update({str(len(all_entries)): normalize(text)})
    print(all_entries)
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["record number", "timestamp", "source", "entry"])
        writer.writerow(
            [
                str(len(all_entries)),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                source,
                text,
            ]
        )


root = tk.Tk()
root.title("RTS-PAM-Agent")
root.geometry("400x300")

selected = tk.StringVar(value="Option 1")
# dropdown = ttk.Combobox(
#    root,
#    textvariable=selected,
#    values=["Option 1", "Option 2", "Option 3"],
#    state="readonly",
# )
# dropdown.pack(pady=20)


def open_window(title):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x300")

    tk.Label(win, text=title, font=("Arial", 18, "bold")).pack(pady=(20, 10))

    textbox = tk.Text(win, font=("Arial", 12), height=8, width=40)
    textbox.pack(padx=20)

    tk.Label(
        win, text="Currently Selected Text Macro: " + selected.get(), font=("Arial", 18)
    ).pack(pady=(20, 10))

    def submit():
        text = textbox.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "Nothing to submit.", parent=win)
            return
        save_to_csv(title, text)
        textbox.delete("1.0", tk.END)
        messagebox.showinfo("Saved", f"Entry saved to entries.csv", parent=win)

    tk.Button(win, text="Submit", font=("Arial", 14, "bold"), command=submit).pack(
        pady=10
    )


cli_btn = tk.Button(
    root,
    text="CLI",
    font=("Arial", 24, "bold"),
    padx=20,
    pady=10,
    command=lambda: open_window("CLI"),
)

kb_btn = tk.Button(
    root,
    text="Knowledge Base",
    font=("Arial", 24, "bold"),
    padx=20,
    pady=10,
    command=lambda: open_window("Knowledge Base"),
)

aut_btn = tk.Button(
    root,
    text="Automated Actions",
    font=("Arial", 24, "bold"),
    padx=20,
    pady=10,
    command=lambda: open_window("Automated Actions"),
)


def open_csv_window():
    win = tk.Toplevel(root)
    win.title("CSV Entries")
    win.geometry("600x400")

    tk.Label(win, text="CSV Entries", font=("Arial", 18, "bold")).pack(pady=(15, 5))

    frame = tk.Frame(win)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        frame, font=("Arial", 11), yscrollcommand=scrollbar.set, width=80
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    def on_select(event):
        selection = listbox.curselection()

        # WHAT HAPPENS WHEN AN ITEM IS SELECTED (THE REACTION TO THE HIGHLIGHT ACTION FROM USER)
        if selection:
            value = listbox.get(selection[0])
            print(value)

    listbox.bind("<<ListboxSelect>>", on_select)

    if not os.path.isfile(CSV_FILE):
        listbox.insert(tk.END, "No entries yet.")
    else:
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                listbox.insert(tk.END, "  |  ".join(row))
                if i % 2 == 0:
                    listbox.itemconfig(i, bg="#f0f0f0")


csv_btn = tk.Button(
    root,
    text="CSV",
    font=("Arial", 24, "bold"),
    padx=20,
    pady=10,
    command=open_csv_window,
)

cli_btn.pack(expand=True)
kb_btn.pack(expand=True)
aut_btn.pack(expand=True)
csv_btn.pack(expand=True)


def load_records_from_csv():
    if not os.path.isfile(CSV_FILE):
        return
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record_id = int(row["record number"])
            all_entries[record_id] = {"record number": row["entry"]}


root.mainloop()
