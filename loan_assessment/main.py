# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


approved_loan_path = 'input_files/LoanStats_2017Q3.csv'
rejected_loan_path = 'input_files/RejectStats_2017Q3.csv'

if __name__ == '__main__':
    approved_df = pd.read_csv(approved_loan_path, low_memory=False)
    # rejected_df = pd.read_csv(rejected_loan_path, low_memory=False)

    approved_df = approved_df[
        ['loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'term', 'int_rate', 'installment', 'grade', 'sub_grade',
         'emp_length', 'home_ownership', 'annual_inc', 'issue_d', 'zip_code', 'addr_state', 'dti', 'total_acc', 'inq_last_12m']
    ]

    # print approved_df.columns.values
    # rejected_df = rejected_df[
    #     ['Amount Requested', 'Application Date', 'Loan Title', 'Risk_Score', 'Debt-To-Income Ratio', 'Zip Code',
    #      'State', 'Employment Length', 'Policy Code']
    # ]
    # #
    # rejected = pd.DataFrame()
    # rejected['dti'] = pd.to_numeric(rejected_df['Debt-To-Income Ratio'].str[:-1])
    # rejected['fico'] = rejected_df['Risk_Score']
    # rejected['title'] = rejected_df['Loan Title']
    # rejected['zip_code'] = rejected_df['Zip Code']
    # rejected['amount'] = rejected_df['Amount Requested']
    # rejected['state'] = rejected_df['State']
    # rejected['emp_len'] = rejected_df['Employment Length']
    # rejected['emp'] = pd.factorize(rejected['emp_len'])[0]
    # rejected['zip'] = pd.factorize(rejected['zip_code'])[0]
    # #
    # #
    # rejected['is_null'] = rejected['fico'].isnull()
    # print len(rejected[(rejected['is_null'] == True)]['is_null'])
    # rejected = rejected[(rejected['dti'] <= 10.0)]
    # rejected = rejected[(rejected['fico'] >= 800.0)]
    # rejected = rejected[(rejected['emp_len'] == '10+ years')]
    # rejected = rejected[(rejected['emp'] == 5)]

    print len(approved_df['inq_last_12m'])

    CountStatus = pd.value_counts(approved_df['inq_last_12m'].values, sort=True)
    print CountStatus

    # print stats.mode(approved_df['inq_last_12m']), np.min(approved_df['inq_last_12m']), np.max(approved_df['inq_last_12m']), approved_df['inq_last_12m'].nlargest(10)
    # print rejected[['title', 'amount']]

    # print rejected['emp'], rejected['emp_len']
    # print rejected['title']

    # print rejected['emp_len'][15]

    # fig, ax1 = plt.subplots()
    # x = approved_df['dti']
    # y = approved_df['inq_last_12m']
    # ax1.plot(x, approved_df['fico'], 'bo')
    # plt.show()


    # approved_dti = approved_df['dti']
    # rejected_df['dti'] = pd.to_numeric(rejected_df['Debt-To-Income Ratio'].str[:-1])
    # print np.mean(approved_dti), np.min(approved_dti), np.max(approved_dti), approved_dti.nlargest(10)

    # risk_score = rejected_df[(rejected_df['Risk_Score'] >= 740.00)]['Risk_Score']


    # print len(rejected_df['Risk_Score']), len(rejected_df[(rejected_df['dti'] <= 30.00)]['Risk_Score'])
    # print len(rejected_df['Risk_Score']), len(rejected_df[(rejected_df['Risk_Score'] <= 30.00)]['Risk_Score'])
