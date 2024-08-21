from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User, Request, Term, Invoice
import datetime

class Command(BaseCommand):    

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    # generates 100 dummy user accounts for the database
    def handle(self, *args, **options):
        user_count=0
        
        while user_count != 100:
            print(f' > {user_count}/100',  end='\r')
            try:
                self.create_user()
                
            except (django.db.utils.IntegrityError):
                continue
            user_count +=1
        print('Database seeded with 100 dummy users')

        self.create_required_user("John", "Doe", 1)
        self.create_required_user("Petra", "Pickles", 2)
        self.create_required_user("Marty", "Major", 3)

        print('----------------------------------------')
        print('Database seeded with 3 required accounts')

        self.create_terms(1, datetime.date(2022,9,1), datetime.date(2022,10,21))
        self.create_terms(2, datetime.date(2022,10,31), datetime.date(2022,12,16))
        self.create_terms(3, datetime.date(2023,1,3), datetime.date(2023,2,10))
        self.create_terms(4, datetime.date(2023,2,20), datetime.date(2023,3,31))
        self.create_terms(5, datetime.date(2023,4,17), datetime.date(2023,5,26))
        self.create_terms(6, datetime.date(2023,6,5), datetime.date(2023,7,21))

        print('----------------------------------------')
        print('Database seeded with 6 terms')

    # function specifically to generate the 3 required users as per the seeder/unseeder specification - R
    def create_required_user(self, first_name, last_name, user_type):

        username = self.create_email(first_name, last_name)

        # user_type is used to set whether the staff and superuser fields are true or not
        if(user_type==3): 
            is_staff=True
            is_superuser=True 
        elif (user_type==2): 
            is_staff = True
            is_superuser = False
        else: 
            is_staff=False
            is_superuser=False

        user = User.objects.create_user(
            username,
            user_type = user_type,
            first_name=first_name,
            last_name=last_name,
            password="Password123",
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        if(user_type==1):
            self.create_requests(user)

    def create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self.create_email(first_name, last_name)
        user = User.objects.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password="Password123"
        )
        self.create_requests(user)


    def create_email(self, first_name, last_name):
        email = f'{first_name}{last_name}@example.org'
        return email

    def create_requests(self, user):

        Request.objects.create(
            user = user,
            availability = 'Monday',
            number_Of_Lessons = '3',
            length = '60 mins',
            interval = 'every 2 weeks',
            body = 'i want to learn music',
            status = False,
        )

        accepted_request = Request.objects.create(
            user = user,
            availability = ['Saturday', 'Sunday'],
            number_Of_Lessons = '2',
            length = '90 mins',
            interval = 'every week',
            body = 'i want to learn music',
            status = True,
        )
        self.create_invoice(accepted_request, user)


    def create_terms(self, num, start, end):
        Term.objects.create(
            term_number=num,
            start_date=start,
            end_date=end
        )

    def create_invoice(self, request, user):
        Invoice.objects.create(
            accepting_admin='PetraPickles@example.org',
            request = request,
            cost=15,
            paid=False,
            invoice_number=f'{user.id}-000'
            )

