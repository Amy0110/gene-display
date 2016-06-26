from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from Searching import views as Searching_views
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SearchGene.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Searching_views.index, name='index'),
    url(r'^hgvs/$', Searching_views.searchhgvs, name='searchhgvs'),
    url(r'^symbol/$', Searching_views.searchsymbol, name='searchsymbol'),
    url(r'^medicine/$', Searching_views.searchmedicine, name='searchmedicine'),
    url(r'^text/$', Searching_views.TextAnalyse, name='TextAnalyse'),
       
    url(r'^display/$', Searching_views.display, name='display'),
    
    url(r'^hgvs_display1/$', Searching_views.hgvs_display1, name='hgvs_display1'),
    url(r'^hgvs_display2/$', Searching_views.hgvs_display2, name='hgvs_display2'),
    
    
    
    
    
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT},name='static'),
)
