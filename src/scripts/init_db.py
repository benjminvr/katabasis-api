import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.config.database import Base, engine
from src.models.user import User, UserNPC

print("Creating dabase tables...")
Base.metadata.create_all(bind=engine)
print("Database setup complete")
