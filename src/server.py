from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import matplotlib.pyplot as plt
import json

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

# python3 server.py
df = pd.read_csv('../data/processed_hcvdat.csv')
hcv_data = pd.read_csv("../data/hcvdat0.csv")
hcv_data_json = hcv_data.to_json(orient='records')

def model_training(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    return model, cm

def normalize_columns(features):
    return (features - features.mean()) / features.std()

app = Flask(__name__)

# homepage
@app.route("/")
def index():
    return render_template("layout.html")

# data overview
@app.route('/overview', methods=['GET', 'POST'])
def overview():
    num_rows = 5
    if request.method == 'POST' or request.args.get('rowSelection'):
        num_rows_param = request.form.get('rowSelection') or request.args.get('rowSelection')
        # Display selected number of rows
        num_rows = int(num_rows_param)
    data_for_overview = hcv_data.iloc[:num_rows, :]
    return render_template('overview.html', data = data_for_overview)

# data exploration
@app.route('/data-exploration', methods=['GET', 'POST'])
def explore():
    return render_template('exploration.html', hcv_data_json = hcv_data_json)

# prediction results
@app.route('/run-model', methods=['GET', 'POST'])
def run_model():
    data = request.json
    selected_model = data.get('model')
    parameters = data.get('parameters')

    # model training
    y = df['Category']
    X = df.iloc[:, :-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # normalize
    X_train.iloc[:, X_train.columns!='Sex'] = normalize_columns(X_train.iloc[:, X_train.columns!='Sex'])
    X_test.iloc[:, X_test.columns!='Sex'] = normalize_columns(X_test.iloc[:, X_test.columns!='Sex'])

    try:
        # convert parameter type
        for key, value in parameters.items():
            try:
                # Convert the string value to an integer
                parameters[key] = int(value)
            except ValueError:
                # Handle the case if the value is not convertible to an integer
                pass
        parameters_dict = json.loads(json.dumps(parameters))

        if selected_model == "XGB":
            model_xgb = xgb.XGBClassifier()
            model_xgb.set_params(**parameters_dict)
            model_xgb, cm = model_training(model_xgb, X_train, y_train, X_test, y_test)
        elif selected_model == "DT":
            model_rf = RandomForestClassifier()
            model_rf.set_params(**parameters_dict)
            model_rf, cm = model_training(model_rf, X_train, y_train, X_test, y_test)
        
        # plot out confusion matrix
        cmd = ConfusionMatrixDisplay(cm)
        cmd.plot()
        plt.title('Confusion Matrix (Random Forest)')
        plt.tight_layout()
        plt.savefig('static/confusion_matrix_run.png')
        plt.close()
        image_url = url_for('static', filename='confusion_matrix_run.png')

        response = {'message': 'ML model processed successfully', 'image_url': image_url}
        return json.dumps(response), 200
    except:
        return json.dumps({'error': 'State not found'}), 404

@app.route('/results')
def results():
    json_file, code = run_model()
    if code == 200:
        value = json.loads(json_file)
        query = value.get('image_url')
        return render_template('result.html', image_url=query)
    return render_template('result.html', image_url=None)

if __name__ == "__main__":
    app.run(debug=True)
