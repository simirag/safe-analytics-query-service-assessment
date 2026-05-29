import csv
from sqlalchemy.orm import Session

from ..models.employee import Employee

def load_csv_data(file_path: str, db: Session):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.add(Employee(**row))
        db.commit()