from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableWidget

class DataTable(QGroupBox):
    def __init__(self):
        super().__init__("Data Table")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)
