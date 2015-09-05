import os
from flask import logging, Flask, render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Email
import sys, logging
from flask.ext.bootstrap import Bootstrap
from NameExtract import NamaeWa
import gzip

extractor = NamaeWa()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


class SimpleForm(Form):
    email = StringField('Email address', validators=[Email()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    email = None
    form = SimpleForm()
    best_guess = None

    if form.validate_on_submit():
        email = form.email.data
        best_guess = extractor.extract_name(email)

    return render_template('index.html', form=form, email=email, best_guess=best_guess)


@app.before_first_request
def load_word_list():
    f = gzip.open('static/names.pklzip', 'rb')
    extractor.build_map(f)
    f.close()



if __name__ == '__main__':
    app.run()
