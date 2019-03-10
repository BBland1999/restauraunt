from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, SubmitOrder
from flask_login import current_user, login_user, logout_user
from app.models import My_User, Item, My_Order, My_Order2
from app import db
from datetime import datetime

# item = Item(None, "Cheese Cake", 'Appetizer', "Desc", "cheesecake.jpg")
# db.session.add(item)
# db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    menu = Item.query.all()
    return render_template('index.html', menuItems=menu)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))

    form = LoginForm()
    if form.validate_on_submit():
        # print(form.password.data)
        # print(form.username.data)
        #return redirect('/')
        user = My_User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #user login failed or username / password invalid
            return redirect(url_for('login'))
        else:
            print('success')
            login_user(user)
            return redirect(url_for('index'))

    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = My_User(None, form.username.data, form.phone.data, form.fname.data, form.lname.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/order', methods=['POST', 'GET'])
def order():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    else:
        order = My_Order.query.filter_by(user_id=current_user.id).first()
        if order is None:
            return redirect(url_for('index'))
        elif order.submit is not None:
            return redirect(url_for('index'))

        form = SubmitOrder()
        if form.validate_on_submit():
            query = "UPDATE my_order SET submit=NOW() WHERE user_id=" + str(current_user.id) + ";"
            db.engine.execute(query)

        string = "SELECT item.name FROM (SELECT my_order2.food_id FROM (SELECT * FROM my_order WHERE user_id ="+ str(current_user.id) +") A INNER JOIN my_order2 ON A.order_id = my_order2.order_id) B INNER JOIN item ON item.food_id = B.food_id;"
        result = db.engine.execute(string)
        d, order_items = {}, []
        for rowproxy in result:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for tup in rowproxy.items():
                # build up the dictionary
                d = {**d, **{tup[0]: tup[1]}}
            order_items.append(d)

        return render_template('order.html', form=form, order_items=order_items)

@app.route('/orderHandler', methods=['POST'])
def orderHandler():
    if current_user.is_authenticated:
        uid = current_user.id
        food_id = request.form['food_id']
        order = My_Order.query.filter_by(user_id=uid).first()
        if order is None:
            try:
                user_order = My_Order(None, uid, None, None)
                db.session.add(user_order)
                db.session.commit()
            except:
                return jsonify(["Error", "Error"])

            try:
                order2 = My_Order.query.filter_by(user_id=uid).first()
                if order2.submit is not None:
                    return jsonify(["Error", "Order already Submitted"])

                user_item = My_Order2(order2.order_id, food_id, None)
                db.session.add(user_item)
                db.session.commit()
                return jsonify(["Success", "Created new order and successfully added item to order"])
            except:
                return jsonify(["Error", "Error"])

        else:
            try:
                if order.submit is not None:
                    return jsonify(["Error", "Order already Submitted"])

                user_item = My_Order2(order.order_id, food_id, None)
                db.session.add(user_item)
                db.session.commit()
                return jsonify(["Success", "Successfully added item to order"])
            except:
                return jsonify(["Error", "Error"])
    else:
        return jsonify(["Error", "You must login to order"])