from django import forms
from django.contrib.auth.models import User
from lessons.models import User, Request, Term, Invoice
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


class LogInForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['first_name', 'last_name', 'username']

    new_password = forms.CharField(label='Password', widget=forms.PasswordInput(), validators=[RegexValidator(
                                                            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                                                            message='Password must contain an uppercase character, a lowercase character and a number'
                                                        )]
                                                    )

    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())


    #clean override and save override fixes test error for unit test checking if password and confirmation are identical
    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if new_password!=password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password. ')

    def save(self):
        super().save(commit=False)
        user=User.objects.create_user(
                self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                password=self.cleaned_data.get('new_password')
            )
        return user

class ContactForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['availability','number_Of_Lessons', 'length', 'interval','body']

class CreateNewAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['first_name', 'last_name', 'username']
       
                                             
    new_password = forms.CharField(label=mark_safe('Default password: Password123<br />Retype here:'), widget=forms.PasswordInput(), validators=[RegexValidator(
                                                            regex=r'Password123',
                                                            message='Default password must be Password123'
                                                        )])

    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    # CHOICES = [
    #     ('super_admin','Admin'), 
    #     ('normal_admin', 'Director')]
    # admin_type=forms.CharField(label='Type of admin user:', widget=forms.RadioSelect(choices=CHOICES))

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password!=password_confirmation:
            self.add_error('new_password', 'Does not match the password confirmation. ')

    def save(self):
        super().save(commit=False)

        admin_user = User.objects.create_user(
            username=(self.cleaned_data.get('username')), 
            first_name=self.cleaned_data.get('first_name'), 
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('new_password'),
            user_type='2',
            is_staff=True
            )

        admin_user.save()
        return admin_user

class SearchAdminForm(forms.Form):
    search_username = forms.CharField(label="Enter username: ")

class EditAdminForm(forms.Form):
    pass


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields=['term_number','start_date','end_date']

    start_date=forms.DateField(widget=forms.SelectDateWidget())
    end_date=forms.DateField(widget=forms.SelectDateWidget())

    # clean override so that start date is always a lesser date than end date
    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")



# class InvoiceForm(forms.ModelForm):
#     class Meta:
#         model = Invoice
#         fields = ['request','cost', 'paid', 'invoice_number']





