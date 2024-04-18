import csv
import json
import sqlite3
from flask import Flask
from flask import url_for
from flask import render_template, send_from_directory

app = Flask(__name__)

con = sqlite3.connect("pizza.db", check_same_thread=False)
cur = con.cursor()

@app.route('/')
def t():
	return send_from_directory('static', 'catalogue.html')
#	return render_template("index.html")
#    res = {}
#    for elem in result:
#        if not elem[5] in res:
#            res[elem[5]] = []
#        res[elem[5]].append([elem[3], elem[2]])
#
#    return json.dumps(res)

@app.route('/api/orders')
def t1():
	result = cur.execute("""select * from orders""").fetchall()
	res = []
	for e in result:
		res.append([e[0], e[1], e[2], e[3]])
	return json.dumps(res)


@app.route('/api/pizzas')
def t2():
	result = cur.execute("""select * from pizza""").fetchall()
	res = []
	for e in result:
		res.append({"p": e[0], 'price': e[1]})
	return json.dumps(res)


if __name__ == '__main__':
	app.run(port=5000, host='127.0.0.1')
	con.close()
