"""
URL configuration for PaisaKeeper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from budget import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("api/expenses",views.ExpenseViewSetView,basename="expenses")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/",views.SignupView.as_view()),
    path("api/v2/expenses/<int:pk>/",views.ExpenseDetailView.as_view()),

    path("api/v1/income/",views.IncomeListCreateView.as_view()),
    path("api/v1/income/<int:pk>/",views.IncomeDetailView.as_view()),
    path("api/v1/summary/",views.TransactionSummaryView.as_view()),



]+router.urls
