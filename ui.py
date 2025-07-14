import tkinter as tk
from tkinter import messagebox, simpledialog
from db import log_event, get_last_direction, get_employee_name, add_employee, get_logs
from excel_export import export_to_excel
import rfid_reader
import threading
import time
from nfc_programmer import NFCProgrammer

class WorkTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WorkTime RFID by Hexagon Lab")

        self.label = tk.Label(root, text="⏳ Waiting for card...", font=("Arial", 12))
        self.label.pack(pady=10)

        self.add_btn = tk.Button(root, text="Add Employee", command=self.add_employee)
        self.add_btn.pack(pady=5)

        self.export_btn = tk.Button(root, text="Export to Excel", command=self.export_excel)
        self.export_btn.pack(pady=5)

        self.show_logs_btn = tk.Button(root, text="History", command=self.show_logs)
        self.show_logs_btn.pack(pady=5)

        self.nfc_prog_btn = tk.Button(root, text="NFC Programming", command=self.open_nfc_programmer)
        self.nfc_prog_btn.pack(pady=10)

        threading.Thread(target=self.auto_scan_loop, daemon=True).start()

    def auto_scan_loop(self):
        last_card = None
        while True:
            try:
                rfid = rfid_reader.read_rfid()
                if rfid and rfid != last_card:
                    last_card = rfid
                    name = get_employee_name(rfid)
                    last = get_last_direction(rfid)
                    direction = "OUT" if last == "IN" else "IN"
                    log_event(rfid, direction)
                    print(f"{name} → {direction}")
                    self.label.config(text=f"{name} marked {direction}")
                    time.sleep(2)
                time.sleep(0.1)
            except Exception:
                time.sleep(0.2)

    def add_employee(self):
        rfid = rfid_reader.read_rfid()
        name = simpledialog.askstring("Name", "Enter employee's name:")
        if name:
            add_employee(rfid, name)
            messagebox.showinfo("Added", f"{name} has been added successfully.")

    def export_excel(self):
        export_to_excel()
        messagebox.showinfo("Export", "Data has been exported to work_report.xlsx")

    def show_logs(self):
        logs = get_logs()
        top = tk.Toplevel(self.root)
        top.title("History")
        text = tk.Text(top, width=60, height=20)
        text.pack()
        for entry in logs:
            text.insert(tk.END, f"{entry[0]} - {entry[1]} - {entry[2]}\n")

    def open_nfc_programmer(self):
        NFCProgrammer(tk.Toplevel(self.root))

def start_gui():
    root = tk.Tk()
    root.title("WorkTime RFID by Hexagon Lab")
    root.geometry("350x400")

    # 👇 Зареждане на икона (icon.ico)
    try:
        root.iconbitmap("rfid.ico")  # Увери се, че icon.ico е в същата директория
    except Exception as e:
        print(f"Неуспешно зареждане на икона: {e}")

    app = WorkTimeApp(root)
    root.mainloop()
