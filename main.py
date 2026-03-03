from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello, World!"

products = [
    Product(id=1,name="Phone",description="Apple Phone",price=999.99,quantity=10),
    Product(id=2,name="Laptop",description="Dell Laptop",price=1499.99,quantity=5),
    Product(id=3,name="Headphones",description="Sony Headphones",price=199.99,quantity=20),
    Product(id=4,name="Smartwatch",description="Samsung Smartwatch",price=299.99,quantity=15)
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()

    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    #db=session()
    #db.query()
    db_products=db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    '''from list Products
    for product in products:
        if product.id==id:
            return products[id-1]
    return "Product not found"'''
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not Found"

@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    '''for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "Product Updated Succesfully"'''
    
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product Updated Successfully"
    else:
        return "Product not found"

@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    '''for i in range(len(products)):
        if products[i].id==id:
            del products[i]
            return "Product Deleted"'''
    db_product=db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"