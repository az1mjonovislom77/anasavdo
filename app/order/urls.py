from django.urls import path

from app.order.views import OrderCreateAPIView, OrderCancelAPIView, OrderHistoryAPIView, OrderDetailAPIView, \
    AllOrderAPIView, OrderStatusAPIView

urlpatterns = [
    path('all/', AllOrderAPIView.as_view(), name='order-create'),
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('status/<int:pk>/', OrderStatusAPIView.as_view(), name='order-status'),
    path('cancel/<int:pk>/', OrderCancelAPIView.as_view(), name='order-cancel'),
    path('history/', OrderHistoryAPIView.as_view(), name='order-history'),
]
