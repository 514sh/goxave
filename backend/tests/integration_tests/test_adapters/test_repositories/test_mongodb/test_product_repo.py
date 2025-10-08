def test_add_new_product(product_repository, product):
    product_repository.add(product)
    added_product = product_repository.get(product)

    assert added_product.url == product.url


def test_product_doesnt_exist(product_repository, product):
    added_product = product_repository.get(product)
    assert added_product is None
