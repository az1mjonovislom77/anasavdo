from decimal import Decimal

from django.core.files import images
from rest_framework import serializers

from app.order.models import Order, Item, ItemValue, ProductValue, ProductColor
from app.user.validations import check_valid_phone, validate_phone_number
from app.utils.models import Location
from app.utils.serializers import LocationSerializer
from core import settings


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

    # def validate_quantity(self, data):
    #     print('order quantity data', data)
    #     return data


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
"""
import os
import random
import string
import uuid

import pandas as pd
import csv
from django.contrib.auth.hashers import make_password
from django.db import transaction
from app.users.models import User
from core import settings


def generate_username():
    # uuid.uuid4.__str__() -> c303282d-f2e6-46ca-a04a-35d3d873712d (takrorlanmas kod yasab beradi)
    temp_username = f"user_{uuid.uuid4().__str__().split('-')[1]}"
    while User.objects.filter(username=temp_username):
        temp_username = f"{temp_username}{random.randint(0, 9)}"
    return temp_username


def generate_password(length: int = 8) -> str:
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choices(chars, k=length))
    return password


def import_user_from_excel(file_path):
    all_rows = pd.read_excel(file_path, header=None)
    total_rows = len(all_rows)

    for header_row in range(min(total_rows, 10)):
        df = pd.read_excel(file_path, header=header_row)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]

        if len(df.columns) >= 2:
            break
    else:
        raise ValueError("Excel faylda kerakli sarlavha topilmadi!")

    df.columns = df.columns.str.strip().str.lower().str.replace(u'\xa0', ' ')

    required_columns = ["full_name", "phone_number"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Excel faylda '{col}' ustuni topilmadi! Hozirgi ustunlar: {df.columns.tolist()}"
            )

    created_users = []
    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for _, row in df.iterrows():
            full_name = str(row.get("full_name", "")).strip()
            phone_number = str(row.get("phone_number", "")).strip()

            if not phone_number:
                continue

            password = generate_password()
            hash_password = make_password(password)

            user, created = User.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    "username": generate_username(),
                    "full_name": full_name,
                    "role": User.UserRoles.SQUAD,
                    "password": hash_password,
                },
            )

            if created:
                created_count += 1
                created_users.append([user.username, password])
            else:
                updated_count += 1

    # 📂 Faylni media papkaga yozamiz
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    file_path = os.path.join(settings.MEDIA_ROOT, "created_users.csv")

    pd.DataFrame(created_users, columns=["username", "password"]).to_csv(file_path, index=False)

    print(f"{created_count} ta yangi user yaratildi, {updated_count} ta user yangilandi.")
    return {
        "created": created_count,
        "updated": updated_count,
        "file_url": settings.MEDIA_URL + "created_users.csv"  # 🔗 Admin orqali olish mumkin
    }
"""

ZERO = Decimal("0.00")

def safe_decimal(value, default=ZERO):
    """Qiymatni xavfsiz Decimal ga aylantirish"""
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

        # Oddiy fieldlarni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Location yangilash
        if location_data:
            if instance.location:
                for attr, value in location_data.items():
                    setattr(instance.location, attr, value)
                instance.location.save()
            else:
                instance.location = Location.objects.create(**location_data)

        # Items yangilash
        if items_data is not None:
            instance.items.all().delete()
            self._create_items(instance, items_data)

        # Umumiy narxni qayta hisoblash
        price = ZERO
        for item in instance.items.all():
            price += safe_decimal(item.price)

        instance.price = price
        instance.save()
        return instance

    def _create_items(self, order, items_data):
        """Buyurtmaga itemlar yaratish yordamchi metodi"""
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
        fields = ['status',]


class OrderHistorySerializer(serializers.ModelSerializer):
    items = ItemHistorySerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'price', 'created', 'items')
