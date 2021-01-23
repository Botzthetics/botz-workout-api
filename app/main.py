from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///botzletics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)  # new


##CONFIGURE TABLE
class BotzleticsDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)


db.create_all()


class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "date")



workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


@app.route('/')
def get_all_workouts():
    workouts = BotzleticsDb.query.all()
    return jsonify(workouts_schema.dump(workouts))

@app.route("/workout/<int:workout_id>")
def get_workout(workout_id):
    if BotzleticsDb.query.get(workout_id):
        workout = BotzleticsDb.query.get(workout_id)
        return jsonify(workout_schema.dump(workout))
    else:
        abort(404)


@app.route("/new-workout", methods=["POST"])
def add_new_workout():
    req_data = request.get_json()
    workout = BotzleticsDb(
        name=req_data['name'],
        date=date.today().strftime("%B %d, %Y")
    )
    db.session.add(workout)
    db.session.commit()
    return 'Submitted'

@app.errorhandler(404)
def page_not_found(error):
   return {'message' : 'Ruh Roh'}


# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# def edit_post(post_id):
#     post = BotzleticsDb.query.get(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = edit_form.author.data
#         post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))
#     return render_template("make-post.html", form=edit_form, is_edit=True)


# @app.route("/delete/<int:post_id>")
# def delete_post(post_id):
#     post_to_delete = BotzleticsDb.query.get(post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
