from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Route to display all contacts (READ)
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# Route to add a new contact (CREATE)
@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        # Create a new contact instance and add it to the database
        new_contact = Contact(name=name, email=email, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        
        # Redirect to the main page after adding the contact
        return redirect(url_for('index'))
    
    # Render the add contact form
    return render_template('add.html')

# Route to edit an existing contact (UPDATE)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)  # Fetch the contact by ID
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        
        # Commit the updates to the database
        db.session.commit()
        
        # Redirect to the main page after editing
        return redirect(url_for('index'))
    
    # Render the edit form with the contact data
    return render_template('edit.html', contact=contact)

# Route to delete a contact (DELETE)
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)  # Fetch the contact by ID
    
    # Delete the contact from the database
    db.session.delete(contact)
    db.session.commit()
    
    # Redirect to the main page after deleting
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


