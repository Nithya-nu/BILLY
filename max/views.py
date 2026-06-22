from django.shortcuts import render, redirect

from max.models import Register,product,Cart
def index(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')

# Create your views here.
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')

        Register.objects.create(
            name=name,
            email=email,
            password=password,
            profile_pic=profile_pic
        )

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email, password=password)

            # Store user information in session
            request.session['email'] = user.email
            request.session['user_name'] = user.name

            return redirect('home')  # Replace with your home page URL name

        except Register.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'login.html')


from django.shortcuts import render, redirect
from .models import Cart, Register

def profile(request):
    email = request.session.get('email')

    if not email:
        return redirect('login')

    user = Register.objects.get(email=email)

    return render(request, 'profile.html', {
        'user': user
    })
from django.shortcuts import render, redirect, get_object_or_404

def edit_profile(request, id):
    user = get_object_or_404(Register, id=id)

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']

        user.save()

        return redirect('home')

    return render(request, 'editprofile.html', {'user': user})

from django.shortcuts import render, redirect
from .models import  Register


def add_product(request):
    if request.method == "POST":

        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product_image = request.FILES.get('product_image')

        # Get email from session
        email = request.session.get('email')

        # Find user using email
        user = Register.objects.get(email=email)

        # Create product
        Product = product.objects.create(
            user=user,
            product_name=product_name,
            description=description,
            price=price,
            stock=stock,
            product_image=product_image
        )

        Product.save()

        return redirect('home')

    return render(request, 'product.html')


def product_list(request):
    products = product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'productlist.html', context)



def my_products(request):
    products = product.objects.all()

    return render(
        request,
        'myproducts.html',
        {
            'products': products
        }
    )


def edit_product(request, id):

    products = get_object_or_404(product, id=id)
 

    if request.method == "POST":

        products.product_name = request.POST.get('product_name')
        products.description = request.POST.get('description')
        products.price = request.POST.get('price')
        products.stock = request.POST.get('stock')

        if request.FILES.get('product_image'):
            product.product_image = request.FILES.get('product_image')

        products.save()

        return redirect('my_products')

    return render(request, 'editproduct.html', {'product': products})


def delete_product(request, id):

    products = get_object_or_404(product, id=id)

    products.delete()

    return redirect('my_products')
def add_to_cart(request, product_id):
    products = get_object_or_404(product, id=product_id)
    email = request.session.get('email')
    userd = Register.objects.get(email=email)
    print(userd)

    cart_item, created = Cart.objects.get_or_create(
        user=userd,
        products=products
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('edit_cart')

def edit_cart(request):
    email = request.session.get('email')
    user = Register.objects.get(email=email)

    cart_items = Cart.objects.filter(user=user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render( request,
        'edit_cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
def update_cart(request, cart_id):
    email = request.session.get('email')
    user = Register.objects.get(email=email)
    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=user
    )

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('edit_cart')


def remove_cart_item(request, cart_id):
    email = request.session.get('email')
    user = Register.objects.get(email=email)
    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=user
    )

    cart_item.delete()

    return redirect('edit_cart')