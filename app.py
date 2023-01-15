from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    prediction = request.form.to_dict() 
    # empty not working right now
    print(prediction)
    return render_template('predict.html', prediction = prediction)

if __name__ == '__main__':
    app.run()