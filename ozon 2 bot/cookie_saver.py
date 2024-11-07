import sys
import time
import pickle
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CookieSaverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.driver = None

    def initUI(self):
        self.setWindowTitle('Cookie Saver')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.link_label = QLabel('Ссылка на страницу:')
        layout.addWidget(self.link_label)

        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText("Введите ссылку на Ozon...")
        layout.addWidget(self.link_input)

        self.start_button = QPushButton('Запустить', self)
        self.start_button.clicked.connect(self.run_bot)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def run_bot(self):
        link = self.link_input.text().strip()

        if not link:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите ссылку!", QMessageBox.Ok)
            return

        self.start_browser(link)

    def start_browser(self, link):
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')

        # Запускаем браузер
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            self.driver.get(link)
            time.sleep(180)  # Ждем 3 минуты на странице

            # Сохраняем куки в файл
            cookies = self.driver.get_cookies()
            with open('cookies.pkl', 'wb') as file:
                pickle.dump(cookies, file)
            QMessageBox.information(self, "Успех", "Куки успешно сохранены в cookies.pkl", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}", QMessageBox.Ok)
        finally:
            self.driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CookieSaverApp()
    ex.show()
    sys.exit(app.exec_())
