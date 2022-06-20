#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, sys, base64, hashlib, requests
from bs4 import BeautifulSoup
import time, csv

request = requests.Session()


def logging(typ='-', text='-'):
    print(f'[{typ}] {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {text}')


def replace_sym(data):
    data = str(data)
    data = data.replace("'", '"')
    data = data.replace(" ", '')
    return data


def login(username, password, ):
    try:
        logging("i", "正在打开登录页面...")
        login_part = BeautifulSoup(request.get(wzk_url, headers=header).text, features="html.parser").find(name='a',
                                                                                                           attrs={
                                                                                                               'class': 'btn btn-info btn-small'}).get(
            'href')
        login_url = wzk_url + login_part
        logging("i", "构造登录请求...")
        login_csrf_token = BeautifulSoup(request.get(login_url, headers=header).text, features="html.parser").find(
            name='input', attrs={'name': 'csrf_token', 'id': 'csrf_token'}).get('value')
        pwd = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        easy = "0"
        data = {"username": username,
                "pwd": pwd,
                "hash": login_csrf_token,
                "easy": easy}
        data = replace_sym(data)
        data = {"datainfo": base64.b64encode(str(data).encode(
            encoding='UTF-8')).decode(encoding='UTF-8')}
        login_post_url = wzk_url + '/?q=user_login_submit'
        logging("i", "提交登录请求")
        login = request.post(login_post_url, data=data, headers=header).text
        login = login.encode('utf8')[3:].decode('utf8')
        logging("!", f'登录状态：{login}')
        if r'\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef' in login:
            logging("!", "用户名或密码错误，请重新输入！")
        elif r'\u7531\u4e8e\u60a8\u8fde\u7eed\u8f93\u5165\u5bc6' in login:
            logging("!", "由于您连续输入密码错误，账号将会锁定5分钟，请5分钟后再登录！")
        elif r"\u9a8c\u8bc1\u672a\u901a\u8fc7\uff0c\u8bf7\u91cd" in login:
            logging("!", "csrf验证失败！")
        else:
            logging("*", f'用户 {json.loads(login)["userid"]} 登录成功')
            return json.loads(login)["userid"]
    except:
        return False
    return False


def get_video_link(courseid):
    for i in range(3):
        logging("i", f'第 {i + 1}/3 次尝试，课程ID为 {courseid}')
        url = wzk_url + '/?q=items/student/study/' + courseid
        header = {"Host": "jsjzyk.36ve.com",
                  "Connection": "keep-alive",
                  "Pragma": "no-cache",
                  "Cache-Control": "no-cache",
                  "Upgrade-Insecure-Requests": "1",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Referer": "http://jsjzyk.36ve.com",
                  "Accept-Encoding": "gzip, deflate",
                  "Accept-Language": "zh-CN,zh;q=0.9"}
        course_page = request.get(url, headers=header)
        center_content = BeautifulSoup(course_page.text, features="html.parser").find(
            name='div', attrs={'class': 'courselist'})
        all_content_element = BeautifulSoup(str(center_content), features="html.parser").find_all(
            name='li', onclick=True)
        all_link = [wzk_url + link_element.find('a').get('href') for link_element in all_content_element if
                    link_element.find(
                        'radius bg-img-half') != '' or link_element.find('class="radius "') != '']
        logging("*", f'获取了 {len(all_link)} 条链接。')
        if len(all_link) > 0:
            return all_link
    logging("!", "没有要学习的项目！")
    return []


def do_auto_new(link, userid, courseid):
    url = wzk_url + '/?q=save_user_item_progress/' + str(courseid) + '/' + link[len(link) - link[::-1].find(
        '/'):] + '/' + str(userid)
    data = {
        'progress': '10'
    }
    try:
        request.post(url, data, header)
    except:
        return 1
    return 0


# 课程评论
def do_auto_new_save(courseid):
    url = wzk_url + '/?q=course_message/' + str(courseid) + '/save/callback'
    # url = wzk_url + '/?q=save_user_item_progress/' + str(courseid) + '/' + link[len(link) - link[::-1].find(
    #     '/'):] + '/' + str(userid)
    print(url)
    data = {
        'flag': 'question',
        'detail': '<p> 如何写作 </p>',
        'title': '课程提问',
        'click_from': 'new_platfrom'
    }
    try:
        request.post(url, data, header)
    except:
        return 1
    return 0


def write_all_links(courseid, links, filename):
    with open(filename, 'a', newline='') as file:
        file = csv.writer(file)
        items = [courseid]
        items.extend(links)
        file.writerow(items)


def get_course_link(userid):
    course_id = []
    if userid:
        while 1:
            logging("!", "输入课程ID（留空按回车结束）")
            i = input(">")
            if i.isnumeric():
                course_id.append(str(int(i)))
            else:
                logging("*", f'共 {len(course_id)} 条课程。')
                return course_id


if __name__ == '__main__':
    wzk_url = 'http://jsjzyk.36ve.com'
    logging("!", "输入用户名")
    username = str(input('>'))
    logging("!", "输入密码")
    password = str(input('>'))
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"}
    try:
        userid = login(username, password)
        if userid == 0:
            logging("!", "登录失败！")
            raise "loginException"
    except:
        sys.exit()
    conf = 0
    while conf != 9:
        logging("!", "等待用户选择！")
        conf = int(input('接下来做什么呢？\n\t1.刷课\n\t2.生成待刷项链接\n\t>'))
        if conf == 1:
            logging("-", "开始运行！")
            with open("test.txt", 'r') as file:
                f = csv.reader(file)
                for _ in f:
                    logging("!", "切换课程...")
                    for i in range(1, len(_)):
                        if i < 30:
                            logging("!", "开始评论了------")
                            do_auto_new_save(courseid=_[0])
                        while i % 66 == 0:
                            logging("*", "重新登录中")
                            login(username, password)
                            break
                        logging("~", f'[{i}/{len(_) - 1}] {_[i]}')
                        do_auto_new(link=_[i], userid=userid, courseid=_[0])
        elif conf == 2:
            course_id = get_course_link(userid)
            file = open('test.txt', 'w')
            file.close()
            for _ in course_id:
                print()
                all_link = get_video_link(_)
                write_all_links(_, all_link, "test.txt")
