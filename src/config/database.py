import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL Config
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_DB = os.getenv("POSTGRES_DB", "katabasis")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # Use "postgres" (service name)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Database URL
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
print("🔗 DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis Config
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Use "redis" (service name)
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ PostgreSQL connection successful")
    except Exception as e:
        print(f"❌ PostgreSQL connection error: {e}")

    try:
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection error: {e}")
