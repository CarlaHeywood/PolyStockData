from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/', include("backend.urls")),
    path("stock/",views.StockListCreate.as_view(), name="stock-view-create"),
    path("stock/<str:symbol>/", views.StockRetrieveUpdateDestroy.as_view(), name="stock-update")
]