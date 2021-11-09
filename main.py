import fitz  # this is pymupdf
from os import listdir
from os.path import isfile, join
import pandas as pd
from data_scraper import gather_pay_data

# PDF files are located in the 2021 folder for now. 
# We need to get the filenames for looping through
LES_PATH = "2021"
LES_FILES = [f for f in listdir(LES_PATH) if isfile(join(LES_PATH, f))]
# Columns for the main DataFrame. 
# If columns are added here, add them to the append statement too!
DATA_COLUMNS = [
    'pp_end_date', 'pp_pay_date', 'base_pay', 'ot_rate', 'tsp_pct', 'gross_pay', 'net_pay', 
    'ytd_gross', 'ytd_net', 'ot_hrs', 'extra_pay', 'medicare', 'union', 'fed_tax', 'tsp', 'fehb',
    'oasdi', 'fers', 'state_tax']

# Main dataframe to hold LES info will be data
data = pd.DataFrame(columns=DATA_COLUMNS)
# Function to get our LES data
data = gather_pay_data(LES_PATH, LES_FILES, data)

data.set_index(['pp_end_date'], inplace=True)
data_sorted_by_max_gross = data.sort_values(['gross_pay'], ascending=False)
print(data)
print(f'Max pay was PP ending {data_sorted_by_max_gross.index[0]} \
    at ${data_sorted_by_max_gross["gross_pay"].iloc[0]}')
