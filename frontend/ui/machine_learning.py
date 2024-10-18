from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton

class MachineLearning(QGroupBox):
    def __init__(self):
        super().__init__("Machine Learning")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        regression_button = QPushButton("Regression")
        regression_button.clicked.connect(self.perform_regression)
        layout.addWidget(regression_button)

        classification_button = QPushButton("Classification")
        classification_button.clicked.connect(self.perform_classification)
        layout.addWidget(classification_button)

    def perform_regression(self):
        # Implement regression logic
        pass

    def perform_classification(self):
        # Implement classification logic
        pass
