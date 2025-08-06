import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QWidget, QHBoxLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class PDFReader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom PDF Reader")
        self.resize(800, 600)

        self.file_path = None
        self.doc = None
        self.page_number = 0

        # Widgets
        self.path_label = QLabel("File path: None")
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Scroll area for large images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)

        # Buttons
        self.open_btn = QPushButton("Upload PDF")
        self.prev_btn = QPushButton("Previous Page")
        self.next_btn = QPushButton("Next Page")

        self.open_btn.clicked.connect(self.upload_pdf)
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.path_label)
        layout.addWidget(self.scroll_area)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.open_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                self.doc = fitz.open(file_path)
                self.file_path = file_path
                self.page_number = 0
                self.path_label.setText(f"File path: {file_path}")
                print(f"Loaded file: {file_path}")
                print(f"Total pages: {len(self.doc)}")
                self.show_page(self.page_number)
            except Exception as e:
                print("Failed to load PDF:", e)

    def show_page(self, page_num):
        if self.doc and 0 <= page_num < len(self.doc):
            print(f"Showing page {page_num + 1} of {len(self.doc)}")
            page = self.doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)

            # Create QImage with a copy of the buffer
            img_format = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, img_format).copy()

            # Set the pixmap
            self.image_label.setPixmap(QPixmap.fromImage(image))
            self.image_label.adjustSize()
        else:
            print("Invalid page number.")

    def next_page(self):
        if self.doc and self.page_number < len(self.doc) - 1:
            self.page_number += 1
            self.show_page(self.page_number)

    def prev_page(self):
        if self.doc and self.page_number > 0:
            self.page_number -= 1
            self.show_page(self.page_number)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    reader = PDFReader()
    reader.show()
    sys.exit(app.exec_())
