from market import db, bcrypt, login_manager
from flask_login import UserMixin


# helper function required by flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User modal
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(length=50), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    # not stored column... relationship with Item established
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'User: {self.username}'

    # to send budget in international format {xxx,xxx,xxx}
    @property
    def prettier_budget(self):
        return f"{self.budget:,}"

    # property to keep plain password
    @property
    def password(self):
        return self.password

    # create and set hashed password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    # match hashed password with attempted_password
    def correct_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    # checks is this user can purchase given item
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    # checks is this user can sell given item
    def can_sell(self, item_obj):
        return item_obj.owner == self.id


# Item Modal
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    # foreign key
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item: {self.name}'

    # move item to given user
    def assign_ownership(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    # move item form user to market
    def move_to_market(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
