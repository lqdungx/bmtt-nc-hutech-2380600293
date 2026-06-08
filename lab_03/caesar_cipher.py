import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        key_text = self.ui.txt_key.toPlainText().strip()

        # Validate key: must be an integer between 0 and 25
        if not key_text:
            QMessageBox.warning(self, "Invalid key", "Key is required and must be an integer between 0 and 25.")
            return

        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid key", "Key must be an integer between 0 and 25.")
            return

        if key < 0 or key > 25:
            QMessageBox.warning(self, "Invalid key", "Key must be between 0 and 25.")
            return

        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)  # Debug dữ liệu API trả về

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.ui.txt_cipher_text.setPlainText(data.get("encrypted_message", ""))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        key_text = self.ui.txt_key.toPlainText().strip()

        # Validate key: must be an integer between 0 and 25
        if not key_text:
            QMessageBox.warning(self, "Invalid key", "Key is required and must be an integer between 0 and 25.")
            return

        try:
            key = int(key_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid key", "Key must be an integer between 0 and 25.")
            return

        if key < 0 or key > 25:
            QMessageBox.warning(self, "Invalid key", "Key must be between 0 and 25.")
            return

        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)  # Debug dữ liệu API trả về

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.ui.txt_plain_text.setPlainText(data.get("decrypted_message", ""))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
            else:
                print("Error while calling API")

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())