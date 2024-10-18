import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import os

class Database:
    def __init__(self, db_type='mysql', user=None, password=None, host=None, port=None, db_name=None):
        self.db_type = db_type
        self.user = user or os.environ.get('DB_USER', 'your_username')
        self.password = password or os.environ.get('DB_PASSWORD', 'your_password')
        self.host = host or os.environ.get('DB_HOST', 'your_host')
        self.port = port or os.environ.get('DB_PORT', 'your_port')
        self.db_name = db_name or os.environ.get('DB_NAME', 'your_database_name')
        self.engine = self.create_engine()
        self.session = sessionmaker(bind=self.engine)()

    def create_engine(self):
        """Create a database engine based on the database type."""
        connection_string = f"{self.db_type}+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        return sa.create_engine(connection_string)

    def fetch_data(self, query):
        """
        Fetch data from the database using the provided SQL query.
        
        :param query: SQL query string
        :return: List of dictionaries containing the query results
        """
        try:
            result = self.session.execute(sa.text(query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            self.session.close()

# Example of a derived class for PostgreSQL
class PostgreSQLDatabase(Database):
    def __init__(self, user=None, password=None, host=None, port=None, db_name=None):
        super().__init__(db_type='postgresql', user=user, password=password, host=host, port=port, db_name=db_name)

# Example of a derived class for Oracle
class OracleDatabase(Database):
    def __init__(self, user=None, password=None, host=None, port=None, db_name=None):
        super().__init__(db_type='oracle', user=user, password=password, host=host, port=port, db_name=db_name)

# Example usage
if __name__ == "__main__":
    # For MySQL
    mysql_db = Database()
    mysql_query = "SELECT * FROM your_table LIMIT 10"
    mysql_data = mysql_db.fetch_data(mysql_query)
    if mysql_data:
        for row in mysql_data:
            print(row)

    # For PostgreSQL
    postgres_db = PostgreSQLDatabase()
    postgres_query = "SELECT * FROM your_table LIMIT 10"
    postgres_data = postgres_db.fetch_data(postgres_query)
    if postgres_data:
        for row in postgres_data:
            print(row)

    # For Oracle
    oracle_db = OracleDatabase()
    oracle_query = "SELECT * FROM your_table WHERE ROWNUM <= 10"
    oracle_data = oracle_db.fetch_data(oracle_query)
    if oracle_data:
        for row in oracle_data:
            print(row)
