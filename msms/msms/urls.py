"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.log_in, name='log_in'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('search_admin/', views.search_admin, name='search_admin'),
    path('edit_delete_admin/', views.edit_delete_admin, name='edit_delete_admin'),
    path('edit_admin/', views.edit_admin, name='edit_admin'),
    path('delete_admin/<str:pk>', views.delete_admin, name='delete_admin'),
    path('admin_view_students/', views.display_students, name='admin_view_students'),
    path('admin_view_requests/', views.display_all_requests, name='admin_view_requests'),
    path('placeholder/', views.placeholder, name='placeholder'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_out/', views.log_out, name='log_out'),
    path('student_home/', views.student_home, name='student_home') ,
    path('student_profile/', views.student_profile, name='student_profile') ,
    path('request_form/', views.contact, name='request_form'),
    path('requests_list/', views.displayRequests, name='requests_list'),
    path('update_requests/<str:pk>/', views.update_request, name='update_requests'),
    path('admin_update_requests/<str:pk>/', views.admin_update_request, name='admin_update_requests'),
    path('delete_requests/<str:pk>/', views.delete_request, name='delete_requests'),
    path('admin_booking/<str:pk>/', views.accept_request, name='admin_booking' ),
    path('create_term', views.create_term, name='create_term'),
    path('term_list', views.display_terms, name='term_list'),
    path('edit_term/<str:pk>/', views.edit_term, name='edit_term'),
    path('term_confirm_delete/<str:pk>', views.delete_term, name = 'term_confirm_delete'),
    path('student_invoices/<str:pk>', views.display_invoice, name='student_invoices'),
    path('your_transactions/', views.display_invoice_cost, name = 'your_transactions'),
    path('incoming_transactions/', views.display_incoming_transactions ,name='incoming_transactions' )

]
