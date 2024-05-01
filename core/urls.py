
from django.urls import path
from . import views


urlpatterns = [
    path('',views.HomePageView.as_view(),name='homepage'),
    path('detail/<str:item_type>/<int:pk>/', views.ItemDetailView.as_view(), name='detail_view'),
    path('try-on/<str:item_type>/<int:pk>/', views.TryOnView.as_view(), name='try_on_page'),
]