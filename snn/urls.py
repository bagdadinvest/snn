from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Non-language-prefixed URLs (optional)
    path('__debug__/', include('debug_toolbar.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher URL
]

urlpatterns += i18n_patterns(
    # Admin
    path("django-admin/", admin.site.urls),
    path('scrapper/', include('scrapper.urls')),  # Include the scrapper app URLs
    path("admin/", include(crx_admin_urls)),
    # Custom Scraper Admin Panel URL
    path("scraper-panel/", include('scrapper.urls')),  # Links to your custom scraper admin page
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search
    path("search/", include(crx_search_urls)),
    # Hand over to the Wagtail page serving mechanism
    path("", include(crx_urls)),
)

# fmt: off
if settings.DEBUG:
    from django.conf.urls.static import static
    # Serve static and media files from the development server
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
# fmt: on
