from django.shortcuts import render, redirect
from .forms import OrderClientPaymentForm
from .models import Order


def new_client_payment(request):
    if request.method == 'POST':
        form = OrderClientPaymentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            return redirect('success_page')
    else:
        order_id = request.GET.get('order_id')
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return redirect('failure_page')

        form = OrderClientPaymentForm(
            initial={
                "order_card": str(order),
                "remaining_amount": order.client_remaining_payable,
                "payment_amount": order.client_remaining_payable
            }
        )
    context = {'form': form}
    return render(request, 'Orders/form.html', context)
