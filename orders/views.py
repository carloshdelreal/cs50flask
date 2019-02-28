import json
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, get_object_or_404
from orders.forms import RegistrationForm, SellingArticleForm, MenuSelectedForm, CustomPizzaForm, CustomSubForm, OrderForm,SellingArticleFormset
from orders.models import Item, ItemGroup, Extras,Topping, ItemGroup, Order, CustomItem, SellingArticle
from django.http import Http404  

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
            ordered = json.loads(request.POST['orderString'])
            print(ordered)
            #Create Order
            o = Order()
            o.user = request.user
            o.placed = False
            o.delivered = False
            o.save()

            #Create Custom Items
            for key in ordered:
                it = Item.objects.get(pk=int(key))
                if it.customizable:
                    for i in range(ordered[key]):
                        ci = CustomItem()
                        ci.user = request.user
                        ci.item = it
                        ci.save()
                        sa = SellingArticle()
                        sa.sell_order = o
                        sa.item = ci
                        sa.save()
                else:
                    nci = CustomItem.objects.get(item__exact=it)
                    nsa = SellingArticle()
                    nsa.sell_order = o
                    nsa.item = nci
                    nsa.save()
            #print(context)
            
        return  redirect(reverse('orders:customizeorder'))

    else:
        #check if there is an order to customize
        try:
            o = Order.objects.filter(user__exact=request.user).filter(placed__exact=False)[0]
            thereisorder = True
        except:
            thereisorder = False
        if thereisorder:
            return  redirect(reverse('orders:customizeorder'))

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
        CustomPizza = CustomItem.objects.filter(user__exact=request.user)
        toppings = Topping.objects.all()
        extras = Extras.objects.all()
        form = MenuSelectedForm()
        context = {
            "regularPizza": regularPizza,
            "sicilianPizza": sicilianPizza,
            "subs": subs,
            "pasta": pasta,
            "salads": salads,
            "dinnerPlatters": dinnerPlatters,
            "custompizza":CustomPizza,
            "toppings": toppings,
            "extras": extras,
            "form": form
        }

        return render(request, "orders/menu.html", context)

def customizeorder(request):

    if request.method == "POST":
        o = Order.objects.filter(user__exact=request.user).filter(placed__exact=False).first()
        instances = o.items.all()
        itms = []
        counter = 0
        valid = True
        print("POST: " + str(request.POST))
        print(request.POST['submit'])
        if request.POST['submit'] == 'Discard':
            o.delete()
            return redirect(reverse('orders:menu'))
        for i in instances:
            if (i.item.itemGroup.itemGroup in ["Regular Pizza", "Sicilian Pizza"]) and i.item.customizable:
                #pizza
                form = CustomPizzaForm(request.POST or None, instance=i, prefix = "form-"+str(counter))
                counter += 1
            elif i.item.itemGroup.itemGroup in ['Subs']:
                ##sub
                form = CustomSubForm(request.POST or None, instance=i, prefix = "form-"+str(counter))
                counter += 1
            else:
                form = None
                
            itms.append({ "item": i,'form': form})
        for i in itms:
            if i['form']:
                if valid == False:
                    form.is_valid()
                else:
                    valid = i['form'].is_valid()
        if valid:
            for i in itms:
                if i['form']:
                    i['form'].save()
            return redirect(reverse('orders:cart'))
        
        
        context = {
            "items": itms
        }
        return render(request, "orders/customize.html", context)

        
        
        
    else:
        o = Order.objects.filter(user__exact=request.user).filter(placed__exact=False).first()
        if not o:
            raise Http404
        instances = o.items.all()
        itms = []
        counter = 0
        for i in instances:
            if (i.item.itemGroup.itemGroup in ["Regular Pizza", "Sicilian Pizza"]) and i.item.customizable:
                #pizza
                form = CustomPizzaForm(instance=i,prefix="form-"+str(counter))
                counter += 1
            elif i.item.itemGroup.itemGroup in ['Subs']:
                ##sub
                form = CustomSubForm(instance=i, prefix="form-"+str(counter))
                counter += 1
            else:
                form = None
            
            itms.append({ "item": i,'form': form})

        #print(itms) 
        context = {
            "items": itms
        }
        
        return render(request, "orders/customize.html", context)


def cart(request):
    if (request.method == "POST"):
        o = Order.objects.filter(user__exact=request.user).filter(placed__exact=False).first()
        form = OrderForm(request.POST or None, instance=o)
        if form.is_valid():
            o.placed = True
            o.save()
            form.save()
            return redirect(reverse('orders:succesfullyordered'))
        else:
            context = {
                'form': form
            }
            return render(request, "orders/cart.html",context)
    else:
        o = Order.objects.filter(user__exact=request.user).filter(placed__exact=False).first()
        if not o:
            raise Http404
        sa = SellingArticle.objects.filter(sell_order__exact=o)
        formset = SellingArticleFormset(queryset=sa)
        #print("formset:")
        #print(dir(formset))
        context = {
            'formset': formset,
            'formsetzip': zip(formset,sa),
            'order': o

        }
        return render(request, "orders/cart.html", context)

def succesfullyordered(request):
    return render(request, "orders/successfully_ordered.html")

def myorders(request):
    ordersQuery = Order.objects.filter(user__exact=request.user).filter(placed__exact=True).filter(delivered__exact=False)
    articles = []
    for orderQ in ordersQuery:
        orderList = []
        SellingArticleQuery = SellingArticle.objects.filter(sell_order__exact=orderQ)
        for a in SellingArticleQuery:
            orderList.append(a)
        articles.append((orderQ,orderList))
    
    return render(request, "orders/myorders.html", { "articles": articles })

def pendingorders(request):
    if request.method == 'POST':
        print(request.POST['submit'])
        o = Order.objects.get(pk=int(request.POST['submit']))
        o.delivered = True
        o.save()
        return redirect(reverse('orders:pendingorders'))
    else:
        ordersQuery = Order.objects.filter(placed__exact=True).filter(delivered__exact=False)
        articles = []
        for orderQ in ordersQuery:
            orderList = []
            SellingArticleQuery = SellingArticle.objects.filter(sell_order__exact=orderQ)
            for a in SellingArticleQuery:
                orderList.append(a)
            articles.append((orderQ,orderList))

        #"articles": zip(o.items.all(),sa )
        return render(request, "orders/pendingorders.html", { "articles": articles })