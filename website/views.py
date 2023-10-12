from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Order
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/all_superstars")
def all_superstars():
    return render_template("superstars_info/all_superstars.html", user=current_user)

@views.route("/champions")
def champions():
    return render_template("superstars_info/champions.html", user=current_user)

@views.route("/shows")
def shows():
    return render_template("shows.html", user=current_user)

@views.route("/shop")
def shop():
    return render_template("shop_info/shop.html", user=current_user)


@views.route("/t_shirts")
def t_shirts():
    return render_template("shop_info/t_shirts.html", user=current_user)

# @views.route("/titles_old", methods=["GET", "POST"])
# def titles_old():
#     if request.method == "POST":
#         return redirect(url_for("views.titles_info", title_picture="WWE_World_Heavyweight_Championship_title.png"))
    
    
#     return render_template("shop_info/titles_old.html", user=current_user)

@views.route("/titles")
def titles():
    return render_template("shop_info/titles.html", user=current_user)


@views.route("/title_info", methods=["GET", "POST"])
def title_info():
    if request.method == "POST":
        #Get the selected img, name, price, size and quantity from the form
        img = request.form.get("img")
        product_title = request.form.get("product_title")
        product_price = request.form.get("product_price")
        # product_size = request.form.get("product_size")
        quantity = int(request.form.get('quantity_input'))

        price = int(''.join(filter(str.isdigit, product_price)))

        # Update the shopping cart with the selected product
        if product_title in shopping_cart:
            shopping_cart[product_title]['total_price'] += price * quantity
            shopping_cart[product_title]['quantity'] += quantity
        else:
            shopping_cart[product_title] = {
                'product_price': price,
                'total_price': price * quantity,
                'quantity': quantity,
                # 'product_size': product_size,
                'img': img
                }
        return redirect(url_for("views.basket"))
    
    img = request.args.get("img")
    product_name = request.args.get("product_name")
    price = request.args.get("price")
    
    return render_template("shop_info/title_info.html", user=current_user, img=img, product_name=product_name, price=price)

@views.route("/toys")
def toys():
    return render_template("shop_info/toys.html", user=current_user)

@views.route("/toy_info", methods=["GET", "POST"])
def toy_info():
    if request.method == "POST":
        #Get the selected img, name, price, size and quantity from the form
        img = request.form.get("img")
        product_title = request.form.get("product_title")
        product_price = request.form.get("product_price")
        # product_size = request.form.get("product_size")
        quantity = int(request.form.get('quantity_input'))

        price = int(''.join(filter(str.isdigit, product_price)))

        # Update the shopping cart with the selected product
        if product_title in shopping_cart:
            shopping_cart[product_title]['total_price'] += price * quantity
            shopping_cart[product_title]['quantity'] += quantity
        else:
            shopping_cart[product_title] = {
                'product_price': price,
                'total_price': price * quantity,
                'quantity': quantity,
                # 'product_size': product_size, 
                'img': img
                }
        return redirect(url_for("views.basket"))
    
    img = request.args.get("img")
    product_name = request.args.get("product_name")
    price = request.args.get("price")
    
    return render_template("shop_info/toy_info.html", user=current_user, img=img, product_name=product_name, price=price)

# Initialize an empty shopping cart (a dictionary)
shopping_cart = {}

@views.route("/product_info", methods=["GET", "POST"])
def product_info():
    if request.method == "POST":
        #Get the selected img, name, price, size and quantity from the form
        img = request.form.get("img")
        product_title = request.form.get("product_title")
        product_price = request.form.get("product_price")
        # product_size = request.form.get("product_size")
        quantity = int(request.form.get('quantity_input'))

        price = int(''.join(filter(str.isdigit, product_price)))

        # Update the shopping cart with the selected product
        if product_title in shopping_cart:
            shopping_cart[product_title]['total_price'] += price * quantity
            # shopping_cart[product_title]['product_size'] = product_size
            shopping_cart[product_title]['quantity'] += quantity
        else:
            shopping_cart[product_title] = {
                'product_price': price,
                'total_price': price * quantity,
                # 'product_size': product_size, 
                'quantity': quantity,
                'img': img
                }
        return redirect(url_for("views.basket"))
    
    img = request.args.get("img")
    product_name = request.args.get("product_name")
    price = request.args.get("price")
    
    return render_template("shop_info/product_info.html", user=current_user, img=img, product_name=product_name, price=price)

@views.route("/basket", methods=["GET", "POST"])
@login_required
def basket():
    if request.method == "POST":
        shipping_address = request.form.get('shipping_address')
        if len(shipping_address) < 20:
            flash("Shipping address must have 20 or more symbols", category="error")
        else:
            product_title = request.form.get('product_title')
            # price = request.form.get('price')
            # quantity = request.form.get('quantity')
            
            new_order = Order(name="Emo", price=2, shipping_address=shipping_address)
            db.session.add(new_order)
            db.session.commit()
            
            flash("You successfully buyed your order", category="success")
            return redirect(url_for("views.home"))
    
    total_amount = 0
    
    for product_title, details in shopping_cart.items():
        total_amount += details['total_price']
        first_key, first_value = list(shopping_cart.items())[0]
        
    return render_template("shop_info/basket.html", user=current_user, shopping_cart=shopping_cart, total_amount=total_amount)

@views.route('/remove_product', methods=['POST'])
def remove_product():
    if request.method == 'POST':
        product_title_to_remove = request.form.get('product_title')

        if product_title_to_remove in shopping_cart:
            del shopping_cart[product_title_to_remove]

    return redirect(url_for('views.basket'))

