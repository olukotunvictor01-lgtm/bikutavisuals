from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'photography_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    session_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    about_info = {
        "name": "Lens & Light Photography",
        "bio": "Capturing your most precious moments with authentic storytelling.",
        "specialties": ["Portraits", "Weddings", "Events"]
    }
    return render_template('about.html', info=about_info)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        new_booking = Booking(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            session_type=request.form.get('session_type'),
            date=request.form.get('date'),
            message=request.form.get('message')
        )
        try:
            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            db.session.rollback()
            return "There was an error saving your booking."

    return render_template('book.html')

# Updated Admin Route with Password Protection
@app.route('/admin/bookings', methods=['GET', 'POST'])
def view_bookings():
    # If the admin submitted the login form
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'photo123':  # <-- Change your password here!
            session['logged_in'] = True
        else:
            flash('Incorrect password, please try again.')

    # Check if the user is logged in
    is_logged_in = session.get('logged_in', False)
    
    all_bookings = []
    if is_logged_in:
        all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        
    return render_template('admin.html', bookings=all_bookings, logged_in=is_logged_in)

# Route to log out
@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)