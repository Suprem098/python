import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MenuItem, Order, CafeModel, Feedback
from .form import OrderForm, FeedbackForm


def home(request):
    return render(request, 'index.html')

from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

def generate_qr(request):
    url = request.build_absolute_uri(reverse('menu'))
    qr = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response


def cafe_view(request):
    cafes = CafeModel.objects.all()
    return render(request, 'cafe.html', {'cafes': cafes})

def place_order(request):
    item_id = request.GET.get('item')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES) 
        if form.is_valid():  
            order = form.save()
            return redirect('order_confirmation', order_id=order.id)
        else:
            errors = form.errors.as_json()
            return render(request, 'menu/order_form.html', {'form': form, 'errors': form.errors, 'errors_json': errors})
    else:
        if item_id:
            form = OrderForm(initial={'item': item_id})
        else:
            form = OrderForm()
    return render(request, 'menu/order_form.html', {'form': form})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def menu_view(request, cafe_slug=None):
    if cafe_slug:
        cafe = get_object_or_404(CafeModel, cafeid=cafe_slug)
        menu_items = MenuItem.objects.filter(cafe=cafe, available=True)
    else:
        menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'menu/menu.html', {'menu_items': menu_items})

def menu_view_by_id(request, cafe_id):
    cafe = get_object_or_404(CafeModel, id=cafe_id)
    return menu_view(request, cafe_slug=cafe.cafeid)

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'menu/feedback.html', {'form': FeedbackForm(), 'success': True})
        else:
            errors = form.errors.as_json()
            return render(request, 'menu/feedback.html', {'form': form, 'errors': form.errors, 'errors_json': errors})
    else:
        form = FeedbackForm()
    return render(request, 'menu/feedback.html', {'form': form})

from django.core.mail import send_mail
#from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import ContactSubmission

from django.shortcuts import render

def contact_form_submit(request):
    if request.method == 'POST':
        cafe_name = request.POST.get('cafe-name')
        contact_person = request.POST.get('contact-person')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save to database
        ContactSubmission.objects.create(
            cafe_name=cafe_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            message=message
        )

        subject = f"New Cafe Contact Submission from {cafe_name}"
        body = f"""\
Cafe Name: {cafe_name}
Contact Person: {contact_person}
Email: {email}
Phone: {phone}
Message: {message}
"""

        admin_email = 'admin@example.com'  # Replace with actual admin email
        send_mail(subject, body, email, [admin_email], fail_silently=False)

        return render(request, 'index.html', {'success': True})
    else:
        return render(request, 'index.html')

