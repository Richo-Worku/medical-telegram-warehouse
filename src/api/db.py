from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://postgres:population@localhost:5432/medical_warehouse"

engine = create_engine(DB_URL, pool_pre_ping=True)