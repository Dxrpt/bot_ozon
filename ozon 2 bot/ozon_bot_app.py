import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QDateEdit, QCheckBox, QTextEdit, QTimeEdit, QMessageBox
)
from PyQt5.QtCore import QDateTime, Qt, QTimer, QThread
from PyQt5.QtGui import QFont
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class OzonBotThread(QThread):
    def __init__(self, link, use_proxy, proxy=None):
        super().__init__()
        self.link = link
        self.use_proxy = use_proxy
        self.proxy = proxy
        self.driver = None

    def run(self):
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if self.use_proxy and self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        start_time = time.time()

        try:
            self.log_message(f"Открытие ссылки: {self.link}")
            self.driver.get(self.link)
            time.sleep(5)

            self.click_button('//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button/div[2]')
            time.sleep(2)

            self.click_button('//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div/div/div[1]/div[3]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button/div[2]')

            self.log_message("Обе кнопки успешно нажаты.")

        except Exception as e:
            self.log_message(f"Ошибка: {str(e)}")

        elapsed_time = time.time() - start_time
        self.log_message(f"Время выполнения: {elapsed_time:.2f} секунд.")

        while True:
            pass

    def click_button(self, xpath):
        try:
            button = self.driver.find_element(By.XPATH, xpath)
            button.click()
            self.log_message(f"Кнопка нажата: {xpath}")
        except Exception as e:
            self.log_message(f"Не удалось нажать кнопку {xpath}: {str(e)}")

    def log_message(self, message):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"[{current_time}] {message}")


class OzonBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)

    def initUI(self):
        self.setWindowTitle('Ozon Bot')
        self.setGeometry(100, 100, 450, 700)
        self.setStyleSheet("background-color: #E6F7FF;")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel('Ozon Bot', self)
        self.title_label.setFont(QFont("Arial", 26, QFont.Bold))
        self.title_label.setStyleSheet("color: #0056B3; text-align: center;")
        layout.addWidget(self.title_label)

        self.link_input = self.create_input_field(layout, "Ссылка на товар:", "Введите ссылку на товар...")
        self.link_input.setText(
            "https://www.ozon.ru/product/myagkaya-antistressovaya-igrushka-homyak-misha-15-sm-plyushevye-zhivotnye-ot-bloptop-1174182764/?__rr=3&campaignId=439")

        self.time_checkbox = QCheckBox('Использовать запланированное время')
        layout.addWidget(self.time_checkbox)

        self.date_input = self.create_date_edit(layout, 'Дата закупки:')
        self.time_input = self.create_time_edit(layout, 'Время закупки:')

        self.proxy_checkbox = QCheckBox('Использовать прокси-сервер')
        layout.addWidget(self.proxy_checkbox)

        self.proxy_input = self.create_input_field(layout, "Прокси-сервер:", "Введите прокси в формате IP:PORT")

        # Обновленная кнопка запуска бота
        self.start_bot_button = QPushButton('Запустить бота', self)
        self.start_bot_button.setStyleSheet(self.get_button_style())
        self.start_bot_button.clicked.connect(self.run_bot)
        layout.addWidget(self.start_bot_button)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: white; border: 1px solid #0056B3; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def create_input_field(self, layout, label_text, placeholder):
        label = QLabel(label_text)
        layout.addWidget(label)
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.get_input_style())
        layout.addWidget(input_field)
        return input_field

    def create_date_edit(self, layout, label_text):
        label = QLabel(label_text)
        layout.addWidget(label)
        date_input = QDateEdit(self)
        date_input.setDate(QDateTime.currentDateTime().date())
        date_input.setStyleSheet(self.get_input_style())
        layout.addWidget(date_input)
        return date_input

    def create_time_edit(self, layout, label_text):
        label = QLabel(label_text)
        layout.addWidget(label)
        time_input = QTimeEdit(self)
        time_input.setTime(QDateTime.currentDateTime().time())
        time_input.setStyleSheet(self.get_input_style())
        layout.addWidget(time_input)
        return time_input

    def get_input_style(self):
        return """
            QLineEdit, QDateEdit, QTimeEdit {
                background-color: #ffffff;
                border: 1px solid #0056B3;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus {
                border: 1px solid #0056B3;
                background-color: #E0F7FF;
            }
        """

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #0056B3;
                color: white;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #003366;
            }
            QPushButton:pressed {
                background-color: #003366;
            }
        """

    def run_bot(self):
        link = self.link_input.text().strip()
        use_proxy = self.proxy_checkbox.isChecked()
        proxy = self.proxy_input.text().strip() if use_proxy else None

        if not link:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите ссылку на товар!", QMessageBox.Ok)
            return

        self.log_output.append(f"Запуск бота...\nСсылка: {link}\nИспользование прокси: {'Да' if use_proxy else 'Нет'}")

        if self.time_checkbox.isChecked():
            self.schedule_bot(link, use_proxy, proxy)
        else:
            self.start_bot_in_thread(link, use_proxy, proxy)

    def schedule_bot(self, link, use_proxy, proxy):
        self.log_output.append(
            f"Запланирована покупка товара...\nСсылка: {link}\nДата: {self.date_input.date().toString()}\nВремя: {self.time_input.time().toString()}")
        self.target_time = QDateTime(self.date_input.date(), self.time_input.time())
        self.timer.start(1000)
        self.timer.timeout.connect(lambda: self.check_time(link, use_proxy, proxy))

    def check_time(self, link, use_proxy, proxy):
        current_time = QDateTime.currentDateTime()
        remaining_time = self.target_time.secsTo(current_time)

        if remaining_time > 0:
            self.log_output.append(f"Ожидание: осталось {remaining_time} секунд до запуска.")
        else:
            self.timer.stop()
            self.log_output.append("Время для покупки наступило.")
            self.start_bot_in_thread(link, use_proxy, proxy)

    def start_bot_in_thread(self, link, use_proxy, proxy):
        self.bot_thread = OzonBotThread(link, use_proxy, proxy)
        self.bot_thread.start()
        self.bot_thread.finished.connect(self.on_bot_finished)

    def on_bot_finished(self):
        self.log_output.append("Бот завершил работу.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot_app = OzonBotApp()
    bot_app.show()
    sys.exit(app.exec_())
