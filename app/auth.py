from datetime import datetime, timedelta
import pytz
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Configuração de segurança
SECRET_KEY = "sua_chave_secreta_super_segura"  # Alterar para algo mais seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Usuários fictícios (substitua por um banco de dados)
fake_users_db = {
    "usuario1": {
        "username": "usuario1",
        "full_name": "Usuário Um",
        "email": "usuario1@example.com",
        "hashed_password": pwd_context.hash("senha123"),  # "senha123"
        "disabled": False,
    }
}

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para obter hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para obter usuário pelo nome
def get_user(db, username: str):
    return db.get(username)

# Função para autenticar o usuário
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    timezone = pytz.timezone("UTC")  # Definindo o fuso horário como UTC, altere conforme necessário
    current_time = datetime.now(timezone)
    if expires_delta:
        expire = current_time + expires_delta
    else:
        expire = current_time + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Função para obter o usuário autenticado
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Não foi possível validar as credenciais"
            )
        return get_user(fake_users_db, username)
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Não foi possível validar as credenciais"
        )