from datetime import datetime

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from task2 import Document
from forms import MakeOrderForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8kliljijkj,lkhoihui'
csrf = CSRFProtect(app)


def get_length(text) -> int:
    sum = 0
    for word in text.split(' '):
        sum += len(word)
    return sum


def calculate(text, language):
    content = {}
    length = get_length(text)
    doc = Document('docx', length, language)
    content['price'] = doc.calculate_price()
    content['ex_time'] = doc.calculate_time()
    content['deadline'] = doc.calculate_deadline(datetime.now(), content['ex_time'])
    return content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/order/', methods=['GET', 'POST'])
def order():
    form = MakeOrderForm()
    if form.validate_on_submit():
        text = form.text.data
        language = form.lang.data
        print(text, language)
        content = calculate(text, int(language))
        return render_template('make_order.html',
                               price=content['price'],
                               ex_time=content['ex_time'],
                               deadline=content['deadline'],
                               form=form)
    return render_template('make_order.html', form=form)


if __name__ == '__main__':
    app.run()


