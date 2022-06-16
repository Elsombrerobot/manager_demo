from flask import Blueprint
from flask import render_template
from manager_demo.models import Project, User, Role

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    projects = Project.query.all()
    users = User.query.all()
    roles = Role.query.all()
    return render_template("home.html", title="Home", projects=projects, users=users, roles=roles)


@main.route("/about")
def about():
    return render_template("about.html", title="About")