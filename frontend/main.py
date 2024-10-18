import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, QMessageBox
from PyQt5.QtCore import Qt
from ui.data_ingestion import DataIngestion
from ui.data_mining import DataMining
from ui.data_preprocessing import DataPreprocessing
from ui.machine_learning import MachineLearning
from ui.data_table import DataTable
from ui.visualisation import Visualisation

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.initUI()
        except Exception as e:
            logger.error(f"Error initializing UI: {str(e)}")
            self.show_error_message("Failed to initialize the application.")

    def initUI(self):
        self.setWindowTitle("Data Analysis Application")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Top row - buttons
        top_row = QHBoxLayout()
        main_layout.addLayout(top_row)

        try:
            self.data_table = DataTable()  # Create DataTable instance first
            self.data_ingestion = DataIngestion(self.data_table)  # Pass data_table instance
            self.data_mining = DataMining()
            self.data_preprocessing = DataPreprocessing()
            self.machine_learning = MachineLearning()

            top_row.addWidget(self.data_ingestion)
            top_row.addWidget(self.data_mining)
            top_row.addWidget(self.data_preprocessing)
            top_row.addWidget(self.machine_learning)
        except Exception as e:
            logger.error(f"Error setting up UI components: {str(e)}")
            self.show_error_message("Failed to set up UI components.")
            return

        # Bottom row - Splitter containing data table and visualisation
        try:
            vertical_splitter = QSplitter(Qt.Vertical)
            main_layout.addWidget(vertical_splitter)

            horizontal_splitter = QSplitter(Qt.Horizontal)
            self.visualisation = Visualisation()

            horizontal_splitter.addWidget(self.data_table)
            horizontal_splitter.addWidget(self.visualisation)
            horizontal_splitter.setStretchFactor(0, 1)
            horizontal_splitter.setStretchFactor(1, 1)

            vertical_splitter.addWidget(horizontal_splitter)
            vertical_splitter.setStretchFactor(2, 1)
        except Exception as e:
            logger.error(f"Error setting up splitters: {str(e)}")
            self.show_error_message("Failed to set up application layout.")
            return

        # Set equal stretch factors for uniform sizing
        for i in range(4):
            top_row.setStretch(i, 1)

        logger.info("Application UI initialized successfully")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        window = DataAnalysisApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"Unhandled exception in main application: {str(e)}")
        QMessageBox.critical(None, "Critical Error", f"An unexpected error occurred: {str(e)}\nPlease check the log file for details.")
        sys.exit(1)