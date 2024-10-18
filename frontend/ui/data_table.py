import logging
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTable(QGroupBox):
    def __init__(self):
        super().__init__("Data Table")
        try:
            self.setup_ui()
            logger.info("DataTable UI component initialized")
        except Exception as e:
            logger.error(f"Error initializing DataTable: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to initialize DataTable: {str(e)}")

    def setup_ui(self):
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)

            self.data_table = QTableWidget()
            layout.addWidget(self.data_table)
            
            logger.info("DataTable UI setup completed successfully")
        except Exception as e:
            logger.error(f"Error setting up DataTable UI: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to set up the DataTable UI: {str(e)}")

    def display_data(self, data):
        """Display data in the table."""
        try:
            if data:
                if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
                    raise ValueError("Invalid data format. Expected a list of lists.")
                
                self.data_table.setRowCount(len(data))
                self.data_table.setColumnCount(len(data[0]))

                for row_index, row in enumerate(data):
                    for column_index, value in enumerate(row):
                        self.data_table.setItem(row_index, column_index, QTableWidgetItem(str(value)))
                
                logger.info(f"Successfully displayed data in table. Rows: {len(data)}, Columns: {len(data[0])}")
            else:
                self.data_table.clear()
                self.data_table.setRowCount(0)
                self.data_table.setColumnCount(0)
                logger.info("Cleared the data table due to empty data")
        except ValueError as ve:
            logger.error(f"Invalid data format: {str(ve)}")
            QMessageBox.warning(self, "Warning", f"Invalid data format: {str(ve)}")
        except Exception as e:
            logger.error(f"Error displaying data in table: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to display data: {str(e)}")

    def clear_table(self):
        """Clear the data table."""
        try:
            self.data_table.clear()
            self.data_table.setRowCount(0)
            self.data_table.setColumnCount(0)
            logger.info("Data table cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing data table: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to clear data table: {str(e)}")

    def get_data(self):
        """Retrieve data from the table."""
        try:
            rows = self.data_table.rowCount()
            cols = self.data_table.columnCount()
            data = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = self.data_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            logger.info(f"Successfully retrieved data from table. Rows: {rows}, Columns: {cols}")
            return data
        except Exception as e:
            logger.error(f"Error retrieving data from table: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to retrieve data from table: {str(e)}")
            return None