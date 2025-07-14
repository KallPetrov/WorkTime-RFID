from openpyxl import Workbook
from db import get_logs
import os

def export_to_excel():
    logs = get_logs()
    os.makedirs("logs", exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.append(["Time", "Name", "Direction"])
    for row in logs:
        ws.append(row)
    wb.save("logs/work_report.xlsx")
