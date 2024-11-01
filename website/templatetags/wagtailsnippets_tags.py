from django import template
from ..models import ServiceSnippet, StaffSnippet, WorkSnippet, PartnerSnippet, PricingSnippet, CounterSnippet, FooterSnippet

register = template.Library()

@register.simple_tag
def get_service_snippets():
    """Returns all service snippets"""
    return ServiceSnippet.objects.all()

@register.simple_tag
def get_staff_snippets():
    """Returns all staff snippets"""
    return StaffSnippet.objects.all()

@register.simple_tag
def get_work_snippets():
    """Returns all work snippets"""
    return WorkSnippet.objects.all()

@register.simple_tag
def get_partner_snippets():
    """Returns all partner snippets"""
    return PartnerSnippet.objects.all()

@register.simple_tag
def get_pricing_snippets():
    """Returns all pricing snippets"""
    return PricingSnippet.objects.all()

@register.simple_tag
def get_counter_snippets():
    """Returns all counter snippets"""
    return CounterSnippet.objects.all()

@register.simple_tag
def get_footer():
    """Retrieve the first instance of FooterSnippet."""
    return FooterSnippet.objects.first()
