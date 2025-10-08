from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.order.serializers import OrderSerializer, OrderHistorySerializer, OrderStatusSerializer
from app.order.models import Order, Item


@extend_schema(tags=['Order'])
class AllOrderAPIView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, ]


@extend_schema(tags=['Order'])
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Order'])
class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderSerializer

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(instance=order, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({'message': "Order has been deleted!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Order'])
class OrderCancelAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        order_id = pk
        user = request.user
        order = get_object_or_404(Order, id=order_id)
        if order.user != user:
            data = {
                'success': False,
                'status_code': 400,
                'message': 'You do not own this order'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if order.status == Order.OrderStatus.Pending:
            order.status = Order.OrderStatus.Cancelled
            order.save()
            data = {
                'success': True,
                'status_code': 200,
                'message': 'Order status has been changed successfully',
                'order': {
                    'id': order.id,
                    'status': order.status
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'success': False,
                'status_code': 400,
                'message': "You can't change your order status"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Order'])
class OrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderStatusSerializer

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusSerializer(instance=order, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Order'])
class OrderHistoryAPIView(ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')
