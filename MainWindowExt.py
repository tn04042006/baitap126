import os
import sys
import pandas as pd
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from baitap126.ui.MainWindow import Ui_MainWindow


class MainWindowExt(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

        self.pushButtonClose.clicked.connect(self.filter_close)
        self.pushButtonDateHighLow.clicked.connect(self.filter_date_high_low)
        self.pushButtonChitietNgay.clicked.connect(self.get_detail_by_date)
        self.pushButtonMangNgay.clicked.connect(self.filter_by_dates)
        self.pushButtonToanbo.clicked.connect(self.load_data)

    def load_data(self):
            """Tải dữ liệu từ CSV vào bảng"""
            # Xác định đường dẫn tuyệt đối của file CSV
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, '../dataset/TCB_2018_2020.csv')

            if not os.path.exists(file_path):
                print(f"File không tồn tại: {file_path}")
                return

            self.df = pd.read_csv(file_path)
            self.display_data(self.df)

    def display_data(self, df):
            """Hiển thị DataFrame lên QTableWidget"""
            self.tableWidget.setRowCount(df.shape[0])
            self.tableWidget.setColumnCount(df.shape[1])
            self.tableWidget.setHorizontalHeaderLabels(df.columns)

            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    item = QTableWidgetItem(str(df.iat[row, col]))
                    self.tableWidget.setItem(row, col, item)

    def filter_close(self):
        x = float(self.lineEditclosex.text())
        y = float(self.lineEditclosey.text())
        filtered_df = self.df[(self.df['Close'] < x) & (self.df['Close'] > y)]
        self.display_data(filtered_df)

    def filter_date_high_low(self):
        x = float(self.lineEditlowx.text())
        y = float(self.lineEditlowy.text())
        filtered_df = self.df[['Date', 'High', 'Low']][(self.df['Low'] >= x) & (self.df['Low'] <= y)]
        self.display_data(filtered_df)

    def get_detail_by_date(self):
        date_input = self.lineEditngay.text()
        filtered_df = self.df[self.df['Date'] == date_input]
        self.display_data(filtered_df)

    def filter_by_dates(self):
        dates_input = self.lineEditmangngay.text().split(',')
        filtered_df = self.df[self.df['Date'].isin(dates_input)]
        self.display_data(filtered_df)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowExt()
    window.show()
    sys.exit(app.exec())
