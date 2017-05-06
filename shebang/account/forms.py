# coding: utf-8

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from account.models import User

class SignupForm(forms.ModelForm):
        
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=True),  required=True, 
            label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True), required=True, 
            label='비밀번호(재입력)')


    class Meta:
        model = User
        fields = ['email', 'name']
        labels = {
            'email': '경북대학교 웹메일',
            'name': '이름',

        }

    def clean(self):
            
        email = self.cleaned_data['email']
        
        if not email.endswith('knu.ac.kr'):
            raise forms.ValidationError('경북대학교 메일(@knu.ac.kr)이 아닙니다.') # 학교 이메일 검사
            
        if get_user_model().objects.filter(email=email).exists(): 
            raise forms.ValidationError('이미 등록된 이메일입니다.') # 이메일 중복 검사

        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('비밀번호가 다릅니다(동일한 비밀번호를 입력해주세요).') # 비밀번호 확인란 검사
        
        return self.cleaned_data              

    def save(self, *args, **kwargs):
        u = get_user_model().objects.create_user(self.cleaned_data['email'],
                                                 self.cleaned_data['password1'],
                                                 self.cleaned_data['name']

        )

        u.save()


class SendEmailForm(forms.Form):
    
    email = forms.EmailField(required=True, label='경북대학교 웹메일')
    name = forms.CharField(max_length=30, required=True, label='이름')


    def clean(self):
        
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        

        if not email.endswith('knu.ac.kr'):
            raise forms.ValidationError('경북대학교 메일(@knu.ac.kr)이 아닙니다.')
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('가입된 메일이 아닙니다.')
        
        user = User.objects.get(email=email)
        if user.name != name:
            raise forms.ValidationError('회원가입시 입력한 이름과 다릅니다.')

        return self.cleaned_data


        

