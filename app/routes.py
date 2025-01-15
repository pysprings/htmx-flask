from flask import Blueprint, render_template, request, jsonify
from .domain import TodoList, Todo, Page

# Global TodoList instance
todos = TodoList()

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    page = Page.create("Todo List", todos=todos)
    return render_template("index.j2.html", page=page)


@bp.route("/todos", methods=["POST"])
def create_todo():
    title = request.form.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    todo = Todo.create(title)
    todos.add(todo)

    # Create page with updated todos for the fragments
    page = Page.create("Todo List", todos=todos)

    # Render the main response (todo list)
    response = render_template("fragments/_todo_list.j2.html", page=page)

    # Render the form as an OOB swap
    form_html = render_template("fragments/_todo_form.j2.html", page=page)

    # Return both, with the form marked for OOB swap
    return f"{response}<div id='todo-form' hx-swap-oob='true'>{form_html}</div>"
