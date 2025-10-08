from typing import Annotated

from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse, RedirectResponse

from goxave.common import commands, message_bus, model, scraper, uow

router = APIRouter(prefix="/api")


def serialize(product: model.Product | None):
    if product is None:
        return None
    return {
        "_id": product.url_id,
        "url": product.url,
        "product_name": product.product_name,
        "product_price": product.product_price,
        "price_history": [
            {
                "price": hist.price,
                "timestamp": hist.timestamp,
            }
            for hist in product.price_history
        ],
        "product_image": {
            "src": product.product_image.src,
            "alt": product.product_image.alt,
        },
    }


@router.post("/products")
async def save_new_item(request: Request, url: Annotated[str, Body(embed=True)]):
    product_model = model.Product(url=url)
    scraper.do_scrape_web.delay(  # type: ignore
        url=url,
        user_id=request.headers.get("user_id", ""),
        user_name=request.headers.get("user_name", ""),
        discord_webhook=request.headers.get("discord_webhook", ""),
    )
    return RedirectResponse(
        url=f"/api/products/{product_model.url_id}?redirect=true", status_code=303
    )


@router.get("/products")
def get_my_products(request: Request):
    user_id = request.headers.get("user_id", "")
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"message": "You are not allowed to get this resources."},
        )
    user_model = model.User(id=user_id)

    handle_get_products = commands.GetMyProducts(user=user_model)
    is_successful = message_bus.handle(handle_get_products, uow)
    my_response = [None]
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]
    print(f"my response get products: {is_successful}")
    if my_response is None:
        return JSONResponse(
            status_code=500, content={"message": "Unable to fetch your products."}
        )
    return JSONResponse(
        status_code=200, content=[serialize(product) for product in my_response]
    )


@router.get("/products/{product_id}")
def get_one_product(request: Request, product_id, redirect=False) -> JSONResponse:
    product_model = model.Product(id=product_id)
    handle_get_one_saved_product = commands.GetOneSavedProduct(product=product_model)
    is_successful = message_bus.handle(handle_get_one_saved_product, uow)
    my_response = [None]
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]

    if my_response is None and redirect:
        return JSONResponse(
            status_code=307,
            content={
                "redirect": "/",
                "message": "We receive your request to add this product to your saved items. We will notify you once we finished evaluating your request.",
            },
        )
    elif my_response is None:
        return JSONResponse(
            status_code=404,
            content={"message": "This product doesn't exists in our database."},
        )

    return JSONResponse(status_code=200, content=my_response)


@router.delete("/products/{product_id}")
def remove_one_from_my_saved_products(request: Request, product_id):
    user_id = request.headers.get("user_id", "")
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"message": "You are not allowed to get this resources."},
        )
    user_model = model.User(id=user_id)

    handle_remove_one_saved_product = commands.RemovedOneSavedProduct(
        user=user_model, product_id=product_id
    )

    is_successful = message_bus.handle(handle_remove_one_saved_product, uow)
    my_response = [None]
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]

    if my_response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"{product_id} is already deleted."},
        )
    return JSONResponse(status_code=204, content=my_response)
