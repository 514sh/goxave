from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from config import get_mongo_db_client as db_instance
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from src.service_layer.message_bus import ping_pong, get_date_time
import asyncio
import uuid

app = FastAPI()

collections = db_instance()["test-goxave"]

class ProductDetails(BaseModel):
    price: float
    timestamp: str

class Product(BaseModel):
    url: str
    image_link: str = ""
    name: str = ""
    details: list[ProductDetails]


@app.post("/products")
async def save_url(product: Product):
    products = collections.products
    product_dict = product.model_dump()
    await products.insert_one(product_dict)
    html_content = ""
    
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False, slow_mo=50)
        browser = await p.chromium.launch()
        page = await browser.new_page()
        wait_until = "load"
        await page.goto(product_dict["url"], wait_until=wait_until, timeout=120000)
        html_content = await page.content()
        print(html_content)
        await browser.close()

    soup = BeautifulSoup(html_content, "html5lib")
    current_price = None
    product_name = ""
    image_link = ""
    price_tag = soup.find_all(class_="pdp-price_size_xl")
    item_name_tag = soup.find_all(class_= "pdp-mod-product-badge-title")
    preview_image = soup.find_all(class_="gallery-preview-panel__image")
    # print(type(price[0]))
    # discounted_price = price.find_all(id="pdpd-price_size_xl")
    for tag in price_tag:
        current_price = tag.string
    
    for tag in item_name_tag:
        tag_str = tag.string.replace("  ", "")
        tag_str = tag_str.replace("\n", " ")
        product_name = tag_str
    
    for tag in preview_image:
        image_link = tag.attrs["src"]

    return {
        "url": product_dict["url"],
        "name": product_name,
        "image_link": image_link,
        "details": [
            {
                "price": current_price,
                "timestamp": "",
            }
        ]
    }
    
async def ping_pong_generator():
    my_id = f"{uuid.uuid4()}"
    yield f"[{my_id}] ping {get_date_time()}\t"
    result = ping_pong.apply_async(task_id=my_id)
    i = 0
    while i < 20:
        if result.ready():
            yield result.get()
            break
        await asyncio.sleep(0.5)
        i += 1

@app.get("/products")
def get_my_products():
    products = collections.products
    my_saved_products = []
    for product in products.find({}):
        del product["_id"]
        my_saved_products.append(product)
    

    return [product for product in my_saved_products]

@app.get("/api/hello")
def hello():
    return "Hello"

@app.get("/api/ping")
async def get_ping_pong():
    return StreamingResponse(ping_pong_generator(), media_type="text/event-stream")