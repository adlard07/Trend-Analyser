import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt
from ui.data_ingestion import DataIngestion
from ui.data_mining import DataMining
from ui.data_preprocessing import DataPreprocessing
from ui.machine_learning import MachineLearning
from ui.data_table import DataTable
from ui.visualisation import Visualisation

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Top row - buttons
        top_row = QHBoxLayout()
        main_layout.addLayout(top_row)

        self.data_ingestion = DataIngestion()
        self.data_mining = DataMining()
        self.data_preprocessing = DataPreprocessing()
        self.machine_learning = MachineLearning()

        top_row.addWidget(self.data_ingestion)
        top_row.addWidget(self.data_mining)
        top_row.addWidget(self.data_preprocessing)
        top_row.addWidget(self.machine_learning)

        # Bottom row - Splitter containing data table and visualisation
        vertical_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(vertical_splitter)

        horizontal_splitter = QSplitter(Qt.Horizontal)
        self.data_table = DataTable()
        self.visualisation = Visualisation()

        horizontal_splitter.addWidget(self.data_table)
        horizontal_splitter.addWidget(self.visualisation)
        horizontal_splitter.setStretchFactor(0, 1)
        horizontal_splitter.setStretchFactor(1, 1)

        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.setStretchFactor(2, 1)
        
        # Set equal stretch factors for uniform sizing
        top_row.setStretch(0, 1)
        top_row.setStretch(1, 1)
        top_row.setStretch(2, 1)
        top_row.setStretch(3, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
