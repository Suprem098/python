import qrcode
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MenuItem, Order
from .form import OrderForm

def home(request):
    return render(request, 'index.html')

def generate_qr(request):
    url = "http://192.168.0.18:8000/menu/"
    qr = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

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
    return render(request, 'menu/order_confirmation.html', {'order': order})

def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu/menu.html', {'menu_items': menu_items})
