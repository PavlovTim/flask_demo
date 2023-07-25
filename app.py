import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import User, Idea, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/users', methods=['GET'])
def show_users():
    return render_template("users.html", users=User.query.all())


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        new_user = User(first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("show_users"))
    return render_template('create_user.html')


@app.route('/show_ideas/<user_id>')
def show_user_ideas(user_id):
    user = User.query.get(user_id)
    return render_template("user_ideas.html", ideas=user.ideas)

@app.route('/add_idea/<user_id>', methods=['GET', 'POST'])
def add_idea(user_id):
    def get_idea(user_id):
        idea_ = requests.get("https://www.boredapi.com/api/activity").json()

        requests.post(f"http://127.0.0.1:5000/add_idea/{user_id}", data=idea_)

    if request.method == 'POST':
        idea = {}
        for key, value in request.form.items():
            idea[key] = value
        new_idea = Idea(
            activity=idea['activity'],
            type=idea['type'],
            participants=int(idea['participants']),
            price=float(idea['price']),
            link=idea['link'],
            key=int(idea['key']),
            accessibility=float(idea['accessibility']),
            user_id=user_id
        )
        db.session.add(new_idea)
        db.session.commit()
        return {"status": 200}
    else:
        get_idea(user_id)
        return redirect(url_for("show_user_ideas", user_id=user_id))


if __name__ == '__main__':
    app.run()
