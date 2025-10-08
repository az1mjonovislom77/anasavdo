from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from rest_framework import permissions, views, status
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from app.about.models import OurContact, Contact, SocialMedia, News, Banner, About
from app.about.serializers import OurContactSerializer, ContactSerializer, SocialMediaSerializer, NewsSerializer, \
    BannerSerializer, AboutSerializer, NewsGetSerializer
from app.user.validations import IsAdminOrSuperAdmin


@extend_schema(tags=['Our Contact'])
class OurContactAPIView(views.APIView):
    serializer_class = OurContactSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        our_contact = OurContact.objects.all()
        serializer = OurContactSerializer(our_contact, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = OurContactSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Our Contact'])
class OurContactDetailView(views.APIView):
    serializer_class = OurContactSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def put(self, request, pk):
        our_contact = get_object_or_404(OurContact, pk=pk)
        serializer = OurContactSerializer(our_contact, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        our_contact = get_object_or_404(OurContact, pk=pk)
        our_contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Contacts'])
class ContactAPIView(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=['Contacts'])
class ContactSDetailAPIView(views.APIView):
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(instance=contact, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response({'message': "Contact deleted successfully!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Social Media'])
class SocialMediaAPIView(ListCreateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]


@extend_schema(tags=['Social Media'])
class SocialMediaDetailAPIView(views.APIView):
    serializer_class = SocialMediaSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        social_media = get_object_or_404(SocialMedia, pk=pk)
        serializer = SocialMediaSerializer(social_media, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        social_media = get_object_or_404(SocialMedia, pk=pk)
        serializer = SocialMediaSerializer(social_media, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        social_media = get_object_or_404(SocialMedia, pk=pk)
        social_media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['News'])
class NewsAPIView(views.APIView):
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsGetSerializer(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['News'])
class NewsDetailAPIView(views.APIView):
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsGetSerializer(news, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(instance=news, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response({'message': "News successfully deleted!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Banner'])
class BannerAPIView(ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]


@extend_schema(tags=['Banner'])
class BannerDetailAPIView(views.APIView):
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def put(self, request, pk):
        banner = get_object_or_404(Banner, pk=pk)
        serializer = BannerSerializer(instance=banner, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        banner = get_object_or_404(Banner, pk=pk)
        banner.delete()
        return Response({'message': "Banner successfully deleted!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['About'])
class AboutAPIView(ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=['About'])
class AboutDetailAPIView(views.APIView):
    serializer_class = AboutSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminOrSuperAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]

    def put(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        serializer = AboutSerializer(instance=about, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        about = get_object_or_404(About, pk=pk)
        about.delete()
        return Response({'message': "About successfully deleted!"}, status=status.HTTP_200_OK)
