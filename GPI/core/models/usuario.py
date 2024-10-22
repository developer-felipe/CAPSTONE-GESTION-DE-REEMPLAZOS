from sqlalchemy import Column, String
from models.base import Base

class Usuario(Base):
   __tablename__ = "usuario"
    
id_usuario = Column(String, primary_key=True)
usuario = Column(String(16), unique=True, index=True)
password = Column(String(16))
tipo_usuario = Column(String(8))