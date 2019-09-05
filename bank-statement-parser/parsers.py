import os
import csv
import tabula
from util import *
import numpy as np
import math
import csv



# reading table using tabula
rows = tabula.read_pdf('/Users/abhishek/Desktop/bs.pdf',
                       pages='all',
                       silent=True,
                       pandas_options={
                           'header': None,
                           'error_bad_lines': False,
                           'warn_bad_lines': False
                       })
# converting to list
rows = rows.values.tolist()

transactions = []  # list to store single row entries

d_i = BANK_DETAILS['HDFC']['date']
p_i = BANK_DETAILS['HDFC']['particulars']

# iterate over all transactions
for i, v_t in enumerate(rows):
    print i, v_t[d_i]
    if not is_nan(v_t[d_i]):
        transactions.append(v_t)
    else:
        transactions[-1][p_i] += str(v_t[p_i])

with open('/Users/abhishek/Desktop/bs.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerows(transactions)

