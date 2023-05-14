from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_name', 'email', 'password', 'is_active', 'is_admin',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('user_name', 'email', 'is_admin', 'is_active', 'withdraw',)
    list_filter = ('is_admin',)
    fieldsets = (
        #'''----------------추가된 부분: 이미지 추가 기능---------------이주한-'''
        (None, {'fields': ('user_name', 'email', 'password', 'image', 'followings',)}),
        #'''----------------fields에 "image"를 추가했습니다.------------------'''
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
            'fields': ('user_name', 'email', 'password1', 'password2', 'image', 'followings',),}),)
    
    search_fields = ('user_name', 'email',)
    ordering = ('user_name',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)