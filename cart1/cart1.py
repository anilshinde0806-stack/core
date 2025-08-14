from pipenv.core import console


class Cart1:
    def __init__(self,request):        # ✅ Create a session if it doesn't exist
        self.session= request.session
        cart = self.session.get('cart')

        console.log(f"in cart1 sessionKey:{self.session.get('cart')}")
        # Optional: Ensure empty cart exists
        if 'cart' not in request.session:
            cart = self.session ['cart'] = {}
        self.cart    = cart

        console.log(f"in cart1 sessionKey:{self.session.get('cart')}")