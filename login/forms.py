from django import forms
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class AddForm(forms.Form):
    poster = (
        ('manager', '管理员'),
        ('worker', '操作员'),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="手机号码", max_length=50, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label='角色', choices=poster)
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
