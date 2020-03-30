"""
ルーティング周りの設定
"""


def http404(env, start_response):
    start_response("404 Not Found", [("Content-type", "text/plain; charset=utf-8")])
    return [b"404 Not Found"]


def http405(env, start_response):
    start_response("405 Method Not Allowed", [("Content-type", "text/plain; charset=utf-8")])
    return [b"405 Method Not Allowed"]


def split_by_slash(path):
    stripped_path = path.lstrip("/").rstrip("/")
    return stripped_path.split("/")


def delete_curly_braces(curly_braces):
    return curly_braces.lstrip("{").rstrip("}")


def match_path(rule, path):
    split_rule = split_by_slash(rule)
    split_path = split_by_slash(path)
    url_vars = {}

    if len(split_rule) != len(split_path):
        return False, {}

    for r, p in zip(split_rule, split_path):
        if r.startswith('{') and r.endswith('}'):
            url_vars[r[1:-1]] = p
            continue
        if r != p:
            return False, {}
    return True, url_vars


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
        match_flag = False
        error_callback = http404
        get_path = split_by_slash(path)

        for route in self.routes:
            url_vars = {}
            if len(route["path"]) == len(get_path):
                for r, gp in zip(route["path"], get_path):
                    if r != gp and r.startswith("{") is False:
                        match_flag = False
                        break

                    if r == gp:
                        match_flag = True
                    elif r != gp and r.startswith("{") and r.endswith("}"):
                        url_vars[delete_curly_braces(r)] = gp
                else:
                    if method == route["method"] and match_flag:
                        match_flag = False
                        return route["callback"], url_vars

        return error_callback, {}
