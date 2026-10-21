from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()


class ProductIn(BaseModel):
    name: str
    price: float
    supplier_cost: float            # internal: what we pay, must never reach customers


class ProductOut(BaseModel):
    id: int
    name: str
    price: float


products = []                       # in-memory storage (wiped on every reload)

COUNTER = 0

@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductIn):
    global COUNTER
    COUNTER += 1
    record = {"id": COUNTER, **product.model_dump()}
    products.append(record)
    return record


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):

    for record in products:
        if record["id"] == product_id:
            return record
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):

    for record in products:
        if record["id"] == product_id:
            products.remove(record)
            return
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/products/{product_id}", response_model=ProductOut, status_code=200)
def put_product(product: ProductIn, product_id: int):
    new_record = {"id": product_id, **product.model_dump()}

    for record in products:
        if record["id"] == product_id:
            record.update(new_record)
            return record
    raise HTTPException(status_code=418, detail="Item not found")