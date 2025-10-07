from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.product.models import Category, Product, Comment, CategoryImages, ProductImage, ProductColor, ProductValue, \
    ProductType
from app.product.serializers import CategorySerializer, ProductSerializer, AllProductSerializer, CommentSerializer, \
    CategoryImagesSerializer, ProductImageSerializer, ProductColorSerializer, ColorSerializer, ProductValueSerializer, \
    ProductTypeSerializer, ProductGetSerializer, CategoryGetSerializer, ColorGetSerializer, ProductTypeGetSerializer
from app.user.validations import IsAdminOrSuperAdmin, IsAdminOrOwner
from app.utils.models import Color


@extend_schema(tags=['Category'])
class CategoryAPIView(APIView):
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        category = Category.objects.filter(is_active=True)
        serializer = CategoryGetSerializer(category, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Category'])
class CategoryDetailAPIView(APIView):
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryGetSerializer(category, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        if category.is_active:
            category.is_active = False
            category.save()
        else:
            return Response({'message': "Category is not active"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Category successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Product'])
class AllProductAPIView(ListAPIView):
    serializer_class = AllProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            return Product.objects.filter(is_active=True, category__slug=name)
        else:
            return Product.objects.filter(is_active=True)


@extend_schema(tags=['Product'])
class ProductAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]


@extend_schema(tags=['Product Image'])
class ProductImageAPIView(CreateAPIView):
    permission_classes = [IsAdminOrSuperAdmin]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


@extend_schema(tags=['Product Image'])
class ProductImageDetailAPIVIew(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ProductImageSerializer

    def get(self, request, pk):
        product_image = ProductImage.objects.filter(product_id=pk)
        serializer = ProductImageSerializer(product_image, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product_image = get_object_or_404(ProductImage, pk=pk)
        serializer = ProductImageSerializer(instance=product_image, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_image = get_object_or_404(ProductImage, pk=pk)
        product_image.delete()
        return Response({"message": "Product color successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Product features'])
class ProductFeaturesAPIView(ListCreateAPIView):
    permission_classes = [IsAdminOrSuperAdmin]
    queryset = ProductValue.objects.all()
    serializer_class = ProductValueSerializer


@extend_schema(tags=['Product features'])
class ProductFeaturesDetailAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ProductValueSerializer

    def put(self, request, pk):
        product_feature = get_object_or_404(ProductValue, pk=pk)
        serializer = ProductValueSerializer(instance=product_feature, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_features = get_object_or_404(ProductValue, pk=pk)
        product_features.delete()
        return Response({'message': "Product feature successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Product type'])
class ProductTypeAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ProductTypeSerializer

    def get(self, request):
        product_type = ProductType.objects.all()
        serializer = ProductTypeGetSerializer(product_type, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Product type'])
class ProductTypeDetailAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ProductTypeSerializer

    def put(self, request, pk):
        product_type = get_object_or_404(ProductType, pk=pk)
        serializer = ProductTypeSerializer(instance=product_type, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_type = get_object_or_404(ProductType, pk=pk)
        product_type.delete()
        return Response({'message': 'Product type successfully deleted!'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Color'])
class ColorAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ColorSerializer

    def get(self, request):
        color = Color.objects.all()
        serializer = ColorGetSerializer(instance=color, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ColorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Color'])
class ColorDetailAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ColorSerializer

    def put(self, request, pk):
        color = get_object_or_404(Color, pk=pk)
        serializer = ColorSerializer(instance=color, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        color = get_object_or_404(Color, pk=pk)
        color.delete()
        return Response({'message': "Color successfully deleted!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Product color'])
class ProductColorsAPIView(ListCreateAPIView):
    permission_classes = [IsAdminOrSuperAdmin]
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer


@extend_schema(tags=['Product color'])
class ProductColorsDetailAPIView(APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    serializer_class = ProductColorSerializer

    def put(self, request, pk):
        product_color = get_object_or_404(Color, pk=pk)
        serializer = ProductColorSerializer(instance=product_color, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_colors = get_object_or_404(ProductColor, pk=pk)
        product_colors.delete()
        return Response({'message': "Product color successfully deleted!"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Product'])
class ProductDetailAPIView(APIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductGetSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_active:
            product.is_active = False
            product.save()
        else:
            return Response({'message': "Product is not active"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Product successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Product comment'])
class CreateCommentAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_active=True)


@extend_schema(tags=['Product comment'])
class DetailCommentAPIView(APIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            print('deleteee')
            return [IsAdminOrOwner()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, is_active=True)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.is_active:
            comment.is_active = False
            comment.save()
        else:
            return Response({'message': "No comment available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Comment successfully deleted"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Product comment'])
class ListCommentAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Comment.objects.filter(is_active=True, product_id=pk)


class ProductByCategoryAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, slug):
        category = get_object_or_404(Category.objects.prefetch_related('products'), slug=slug)
        products = category.products.all()
        images = CategoryImages.objects.filter(category__slug=slug)

        product_data = ProductSerializer(products, many=True, context={"request":request}).data
        images_data = CategoryImagesSerializer(images, many=True).data

        data = {
            'products': product_data,
            'images': images_data
        }
        return Response(data)


