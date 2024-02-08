from django.views import View
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from django.shortcuts import render, redirect
from allauth.account import views # 追加
from accounts.forms import ProfileForm, SignupUserForm # 追加
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('attendance')  # 'attendance'は実際のURLに置き換えてください

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('attendance')

        return super().post(*args, **kwargs)

    
class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })



class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'department': user_data.department
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.department = form.cleaned_data['department']
            user_data.save()
            return redirect('profile')

        return render(request, 'accounts/profile.html', {
            'form': form
        })
    

