from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # 공백 지우고 데이터만 가져오기
            raw_password = form.cleaned_data.get('password1') # password1은 raw_password에 담는다
            user = authenticate(username=username, password=raw_password) # user정보 인증처리
            login(request, user) # 요청정보와 user정보로 로그인 자동 처리
            return redirect('index') # config/urls.py에 index 설정했었음
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})