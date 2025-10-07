from django.urls import path

from app.product.views import CategoryAPIView, ProductAPIView, AllProductAPIView, CreateCommentAPIView, \
     ProductByCategoryAPIView, CategoryDetailAPIView, ProductDetailAPIView,  \
    ProductImageAPIView, ProductColorsAPIView, ColorAPIView, ProductFeaturesAPIView, ProductTypeAPIView, \
    ColorDetailAPIView, ProductImageDetailAPIVIew, ProductFeaturesDetailAPIView, ProductTypeDetailAPIView, \
    ProductColorsDetailAPIView, ListCommentAPIView, DetailCommentAPIView

urlpatterns = [

    # product
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('all/', AllProductAPIView.as_view(), name='all-product'),
    path('create/', ProductAPIView.as_view(), name='create-product'),

    path('create-images/', ProductImageAPIView.as_view(), name='create-product-image'),
    path('detail-images/<int:pk>/', ProductImageDetailAPIVIew.as_view(), name='create-product-image'),

    path('create-features/', ProductFeaturesAPIView.as_view(), name='create-product-image'),
    path('detail-features/<int:pk>/', ProductFeaturesDetailAPIView.as_view(), name='create-product-image'),

    path('create-color/', ColorAPIView.as_view(), name='create-colors'),
    path('detail-color/<int:pk>/', ColorDetailAPIView.as_view(), name='delete-colors'),

    path('create-product-colors/', ProductColorsAPIView.as_view(), name='create-product-colors'),
    path('detail-product-colors/<int:pk>/', ProductColorsDetailAPIView.as_view(), name='create-product-colors'),

    path('create-product-type/', ProductTypeAPIView.as_view(), name='create-colors'),
    path('detail-product-type/<int:pk>/', ProductTypeDetailAPIView.as_view(), name='create-colors'),

    # category
    path('categories/', CategoryAPIView.as_view(), name='list-create-category'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='detail-category'),


    path('comments/create/', CreateCommentAPIView.as_view(), name='create-comment'),
    path('comments/all/<int:pk>/', ListCommentAPIView.as_view(), name='list-comment'),
    path('comments/<int:pk>/', DetailCommentAPIView.as_view(), name='detail-comment'),

    path('categories/<slug:slug>/products/', ProductByCategoryAPIView.as_view(), name='product-by-category'),
]
