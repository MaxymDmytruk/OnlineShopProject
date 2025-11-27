class User:
    def __init__(self, id, email, role="buyer"):
        self.id = id
        self.email = email
        self.role = role


class Product:
    def __init__(self, id, name, description, price: float):
        self.id = id
        self.name = name
        self.description = description

        if price < 0:
            raise ValueError("Ціна не може бути негативною")
        self.price = price

    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Нова ціна не може бути негативною")
        self.price = new_price


class Order:
    def __init__(self, id, user: User, product: Product):
        self.id = id
        self.user_id = user.id
        self.product_id = product.id
        self.price_at_purchase = product.price