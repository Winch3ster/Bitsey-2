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
from django.urls import path
from browse import views
from django.conf import settings
from django.conf.urls.static import static
from home import views as home
from browse import views as browse
from user import views as userviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home),
    path('browse', browse.browse),
    path('browse/<int:game_id>', browse.game_detail),
    path('signin/', userviews.signin, name='signin'),
    path('signup/', userviews.signup, name='signup'),
    path('cart/', userviews.cart, name='cart'),
    path('account/<int:user_id>/', userviews.edit_user, name='edit_user'),
    path('userDataViewer', userviews.userDataViewer)
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)