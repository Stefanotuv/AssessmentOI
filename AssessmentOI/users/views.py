from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, LogoutView, SignupView
from allauth.utils import get_form_class,get_request_param
from allauth.account.views import _ajax_response
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from . import app_settings
from django.shortcuts import resolve_url
from allauth.account.adapter import get_adapter, DefaultAccountAdapter
from django.views.generic import UpdateView, CreateView

from allauth.account.utils import (
    complete_signup,
    get_login_redirect_url,
    get_next_redirect_url,
    logout_on_password_change,
    passthrough_next_redirect_url,
    perform_login,
    sync_user_email_addresses,
    url_str_to_user_pk,

)


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('users_login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Account update successfully!')
            return redirect('users_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'users/profile.html',context)

class UserLoginView(LoginView):
        form_class = UserLoginForm
        template_name = "users/login.html"

        def get_context_data(self, **kwargs):
            ret = super(LoginView, self).get_context_data(**kwargs)
            signup_url = passthrough_next_redirect_url(self.request,
                                                       reverse("users_signup"),
                                                       self.redirect_field_name)
            redirect_field_value = get_request_param(self.request,
                                                     self.redirect_field_name)
            site = get_current_site(self.request)

            ret.update({"signup_url": signup_url,
                        "site": site,
                        "redirect_field_name": self.redirect_field_name,
                        "redirect_field_value": redirect_field_value})
            return ret

class UserLogoutView(LogoutView):
        template_name = "users/logout.html"

        def get(self, *args, **kwargs):
            if app_settings.LOGOUT_ON_GET:
                return self.post(*args, **kwargs)
            if not self.request.user.is_authenticated:
                response = redirect(self.get_redirect_url())
                return _ajax_response(self.request, response)
            if self.request.user.is_authenticated:
                self.logout()
            ctx = self.get_context_data()
            response = self.render_to_response(ctx)
            return _ajax_response(self.request, response)

        def post(self, *args, **kwargs):
            url = self.get_redirect_url()
            if self.request.user.is_authenticated:
                self.logout()
            response = redirect(url)
            return _ajax_response(self.request, response)


        def get_redirect_url(self):
            return (
                    get_next_redirect_url(
                        self.request,
                        self.redirect_field_name) or get_adapter(
                self.request).get_logout_redirect_url(
                self.request))


# adding profile and register classes this would enable the
# change in template when called from other apps in the project

class UserSignupView(SignupView):
    form_class = UserRegisterForm
    template_name = "users/signup.html"
    # success_url = 'users/login.html'

    def get(self, *args, **kwargs):
        output = super().get(*args, **kwargs)
        return output

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret['form']
        email = self.request.session.get('account_verified_email')
        if email:
            email_keys = ['email']
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append('email2')
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("users_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret


    def post(self, request, *args, **kwargs):
        output = super().post(request,*args, **kwargs)
        return output


class UserProfileView(UpdateView):
    template_name = 'core_bm/profile.html'

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'core_bm/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account update successfully!')

        return redirect('core_bm_users_profile')



