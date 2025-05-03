from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('qr/', views.generate_qr, name='generate_qr'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('cafes/', views.cafe_view, name='cafe_list'),
    path('cafes/<int:cafe_id>/', views.menu_view_by_id, name='cafe_menu_by_id'),
    path('cafes/<slug:cafe_slug>/', views.menu_view, name='cafe_menu'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('contact-submit/', views.contact_form_submit, name='contact_submit'),
]
