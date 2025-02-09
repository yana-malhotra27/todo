from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
swagger = Swagger(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)

@app.route('/')
def index():
    """
    Show all todos
    ---
    responses:
      200:
        description: A list of todos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              complete:
                type: boolean
    """
    #show all todos
    todo_list=Todo.query.all()
    return render_template('base.html',todo_list=todo_list)
    #return "Hello World"

@app.route('/add', methods=['POST'])
def add():
    """
    Add a new todo item
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
        description: The title of the todo item
    responses:
      201:
        description: Redirect to the index page
    """
    #add new item
    title=request.form.get("title")
    new_todo=Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    """
    Update a todo item
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
        description: The ID of the todo item
    responses:
      200:
        description: Redirect to the index page
    """
    #add new item
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    """
    Delete a todo item
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
        description: The ID of the todo item
    responses:
      200:
        description: Redirect to the index page
    """
    #add new item
    todo=Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/about') #define diff urls
# def about():
#     return "About"

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)