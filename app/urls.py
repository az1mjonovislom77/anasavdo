from django.urls import path, include


urlpatterns = [
    path('user/', include('app.user.urls')),
    path('bot/', include('app.bot.urls')),
    path('product/', include('app.product.urls')),
    path('order/', include('app.order.urls')),
    path('about/', include('app.about.urls')),
    path('', include('app.utils.urls')),
]
