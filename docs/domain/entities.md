## Ключові Сутності (Entities)

### 1. Піддомен: Користувачі (Identity & Access)
* **User (Користувач)**
    * `id` (ідентифікатор)
    * `email` (пошта)
    * `password_hash` (хеш пароля)
    * `role` (роль: "buyer" або "admin")

### 2. Піддомен: Каталог (Catalog)
* **Product (Товар)**
    * `id` (ідентифікатор)
    * `name` (назва)
    * `description` (опис)
    * `price` (ціна)

### 3. Піддомен: Замовлення (Ordering)
* **Order (Замовлення)**
    * `id` (ідентифікатор)
    * `user_id` (ID покупця)
    * `product_id` (ID купленого товару)
    * `order_date` (дата покупки)