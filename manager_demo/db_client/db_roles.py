from manager_demo import db
from manager_demo.db_client.db_utils import commit
from manager_demo.models import Role, User
from datetime import datetime

def get(user_id : str):
    """Get a User."""
    return User.query.get(user_id)

@commit
def create(name : str, level : int, description : str):
    """Create a role."""
    role = Role(name=name, level=level, description=description)
    db.session.add(role)
    return role

@commit
def update(role : Role, name : str=None,
                        level : int=None,
                        description : str=None):
    """Update a role."""
    role.name = name or role.name
    role.level = level or role.level
    role.description = description or role.description
    role.date_modified = datetime.utcnow()
    return role

@commit
def delete(role : Role):
    """Delete a role."""
    db.session.delete(role)
