from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField





#User model implementation
# The user model should have the following fields: username(as email), user_type, password, first_name and last_name
# username should be an EmailField that is unique and not blank or false, it has a verbose name 'Email' so is represented to the user as Email
# user_type should be a PositiveSmallIntegerField where the integer represent a value in a set of options, it should default to a student role
# password should be a CharField with a max length of 50 that is not null
# first_name should be a CharField with a max length of 50 that is not null
# last_name should be a CharField with a max length of 50 that is not null

class User(AbstractUser):
    USER_TYPE =(
        # an extra user type 'dev' is added purely for the development and viewing
        # of the super user page and accessing the User database
        # This may be deleted following completion of the project - R
        (0, 'Dev'), 
        (1, 'Student'),
        (2, 'Admin'),
        (3, 'Director'),
    )
    
    # the default username field takes on the email, its verbose name is Email so that it appears
    # as Email when its form is displayed.
    username = models.EmailField('Email', unique=True, blank=False)

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE, default=1)

    first_name = models.CharField(max_length=50, unique=False, blank = False)

    last_name = models.CharField(max_length=50, unique=False, blank = False)

    # object function that appends firstname and lastname into a f string to display fullname
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Request(models.Model):
    OPTIONS = (('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = MultiSelectField(max_length=57, max_choices = 7,choices = OPTIONS)
    number_Of_Lessons = models.CharField(max_length = 1, choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9')], blank = False,default = '1')
    length = models.CharField(max_length = 7, choices = [('30 mins', '30 mins'), ('60 mins', '60 mins'), ('90 mins', '90 mins')], blank = False, default = '30 mins')
    interval = models.CharField(max_length = 13,choices = [('every week' , 'every week'), ('every 2 weeks', 'every 2 weeks'), ('every 3 weeks', 'every 3 weeks'), ('every 4 weeks', 'every 4 weeks')], blank = False, default = 'every week')
    body = models.TextField(max_length = 200, blank = True)
    status = models.BooleanField(default = False, blank = False)
    date = models.DateTimeField(auto_now = True)

# The Term model should have the following fields: term_number, start_date and end_date
# term_number should be a PositiveIntegerField which is unique
# start_date and end_date should both be DateFields
class Term(models.Model):
    term_number = models.PositiveIntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

# The Invoice model should have the following fields: request, accepting_admin, cost, paid, invoice_number, date
# request should be a ForeignKey field of a Request object in which the invoice is deleted when a request is deleted
# accepting_admin is a CharField which has a max_length of 50 and is neither null or unique
# cost is a DecimalField which is maximum 5 digits, has 2 decimal places and is not null
# paid is a BooleanField which is not null
# invoice_number is a CharField which has max_length of 50 and is neither null or unique
# date is a DateTimeField which is automatically assigned the current time
class Invoice(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    accepting_admin = models.CharField(max_length=50, null=False, unique=False)
    cost = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    paid = models.BooleanField(null=False)
    invoice_number = models.CharField(max_length=50, null=False, unique=True)
    date = models.DateTimeField(auto_now = True)



# Model for normal admin staff
# class AdminStaff(models.Model):
#     username = models.EmailField('Email', unique=True, blank=False)

#     first_name = models.CharField(max_length=50, unique=False, blank = False)

#     last_name = models.CharField(max_length=50, unique=False, blank = False)

#     is_staff = True

#     is_super_user = False

# Model for a super admin user
# class SuperAdminStaff(models.Model):
#     username = models.EmailField('Email', unique=True, blank=False)

#     first_name = models.CharField(max_length=50, unique=False, blank = False)

#     last_name = models.CharField(max_length=50, unique=False, blank = False)

#     is_staff = True

#     is_super_user = True




# class Lesson(models.Model):
#     Date = models.DateTimeField()
#     Time = models.DateTimeField()
#     Duration = models.IntegerField()
#     StudentID = models.ForeignKey( User.id, on_delete=models.CASCADE)
#     ApprovalID = models.ForeignKey('approvals.Approval', on_delete=models.CASCADE)
#     RequestApproval = models.BooleanField()
#     Instrument = models.CharField(max_length=50)
#     # TeacherID = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
#     InvoiceReference = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('Date', 'Time', 'StudentID')

#     class Meta:
#         unique_together = ('Date', 'Time', 'TeacherID')

#     def __str__(self):
#         return self.Date



# The teacher model should have the following fields: TeacherID (Which is a foreign key to the user model), Instrument, and CostPerHour

# TeacherID should be a foreign key to the user model
# Instrument should be a CharField with a max length of 50 that is not null
# CostPerHour should be a decimal field with a max digits of 5 and a decimal places of 2

# class Teacher(models.Model):
#     TeacherID = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     Instrument = models.CharField(max_length=50, null=False)
#     CostPerHour = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return self.TeacherID

# The invoice model should have the following fields: InvoiceID, InvoiceDate, UserID, cost, paid, and invoice_number

# InvoiceID should be an integer field that is the primary key and auto increments
# InvoiceDate should be a DateTime field that is not null
# UserID should be a foreign key to the user model that is not null
# cost should be a decimal field with a max digits of 5 and a decimal places of 2 that is not null
# paid should be a boolean field that is not null
# Invoice number should be a CharField with a max length of 50 that is not null and unique that follows the format of "UUU-IIII" where UUU is the usersID and IIII is the invoiceID


# class Invoice(models.Model):
#     invoice_date = models.DateTimeField(null=False)
#     # For the user ID ensure that the user is a student and not a teacher or admin therefore the user type must be 1
#     user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, limit_choices_to={'user_type': 1})
#     cost = models.DecimalField(max_digits=5, decimal_places=2, null=False)
#     paid = models.BooleanField(null=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_due = models.DateTimeField(null=False)
#     invoice_number = models.CharField(max_length=50, null=False, unique=True, validators=[RegexValidator(regex='^.{3}-\d{4}$', message='Invoice number must be in the format of "UUU-IIII" where UUU is the usersID and IIII is the invoiceID', code='nomatch')])

#     def __str__(self):
#         return self.InvoiceNumber




#     def __str__(self):
#         return self.Invoice_number


