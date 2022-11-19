from flask import Flask, render_template, request, redirect, session 
import ibm_db
import re
from datetime import datetime


app = Flask(__name__)


app.secret_key = 'safste5eyhrsgh'
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rbb98449;PWD=13r2ik5sdnuxEUYm",'','')
except Exception as e:
    print(e)


#HOME--PAGE
@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")



#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        query = 'SELECT * FROM register WHERE username =?;'
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            query = "INSERT INTO register (username,email,password) VALUES (?,?,?)"
            stmt=ibm_db.prepare(conn,query)
            ibm_db.bind_param(stmt,1,username)
            ibm_db.bind_param(stmt,2,email)
            ibm_db.bind_param(stmt,3,password)
            ibm_db.execute(stmt)
            msg = 'You have successfully registered !'
    return render_template('signup.html', msg = msg)
        
        
 
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM register WHERE username = ? AND password = ?;"
        stmt = ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_tuple(stmt)
        print (account)
        
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



       





#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    
    date = request.form['date']
    date = str(datetime.strptime(date.replace("T"," "),"%Y-%m-%d %H:%M"))
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']
    print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
    query = 'INSERT INTO expenses (userid,date,expensename,amount,paymode,category) VALUES (?, ?, ?, ?, ?, ?)'
    stmt = ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,session['id'])
    ibm_db.bind_param(stmt,2,date)  
    ibm_db.bind_param(stmt,3,expensename)
    ibm_db.bind_param(stmt,4,amount)
    ibm_db.bind_param(stmt,5,paymode)
    ibm_db.bind_param(stmt,6,category)
    ibm_db.execute(stmt)
    # cursor.execute('INSERT INTO expenses VALUES (NULL,  % s, % s, % s, % s, % s, % s)', (session['id'] ,date, expensename, amount, paymode, category))
    
    return redirect("/display")



#DISPLAY---graph 

@app.route("/display")
def display():
    print(session["username"],session['id'])
    query = 'SELECT * FROM expenses WHERE userid = ? ORDER BY date DESC'
    stmt = ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,(str(session['id'])))
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    expense = []
    while tuple != False:
        expense.append(list(tuple))
        tuple = ibm_db.fetch_tuple(stmt)
    query = 'SELECT SUM(amount) FROM expenses WHERE userid= ?'
    stmt = ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,(str(session['id'])))
    ibm_db.execute(stmt)
    texpense = []   
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple!=False:
        texpense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    print(texpense)
    total=0
    t_food=0
    t_entertainment=0
    t_business=0
    t_rent=0
    t_EMI=0
    t_other=0
 
    for x in expense:
          x[2] = datetime.strftime(x[2],"%d/%m/%Y %-I:%M %p")
          total += float(x[4])
          if x[6] == "food":
              t_food += float(x[4])
            
          elif x[6] == "entertainment":
              t_entertainment  += float(x[4])
        
          elif x[6] == "business":
              t_business  += float(x[4])
          elif x[6] == "rent":
              t_rent  += float(x[4])
           
          elif x[6] == "EMI":
              t_EMI  += float(x[4])
         
          elif x[6] == "other":
              t_other  += float(x[4])
        
    if expense:
            return render_template('display.html' ,expense = expense,title="History",texpense = texpense, total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other)
    return redirect('/add')                  



# #delete---the--data

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
    query = 'DELETE FROM expenses WHERE  id = ?'
    stmt = ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,str(id))
    ibm_db.execute(stmt)
    # cursor.execute('DELETE FROM expenses WHERE  id = {0}'.format(id))
    # mysql.connection.commit()
    print('deleted successfully')    
    return redirect("/display")
 
    
# #UPDATE---DATA

@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM expenses WHERE  id = %s', (id,))
    # row = cursor.fetchall()
    query = 'SELECT * FROM expenses WHERE  id =?'
    stmt = ibm_db.prepare(conn,query)
    ibm_db.bind_param(stmt,1,str(id))
    ibm_db.execute(stmt)
    row = []
    tuple = ibm_db.fetch_tuple(stmt)
    while tuple!=False:
        row.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    print(row[0])
    return render_template('edit.html', expenses = row[0])




@app.route('/update/<id>', methods = ['POST'])
def update(id):
  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
    
      query = 'UPDATE expenses SET date = ? , expensename = ? , amount = ?, paymode = ?, category = ? WHERE expenses.id = ? '
    #   cursor.execute("UPDATE `expenses` SET `date` = % s , `expensename` = % s , `amount` = % s, `paymode` = % s, `category` = % s WHERE `expenses`.`id` = % s ",(date, expensename, amount, str(paymode), str(category),id))
    #   mysql.connection.commit()
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,date)
      ibm_db.bind_param(stmt,2,expensename)
      ibm_db.bind_param(stmt,3,amount)
      ibm_db.bind_param(stmt,4,str(paymode))
      ibm_db.bind_param(stmt,5,str(category))
      ibm_db.bind_param(stmt,6,id)
      ibm_db.execute(stmt)
      print('successfully updated')
      return redirect("/display")
     
      

            
 
         
    
            
#  #limit
@app.route("/limit" )
def limit():
       return redirect('/limitn')

@app.route("/limitnum" , methods = ['POST' ])
def limitnum():
     if request.method == "POST":
         number= request.form['number']
         print(number)
         query = 'INSERT INTO limits (userid,limitss) VALUES (?, ?) '
         stmt = ibm_db.prepare(conn,query)
        #  cursor.execute('INSERT INTO limits VALUES (NULL, % s, % s) ',(session['id'], number))
        #  mysql.connection.commit()
         ibm_db.bind_param(stmt,1,session['id'])
         ibm_db.bind_param(stmt,2,number)
         ibm_db.execute(stmt)
         return redirect('/limitn')
     
         
@app.route("/limitn") 
def limitn():
    query = "SELECT limitss FROM limits ORDER BY limits.id DESC LIMIT 1"
    stmt = ibm_db.prepare(conn,query)
    # cursor.execute('SELECT limitss FROM `limits` ORDER BY `limits`.`id` DESC LIMIT 1')
    ibm_db.execute(stmt)
    x= ibm_db.fetch_tuple(stmt)
    if x:
        s = x[0]
        return render_template("limit.html" ,title="Limit", y=s)
    else:
        return render_template("limit.html",title="Limit" , y=0)

# #REPORT

@app.route("/today")
def today():
      query = 'SELECT TIME(date), amount FROM expenses  WHERE userid = ? AND DATE(date) = DATE(NOW())'
    #   cursor.execute('SELECT TIME(date), amount FROM expenses  WHERE userid = %s AND DATE(date) = DATE(NOW()) ',(str(session['id'])))
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      tuple = ibm_db.fetch_tuple(stmt)
      texpense = []   
      while tuple!=False:
        texpense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
      print(texpense)
      query = 'SELECT * FROM expenses WHERE userid = ? AND DATE(date) = DATE(NOW()) ORDER BY expenses.date DESC'
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      expense = []   
      while tuple!=False:
        expense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
      print(expense)
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    #   expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += float(x[4])
            
          elif x[6] == "entertainment":
              t_entertainment  += float(x[4])
        
          elif x[6] == "business":
              t_business  += float(x[4])
          elif x[6] == "rent":
              t_rent  += float(x[4])
           
          elif x[6] == "EMI":
              t_EMI  += float(x[4])
         
          elif x[6] == "other":
              t_other  += float(x[4])
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html",title="Today" ,texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
     

@app.route("/month")
def month():
      query = 'SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= ? AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) '
    #   cursor.execute('SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= %s AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) ',(str(session['id'])))
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      tuple = ibm_db.fetch_tuple(stmt)
      texpense = []   
      while tuple!=False:
        texpense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
      print(texpense)
      
    #   cursor = mysql.connection.cursor()
      query = 'SELECT * FROM expenses WHERE userid = ? AND MONTH(DATE(date))= MONTH(now()) ORDER BY expenses.date DESC'
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND MONTH(DATE(date))= MONTH(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      expense = []   
      tuple = ibm_db.fetch_tuple(stmt)
      while tuple!=False:
        expense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
    #   expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += float(x[4])
          if x[6] == "food":
              t_food += float(x[4])
            
          elif x[6] == "entertainment":
              t_entertainment  += float(x[4])
        
          elif x[6] == "business":
              t_business  += float(x[4])
          elif x[6] == "rent":
              t_rent  += float(x[4])
           
          elif x[6] == "EMI":
              t_EMI  += float(x[4])
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("month.html",title="Month", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
         
@app.route("/year")
def year():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= %s AND YEAR(DATE(date))= YEAR(now()) GROUP BY MONTH(date) ORDER BY MONTH(date) ',(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)
      query = 'SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= ? AND YEAR(DATE(date))= YEAR(now()) GROUP BY DATE(date) ORDER BY DATE(date)'
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      texpense = []   
      tuple = ibm_db.fetch_tuple(stmt)
      while tuple!=False:
        texpense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
      
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND YEAR(DATE(date))= YEAR(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    #   expense = cursor.fetchall()
      query = 'SELECT * FROM expenses WHERE userid = ? AND YEAR(DATE(date))= YEAR(now()) ORDER BY expenses.date DESC'
      stmt = ibm_db.prepare(conn,query)
      ibm_db.bind_param(stmt,1,session['id'])
      ibm_db.execute(stmt)
      expense = []   
      tuple = ibm_db.fetch_tuple(stmt)
      while tuple!=False:
        expense.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
     
      for x in expense:
          print(x)
          total += float(x[4])
          if x[6] == "food":
              t_food += float(x[4])
            
          elif x[6] == "entertainment":
              t_entertainment  += float(x[4])
        
          elif x[6] == "business":
              t_business  += float(x[4])
          elif x[6] == "rent":
              t_rent  += float(x[4])
           
          elif x[6] == "EMI":
              t_EMI  += float(x[4])
         
          elif x[6] == "other":
              t_other  += float(x[4])
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html",title="Year", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )

#log-out

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

             

if __name__ == "__main__":
    app.run(debug=True)