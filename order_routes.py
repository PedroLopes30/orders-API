from fastapi import APIRouter, Depends, HTTPException
from models import User, Order, OrderItem
from dependencies import pick_session
from main import bcrypt_context
from schemas import UserSchema, OrderSchema
from dependencies import pick_session, verificate_token
from sqlalchemy.orm import Session

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=())

@order_router.get("/")
async def orders():
    return {"message": "You have accessed the order route."}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(pick_session)):
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()  
    return {"message": f"Order placed successfully: #{new_order.id}"}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(pick_session), user: User = Depends(verificate_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Access denied: you are not authorized to make this change")
    order.status = "CANCELLED"
    session.commit() #salvar as alterações 
    session.refresh(order) #atualiza o db
    return {
        "message": f"Order #{order_id}: Successfully Cancelled!",
        "order": f"{order}"
    }

@order_router.get("list")
async def list_orders(session: Session = Depends(pick_session), user: User = Depends(verificate_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Access denied: you are not authorized to make this operation")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }