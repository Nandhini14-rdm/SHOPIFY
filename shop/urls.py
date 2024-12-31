from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
    path('item/<int:product_id>/', views.item_detail, name='item_detail'),
    path('payment/<int:product_id>/', views.payment_view, name='payment'),


] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)