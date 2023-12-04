"""
URL configuration for bitsey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from browse import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from home import views as home
from browse import views as browse
from user import views as userviews
from order import views as orderviews
from system import views as systemviews

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('user/', include('user.urls')),
    #path('home/', include('home.urls')),



    path('', home.home, name='homepage'),
    path('browse', browse.browse, name='browse'),
    path('browse/<int:game_id>', browse.game_detail, name='game_Details'),
    path('signin/', userviews.signin, name='signin'),
    path('signup/', userviews.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),


    path('cart/', orderviews.view_cart, name='cart'),



    path('account/<int:user_id>/', userviews.edit_user, name='edit_user'),
    path('addToCart/<int:gameId>/', browse.addToCart, name='add_to_cart'),
    path('removeFromCart/<int:cartItemId>/', orderviews.remove_from_cart, name="remove_from_cart" ),
    path('GetNumberOfCartItem/', orderviews.GetNumberOfCartItem,  name="get_number_of_cart_item" ),
    path('search/', browse.search_for_game, name='search_for_game'),
    path('userDataViewer', userviews.userDataViewer),
    path('get_game_platform_data/<int:gameId>/', browse.get_game_platform_data, name='get_data'),
    path('wishlist/', userviews.view_wishlist, name='wishlist_view'),
    path('wishListItem/', userviews.WishListItemCreate, name='wishListItem'),
    
    path('notifications/', systemviews.GetUserNotifications, name="get_notifications"),
    path('notifications/Delete/<int:notificationId>/', systemviews.DeleteSpecificNotification, name="delete_specific_notifications"),
    path('notifications/Read/', systemviews.ReadNotification, name="read_notifications"),

    path('notifications/anyUnread/', systemviews.AnyUnreadNotification, name="any_unread_notifications"),

    path('notifications/DeleteAll/', systemviews.DeleteAllNotification, name="delete_all_notifications"),

    path('convert-cart-to-order/', orderviews.convert_cart_to_order, name='convert_cart_to_order'),
    path('purchaseHistory/', userviews.view_purchase_history, name='view_purchase_history'),
    path('UpdateCartItemQuantity/', orderviews.UpdateCartItemQuantity, name='update_cart_item_quantity'),
    path('removeFromWishlist/<int:wishListItemId>/', userviews.remove_from_wishList, name='remove_from_wishlist'),

   #path('send_email/', systemviews.send_email, name='send_email'),
    path('Support/', systemviews.Support, name='support_page'),


    path('searchfilter/', browse.SearchFilter, name="SearchFilter"),


    

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)