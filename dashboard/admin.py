from django.contrib import admin

from .models import Profile
from .models import User
from .models import Data
admin.site.register(User)
admin.site.register(Data)
admin.site.register(Profile)
# Register your models here.
