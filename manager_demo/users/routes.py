from flask import Blueprint, abort
from flask import render_template, url_for, flash, redirect, request
from manager_demo.users.forms import (EditUserForm, NewUserForm, LoginForm, UserProjectForm, UserRoleForm)
from manager_demo import bcrypt
from manager_demo.models import Role, User, Project
from manager_demo.users.utils import admin_required, delete_picture, generate_email, generate_password, generate_profile_picture, hash_password, save_picture
from flask_login import login_user, logout_user, login_required
from manager_demo.db_client import db_users


users = Blueprint("users", __name__)

@users.route("/user/new_user", methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        email = generate_email(form.first_name.data, form.last_name.data)
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f'{form.first_name.data} {form.last_name.data} already registered.', 'danger')
            return render_template('users/new_user.html', title='New user', form=form)
        hashed_password = generate_password(form.first_name.data, form.last_name.data)
        image_file = generate_profile_picture((form.first_name.data[0] + form.last_name.data[0]).upper())
        db_users.create(first_name=form.first_name.data.capitalize(),
                        last_name=form.last_name.data.capitalize(),
                        email=email, password=hashed_password, image_file=image_file)
        flash('User has been created !', 'success')
        return redirect(url_for('users.new_user'))
    return render_template('users/new_user.html', title='New user', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            logout_user()
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/user/all_users")
def all_users():
    users = User.query.all()
    return render_template('users/all_users.html', title='All users', users=users)

@users.route("/user/edit/<int:user_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    
    if user_id == 5:
        abort(403)

    #Update form
    user = User.query.get_or_404(user_id)
    form = EditUserForm()
    
    if request.form.get('image_reset'):
        delete_picture(user.image_file)
        image_file = generate_profile_picture((user.first_name[0] + user.last_name[0]))
        db_users.update(user, image_file=image_file)
        flash('Profile image has been updated!', 'success')
        return redirect(url_for('users.edit_user', user_id=user_id))
    
    if form.submit_update.data and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            delete_picture(user.image_file)
            db_users.update(user, image_file=picture_file)
        password = hash_password(form.password.data) if form.password.data else None
        db_users.update(user, first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              email=form.email.data,
                              password=password)
        flash('User has been updated.', 'success')
        return redirect(url_for('users.edit_user', user_id=user_id))

    #Project form
    projects = Project.query.all()
    user_project_form = UserProjectForm()
    user_project_form.project.choices = [project.title for project in projects]


    if user_project_form.submit_project.data:
        return redirect(url_for('projects.assign_project',
                        next_page=url_for('users.edit_user',user_id=user.id),
                        project_title=user_project_form.project.data
                        ,user_id=user.id),code=307)

    #Role form
    roles = Role.query.all()
    user_role_form = UserRoleForm()
    user_role_form.role.choices = [role.name for role in roles]

    if user_role_form.submit_role.data:
        return redirect(url_for('roles.assign_role',
                        next_page=url_for('users.edit_user',user_id=user.id),
                        role_name=user_role_form.role.data,
                        user_id=user.id),code=307)

    if request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        
    return render_template("users/edit_user.html",
                            title="Edit user",
                            form=form,
                            user=user,
                            roles=roles,
                            projects=projects,
                            user_role_form=user_role_form,
                            user_project_form=user_project_form)

@login_required
@admin_required
@users.route("/user/delete_user/<string:user_id>", methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db_users.delete(user)
        flash(f'{user.full_name} deleted.', 'success')
    else:
        flash('User does not exists.', 'danger')
    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)
    return redirect(url_for("main.home"))