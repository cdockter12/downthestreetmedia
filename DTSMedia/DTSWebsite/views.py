from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpRequest
from DTSMedia.forms import SetupPhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from DTSWebsite.models import Album, AlbumImage

import datetime
# Create your views here.


def index(request):
    return render(request, 'DTSWebsite/index.html')


def book_now(request):
    if request.method == 'POST':
        # Create a form instance and populate it.
        form = SetupPhotoForm(request.POST)

        if form.is_valid():
            # Process the data in form.cleaned_data as required.
            contact_first_name = form.cleaned_data['contact_first_name']
            contact_last_name = form.cleaned_data['contact_last_name']
            contact_email = form.cleaned_data['contact_email']
            listing_address = form.cleaned_data['listing_address']
            house_sqft = form.cleaned_data['house_sqft']
            photo_date = form.cleaned_data['photo_date']

            message = str('Agent Name: ' + contact_first_name + ' ' + contact_last_name + ' ' + 'Email: ' + contact_email + ' ' + 'Listing Address: ' +
                          listing_address + ' ' + 'Property SQFT (dropdown option): ' + house_sqft + ' ' + 'Desired Shoot Date: ' + photo_date.strftime('%m/%d/%Y'))

            try:
                send_mail('Photo Request', message, contact_email, [
                          'cole.dockter@gmail.com', ], fail_silently=False,)
            except BadHeaderError:
                return HttpResponse('Invalid Header Found.')

            return render(request, 'DTSWebsite/thanks.html', {'form': form})
    else:
        form = SetupPhotoForm()

    context = {
        'form': form,
    }

    return render(request, 'DTSWebsite/book_now.html', context)


def gallery(request):
    list = Album.objects.order_by('-created')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)

    return render(request, 'DTSWebsite/gallery.html', {'albums': list})


class AlbumDetail(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 4040)
