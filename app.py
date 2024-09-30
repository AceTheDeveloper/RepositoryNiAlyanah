from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

class Education:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "I miss you"
        self.setUpDb()
        self.defineRoute()
        
    def setUpDb(self):
        self.app.config['MYSQL_HOST'] = 'localhost'
        self.app.config['MYSQL_USER'] = 'root'
        self.app.config['MYSQL_PASSWORD'] = ''
        self.app.config['MYSQL_DB'] = 'education'
        self.mysql = MySQL(self.app)
    
    def defineRoute(self):
        self.app.add_url_rule('/', 'index', self.index, methods=['GET','POST'])
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        
    def index(self):
        
        if request.method == "POST":
            userName = request.form.get('name')
            userGender = request.form.get('gender')
            userAge = request.form.get('age')
            userEmail = request.form.get('email')
            userPass = request.form.get('password')
            
            cur = self.mysql.connection.cursor()
            insertUser = "INSERT INTO users (name, gender, age, email, password, userType) VALUES(%s,%s,%s,%s,%s,%s)"
            cur.execute(insertUser, (userName, userGender, userAge,userEmail, userPass, "user",))
            self.mysql.connection.commit()
            cur.close()
            
            return url_for('login')
            
        return render_template('register.html')
    
    def login(self):
        
        loginEmail = request.form.get('logemail')
        loginPassword = request.form.get('logpassword')
        
        if request.method == "POST":
            cur = self.mysql.connection.cursor()
            validateUser = "SELECT *FROM users WHERE email = %s AND password = %s"
            cur.execute(validateUser, (loginEmail, loginPassword))
            user = cur.fetchone()
            if user:
                session['id'] = user[0]
                return redirect(url_for('userDashBoard'))
        
            
        return render_template('login.html')
    
    def userDashboard(self):
        return render_template('userDashboard')
    
    
    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    app = Education()
    app.run()