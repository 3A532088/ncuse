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
from django.db.models import Count


def hello_world(request):
    name = Table1.objects.all()

    # User = Table1()

    return render(request, 'hello.html', {
        'current_time': str(datetime.now()),
        'aa': '1312223',
        'name': name,
    })


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

        if request.method == "POST":
            country = request.POST.get("country", None)
            year = request.POST.get("year", None)
            month = request.POST.get("month", None)
            return render(request, "home.html", {'username': username, 'data': data, 'country': country, 'rainfallcountry': rainfallcountry, 'rainfallyear': rainfallyear, 'userid': userid, 'year': year, 'month': month, 'alldata': alldata, 'list_time': list_time})
        return render(request, "home.html", {'username': username, 'data': data, 'rainfallcountry': rainfallcountry, 'rainfallyear': rainfallyear, 'alldata': alldata, 'list_time': list_time})
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


def search(request):
    if request.method == "POST":
        country = request.POST.get("country", None)
        year = request.POST.get("year", None)
        month = request.POST.get("month", None)

        username = request.session['username']
        userid = Table1.objects.get(name=username)
        getdata = TestRainfall.objects.filter(
            year=year, month=month, country=country)
        rainfallid = getdata[0].id
        getpost = Post.objects.filter(rainfall=rainfallid)

    return render(request, 'home.html', {
        'post': getpost
    })


def post(request):
    if request.method == "POST":
        country = request.POST.get("country", None)
        year = request.POST.get("year", None)
        month = request.POST.get("month", None)
        getpost = request.POST.get("comment", None)
        username = request.session['username']
        userid = Table1.objects.get(name=username)
        getdata = TestRainfall.objects.filter(
            year=year, month=month, country=country)
        rainfallid = getdata[0].id
        dataid = TestRainfall.objects.get(id=rainfallid)
        Post.objects.create(post=getpost, table1=userid,  rainfall=dataid)

        return redirect("/home",)


def result(request):
    return render(request, 'base.html', {

    })


def logout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/login",)
    # return render(request, "login.html", {'messages': '成功登出'})


def mainweb(request):
    if request.session['is_login'] == True:
        username = request.session['username']
        data = TestRainfall.objects.all()

        return render(request, "mainweb.html", {'username': username, 'data': data, })
    else:
        messages.success(request, '請先登入')
        return redirect("/login",)


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
                return redirect("/manager",)
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
        data = Table1.objects.all()

        return render(request, "manager.html", {'username': username, 'data': data, })
    else:
        messages.success(request, '請先登入')
        return redirect("/manager/login",)


def managerlogout(request):
    request.session['is_login'] = False
    # messages.success(request, "登出")
    messages.success(request, '登出成功')
    return redirect("/manager/login",)


def manageredit(request):
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
    return redirect("/manager",)


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
