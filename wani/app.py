from .routes import Router
from .requests import Request
from .responses import TemplateResponse, Response
import os
from jinja2 import Environment, FileSystemLoader


class Wani:
    def __init__(self, templates=None):
        self.router = Router()
        if templates is None:
            templates = [os.path.join(os.path.abspath("."), "templates")]
        self.jinja2_environment = Environment(loader=FileSystemLoader(templates))

    def run(self, host=None, port=None, **options):
        """ ローカルの開発用サーバーにアプリを立ち上げる

        :param host: listenするホストネーム。デフォルトは `'127.0.0.1'``
        :param port: Webサーバーのポート番号。デフォルトは ``5000``
        :param options: Werkzeug serverで使うためのオプション. 詳しくは `werkzeug.serving.run_simple`
        """
        if not host:
            host = "127.0.0.1"

        if port or port == 0:
            port = int(port)
        else:
            port = 5000

        from werkzeug.serving import run_simple

        try:
            run_simple(host, port, self, **options)
        except Exception as e:
            print(e)

    def route(self, path=None, method="GET", callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        request = Request(env)
        callback, url_vars = self.router.match(request.method, request.path)

        if request.path != "/favicon.ico":
            response = callback(request, **url_vars)
        else:
            response = Response(status=404)

        start_response(response.status_code, response.header_list)

        if isinstance(response, TemplateResponse):
            return [response.render_body(self.jinja2_environment)]
        return response.body
