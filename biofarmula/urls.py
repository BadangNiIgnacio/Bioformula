from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Badang ni Ignacio'
admin.site.index_title = 'Badang ni Ignacio Admin'
admin.site.site_title = 'BioFarmula Information System'

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
