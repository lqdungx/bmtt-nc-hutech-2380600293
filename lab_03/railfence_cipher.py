import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow  # Thay bằng tên file UI của Rail Fence nếu có
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"

        # Lấy giá trị key và chuyển thành số nguyên (mặc định là 2 nếu trống)
        key_text = self.ui.txt_key.toPlainText().strip()
        if not key_text:
            QMessageBox.warning(self, "Invalid key", "Key is required and must be an integer >= 2.")
            return

        if not key_text.isdigit():
            QMessageBox.warning(self, "Invalid key", "Key must be an integer >= 2.")
            return

        key = int(key_text)
        if key < 2:
            QMessageBox.warning(self, "Invalid key", "Key must be at least 2 for Rail Fence cipher.")
            return

        plain = self.ui.txt_plain_text.toPlainText()
        if plain and key >= len(plain):
            QMessageBox.warning(self, "Invalid key", "Key should be smaller than the plain text length.")
            return

        payload = {
            "plain_text": plain,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()

                self.ui.txt_cipher_text.setPlainText(
                    data.get("encrypted_text", "")
                )

                QMessageBox.information(
                    self, "Success", "Rail Fence Encrypted Successfully"
                )
            else:
                QMessageBox.warning(
                    self, "Error", "Error while calling Encrypt API"
                )

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            QMessageBox.critical(self, "Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"

        # Lấy giá trị key và chuyển thành số nguyên
        key_text = self.ui.txt_key.toPlainText().strip()
        if not key_text or not key_text.isdigit():
            QMessageBox.warning(self, "Invalid key", "Key is required and must be an integer >= 2.")
            return

        key = int(key_text)
        if key < 2:
            QMessageBox.warning(self, "Invalid key", "Key must be at least 2 for Rail Fence cipher.")
            return

        cipher = self.ui.txt_cipher_text.toPlainText()
        if cipher and key >= len(cipher):
            QMessageBox.warning(self, "Invalid key", "Key should be smaller than the cipher text length.")
            return

        payload = {
            "cipher_text": cipher,
            "key": key
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()

                self.ui.txt_plain_text.setPlainText(
                    data.get("decrypted_text", "")
                )

                QMessageBox.information(
                    self, "Success", "Rail Fence Decrypted Successfully"
                )
            else:
                QMessageBox.warning(
                    self, "Error", "Error while calling Decrypt API"
                )

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())