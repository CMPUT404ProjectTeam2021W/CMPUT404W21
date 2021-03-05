from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser, Post


# Register your models here.
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', 'github_link']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ['github_link']}),
    )


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post)