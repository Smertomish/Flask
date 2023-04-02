from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Ищем пользователя с таким же именем в базе данных
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # Если пользователь уже существует, перенаправляем на страницу входа
            return redirect('/login')
        else:
            # Создаем нового пользователя и добавляем его в базу данных
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/home')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Ищем пользователя с таким же именем и паролем в базе данных
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return 'вы успешно вошли'
        else:
            # Если пользователь не найден, выводим сообщение об ошибке
            return 'Неверные данные'
    else:
        return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)