import datetime
import numpy as np
import pandas as pd
import requests

count = 0
time_stamp= datetime.datetime.now()
time_stamp_str = str(time_stamp.strftime("%I_%M_%p__%d_%b_%Y"))
columns = ['Name', 'ImagePath', 'Category', 'SubCategory', 'KVAT', 'GstRate', 'HsnCode', 'DailyPrice', 'Unit']


r = requests.post("http://wotu.in/api/product/productcatalogdetailsforweb", data={"PageNo":1,"PaginationRecordCount":1200})
print(r.status_code, r.reason)
data = r.json()

print "Product count: ", data['TotalCount']
print  len(data['ProductCatalogDetails'])

required_fields = ['Name', 'ImagePath', 'CategoryNames', 'KVAT', 'GstRate', 'HsnCode', 'DailyPrice', 'Unit']

table_data = [{k: datum[k] for k in required_fields} for datum in data['ProductCatalogDetails']]

for t in table_data:
    if len(t['CategoryNames']) > 0:
        t['Category'] = t['CategoryNames'][0]
    else:
        t['Category'] = ''
    if len(t['CategoryNames']) > 1:
        t['SubCategory'] = t['CategoryNames'][1]
    else:
        t['SubCategory'] = ''
    del t['CategoryNames']

final_data = []
for t in table_data:
    final_data.append([t[k] for k in columns])

writer = pd.ExcelWriter(
        '/Users/abhishek/Desktop/wotu - ' + time_stamp_str + '.xlsx',
        engine='openpyxl')

df = pd.DataFrame(np.array(final_data), columns=columns)
df.to_excel(writer, 'Item List')
writer.save()
print "Done"
#