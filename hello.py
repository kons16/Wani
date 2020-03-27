from wani.app import Wani
from wani.responses import Response
from wsgiref.simple_server import make_server
from wani.responses import TemplateResponse

app = Wani()


@app.route("^/$", "GET")
def hello(request):
    return Response("Hello World")


@app.route("^/user/(?P<name>\w+)/$", "GET")
def user_detail(request, name):
    return Response("Hello {name}".format(name=name))


@app.route('^/user/$', 'GET')
def users(request):
    users = ['user%s' % i for i in range(10)]
    return TemplateResponse('users.html', title='User List', users=users)


if __name__ == "__main__":
    httpd = make_server("", 8000, app)
    httpd.serve_forever()
