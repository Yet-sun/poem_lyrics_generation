from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .models import User, Log
from django.http import JsonResponse
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from .chinese_poem_generate.eval_poem import *
from .lyrics_generation.lstm_model.generate_lyrics_word_based import *


# 将请求定位到index.html文件中
def main(request):
    return render(request, 'main.html')


def index(request):  # 登陆界面
    # generate_poem()
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # re = auth.authenticate(id=username, password=password)  # 用户认证

        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
            # 验证码正确
            if username and password:  # 确保用户名和密码都不为空
                username = username.strip()
                # 用户名字符合法性验证
                # 密码长度验证
                # 更多的其它验证.....
                try:
                    user = User.objects.get(username=username)
                    if user.password == password:
                        Log.objects.create(username=username)
                        return render(request, 'main.html')
                    else:
                        message = "密码不正确！"
                except:
                    message = "用户名不存在！"
            return render(request, 'index.html', {"error": message})
        else:
            return render(request, 'index.html', {'error': '验证码错误!'})
    else:
        return render(request, 'index.html')


# 获取验证码图片的视图
def get_valid_img(request):
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def get_random_color_bg():
        return random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)

    def get_random_color_font():
        return random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (160, 40),
        get_random_color_bg()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(4):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((10 + 40 * i, 0), tmp, fill=get_random_color_font(), font=font_obj)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 160  # 图片宽度（防止越界）
    height = 40
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


def regist(request):
    print("注册页面open")
    if request.method == 'POST':
        # regform = UserCreationForm(request.POST)
        # if regform.is_valid():
        #     user = authenticate( username=request.POST['username'], password=request.POST['password'])
        yzcode1 = int(request.POST['yzcode'])

        yzcode = request.session.get("yzcode")
        username = request.POST.get('valid_code', None)
        # username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

        print("输入验证码: ", yzcode1)
        print("正确的验证码: ", yzcode)
        if yzcode1 == yzcode:
            print("验证码正确")
            # return HttpResponse('验证码正确！')
            print('password: ', password)
            print('repassword: ', repassword)
            if password == repassword:
                # 添加到数据库
                User.objects.create(username=username, password=password)
                # return HttpResponse('注册成功!!')
                return render(request, 'index.html', {'error': '注册成功，请进行登陆!'})
            else:
                return render(request, 'register.html', {'error': '注册失败!'})


        else:
            return render(request, 'register.html', {'error': '验证码错误!'})

    return render(request, 'register.html')


# """获取手机验证码"""
def sendMsg(request):
    # 短信应用 SDK AppID
    appid = 1400  # ...   # SDK AppID 以1400pip开头
    appkey = "........."
    template_id = 267071
    ssender = SmsSingleSender(appid, appkey)
    yzcode = random.randint(1000, 9999)
    request.session["yzcode"] = yzcode
    # request.session['yzcode'].setMaxInactiveInterval(60*1)
    request.session.set_expiry(60)

    params = ["{code}".format(code=yzcode)]
    sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
    phone_numbers = "{mobile}".format(mobile=request.GET['mobile'])

    print("phone:  ", phone_numbers)
    sms_sign = "诗歌生成"
    try:
        # result = ssender.send_with_param(sms_type, 86, phone_numbers,template_id, params, sign=sms_sign, extend="", ext="" )
        result = ssender.send_with_param(86, phone_numbers, template_id, params, sign=sms_sign, extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
        print("success 发送验证码: ", phone_numbers)
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    print(result)
    return HttpResponse('发送成功')


# 历史记录查看
def log(request):
    # if request.method == "POST":
    data = Log.objects.all().values('username')
    length = len(data)
    dict = data[length - 1]
    username = dict['username']
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT poem FROM poem_app_log WHERE username = %s", [username])
    poem = cursor.fetchall()
    if poem:
        return render(request, 'log.html', {"data": poem})  # "".join(list(poem))
    return render(request, 'log.html')


graph = tf.get_default_graph()


def get_rand_poem(request):
    global graph
    with graph.as_default():
        new_poem = generate_poem()
        # new_poem = "".join(str(new_poem).replace(',', '').lstrip('[').rstrip(']'))
        print(new_poem)
        if request.method == "GET":
            data = Log.objects.all().values('id')
            length = len(data)
            dict = data[length - 1]
            id = dict['id']
            user = Log.objects.get(id=id)
            username = user.username
            poem = user.poem
            if poem is not None:
                Log.objects.create(username=username, poem=new_poem)
            else:
                user.poem = new_poem
                user.save()
        context = {"data1": new_poem}
    return JsonResponse(context)


def f_poem(request):
    keyword = "{keyword}".format(keyword=request.GET['keyword'])
    global graph
    with graph.as_default():
        print('五言藏头字： ', keyword)
        new_poem = generate_acrostic(keyword, 5)
        print(new_poem)

        data = Log.objects.all().values('id')
        length = len(data)
        dict = data[length - 1]
        id = dict['id']
        user = Log.objects.get(id=id)
        username = user.username
        poem = user.poem
        if poem is not None:
            Log.objects.create(username=username, poem=new_poem)
        else:
            user.poem = new_poem
            user.save()

        context = {"data1": new_poem}
    return JsonResponse(context)


def s_poem(request):
    keyword = "{keyword}".format(keyword=request.GET['keyword'])
    global graph
    with graph.as_default():
        print('七言藏头字： ', keyword)
        new_poem = generate_acrostic(keyword, 7)
        print(new_poem)

        data = Log.objects.all().values('id')
        length = len(data)
        dict = data[length - 1]
        id = dict['id']
        user = Log.objects.get(id=id)
        username = user.username
        poem = user.poem
        if poem is not None:
            Log.objects.create(username=username, poem=new_poem)
        else:
            user.poem = new_poem
            user.save()

        context = {"data1": new_poem}
    return JsonResponse(context)


def get_rand_sing(request):
    # global graph
    # with graph.as_default():
    data = eval_lyrics()
    context = {"data1": data}
    print(data)
    return JsonResponse(context)
