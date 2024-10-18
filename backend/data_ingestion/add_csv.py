import pandas as pd
import os

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_frame = None

    def read_csv(self):
        """Read data from a CSV file."""
        self.data_frame = pd.read_csv(self.file_path)
        return self.data_frame

    def read_excel(self):
        """Read data from an Excel file."""
        self.data_frame = pd.read_excel(self.file_path)
        return self.data_frame

    def read_json(self):
        """Read data from a JSON file."""
        self.data_frame = pd.read_json(self.file_path)
        return self.data_frame

    def display_data(self):
        """Display the DataFrame."""
        if self.data_frame is not None:
            print(self.data_frame)
        else:
            print("No data to display.")

# Example usage
if __name__ == "__main__":
    file_path = 'data/NVIDIA.csv'

    if file_path.endswith('.csv'):
        data_reader = DataReader(file_path)
        data_reader.read_csv()
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data_reader = DataReader(file_path)
        data_reader.read_excel()
    elif file_path.endswith('.json'):
        data_reader = DataReader(file_path)
        data_reader.read_json()
    else:
        print("Unsupported file format.")

    # Display the data
    data_reader.display_data()
