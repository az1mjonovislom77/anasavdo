from rest_framework import serializers

from app.product.models import Category, Product, ProductImage, Comment, ProductColor, ProductValue, CategoryImages, \
    ProductType
from app.utils.models import Color


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'product', 'rate', 'message', 'created')
        extra_kwargs = {
            "product": {"write_only": True},
            "id": {"read_only": True},
            "created": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        product = validated_data.get("product")
        rate = validated_data.get("rate")
        message = validated_data.get("message")

        has_order = user.order_set.filter(items__product=product, status="s").exists()
        if not has_order:
            raise serializers.ValidationError(
                {"detail": "Siz faqat sotib olgan mahsulotlaringizga sharh qoldira olasiz."}
            )

        comment = Comment.objects.create(
            user=user,
            product=product,
            rate=rate,
            message=message,
            is_active=True
        )
        return comment

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.full_name
        request = self.context.get('request')
        if instance.user.image:
            if request:
                data['image'] = request.build_absolute_uri(instance.user.image.url)
            else:
                data['image'] = instance.user.image.url
        else:
            data['image'] = None
        return data


class CategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'name_uz', 'name_en', 'name_ru', 'slug', 'image')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        rep['name'] = getattr(instance, f"name_{lang}", instance.name)
        return rep


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name_uz', 'name_en', 'name_ru', 'slug', 'image')
        extra_kwargs = {'slug': {'read_only': True}}


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'product')


class ColorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'name_uz', 'name_en', 'name_ru', 'image')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        rep['name'] = getattr(instance, f"name_{lang}", instance.name)
        return rep


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name_uz', 'name_en', 'name_ru', 'image')


class ProductTypeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'product', 'name')


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'product', 'name_uz', 'name_en', 'name_ru')


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id', 'product', 'color', 'image', 'price')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        lang = request.LANGUAGE_CODE
        if instance.color:
            data['name'] = getattr(instance.color.name, f"name_{lang}", instance.color.name)
        else:
            data['name'] = None

        if instance.color:
            data['color_image'] = request.build_absolute_uri(instance.color.image.url)
        else:
            data['color_image'] = None

        if request and instance.image:
            data["image"] = request.build_absolute_uri(instance.image.url)

        if instance.image.url:
            data['image'] = request.build_absolute_uri(instance.image.url)
        else:
            data['image'] = None

        return data


class ProductValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductValue
        fields = ('id', 'product', 'type', 'value', 'price')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        data['type_name'] = getattr(instance.type.name, f"name_{lang}", instance.type.name)
        return data


class ProductGetSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source="productimage_set", read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    features = ProductValueSerializer(many=True, read_only=True, source='values')

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'old_price', 'images', 'colors', 'features')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        data['title'] = getattr(instance, f"title_{lang}", instance.title)
        data['description'] = getattr(instance, f"description_{lang}", instance.description)
        data['category'] = instance.category.slug
        return data


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source="productimage_set", read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    features = ProductValueSerializer(many=True, read_only=True, source='values')

    class Meta:
        model = Product
        fields = ('id', 'category', 'title', 'title_uz', 'title_en', 'title_ru', 'description_uz', 'description_en',
                  'description_ru', 'price', 'old_price', 'images', 'colors', 'features')
        extra_kwargs = {
            'title': {'required': False},
            'category': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.slug
        return data


class AllProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source="productimage_set")
    features = ProductValueSerializer(many=True, read_only=True, source='values')

    class Meta:
        model = Product
        fields = ('id', 'title', 'title_uz', 'title_en', 'title_ru', 'description', 'description_uz', 'description_en',
                  'description_ru', 'price', 'old_price', 'images', 'features')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.category.slug:
            data['category'] = instance.category.slug
        else:
            data['category'] = None

        lang = self.context['request'].LANGUAGE_CODE
        data['title'] = getattr(instance, f"title_{lang}", instance.title)
        data['description'] = getattr(instance, f"description_{lang}", instance.description)
        return data


class CategoryImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImages
        fields = ('id', 'image')
