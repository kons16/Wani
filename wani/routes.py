import re


def http404(env, start_response):
    start_response("404 Not Found", [("Content-type", "text/plain; charset=utf-8")])
    return [b"404 Not Found"]


def http405(env, start_response):
    start_response("405 Method Not Allowed", [("Content-type", "text/plain; charset=utf-8")])
    return [b"405 Method Not Allowed"]


def split_by_slash(path):
    stripped_path = path.lstrip('/').rstrip('/')
    return stripped_path.split('/')


class Router:
    def __init__(self):
        self.routes = []

    def add(self, method, path, callback):
        for m in method:
            self.routes.append({
                "method": m,
                "path": path,
                "path_compiled": re.compile(path),
                "callback": callback
            })

    def match(self, method, path):
        error_callback = http404
        for r in self.routes:
            matched = r["path_compiled"].match(path)
            if not matched:
                continue

            error_callback = http405
            print(matched.groupdict())
            url_vars = matched.groupdict()
            if method == r["method"]:
                return r["callback"], url_vars
        return error_callback, {}
