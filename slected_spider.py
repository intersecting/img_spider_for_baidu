from fake_useragent import UserAgent
import requests
import re
import os
import uuid
import base64

def selecting_image(img_path, img_name):
    """图像审核接口"""
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
    # 二进制方式打开图片文件
    img_path_uns = os.path.join(img_path, img_name + '_unselected')
    img_path_s = os.path.join(img_path, img_name + '_selected')
    # 创建一个{img_name}_selected文件夹
    if os.path.exists(img_path_s):
        print("文件夹已存在，无需创建")
    else:
        os.mkdir(img_path_s)
        print("已创建文件夹%s" % img_path)
    # 将要筛选的文件夹中的文件名以列表形式储存在dir_imgs
    dir_imgs = os.listdir(img_path_uns)
    for img_uns in dir_imgs:
        f = open('{path}/{img_uns}'.format(path = img_path_uns, img_uns=img_uns), 'rb')
        img_s = f.read()
        # 开始使用百度识图API
        img = base64.b64encode(img_s)
        params = {"image":img}

        # 输入自己的百度识图token
        access_token = '' #！！！输入自己的token，要在百度识图上创建，之后用aK和sk得到自己的token！！！
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            # 将响应以json存到result
            result = response.json()
            print (response.json(),img_uns)
            # 如果图片合规则存入文件夹
            s = '合规'
            if result['conclusion'] == s:
                tmp_file_name = '{path}/{name}.jpg'.format(path=img_path_s, name=img_uns)
                with open(file=tmp_file_name, mode="wb") as file:
                    try:
                        file.write(img_s)
                    except:
                        pass
    print("已全部筛选")


headers = {"User-agent": UserAgent().random,  # 随机生成一个代理请求
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
           "Connection": "keep-alive"}

img_re = re.compile('"thumbURL":"(.*?)"')
img_format = re.compile("f=(.*).*?w")


def file_op(img,img_path,img_name,i):
    i = str(i)
    tmp_file_name = '{path}/{name}.jpg'.format(path=img_path, name=i)
    with open(file=tmp_file_name, mode="wb") as file:
        try:
            file.write(img)
        except:
            pass


def xhr_url(url_xhr, img_path, img_name, start_num=0, page=5):

    end_num = page*30
    i = 0
    img_path = os.path.join(img_path, img_name+'_unselected')
    # 创建一个{img_name}_unselected文件夹
    if os.path.exists(img_path):
        print("文件夹已存在，无需创建")
    else:
        os.mkdir(img_path)
        print("已创建文件夹%s" % img_path)
    # 循环爬取，百度图片是每次请求30个图片
    for page_num in range(start_num, end_num, 30):
        resp = requests.get(url=url_xhr+str(page_num), headers=headers)
        if resp.status_code == 200:
            img_url_list = img_re.findall(resp.text)  # 这是个列表形式
            for img_url in img_url_list:
                # 以数字排序命名每张图片
                i = i+1
                img_rsp = requests.get(url=img_url, headers=headers)
                file_op(img=img_rsp.content, img_path=img_path, img_name=img_name, i=i)
                print("已下载：{num}.jpg".format(num=i))
        else:
            break
    print("内容已经全部爬取")


if __name__ == "__main__":
    img_name = input("输入你想检索内容:")
    file_path = input("文件夹路径：(例如D:/spider)")
    if os.path.exists(file_path):
        print("文件夹已存在，无需创建")
    else:
        os.mkdir(file_path)
        print("已创建文件夹%s" % file_path)
    # 百度图片的url
    org_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&word={text}&pn=".format(text=img_name)
    # 进入爬取图片函数
    xhr_url(url_xhr=org_url, start_num=int(input("开始页:")), page=int(input("所需爬取页数:")), img_path=file_path, img_name=img_name)
    # 进入筛选函数，注意可以不选用此功能，需要接入百度识图的API，要注册并创建一个应用，得到token，如果不需要筛选直接注释掉就可以
    selecting_image(img_path=file_path,img_name=img_name)
