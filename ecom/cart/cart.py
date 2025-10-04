from store.models import Product,Profile
class Cart():
    def __init__(self,request):
        self.session = request.session
        #get request
        self.request=request
        #get the current session key if it exists
        cart =self.session.get('session_key')
        #no session key
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}


        #making sure caart is available on all pages of the site
        self.cart=cart
    def db_add(self,product,quantity):
        product_id=str(product)
        product_qty=str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)
        self.session.modified = True
        #dealing with logged in user
        if self.request.user.is_authenticated:
            current_user=Profile.objects.filter(user_id=self.request.user.id)
            #convert the dict single quotes for json
            cartz=str(self.cart)
            cartz=cartz.replace("\'","\"")
            current_user.update(old_cart=str(cartz))
    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]=int(product_qty)
        self.session.modified = True
        #dealing with logged in user
        if self.request.user.is_authenticated:
            current_user=Profile.objects.filter(user_id=self.request.user.id)
            #convert the dict single quotes for json
            cartz=str(self.cart)
            cartz=cartz.replace("\'","\"")
            current_user.update(old_cart=str(cartz))

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids=self.cart.keys()
        #use ids to look up procucts in database
        products=Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities=self.cart
        return quantities

#we created this session based cart cuz  work for both anonymous and logged-in users.

    def update(self,product,quantity):
        product_id=str(product)
        product_qty=int(quantity)

        ourcart=self.cart
        #update cart dict
        ourcart[product_id]=product_qty

        self.session.modified=True

        thing=self.cart
        if self.request.user.is_authenticated:
            current_user=Profile.objects.filter(user_id=self.request.user.id)
            #convert the dict single quotes for json
            cartz=str(self.cart)
            cartz=cartz.replace("\'","\"")
            current_user.update(old_cart=str(cartz))
        return thing
    
    def delete(self,product):
        product_id=str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified=True

        if self.request.user.is_authenticated:
            current_user=Profile.objects.filter(user_id=self.request.user.id)
            #convert the dict single quotes for json
            cartz=str(self.cart)
            cartz=cartz.replace("\'","\"")
            current_user.update(old_cart=str(cartz))
    
    def cart_total(self):
        #get prod ids
        product_ids=self.cart.keys()
        #look up those keys in db
        products=Product.objects.filter(id__in=product_ids)
        quantities=self.cart
        total=0
        for key,value in quantities.items():
            #so the cart dictionary returns a key value pair right like{"prod_id":qty} so we covert it to like int for calc
            key=int(key)
            for product in products:
                if product.id==key:
                    if product.is_sale:
                        total=total+(product.sale_price * value)
                    else:
                        total=total+(product.price * value)
        return total

    