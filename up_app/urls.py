from django.urls import path
from up_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
                  path('parse/', views.parse, name='parse'),
                  path('filter123/', views.filter123, name='filter123'),
                  path('test/', views.test, name='test'),
                  path('catalog/', views.catalog, name='catalog'),
                  path('plan/', views.plan, name='plan'),
                  path('product_add/', views.product_add, name='product_add'),
                  path('product_change/', views.product_change, name='product_change'),
                  path('get_delivery/<int:pk>', views.get_delivery, name='get_delivery'),
                  path('cart/', views.cart, name='cart'),
                  path('cart/delete/<int:pk>', views.cart_delete, name='cart_delete'),
                  path('', views.product_list, name='product_list'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
