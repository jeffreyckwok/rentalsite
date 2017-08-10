from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    # url(r'^admin$', views.admin, name="admin"),
    url(r'^search$', views.search, name = "search"),
    url(r'^rentals$', views.rentals, name="rentals"),
    url(r'^account$', views.account, name="account"),
    url(r'^addtocart$', views.addtocart, name="addtocart"),
    url(r'^addreservation$', views.addreservation, name="addreservation"),
    url(r'^cart$', views.cart, name ="cart"),
    url(r'^checkout$', views.checkout, name="checkout"),
    url(r'^thankyou$', views.thankyou, name="thankyou"),
    url(r'^info/(?P<id>\d+)?$', views.info, name="info"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
