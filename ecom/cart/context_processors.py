from .cart import Cart

#create the processors so our cart can work on all the pages of the site
def cart(request):
    return {'cart':Cart(request)}