
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quiz_api.views import *
from rest_framework_simplejwt.views import *

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("invitations/", include('invitations.urls', namespace='invitations')),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apiv1/', include('quiz_api.urls')),
    path('export_action/', include("admin_export_action.urls",
         namespace="admin_export_action")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
