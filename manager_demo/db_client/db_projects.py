from manager_demo import db
from manager_demo.db_client.db_utils import commit
from manager_demo.models import Project
from datetime import datetime

def get(project_id : str):
    """Get a Project."""
    return Project.query.get(project_id)

@commit
def create(name : str, title : str, short_name : str, fps : str, production_type : str, description : str):
    """Create a project."""
    project = Project(name=name, title=title, short_name=short_name, fps=fps, production_type=production_type, description=description)
    db.session.add(project)
    return project

@commit
def update(project : Project, name : str=None,
                          title : str=None,
                          short_name : str=None,
                          fps : float=None,
                          production_type : str=None,
                          description : str=None):
    """Update a project."""
    project.name = name or project.name
    project.title = title or project.title
    project.short_name = short_name or project.short_name
    project.fps = fps or project.fps
    project.description = description or project.description
    project.production_type = production_type or project.production_type
    project.date_modified = datetime.utcnow()
    return project

@commit
def delete(project : Project):
    """Delete a project."""
    db.session.delete(project)

