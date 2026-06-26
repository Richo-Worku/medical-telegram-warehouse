from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))

        for row in result:
            print(row[0])

    print("\nDatabase connection successful!")

except Exception as e:
    print("Connection failed:")
    print(e)