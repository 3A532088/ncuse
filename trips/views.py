from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib import messages
from trips.models import Table1
from trips.models import TestRainfall
from trips.models import Manager
from trips.models import Post
from trips.models import Report
from django.db.models import Count
from django.urls import reverse

# 沒用


def hello_world(request):
    name = Table1.objects.all()

    # User = Table1()
    # return HttpResponse('你輸入的參數是pk: {}'.format(pk))
    return render(request, 'hello.html', {'current_time': str(datetime.now())[0:19], 'aa': '1312223', 'name': name, })


# 沒用
def mainweb(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        data = TestRainfall.objects.all()

        return render(request, "mainweb.html", {'username': username, 'data': data, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)

# 沒用


def base(request):
    return render(request, 'base.html', {

    })


def api(name, password):
    username = "qaz123"
    passwd = "qaz123"
    if(name == username and password == passwd):
        data = "登入成功"
    else:
        data = "帳號密碼不正確"
    return data
# 沒用


def result(request):
    if request.method == "POST":
        if request.POST:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            Table1.objects.create(name=username, password=password)
            result = api(username, password)

            return HttpResponse(result)
        else:
            return HttpResponse("請輸入參數")

    else:
        return HttpResponse("請求方法不正確")


# 首頁


def home(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        # data = TestRainfall.objects.filter(year=1998, month=2, country="台灣")
        userid = Table1.objects.get(name=username).id
        # userid = getuserid.id
        getdata = TestRainfall.objects.filter(year=1998, month=2, country="台灣")
        data = getdata[0].id

        rainfallcountry = TestRainfall.objects.values(
            'country').annotate(id=Count('id'))

        rainfallyear = TestRainfall.objects.values(
            'year').annotate(id=Count('id'))
        alldata = TestRainfall.objects.all()

        list_time = TestRainfall.objects.all().values_list('country', 'year', 'month')
        allyear = []
        for i in range(1990, 2026):
            allyear.append(i)

        if request.method == "POST":
            country = request.POST.get("country", None)
            year = request.POST.get("year", None)
            month = request.POST.get("month", None)
            return render(request, "home.html", {'username': username, })
        return render(request, "home.html", {'username': username, 'allyear': allyear})
    else:
        messages.success(request, '尚未登入會員')
        return redirect("/login",)


''' 測試用
def home(request):

    username = 'username'
    
    # data = TestRainfall.objects.filter(year=1998, month=2, country="台灣")
    userid = Table1.objects.get(name=username).id
    # userid = getuserid.id
    getdata = TestRainfall.objects.filter(year=1998, month=2, country="台灣")
    data = getdata[0].id
    rainfallcountry = TestRainfall.objects.values(
        'country').annotate(id=Count('id'))
    rainfallyear = TestRainfall.objects.values(
        'year').annotate(id=Count('id'))
    alldata = TestRainfall.objects.all()
    list_time = TestRainfall.objects.all().values_list('country', 'year', 'month')
    allyear = []
    for i in range(1990, 2026):
        allyear.append(i)
    if request.method == "POST":

        country = request.POST.get("country", None)
        year = request.POST.get("year", None)
        month = request.POST.get("month", None)
        return render(request, "home.html", {'username': username, })
    return render(request, "home.html", {'username': username, 'allyear': allyear})
'''
# 查詢功能


def search(request):
    if request.method == "GET":
        '''
        country = request.POST.get("country", None)
        year = request.POST.get("year", None)
        month = request.POST.get("month", None)
        toyear = request.POST.get("toyear", None)
        tomonth = request.POST.get("tomonth", None)
        '''
        country = request.GET.get("country", None)
        year = request.GET.get("year", None)
        month = request.GET.get("month", None)
        toyear = request.GET.get("toyear", None)
        tomonth = request.GET.get("tomonth", None)

        username = request.session['username']
        userid = Table1.objects.get(name=username)
        getdata = TestRainfall.objects.filter(
            year=year, month=month, country=country)

        rainfallid = getdata[0].id

        getrainfallid = TestRainfall.objects.filter(
            year=year, month=month, country=country)
        rainfallid = getrainfallid[0].id

        togetrainfallid = TestRainfall.objects.filter(
            year=toyear, month=tomonth, country=country)
        torainfallid = togetrainfallid[0].id

        getrainfall = TestRainfall.objects.filter(
            id__range=[rainfallid, torainfallid], country=country)

        allyear = []
        for i in range(1990, 2026):
            allyear.append(i)

        if year == toyear and month == tomonth:
            getpost = Post.objects.filter(rainfall=rainfallid)
            ifpost = 1

            getcountrytrainfall = TestRainfall.objects.filter(
                year=year, month=month)
            getcountrytrainfallsize = getcountrytrainfall.count()
            sumcountryrainfall = 0
            for i in range(0, getcountrytrainfallsize):
                sumcountryrainfall += getcountrytrainfall[i].rainfall
            avgcountryrainfall = sumcountryrainfall/getcountrytrainfallsize

            return render(request, 'home.html', {'allyear': allyear, 'waterrainfall': getrainfallid[0].rainfall, 'rainfall': getcountrytrainfall, 'post': getpost, 'ifpost': ifpost, 'country': country, 'year': int(year), 'month': month, 'toyear': toyear, 'tomonth': tomonth, })

        getrainfallsize = getrainfall.count()
        sumrainfall = 0
        for i in range(0, getrainfallsize):
            sumrainfall += getrainfall[i].rainfall
        avgrainfall = sumrainfall/getrainfallsize
        issearch = 1

    return render(request, 'home.html', {
        'rainfall': getrainfall,
        'country': country,
        'year': year,
        'month': month,
        'toyear': toyear,
        'tomonth': tomonth,
        'sumrainfall':  round(sumrainfall, 1),
        'avgrainfall': round(avgrainfall, 1),
        'issearch': issearch,
        'allyear': allyear,
    })

# 發佈貼文


def post(request):
    if request.method == "POST":
        country = request.POST.get("country", None)
        year = request.POST.get("year", None)
        month = request.POST.get("month", None)
        toyear = request.POST.get("toyear", None)
        tomonth = request.POST.get("tomonth", None)
        comment = request.POST.get("comment", None)
        username = request.session['username']
        userid = Table1.objects.get(name=username)
        getdata = TestRainfall.objects.filter(
            year=year, month=month, country=country)
        rainfallid = getdata[0].id
        dataid = TestRainfall.objects.get(id=rainfallid)
        time = str(datetime.now())[0:19]
        Post.objects.create(post=comment, table1=userid,
                            rainfall=dataid, time=time)
        getpost = Post.objects.filter(rainfall=rainfallid)
        ifpost = 1

        getcountrytrainfall = TestRainfall.objects.filter(
            year=year, month=month)

        getrainfallid = TestRainfall.objects.filter(
            year=year, month=month, country=country)

        allyear = []
        for i in range(1990, 2026):
            allyear.append(i)

        return render(request, 'home.html', {
            'post': getpost,
            'country': country,
            'year': year,
            'month': month,
            'toyear': toyear,
            'tomonth': tomonth,
            'ifpost': ifpost,
            'rainfall': getcountrytrainfall,
            'waterrainfall': getrainfallid[0].rainfall,
            'allyear': allyear,

        })

# 會員中心


def memberspace(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        return render(request, "memberspace.html", {'username': username, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)

# 會員歷史貼文


def memberpost(request):
    if request.session['is_login'] == True:
        username = request.session['username']

        getuser = Table1.objects.filter(name=username)
        getuserid = getuser[0].id
        getpost = Post.objects.filter(table1=getuserid).order_by('-id')
        return render(request, "memberpost.html", {'username': username, 'post': getpost})
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)

# 會員回報問題


def memberreport(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getreport = request.POST.get("report", None)
        userid = Table1.objects.get(name=username)
        if request.method == "POST":
            Report.objects.create(table1=userid, post=getreport)
            return render(request, "memberreport.html", {'username': username, })
        else:
            return render(request, "memberreport.html", {'username': username, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)

# 會員刪除貼文


def memberpostdel(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        post = Post.objects.get(id=postid)
        post.delete()
    # return redirect("/manager/post",)
    return redirect("/memberpost",)

# 會員編輯貼文頁面


def memberposteditpage(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        getpost = Post.objects.get(id=postid)
        return render(request, "memberpostedit.html", {'username': username, 'post': getpost})
    return redirect("/memberpost",)

# 會員編輯貼文


def memberpostedit(request):
    if request.method == "POST":
        username = request.session['username']
        post = request.POST.get("post", None)
        postid = request.POST.get("postid", None)
        getpost = Post.objects.get(id=postid)
        getpost.post = post
        getpost.save()
        return redirect("../memberpost/",)

# 會員修改密碼


def memberedit(request):
    if request.method == "POST":
        username = request.session['username']

        password = request.POST.get("password", None)
        user = Table1.objects.get(name=username)
        user.password = password
        user.save()
        return redirect("../memberspace/",)
# ----------------------------------------------------------------------------------------------------------------------------------
# @cache_page(60 * 15)  # 60秒數，這裡指快取 15 分鐘，不直接寫900是為了提高可讀性

# 會員註冊


def signup(request):
    # return  HttpResponse("hello world!")
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if Table1.objects.filter(name=username):
            # 這裡通過httpresponse返回給前端資訊，前端index.html通過get_insert_response()來提示註冊失敗資訊alert("")
            # return render(request, "signup.html", {'messages': '帳號已註冊'})
            messages.success(request, '帳號已註冊')
            return redirect("/signup",)
        else:
            # 接收資料儲存到資料庫,creatr_user用hash值儲存
            Table1.objects.create(name=username, password=password)
            messages.success(request, '註冊成功')
            return redirect("/login",)
            # return render(request, "login.html", {'messages': '註冊成功'})
            # return render(request, "login.html",)

    user_list = Table1.objects.all()  # 從資料庫讀取所有資料
    # 第三個引數是後臺返回給瀏覽器的資料，定義data物件，返回一個字典，data會被index.html檔案引用
    return render(request, "signup.html", {"data": user_list})

# 會員登入
# @cache_page(60 * 15)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        list_user_pwd = Table1.objects.all().values_list('name', 'password')
        if list_user_pwd:  # 取出資料庫表中username,userlist兩列生成一個列表
            if (username, password) in list_user_pwd:
                request.session['is_login'] = True
                request.session['username'] = username
                # messages.success(request, "登入成功")
                messages.success(request, '登入成功')
                return redirect("/home",)
                # return render(request, "mainweb.html", {'messages': '登入成功'})
            else:
                messages.success(request, '帳號密碼錯誤')
                return redirect("/login",)
        else:
            return HttpResponse("使用者名稱不存在,請註冊")
    return render(request, "login.html",)


'''
def login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        list_user_pwd = Table1.objects.all().values_list('name', 'password')
        if list_user_pwd:  # 取出資料庫表中username,userlist兩列生成一個列表
            if (username, password) in list_user_pwd:
                # messages.success(request, "登入成功")
                messages.success(request, '登入成功')
                return redirect("/login",)
                # return render(request, "mainweb.html", {'messages': '登入成功'})
            else:
                messages.success(request, '帳號密碼錯誤')
                return redirect("/login",)
        else:
            return HttpResponse("使用者名稱不存在,請註冊")
    return render(request, "login.html",)
'''
# 會員登出


def logout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/login",)
    # return render(request, "login.html", {'messages': '成功登出'})
# ------------------------------------------------------------------------------------------------------------------------

# 管理員登入


def managerlogin(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        list_user_pwd = Manager.objects.all().values_list('name', 'password')

        if list_user_pwd:  # 取出資料庫表中username,userlist兩列生成一個列表
            if (username, password) in list_user_pwd:
                request.session['is_login'] = True
                request.session['username'] = username
                # messages.success(request, "登入成功")
                messages.success(request, '登入成功')
                return redirect("/manager/password",)
                # return render(request, "mainweb.html", {'messages': '登入成功'})
            else:
                messages.success(request, '帳號密碼錯誤')
                return redirect("/manager/login",)
        else:
            return HttpResponse("使用者名稱不存在,請註冊")
    return render(request, "managerlogin.html",)

# 管理員管理密碼


def manager(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getuser = Table1.objects.all().order_by('-id')

        return render(request, "managerpassword.html", {'username': username, 'data': getuser, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)

# 管理員管理密碼帳號查詢


def managerpasswordsearch(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        if request.method == "POST":
            getpostuser = request.POST.get("username", None)
            getuser = Table1.objects.filter(name=getpostuser)
            try:
                getuserid = getuser[0].id
            except:
                err = "查無此使用者"
                return render(request, "managerpassword.html", {'username': username, 'err': err})

            return render(request, "managerpassword.html", {'username': username, 'data': getuser, })
        else:
            getpost = Post.objects.all()
            return render(request, "managerpassword.html", {'username': username, 'post': getpost, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)

# 管理員管理貼文


def managerpost(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getpost = Post.objects.all().order_by('-id')

        return render(request, "managerpost.html", {'username': username, 'post': getpost, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)

# 管理員查看問題回報


def managerreport(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getpost = Report.objects.all().order_by('-id')

        return render(request, "managerreport.html", {'username': username, 'post': getpost, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)
# 管理員管理貼文帳號查詢


def managerpostsearch(request):
    if request.session['is_login'] == True:
        username = request.session['username']

        if request.method == "POST":
            getpostuser = request.POST.get("username", None)
            getuser = Table1.objects.filter(name=getpostuser)
            try:
                getuserid = getuser[0].id
            except:
                err = "查無此使用者"
                return render(request, "managerpost.html", {'username': username, 'err': err})
            getuserpost = Post.objects.filter(table1=getuserid)
            return render(request, "managerpost.html", {'username': username, 'post': getuserpost, })
        else:
            getpost = Post.objects.all()
            return render(request, "managerpost.html", {'username': username, 'post': getpost, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)

# 管理員管理貼文刪除


def delete(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        post = Post.objects.get(id=postid)
        post.delete()
    # return redirect("/manager/post",)
    return redirect("/manager/post",)

# 管理員登出


def managerlogout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/manager/login",)

# 管理員修改密碼頁面


def managerpsedit(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
    return render(request, 'manageredit.html', {
        'username': username
    })

# 管理員修改密碼


def modify(request):
    if request.method == "POST":
        password = request.POST.get("password", None)
        username = request.POST.get("username", None)
        user = Table1.objects.get(name=username)
        user.password = password
        user.save()
    return redirect("/manager/password",)
