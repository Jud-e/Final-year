from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required,logout_user, current_user
from datetime import datetime
import test
from test import phase_one
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staff.db'
db = SQLAlchemy(app)
app.secret_key = "String"
new_test=test.total

@app.route("/")
def index():
    return redirect(url_for("login"))


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scopus_id = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), nullable=False)
    promoted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False, default=0)

    def __repr__(self):
        return "Admin" + str(self.id)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, name, scopus_id, password_hash, email, score, promotion_date):
        self.name = name
        self.scopus_id = scopus_id
        self.password_hash = password_hash
        self.email = email
        self.score = score
        self.promotion_date = promotion_date

#admin parts
#==============================
@app.route("/admin",methods=['GET','POST'])
# @login_required
def admin():
    all_data = Employee.query.all()
    return render_template('admin.html', employees =all_data)

#updating:
@app.route('/edit', methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        my_data = Employee.query.get(int(request.form.get('id')))
        my_data.scopus_id = request.form['scopus_id']
        my_data.password_hash = request.form['password_hash']
        my_data.email = request.form['email']
        my_data.name = request.form['name']
        db.session.commit()
        flash('Employee Updated successfully')
        return redirect(url_for('admin'))

@app.route('/calculate', methods=['GET','POST'])
@login_required
def calculate():
    try:
        my_data = Employee.query.all()
        trying = session.query(Employee)
        attempt = trying.scopus_id
        phase_one(attempt)
        my_data.score = new_test
        db.session.commit()
        return render_template("profile.html")
    except:
        return render_template('profile.html')


#deletion of data(admin)
@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Employee Deleted Successfully')
    return redirect(url_for('admin'))
#=====================================

#=================user end============
@app.route('/signup', methods=['POST','GET'])
def signup():
    return render_template('signup.html')
#Part that has to do with insertion
@app.route('/insert',methods=['POST'])
def insert():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password_hash'], 'sha256')
        date_string = request.form["date"]
        date_format = [int(i) for i in date_string.split("-")]
        score = 0
        my_data = Employee(name=request.form['name'], scopus_id=request.form['scopus_id'],
                           password_hash=hashed_pw, promotion_date=datetime(*date_format),
                           email=request.form['email'],score=score)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('login'))
#end part
#Flask_login stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form.get('scopus_id') == 'admin' and request.form.get('password_hash') == 'admin':
            return redirect(url_for('admin'))
        else:
            user = Employee.query.filter_by(scopus_id =request.form.get('scopus_id')).first()
            if user:
                #Check the hash
                if check_password_hash(user.password_hash,request.form.get('password_hash')):
                    session['user'] = request.form.get('scopus_id')
                    login_user(user)
                    return redirect(url_for('profile'))

                else:
                    return render_template("login.html", error="Invalid Username or Password")
            else:
                return render_template("login.html", error="Invalid Username or Password")
    return render_template('login.html')


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/profile", methods= ['GET','POST'])
@login_required
def profile():
    return render_template('profile.html')


@app.route('/update', methods=['GET','POST'])
def update():
    my_data = current_user
    if request.method == 'POST':
        my_data.scopus_id = request.form['scopus_id']
        my_data.email = request.form['email']
        my_data.name = request.form['name']
        db.session.commit()
        return render_template('profile.html')
    return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)
