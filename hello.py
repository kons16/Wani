from wani.app import Wani
from wani.responses import  Response
from wsgiref.simple_server import make_server


app = Wani()


@app.route("^/$", "GET")
def hello(request):
    return Response("Hello World")


@app.route("^/user/(?P<name>\w+)/$", "GET")
def user_detail(request, name):
    return Response("Hello {name}".format(name=name))


if __name__ == "__main__":
    httpd = make_server("", 8000, app)
    httpd.serve_forever()
