from .routes import Router
from .requests import Request


class Wani:
    def __init__(self):
        self.router = Router()

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func

        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        request = Request(env)
        callback, kwargs = self.router.match(request.method, request.path)
        return callback(env, start_response, **kwargs)
