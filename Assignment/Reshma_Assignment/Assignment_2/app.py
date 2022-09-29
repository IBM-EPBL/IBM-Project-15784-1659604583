from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/confirm', methods=['POST','GET'])
def confirm():
    if request.method == 'POST':
        n=request.form.get('name')
        e=request.form.get('mail')
        return render_template('confirm.html',name=n,mail=e)

if(__name__=="__main__"):
    app.run(debug=True)