from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from app.db.base import Base
from app.models.statistic import Statistic

engine = create_engine("sqlite:///src/app/db/stats.db", echo=False, future=True)
Session = sessionmaker(bind=engine)

def init_db():
	Base.metadata.create_all(engine)

def seed_statistics():
	stats = [
		"Total requests to /stats",
		"Total requests to /tickets*",
		"Total auth failures",
		"Total requests"
	]
	with Session() as session:
		for stat in stats:
			existing = session.query(Statistic).filter_by(statistic=stat).first()
			if not existing:
					session.add(Statistic(statistic=stat, value=0))
		session.commit()

def increment_statistic(stat_names, increment=1):
	if isinstance(stat_names, str):
		stat_names = [stat_names]

	with Session() as session:
		for stat_name in stat_names:
			stat = session.query(Statistic).filter_by(statistic=stat_name).first()
			if stat:
					stat.value += increment
			else:
					stat = Statistic(statistic=stat_name, value=increment)
					session.add(stat)
		session.commit()

def get_all_statistics():
	with Session() as session:
		stats = session.query(Statistic).all()
		return {stat.statistic: stat.value for stat in stats}

