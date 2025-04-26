import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MenuItem, Order, CafeModel, Feedback
from .form import OrderForm, FeedbackForm


def home(request):
    return render(request, 'index.html')

def generate_qr(request):
    url = "http://192.168.0.18:8000/menu/"
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
            return render(request, 'menu/order_form.html', {'form': form, 'errors': form.errors})
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
            return render(request, 'menu/feedback.html', {'form': form, 'errors': form.errors})
    else:
        form = FeedbackForm()
    return render(request, 'menu/feedback.html', {'form': form})

