from wani import Wani, Response, TemplateResponse
from wsgiref.simple_server import make_server
from wsgi_static_middleware import StaticMiddleware
import os

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]

app = Wani()


@app.route("/", ["GET"])
def hello(request):
    return Response("Hello World, {}".format(request.query["name"]))


@app.route("/user/{name}", ["GET"])
def user_detail(request, name):
    return Response("Hello {name}".format(name=name))


@app.route("/data", method=["GET", "POST"])
def get_data(request):
    if request.method == "GET":
        return TemplateResponse("data-form.html")
    else:
        return Response("{}".format(request.forms["num"]))


@app.route("/user", ["GET"])
def users(request):
    users = ["user%s" % i for i in range(10)]
    return TemplateResponse("users.html", title="User List", users=users)


if __name__ == "__main__":
    app = StaticMiddleware(app, static_root='static', static_dirs=STATIC_DIRS)
    httpd = make_server("", 8000, app)
    httpd.serve_forever()
