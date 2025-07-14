import sqlite3
import nfc
import threading
from tkinter import Toplevel, Label, Entry, Button, Text, messagebox, simpledialog
from db import add_employee

class NFCProgrammer:
    def __init__(self, window):
        self.window = window
        self.window.title("NFC Programming")
        self.window.geometry("400x280")

        Label(self.window, text="NFC Reader - ACR122U", font=("Arial", 14)).pack(pady=10)

        self.entry = Entry(self.window, width=30)
        self.entry.insert(0, "")
        self.entry.pack(pady=5)

        Button(self.window, text="📥 Write to Card", command=self.write_tag).pack(pady=5)
        Button(self.window, text="📖 Read from Card", command=self.read_tag).pack(pady=5)

        self.output = Text(self.window, height=6, width=40)
        self.output.pack(pady=10)

    def generate_next_id(self):
        conn = sqlite3.connect("data/work_log.db")
        cursor = conn.cursor()
        cursor.execute("SELECT rfid FROM employees WHERE rfid LIKE 'EMP-%'")
        rows = cursor.fetchall()
        conn.close()
        numbers = [int(row[0].split("-")[1]) for row in rows if row[0].startswith("EMP-")]
        next_number = max(numbers, default=0) + 1
        return f"EMP-{next_number:04d}"

    def write_tag(self):
        text = self.entry.get().strip()
        if not text:
            text = self.generate_next_id()
            self.output.insert("end", f"⚠️ Generated ID: {text}\n")

        threading.Thread(target=self._write_thread, args=(text,), daemon=True).start()

    def read_tag(self):
        threading.Thread(target=self._read_thread, daemon=True).start()

    def _write_thread(self, text):
        def on_connect(tag):
            if tag.ndef:
                tag.ndef.message = nfc.ndef.Message(nfc.ndef.TextRecord(text))
                self.output.insert("end", f"✔️ Written to card: {text}\n")
                name = simpledialog.askstring("Name", f"Enter employee name for ID {text}:")
                if name:
                    add_employee(text, name)
                    self.output.insert("end", f"💾 Employee saved: {name} ({text})\n")
                else:
                    self.output.insert("end", "⚠️ No name entered – employee was not saved.\n")
            else:
                self.output.insert("end", "❌ The card does not support NDEF.\n")
            return True

        try:
            with nfc.ContactlessFrontend('usb') as clf:
                self.output.insert("end", "Place card near the reader...\n")
                clf.connect(rdwr={'on-connect': on_connect})
        except Exception as e:
            self.output.insert("end", f"⚠️ Write error: {e}\n")

    def _read_thread(self):
        def on_connect(tag):
            if tag.ndef:
                content = ""
                for record in tag.ndef.message:
                    content += f"{record.text}\n"
                self.output.insert("end", f"📖 Read from card: {content}")
            else:
                self.output.insert("end", "❌ The card does not contain an NDEF message.\n")
            return True

        try:
            with nfc.ContactlessFrontend('usb') as clf:
                self.output.insert("end", "Place card near the reader...\n")
                clf.connect(rdwr={'on-connect': on_connect})
        except Exception as e:
            self.output.insert("end", f"⚠️ Read error: {e}\n")
