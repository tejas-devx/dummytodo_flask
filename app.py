from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.route('/')
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": request.form['title'],
        "description": request.form['description'],
        "status": "Pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        return redirect(url_for("index"))

    if request.method == 'POST':
        task["title"] = request.form["title"]
        task["description"] = request.form["description"]
        task["status"] = request.form["status"]
        save_tasks(tasks)
        return redirect(url_for('index'))

    return render_template("edit.html", task=task)


@app.route('/delete/<int:id>')
def delete(id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != id]

    for i, t in enumerate(tasks, start=1):
        t["id"] = i

    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
