"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import customers
import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'c-this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    if not session.get('cart'): 
        flash("Your cart is empty, add something to it")
        return redirect("/melons")
    else:        
        cart_dict = session['cart']
        total_price = 0
        # {'cren' : 2, 'alib' : 3}
        list_of_melons = []
        for melon_key, melon_value in cart_dict.items():
            melon = melons.get_by_id(melon_key)
            melon.quantity = melon_value
            melon.total_price = melon.quantity * melon.price
            total_price += melon.total_price
            list_of_melons.append(melon)


        return render_template("cart.html", 
                                list_of_melons = list_of_melons,
                                total_price=total_price)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    if 'cart' not in session: 
        session['cart'] = {melon_id: 1}
    else: 
        if melon_id not in session['cart']: 
            session['cart'][melon_id] = 1
        else: 
            session['cart'][melon_id] = session['cart'][melon_id] + 1

    # if 'cart' not in session: 
    #     session['cart'] = {}

    # session['cart'][melon_id] = session['cart'].get(melon_id, 0) + 1

    print("session cart details: {}".format(session['cart']))
    print("session:{}".format(session))

    flash('Added to cart!')

    return redirect('http://localhost:5000/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    user_name = request.form.get("email")
    password = request.form.get("password")


    customer = customers.get_by_email(user_name)

    if not bool(customer): 
        flash("Customer does not exist")
        return redirect("/login")
    else: 
        if customer.is_correct_password(password): 
            session["logged_in_customer_email"] = customer.email
            flash("Login successful!")
            return redirect("/melons")
        else:
            flash("Incorrect password")
            return redirect("/login")


        # if password == customer.password: 
        #     session["logged_in_customer_email"] = customer.email
        #     flash("Login successful!")
        #     return redirect("/melons")
        # elif password != customer.password: 
        #     flash("Incorrect password")
        #     return redirect("/login")
   

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


@app.route("/logout")
def process_logout(): 
    """ Logs out customer ny deleting the log in session entry""" 

    del(session["logged_in_customer_email"])
    flash("Logged out")
    return redirect("/melons")


@app.route("/clear_cart")
def clear_cart(): 
    """ Empty the cart by clearing cart in session """

    del(session["cart"])
    # session["cart"] = {}
    flash("Your cart was cleared")
    return redirect("/melons")


@app.route("/remove_from_cart/<melon_id>")
def remove_from_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page

    if 'cart' not in session: 
        flash("Your cart is empty.")
        return redirect("/melons")
    else: 
        if session['cart'][melon_id] <= 0: 
            del(session['cart'][melon_id])
        else: 
            session['cart'][melon_id] = session['cart'][melon_id] - 1

    # if 'cart' not in session: 
    #     session['cart'] = {}

    # session['cart'][melon_id] = session['cart'].get(melon_id, 0) + 1

    print("session cart details: {}".format(session['cart']))
    print("session:{}".format(session))

    flash('Removed from cart!')

    return redirect('/cart')


if __name__ == "__main__":
    app.run(debug=True)
