#importing the required libraries
from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

#initializing the flask app
app = Flask(__name__)
Scss(app)

#configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Task {self.id}>'
        
 

#main page(home page) of the website

#main logic of the website
@app.route('/', methods=['POST','GET'])
def index():
    #adding a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
        
        #view all current entered tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)
    
    
#deleting a task
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"
    


#edit an item
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue editing your task"
    else:
        return render_template('edit.html', task=task)
    
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)