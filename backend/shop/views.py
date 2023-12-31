from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ProductQuantityForm, ReviewForm, UserEditForm, UserRegisterForm
from .models import Cart, CartItem, Category, Product, User

# Create your views here.


def handle_carts(request, user):
    # There are 3 scenarios
    # Old Cart && no new cart
    # Old cart && new cart
    # no old cart && new cart
    old_cart_id = request.session.get("active_cart_id")

    if old_cart_id:
        old_cart = Cart.objects.get(pk=old_cart_id)
    else:
        old_cart = None

    try:
        active_cart = user.carts.get(status="active")
    except Exception:
        active_cart = None

    if old_cart and not active_cart:
        old_cart.user = user
        old_cart.save()

    elif old_cart and active_cart:
        old_cart_items = old_cart.items.all()

        for item in old_cart_items:
            try:
                existing_active_item = active_cart.items.get(product=item.product)
                existing_active_item.quantity += item.quantity
                existing_active_item.save()
            except Exception:
                new_item = CartItem(
                    product=item.product, quantity=item.quantity, cart=active_cart
                )

    del request.session["active_cart_id"]
    old_cart.delete()


# Index & Product Views
class IndexView(View):
    def get(self, request):
        top_level_categories = Category.objects.filter(parent_category=None)
        latest_products = Product.objects.all().order_by("-updated_at")[:8]

        # TODO Pass in Top Selling products
        # TODO Pass in some recommended products for logged in users

        return render(
            request,
            "shop/front_page.html",
            {"latest_products": latest_products, "categories": top_level_categories},
        )

    def post(self, request):
        pass


class ProductListView(ListView):
    # Pass in products ordered by top selling by default
    template_name = "shop/product_list.html"
    model = Product
    paginate_by = 12
    context_object_name = "product_list"


class ProductDetailView(View):
    def get(self, request, slug):
        # TODO pass in review avg and count
        product = Product.objects.get(slug=slug)
        all_reviews = product.reviews.all()
        review_form = ReviewForm()
        quantity_form = ProductQuantityForm()

        return render(
            request,
            "shop/single_product.html",
            {
                "product": product,
                "reviews": all_reviews,
                "review_form": review_form,
                "quantity_form": quantity_form,
            },
        )

    def post(self, request, slug):
        user = self.request.user
        product = Product.objects.get(slug=slug)
        review_form = ReviewForm(self.request.POST)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = user
            new_review.product = product
            new_review.save()

        return redirect("single_product", slug=slug)


class ProductCategoryListView(ListView):
    template_name = "shop/product_list.html"
    paginate_by = 10
    context_object_name = "product_list"

    def get_queryset(self):
        self.slug = self.kwargs["slug"]
        return Product.objects.filter(
            Q(categories__slug=self.slug)
            | Q(categories__parent_category__slug=self.slug)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.slug
        return context


# User Profile
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(
            initial={
                "avatar": request.user.avatar,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "bio": request.user.bio,
            }
        )

        return render(request, "shop/user_profile.html", {"form": user_form})

    def post(self, request):
        user_form = UserEditForm(request.POST)

        if user_form.is_valid():
            user_form.save()

        return render(request, "shop/user_profile.html", {"form": user_form})


class UserRegisterView(View):
    def get(self, request):
        register_form = UserRegisterForm()

        return render(request, "registration/register.html", {"form": register_form})

    def post(self, request):
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            form_data = register_form.clean()

            new_user = User.objects.create_user(
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                username=form_data["username"],
                email=form_data["email"],
                phone=form_data["phone"],
                password=form_data["password"],
            )

            return redirect("login")

        return render(request, "registration/register.html", {"form": register_form})


class UserLoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        # breakpoint()
        return render(request, "registration/login.html", {"form": login_form})

    def post(self, request):
        # Login & Merge old cart with new Cart
        login_form = AuthenticationForm()
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        handle_carts(request, user)

        if user is not None:
            login(request, user)

            return redirect(reverse("profile"))
        else:
            login_form = AuthenticationForm({"username": username, "password": ""})
            return render(
                request,
                "registration/login.html",
                context={"form": login_form, "error": "Your credentials are invalid."},
            )


# Cart View
class CartAddView(View):
    # TODO Handle if Item is already in shopping cart
    def post(self, request, id):
        product_quantity = int(request.POST["quantity"])
        product = Product.objects.get(pk=id)
        user = request.user

        # Get the active cart for authenticated and non-authenticated users
        if user.is_authenticated:
            try:
                active_cart = user.carts.get(status="active")
            except Exception:
                active_cart = Cart(created_by=user, status="active")
                active_cart.save()

        else:
            active_cart_id = request.session.get("active_cart_id")
            if active_cart_id:
                active_cart = Cart.objects.get(pk=active_cart_id)
            else:
                active_cart = Cart(status="active")
                active_cart.save()
                request.session["active_cart_id"] = active_cart.id

        # Add quantity if cart item already is in cart
        try:
            cart_item = active_cart.items.get(product=product)
            cart_item.quantity += product_quantity

        except Exception:
            cart_item = CartItem(
                product=product,
                quantity=product_quantity,
                cart=active_cart,
            )

        cart_item.save()

        return redirect(request.META["HTTP_REFERER"])


class CartOrderView(View):
    pass


# Order Views
class OrderListView(ListView):
    pass


class OrderView(View):
    pass
