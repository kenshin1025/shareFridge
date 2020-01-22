import tornado.web
from model.user import user
from model.wishList import wishList
from model.innerList import innerList
from controller.AuthenticationHandlers import SigninBaseHandler

class moveHandler(SigninBaseHandler):
    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_id = self.get_argument("wishlist_id", None)

        w = wishList.move(p_id)

        il = innerList.build()

        il.attr["user_id"] = w.attr["user_id"] # ユーザーIDはサインインユーザーより取得

        il.attr["product_name"] = w.attr["name"]

        il.attr["kind"] = w.attr["kind"]

        il.attr["amount"] = w.attr["quantity"]

        il.attr["whose"] = ""
        il.attr["lim"] = ""

        il.save()

        self.redirect("/wishlist")