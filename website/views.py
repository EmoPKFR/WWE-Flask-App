import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user
from .models import Order
from .auth import admin_required

views = Blueprint("views", __name__)

@views.route("/admin_dashboard")
def admin_dashboard():
    if current_user.is_authenticated and current_user.role == 'admin':
        return render_template('admin_dashboard.html', user=current_user)
    else:
        return render_template("auth/catch_all_routes.html")

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/shop")
def shop():
    return render_template("shop_info/shop.html", user=current_user)

@views.route("/t_shirts")
def t_shirts():
    return render_template("shop_info/t_shirts.html", user=current_user)

@views.route("/titles")
def titles():
    return render_template("shop_info/titles.html", user=current_user)

cart = {}

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
        if product_title in cart:
            cart[product_title]['total_price'] += price * quantity
            cart[product_title]['quantity'] += quantity
        else:
            cart[product_title] = {
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
        if product_title in cart:
            cart[product_title]['total_price'] += price * quantity
            cart[product_title]['quantity'] += quantity
        else:
            cart[product_title] = {
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
        if product_title in cart:
            cart[product_title]['total_price'] += price * quantity
            # cart[product_title]['product_size'] = product_size
            cart[product_title]['quantity'] += quantity
        else:
            cart[product_title] = {
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
    global cart  # Declare 'cart' as a global variable
    
    if not (current_user.card_number and current_user.expiry_date and current_user.cvv):
        flash("Please Add Payment Card before making a purchase.", category="warning")
        return redirect(url_for("auth.profile_page"))  # Redirect to the profile page to update payment info
    
    total_amount = 0
    all_products = {}  # Initialize an empty dictionary
    total_product_price = 0  # Initialize a variable to track the total product price

    if request.method == "POST":
        shipping_address = request.form.get('shipping_address')
        if len(shipping_address) < 3:
            flash("Shipping address must have 3 or more symbols", category="error")
        else:
            product_title = request.form.get('product_title')
            
            product_titles = []  # Initialize a list to store formatted product details

            for product_title, details in cart.items():
                # Format the product details
                product_detail = f"{product_title}, price={details['product_price']}, quantity={details['quantity']}"
                product_titles.append(product_detail)
                
            # Convert the list of formatted product details to a JSON string
            products_str = json.dumps(product_titles)
            
            # Populate the all_products dictionary from the cart
            for product_title, data in cart.items():
                all_products[product_title] = data

            # Convert the dictionary to a JSON string
            all_products_str = json.dumps(all_products)
            
            # Populate the product_titles list from the cart
            product_titles = list(cart.keys())
            
            
            # Calculate the total product price
            for product_title, data in all_products.items():
                total_product_price += data['product_price'] * data['quantity']

            if total_product_price >= 500:
                total_product_price *= 0.9      
            
            session["products"] = products_str
            session["total_price"] = total_product_price
            session["shipping_address"] = shipping_address
            session['cart'] = cart
            session['total_product_price'] = total_product_price
            
            # Clear the cart by reassigning it as an empty dictionary
            cart = {}
            return redirect(url_for("emails.send_email_order"))

    for product_title, details in cart.items():
        total_amount += details['total_price']
    
    #Format the total amount to the second digit after the decimal point
    total_amount = round(total_amount, 2)
    formatted_total_amount_str = "{:.2f}".format(total_amount)
    total_amount_with_discount = round(total_amount * 0.9, 2)
    formatted_total_amount_with_discount = "{:.2f}".format(total_amount_with_discount)
    
    return render_template("shop_info/basket.html", user=current_user, cart=cart, 
                        total_amount=total_amount, 
                        formatted_total_amount_str=formatted_total_amount_str,
                        total_amount_with_discount=total_amount_with_discount,
                        formatted_total_amount_with_discount=formatted_total_amount_with_discount)

@views.route('/remove_product', methods=['POST'])
def remove_product():
    if request.method == 'POST':
        product_title_to_remove = request.form.get('product_title')

        if product_title_to_remove in cart:
            del cart[product_title_to_remove]

    return redirect(url_for('views.basket'))

@views.route('/orders_history')
@login_required
def orders_history():
    user_orders = Order.query.filter_by(username=current_user.username).all()
    orders = Order.query.all()

    return render_template("orders_history.html", user=current_user, user_orders=user_orders, orders=orders)