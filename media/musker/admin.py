from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep



# mix profile info into user info 
class ProfileInline(admin.StackedInline):
    model = Profile


# unregister Groups
admin.site.unregister(Group)
#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]

# unregister user
admin.site.unregister(User)
# register user
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)
admin.site.register(Meep)


