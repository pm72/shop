from django.shortcuts import render, redirect, get_object_or_404

from main.models import Product
from . cart import Cart
from . forms import CartAddProductForm
from django.views.decorators.http import require_POST   # POST ფოორმის ვალიდაცია


@require_POST
def cart_add(request, product_id):
  '''
  კალატაში პროდუქტის დამატება

  მუშაობს მხოლოდ POST მეთოდით
  დანარჩენ მეთოდებზე (GET, PUT, DELETE) 405 შეცდომა (Method Not Allowed)
  '''

  # კალათის ობიექტის შექმნა
  cart = Cart(request)

  # პროდუქტის მიღება მონაცემთა ბაზიდან (404 თუ არ არსებობს)
  product = get_object_or_404(Product, id=product_id)

  # ფორმის დამუშავება POST მონაცემებით
  form = CartAddProductForm(request.POST)

  # ფორმის ვალიდაცია
  if form.is_valid():
    cd = form.cleaned_data    # ვალიდირებული მონაცემები: {'quantity': 2, 'override': False}
    cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
  
  return redirect('cart:cart-detail')     # url 'cart:cart-detail' შესაქმნელია


@require_POST
def cart_remove(request, product_id):
  '''
  პროდუქტის წაშლა კალათიდან

  მუშაობს მხოლოდ POST მეთოდით
  დანარჩენ მეთოდებზე (GET, PUT, DELETE) 405 შეცდომა (Method Not Allowed)
  '''

  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)

  cart.remove(product)

  return redirect('cart:cart-detail')     # url 'cart:cart-detail' შესაქმნელია


def cart_detail(request):
  '''
  კალათის შიგთავსის ჩვენება

  შესაძლო HTTP მეთოდი: GET
  '''

  cart = Cart(request)

  for item in cart:
    item['update_quantity_form'] = CartAddProductForm(
      initial={
        'quantity': item['quantity'],
        'override': True
      }
    )
  
  context = {
    'cart': cart,
  }

  return render(request, 'cart/cart_detail.html', context)