from sqlalchemy import create_engine

USERNAME = "root"
PASSWORD = "root"

HOST = "localhost"
PORT = "3306"
DATABASE = "retail_dw"

engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)