"""NurtureHealth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from NurtureHealthApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeP,name="Homes"),
    path('ContactUS/',views.ContactUS,name="ContactUS" ),
    path('Departments/',views.Departments,name="Departments" ),
    path('doctor-profile/',views.doctor_profile,name='doctor_profile'),
    path('HeadFoot/',views.HeadFoot ),
    path('Review/',views.Review,name="Review" ),
    path('AboutUS/',views.AboutUS,name="AboutUS"),
    path('doctors/',views.doctors,name="doctors"),
    path('all-doctors/',views.all_doctors,name="all_doctors"),
    path('SignUp/',views.SignUp,name="SignUp"),
    path('ForgPassword/',views.ForgPassword,name="ForgPassword"),
    path("check_user/",views.check_user,name="check_user"),
    path("login_page/",views.login_page,name="login_page"),
    path("doctor_dashboard",views.doctor_dashboard,name="doctor_dashboard"),
    path("patient_dashboard",views.patient_dashboard,name="patient_dashboard"),
    path('profile-mypatients/',views.profile_mypatients,name='profile_mypatients'),
    path("user_logout",views.user_logout,name="user_logout"),
    path("edit_profile",views.edit_profile,name="edit_profile"),
    path("change_password",views.change_password,name="change_password"),
    path("add_treatment",views.add_treatment_view,name="add_treatment_view"),
    path("my_treatments",views.my_treatments,name="my_treatments"),
    path("single_treatment",views.single_treatment,name="single_treatment"),
    path("update_treatment",views.update_treatment,name="update_treatment"),
    path("delete_treatment",views.delete_treatment,name="delete_treatment"),
    path("all_treatments",views.all_treatments,name="all_treatments"),
    path("sendemail",views.sendemail,name="sendemail"),
    path("forgotpass",views.forgotpass,name="forgotpass"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("cart",views.add_to_cart,name="cart"),
    path("get_chart_data",views.get_chart_data,name="get_chart_data"),
    path("change_quan",views.change_quan,name="change_quan"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path("process_payment",views.process_payment,name="process_payment"),
    path("payment_done",views.payment_done,name="payment_done"),
    path("payment_cancelled",views.payment_cancelled,name="payment_cancelled"),
    path("Feedback",views.Reviewpage,name="Reviewpage"),
    path("treatment_history",views.treatment_history,name="treatment_history"),
    path("profile_reviews",views.profile_reviews,name="profile_reviews"),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
