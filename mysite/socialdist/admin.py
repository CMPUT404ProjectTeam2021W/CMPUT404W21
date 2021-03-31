from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AuthorCreationForm, AuthorChangeForm
from .models import Author, Post, Comment


# Register your models here.
class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    list_display = ['username', 'github_link']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ['github_link']}),
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post)
admin.site.register(Comment)
