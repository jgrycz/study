from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-agent')
    return "Twoja przeglądarka to {}".format(user_agent)

@app.route('/user/<name>')
def name(name):
    # import ipdb; ipdb.set_trace()
    return "SIema {}".format(name)

@app.route('/incorrect_req')
def incorrect_req():
    # import ipdb; ipdb.set_trace()
    return "Nieprawidlowe żądanie!", 400

@app.route('/cookie')
def cookie():
    resp = make_response("hehe dostaleś też cookiesa")
    resp.set_cookie('hehe', '100')
    return resp

@app.route('/abort/<user>')
def my_abort(user):
    if user == 'jarek':
        abort(404)
    return "SIema {}".format(user)

@app.route('/redirect')
def my_redirect():
    return redirect('https://google.com')


# app.add_url_rule('/', 'index', index)
