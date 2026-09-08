from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Artwork, ArtClass

class ArtworkSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Artwork.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


class ArtClassSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ArtClass.objects.all()

    def location(self, obj):
        return reverse('gallery:classes_list')


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ['gallery:home', 'gallery:gallery_list', 'gallery:commission', 'gallery:classes_list', 'gallery:contact']

    def location(self, item):
        return reverse(item)
