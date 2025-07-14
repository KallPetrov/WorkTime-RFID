# Reading and Writing RFID/NFC Cards with Python (nfcpy)

When working with reading and writing RFID/NFC cards in combination with Python (using nfcpy), it's important to choose a reader that:

- ✅ Supports NDEF (writing)
- ✅ Works with nfcpy or PC/SC drivers
- ✅ Is compatible with 13.56 MHz (NFC) cards

---

### ✅ Recommended NFC/RFID Readers for Python

🔹 **1. ACR122U — [Recommended]**
- 📡 Frequency: 13.56 MHz (ISO14443 A/B, MIFARE)
- 📥 Supports NDEF reading and writing
- 💻 Interface: USB
- 🎯 Compatible with nfcpy, works on Windows/Linux/Mac
- ✅ Most supported for NDEF writing in Python
- 🛒 [ACR1252U / ACR1255U-J1] [link](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/)

---

🔹 **2. ACR1252U / ACR1255U-J1**
- 🔐 Supports higher security levels (SAM slot)
- 🚀 Faster and newer models than ACR122U
- 🔌 Compatible with nfcpy, but ACR1255U requires BT configuration
- 🟡 Suitable for long-term and professional solutions

---

🔹 **3. PN532 (USB or UART)**
- 💡 Supports reading/writing, NFC peer-to-peer
- 💻 Works with nfcpy (in HSU/USB mode, not I2C)
- 🧪 More settings, more complex integration
- 🟡 Works, but more suitable for developers/hardware enthusiasts

---

❌ **To Avoid (If You Want Writing Capabilities):**
- 📛 USB 125kHz RFID readers – they do not support writing, only UID reading
- 📛 Many cheap Chinese NFC readers – often not recognized by nfcpy

---

🏆 **Recommendation #1:**
**Model**: ACR122U  
**Frequency**: 13.56 MHz  
**Interface**: USB  
**Software Support**: Excellent  
**Supports nfcpy**: ✅ Yes  
🔧 Plug & play, supports everything we do, and requires no complex configuration  

---
