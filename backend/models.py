from sqlalchemy import Column, String, Float
from database import Base

class DBScan(Base):
    __tablename__ = "scans"

    # Define the columns based on Arushi's app data
    id = Column(String, primary_key=True, index=True)
    height_cm = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)