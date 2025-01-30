from django.contrib import admin
from .models import *
from import_export.admin import ImportMixin



class Reg(admin.ModelAdmin):
    list_display = ['regulation']


class Dept(admin.ModelAdmin):
    list_display = ['department']

class Regs(admin.ModelAdmin):
    list_display = ['user_name', 'roll_number']


class StudentAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['roll_number',
                    'name',
                    'department',
                    'regulation',
                    'mobile_number',
                    'email']



admin.site.register(Regulation, Reg)
admin.site.register(Department, Dept)
admin.site.register(Re,Regs)
admin.site.register(Student, StudentAdmin)
