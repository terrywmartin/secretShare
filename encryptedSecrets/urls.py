from django.contrib import admin
from django.urls import path

from . import views

app_name = 'encryptedSecrets'

urlpatterns = [
    path('secrets/', views.SecretsViewSecrets.as_view(),name='secrets'),
    path('secrets/<uuid:pk>', views.SecretsViewSecret.as_view(),name='secret_view'),
    path('secrets/share/<uuid:pk>', views.SecretsShareSecret.as_view(),name='secret_share_view'),
    path('secrets/edit/<uuid:pk>', views.SecretsEditSecret.as_view(),name='secret_edit'),
    path('secrets/delete/<uuid:pk>', views.SecretsDeleteSecret.as_view(),name='secret_delete'),
    path('secrets/add-secret/', views.SecretsAddSecret.as_view(),name='secret_add'),
]
