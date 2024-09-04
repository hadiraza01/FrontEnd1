from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import UserDatabase

class DoctorApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key'
        self.db = UserDatabase()

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/signup', 'signup', self.signup, methods=['GET', 'POST'])
        self.app.add_url_rule('/patient', 'patient', self.patient, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)
        self.app.add_url_rule('/new','new', self.new)

    def new(self):
        return render_template('new.html')

    def index(self):
        return redirect(url_for('login'))

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            doctor = self.db.get_user(username, password)
            
            if doctor:
                session['doctor'] = doctor[1]
                return redirect(url_for('patient'))
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('login.html')

    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.db.get_user(username):
                flash('Username already exists', 'danger')
            else:
                self.db.insert_user(username, password)
                flash('Signup successful, please login', 'success')
                return redirect(url_for('login'))
        
        return render_template('signup.html')

    def patient(self):
        if 'doctor' not in session:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            flash(f'Patient ID {patient_id} submitted successfully!', 'success')
        
        return render_template('dashboard.html')

    def logout(self):
        session.pop('doctor', None)
        return redirect(url_for('login'))

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = DoctorApp()
    app_instance.run()