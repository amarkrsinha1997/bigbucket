from django.conf.urls import url, include
from bigbucketapp import views
urlpatterns = [
    # url(r'^login/',views.login,name='login'),
    url(r'^register/',views.RegistrationView.as_view(), name='register'),
]
