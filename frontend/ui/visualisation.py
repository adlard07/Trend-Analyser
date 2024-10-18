from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableWidget

class Visualisation(QGroupBox):
    def __init__(self):
        super().__init__("Visualisation")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.visual_table = QTableWidget()
        layout.addWidget(self.visual_table)
