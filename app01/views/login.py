from django.core.exceptions import ValidationError
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from io import BytesIO
from app01 import models
from app01.utils.code import check_code
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    Username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    Password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )

    def clean_Password(self):
        pwd = self.cleaned_data.get("Password")
        return md5(pwd)


def login_view(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        admin_object = models.AdminInfo.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("Password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 根据 user_type 值进行页面跳转
        if int(admin_object.user_type) == 1:
            # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
            request.session["info"] = {'id': admin_object.id, 'name': admin_object.Username, 'type': admin_object.user_type}
            # session可以保存 7天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/admin/')  # 跳转到管理员页面
        else:
            # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
            request.session["info"] = {'id': admin_object.id, 'name': admin_object.Username, 'type': admin_object.user_type}
            # session可以保存 7 天
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/user/')  # 跳转到普通用户页面

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')


def index(request):
    return redirect('/asset')