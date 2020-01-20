import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.fridge import fridge
from controller.AuthenticationHandlers import SigninBaseHandler

class fridgeCreateHandler(SigninBaseHandler):
    def post(self):
        