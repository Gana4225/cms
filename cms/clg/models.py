from django.db import models

class Regulation(models.Model):
    regulation = models.CharField(max_length=30)

    def __str__(self):
        return self.regulation

class Department(models.Model):
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.department

class Student(models.Model):
    roll_number = models.CharField(max_length=30,null=False)
    name = models.CharField(max_length=50,null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=False)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE,null=False)
    mobile_number = models.CharField(max_length=20,null=False)
    email = models.EmailField(max_length=250,null=False)

    def __str__(self):
        return f"{self.roll_number} {self.name} {self.department}"

# class for register the user
class Re(models.Model):
    user_name = models.CharField(max_length=250,null=False,)
    password = models.CharField(max_length=200,null=False)
    roll_number = models.CharField(max_length=30,null=False)
    mobile_number = models.CharField(max_length=20,null=False)


    def __str__(self):
        return f"{self.user_name} {self.roll_number}"