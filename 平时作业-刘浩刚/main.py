import requests
from urllib.parse import urlencode
import pandas as pd
import re
from pyecharts import options as opts
from pyecharts.charts import Geo
from sklearn import linear_model

url = 'http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?'   # 爬取网站

params = {
    'name': 'ssq',
    'issueCount': '1000',
    'issueStart':'',
    'issueEnd': '',
    'dayStart': '',
    'dayEnd': '',
}

url = url+urlencode(params)         #url＋params的url编码
resp = requests.get(url)            #爬取数据
#print(resp.json())


#数据处理：
codes,sales,loc_nums,r1,r2,r3,r4,r5,r6,b1= [[] for i in range(10)]
#分别为期号，销售额，地区与中奖数键值队，红球第n个号码和篮球号码
for ssq in resp.json()['result']:
    code = ssq['code']      #双色球编号
    codes.append(code)

    sale = ssq['sales']     #总销量
    sales.append(sale)

    content = ssq['content'].replace('注','')  #字符串处理
    tam = content.find('其')            #删去后缀多余部分
    if tam!=-1 :
        content = content[ : tam]
    content = content.split(',')       #按地区分割
    content = content[:-1]             #删掉末尾统计数据
    loc=[]                             #将地区与中奖个数分割
    num=[]
    loc_num = {}
    for x in content :
        loc.append(re.sub(r'[0-9]+','',x))     #用空格替换数字部分保留地区名
        num.append(re.sub(u'[^0-9]+','',x))    #用空格替换非数字部分
    for key,value in zip(loc,num):
        loc_num[key]=value
    loc_nums.append(loc_num)
    # 红球号码
    red=ssq['red'].split(',')
    r1.append(int(red[0]))
    r2.append(int(red[1]))
    r3.append(int(red[2]))
    r4.append(int(red[3]))
    r5.append(int(red[4]))
    r6.append(int(red[5]))
    # 篮球号码
    blue=ssq['blue']
    b1.append(int(blue))

#创建字典为创建多维表做准备
dic = {'codes':codes,'sales':sales,'r1':r1,'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'b1':b1,'loc_nums':loc_nums}
frame = pd.DataFrame(dic)
#将数据储存到CSV文件
frame.to_csv('./ssq.csv')

print(frame)



# 统计各地区中奖数字和：
loc_nums_sum={}
for x in loc_nums:
    for k in x.keys():
        if(k not in loc_nums_sum.keys()):
            loc_nums_sum[k]=0
        loc_nums_sum[k]=loc_nums_sum[k]+int(x[k])

print(loc_nums_sum)

#将字典转为列表便于绘图：
loc_nums_sums=[]
for key,value in loc_nums_sum.items():
    loc_nums_sums.append((key,value))
print(loc_nums_sums)




#以100为单位设置不同颜色分段显示
pieces = [
        {'max': 0, 'label': '0以下', 'color': '#50A3BA'},
        {'min': 1, 'max': 100, 'label': '1-10', 'color': '#3700A4'},
        {'min': 101, 'max': 200, 'label': '72-74', 'color': '	#FF0000'},     #红色
        {'min': 201, 'max': 300, 'label': '110-112', 'color': '#FF8C00'},  #橙色
        {'min': 301, 'max': 400, 'label': '30-50', 'color': '#FCF84D'},
        {'min': 401, 'max': 500, 'label': '50-100', 'color': '#DD0200'},
        {'min':501, 'max': 800, 'label': '150-155', 'color': '#00CED1'},   #绿色
        {'min':801, 'max': 1000, 'label': '190-192', 'color': '#0000FF'}   #  蓝色
    ]

#制图方法：
def create_china_map():
    (
        #初始化地图并设置地图大小
        Geo(init_opts=opts.InitOpts(width="1980px", height="900px"))
        # 选择中国地图模板
        .add_schema(maptype='china')
        # 设置系列名称和数据项
        .add(

            series_name='中奖数量',  #点类名
            data_pair=loc_nums_sums,   #数据
            symbol_size=20        #点大小

        )

        # 将标签名称显示为省名称
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True,formatter='{b}'))
        # 全局配置项
        .set_global_opts(
            # 设置标题
            title_opts=opts.TitleOpts(title="中国福利彩票双色球近1000期各省中奖数量"),

            #设置视觉配置项分段显示
            visualmap_opts=opts.VisualMapOpts(
                 pieces=pieces,
                 is_piecewise=True,
                 is_show=True
            )
        )
        # 生成本地html文件
        .render("中国福利彩票双色球近1000期各省中奖数量.html")
    )

create_china_map()



#处理数据并获取x和y，x为第几个号码，y为号码
def get_lotto_data(data, lotto, lotto_id):
    data['lotto_id'] = lotto_id
    X = []
    Y = []
    # single_square_feet, single_price_value
    for s, p in zip(data['lotto_id'], data[lotto]):
        X.append([float(s)])
        Y.append(float(p))
    return X, Y


#建立线性模型
def linear_model_test(X, Y, predict_value):
    regr = linear_model.LinearRegression()   #调用线性模型库函数
    regr.fit(X, Y)                           #传入x和y
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_    #截距
    predictions['coefficient'] = regr.coef_       #回归系数
    predictions['predicted_value'] = predict_outcome
    return predictions



#预测函数：
def get_predicted_num(file, lotto, lotto_id):

    X, Y = get_lotto_data(file, lotto, lotto_id)
    #print(X)
    #print(Y)
    predict_value = [[33]]
    result = linear_model_test(X, Y, predict_value)
    if lotto_id < 7:
        print(f'中奖第{lotto_id}个红球为：', result['predicted_value'].astype('int64'), '号球')
    else:
        print('中奖蓝球为：', result['predicted_value'].astype('int64'), '号球')



df =frame
# 使用线性回归模型进行预测
print('线性回归模型预测：')
get_predicted_num(df, 'r1', 1)  # 预测红1
get_predicted_num(df, 'r2', 2)  # 预测红2
get_predicted_num(df, 'r3', 3)  # 预测红3
get_predicted_num(df, 'r4', 4)  # 预测红4
get_predicted_num(df, 'r5', 5)  # 预测红5
get_predicted_num(df, 'r6', 6)  # 预测红6
get_predicted_num(df, 'b1', 7)  # 预测蓝7


#统计预测，统计各个号码出现的最大值：
def get_predicted_num2(lotto, lotto_id):
    dit_num={}
    for i in lotto:
        if i not in dit_num.keys():
            dit_num[i]=0
        dit_num[i]=dit_num[i]+1
    ans = max(dit_num, key=lambda x: dit_num[x])
    if lotto_id < 7:
        print(f'中奖第{lotto_id}个红球为：', ans, '号球')
    else:
        print('中奖蓝球为：',ans, '号球')


print('统计预测：')
get_predicted_num2(r1, 1)  # 预测红1
get_predicted_num2(r2, 2)  # 预测红2
get_predicted_num2(r3, 3)  # 预测红3
get_predicted_num2(r4, 4)  # 预测红4
get_predicted_num2(r5, 5)  # 预测红5
get_predicted_num2(r6, 6)  # 预测红6
get_predicted_num2(b1, 7)  # 预测蓝7


