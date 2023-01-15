from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    link = request.form['link']
    # the link is then passed to the ML Code which returns an output stored in a variable
    # this variable x will be put inside prediction = x
    return render_template('predict.html', prediction = link)

if __name__ == '__main__':
    app.run()