from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, ContactForm, CreateNewAdminForm, SearchAdminForm, EditAdminForm, TermForm
from lessons.models import  Request, Term, Invoice, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .helpers import login_prohibited, student_prohibited, admin_prohibited

def home(request): 
    return render(request, 'log_in.html')

def placeholder(request):
    return render(request, 'placeholder.html')

@login_prohibited
def log_in(request):
    if request.method=='POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if(user.is_staff==True):
                    return redirect('admin_home')
                else:
                    return redirect('student_home')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_home')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
@student_prohibited
def display_students(request):
    users = User.objects.all().filter(user_type='1')
    return render(request, 'admin_view_students.html', {'users':users})

@login_required
@admin_prohibited
def student_home(request):
    return render(request, 'student_home.html')

@login_required
@admin_prohibited
def student_profile(request):
    return render(request, 'student_profile.html')

@login_required
@admin_prohibited
def displayRequests(request):
    requests = Request.objects.all().filter(user = request.user)
    pending_requests = Request.objects.all().filter(user = request.user).filter(status = False)
    accepted_requests = Request.objects.all().filter(user = request.user).filter(status = True)
    return render(request, 'user_requests.html', {'pending_requests':pending_requests, 'accepted_requests':accepted_requests})

@login_required
def display_all_requests(request):
    requests = Request.objects.all()
    return render(request, 'admin_view_student_requests.html', {'requests':requests})

@login_required
def contact(request):

    if request.POST:
        form = ContactForm(request.POST)
        #print(form.errors) checks to see what is causing form to be invalid
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('requests_list')

    form = ContactForm()
    return render(request, 'form.html', {'form' : form})

@login_required
def update_request(request, pk):

    #first need a check to see whether status of request is still pending or accepted
    requests = Request.objects.get(id = pk)
    form  = ContactForm(instance = requests)

    if request.POST:
        form = ContactForm(request.POST, instance = requests)
        if form.is_valid():
            form.save()
            return redirect('requests_list')
    return render(request, 'form.html', {'form' : form})

# update request to be used by admin users
# it finds the relevant request object via the id parameter and opens up its instance of the contact form for editing
# a try catch exception for an ObjectDoesNotExist error is used, if the request  has an associated invoice,
# update its request foreign key field with the new saved request, else, pass
@login_required
def admin_update_request(request, pk):

    requests = Request.objects.get(id = pk)
    form  = ContactForm(instance = requests)
    
    if request.POST:
        form = ContactForm(request.POST, instance = requests)
        if form.is_valid():
            form.save()
            try:
                invoice = Invoice.objects.get( request__id = pk )
                invoice.request = requests
                invoice.save()
            except ObjectDoesNotExist:
                pass
            return redirect('admin_view_requests')
    return render(request, 'admin_form.html', {'form' : form})

@login_required
def delete_request(request, pk):

    #first need a check to see whether status of request is still pending or accepted

    requests = Request.objects.get(id=pk)

    if request.POST:
        requests.delete()
        return redirect('requests_list')
    return render(request, 'delete_confirmation.html')

#for when admins accept and confirm a booking request
#receives the id of a specific request and toggles the status boolean field to be True so
# that is marked as 'Accepted'
# An associated invoice object is also created which takes the current request as a foreign key reference
# COST NEEDS TO BE CALCULATED PROPERLY - R
@login_required
def accept_request(request, pk):
    requests = Request.objects.get(id=pk)
    user = requests.user
    if request.POST:
        requests.status=True
        requests.save()
        invoice = Invoice.objects.create(
            request = requests,
            accepting_admin=request.user.username,
            cost=15,
            paid=False,
            invoice_number=f'{user.id}-{requests.id}'
            )
        invoice.save()

        return redirect('admin_view_requests')
    return render(request, 'admin_booking.html')

@login_required
def request_page(request):
    form = ContactForm()
    return render(request, 'user_requests.html', {'form': form})
  
@login_required
def request_list(request):
    return render(request, 'requests_list')

# ADMIN VIEWS
@login_required
@student_prohibited
def admin_home(request):
    return render(request, 'admin_home.html')

#Create admin view
@login_required
@student_prohibited
def create_admin(request):
    if request.method == 'POST':
        form = CreateNewAdminForm(request.POST)
        if form.is_valid():
            admin = form.save()
            return redirect('admin_home')
    else:
        form = CreateNewAdminForm()
    return render(request, 'create_admin.html', {'form': form})

#Search admin view
@login_required
def search_admin(request):
    form = SearchAdminForm()
    return render(request, 'search_admin.html', {'form': form})

#Filters for a specific admin user if searched, or displays all admin users
@login_required
def edit_delete_admin(request):
    query = request.GET.get("q")
    if (query == None):
        admin_users = User.objects.all().filter(user_type = '2')
        return render(request, 'edit_delete_admin.html', {'admin_users':admin_users})
    else: 
        admin_users = User.objects.all().filter(username=query)
        return render(request, 'edit_delete_admin.html', {'admin_users':admin_users})

@login_required
def edit_admin(request):
    form = EditAdminForm()
    return render(request, 'edit_admin.html', {'form': form})

@login_required
#Deletes a specific admin user
def delete_admin(request, pk):
    admin_user = User.objects.get(username=pk)
    if request.POST:
        admin_user.delete()
        return redirect('search_admin')
    return render(request, 'delete_admin.html')

# def admin_view_students(request):
#     form = AdminViewStudentsForm()
#     return render(request, 'admin_view_students.html', {'form': form})

# def admin_view_requests(request):
#     form = AdminViewRequestsForm()
#     return render(request, 'admin_view_student_requests.html', {'form': form})

# TERM VIEWS
# creates term object using data extracted from the term form
# redirects back to term list view after successful creation
@login_required
@student_prohibited
def create_term(request):
    if request.method == 'POST':
        form=TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('term_list')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid")

    else:
        form = TermForm()
    return render(request, 'create_term.html', {'form': form})

# creates and returns a list of all existing term objects to be displayed on the term list view
@login_required
@student_prohibited
def display_terms(request):
    terms = Term.objects.all()
    return render(request, 'term_list.html', {'terms':terms})

# gets relevant term object via the id parameter and opens up its instance of the term form for editing
@login_required
def edit_term(request, pk):
    term = Term.objects.get(id = pk)
    form  = TermForm(instance = term)
    if request.POST:
        form = TermForm(request.POST, instance = term)
        if form.is_valid():
            form.save()
            return redirect('term_list')
    return render(request, 'create_term.html', {'form' : form})

# gets relevant term object via the id parameter and deletes it from the database
@login_required
def delete_term(request, pk):

    term = Term.objects.get(id=pk)

    if request.POST:
        term.delete()
        return redirect('term_list')
    return render(request, 'term_confirm_delete.html')

# creates and returns the invoice object associated with the request id parameter to be viewed
@login_required
def display_invoice(request, pk):
    invoice = Invoice.objects.get( request__id = pk )
    return render(request, 'student_invoices.html', {'invoice':invoice})

@login_required
@admin_prohibited
def display_invoice_cost(request):
    invoices = Invoice.objects.all().filter(request__user = request.user)
    total = 0
    for i in invoices:
        total += i.cost
    return render(request, 'your_transactions.html', {'invoices':invoices, 'total':total})

@login_required
@student_prohibited
def display_incoming_transactions(request):
    invoices = Invoice.objects.all()
    return render(request, 'incoming_transactions.html', {'invoices':invoices})

