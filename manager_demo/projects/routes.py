from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from manager_demo.models import Project, User
from manager_demo.projects.forms import NewProjectForm, EditProjectForm, ProjectUserForm
from manager_demo.db_client import db_projects, db_users
from manager_demo.users.utils import admin_required

projects = Blueprint("projects", __name__)

fps_choice = [24, 25, 30, 29.999]
production_type = ["tvshow", "feature_film", "short"]

@projects.route("/project/all_projects")
def all_projects():
    projects = Project.query.all()
    return render_template('projects/all_projects.html', title='All Projects', projects=projects)

@projects.route("/project/new_project", methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    form = NewProjectForm()
    form.fps.choices = fps_choice
    form.production_type.choices = production_type
    if form.validate_on_submit():
        db_projects.create(name = form.name.data,
                          title = form.title.data,
                          short_name = form.short_name.data,
                          description = form.description.data,
                          fps = form.fps.data,
                          production_type = form.production_type.data)
        flash('Project has been created !', 'success')
        return redirect(url_for('projects.new_project'))
    return render_template('projects/new_project.html', title='New project', form=form)

@projects.route("/project/edit/<int:project_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = EditProjectForm(project=project)
    form.fps.choices = fps_choice
    form.production_type.choices = production_type
    if form.submit.data and form.validate() :
        db_projects.update(project, name=form.name.data,
                              title=form.title.data,
                              short_name=form.short_name.data,
                              fps=form.fps.data,
                              production_type=form.production_type.data,
                              description=form.description.data
                              )
        flash('User has been updated.', 'success')
        return redirect(url_for('projects.edit_project', project_id=project.id))
    
    #User form
    users = User.query.all()
    project_user_form = ProjectUserForm()
    project_user_form.user.choices = [user.full_name for user in users]

    if project_user_form.submit_user.data:
        user_id = None
        for user in users:
            if project_user_form.user.data == user.full_name:
                user_id = user.id
                break
        return redirect(url_for('projects.assign_project',
                        next_page=url_for('projects.edit_project',project_id=project.id),
                        project_title=project.title
                        ,user_id=user_id),code=307)

    if request.method == "GET":
        form.fps.choices = fps_choice
        form.production_type.choices = production_type
        form.name.data = project.name
        form.title.data = project.title
        form.short_name.data = project.short_name
        form.fps.data = project.fps
        form.production_type.data = project.production_type
        form.description.data = project.description
    return render_template("projects/edit_project.html",
                            title="Edit projects",
                            form=form,
                            project=project,
                            project_user_form=project_user_form)

@login_required
@admin_required
@projects.route("/role/assign_project", methods=['POST'])
def assign_project():
    project_title = request.args.get("project_title")
    user_id = request.args.get("user_id")
    next_page = request.args.get("next_page")
    user = User.query.get(user_id)
    project = Project.query.filter_by(title=project_title).one_or_none()

    if user and project:
        if project.title not in [project.title for project in user.projects]:
            db_users.assign_project(user, project)
            flash(f'{user.full_name} assigned to {project.title}.', 'success')
        else:
            flash(f'{user.full_name} is already assigned to {project.title}.', 'danger')
    else:
        flash('User or project does not exists.', 'danger')
    return redirect(next_page)

@login_required
@admin_required
@projects.route("/role/remove_project", methods=['GET', 'POST'])
def remove_project():
    project_title = request.args.get("project_title")
    user_id = request.args.get("user_id")
    next_page = request.args.get("next_page")
    user = User.query.get(user_id)
    project = Project.query.filter_by(title=project_title).one_or_none()

    if user and project:
        if project.title in [project.title for project in user.projects]:
            db_users.remove_project(user, project)
            flash(f'{user.full_name} unassigned from {project.title}.', 'success')
        else:
            flash(f'{user.full_name} is not assigned {project.title}.', 'danger')
    else:
        flash('User or project does not exists.', 'danger')
    return redirect(next_page)

@login_required
@admin_required
@projects.route("/project/delete_project/<string:project_id>", methods=['POST'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        db_projects.delete(project)
        flash(f'{project.title} deleted.', 'success')
    else:
        flash('project does not exists.', 'danger')
    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)
    return redirect(url_for("main.home"))