import json
import cgi
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ, charset="utf-8"):
        self.environ = environ
        self._body = None
        self.charset = charset

    @property
    def path(self):
        return self.environ["PATH_INFO"] or "/"

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"].upper()

    @property
    def forms(self):
        form = cgi.FieldStorage(
            fp=self.environ["wsgi.input"],
            environ=self.environ,
            keep_blank_values=True,
        )
        params = {k: form[k].value for k in form}
        return params

    @property
    def query(self):
        get_param = parse_qs(self.environ["QUERY_STRING"])

        return parse_qs(self.environ["QUERY_STRING"])

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get("CONTENT_LENGTH", 0))
            self._body = self.environ["wsgi.input"].read(content_length)
        return self._body

    @property
    def text(self):
        return self.body.decode(self.charset)

    @property
    def json(self):
        return json.loads(self.body)

