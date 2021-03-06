from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AuthorCreationForm, AuthorChangeForm
from .models import Author, Post, Comment, Server
from markdownx.admin import MarkdownxModelAdmin


# Register your models here.
class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    list_display = ['username', 'github', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ['github']}),
    )


admin.site.register(Author, AuthorAdmin)
#admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Server)
admin.site.register(Post, MarkdownxModelAdmin)