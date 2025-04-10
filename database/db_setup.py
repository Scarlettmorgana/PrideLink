from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Caminho para o banco de dados SQLite
DATABASE_URL = "sqlite:///pridelink.db"

# Criando a base do SQLAlchemy
Base = declarative_base()

# Criando o engine para conexão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configurando a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


