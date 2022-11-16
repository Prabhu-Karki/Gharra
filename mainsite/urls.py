from urllib import request
from wsgiref.util import request_uri
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import *


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),

    #Accounts
    path('signins/', views.signin, name='signins'),
    path('signups/', views.signup, name='signups'),
    path('signout/', views.signout, name='signout'),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),

    

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForms, extra_context={'active': 'nav-link'},success_url='/passwordchangedone/'),  name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html', extra_context={'active': 'nav-link'},), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user-reset-password.html', form_class=MyPasswordResetForm, extra_context={'active': 'nav-link'},), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html', extra_context={'active': 'nav-link'},), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm, extra_context={'active': 'nav-link'},), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset-complete.html', extra_context={'active': 'nav-link'},), name='password_reset_complete'),

    path('iphone/', views.iphone, name='iphone'),
    path('macbook/', views.macbook, name='macbook'),
    path('iphone/', views.ipad, name='ipad'),

    #Cart Related
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('pluscart/', views.plus_cart), 
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart), 

    path('productdetail/<int:pk>/', views.ProductDetailView.as_view(), name='productdetail'),
    path('review_rate/', views.review_rate, name='review_rate'),

    path('checkout/', views.checkout, name='checkout'),     
    path('address/', views.address, name='address'),

    path('create-user-account/', views.create_profile, name='create-user-account'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.editprofile, name='editprofile'),

    path('orders/', views.orders, name='orders'),
    path('paymentmethod/', views.payment_method, name='paymentmethod'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
