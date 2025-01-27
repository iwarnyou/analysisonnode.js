#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template

app = Flask(__name__) # 'hello'

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)
#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request

app = Flask(__name__) # 'hello'

@app.route("/hello") # localhost:5000/hello?name=zhangsan
def hello():
    name = request.args.get("name", "anonymous")
    return render_template("index.html", name=name)
