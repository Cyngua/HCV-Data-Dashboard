from flask import Flask, render_template, request, jsonify, url_for, send_file
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import matplotlib
import time
matplotlib.use('Agg')

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

# python3 server.py
df = pd.read_csv('../data/processed_hcvdat.csv')
df.drop(columns = ['Unnamed: 0'], inplace = True)
hcv_data = pd.read_csv("../data/hcvdat0.csv")
hcv_data_json = hcv_data.to_json(orient='records')

def normalize_columns(features):
    return (features - features.mean()) / features.std()

app = Flask(__name__, static_folder='/Users/cynthia/Desktop/BIS634_CMHI/BIS634 Final')

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
    print(parameters)

    # model training
    y = df['Category']
    X = df.iloc[:, :-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    # normalize
    X_train.iloc[:, X_train.columns!='Sex'] = normalize_columns(X_train.iloc[:, X_train.columns!='Sex'])
    X_test.iloc[:, X_test.columns!='Sex'] = normalize_columns(X_test.iloc[:, X_test.columns!='Sex'])
    # convert parameter type
    parameters_dict = {}
    for key, value in parameters.items():
        try:
            # Convert the string value to numerical
            parameters_dict[key] = int(value)
        except ValueError:
            parameters_dict[key] = float(value)
            

    model_name = 'NA'
    if selected_model == "XGB":
        model_xgb = xgb.XGBClassifier()
        model_name = 'XGBoost'
        model_xgb.set_params(**parameters_dict)
        model_xgb.fit(X_train, y_train)
        y_pred = model_xgb.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
    elif selected_model == "DT":
        model_rf = RandomForestClassifier()
        model_name = 'Random Forest'
        model_rf.set_params(**parameters_dict)
        model_rf.fit(X_train, y_train)
        y_pred = model_rf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
    
    # plot out confusion matrix
    cmd = ConfusionMatrixDisplay(cm)
    cmd.plot()
    plt.title(f'Confusion Matrix ({model_name})')
    plt.tight_layout()
    filename = f"confusion_matrix_{int(time.time())}.png"  # Unique filename using a timestamp
    plt.savefig(f"../figures/{filename}")
    image_url = url_for('static', filename=f'figures/{filename}')
    plt.close()
    return json.dumps({'image_url': image_url})

@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)
