from sqlalchemy import create_engine, Column, Integer,  String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

#criando a conexão do banco
db = create_engine("sqlite:///banco.db")
#criando a base do banco de dados
Base = declarative_base()
# criar as classes/tabelas do banco

# Usuario
# Pedido
# ItensPedido

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)
    
    #será executada sempre que a criação de um usuario for realizada
    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"

    # ORDERS_STATUS = (
    #     ("PENDING", "PENDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("FINISHED", "FINISHED")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #Cancelado #Finalizado #Pendente
    user = Column("user", ForeignKey("users.id"))
    total_price = Column("price", Float)
   # items = 

    def __init__(self, user, status="PENDING", price=0):
       self.user = user
       self.price = price
       self.status = status 

class OrderItem(Base):
    __tablename__= "order_items"

    # ITEMS_SIZE = (
    #     ("P", "P"),
    #     ("M", "M"),
    #     ("G", "G"),
    #     ("GG", "GG")
    # ) 

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    flavor = Column("flavor", String, nullable=False)
    amount = Column("amount", Integer, nullable=False)
    size = Column("size", String)
    description = Column("description", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, flavor, amount, size, description, unit_price, order):
        self.flavor = flavor
        self.amount = amount
        self.size = size
        self.description = description
        self.unit_price = unit_price
        self.order = order