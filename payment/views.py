from django.shortcuts import render
from cart.cart import CartHandler
# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Order, OrderItem
from user_app.models import User
from .forms import PaymentForm
from midtransclient import Snap
from django.contrib.auth.decorators import login_required
import time
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        # Hitung total
        cart = CartHandler(request)
        totals = cart.cart_total()

        if form.is_valid():
            # Buat pesanan dan tetapkan pengguna
            order = form.save(commit=False)
            order.user = request.user
            order.amount_paid = totals
            order.status = False
            order.save()

            # Buat item pesanan
            cart_products = cart.get_prodss()
            for post in cart_products:
                post_id = post.id
                price = post.price

                # Buat OrderItem
                OrderItem.objects.create(
                    order=order,
                    post_id=post_id,
                    user=request.user,
                    price=price
                )

            # Buat transaksi menggunakan Snap
            snap = Snap(
                client_key='SB-Mid-client-1BPQEpo-ZNXfhfDB',
                server_key='SB-Mid-server-80qy6PpZXuTGZOQc_-riaYQ9',
            )

            # Buat transaksi
            transaction = {
                "transaction_details": {
                    "order_id": f"order-{order.id}-{int(time.time())}",
                    "gross_amount": float(totals),
                },
                "credit_card": {
                    "secure": True
                },
                "callbacks": {
                    "finish": "https://bb0e-36-83-205-186.ngrok-free.app/payment/finish/"
                },
            }
            print("Transaction payload:", transaction)

            # Dapatkan URL pembayaran
            response = snap.create_transaction(transaction)
            print("Transaction response:", response)

            redirect_url = response.get('redirect_url')
            if redirect_url:
                return redirect(redirect_url)
            else:
                raise ValueError("Redirect URL tidak ditemukan.")

    else:
        form = PaymentForm()

    # Ambil produk keranjang dan total untuk permintaan GET
    cart = CartHandler(request)
    cart_products_student = cart.get_prodss()
    totals = cart.cart_total()

    return render(request, "payment/payment.html", {
        'form': form,
        'cart_products_student': cart_products_student,
        "totals": totals,
    })

def payment_t(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        # Calculate totals
        cart = CartHandler(request)
        totals = cart.cart_total()

        if form.is_valid():
            # Create the order and assign the user
            order = form.save(commit=False)
            order.user = request.user  # Assign the logged-in user
            order.amount_paid = totals
            order.status = False
            order.save()

            # Create order items
            cart_products = cart.get_prods()  # Fetch products from the cart
            for product in cart_products:
                product_id = product.id
                price = product.sell_price  # Use the selling price

                # Create OrderItem
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,  # Reference the Product model
                    user=request.user,  # Optionally associate user with OrderItem
                    price=price
                )

            messages.success(request, "Order placed successfully!")
            return redirect('post_list')

    else:
        form = PaymentForm()

    # Fetch cart products and totals for GET request
    cart = CartHandler(request)
    cart_products = cart.get_prods()  # Use 'get_prods' to fetch products
    totals = cart.cart_total()

    return render(request, "payment/payment_.html", {
        'form': form,
        'cart_products': cart_products,
        "totals": totals,
    })

def payment_finish(request):
    # Dapatkan data dari query string Midtrans
    order_id = request.GET.get('order_id')
    status_code = request.GET.get('status_code')
    transaction_status = request.GET.get('transaction_status')

    print("Query Params:", request.GET)  # Debug: Tampilkan query parameters

    # Pastikan order_id valid dan ambil angka dari order_id
    if order_id:
        try:
            order_id_number = int(order_id.split('-')[1])  # Ambil angka dari order_id
            order = Order.objects.filter(id=order_id_number).first()
        except (IndexError, ValueError):
            order = None
            transaction_status = 'error'
            message = "Order ID tidak valid."
    else:
        order = None
        message = "Order ID tidak ditemukan."
    
    # Periksa status transaksi dan lakukan logika tertentu
    if transaction_status == 'settlement':
        message = "Pembayaran berhasil! Pesanan Anda sedang diproses."
        if order:
            order.status = True  # Perbarui status pesanan di database
            order.save()
    elif transaction_status == 'pending':
        message = "Pembayaran Anda masih tertunda. Silakan selesaikan pembayaran Anda."
    elif transaction_status == 'deny':
        message = "Pembayaran ditolak. Silakan coba lagi."
    elif transaction_status == 'cancel':
        message = "Pembayaran dibatalkan oleh pengguna."
    elif transaction_status == 'expire':
        message = "Waktu pembayaran telah habis."
    else:
        message = "Terjadi kesalahan pada pembayaran."

    # Tampilkan halaman selesai
    return render(request, 'payment/finish.html', {
        'order': order,
        'message': message,
        'transaction_status': transaction_status,
        'status_code': status_code,
    })


@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        # Ambil notifikasi dari Midtrans
        notification = json.loads(request.body.decode('utf-8'))
        order_id = notification.get('order_id')

        # Ekstrak angka dari order_id
        order_id_number = int(order_id.split('-')[1])  # Ambil angka dari order_id

        # Cari pesanan berdasarkan order_id yang sudah diekstrak
        order = Order.objects.filter(id=order_id_number).first()

        transaction_status = notification.get('transaction_status')

        # Perbarui status pesanan di database
        if transaction_status == 'settlement' and order:
            order.status = True
            order.save()
        elif transaction_status in ['cancel', 'deny', 'expire'] and order:
            order.status = False
            order.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)