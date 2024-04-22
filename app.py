import csv
import json
import sqlite3
from flask import Flask
from flask import url_for
from flask import render_template, send_from_directory
from flask import request
from flask import redirect
from flask_simplelogin import SimpleLogin, get_username, login_required

my_users = {
    "admin": {"password": "admin", "roles": ["admin"]},
}

def check_my_users(user):
    user_data = my_users.get(user["username"])
    if not user_data:
        return False 
    elif user_data.get("password") == user["password"]:
        return True  
    return False  

app = Flask(__name__)

simple_login = SimpleLogin(app, login_checker=check_my_users)


con = sqlite3.connect("pizza.db", check_same_thread=False)
cur = con.cursor()

## PAGE

@app.route('/')
def t_root():
	return send_from_directory('static', 'catalogue.html')


@app.route('/clientOrder/<int:orderId>')
def clientOrder(orderId):
	result = cur.execute("""select orderId, clientName, clientPhone, clientAddress, orderStatus from orders where orderId=?""", (orderId,)).fetchall()
	e = result[0]
	return render_template('clientOrder.html', orderId=orderId, clientName=e[1], clientPhone=e[2], clientAddress=e[3], orderStatus=e[4])


@app.route('/orders')
@login_required(username=["admin"])
def t_orders():
	return render_template('orders.html')

@app.route('/login')
def mylogin():
	return render_template('login.html')



## API

@app.route('/api/orders')
@login_required(username=["admin"])
def t1():
	result = cur.execute("""select orderId, clientName, clientPhone, clientAddress, orderStatus from orders""").fetchall()
	res = []
	for e in result:
		orderId = int(e[0])
		items = cur.execute("""select pizzaName from orderItems where orderId=?""", (orderId,)).fetchall()
		pizzaList = []
		for i in items:	
			pizzaList.append({"pizzaName": i[0]})

		res.append({"orderId": e[0], "clientName": e[1], "clientPhone": e[2], "clientAddress": e[3], "orderStatus": e[4], "pizzas": pizzaList})

	return json.dumps(res)


@app.route('/api/pizzas')
def t2():
	result = cur.execute("""select * from pizza""").fetchall()
	res = []
	for e in result:
		res.append({"p": e[0], 'price': e[1]})
	return json.dumps(res)


@app.route('/api/postOrder', methods=['GET', 'POST'])
def t3():
	clientName = request.form['clientName']
	clientPhone = request.form['clientPhone']
	clientAddress = request.form['clientAddress']

	cur.execute("""insert into orders (clientName, clientPhone, clientAddress, orderStatus) 
				values (?, ?, ?, ?) 
			""", (clientName, clientPhone, clientAddress, "NEW")).fetchall()
	orderId = cur.lastrowid

	pizzaList = json.loads(request.form['pizzas'])
	for p in pizzaList:
		cur.execute("""insert into orderItems (orderId, pizzaName) 
				values (?, ?)
		    """, (orderId, p['p'])).fetchall()
	con.commit()

	return redirect(url_for('clientOrder', orderId=orderId))


@app.route('/api/postOrderStatus', methods=['GET', 'POST'])                                       
def t4():
	orderId = request.form['orderId']
	orderStatus = request.form['orderStatus']

	cur.execute("""update orders set orderStatus=? where orderId=?""", (orderStatus, orderId)).fetchall()
	con.commit()

	return redirect("/orders")


if __name__ == '__main__':
	app.run(port=5000, host='127.0.0.1')
	con.close()
