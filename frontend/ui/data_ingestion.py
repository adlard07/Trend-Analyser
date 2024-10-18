import logging
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import requests

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataIngestion(QGroupBox):
    def __init__(self, data_table):
        super().__init__("Data Ingestion")
        self.setup_ui()
        self.sheets = []  # To store fetched sheets
        self.data_table = data_table  # Reference to DataTable instance
        logger.info("DataIngestion UI component initialized")

    def setup_ui(self):
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)

            # Google Sheets
            google_button = QPushButton("Connect Google Sheets")
            google_button.clicked.connect(self.google_login)
            layout.addWidget(google_button)

            self.sheets_combo = QComboBox()
            self.sheets_combo.setEnabled(False)
            layout.addWidget(self.sheets_combo)

            # Add Button
            add_button = QPushButton("Add")
            add_button.clicked.connect(self.add_sheet_to_table)
            add_button.setEnabled(False)
            layout.addWidget(add_button)

            # Enable button only when sheets are loaded
            self.sheets_combo.currentIndexChanged.connect(lambda: add_button.setEnabled(True))

            # CSV
            csv_button = QPushButton("Select CSV File")
            csv_button.clicked.connect(self.select_csv)
            layout.addWidget(csv_button)

            # Database
            db_layout = QHBoxLayout()
            db_label = QLabel("Database URL:")
            self.db_input = QLineEdit()
            db_connect = QPushButton("Connect")
            db_connect.clicked.connect(self.connect_database)
            db_layout.addWidget(db_label)
            db_layout.addWidget(self.db_input)
            db_layout.addWidget(db_connect)
            layout.addLayout(db_layout)

            logger.info("DataIngestion UI setup completed successfully")
        except Exception as e:
            logger.error(f"Error setting up DataIngestion UI: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to set up the UI: {str(e)}")

    def google_login(self):
        try:
            # Indicate loading
            self.sheets_combo.clear()
            self.sheets_combo.addItem("Loading...", None)
            # Fetch the sheets from the FastAPI backend
            response = requests.post("http://127.0.0.1:8000/load-google-sheets")
            response.raise_for_status()  # Raise an exception for bad status codes
            
            self.sheets = response.json()
            self.sheets_combo.clear()
            for sheet in self.sheets:
                self.sheets_combo.addItem(sheet['name'], sheet['id'])
            self.sheets_combo.setEnabled(True)
            logger.info(f"Successfully loaded {len(self.sheets)} Google Sheets")
        except requests.RequestException as e:
            logger.error(f"Failed to load Google Sheets: {str(e)}")
            self.sheets_combo.clear()
            QMessageBox.critical(self, "Error", f"Failed to load sheets: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during Google Sheets login: {str(e)}")
            self.sheets_combo.clear()
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def add_sheet_to_table(self):
        try:
            selected_sheet_id = self.sheets_combo.currentData()
            if selected_sheet_id:
                # Fetch sheet content from the backend
                response = requests.post(f"http://127.0.0.1:8000/load-sheet-content/{selected_sheet_id}")
                response.raise_for_status()
                
                data = response.json()
                self.data_table.display_data(data)  # Update data_table with the fetched data
                logger.info(f"Successfully loaded and displayed sheet content for sheet ID: {selected_sheet_id}")
            else:
                logger.warning("No sheet selected for adding to table")
                QMessageBox.warning(self, "Warning", "Please select a sheet to add.")
        except requests.RequestException as e:
            logger.error(f"Failed to load sheet content: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load selected sheet: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error adding sheet to table: {str(e)}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def select_csv(self):
        try:
            file_dialog = QFileDialog()
            csv_file, _ = file_dialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
            if csv_file:
                # Code to handle CSV
                logger.info(f"CSV file selected: {csv_file}")
                # Add your CSV handling logic here
            else:
                logger.info("CSV file selection cancelled")
        except Exception as e:
            logger.error(f"Error selecting CSV file: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to select CSV file: {str(e)}")

    def connect_database(self):
        try:
            db_url = self.db_input.text()
            if db_url:
                # Code to connect to database
                logger.info(f"Attempting to connect to database: {db_url}")
                # Add your database connection logic here
            else:
                logger.warning("No database URL provided")
                QMessageBox.warning(self, "Warning", "Please enter a database URL.")
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to connect to database: {str(e)}")