from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('menu-data/', views.menu_data, name='menu_data'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # or use LogoutView.as_view()
    path('signup/', views.signup, name='signup'),
]
