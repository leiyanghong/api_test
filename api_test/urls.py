
from django.contrib import admin
from django.urls import path,include,re_path


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('v01/', include('guoya_api.urls')),
]
