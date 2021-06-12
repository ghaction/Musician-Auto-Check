import configparser
import os
import requests
import json

#读取配置文件
root_dir = os.path.abspath(os.curdir)
configpath = os.path.join(root_dir, "config.ini")
config = configparser.ConfigParser()
config.read(configpath,encoding='utf-8')

#读取API接口
api = config.get("setting","api")

#读取md5选项
md5 = config.get("setting","md5")

#读取手机号码
phone = config.get("setting","phone")

#读取密码
password = config.get("setting","password")

#登录
def login():

    if md5 == "true":
        login = requests.get(api + "/login/cellphone?phone=" + phone + "&md5_password=" + password)
    elif md5 == "false":
        login = requests.get(api + "/login/cellphone?phone=" + phone + "&password=" + password)

    #返回cookie
    if login.status_code == 200:
        print("登录成功！")
        return login.cookies


login_cookie = login()
#print(login_cookie)

#获取任务userMissionId和period
def get_task():

    global userMissionId
    global period

    get_task = requests.get(api + "/musician/tasks",cookies=login_cookie)

    if get_task.status_code == 200:
        
        task_json = get_task.json()
        #print(jsonstr)

        json_array = json.loads(json.dumps(json.loads(json.dumps(task_json))['data']['list']))[7]
        #print(json_array)
        userMissionId = str(json_array['userMissionId'])
        print("获取missionId成功！")

        period = str(json_array['period'])
        print("获取period成功！")

get_task()

#签到
def check():
    check = requests.get(api + "/musician/cloudbean/obtain?id=" + userMissionId + "&period=" + period,cookies=login_cookie)
    if check.status_code == 200:
        print("签到成功！")

check()