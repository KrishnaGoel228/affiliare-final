from flask import Flask, render_template, request, redirect,flash,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
import json

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(25))

class Affiliate(User):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(50))
    phonenoaff = db.Column(db.Integer)
    exp = db.Column(db.String(75))
    niche = db.Column(db.String(75))
    audtype = db.Column(db.String(75))
    audsize = db.Column(db.String(75))

class Company(User):
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cname = db.Column(db.String(50))
    headname = db.Column(db.String(50))
    phoneno = db.Column(db.Integer) 
    compniche = db.Column(db.String(50))
    compsize = db.Column(db.Integer) 
    techstack = db.Column(db.String(50))
    trmethod = db.Column(db.String(50))
    weblink = db.Column(db.String(150))
    products = db.relationship('Product',backref='author', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    commision = db.Column(db.Float)
    price = db.Column(db.Float)
    description = db.Column(db.String(150))
    type = db.Column(db.String(50))
    cpa = db.Column(db.Boolean)
    link = db.Column(db.String(150))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
class Affiliateproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aff_id = db.Column(db.Integer, db.ForeignKey('affiliate.id'), nullable=False)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    visits = db.Column(db.Integer)
    sales = db.Column(db.Integer)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')


@app.route("/signup", methods=["GET", "POST"] )
def signup():
    return render_template("signup0.html")


@app.route("/signup1", methods=["GET", "POST"] )

def signup1():
    if current_user.is_authenticated:
        flash("You are already logged in", category="success")
        return redirect("/")
    if request.method == "POST":
        nameaff = request.form['nameaff']
        emailaff = request.form['emailaff']
        passwordaff1 = request.form['passwordaff1']
        passwordaff2 = request.form['passwordaff2']
        phonenoaff = request.form['phoneno']
        exp = request.form['exp']
        nicheaff = request.form['niche']
        audtype = request.form['audtype']
        audsize = request.form['audsize']

        print(nameaff, emailaff, passwordaff1, passwordaff2)
        user = User.query.filter_by(email=emailaff).first()
        if user:    
            flash("Email already exists", category="error")
            return redirect("/signup1")
        elif passwordaff1 != passwordaff2:
            flash("Passwords don't match", category="error")
            return redirect("/signup1")
        
        elif len(passwordaff1) < 6:
            flash("Password must be at least 6 characters", category="error")
            return redirect("/signup1")
        
        elif len(nameaff) < 1:
            flash("Name cannot be empty", category="error")
            return redirect("/signup1")
        
        elif len(emailaff) < 1:
            flash("Email cannot be empty", category="error")
            return redirect("/signup1")
        
        else:
            new_user = Affiliate(name=nameaff, email=emailaff,phonenoaff=phonenoaff,niche=nicheaff,audsize=audsize,audtype=audtype,exp=exp,  password=generate_password_hash(passwordaff1, method='sha256'), user_type="affiliate")
            db.session.add(new_user)
            db.session.commit()
            flash("Account  created!", category="success")
            login_user(new_user, remember=True)
            return redirect("/")
        
    return render_template("signup1.html", user=current_user)

@app.route("/signup2", methods=["GET", "POST"] )
def signup2():
    if current_user.is_authenticated:
        flash("You are already logged in", category="success")
        return redirect("/")
    if request.method == "POST":
        namecomp = request.form['namecomp']
        emailcomp = request.form['emailcomp']
        passwordcomp1 = request.form['passwordcomp1']
        passwordcomp2 = request.form['passwordcomp2']
        headname = request.form['headname']
        phoneno = request.form['phoneno'] 
        compniche = request.form['compniche']
        compsize = request.form['compsize'] 
        techstack = request.form['techstack']
        trmethod = request.form['trmethod']
        weblink = request.form['weblink']

        print(namecomp, emailcomp, passwordcomp1, passwordcomp2)
        user = Company.query.filter_by(email=emailcomp).first()
        if user:    
            flash("Email already exists", category="error")
            return redirect("/signup2")
        elif passwordcomp1 != passwordcomp2:
            flash("Passwords don't match", category="error")
            return redirect("/signup2")
        
        elif len(passwordcomp1) < 6:
            flash("Password must be at least 6 characters", category="error")
            return redirect("/signup2")
        
        elif len(namecomp) < 1:
            flash("Name cannot be empty", category="error")
            return redirect("/signup2")
        
        elif len(emailcomp) < 1:
            flash("Email cannot be empty", category="error")
            return redirect("/signup2")
        
        else:
            new_company = Company(cname=namecomp, email=emailcomp,phoneno=phoneno, compniche=compniche, compsize=compsize, headname=headname, techstack=techstack,trmethod=trmethod,weblink=weblink, password=generate_password_hash(passwordcomp1, method='sha256'), user_type="company")
            db.session.add(new_company)
            db.session.commit()
            flash("Account  created!", category="success")
            login_user(new_company, remember=True)
            return redirect("/")
    print(current_user)   
    return render_template("signup2.html", company=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect("/")
        else:
            flash("Email or password is incorrect", category="error")
            return redirect("/login")
        
    return render_template("login1.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/test")
@login_required
def test():
    value = request.cookies.get("affiliare")
    if value:   
        return value
    else:
        return jsonify(current_user.user_type)


@app.route("/addproduct", methods=["GET", "POST"] )
def addproduct():
    
    if current_user.is_authenticated and current_user.user_type == "company":
        if request.method == "POST":
            nameprod = request.form['nameprod']
            price = request.form['price']
            commision = request.form['commision']
            
            description = request.form['description']
            ptype = ''
            link = request.form['link']

            print(nameprod, commision, price, description, ptype, link)
            # product = product.query.filter_by(name=nameprod).first()
            # if product:    
            #     flash("Product already exists", category="error")
            #     return redirect("/addproduct")
            # else:
            new_product = Product(name=nameprod, commision=commision, price=price, description=description, type=ptype, link=link, company_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            flash("Product  added!", category="success")
            return redirect("/addproduct")
        products = Product.query.filter_by(company_id=current_user.id).all()
        return render_template("addproduct.html", products=products)

    else:
        return redirect("/")

@app.route("/viewproducts", methods=["GET", "POST"] )
def viewproducts():
    if current_user.is_authenticated and current_user.user_type == "affiliate":
        products = Product.query.all()
        p = {}
        # for product in products:
            # print(product.name)
            # p[str(product.id)] = [product.name, product.commision, product.price, product.description, product.type, product.link, product.company_id]
        id = current_user.id
        return render_template("viewproducts.html", products=products, id=id)
    else:
        return redirect("/")

@app.route("/<affid>/<prodid>")
def afflink(affid, prodid):
    if User.query.filter_by(id=affid).first() and Product.query.filter_by(id=prodid).first():
        print(affid, prodid)
        product = Product.query.filter_by(id=prodid).first()
        data = Affiliateproduct.query.filter_by(aff_id=affid, prod_id=prodid).first()
        if data:
            data.visits += 1
           
            db.session.commit()
        else:
            
            new_data = Affiliateproduct(aff_id=affid, prod_id=prodid, visits=1, sales=0)
            db.session.add(new_data)
            db.session.commit()

        if request.cookies.get("affiliare"):
            print("cookie exists")
            response = make_response(redirect("https://"+product.link))
            response.delete_cookie('affiliare')
            
            val = json.dumps([affid, prodid])
            response.set_cookie("affiliare", val, max_age=60*60*24*30)
            return response
        else:
            print("cookie does not exist")
            response = make_response(redirect("https://"+product.link))
            val = json.dumps([affid, prodid])
            response.set_cookie("affiliare", val, max_age=60*60*24*30)
            return response
        return redirect("https://"+product.link)
    else:
        return redirect("/")

@app.route("/sold")
def sold():
    if request.cookies.get("affiliare"):
        value = request.cookies.get("affiliare")
        value = json.loads(value)
        print(value)
        aff_id = value[0]
        prod_id = value[1]
        product = Product.query.filter_by(id=prod_id).first()
        data = Affiliateproduct.query.filter_by(aff_id=aff_id, prod_id=prod_id).first()
        data.sales += 1
        
        db.session.commit()
        
        company = Company.query.filter_by(id=product.company_id).first()
        return redirect("https://"+company.weblink)
    else:
        return redirect("/")


@app.route("/affdashboard")
@login_required
def affdashboard():
    if current_user.is_authenticated and current_user.user_type == "affiliate":
        id = current_user.id
        affiliate = Affiliate.query.filter_by(id=id).first()
        data = Affiliateproduct.query.filter_by(aff_id=id).all()
        p = defaultdict(list)
        def add_value(key, value):
            if key not in p:
                p[key] = []
                p[key].append(value)
            else:
                p[key].append(value)
        
        for d in data:
            product = Product.query.filter_by(id=d.prod_id).first()
            commision = product.commision
            rev = commision * d.sales
            add_value(product.name, [d.visits, d.sales, rev])
        
        return render_template("affdashboard.html", affiliate=affiliate, products=p)
    else:
        return redirect("/")

@app.route("/compdashboard")
@login_required
def compdashboard():
    if current_user.is_authenticated and current_user.user_type == "company":
        id = current_user.id
        company = Company.query.filter_by(id=id).first()
        products = Product.query.filter_by(company_id=id).all()
        p = defaultdict(list)
        def add_value(key, value):
            if key not in p:
                p[key] = []
                p[key].append(value)
            else:
                p[key].append(value)
        for product in products:
            print(product.name)
            commision = product.price * (product.commision/100)
            data = Affiliateproduct.query.filter_by(prod_id=product.id).all()
            traffic = 0
            sales = 0
            for d in data:
                traffic += d.visits
                sales += d.sales
            rev = sales * product.price
            t_commision = sales * product.commision
            add_value(product.name, [commision, product.price,len(data),traffic,sales,rev,t_commision])
            # p[str(product.id)] = [product.name, product.commision, product.price, product.description, product.type, product.link, product.company_id]
        return render_template("compdashboard.html", company=company, products=p)
    else:
        return redirect("/")

def create_database1(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database!")


if __name__ == "__main__": 
    create_database1(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    app.run(debug=True)