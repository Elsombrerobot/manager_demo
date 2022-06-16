from manager_demo import db
from manager_demo.db_client.db_utils import commit
from manager_demo.models import Role, User, Project
from datetime import datetime

def get(user_id : str):
    """Get a User."""
    return User.query.get(user_id)

@commit
def create(first_name : str, last_name : str, email : str, password : str, image_file : str):
    """Create a user."""
    user = User(first_name=first_name, last_name=last_name, email=email, password=password, image_file=image_file)
    db.session.add(user)
    return user

@commit
def update(user : User, first_name : str=None,
                        last_name : str=None,
                        email : str=None,
                        password : str=None,
                        image_file : str=None):
    """Update a user."""
    user.first_name = first_name or user.first_name
    user.last_name = last_name or user.last_name
    user.email = email or user.email
    user.password = password or user.password
    user.image_file = image_file or user.image_file
    user.date_modified = datetime.utcnow()
    return user

@commit
def delete(user : User):
    """Delete a user."""
    db.session.delete(user)

@commit
def assign_role(user : User, role: Role):
    """Add a role to the user."""
    user.roles.append(role)
    db.session.add(user)

@commit
def remove_role(user : User, role: Role):
    """Remove a role from the user."""
    user.roles.remove(role)
    db.session.add(user)

@commit
def assign_project(user : User, project: Project):
    """Add a project to the user."""
    user.projects.append(project)
    db.session.add(user)

@commit
def remove_project(user : User, project: Project):
    """Remove a project from the user."""
    user.projects.remove(project)
    db.session.add(user)