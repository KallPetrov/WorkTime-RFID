import tkinter as tk
from tkinter import messagebox
import nfc
import threading

class NFCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFC Writer / Reader")
        self.root.geometry("400x250")

        self.label = tk.Label(root, text="NFC Reader - ACR122U", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=30)
        self.entry.insert(0, "Enter text to write...")
        self.entry.pack(pady=5)

        self.write_btn = tk.Button(root, text="📥 Write to Card", command=self.write_tag)
        self.write_btn.pack(pady=5)

        self.read_btn = tk.Button(root, text="📖 Read from Card", command=self.read_tag)
        self.read_btn.pack(pady=5)

        self.output = tk.Text(root, height=5, width=40)
        self.output.pack(pady=10)

    def write_tag(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Error", "Please enter text to write.")
            return
        threading.Thread(target=self._write_thread, args=(text,), daemon=True).start()

    def read_tag(self):
        threading.Thread(target=self._read_thread, daemon=True).start()

    def _write_thread(self, text):
        def on_connect(tag):
            if tag.ndef:
                tag.ndef.message = nfc.ndef.Message(nfc.ndef.TextRecord(text))
                self.output.insert(tk.END, f"✔️ Written: {text}\n")
            else:
                self.output.insert(tk.END, "❌ The card does not support NDEF.\n")
            return True

        try:
            with nfc.ContactlessFrontend('usb') as clf:
                self.output.insert(tk.END, "Place the NFC card near the reader...\n")
                clf.connect(rdwr={'on-connect': on_connect})
        except Exception as e:
            self.output.insert(tk.END, f"⚠️ Write error: {e}\n")

    def _read_thread(self):
        def on_connect(tag):
            if tag.ndef:
                content = ""
                for record in tag.ndef.message:
                    content += f"{record.text}\n"
                self.output.insert(tk.END, f"📖 Read from card: {content}")
            else:
                self.output.insert(tk.END, "❌ The card does not contain an NDEF message.\n")
            return True

        try:
            with nfc.ContactlessFrontend('usb') as clf:
                self.output.insert(tk.END, "Place the NFC card near the reader...\n")
                clf.connect(rdwr={'on-connect': on_connect})
        except Exception as e:
            self.output.insert(tk.END, f"⚠️ Read error: {e}\n")

def main():
    root = tk.Tk()
    app = NFCApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
