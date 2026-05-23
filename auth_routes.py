from fastapi import APIRouter, Depends, HTTPException
from models import User, Order, OrderItem
from dependencies import pick_session, verificate_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from dependencies import pick_session
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dict_info = {"sub": str(user_id), "exp": expiration_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user: 
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False 
    return user

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False} 

@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session: Session = Depends(pick_session)):
    #Abre uma sessão que busca os usuários e filtra entre eles, qual usuário tem o email IGUAL ao email enviado
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password, user_schema.active, user_schema.admin)
        session.add(new_user)  
        session.commit()  
        return {"mensagem": f"usuário cadastrado com sucesso{user_schema.email}"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pick_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.post("/login-form") 
async def login_form(forms_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pick_session)):
    user = authenticate_user(forms_data.username, forms_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }    
    
@auth_router.get("/refresh")  
async def use_refresh_token(user: User = Depends(verificate_token)):  
    access_token = create_token(user.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
