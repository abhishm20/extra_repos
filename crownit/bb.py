import urllib2
import json
import datetime
import numpy as np
import pandas as pd
import json
from pprint import pprint


with open('cat_big.json') as data_file:
    data = json.loads(json.load(data_file))
    categories = data['topcats']

request_headers = {
    "Cookie": '_bb_tc=0; _bb_rdt="MzE1MTU0MzQ2NA==.0"; _bb_vid="Mjg3MTM2Mzk1Mg=="; _bb_cid=1; sessionid=295a2fc410b32636ab8afd3df692420e; ts="2017-08-01 17:05:24.728"; _bb_rd=6',
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

columns = ['Category', 'Sub Category 1', 'Sub Category 2', 'Brand', 'Product Name', 'MRP', 'Price', 'Size/Quantity', 'Packaging Type']

final_data = []

for category in categories:
    category_name = category['top_category']['name']
    for sub1 in category['sub_cats'][0]:
        sub_category1_name = sub1['sub_category'][0]
        for sub2 in sub1['cats']:
            sub2 = sub2['cat']
            sub_category2_name = sub2[0]
            url_name = sub2[1]
            print category_name, sub_category1_name, sub_category2_name, url_name

            request = urllib2.Request("https://www.bigbasket.com/custompage/sysgenpd/?slug=" + url_name + "&type=pc",
                                      headers=request_headers)
            content = urllib2.urlopen(request).read()
            try:
                header = json.loads(content)
            except:
                continue
            if 'header_section' in header['tab_info'][0]:
                item_count = header['tab_info'][0]['header_section']['items'][0]['count']
            else:
                print "Not Found", url_name
                break
            page_count = (item_count // 20) + 1
            for page in range(page_count):
                request = urllib2.Request("https://www.bigbasket.com/product/get-products/?slug="+url_name+"&page="+str(page)+"&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc", headers=request_headers)
                content = urllib2.urlopen(request).read()
                try:
                    result = json.loads(content)['tab_info']['product_map']['all']['prods']
                except:
                    continue
                for r in result:
                    print '------------------',r['p_desc']
                    final_data.append([
                        category_name,
                        sub_category1_name,
                        sub_category2_name,
                        r['p_brand'],
                        r['p_desc'],
                        r['mrp'],
                        r['sp'],
                        r['w'],
                        r['pack_desc']
                    ])


writer = pd.ExcelWriter(
        '/Users/abhishek/Desktop/bb.xlsx',
        engine='openpyxl')

df = pd.DataFrame(np.array(final_data), columns=columns)
df.to_excel(writer, 'Item List')
writer.save()
print "Done"