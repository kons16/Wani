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
                "path": split_by_slash(path),
                # "path_compiled": re.compile(path),
                "callback": callback
            })

    def match(self, method, path):
        error_callback = http404
        get_path = split_by_slash(path)

        for route in self.routes:
            url_vars = {}
            if len(route["path"]) == len(get_path):
                for r, gp in zip(route["path"], get_path):
                    if r != gp and r not in "{":
                        # r  ['user', 'name']
                        # gp ['user', 'tom']
                        break
                    elif r != gp and r in "{":
                        # r  ['user', '{name}']
                        # gp ['user', 'tom']
                        url_vars = gp

                    error_callback = http405
                    if method == route["method"]:
                        return route["callback"], url_vars
                else:
                    continue

        return error_callback, {}
