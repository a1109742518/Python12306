# coding=utf-8
import json
import re
import urllib2
import urllib
import ssl
import cookielib
from PIL import Image

from ResultItem import ResultItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/62.0.3202.94 Safari/537.36')]

ssl._create_default_https_context = ssl._create_unverified_context

# 验证码图片坐标
position = {'1': '35,35', '2': '105,35', '3': '175,35', '4': '245,35',
            '5': '35,105', '6': '105,105', '7': '175,105', '8': '245,105'}


def print_msg(msgs):
    if isinstance(msgs, list):
        for msg in msgs:
            print msg
    else:
        print msgs


# 获取图片验证并打开
def get_code():
    code_req = urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand'
                               '=sjrand&0.832671395429045')
    code_req.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
    code_img = opener.open(code_req).read()

    with open('code.png', 'wb') as fn:
        fn.write(code_img)

    # 两种方式打开图片
    im = Image.open('code.png')
    im.show()
    # os.system('start code.png')


# 验证验证码
def captcha_check():
    check_req = urllib2.Request("https://kyfw.12306.cn/passport/captcha/captcha-check")

    answer_data = {
        'answer': answer,
        'login_site': 'E',
        'rand': 'sjrand'
    }

    check_html = opener.open(check_req, data=urllib.urlencode(answer_data)).read()
    check_result = json.loads(check_html)
    if check_result['result_code'] == "4":
        print '验证码通过'
    else:
        print '验证码错误'
        exit(10086)


# 登录
def login():
    login_req = urllib2.Request('https://kyfw.12306.cn/passport/web/login')
    login_req.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')

    login_data = {
        'username': 'a1109742518@qq.com',
        'password': 'sc11427cxb',
        'appid': 'otn'
    }
    login_html = opener.open(req, data=urllib.urlencode(login_data)).read()

    login_result = json.loads(login_html)
    if login_result['result_code'] == 0:
        print '登录成功'
    else:
        print '登录失败'
        exit(10087)


# 验证
def uamtk():
    uamtk_req = urllib2.Request('https://kyfw.12306.cn/passport/web/auth/uamtk?appid=otn')
    uamtk_req.add_header('Referer', 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin')
    uamtk_result = json.loads(opener.open(uamtk_req).read())
    if uamtk_result['result_code'] == 0:
        print '验证UAMTK通过'
    else:
        print '验证UAMTK失败'
        exit()

    uamauth_data = {
        'tk': uamtk_result['newapptk']
    }
    uamauth_req = urllib2.Request('https://kyfw.12306.cn/otn/uamauthclient')
    uamauth_req.add_header('Referer', 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin')
    uamauth_html = opener.open(req, data=urllib.urlencode(uamauth_data)).read()
    try:
        uamauth_result = json.loads(uamauth_html)
        if uamauth_result['result_code'] == 0:
            print '验证uamauthclient通过，用户名' + uamauth_result['username']
        else:
            print '验证uamauthclient失败'
            exit()
    except:
        print '验证uamauthclient失败'
        exit()


get_code()
code = raw_input('>>>')
answer = ''
for x in code:
    if int(x) > 8:
        break
    answer = answer + position[x] + ','
captcha_check()
login()
uamtk()

req = urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-12-08&leftTicketDTO'
                      '.from_station=CBQ&leftTicketDTO.to_station=GGQ&purpose_codes=ADULT')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/leftTicket/init')
html = opener.open(req).read()

try:
    result = json.loads(html)
except:
    exit()

if not result['status']:
    exit()

resultDict = {}
for item in result['data']['result']:
    i = ResultItem(item, result['data']['map'])
    # print i.date + " " + i.startTime + "-" + i.endTime + " " \
    #       + i.no + " " + i.startStation + " " + i.endStation + " " \
    #       + "二等座:" + i.secondClass

    # print i.status
    resultDict[i.no] = i

if len(resultDict) == 0:
    print '查询不到车次'
    exit(10088)
print '查询到车次'

filterList = ['G6315']
for val in filterList:
    selectItem = None
    if resultDict.has_key(val):
        if resultDict[val].status:
            print '选择班次：' + val + '有车票可预定'
            if resultDict[val].secondClass == '有' or resultDict[val].secondClass > 0:
                print '选择班次：' + val + '有二等车票可预定'
                selectItem = resultDict[val]
                break
            else:
                print '选择班次：' + val + '无二等车票可预定'
        else:
            print '选择班次：' + val + '无车票可预定'
    else:
        print '找不到' + val + '车次'

# checkUser:
req = urllib2.Request('https://kyfw.12306.cn/otn/login/checkUser')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/leftTicket/init')
html = opener.open(req).read()
userLoginResult = json.loads(html)
if not userLoginResult['data']['flag']:
    print '未登录'
    exit()

if not selectItem:
    print '订票失败：找不到可预定车次'
    exit()

# od = OrderedDict()
# od['secretStr'] = selectItem.secretStr,
# od['train_date'] = selectItem.date,
# od['back_train_date'] = selectItem.date,
# od['tour_flag'] = 'dc',
# od['purpose_codes'] = 'ADULT',
# od['query_from_station_name'] = selectItem.startStation,
# od['query_to_station_name'] = selectItem.endStation,
# od = {
#     'secretStr': selectItem.secretStr,
#     'train_date': selectItem.date,
#     'back_train_date': selectItem.date,
#     'tour_flag': 'dc',
#     'purpose_codes': 'ADULT',
#     'query_from_station_name': selectItem.startStation,
#     'query_to_station_name': selectItem.endStation,
# }
query = 'secretStr=' + selectItem.secretStr + "&train_date=" + selectItem.date + "&back_train_date=" + selectItem.date + "&tour_flag=dc&purpose_codes=ADULT" + "&query_from_station_name=" + selectItem.startStation + "&query_to_station_name=" + selectItem.endStation
req = urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest?' + query)
req.add_header('Referer', 'https://kyfw.12306.cn/otn/leftTicket/init')
html = opener.open(req).read()
result = json.loads(html)

if not result['status']:
    print_msg(result['messages'])
    exit()
else:
    print '预订提交成功'

# 获取车票预定确认页面，不可省略
req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/initDc?_json_att=')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/leftTicket/init')
html = opener.open(req).read()
globalRepeatSubmitToken = re.findall("var globalRepeatSubmitToken = '(.*?)'", html, re.S)[0]
key_check_isChange = re.findall("'key_check_isChange':'(.*?)'", html, re.S)[0]
leftTicketStr = re.findall("'leftTicketStr':'(.*?)'", html, re.S)[0]
train_no = re.findall("'train_no':'(.*?)'", html, re.S)[0]
# print 'globalRepeatSubmitToken:' + globalRepeatSubmitToken

req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/confirmPassenger/initDc')
result = json.loads(opener.open(req).read())
if not result['status']:
    print '获取联系人失败'
    exit()

print '获取联系人数量：' + str(len(result['data']['normal_passengers']))

data = {
    'cancel_flag': 2,
    'bed_level_order_num': '000000000000000000000000000000',
    'passengerTicketStr': 'O,0,1,邱婷婷,1,445121199407043622,18312713106,N',
    'oldPassengerStr': '邱婷婷,1,445121199407043622,1_',
    'tour_flag': 'dc',
    'randCode': '',
    '_json_att': '',
    'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken
}
req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/confirmPassenger/initDc')
html = opener.open(req, data=urllib.urlencode(data)).read()
result = json.loads(html)
if result['status'] and result['submitStatus']:
    print '提交成功，选择席位'
else:
    print '提交失败'
    exit()

# req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount')
# req.add_header('Referer', 'https://kyfw.12306.cn/otn/confirmPassenger/initDc')
# html = opener.open(req).read()
# result = json.loads(html)
# print html


# passengerTicketStr:O,0,1,邱婷婷,1,445121199407043622,18312713106,N_O,0,1,陈侠彬,1,445121199307103915,13922074967,N
# oldPassengerStr:邱婷婷,1,445121199407043622,1_陈侠彬,1,445121199307103915,1_
# tour_flag:dc
# randCode:
# purpose_codes:00
# key_check_isChange:73181FC938AAA0B66C93437ADA54CF1EB215AA119B71207D352021CF
# train_location:Q9
# choose_seats:1F2D
# seatDetailType:000
# roomType:00
# dwAll:N
# _json_att:
# REPEAT_SUBMIT_TOKEN:8b0aef00dc4c79a9f321e50a587c5b6b

data = {
    'passengerTicketStr': 'O,0,1,邱婷婷,1,445121199407043622,18312713106,N',
    'oldPassengerStr': '邱婷婷,1,445121199407043622,1_',
    'tour_flag': 'dc',
    'randCode': '',
    'purpose_codes': '00',
    'key_check_isChange': key_check_isChange,
    'train_location': 'Q9',
    'choose_seats': '1F',
    'seatDetailType': '000',
    'roomType': '00',
    'dwAll': 'N',
    '_json_att': '',
    'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken
}
req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingle')
req.add_header('Referer', 'https://kyfw.12306.cn/otn/confirmPassenger/initDc')
html = opener.open(req, data=urllib.urlencode(data)).read()
result = json.loads(html)
if result['status'] and result['submitStatus']:
    print '提交成功，席位已锁定，订单待支付'
else:
    print '提交失败'
    exit()
