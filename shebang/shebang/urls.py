from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

from oneroom import views

urlpatterns = [
    # index page    
    url(r'^$', lambda request: redirect('oneroom:index'), name='root'),
    
    # oneroom app 
    url(r'^oneroom/', include('oneroom.urls', namespace='oneroom')),

    # user app
    url(r'^account/', include('account.urls', namespace='account')),
     
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # summernote
    url(r'^summernote/', include('django_summernote.urls')),
]

# static
urlpatterns += static(settings.STATIC_URL, 
                      document_root=settings.STATIC_ROOT)

