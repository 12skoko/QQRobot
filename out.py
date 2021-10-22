import requests
import re
import time
import yaml

def encryption(n,e,pt):
    arr = 0
    for c in pt:
        arr *= 256
        arr += ord(c)
    q = pow(arr, int(e,16)) % int(n,16)
    q=hex(q)[2:]
    for i in range(len(q),128):
        q='0'+q
    return q

def out(name):
    with open('out_config.yaml', encoding='utf-8') as f:
        info = yaml.load(f, Loader=yaml.SafeLoader)[name]


    se = requests.session()

    headers = {
        'Host': 'bsdtlc.njupt.edu.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://rzfw.njupt.edu.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': 'UserID='+UserID+';route='+route+';JSESSIONID=' + JSESSIONID + ';PortalToken=' + PortalToken,
        'Connection': 'keep-alive',
    }

    req = se.get(url='http://bsdtlc.njupt.edu.cn/StartWorkflow?Workflow=WF_XSCXSQ', headers=headers,
                 allow_redirects=False)

    # print(req.headers['Set-Cookie'])

    r0 = re.compile('route=(.*?);')
    t0 = re.search(r0, req.headers['Set-Cookie'])

    route = t0[1]

    r0 = re.compile('JSESSIONID=(.*?);')
    t0 = re.search(r0, req.headers['Set-Cookie'])

    JSESSIONID1 = t0[1]

    se.headers.clear()

    req = se.get('http://rzfw.njupt.edu.cn/cas/login?service=http://bsdtlc.njupt.edu.cn:80/CASLogin')

    r0 = re.compile('<input type=\"hidden\" name=\"execution\" value=\"(.*?)\" />')
    t0 = re.search(r0, req.text)

    execution = t0[1]

    # print(execution)

    JSESSIONID = req.cookies.get_dict()['JSESSIONID']

    # print('JSESSIONID='+JSESSIONID)

    headers = {
        'Cookie': 'JSESSIONID=' + JSESSIONID
    }

    req = se.get('http://rzfw.njupt.edu.cn/cas/v2/getPubKey', headers=headers)

    # print(req.text)

    r0 = re.compile('_pv0=(.*?); Domain=rzfw.njupt.edu.cn; Path=/')
    t0 = re.search(r0, req.headers["Set-Cookie"])

    _pv0 = t0[1]

    r0 = re.compile('{\"modulus\":\"(.*?)\",\"exponent\":\"(.*?)\"}')
    t0 = re.search(r0, req.text)

    n = t0[1]

    e = t0[2]

    password = encryption(n, e, info['password'])

    # print('_pv0='+_pv0)

    data = {
        'username': info['account'],
        'mobileCode': '',
        'password': password,
        'authcode': '',
        'execution': execution,
        '_eventId': 'submit'
    }

    headers = {
        'Host': 'rzfw.njupt.edu.cn',
        'Content-Length': '7370',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://rzfw.njupt.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://rzfw.njupt.edu.cn/cas/login?service=http%3A%2F%2Fbsdtlc.njupt.edu.cn%2FCASLogin',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'JSESSIONID=' + JSESSIONID + ';_pv0=' + _pv0,
        'Connection': 'keep-alive',
    }
    se.headers.clear()
    req = se.post(url='http://rzfw.njupt.edu.cn/cas/login?service=http%3A%2F%2Fbsdtlc.njupt.edu.cn%2FCASLogin',
                  data=data, headers=headers, allow_redirects=False)

    # print(req.status_code)
    # print(req.headers)

    ticketurl = req.headers['Location']

    # print(ticketurl)

    # return 0

    se.headers.clear()
    req = se.get(url=ticketurl, allow_redirects=False)
    # print(req.text)
    # print(req.headers['Set-Cookie'])
    # print(req.headers)

    # r0 = re.compile('JSESSIONID=(.*?); Path=/; HttpOnly, UserID=(.*?); Max-Age=\d*?; Expires=.*?; Path=/, PortalToken=(.*?); Path=/')

    # r0 = re.compile('JSESSIONID=(.*?);')
    # t0 = re.search(r0, req.headers["Set-Cookie"])

    JSESSIONID = JSESSIONID1

    r0 = re.compile('UserID=(.*?);')
    t0 = re.search(r0, req.headers["Set-Cookie"])

    UserID = t0[1]

    r0 = re.compile('PortalToken=(.*?);')
    t0 = re.search(r0, req.headers["Set-Cookie"])

    PortalToken = t0[1]

    se.headers.clear()

    mainurl = 'http://bsdtlc.njupt.edu.cn/welcome.do'

    headers = {
        'Host': 'bsdtlc.njupt.edu.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://rzfw.njupt.edu.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'UserID=' + UserID + ';route=' + route + ';JSESSIONID=' + JSESSIONID + ';PortalToken=' + PortalToken,
        'Connection': 'keep-alive',
    }

    req = se.get(url='http://bsdtlc.njupt.edu.cn/StartWorkflow?Workflow=WF_XSCXSQ', headers=headers)

    # print(req.text)

    r0 = re.compile('/WorkProcessor\?Table=WF_XSCXSQ&Token=(.*?)&WorkID=(\d*?)&StepID=initialStep')
    t0 = re.search(r0, req.text)

    # print(t0)

    Token = t0[1]
    WorkID = t0[2]

    # print(Token)
    # print(WorkID)

    posturl = 'http://bsdtlc.njupt.edu.cn/OperateProcessor?operate=WorkAction.4&WorkActionID=4&Table=WF_XSCXSQ&Token=' + Token + '&WorkID=' + WorkID + '&StepID=initialStep&&isSubmit=1'

    data = {
        'operate': 'Add',
        '$C{sqr}': '0',
        'sqr': info['sqr'],
        '$C{xh}': '0',
        '$C{xy}': '0',
        'xy': info['xy'],
        '$C{zy}': '0',
        'zy': info['zy'],
        '$C{BJ}': '0',
        'BJ': info['BJ'],
        '$C{lxdh}': '1',
        'lxdh': info['lxdh'],
        '$C{qjdmc}': '0',
        '$C{sqsj}': '0',
        'sqsj': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '$C{jhcxrq}': '3',
        'jhcxrq': time.strftime("%Y-%m-%d", time.localtime()),
        '$C{jhfxrq}': '3',
        'jhfxrq': time.strftime("%Y-%m-%d", time.localtime()),
        '$C{mdd}': '2',
        'mdd': '1',
        '$C{cxsy}': '7',
        'cxsy': info['cxsy'],
        '$C{jjlxr}': '1',
        'jjlxr': info['jjlxr'],
        '$C{jjlxrdh}': '1',
        'jjlxrdh': info['jjlxrdh']
    }

    headers = {
        'Host': 'bsdtlc.njupt.edu.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://bsdtlc.njupt.edu.cn/StartWorkflow?Workflow=WF_XSCXSQ',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'UserID=' + UserID + ';route=' + route + ';JSESSIONID=' + JSESSIONID + ';PortalToken=' + PortalToken,
        'Connection': 'keep-alive',
    }

    se.headers.clear()

    req = se.post(url=posturl, headers=headers, data=data)

    # print(req.text)


# info={
#     'account':'',#智慧校园账号
#     'password':'',#智慧校园密码
#     'xy': '',#学院
#     'zy': '',#专业
#     'BJ': '',#班级
#     'sqr': '',#申请人
#     'lxdh': '',#电话
#     'cxsy': '',#申请事由
#     'jjlxr': '',#紧急联系人
#     'jjlxrdh': ''#紧急联系电话
# }


