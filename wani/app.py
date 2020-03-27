from .routes import Router
from .requests import Request
from .responses import TemplateResponse
import os
from jinja2 import Environment, FileSystemLoader


class Wani:
    def __init__(self, templates=None):
        self.router = Router()
        if templates is None:
            templates = [os.path.join(os.path.abspath("."), "templates")]
        self.jinja2_environment = Environment(loader=FileSystemLoader(templates))

    def route(self, path=None, method="GET", callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        request = Request(env)
        callback, url_vars = self.router.match(request.method, request.path)

        response = callback(request, **url_vars)
        start_response(response.status_code, response.header_list)

        if isinstance(response, TemplateResponse):
            print("instanceです")
            return [response.render_body(self.jinja2_environment)]
        return [response.body]
