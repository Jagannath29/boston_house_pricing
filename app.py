import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

# load model 
reg_model = pickle.load(open("regmodel.pkl", 'rb'))
# load model 
reg_model = pickle.load(open("regmodel.pkl", 'rb'))
scalar = pickle.load(open("scaling.pkl", 'rb'))


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output=reg_model.predict(new_data)
    print(output[0])
    return jsonify(output[0])



@app.route('/predict',methods=['POST'])
def predict():
    try:
        data = [float(x) for x in request.form.values()]
        final_input = scalar.transform(np.array(data).reshape(1,-1))
        output = reg_model.predict(final_input)[0]
        # Format the prediction with comma separator and 2 decimal places
        formatted_price = "${:,.2f}k".format(output)
        return render_template("home.html", 
                             prediction_text=f"Predicted House Price: {formatted_price}")
    except Exception as e:
        return render_template("home.html", 
                             prediction_text="Error: Please ensure all fields contain valid numbers.")


if __name__ == "__main__":
    app.run(debug=True)