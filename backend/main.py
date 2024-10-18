from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from data_ingestion.google_sheets import GoogleDriveClient
from data_ingestion.add_csv import DataReader
from data_ingestion.integrate_db import Database, PostgreSQLDatabase, OracleDatabase
from pydantic import BaseModel

app = FastAPI()

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Drive Client for Sheets
google_drive_client = GoogleDriveClient()

# Define Data Request Models
class CSVFilePath(BaseModel):
    file_path: str

class ExcelFilePath(BaseModel):
    file_path: str

class JSONFilePath(BaseModel):
    file_path: str

class GoogleSheetRequest(BaseModel):
    sheet_id: str
    range_name: str = 'Sheet1!A1:Z1000'

class SQLQuery(BaseModel):
    db_type: str
    query: str
    user: str = None
    password: str = None
    host: str = None
    port: str = None
    db_name: str = None

@app.post("/load-google-sheet")
def load_google_sheet(data: GoogleSheetRequest):
    try:
        sheet_data = google_drive_client.fetch_sheet_content(data.sheet_id, data.range_name)
        if not sheet_data:
            raise HTTPException(status_code=404, detail="No data found in the sheet.")
        
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-csv")
def load_csv(data: CSVFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_csv()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-excel")
def load_excel(data: ExcelFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_excel()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-json")
def load_json(data: JSONFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_json()
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute-sql")
def execute_sql(query: SQLQuery):
    try:
        # Determine which database to use
        if query.db_type.lower() == 'mysql':
            db = Database(user=query.user, password=query.password, host=query.host, port=query.port, db_name=query.db_name)
        elif query.db_type.lower() == 'postgresql':
            db = PostgreSQLDatabase(user=query.user, password=query.password, host=query.host, port=query.port, db_name=query.db_name)
        elif query.db_type.lower() == 'oracle':
            db = OracleDatabase(user=query.user, password=query.password, host=query.host, port=query.port, db_name=query.db_name)
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type.")

        # Fetch data from the database
        data = db.fetch_data(query.query)
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="No data found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
