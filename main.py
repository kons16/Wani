from wani import Wani, Response, TemplateResponse, WactiveRecord, Auth
import os

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]

app = Wani()


@app.route("/", ["GET"])
def hello(request):
    u = WactiveRecord("users")
    all_users = u.all()
    # all_usersの一番目のレコードを表示
    return Response("Hello, {}".format(all_users[0]["name"]))


@app.route("/user/{name}", ["GET"])
def user_detail(request, name):
    """ {name}をテーブルに保存 """
    u = WactiveRecord("users")
    u.create([name, "a@a.com", "pass"])
    return Response("Hello {name}".format(name=name))


@app.route("/find_user/{id}", ["GET"])
def find_user(request, id):
    """ usersテーブルの{id}レコードを見つける"""
    u = WactiveRecord("users")
    record = u.find(id)
    return Response("{}".format(record.data))


@app.route("/find_by", ["GET"])
def find_by(request):
    """ usersテーブルの指定されたnameレコードを見つける """
    u = WactiveRecord("users")
    record = u.find_by(id=1)
    return Response("{}".format(record.data[0]["name"]))


@app.route("/where", ["GET"])
def where(request):
    """ where句で指定されたレコードを表示 """
    u = WactiveRecord("users")
    # idが3以上のレコードを全件取得
    all_record = u.where("name == tom")
    return Response("{}".format(all_record))


@app.route("/change_user/{id}", ["GET"])
def change_user(request, id):
    """ usersテーブルの{id}レコードを見つけて名前をyayに変更 """
    u = WactiveRecord("users")
    record = u.find(id)
    record.update(name="yay")
    return Response("{}".format(record.data))


@app.route("/data", method=["GET", "POST"])
def get_data(request):
    if request.method == "GET":
        return TemplateResponse("data-form.html")
    else:
        return Response("{}".format(request.forms["num"]))


@app.route("/create", ["GET"])
def create(request):
    """ ユーザーを登録する """
    data = {}
    data.setdefault("name", "ks")
    data.setdefault("email", "test@test.com")
    data.setdefault("password", "password")

    auth = Auth("users")
    auth.create_user(data)

    return TemplateResponse("users.html")


@app.route("/login", ["GET"])
def login(request):
    data = {}
    data.setdefault("email", "test@test.com")
    data.setdefault("password", "password")

    auth = Auth("users")
    auth.session_create(email="test@test.com", password="password")

    return TemplateResponse("users.html")


@app.route("/user", ["GET"])
def users(request):
    users = ["user%s" % i for i in range(10)]
    return TemplateResponse("users.html", title="User List", users=users)


if __name__ == "__main__":
    app.run()
