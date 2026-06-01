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
        key = int(key_text) if key_text.isdigit() else 2

        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
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
        key = int(key_text) if key_text.isdigit() else 2

        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
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