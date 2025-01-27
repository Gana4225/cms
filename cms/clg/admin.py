from django.contrib import admin
from .models import *


class Std(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'department']


class Reg(admin.ModelAdmin):
    list_display = ['regulation']


class Dept(admin.ModelAdmin):
    list_display = ['department']

class Regs(admin.ModelAdmin):
    list_display = ['user_name', 'roll_number']


admin.site.register(Regulation, Reg)
admin.site.register(Department, Dept)
admin.site.register(Student, Std)
admin.site.register(Re,Regs)
