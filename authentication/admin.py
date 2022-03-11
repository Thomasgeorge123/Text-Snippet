from django.contrib import admin
from .models import User,UserRole,Role,PasswordRule

# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(PasswordRule)