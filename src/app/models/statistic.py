from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Statistic(Base):
	__tablename__ = "statistic"

	id = Column(Integer, primary_key=True)
	statistic = Column(String, unique=True, nullable=False)
	value = Column(Integer, default=0, nullable=False)