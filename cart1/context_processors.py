from pipenv.core import console
from .cart1 import Cart1

def cart(request):
        console.log(f"incp")
        return {'cart': Cart1(request)}