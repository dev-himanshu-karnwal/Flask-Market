from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


# route for homepage
@app.route('/home')
@app.route('/index')
@app.route('/')
def home_page():
    '''render Home page'''
    return render_template('home.html')


# route for market page, purchase, sell item
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    '''
    Route for market page, purchase, sell item
    GET: render market page
    POST: Sell/Purchase Item
    '''

    if request.method == 'POST':
        # get name of item to be purhcased from form
        purchased_item = request.form.get('purchased_item')
        # get complete db Item object from name
        purchased_item_object = Item.query.filter_by(
            name=purchased_item).first()

        # if purchase form was filled and such item exists
        if purchased_item_object:
            # check if current user can purchase the item
            if current_user.can_purchase(purchased_item_object):
                # purchase
                purchased_item_object.assign_ownership(current_user)
                flash(
                    f'Congratulations! You had successfully purchased {purchased_item_object.name} for {purchased_item_object.price}$', category='success')

            # can not purchase
            else:
                flash(
                    f'Insufficient budget of {current_user.budget}$ to purchase {purchased_item_object.name} for {purchased_item_object.price}$', category='danger')

            # redirect to market page
            return redirect(url_for('market_page'))

        # get name of item to be sold from form
        sold_item = request.form.get('sold_item')
        # get complete Item object from DB from name
        sold_item_object = Item.query.filter_by(
            name=sold_item).first()

        # if sale form was filled and such item exists
        if sold_item_object:
            # if user can sell item
            if current_user.can_sell(sold_item_object):
                # sell
                sold_item_object.move_to_market(current_user)
                flash(
                    f'{sold_item_object.name} had been sold successfully for {sold_item_object.price}$', category='success')
            # user can't sell item
            else:
                flash(
                    f"You not being the owner of {sold_item_object.name} can't sell it", category='danger')

            # redirect to market page
            return redirect(url_for('market_page'))

    if request.method == 'GET':
        # create purchase and sell form
        purchase_form = PurchaseItemForm()
        selling_form = SellItemForm()

        # get items that are currently not owned by anyone
        items = Item.query.filter_by(owner=None)
        # items that are owned by current user
        owned_items = Item.query.filter_by(owner=current_user.id)
        # render market page with all details
        return render_template('market.html', items=items, owned_items=owned_items, purchase_form=purchase_form, selling_form=selling_form)


# route for signup
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # create user registration form
    form = RegisterForm()

    # if form was submitted and all validations were successful
    if form.validate_on_submit():
        # create new user
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)

        # add and save db session
        db.session.add(new_user)
        db.session.commit()
        # login same user
        login_user(new_user)
        flash(
            f'Registered successfully. You are now logged in as {new_user.username}', category='success')

        return redirect(url_for('market_page'))

    # if there are errors from form validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')

    # render register page
    return render_template('register.html', form=form)


# route for login
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # create login form
    form = LoginForm()

    # if form was submitted and validations were successful
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.correct_password(attempted_password=form.password.data):
            login_user(user)
            flash(
                f'Logged in successfully as {user.username}', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Invalid username or password', category='danger')

    # if there are errors from form validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')

    return render_template('login.html', form=form)


# route for logout
@app.route('/logout')
def logout_page():
    # logout user
    logout_user()
    flash('Logged out successfully', category='info')
    # redirect back to home page
    return redirect(url_for('home_page'))
