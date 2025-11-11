from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Disable SQLAlchemy pool because Supabase uses its own pooler
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Read the schema.sql file
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
with open(schema_path, "r", encoding="utf-8") as file:
    schema_sql = file.read()


# Execute all SQL commands
try:
    with engine.begin() as conn:  # begin() = auto commit/rollback
        conn.execute(text(schema_sql))
        print("✅ Database schema created successfully!")
except Exception as e:
    print(f"❌ Failed to initialize database: {e}")