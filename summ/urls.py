from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.summ, name='summ'),
    path('text', views.text, name='text'),
    path('textop', views.textop, name='textoutput'),
    path('admin/', admin.site.urls),
    path('audio', views.audio , name="audio"),
    path('portfolio', views.portfolio , name="audio"),
    path('audioop', views.audioop , name='audiooutput'),
    path('send_mail', views.send_mail , name='sendmail'),
    path('video', views.video , name="audio"),
    path('vidop', views.vidop , name="audio"),
    path('wiki', views.wiki , name="audio"),
    path('wikiop', views.wikiop , name="audio"),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
