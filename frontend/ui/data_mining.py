from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QComboBox, QPushButton

class DataMining(QGroupBox):
    def __init__(self):
        super().__init__("Data Mining")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        mining_combo = QComboBox()
        mining_combo.addItems(["Association Rule Mining", "Sequential Pattern Mining"])
        layout.addWidget(mining_combo)

        mining_button = QPushButton("Run Mining")
        mining_button.clicked.connect(self.run_mining)
        layout.addWidget(mining_button)

    def run_mining(self):
        # Implement data mining logic here
        pass
