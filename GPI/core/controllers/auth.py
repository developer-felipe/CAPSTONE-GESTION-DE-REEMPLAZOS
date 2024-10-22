from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import SessionLocal
from models import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def login_usuario(usuario: Usuario, db:Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.usuario == usuario.usuario).first()
    
    if db_usuario is None or not pwd_context.verify(usuario.password, db_usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    return {"msg": "Inicio de sesión exitoso", "tipo_usuario": db_usuario.tipo_usuario}
