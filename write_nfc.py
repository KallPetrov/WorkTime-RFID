import nfc
import nfc.clf

def write_to_tag(message="DEMO-ID-1234"):
    def connected(tag):
        print(f"Card detected: {tag}")
        if tag.ndef:
            record = nfc.ndef.TextRecord(message)
            tag.ndef.message = nfc.ndef.Message(record)
            print("✔️ Successfully written:", message)
        else:
            print("❌ The card does not support NDEF.")
        return True

    try:
        with nfc.ContactlessFrontend('usb') as clf:
            print("Place NFC card near the reader...")
            clf.connect(rdwr={'on-connect': connected})
    except Exception as e:
        print("⚠️ Error:", e)

if __name__ == "__main__":
    msg = input("Enter text to write on the card (e.g., name or ID): ")
    write_to_tag(msg)
