from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip_list'),
    path('trip/new/', views.TripCreateView.as_view(), name='trip_create'),
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_update'),
    path('trip/<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),

    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]
