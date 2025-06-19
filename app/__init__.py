#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error


# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():

    with connect_db() as client:
        # Get all the tasks from the DB
        sql = "SELECT id, name, priority, complete FROM tasks ORDER BY priority ASC"
        result = client.execute(sql)
        tasks = result.rows

        # And show them on the page
    return render_template("pages/home.jinja", tasks=tasks)
#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    priority = request.form.get("priority")

    # sanitize the inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the task to the DB
        sql = "INSERT INTO tasks (name, priority) VALUES (?, ?)"


        values = [name, priority]
        client.execute(sql, values)

        # Go back to the home page
        flash(f"task '{name}' added", "success")
        return redirect("/")


#-----------------------------------------------------------
# Route for deleting a task, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_task(id):
    with connect_db() as client:
        # Delete the task from the DB
        sql = "DELETE FROM tasks WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        return redirect("/")
    
#-----------------------------------------------------------
# Route for deleting a task, Id given in the route
#-----------------------------------------------------------
@app.get("/complete/<int:id>")
def complete_task(id):
    with connect_db() as client:
        sql = "UPDATE tasks set complete=? WHERE id=?"
        values = [1, id]
        client.execute(sql, values)
        

        #Go back to home
        return redirect("/")


@app.get("/incomplete/<int:id>")
def incomplete_task(id):
    with connect_db() as client:
        sql = "UPDATE tasks set complete=? WHERE id=?"
        values = [0, id]
        client.execute(sql, values)

        #Go back to home
        return redirect("/")