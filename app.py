from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
db = SQLAlchemy() # create the extension
db.init_app(app) # initialize the app with the extension

# Specify what a TODO Item look like in the database
class TodoItem(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   todotext = db.Column(db.String, nullable=False)
   done = db.Column(db.Boolean)

# Create the database and tables if it does not exist
with app.app_context():
   db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
   # Let's deal with form submissions first
   if request.method == 'POST':
       todoItem = TodoItem(
           todotext = request.form["todotext"],
           done = False
       )
       db.session.add(todoItem)
       db.session.commit()
       return redirect("/")
   else:
       todolist = db.session.execute(db.select(TodoItem)).scalars()
       return render_template("index.html", todolist=todolist)

