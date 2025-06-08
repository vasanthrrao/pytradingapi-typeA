from model.user_handler import UserHandler
from model.myorder_handler import MyOrderHandler
from model.order_handler import OrderHandler

#from model.option_handler import OptionHandler
#from model.market_handler import MarketHandler

user_handler = UserHandler()
my_order_handler = MyOrderHandler()
order_handler = OrderHandler()

#option_handler = OptionHandler()
#market_handler = MarketHandler()

# option_handler.get_option_chain()
#user_handler.get_fund_summary()
#user_handler.get_portfolio()
#market_handler.get_GainLoss()
#user_handler.get_position()
#my_order_handler.get_order_book()
#my_order_handler.get_order_history()
# Placing a new order
#order_handler.place_order()
order_handler.modify_order_with_stoploss()

