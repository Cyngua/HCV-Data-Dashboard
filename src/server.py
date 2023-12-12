from flask import Flask, render_template, request
import pandas as pd

# python3 server.py
df = pd.read_csv('../data/processed_hcvdat.csv')
hcv_data = pd.read_csv("../data/hcvdat0.csv")
hcv_data_json = hcv_data.to_json(orient='records')

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
@app.route('/prediction-results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')

if __name__ == "__main__":
    app.run(debug=True)