from django.shortcuts import render,redirect,HttpResponse
from . import models
from .forms import UserForm,AddForm,UpdateForm
from .models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
import json


# Create your views here.

def index(request):
    if request.session.get('is_login', None):
        return render(request, 'login/index.html')
    else:
        return redirect('/login/')
    # return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "请输入正确的信息！！！"
            except:
                message = "请输入正确的信息！！！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()

    return redirect('/login/')

@xframe_options_exempt
def add_staff(request):
    context = {}
    user_list_all = models.User.objects.all()
    paginator = Paginator(user_list_all, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    context['user_list'] = contacts
    if not request.session.get('is_login', None):
        return redirect('/index/')

    return render(request, 'login/admin-list.html',context)

def add_staff_add(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        register_form = AddForm(request.POST)
        resp = {'status': False, 'error': None, 'data': '请检查填写的内容！'}

        #print(register_form.errors.as_text())
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']
            role = register_form.cleaned_data['role']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']


            if password1 != password2:  # 判断两次密码是否相同
                resp = {'status': False, 'error': None, 'data': '两次输入的密码不同！'}
                return HttpResponse(json.dumps(resp))
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    resp = {'status': False, 'error': None, 'data': '用户已经存在，请重新选择用户名！'}
                    return HttpResponse(json.dumps(resp))
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    resp = {'status': False, 'error': None, 'data': '该邮箱地址已被注册，请使用别的邮箱！'}
                    return HttpResponse(json.dumps(resp))
                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.phone = phone
                new_user.password = password1
                new_user.email = email
                new_user.role = role
                new_user.save()

                # resp = HttpResponse()  # 请求处理成功后，返回'OK'到html中显示
                # resp['Access-Control-Allow-Origin'] = '*'
                # resp['Access-Control-Allow-Methods'] = 'POST'
                # resp['status'] = 200

                resp = {'status': True, 'error': None, 'data': '添加成功'}


                #resp.headers['Access-Control-Allow-Origin'] = '*'
                #resp.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
                return HttpResponse(json.dumps(resp))
                #return redirect('/add_staff/')  # 自动跳转到登录页面
                #return render(request, 'login/admin-list.html', locals())
    register_form = AddForm()
    return render(request, 'login/admin-add.html',locals())

def add_staff_update(request,id):
    if not request.session.get('is_login', None):
        return redirect('/index/')

    user_obj = User.objects.get(pk=id)

    if request.method == "POST":
        register_form = UpdateForm(request.POST)

        #print(register_form.errors.as_text())
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']
            role = register_form.cleaned_data['role']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']


            if password1 != password2:  # 判断两次密码是否相同
                resp = {'status': False, 'error': None, 'data': '两次输入的密码不同！'}
                return HttpResponse(json.dumps(resp))
            else:
                same_name_user = models.User.objects.filter(name=username)

                #print(same_name_user.name)
                #print(same_name_user.email)
                # if same_name_user:  # 用户名唯一
                #     #if user_obj.name.name != same_name_user.name:
                #         resp = {'status': False, 'error': None, 'data': '用户已经存在，请重新选择用户名！'}
                #         return HttpResponse(json.dumps(resp))
                # same_email_user = models.User.objects.filter(email=email)
                # if same_email_user:  # 邮箱地址唯一
                #     #if user_obj.email != same_email_user.email:
                #         resp = {'status': False, 'error': None, 'data': '该邮箱地址已被注册，请使用别的邮箱！'}
                #         return HttpResponse(json.dumps(resp))
                # 当一切都OK的情况下，创建新用户
                models.User.objects.filter(id=id).update(
                    name=username,
                    phone = phone,
                    password = password1,
                    email=email,
                    role=role
                )
                # new_user = models.User.objects.get(id=id)
                # new_user.name = username
                # new_user.phone = phone
                # new_user.password = password1
                # new_user.email = email
                # new_user.role = role
                # new_user.save()

                # resp = HttpResponse()  # 请求处理成功后，返回'OK'到html中显示
                # resp['Access-Control-Allow-Origin'] = '*'
                # resp['Access-Control-Allow-Methods'] = 'POST'
                # resp['status'] = 200

                resp = {'status': True, 'error': None, 'data': '修改成功'}


                #resp.headers['Access-Control-Allow-Origin'] = '*'
                #resp.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
                return HttpResponse(json.dumps(resp))
                #return redirect('/add_staff/')  # 自动跳转到登录页面
                #return render(request, 'login/admin-list.html', locals())
    #register_form = AddForm()
    return render(request, 'login/admin-edit.html',{'user_obj':user_obj})

# class AddStaff(View):
#     template_name = 'login/admin-add.html'
#     def get(self, requset):
#         pass
#         return render(request, self.template_name)

def hash_code(s, salt='qazwsxedc'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# 404
def page_not_found(request, exception):  # 注意点
    return render(request, '404.html')

# # 500
# def page_error(request):
#     return render(request, '500.html')

