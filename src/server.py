from flask import Flask, render_template, request
import pandas as pd
import plotly
import plotly.express as px

# python3 server.py
df = pd.read_csv('../data/processed_hcvdat.csv')
hcv_data = pd.read_csv("../data/hcvdat0.csv")

app = Flask(__name__)

# homepage
@app.route("/")
def index():
    return render_template("layout.html")

# data overview
@app.route('/overview', methods=['GET', 'POST'])
def overview():
    # Default number of rows to display
    num_rows = 5

    if request.method == 'POST' or request.args.get('rowSelection'):
        num_rows_param = request.form.get('rowSelection') or request.args.get('rowSelection')
        # Display selected number of rows
        num_rows = int(num_rows_param)
    
    data_for_overview = hcv_data.iloc[:num_rows, :]
    return render_template('overview.html', data = data_for_overview)

# data exploration
@app.route('/overview', methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(debug=True)