class Cart1:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'price': str(product.price),   # stored as string
                'quantity': quantity
            }
        else:
            self.cart[product_id]['quantity'] += quantity
        self.session.modified = True

    def remove(self, product_id):
        """Remove a product completely from cart"""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product_id, quantity):
        """Update quantity of a product"""
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                # If quantity is 0, remove the item
                self.remove(product_id)
            self.session.modified = True

    def total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())

    def total_price(self):
        from decimal import Decimal
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def __iter__(self):
        from decimal import Decimal
        for product_id, item in self.cart.items():
            subtotal = Decimal(item['price']) * item['quantity']
            yield {
                "id": product_id,
                "name": item['name'],
                "price": item['price'],
                "quantity": item['quantity'],
                "subtotal": str(subtotal)
            }

    def as_dict(self):
        return {
            "items": list(self.__iter__()),
            "total_quantity": self.total_quantity(),
            "total_price": str(self.total_price())
        }

    def get_items(self):
        """Return all items as a list of dictionaries"""
        return [
            {
                'id': product_id,
                'name': item['name'],
                'price': float(item['price']),
                'quantity': item['quantity'],
                'subtotal': float(item['price']) * item['quantity']
            }
            for product_id, item in self.cart.items()
        ]