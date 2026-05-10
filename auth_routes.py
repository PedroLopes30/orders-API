from fastapi import APIRouter, Depends, HTTPException
from models import User, Order, OrderItem
from dependencies import pick_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from dependencies import pick_session
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id_user):
    token = f"knsvsuibvrjngfoafn{id_user}"
    return token

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
    user = session.query(User).filter(User.email==login_schema.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    else:
        acess_token = create_token(user.id)
    
