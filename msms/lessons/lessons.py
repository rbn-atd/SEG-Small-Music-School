from models import *
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Given the studentUser id, and the teacherUser id, calculate the cost of each lesson and create a new invoice for the studentUser

# Take a request object and create a new invoice for the studentUser
def convertRequestToInvoice(request):
    # Get the studentUser
    studentUser = request.user
    # Get the teacherUser
    teacherUser = request.teacher
    # Get the number of lessons
    numLessons = request.numLessons
    # Get the cost per lesson
    costPerLesson = teacherUser.costPerHour
    # Calculate the total cost
    totalCost = costPerLesson * numLessons
    # Create a new invoice
    # Invoice number must be in the format of "UUU-IIII" where UUU is the usersID and IIII is the invoiceID
    if len(str(studentUser.id)) == 1:
        studentID = "00" + str(studentUser.id)
    elif len(str(studentUser.id)) == 2:
        studentID = "0" + str(studentUser.id)
    else:
        studentID = str(studentUser.id)
    if len(str(Invoice.objects.count() + 1)) == 1:
        invoiceID = "000" + str(Invoice.objects.count() + 1)
    elif len(str(Invoice.objects.count() + 1)) == 2:
        invoiceID = "00" + str(Invoice.objects.count() + 1)
    elif len(str(Invoice.objects.count() + 1)) == 3:
        invoiceID = "0" + str(Invoice.objects.count() + 1)
    else:
        invoiceID = str(Invoice.objects.count() + 1)
    invoiceNumber = studentID + "-" + invoiceID
    invoice = Invoice.objects.create(user_id=studentUser, cost = totalCost,paid = False, date_created = datetime.datetime.now(), date_due = datetime.datetime.now() + datetime.timedelta(days=30), invoice_number = invoiceNumber)
    invoice.save()

    request.status = True

    request.save()


