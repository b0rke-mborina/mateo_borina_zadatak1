import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.stats_orm import engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
	"""Create all tables at the start of the test session and drop them at the end."""
	Base.metadata.create_all(bind=engine)
	yield
	Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
	"""Provide a transactional scope around each test."""
	connection = engine.connect()
	transaction = connection.begin()
	session = TestingSessionLocal(bind=connection)

	try:
		yield session
	finally:
		session.close()
		transaction.rollback()
		connection.close()