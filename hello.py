from wani.app import Wani
from wsgiref.simple_server import make_server


app = Wani()


@app.route('^/$', 'GET')
def hello(request, start_response):
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'Hello World']


if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    httpd.serve_forever()
