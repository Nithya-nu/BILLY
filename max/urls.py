from django.urls import path
from.import views
urlpatterns=[
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/<int:id>/', views.edit_profile, name='edit_profile'),
    path('add-product/', views.add_product, name='add_product'),
    path('product-list/', views.product_list, name='product_list'),

]
    