import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.wishList import wishList
from controller.AuthenticationHandlers import SigninBaseHandler

class WishListsHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None: messages.append(_message)

        results = []

        _word = self.get_argument("word", None)
        if _word is not None:
            results = wishList.search(_id,_word)
        else:
            # ユーザーごとの現金出納帳データを取得
           results = wishList.select_by_user_id(_signedInUser.attr["id"])

        self.render("wishLists.html", user=_signedInUser, wishLists=results, messages=messages, errors=[])

        """# 概要を取得
        _name = self.get_argument("name", None)
        _kind = self.get_argument("kind", None)

        # ユーザーごとの現金出納帳データを取得
        if _name is not None:
            results = wishList.name(_id,_name)

        if _kind is not None:
            results = wishList.kind(_id,_kind)
        else:
            results = wishList.select_by_user_id(_signedInUser.attr["id"])
        self.render("search.html",
            user=_signedInUser,
            search=results,
            messages=messages,
            name=_name,
            kind=_kind,
            errors=[])"""

class WishShowHandler(SigninBaseHandler):
    def get(self, id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        w = wishList.find(id)
        if w is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        if w.attr["user_id"] != _signedInUser.attr["id"]: raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        self.render("wishList_form.html", user=_signedInUser, mode="edit", wishList=w, messages=[], errors=[])

    def post(self,id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_name = self.get_argument("form-name", None)
        p_quantity = self.get_argument("form-quantity",None)
        p_kind = self.get_argument("form-kind", None)


        # 現金出納帳データの組み立て
        w = wishList.build()
        w.attr["user_id"] = int(_id) # ユーザーIDはサインインユーザーより取得
        w.attr["id"] = id
        errors = []
        if p_name is None: errors.append("品名は必須です。")
        w.attr["name"] = p_name

        w.attr["kind"] = p_kind

        w.attr["quantity"] = p_quantity
        #il.attr["last_updated"] = p_last_updated

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=[])
            return

        # 登録
        # print(vars(w))
        w_id = w.save()
        if w_id == False:
            self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/wishlist?message=%s" % tornado.escape.url_escape("変更を完了しました。(ID:%s)" % w_id))

class WishCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        w = wishList.build()
        self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_name = self.get_argument("form-name", None)
        p_quantity = self.get_argument("form-quantity", None)
        p_kind = self.get_argument("form-kind", None)
        #p_last_updated = self.get_argument("form-last_updated", None)

        # 現金出納帳データの組み立て
        w = wishList.build()
        w.attr["user_id"] = int(_id) # ユーザーIDはサインインユーザーより取得

        errors = []
        if p_name is None: errors.append("品名は必須です。")
        w.attr["name"] = p_name

        w.attr["quantity"] = p_quantity

        w.attr["kind"] = p_kind

        #w.attr["last_updated"] = p_last_updated

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=[])
            return

        # 登録
        # print(vars(w))
        w_id = w.save()
        if w_id == False:
            self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/wishlist?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % w_id))

class WishDeleteHandler(SigninBaseHandler):
    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_id = self.get_argument("wishlist_id", None)

        w = wishList.find(p_id)

        w.delete()

        self.redirect("/wishlist")

        # w_id = wishList.delete(p_id)
        # if w_id == False:
        #     self.render("wishList_form.html", user=_signedInUser, mode="new", wishList=w, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        # else:
        #     # 登録画面へリダイレクト(登録完了の旨を添えて)
        #     self.redirect("/wishlist?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % w_id))
