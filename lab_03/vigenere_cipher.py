import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.vigenere import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/encrypt"

        key_text = self.ui.txt_key.toPlainText().strip()

        # Validate key: must be non-empty and alphabetic
        if not key_text:
            QMessageBox.warning(self, "Invalid key", "Key is required and must contain only letters.")
            return

        if not key_text.isalpha():
            QMessageBox.warning(self, "Invalid key", "Key must contain only alphabetic characters (A-Z).")
            return

        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key_text
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()

                # Kiểm tra kĩ xem backend trả về "encrypted_message" hay "encrypted_text" nhé
                self.ui.txt_cipher_text.setPlainText(
                    data.get("encrypted_text", "")
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Encrypted Successfully"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Error while calling Encrypt API"
                )

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/decrypt"

        key_text = self.ui.txt_key.toPlainText().strip()

        # Validate key: must be non-empty and alphabetic
        if not key_text:
            QMessageBox.warning(self, "Invalid key", "Key is required and must contain only letters.")
            return

        if not key_text.isalpha():
            QMessageBox.warning(self, "Invalid key", "Key must contain only alphabetic characters (A-Z).")
            return

        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key_text
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json()

                # ĐÃ SỬA: Đổi từ txt_plainText thành txt_plain_text cho đồng bộ với bên trên
                self.ui.txt_plain_text.setPlainText(
                    data.get("decrypted_text", "")
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Decrypted Successfully"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Error while calling Decrypt API"
                )

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())