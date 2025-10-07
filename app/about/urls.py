from  django.urls import path

from app.about.views import OurContactAPIView, ContactAPIView, SocialMediaAPIView, BannerAPIView, NewsAPIView, \
    AboutAPIView, AboutDetailAPIView, BannerDetailAPIView, ContactSDetailAPIView, NewsDetailAPIView, \
    OurContactDetailView, SocialMediaDetailAPIView

urlpatterns = [
    # about
    path('', AboutAPIView.as_view(), name='about'),
    path('<int:pk>/', AboutDetailAPIView.as_view(), name='about-detail'),

    # contact
    path('our-contact/', OurContactAPIView.as_view(), name='our-contact'),
    path('our-contact/<int:pk>/', OurContactDetailView.as_view(), name='our-contact'),


    path('contact/', ContactAPIView.as_view(), name='contact'),
    path('contact/<int:pk>/', ContactSDetailAPIView.as_view(), name='contact-detail'),

    # social-media
    path('social-media/', SocialMediaAPIView.as_view(), name='social-media'),
    path('social-media/<int:pk>/', SocialMediaDetailAPIView.as_view(), name='social-media-detail'),

    # banners
    path('banners/', BannerAPIView.as_view(), name='banners'),
    path('banners/<int:pk>/', BannerDetailAPIView.as_view(), name='banner-detail'),

    # news
    path('news/', NewsAPIView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),
]
