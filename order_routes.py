from fastapi import APIRouter, Depends, HTTPException
from models import User, Order, OrderItem
from dependencies import pick_session
from main import bcrypt_context
from schemas import UserSchema, OrderSchema
from dependencies import pick_session
from sqlalchemy.orm import Session

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    """
    Essa é a rota padrão de peidos do nosso sistema
    """
    return {"mensagem": "Você acessou a rota de pedidos."}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(pick_session)):
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()  
    return {"mensagem": f"pedido realizado com sucesso{new_order.id}"}
