from datetime import datetime
from typing import Union
from flask import current_app
from manager_demo import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_role_table = db.Table('user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)

user_project_table = db.Table('user_project', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text(1500), unique=False, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    users = db.relationship("User",secondary=user_role_table, back_populates="roles")

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Role({self.name}, {self.level})"

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship("Role",secondary=user_role_table, back_populates="users")
    projects = db.relationship("Project",secondary=user_project_table, back_populates="users")

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id' : self.id}).decode("utf-8")
    
    
    def is_admin(self):
        """
        Compare the user against an admin role, and return True if the user qualify.

        It will compare the name of the role.
        """
        return "admin" in [role.name for  role in self.roles]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return (f"User(first_name = {self.first_name}, "
                f"last_name = {self.last_name}, "
                f"email = {self.email}, "
                f"roles = [{', '.join([role.name for  role in self.roles])}], "
                f"projects = [{', '.join([project.name for  project in self.projects])}])")


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), unique=True, nullable=False)
    title = db.Column(db.String(512), unique=True, nullable=False)
    short_name = db.Column(db.String(3), unique=True, nullable=False)
    description = db.Column(db.Text(2048), unique=False, nullable=True)
    production_type = db.Column(db.Text(64), unique=False, nullable=False)
    fps = db.Column(db.Float(64), unique=False, nullable=False)
    users = db.relationship("User",secondary=user_project_table, back_populates="projects")
    
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Project(title={self.title}, production_type={self.production_type}, fps={self.fps})"


