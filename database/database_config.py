from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This conn string is meant for IPv4 only
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:525DloVS4uuldi0X@db.rbuwsyjyaobjdyqizakw.supabase.co:5432/postgres"
# This is meant for IPv6 via connection pooling on supabase hosted database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.rbuwsyjyaobjdyqizakw:525DloVS4uuldi0X@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

