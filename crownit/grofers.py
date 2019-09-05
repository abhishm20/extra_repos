import urllib2
import json
import datetime
import numpy as np
import pandas as pd


cities = [(26167, "New Delhi"),
          (26238, "Mumbai"),
          (26015, "Bengaluru"),
          (26688, "Pune"),
          (26523, "Jaipur"),
          (26782, "Chennai"),
          (28357, "Hyderabad"),
          (25568, "Kolkata"),
          (26528, "Lucknow"),
          (26391, "Ahmedabad"),
          (26171, "Gurgaon-Faridabad"),
          (26511, "Noida-GZB"),
          (27860, "Kochi"),
          (27852, "Bhubaneswar"),
          (28521, "Indore"),
          (27850, "Bhopal"),
          (27364, "Kanpur")]

request_headers = {
    "auth_key": "299b416b842223533b30636b82e520b1dd91df5d8e09ecb7670a1d53f230db1f",
    "app_client": "customer_web"
}

columns = ['Category', 'Sub Category 1', 'Sub Category 2', 'Brand', 'Product Name', 'MRP', 'Price', 'Size/Quantity']
categories = [9, 16, 12, 1047, 18, 163, 14, 13, 15, 972, 7, 650, 5, 4, 343]

final_data = []

for cc, cn in cities:
    for category in categories:
        request = urllib2.Request("https://grofers.com/v4/search/merchants/%s/products/?l0_cat=%s&start=0&next=2000" % (str(cc), str(category)), headers=request_headers)
        content = urllib2.urlopen(request).read()
        result = json.loads(content)['result']['products']
        print len(result)
        for r in result:
            print category, r['level0_category'][0]['name'], r['name']
            sub_category1 = ''
            if r['level1_category'] and 'name' in r['level1_category'][0]:
                sub_category1 = r['level1_category'][0]['name']

            sub_category2 = ''
            if r['subcategories'] and 'name' in r['subcategories'][0]:
                sub_category2 = r['subcategories'][0]['name']
            final_data.append([
                r['level0_category'][0]['name'],
                sub_category1,
                sub_category2,
                r['brand'],
                r['name'],
                r['mrp'],
                r['price'],
                r['unit']
            ])


    writer = pd.ExcelWriter(
            '/Users/abhishek/Desktop/grofers/'+cn+'.xlsx',
            engine='openpyxl')

    df = pd.DataFrame(np.array(final_data), columns=columns)
    df.to_excel(writer, 'Item List')
    writer.save()
    print "Done"