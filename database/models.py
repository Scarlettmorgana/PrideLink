from sqlalchemy import Column, Integer, String, Text, Float
from database.db_setup import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False, unique=True)
    interesses = Column(Text, nullable=True)  # Lista de interesses com pesos ex.: "música:3, esportes:2"
    descricao = Column(Text, nullable=True)  # Breve descrição pessoal
    genero = Column(String, nullable=False)  # Gênero do usuário
    preferencia_sexual = Column(String, nullable=False)  # Preferência sexual do usuário
    latitude = Column(Float, nullable=True)  # Latitude para localização
    longitude = Column(Float, nullable=True)  # Longitude para localização
    hobbies_prioritarios = Column(Text, nullable=True)  # Hobbies principais

