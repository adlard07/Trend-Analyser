import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from data_ingestion.google_sheets import GoogleDriveClient
from data_ingestion.add_csv import DataReader
from data_ingestion.integrate_db import Database, PostgreSQLDatabase, OracleDatabase
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

@app.post("/load-google-sheets")
async def load_google_sheets():
    try:
        sheets = google_drive_client.fetch_sheets()
        logger.info(f"Successfully fetched {len(sheets)} Google Sheets")
        return sheets
    except Exception as e:
        logger.error(f"Error fetching Google Sheets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch Google Sheets: {str(e)}")

@app.post("/load-sheet-content/{sheet_id}")
async def load_sheet_content(sheet_id: str):
    try:
        content = google_drive_client.fetch_sheet_content(sheet_id)
        if content is not None:
            logger.info(f"Successfully loaded content from sheet {sheet_id}")
            return content
        else:
            logger.warning(f"No content found in sheet {sheet_id}")
            return {"detail": "No content found in the sheet"}
    except Exception as e:
        logger.error(f"Error loading sheet content for {sheet_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load sheet content: {str(e)}")

@app.post("/load-csv")
def load_csv(data: CSVFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_csv()
        logger.info(f"Successfully loaded CSV file: {data.file_path}")
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error loading CSV file {data.file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load CSV file: {str(e)}")

@app.post("/load-excel")
def load_excel(data: ExcelFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_excel()
        logger.info(f"Successfully loaded Excel file: {data.file_path}")
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error loading Excel file {data.file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load Excel file: {str(e)}")

@app.post("/load-json")
def load_json(data: JSONFilePath):
    try:
        data_reader = DataReader(data.file_path)
        df = data_reader.read_json()
        logger.info(f"Successfully loaded JSON file: {data.file_path}")
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error loading JSON file {data.file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load JSON file: {str(e)}")

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
            logger.error(f"Unsupported database type: {query.db_type}")
            raise HTTPException(status_code=400, detail="Unsupported database type.")

        # Fetch data from the database
        data = db.fetch_data(query.query)
        if data:
            logger.info(f"Successfully executed SQL query on {query.db_type} database")
            return data
        else:
            logger.warning("SQL query returned no data")
            raise HTTPException(status_code=404, detail="No data found.")
    except Exception as e:
        logger.error(f"Error executing SQL query on {query.db_type} database: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to execute SQL query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the FastAPI application")
    uvicorn.run(app, host="127.0.0.1", port=8000)