from django.conf.urls import url, include
from bigbucketapp import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='MyApi')),
    url(r'^register/',views.UserCreateAPIView.as_view(), name='register'),
    url(r'^login/',views.UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/',views.UserLogoutAPIView.as_view(), name='logout'),
    url(r'^product/create/',views.ProductCreateView.as_view(), name='product-create'),
    url(r'^product/all/',views.ProductListAPIView.as_view(), name='product-all'),
    url(r'^product/edit/(?P<pk>[0-9]+)',views.ProductUpdateAPIView.as_view(), name='product-edit'),
    url(r'^product/detail/(?P<pk>[0-9]+)',views.ProductRetrieveAPIView.as_view(), name='product-detail'),
    url(r'^product/buy/(?P<pk>[0-9]+)',views.ProductBuyAPIView.as_view(), name='buy-product'),
    url(r'^product/addtocart/(?P<pk>[0-9]+)',views.AddToCartAPIView.as_view(), name='add-to-cart'),

]