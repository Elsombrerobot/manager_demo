from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from manager_demo.models import Role, User
from manager_demo.roles.forms import NewRoleForm, EditRoleForm
from manager_demo.users.utils import admin_required
from manager_demo.db_client import db_roles, db_users

roles = Blueprint("roles", __name__)


@roles.route("/role/new_role", methods=['GET', 'POST'])
@login_required
@admin_required
def new_role():
    form = NewRoleForm()
    if form.validate_on_submit():
        db_roles.create(name = form.name.data.lower(),
                        level = form.level.data,
                        description = form.description.data)
        flash(f'{form.name.data} role has been created !', 'success')
        return redirect(url_for('roles.new_role'))
    return render_template('roles/new_role.html', title='New role', form=form)

@login_required
@admin_required
@roles.route("/role/assign_role", methods=['POST'])
def assign_role():
    role_name = request.args.get("role_name")
    user_id = request.args.get("user_id")
    next_page = request.args.get("next_page")
    user = User.query.get(user_id)
    role = Role.query.filter_by(name=role_name).one_or_none()
    if user and role:
        if role.name not in [role.name for role in user.roles]:
            db_users.assign_role(user, role)
            flash(f'{user.full_name} is now {role.name}.', 'success')
        else:
            flash(f'{user.full_name} is already {role.name}.', 'danger')
    else:
        flash('User or role does not exists.', 'danger')

    return redirect(next_page)

@login_required
@admin_required
@roles.route("/role/remove_role", methods=['POST', 'GET'])
def remove_role():
    role_name = request.args.get("role_name")
    user_id = request.args.get("user_id")
    next_page = request.args.get("next_page")
    user = User.query.get(user_id)
    role = Role.query.filter_by(name=role_name).one_or_none()

    if user and role:
        if role.name in [role.name for role in user.roles]:
            db_users.remove_role(user, role)
            flash(f'{role.name} removed.', 'success')
        else:
            flash(f'{role.name} not in user roles.', 'danger')
    else:
        flash('User or role does not exists.', 'danger')

    return redirect(next_page)

@roles.route("/role/all_roles")
def all_roles():
    roles = Role.query.all()
    return render_template('roles/all_roles.html', title='All Roles', roles=roles)

@roles.route("/role/edit/<int:role_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role(role_id):

    if role_id == 1:
        abort(403)

    role = Role.query.get_or_404(role_id)
    form = EditRoleForm(role=role)
    if form.submit.data and form.validate():
        db_roles.update(role, name=form.name.data,
                              level=form.level.data,
                              description=form.description.data,
                              )
        flash('Role has been updated.', 'success')
        return redirect(url_for('roles.edit_role', role_id=role.id))
    
    if request.method == "GET":
        form.name.data = role.name
        form.level.data = role.level
        form.description.data = role.description
    return render_template("roles/edit_role.html", title="Edit roles", form=form, role=role)

@login_required
@admin_required
@roles.route("/role/delete_role/<string:role_id>", methods=['POST'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db_roles.delete(role)
        flash(f'{role.name} deleted.', 'success')
    else:
        flash('Role does not exists.', 'danger')
    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)
    return redirect(url_for("main.home"))