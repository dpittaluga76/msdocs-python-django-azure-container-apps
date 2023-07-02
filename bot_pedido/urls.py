from django.urls import path
from .views import OrderImportView

urlpatterns = [
    path('import_order/', OrderImportView.as_view(), name='import_order'),
    # other urls...
]