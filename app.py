from flask import Flask, render_template, redirect, url_for, request, session, flash
from models import UserDatabase
import pandas

class DoctorApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your_secret_key'
        self.db = UserDatabase()
        self.db.load_patient_data('test.csv')

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/signup', 'signup', self.signup, methods=['GET', 'POST'])
        self.app.add_url_rule('/patient', 'patient', self.patient, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout', 'logout', self.logout)

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
        
        return render_template('new.html')

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
        
        return render_template('newsignup.html')

    def patient(self):
        if 'doctor' not in session:
            return redirect(url_for('login'))
        
        patient_data = None
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            patient_data = self.db.get_patient_by_id(patient_id)
            if patient_data:
                flash(f'Patient ID {patient_id} found!', 'success')
            else:
                flash(f'Patient ID {patient_id} not found!', 'danger')
        
        return render_template('dashboard.html', patient_data=patient_data)

    def logout(self):
        session.pop('doctor', None)
        return redirect(url_for('login'))

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = DoctorApp()
    app_instance.run()