from flask import Flask, render_template, redirect, session, flash
from forms import UserForm, LoginForm
from models import User, connect_db, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SECRET_KEY'] = 'HeisKing!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    """Show Homepage"""
    print(session)
    return redirect ('/register')

#Register routes---------------------------------------------------
@app.route('/register')
def register_form():
    """Show register form on page"""
    form = UserForm()
    return render_template('register_form.html',form=form)

@app.route('/register', methods=['POST'])
def register_user():
    """Submit form to server to register a new user"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.commit()
        session['username'] = new_user.username
        return redirect('/secret')

#Log in routes---------------------------------------------------
@app.route('/login')
def login_form():

    if 'username' in session:
        return redirect('/secret')
    
    form = LoginForm()
    return render_template('login_form.html', form=form)

@app.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        user = User.authenticate(username, password)
        session['username'] = username
        
        if user:
            return redirect('/secret')

#Route for the /secret page!-------------------------------------
@app.route('/secret')
def secret_page():
    if 'username' not in session:
        flash('Please login/register first!')
        return redirect('/')
    return render_template('secret.html')

#Route to logout------------------------------------------------
@app.route('/logout')
def user_loguout():
    session.pop('username')
    flash('Goodbye!')
    return redirect('/')