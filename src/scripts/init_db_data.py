import csv
from sqlalchemy.orm import Session
# from src.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.employee import Employee

from src.config import settings

def load_csv_data(model, csv_file):
    # DATABASE_URL: str = "mysql+pymysql://simirag:Qwerty123!@localhost:3306/analytics_db"
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj = model(**row)
                print (f"Adding {obj} to database")
                db.add(obj)
        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_csv_data(Employee, 'data/employees.csv')