import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow  # Đảm bảo đường dẫn này đúng với file UI của bạn
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def generate_and_format_matrix(self, key_text):
        """Hàm tự động sinh ma trận 5x5 từ Key và định dạng chuỗi hiển thị"""
        if not key_text:
            return ""
            
        key_text = key_text.upper().replace('J', 'I')
        clean_key = []
        for char in key_text:
            if char.isalpha() and char not in clean_key:
                clean_key.append(char)
                
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in clean_key:
                clean_key.append(char)
                
        matrix_lines = []
        for i in range(0, 25, 5):
            row = clean_key[i:i+5]
            matrix_lines.append("    ".join(row))  
            
        return "\n".join(matrix_lines)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        key_value = self.ui.txt_key.toPlainText().strip()

        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": key_value
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

                formatted_matrix = self.generate_and_format_matrix(key_value)
                self.ui.txt_matrix.setPlainText(formatted_matrix)

                QMessageBox.information(
                    self, "Success", "Playfair Encrypted Successfully"
                )
            else:
                QMessageBox.warning(
                    self, "Error", "Error while calling Encrypt API"
                )

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            QMessageBox.critical(self, "Error", str(e))

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        key_value = self.ui.txt_key.toPlainText().strip()

        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": key_value
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

                formatted_matrix = self.generate_and_format_matrix(key_value)
                self.ui.txt_matrix.setPlainText(formatted_matrix)

                QMessageBox.information(
                    self, "Success", "Playfair Decrypted Successfully"
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