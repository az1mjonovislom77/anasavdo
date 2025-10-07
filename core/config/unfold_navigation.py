from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Home Page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Users"),
        "items": [
            {
                "title": _("Users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:user_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Verifications"),
                "icon": "check",
                "link": reverse_lazy("admin:user_verificationotp_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Bot User"),
                "icon": "check",
                "link": reverse_lazy("admin:bot_botuser_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            }
        ]
    },
    {
        "seperator": True,
        "title": _("Product"),
        "items": [
            {
                "title": _("Category"),
                "icon": "layers",
                "link": reverse_lazy("admin:product_category_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Product"),
                "icon": "package",
                "link": reverse_lazy("admin:product_product_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Product Image"),
                "icon": "image",
                "link": reverse_lazy("admin:product_productimage_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Product Color"),
                "icon": "palette",
                "link": reverse_lazy("admin:product_productcolor_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Product Type"),
                "icon": "list",
                "link": reverse_lazy("admin:product_producttype_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Product Value"),
                "icon": "sliders",
                "link": reverse_lazy("admin:product_productvalue_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Comment"),
                "icon": "comment",
                "link": reverse_lazy("admin:product_comment_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            }
        ]
    },
    {
        "seperator": True,
        "title": _("Order"),
        "items": [
            {
                "title": _("Order"),
                "icon": "shopping_cart",
                "link": reverse_lazy("admin:order_order_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Item"),
                "icon": "receipt",
                "link": reverse_lazy("admin:order_item_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Item Value"),
                "icon": "sliders",
                "link": reverse_lazy("admin:order_itemvalue_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            }
        ]
    },
    {
        "seperator": True,
        "title": _("Utils"),
        "items": [
            {
                "title": _("Color"),
                "icon": "palette",
                "link": reverse_lazy("admin:utils_color_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Location"),
                "icon": "location_on",
                "link": reverse_lazy("admin:utils_location_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            },
            {
                "title": _("Notification"),
                "icon": "notifications",
                "link": reverse_lazy("admin:utils_notification_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                )
            }
        ]
    }
]

TABS = [
    {
        "models": [
            # "auth.user",
            "auth.group",
        ],
        "items": [
            # {
            #     "title": _("Foydalanuvchilar"),
            #     "link": reverse_lazy("admin:auth_user_changelist"),
            # },
            {
                "title": _("Guruhlar"),
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
        ],
    },
]