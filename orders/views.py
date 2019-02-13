import json
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from orders.forms import RegistrationForm, SellingArticleForm, MenuSelectedForm
from orders.models import Item, ItemGroup, Extras, ItemGroup

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("orders:login"))
    return render(request, "orders/index.html")

def profile(request):
    return render(request, "registration/profile.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            context = {
                'reg_user': request.POST['username'],
                'reg_email': request.POST['email'],
                'reg_name': request.POST['first_name'],
                'reg_lastName': request.POST['last_name'],
            }
            form.save()

            return render(request, 'registration/register_success.html', context)
        else:
            context = { 'form': form }
            return render(request, 'registration/register.html', context)
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

def menu(request):
    if request.method == "POST":
        form = MenuSelectedForm(request.POST)
        if form.is_valid():
            print(request.POST['orderString'])
            context = json.loads(request.POST['orderString'])
        return  redirect(reverse('orders:customizeorder'), context)

    else:        
        regularPizza = ItemGroup.objects.get(itemGroup="Regular Pizza")
        regularPizza = Item.objects.filter(itemGroup=regularPizza)
        sicilianPizza = ItemGroup.objects.get(itemGroup="Sicilian Pizza")
        sicilianPizza = Item.objects.filter(itemGroup=sicilianPizza)
        subs = ItemGroup.objects.get(itemGroup="Subs")
        subs = Item.objects.filter(itemGroup=subs)
        pasta = ItemGroup.objects.get(itemGroup="Pasta")
        pasta = Item.objects.filter(itemGroup=pasta)
        salads = ItemGroup.objects.get(itemGroup="Salads")
        salads = Item.objects.filter(itemGroup=salads)
        dinnerPlatters = ItemGroup.objects.get(itemGroup="Dinner Platters")
        dinnerPlatters = Item.objects.filter(itemGroup=dinnerPlatters)
        form = MenuSelectedForm()
        context = {
            "regularPizza": regularPizza,
            "sicilianPizza": sicilianPizza,
            "subs": subs,
            "pasta": pasta,
            "salads": salads,
            "dinnerPlatters": dinnerPlatters,
            "form": form
        }

        return render(request, "orders/menu.html", context)

def cart(request):
    if(request.method == "POST"):
        ig = ItemGroup.objects.get(pk=2)
        form = SellingArticleForm(ig,request.POST)
        if form.is_valid():
            form.save(request)
            return redirect(reverse('orders:succesfullyordered'))
        else:
            context = {
                'form': form
            }
            return render(request, "orders/cart.html",context)
    else:
        ig = ItemGroup.objects.get(pk=2)
        form = SellingArticleForm(ig)
        context = {
            'form': form
        }
        return render(request, "orders/cart.html",context)

def customizeorder(request):
    
    context = {

    }
    return render(request, "orders/customize.html", context)

def succesfullyordered(request):
    return render(request, "orders/successfully_ordered.html")