from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('user.urls', 'user'), namespace='user')),
    path('', include(('pages.urls', 'pages'), namespace='pages')),
]
