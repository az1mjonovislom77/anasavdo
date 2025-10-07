from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import unfold_navigation as navigation


UNFOLD = {
    "SITE_TITLE": "M-Electro",
    "SITE_HEADER": "M-Electro",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("icon/main.png"),

    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "48x48",
            "type": "image/svg+xml",
            "href": lambda request: static("icon/main.png"),
        },
    ],    # Bu titleda turadigan logo

    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": True, # show/hide "Back" button on changeform in header, default: False
    "ENVIRONMENT": "core.config.unfold.environment_callback",
    # "ENVIRONMENT_TITLE_PREFIX": "sample_app.environment_title_prefix_callback", # environment name prefix in title tag
    # "DASHBOARD_CALLBACK": "apps.shared.views.dashboard.dashboard_callback",
    "THEME": "dark", # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        "image": lambda request: static("icon/main2.png"),
    },
    # "STYLES": [
    #     lambda request: static("css/tailwind.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    "BORDER_RADIUS": "16px",
    "COLORS": {
        "base": {
            "50": "249, 250, 251",
            "100": "243, 244, 246",
            "200": "229, 231, 235",
            "300": "209, 213, 219",
            "400": "156, 163, 175",
            "500": "107, 114, 128",
            "600": "75, 85, 99",
            "700": "55, 65, 81",
            "800": "31, 41, 55",
            "900": "17, 24, 39",
            "950": "3, 7, 18",
        },
        "primary": {
            "50": "250, 245, 255",
            "100": "243, 232, 255",
            "200": "233, 213, 255",
            "300": "216, 180, 254",
            "400": "192, 132, 252",
            "500": "168, 85, 247",
            "600": "147, 51, 234",
            "700": "126, 34, 206",
            "800": "107, 33, 168",
            "900": "88, 28, 135",
            "950": "59, 7, 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": navigation.PAGES,
    },
    # "TABS": navigation.TABS,
}


def environment_callback(request):
    from django.conf import settings
    if settings.DEBUG:
        return "Development"
    return "Production"
