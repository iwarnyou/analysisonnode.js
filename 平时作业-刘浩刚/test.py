import requests # 数据请求
import pandas as pd
from pyecharts.charts import *
import LogisticRegression

# 发送请求的url地址
url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice'

params = {
    'name': 'ssq',
    'issueCount': '',
    'issueStart': '',
    'issueEnd': '',
    'dayStart': '2017-10-24',
    'dayEnd': '2021-08-04',

}
headers = {
    'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
result = requests.get(url=url, params=params, headers=headers)
# <> 对象 200 请求成功  状态码
for i in result:
    dit = {
        '期号': i['code'],
        '开奖日期': i['date'],
        '红球': i['red'],
        '蓝球': i['blue'],
        '一等奖中奖注数': i['prizegrades'][0]['typenum'],
        '一等奖中奖金额': i['prizegrades'][0]['typemoney'],
        '二等奖中奖注数': i['prizegrades'][1]['typenum'],
        '二等奖中奖金额': i['prizegrades'][1]['typemoney'],
        '三等奖中奖注数': i['prizegrades'][2]['typenum'],
        '三等奖中奖金额': i['prizegrades'][2]['typemoney'],
        '四等奖中奖注数': i['prizegrades'][3]['typenum'],
        '四等奖中奖金额': i['prizegrades'][3]['typemoney'],
        '五等奖中奖注数': i['prizegrades'][4]['typenum'],
        '五等奖中奖金额': i['prizegrades'][4]['typemoney'],
        '六等奖中奖注数': i['prizegrades'][5]['typenum'],
        '六等奖中奖金额': i['prizegrades'][5]['typemoney'],
        '一等奖中奖地区': i['content'],
        '奖池金额': i['poolmoney']
    }
import csv # 内置模块

f = open('双色球.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['期号',
                                '开奖日期',
                                '红球',
                                '蓝球',
                                '一等奖中奖注数',
                                '一等奖中奖金额',
                                '二等奖中奖注数',
                                '二等奖中奖金额',
                                '三等奖中奖注数',
                                '三等奖中奖金额',
                                '四等奖中奖注数',
                                '四等奖中奖金额',
                                '五等奖中奖注数',
                                '五等奖中奖金额',
                                '六等奖中奖注数',
                                '六等奖中奖金额',
                                '一等奖中奖地区',
                                '奖池金额'])

csv_writer.writeheader() # 写入表头
csv_writer.writerow(dit)
print(dit)


data = pd.read_csv('双色球.csv',encoding='utf-8', engine='python')
data.head()

def get_lotto_data(data, lotto, lotto_id):
    data['lotto_id'] = lotto_id
    X = []
    Y = []
    # 标签and值
    for s, p in zip(data['lotto_id'], data[lotto]):
        X.append([float(s)])
        Y.append(float(p))
    return X, Y


def linear_model_test(X, Y, predict_value):
    regr = LogisticRegression()
    regr.fit(X, Y)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions



def get_predicted_num(file, lotto, lotto_id):
    X, Y = get_lotto_data(file, lotto, lotto_id)
    predict_value = [[33]]
    result = linear_model_test(X, Y, predict_value)
    if lotto_id < 7:
        print(f'中奖第{lotto_id}个红球为：', result['predicted_value'].astype('int64'), '号球')
    else:
        print('中奖蓝球为：', result['predicted_value'].astype('int64'), '号球')


get_predicted_num(data, 'r1', 1)  # 预测红1
get_predicted_num(data, 'r2', 2)  # 预测红2
get_predicted_num(data, 'r3', 3)  # 预测红3
get_predicted_num(data, 'r4', 4)  # 预测红4
get_predicted_num(data, 'r5', 5)  # 预测红5
get_predicted_num(data, 'r6', 6)  # 预测红6
get_predicted_num(data, '蓝球', 7)  # 预测蓝7
