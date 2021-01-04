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


def hello_world(request):
    name = Table1.objects.all()

    # User = Table1()
    # return HttpResponse('你輸入的參數是pk: {}'.format(pk))
    return render(request, 'hello.html', {'current_time': str(datetime.now())[0:19], 'aa': '1312223', 'name': name, })


def base(request):
    return render(request, 'base.html', {

    })


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

        '''
        japanyear = TestRainfall.objects.filter(country="日本").values(
            'year').annotate(id=Count('id'))
        '''
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
        messages.success(request, '請先登入')
        return redirect("/login",)


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

            return render(request, 'home.html', {'allyear': allyear, 'waterrainfall': getrainfallid[0].rainfall, 'rainfall': getcountrytrainfall, 'post': getpost, 'ifpost': ifpost, 'country': country, 'year': year, 'month': month, 'toyear': toyear, 'tomonth': tomonth, })

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


def result(request):
    return render(request, 'base.html', {

    })


def mainweb(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        data = TestRainfall.objects.all()

        return render(request, "mainweb.html", {'username': username, 'data': data, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


def memberspace(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        return render(request, "memberspace.html", {'username': username, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


def memberpost(request):
    if request.session['is_login'] == True:
        username = request.session['username']

        getuser = Table1.objects.filter(name=username)
        getuserid = getuser[0].id
        getpost = Post.objects.filter(table1=getuserid)
        return render(request, "memberpost.html", {'username': username, 'post': getpost})
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


def memberreport(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getreport = request.POST.get("report", None)
        userid = Table1.objects.get(name=username)
        Report.objects.create(table1=userid, post=getreport)
        return render(request, "memberreport.html", {'username': username, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


def memberpostdel(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        post = Post.objects.get(id=postid)
        post.delete()
    # return redirect("/manager/post",)
    return redirect("/memberpost",)


def memberposteditpage(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        getpost = Post.objects.get(id=postid)
        return render(request, "memberpostedit.html", {'username': username, 'post': getpost})
    return redirect("/memberpost",)


def memberpostedit(request):
    if request.method == "POST":
        username = request.session['username']
        post = request.POST.get("post", None)
        postid = request.POST.get("postid", None)
        getpost = Post.objects.get(id=postid)
        getpost.post = post
        getpost.save()
        return redirect("../memberpost/",)


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


# @cache_page(60 * 15)
def login(request):
    '''
    if request.session['is_login'] == True:
        username = request.session['username']
        allyear = []
        for i in range(1990, 2026):
            allyear.append(i)
        return render(request, "home.html", {'username': username, 'allyear': allyear})
    '''
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


def logout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/login",)
    # return render(request, "login.html", {'messages': '成功登出'})
# ------------------------------------------------------------------------------------------------------------------------


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


def manager(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getuser = Table1.objects.all()

        return render(request, "managerpassword.html", {'username': username, 'data': getuser, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)


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


def managerpost(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        getpost = Post.objects.all()

        return render(request, "managerpost.html", {'username': username, 'post': getpost, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)


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


def delete(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        postid = request.POST.get("postid", None)
        post = Post.objects.get(id=postid)
        post.delete()
    # return redirect("/manager/post",)
    return redirect("/manager/post",)


def managerlogout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/manager/login",)


def managerpsedit(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
    return render(request, 'manageredit.html', {
        'username': username
    })


def modify(request):
    if request.method == "POST":
        password = request.POST.get("password", None)
        username = request.POST.get("username", None)
        user = Table1.objects.get(name=username)
        user.password = password
        user.save()
    return redirect("/manager/password",)


'''
@login_required(login_url="Login")
def index(request):
    return render(request, 'index.html')


def sign_up(request):
    form = RegisterForm()

    # User.ID = 4
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password1")
            User = Table1(name=username, password=password)
            User.save()
            # User.name = username
            # User.password = password
            # form.save()
            return redirect('/login')  # 重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def sign_in(request):
    form = LoginForm()
    # name1 = Table1.objects.all().values_list('name', 'password')
    # Table1.objects.filter(id=3).update(name='test')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        name = Table1.objects.filter(name=username)

        if name is not None:
            login(request, user)
            return redirect('/')  # 重新導向到首頁
    context = {
        'form': form,
        # 'name1': ('test1', 'pstest2') in name1
    }
    return render(request, 'login.html', context)


def log_out(request):
    logout(request)
    return redirect('/login')  # 重新導向到登入畫面
'''
