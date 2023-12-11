import pandas as pd
from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
hcv_data = pd.read_csv("../data/hcvdat0.csv")
hcv_data.drop(columns = ['Unnamed: 0'], inplace = True)

html_table = hcv_data.to_html()
with open('templates/table.html', 'w') as f:
    f.write(f''' 
        {html_table}
    ''')