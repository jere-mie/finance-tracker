from flask import render_template, url_for, flash, redirect, request
from website import app, db
from website.forms import Registration, Login, AddExpense, AddGoal
from website.models import User, Expense, Goal
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    total=0.0
    remaining=100
    bg='warning'
    status='N/A'
    if current_user.is_authenticated:
        if current_user.expenses:
            for expense in current_user.expenses:
                total+=expense.price
        remaining = round(((current_user.income - total)/current_user.income)*100)
    if remaining >=66:
        bg='success'
        status='Very Good'
    elif remaining <=33:
        bg='danger'
        status='Not Good'
    else:
        bg='warning'
        status='Ok'
    if remaining<0:
        remaining = 0
    return render_template('home.html', total=total, remaining=remaining, bg=bg, status=status)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, income=form.income.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Created account for {form.username.data}. You may now log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and form.password.data==user.password:
            login_user(user, remember=form.rememberMe.data)
            return redirect(url_for('home'))
        else:
            flash('Error Logging In', 'danger')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = AddExpense()
    if form.validate_on_submit():
        expense = Expense(name=form.name.data, description=form.description.data, owner=current_user, price=round(form.price.data,2))
        db.session.add(expense)
        db.session.commit()
        flash('You have successfully added a transaction!', 'success')
        return redirect(url_for("home"))
    return render_template("new.html", form=form, legend='Add an Expense')

@app.route('/expense/<expense_id>/delete', methods=['GET','POST'])
@login_required
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.owner!=current_user:
        flash('You cannot delete someone else\'s expense!', 'danger')
        return redirect(url_for('home'))
    db.session.delete(expense)
    db.session.commit()
    flash('Successfully deleted expense!', 'success')
    return redirect(url_for('home'))


@app.route('/expense/<expense_id>/update', methods=['GET', 'POST'])
@login_required
def update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.owner!=current_user:
        flash('You cannot update someone else\'s expense!', 'danger')
        return redirect(url_for('home'))
    form = AddExpense()
    
    if form.validate_on_submit():
        expense.name = form.name.data
        expense.description = form.description.data
        expense.price = round(form.price.data,2)
        db.session.commit()
        flash('You have successfully updated the expense!', 'success')
        return redirect(url_for("home"))
    elif request.method == 'GET':
        form.name.data = expense.name
        form.description.data = expense.description
        form.price.data = expense.price
    return render_template("new.html", form=form, legend='Update Expense')

@app.route('/expense/<expense_id>', methods=['GET', 'POST'])
def see(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.owner != current_user:
        return redirect(url_for('home'))
    return render_template('expense.html', expense=expense)



@app.route('/newGoal', methods=['GET', 'POST'])
@login_required
def newGoal():
    form = AddGoal()
    if form.validate_on_submit():
        goal = Goal(description=form.description.data, author=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('You have successfully added a goal!', 'success')
        return redirect(url_for("home"))
    return render_template("newGoal.html", form=form, legend='Add a Goal')

@app.route('/goal/<goal_id>/delete', methods=['GET','POST'])
@login_required
def deleteGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.author!=current_user:
        flash('You cannot delete someone else\'s goal!', 'danger')
        return redirect(url_for('home'))
    db.session.delete(goal)
    db.session.commit()
    flash('Successfully deleted goal!', 'success')
    return redirect(url_for('home'))


@app.route('/goal/<goal_id>/update', methods=['GET', 'POST'])
@login_required
def updateGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.author!=current_user:
        flash('You cannot update someone else\'s goal!', 'danger')
        return redirect(url_for('home'))
    form = AddGoal()
    
    if form.validate_on_submit():
        goal.description = form.description.data
        goal.completed = form.completed.data
        db.session.commit()
        flash('You have successfully updated the expense!', 'success')
        return redirect(url_for("home"))
    elif request.method == 'GET':
        form.description.data = goal.description
        form.completed.data = goal.completed
    return render_template("newGoal.html", form=form, legend='Update Goal')

@app.route('/goal/<goal_id>', methods=['GET', 'POST'])
def seeGoal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.author != current_user:
        return redirect(url_for('home'))
    return render_template('goal.html', goal=goal)