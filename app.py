from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

#create flask app 
app = Flask(__name__)

#create SQLite database instance 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

#define model of a todo lisst task
class Task(db.Model):
    #db.Column is a column in the database
    #also specify data type of that key
    #pick one ot be the 'primary key', like DF labels 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    #string representation of the object 
    def __repr__(self):
        return f'<Task {self.id}>'
    
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding task to database'
    #sleect all Task objects from database
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)   
    
    
    
if __name__ == "__main__":
    with app.app_context():
        # Ensure the database schema is created with the updated model
        db.drop_all()  # Drop all tables
        db.create_all()  # Create all tables
    app.run(debug=True, host="0.0.0.0", port="5421")