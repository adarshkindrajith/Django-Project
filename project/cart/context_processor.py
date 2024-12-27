from .cart import Cart

#creating context-processor so cart can work all pages
def cart(request):
    #set default data in to the cart
    return {'cart':Cart(request)}
