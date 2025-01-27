#!/usr/bin/env python
# coding: utf-8


def foo(bar, buz):
    if bar > buz:
        bar += buz
    else:
        buz *= bar

    return bar + buz

foo(3, 4)
foo(5, 4)



#!/usr/bin/env python
# coding: utf-8

from flask import Flask

app = Flask(__name__) # 'hello'

@app.route("/<name>")
def hello(name):
    return f"""<!DOCTYPE html>
<html>
    <body>
        <p>hello world, <b>{name}</b></p>
    </body>
</html>"""



#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template

app = Flask(__name__) # 'hello'

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("index.html", name=name)
