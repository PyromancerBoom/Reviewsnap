from flask import Flask, render_template, request
import pickle

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


model = pickle.load(open('ReviewSnap.py', 'rb'))


@app.route('/predict', methods=['POST'])
def predict():
    link = request.form['link']
    # the link is then passed to the ML Code which returns an output stored in a variable
    # this variable x will be put inside prediction = x
    prediction = model.predict(link)
    return render_template('predict.html', prediction=link)


if __name__ == '__main__':
    app.run()
