from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from .models import Artwork, CommissionRequest, ArtClass, ContactMessage
from .forms import CommissionRequestForm, ContactForm, SeatReservationForm
from .utils import send_whatsapp_alert

class HomeView(TemplateView):
    template_name = 'gallery/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_artworks'] = Artwork.objects.filter(is_featured=True)[:6]
        if not context['featured_artworks'].exists():
            context['featured_artworks'] = Artwork.objects.all()[:6]
        context['upcoming_classes'] = ArtClass.objects.filter(date__gte=timezone.now())[:3]
        context['total_artworks'] = Artwork.objects.count()
        context['available_count'] = Artwork.objects.filter(is_available=True).count()
        return context


class GalleryListView(ListView):
    model = Artwork
    template_name = 'gallery/gallery.html'
    context_object_name = 'artworks'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artwork.objects.all()

        # Medium filter
        medium = self.request.GET.get('medium')
        if medium and medium != 'all':
            queryset = queryset.filter(medium__iexact=medium)

        # Availability filter
        availability = self.request.GET.get('availability')
        if availability == 'available':
            queryset = queryset.filter(is_available=True)
        elif availability == 'sold':
            queryset = queryset.filter(is_available=False)

        # Price range filter
        price_range = self.request.GET.get('price_range')
        if price_range == 'under-1000':
            queryset = queryset.filter(price__lt=1000)
        elif price_range == '1000-2500':
            queryset = queryset.filter(price__gte=1000, price__lte=2500)
        elif price_range == 'over-2500':
            queryset = queryset.filter(price__gt=2500)

        # Search query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(medium__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mediums'] = Artwork.objects.values_list('medium', flat=True).distinct()
        context['selected_medium'] = self.request.GET.get('medium', 'all')
        context['selected_availability'] = self.request.GET.get('availability', 'all')
        context['selected_price'] = self.request.GET.get('price_range', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'gallery/detail.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.object
        context['related_artworks'] = Artwork.objects.filter(
            medium=artwork.medium
        ).exclude(id=artwork.id)[:3]
        if not context['related_artworks'].exists():
            context['related_artworks'] = Artwork.objects.exclude(id=artwork.id)[:3]
        return context


class CommissionView(View):
    def get(self, request):
        form = CommissionRequestForm()
        return render(request, 'gallery/commission.html', {'form': form})

    def post(self, request):
        form = CommissionRequestForm(request.POST, request.FILES)
        if form.is_valid():
            commission = form.save()
            send_whatsapp_alert(
                name=commission.client_name,
                email=commission.email,
                phone=commission.phone,
                message_text=f"Style: {commission.style} | Budget: {commission.budget} | Description: {commission.description}",
                form_type="Custom Commission Inquiry"
            )
            messages.success(
                request,
                f"Thank you, {commission.client_name}! Your custom commission inquiry for '{commission.style}' has been received. D-Art Studio team will contact you at {commission.email} within 24 hours."
            )
            return redirect('gallery:commission')
        else:
            messages.error(request, "Please correct the errors in the commission form below.")
        return render(request, 'gallery/commission.html', {'form': form})


class ClassesView(View):
    def get(self, request):
        classes = ArtClass.objects.all()
        reservation_form = SeatReservationForm()
        return render(request, 'gallery/classes.html', {
            'classes': classes,
            'reservation_form': reservation_form
        })

    def post(self, request):
        form = SeatReservationForm(request.POST)
        if form.is_valid():
            class_id = form.cleaned_data['class_id']
            seats_requested = form.cleaned_data['seats_count']
            art_class = get_object_or_404(ArtClass, pk=class_id)

            if art_class.seats_available >= seats_requested:
                art_class.seats_available -= seats_requested
                art_class.save()
                messages.success(
                    request,
                    f"Seats Confirmed! Reserved {seats_requested} seat(s) for '{art_class.title}' for {form.cleaned_data['name']}. Confirmation sent to {form.cleaned_data['email']}."
                )
            else:
                messages.error(
                    request,
                    f"Sorry, only {art_class.seats_available} seat(s) are remaining for '{art_class.title}'."
                )
            return redirect('gallery:classes_list')

        classes = ArtClass.objects.all()
        return render(request, 'gallery/classes.html', {
            'classes': classes,
            'reservation_form': form
        })


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'gallery/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            send_whatsapp_alert(
                name=msg.name,
                email=msg.email,
                message_text=f"Subject: {msg.subject}\nMessage: {msg.message}",
                form_type="Contact Inquiry"
            )
            messages.success(
                request,
                f"Thank you, {msg.name}! Your message regarding '{msg.subject}' has been sent to D-Art Studio."
            )
            return redirect('gallery:contact')
        else:
            messages.error(request, "Please fill in all required fields in the contact form.")
        return render(request, 'gallery/contact.html', {'form': form})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
