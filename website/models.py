"""
Create or customize your page models here.
"""

from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


from django.db import models
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.images.models import Image
from coderedcms.models import CoderedWebPage
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.blocks import TextBlock
from wagtail import blocks

class HomePage(CoderedWebPage):
    template = "coderedcms/pages/home_page.html"

    # Hero Section
    hero_background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for the hero section."
    )
    hero_title = models.CharField(
        max_length=255,
        help_text="Main title in the hero section."
    )
    hero_subtitle = models.TextField(
        blank=True,
        help_text="Subtitle text in the hero section."
    )
    appointment_phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone number for the 'click to chat' link."
    )

    # Discount Section
    discount_background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for the discount section."
    )
    discount_title = models.CharField(
        max_length=255,
        help_text="Title for the discount section."
    )
    discount_subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Subtitle for the discount section."
    )
    discount_description = models.TextField(
        blank=True,
        help_text="Description text for the discount section."
    )

    # Appointment Info Section
    appointment_address = models.TextField(
        blank=True,
        help_text="Address displayed in the appointment section."
    )
    appointment_phone_primary = models.CharField(
        max_length=20,
        blank=True,
        help_text="Primary phone number displayed in the appointment section."
    )
    appointment_phone_secondary = models.CharField(
        max_length=20,
        blank=True,
        help_text="Secondary phone number displayed in the appointment section."
    )
    appointment_opening_hours = models.CharField(
        max_length=255,
        blank=True,
        help_text="Opening hours displayed in the appointment section."
    )

    # Panels
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('hero_background_image'),
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('appointment_phone_number'),
        FieldPanel('discount_background_image'),
        FieldPanel('discount_title'),
        FieldPanel('discount_subtitle'),
        FieldPanel('discount_description'),
        FieldPanel('appointment_address'),
        FieldPanel('appointment_phone_primary'),
        FieldPanel('appointment_phone_secondary'),
        FieldPanel('appointment_opening_hours'),
    ]


@register_snippet
class ServiceSnippet(models.Model):
    title = models.CharField(max_length=255, help_text="Service title")
    description = models.TextField(help_text="Service description")
    icon_class = models.CharField(
        max_length=50,
        help_text="CSS class for the icon (e.g., 'flaticon-facial-treatment')",
        blank=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("icon_class"),
    ]

    def __str__(self):
        return self.title


@register_snippet
class StaffSnippet(models.Model):
    """Snippet to represent a staff member with image, name, position, link, and description."""

    name = models.CharField(max_length=255, help_text="Name of the staff member.")
    position = models.CharField(max_length=255, help_text="Position or title of the staff member.")
    description = models.TextField(help_text="Brief description of the staff member.")
    link = models.URLField(blank=True, help_text="URL link to the staff member's profile.")
    background_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Background image for the staff member."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("position"),
        FieldPanel("description"),
        FieldPanel("link"),
        FieldPanel("background_image"),
    ]

    def __str__(self):
        return self.name


@register_snippet
class WorkSnippet(models.Model):
    """Snippet to represent a work entry with an image, title, and link."""

    title = models.CharField(max_length=255, help_text="Title of the work entry.")
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Image for the work entry."
    )
    link = models.URLField(blank=True, help_text="URL link to the detailed work page or image.")

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("link"),
    ]

    def __str__(self):
        return self.title

@register_snippet
class PartnerSnippet(models.Model):
    """Snippet to represent a partner with an image and optional link."""

    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Image for the partner logo."
    )
    link = models.URLField(blank=True, help_text="URL link to the partner's website.")

    panels = [
        FieldPanel("image"),
        FieldPanel("link"),
    ]

    def __str__(self):
        return self.link if self.link else "Partner Image"


@register_snippet
class PricingSnippet(models.Model):
    """Snippet to represent a pricing entry with title, price, frequency, and a list of features."""

    title = models.CharField(max_length=255, help_text="Title of the pricing plan (e.g., Basic, Standard).")
    price = models.CharField(max_length=50, help_text="Price of the plan (e.g., $24.50).")
    frequency = models.CharField(max_length=50, blank=True, help_text="Frequency of the pricing (e.g., per trip).")

    # StreamField for list of features
    features = StreamField(
        [("feature", TextBlock())],
        blank=True,
        help_text="List of features included in the pricing plan."
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("price"),
        FieldPanel("frequency"),
        FieldPanel("features"),
    ]

    def __str__(self):
        return self.title


@register_snippet
class CounterSnippet(models.Model):
    """Snippet to represent a counter entry with procedure name and number."""

    procedure = models.CharField(max_length=255, help_text="Name of the procedure (e.g., Makeup Over Done).")
    number = models.PositiveIntegerField(help_text="Number to display for the counter.")

    panels = [
        FieldPanel("procedure"),
        FieldPanel("number"),
    ]

    def __str__(self):
        return f"{self.procedure}: {self.number}"


@register_snippet
class FooterSnippet(models.Model):
    """Snippet to represent a customizable footer with about text, social media, custom links, and contact info."""

    # About Us Section
    about_title = models.CharField(max_length=255, default="About Us", help_text="Title for the About Us section.")
    about_text = models.TextField(help_text="Text for the About Us section.")

    # Social Media Links
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL.")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL.")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL.")

    # Custom Link Section
    custom_links_title = models.CharField(max_length=255, default="Spa Center", help_text="Title for custom links.")
    custom_links = StreamField(
        [("link", blocks.StructBlock([
            ("title", blocks.CharBlock(required=True, help_text="Link text")),
            ("url", blocks.URLBlock(required=True, help_text="URL for the link")),
        ]))],
        blank=True,
        help_text="List of custom links for the footer."
    )

    # Contact Information
    address = models.CharField(max_length=255, help_text="Contact address.")
    phone = models.CharField(max_length=20, help_text="Contact phone number.")
    email = models.EmailField(help_text="Contact email address.")

    panels = [
        MultiFieldPanel([
            FieldPanel("about_title"),
            FieldPanel("about_text"),
        ], heading="About Us Section"),

        MultiFieldPanel([
            FieldPanel("twitter_url"),
            FieldPanel("facebook_url"),
            FieldPanel("instagram_url"),
        ], heading="Social Media Links"),

        MultiFieldPanel([
            FieldPanel("custom_links_title"),
            FieldPanel("custom_links"),
        ], heading="Custom Links Section"),

        MultiFieldPanel([
            FieldPanel("address"),
            FieldPanel("phone"),
            FieldPanel("email"),
        ], heading="Contact Information"),
    ]

    def __str__(self):
        return "Footer Content"



from coderedcms.models import CoderedWebPage
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import TextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from django.db import models

# Product Index Page: Parent page that holds all product pages
class ProductIndexPage(CoderedWebPage):
    template = "coderedcms/pages/product_index_page.html"

    class Meta:
        verbose_name = "Product Index Page"

    # Only allow ProductPages to be children of this index page
    subpage_types = ["website.ProductPage"]
    index_query_pagemodel = "website.ProductPage"

    # Panels for CMS interface
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel("title"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['products'] = ProductPage.objects.live().descendant_of(self)
        return context


# Product Page: Represents a single product
class ProductPage(CoderedWebPage):
    template = "coderedcms/pages/product_page.html"

    # Product-specific fields
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description_short = RichTextField(blank=True, null=True)
    description_long = RichTextField(blank=True, null=True)
    images = StreamField([('image', ImageChooserBlock())], blank=True)

    # Panels to control which fields are shown in the Wagtail admin
    content_panels = CoderedWebPage.content_panels + [
        FieldPanel('price'),
        FieldPanel('discount_price'),
        FieldPanel('description_short'),
        FieldPanel('description_long'),
        FieldPanel('images'),
    ]

    class Meta:
        verbose_name = "Product Page"

    parent_page_types = ["website.ProductIndexPage"]



