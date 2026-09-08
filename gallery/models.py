from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    image = models.ImageField(upload_to='artworks/')
    medium = models.CharField(max_length=100, help_text="e.g. Oil on Canvas, Acrylic, Watercolor, Digital Art")
    dimensions = models.CharField(max_length=100, help_text="e.g. 24\" x 36\" or 60cm x 90cm")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, help_text="Detailed story or background of the artwork")
    year_created = models.PositiveIntegerField(default=2025)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Artwork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery:artwork_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class CommissionRequest(models.Model):
    client_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    style = models.CharField(max_length=100)
    budget = models.CharField(max_length=100, help_text="Estimated budget range")
    deadline = models.DateField()
    reference_image = models.ImageField(upload_to='commissions/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commission for {self.client_name} ({self.style})"


class ArtClass(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=250)
    seats_available = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField(default=15)
    instructor = models.CharField(max_length=100, default="D-Art Studio Team")
    image = models.ImageField(upload_to='classes/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Art Classes"
        ordering = ['date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ArtClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%b %d, %Y')}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
