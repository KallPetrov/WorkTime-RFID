import nfc

def read_from_tag():
    def connected(tag):
        print(f"Card: {tag}")
        if tag.ndef:
            for record in tag.ndef.message:
                print("📥 Read:", record.text)
        else:
            print("❌ The card does not contain an NDEF record.")
        return True

    try:
        with nfc.ContactlessFrontend('usb') as clf:
            print("Place the card near the reader...")
            clf.connect(rdwr={'on-connect': connected})
    except Exception as e:
        print("⚠️ Error:", e)

if __name__ == "__main__":
    read_from_tag()
