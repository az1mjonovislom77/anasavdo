from decimal import Decimal
from rest_framework import serializers

from app.order.models import Order, Item, ItemValue, ProductValue
from app.user.validations import validate_phone_number
from app.utils.models import Location
from app.utils.serializers import LocationSerializer


class ItemSerializer(serializers.ModelSerializer):
    feature = serializers.ListSerializer(write_only=True, child=serializers.IntegerField())
    images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('product', 'quantity', 'color', 'feature', 'price', 'images')
        extra_kwargs = {
            "feature": {"required": False},
            "color": {"required": False},
            "price": {"read_only": True}
        }

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.product.productimage_set.all()
        return [request.build_absolute_uri(img.image.url) for img in images if img.image]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = instance.product.title
        if instance.color and instance.color.color:
            data['color'] = instance.color.color.name
        else:
            data['color'] = None

        tmp = list()
        for feature in instance.itemvalue_set.all():
            tmp.append(feature.feature.type.name)
        data['feature'] = tmp
        return data


ZERO = Decimal("0.00")


def safe_decimal(value, default=ZERO):
    try:
        if value in [None, "", "nan", "NaN"]:
            return default
        return Decimal(str(value))
    except Exception:
        return default


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, write_only=True)
    items_detail = ItemSerializer(many=True, read_only=True, source='items')
    location = LocationSerializer()
    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        allow_null=True,
        coerce_to_string=False
    )

    class Meta:
        model = Order
        fields = (
            'id', 'status', 'location', 'receive', 'payment',
            'name', 'phone_number', 'additional_phone_number',
            'items', 'items_detail', 'price', 'created'
        )
        extra_kwargs = {
            "price": {"read_only": True},
            "phone_number": {"read_only": True},
        }

    def validate(self, data):
        phone_number = data.get('phone_number')
        additional_phone_number = data.get('additional_phone_number')

        if phone_number:
            validate_phone_number(phone_number)

        if additional_phone_number:
            validate_phone_number(additional_phone_number)
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        validated_data['location'] = location
        order = Order.objects.create(**validated_data)
        user = validated_data.get('user')
        if user:
            order.phone_number = user.phone_number

        price = ZERO
        for item in items_data:
            features = item.pop('feature', [])
            item['order'] = order
            tmp = Item.objects.create(**item)
            tmp_price = self._calculate_item_price(tmp, features)
            tmp.price = tmp_price
            tmp.save()
            price += tmp_price

        order.price = price
        order.save()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        location_data = validated_data.pop('location', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if location_data:
            if instance.location:
                for attr, value in location_data.items():
                    setattr(instance.location, attr, value)
                instance.location.save()
            else:
                instance.location = Location.objects.create(**location_data)

        if items_data is not None:
            instance.items.all().delete()
            self._create_items(instance, items_data)

        price = ZERO
        for item in instance.items.all():
            price += safe_decimal(item.price)

        instance.price = price
        instance.save()
        return instance

    def _create_items(self, order, items_data):
        for item in items_data:
            features = item.pop('feature', [])
            item['order'] = order
            tmp = Item.objects.create(**item)
            tmp.price = self._calculate_item_price(tmp, features)
            tmp.save()

    def _calculate_item_price(self, item, features):
        tmp_price = ZERO
        for feature in features:
            if ProductValue.objects.filter(id=feature, product_id=item.product_id).exists():
                t = ItemValue.objects.create(item=item, feature_id=feature)
                tmp_price += safe_decimal(t.feature.price)

        product_price = safe_decimal(item.product.price)
        color_price = safe_decimal(item.color.price) if item.color else ZERO

        tmp_price += product_price + color_price
        tmp_price *= item.quantity or 1
        return tmp_price

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        lang = self.context['request'].LANGUAGE_CODE
        rep['name'] = getattr(instance, f"name_{lang}", instance.name)

        price = safe_decimal(instance.price)
        rep['price'] = str(price.quantize(Decimal("0.00")))
        return rep


class ItemHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'price')

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        print('instance order:', instance)
        data['name'] = instance.product.title
        images = instance.product.productimage_set.all()
        if images:
            data['image'] = request.build_absolute_uri(images[0].image.url)
        else:
            data['image'] = None
        return data


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', ]


class OrderHistorySerializer(serializers.ModelSerializer):
    items = ItemHistorySerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'price', 'created', 'items')
