from sqlalchemy import create_engine, text

# Update these with your actual values or use os.getenv as in your other script
db_user = "user"
db_password = "password"  # <-- Replace with your real password
db_host = "127.0.0.1"  # Use IP instead of localhost
db_port = "5432"
db_name = "city_db"

conn_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?connect_timeout=5"
print(f"Connection string: {conn_str.replace(db_password, '***')}")

try:
    engine = create_engine(conn_str, echo=True)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1;"))
        print("Connection successful!", result.scalar())
except Exception as e:
    print(f"Connection failed: {e}")
