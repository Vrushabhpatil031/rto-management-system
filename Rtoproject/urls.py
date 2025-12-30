"""Rtoproject URL Configuration

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
from rtoapp.views import *

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name="index"),
    path('mail/', mail, name="mail"),
    path('index_about/', index_about, name="index_about"),
    path('admin_login/', admin_login, name="admin_login"),
    path('logout_admin/', logout_admin, name="logout_admin"),
    path('rto_login/', rto_login, name="rto_login"),
    path('logout_rto/', logout_rto, name="logout_rto"),
    path('user_login/', user_login, name="user_login"),
    path('logout_user/', logout_user, name="logout_user"),
    path('rto_profile/', rto_profile, name="rto_profile"),
    path('user_profile/', user_profile, name="user_profile"),
    path('user_registration/', user_registration, name="user_registration"),
    path('rto_change_password/', rto_change_password, name="rto_change_password"),
    path('admin_change_password/', admin_change_password, name="admin_change_password"),
    path('user_change_password/', user_change_password, name="user_change_password"),
    path('dashboard/', dashboard, name="dashboard"),
    path('rto_dashboard/', rto_dashboard, name="rto_dashboard"),
    path('add_state/', add_state, name="add_state"),
    path('edit_state/<int:pid>/', add_state, name="edit_state"),
    path('delete_state/<int:pid>/', delete_state, name="delete_state"),
    path('view_state/', view_state, name="view_state"),
    path('add_city/', add_city, name="add_city"),
    path('edit_city/<int:pid>/', add_city, name="edit_city"),
    path('delete_city/<int:pid>/', delete_city, name="delete_city"),
    path('view_city/', view_city, name="view_city"),
    path('add_rto/', add_rto, name="add_rto"),
    path('edit_rto/<int:pid>/', add_rto, name="edit_rto"),
    path('delete_rto/<int:pid>/', delete_rto, name="delete_rto"),
    path('view_rto/', view_rto, name="view_rto"),
    path('add_learning_licence/', add_learning_licence, name="add_learning_licence"),
    path('edit_learning_licence/<int:pid>/', edit_learning_licence, name="edit_learning_licence"),
    path('delete_learning_licence/<int:pid>/', delete_learning_licence, name="delete_learning_licence"),
    path('view_learning_licence/', view_learning_licence, name="view_learning_licence"),
    path('add_driving_licence/', add_driving_licence, name="add_driving_licence"),
    path('edit_driving_licence/<int:pid>/', edit_driving_licence, name="edit_driving_licence"),
    path('delete_driving_licence/<int:pid>/', delete_driving_licence, name="delete_driving_licence"),
    path('view_driving_licence/', view_driving_licence, name="view_driving_licence"),
    path('detail/<int:pid>/', detail, name="detail"),
    path('learninglist/', learninglist, name="learninglist"),
    path('drivinglist/', drivinglist, name="drivinglist"),
    path('learning_detail/<int:pid>/', learning_detail, name="learning_detail"),
    path('detail2/<int:pid>/', detail2, name="detail2"),
    path('driving_detail/<int:pid>/', driving_detail, name="driving_detail"),
    path('rto_search_ll/', rto_search_ll, name="rto_search_ll"),
    path('rto_search_dl/', rto_search_dl, name="rto_search_dl"),
    path('rto_user_ll/', rto_user_ll, name="rto_user_ll"),
    path('rto_user_dl/', rto_user_dl, name="rto_user_dl"),
    path('admin_search_ll/', admin_search_ll, name="admin_search_ll"),
    path('admin_search_dl/', admin_search_dl, name="admin_search_dl"),
    path('reg_user/', reg_user, name="reg_user"),
    path('driving_licence/<int:pid>/', driving_licence, name="driving_licence"),
    path('learning_licence/<int:pid>/', learning_licence, name="learning_licence"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('admin_user_ll/', admin_user_ll, name="admin_user_ll"),
    path('admin_user_dl/', admin_user_dl, name="admin_user_dl"),
    path('add_contact/', add_contact, name="add_contact"),
    path('edit_contact/<int:pid>/', edit_contact, name="edit_contact"),
    path('contactlist/', contactlist, name="contactlist"),
    path('delete_contact/<int:pid>/', delete_contact, name="delete_contact"),
    path('city/', city, name="city"),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
