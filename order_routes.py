from fastapi import APIRouter, Depends, HTTPException
from models import User, Order, OrderItem
from dependencies import pick_session
from main import bcrypt_context
from schemas import UserSchema, OrderSchema, ItemSchema
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

@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(pick_session), user: User = Depends(verificate_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Access denied: you are not authorized to make this change")
    order.status = "CANCELLED"
    session.commit() #salvar as alterações 
    session.refresh(order) #atualiza o db
    return {
        "message": f"Order #{id_order}: Successfully Cancelled!",
        "order": f"{order}"
    }

@order_router.get("/list")
async def list_orders(session: Session = Depends(pick_session), user: User = Depends(verificate_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Access denied: you are not authorized to make this operation")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }

@order_router.post("/order/add-item/{id_order}")
async def add_item_in_order(id_order: int, item_schema: ItemSchema, session: Session = Depends(pick_session), user: User = Depends(verificate_token)):
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="Access denied: you are not authorized to make this change")
    item_order = OrderItem(item_schema.flavor, item_schema.amount, item_schema.size, item_schema.description, item_schema.unit_price, id_order)
    session.add(item_order)
    order.calculate_price()
    session.commit()
    return {
        "message": "Item created successfully",
        "id_item": item_order.id,
        "order_price": order.total_price
    }