from crypt import methods
from flask import Flask,render_template,url_for,request,flash,session,redirect
import sqlite3,os

#app Instance
app = Flask(__name__)

app.secret_key=os.urandom(24)

@app.route('/login')
@app.route("/")
def login():
    return render_template("login.html",title="Login")



@app.route("/register")
def register():
    return render_template("register.html",title="register")


@app.route("/home")
def index():
    if 'id' in session:
        return render_template('home.html',title="Home")
    else:
        return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html",title="About")

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route("/add_user",methods=['POST'])
def add_user():
    name=request.form.get('name') 
    email=request.form.get('uemail')
    rpassword=request.form.get('rpassword')
    password=request.form.get('upassword')
    if(password==rpassword):
        try:
            conn=sqlite3.connect('register.db')
            cur=conn.cursor()
            #cur.execute("UPDATE users SET password='{}'WHERE name = '{}'".format(password, name))
            cur.execute("""INSERT INTO  users(name,email,password) VALUES('{}','{}','{}')""".format(name,email,password))
            conn.commit()
            cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
            myuser=cur.fetchall()
        except sqlite3.Error as e:
            print(f"sqlite3 error:\n{e}")
        flash('You have successfully registered!')
        session['id']=myuser[0][0]
        return redirect('/')
    else:
        flash("password didn't match")
        return redirect("/")

@app.route("/login_validation",methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    print(email,password)
    conn=sqlite3.connect('register.db')
    cur=conn.cursor()
    cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cur.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        flash('You were successfully logged in')
        return redirect('/home')
    else:
        flash('Invalid credentials !!!')
        return redirect('/')

#Main Method
if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True) 