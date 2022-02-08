from config import app
from log.helpper import logger
from route.user_route import user_bp
from route.cart_bp import cart_bp
from route.cart_item_bp import cart_item_bp


app.register_blueprint(user_bp, url_prefix='/shoppingcart/user')
app.register_blueprint(cart_bp, url_prefix='/shoppingcart/cart')
app.register_blueprint(cart_item_bp, url_prefix='/shoppingcart/cart_item')

if __name__== '__main__':
    try:
        app.debug = True
        app.run()
        logger.info('app start')
    except Exception as e:
        logger.error(e)