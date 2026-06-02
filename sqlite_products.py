import sqlite3
import sys
from typing import List, Optional

from openpyxl import Workbook
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

DB_FILE = "products.db"


def get_connection(db_file: str = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def create_products_table(conn: sqlite3.Connection) -> None:
    sql = """
    CREATE TABLE IF NOT EXISTS Products (
        productID INTEGER PRIMARY KEY AUTOINCREMENT,
        productName TEXT NOT NULL,
        productPrice INTEGER NOT NULL
    );
    """
    conn.execute(sql)
    conn.commit()


def insert_product(conn: sqlite3.Connection, product_name: str, product_price: int) -> int:
    sql = "INSERT INTO Products (productName, productPrice) VALUES (?, ?)"
    cursor = conn.execute(sql, (product_name, product_price))
    conn.commit()
    return cursor.lastrowid


def update_product(conn: sqlite3.Connection, product_id: int, product_name: str, product_price: int) -> bool:
    sql = "UPDATE Products SET productName = ?, productPrice = ? WHERE productID = ?"
    cursor = conn.execute(sql, (product_name, product_price, product_id))
    conn.commit()
    return cursor.rowcount > 0


def get_product_by_id(conn: sqlite3.Connection, product_id: int) -> Optional[sqlite3.Row]:
    sql = "SELECT productID, productName, productPrice FROM Products WHERE productID = ?"
    cursor = conn.execute(sql, (product_id,))
    return cursor.fetchone()


def delete_product(conn: sqlite3.Connection, product_id: int) -> bool:
    sql = "DELETE FROM Products WHERE productID = ?"
    cursor = conn.execute(sql, (product_id,))
    conn.commit()
    return cursor.rowcount > 0


def list_products(conn: sqlite3.Connection) -> List[sqlite3.Row]:
    sql = "SELECT productID, productName, productPrice FROM Products ORDER BY productID"
    cursor = conn.execute(sql)
    return cursor.fetchall()


def export_products_to_excel(rows: List[sqlite3.Row], file_path: str) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Products"
    sheet.append(["productID", "productName", "productPrice"])

    for row in rows:
        sheet.append([row["productID"], row["productName"], row["productPrice"]])

    workbook.save(file_path)


class ProductApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("제품 관리")
        self.setFixedSize(800, 600)

        self.conn = get_connection()
        create_products_table(self.conn)

        self.product_name_input = QLineEdit()
        self.product_price_input = QSpinBox()
        self.product_price_input.setRange(0, 100000000)
        self.product_price_input.setSuffix(" 원")

        self.current_product_id: Optional[int] = None

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_product)

        self.update_button = QPushButton("수정")
        self.update_button.clicked.connect(self.update_selected_product)

        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_selected_product)

        self.export_button = QPushButton("엑셀 저장")
        self.export_button.clicked.connect(self.export_to_excel)

        self.product_list = QListWidget()
        self.product_list.setSelectionMode(self.product_list.SingleSelection)
        self.product_list.itemDoubleClicked.connect(self.load_selected_product)

        self.init_layout()
        self.apply_styles()
        self.load_products()

    def init_layout(self) -> None:
        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("제품 이름:"), 0, 0)
        form_layout.addWidget(self.product_name_input, 0, 1)
        form_layout.addWidget(QLabel("제품 가격:"), 1, 0)
        form_layout.addWidget(self.product_price_input, 1, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.export_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(QLabel("제품 목록:"))
        main_layout.addWidget(self.product_list, stretch=1)

        self.setLayout(main_layout)

    def apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                font-family: "Malgun Gothic", "Segoe UI", sans-serif;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QListWidget {
                background: rgba(236, 240, 241, 0.95);
                color: #2c3e50;
                border: 2px solid #2980b9;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget {
                selection-background-color: #2980b9;
                selection-color: #ffffff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1abc9c, stop:1 #16a085);
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 13px;
                min-height: 36px;
                padding: 0 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #48c9b0, stop:1 #1abc9c);
            }
            QPushButton:pressed {
                background: #13958a;
            }
            """
        )

    def load_products(self) -> None:
        self.product_list.clear()
        rows = list_products(self.conn)
        for row in rows:
            display_text = f"{row['productID']} | {row['productName']} | {row['productPrice']}원"
            self.product_list.addItem(display_text)

    def load_selected_product(self, item) -> None:
        product_id = int(item.text().split("|")[0].strip())
        row = get_product_by_id(self.conn, product_id)
        if row is None:
            return

        self.current_product_id = row["productID"]
        self.product_name_input.setText(row["productName"])
        self.product_price_input.setValue(row["productPrice"])

    def clear_form(self) -> None:
        self.current_product_id = None
        self.product_name_input.clear()
        self.product_price_input.setValue(0)

    def add_product(self) -> None:
        name = self.product_name_input.text().strip()
        price = self.product_price_input.value()

        if not name:
            QMessageBox.warning(self, "입력 오류", "제품 이름을 입력하세요.")
            return

        insert_product(self.conn, name, price)
        self.clear_form()
        self.load_products()

    def update_selected_product(self) -> None:
        if self.current_product_id is None:
            QMessageBox.warning(self, "수정 오류", "먼저 수정할 제품을 더블클릭으로 선택하세요.")
            return

        name = self.product_name_input.text().strip()
        price = self.product_price_input.value()
        if not name:
            QMessageBox.warning(self, "입력 오류", "제품 이름을 입력하세요.")
            return

        if update_product(self.conn, self.current_product_id, name, price):
            QMessageBox.information(self, "수정", "제품 정보가 수정되었습니다.")
            self.clear_form()
            self.load_products()
        else:
            QMessageBox.warning(self, "수정 실패", "제품 수정에 실패했습니다.")

    def delete_selected_product(self) -> None:
        selected = self.product_list.currentItem()
        if selected is None:
            QMessageBox.information(self, "삭제", "삭제할 제품을 선택하세요.")
            return

        product_id = int(selected.text().split("|")[0].strip())
        delete_product(self.conn, product_id)
        self.clear_form()
        self.load_products()

    def export_to_excel(self) -> None:
        rows = list_products(self.conn)
        file_path = "products_export.xlsx"
        export_products_to_excel(rows, file_path)
        QMessageBox.information(self, "엑셀 저장", f"{file_path}로 저장되었습니다.")

    def closeEvent(self, event) -> None:
        self.conn.close()
        event.accept()


def main() -> None:
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
