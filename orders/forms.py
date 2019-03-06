from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ( AuthenticationForm, UserCreationForm )
from orders.models import Item, Extras, SellingArticle, Order, ItemGroup, CustomItem
from django.forms.widgets import HiddenInput

class LoginForm (AuthenticationForm):
    class Meta:
        model = User
        fields = [ 'username', 'password']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
    
       

class MenuSelectedForm(forms.Form):
    orderString = forms.CharField()

class CustomPizzaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomPizzaForm, self).__init__(*args, **kwargs)
        
        self.fields["topping"].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = CustomItem
        fields = ["topping"]
    
    def clean_topping(self):
        data = self.cleaned_data['topping']
        #print(data)
        #print(int(self.instance.item.itemName[:1]))
        if self.instance.item.itemName == 'Special':
            if len(data) == 5:
                return data
            else:
                raise forms.ValidationError("Special Pizza Must to have 5 Toppings!!, you put {}".format(len(data)))
        elif len(data) == int(self.instance.item.itemName[:1]):
            return data
        else:
            raise forms.ValidationError("The Number of Toppings has to coincide with the Item you are ordering, you are ordering {} and your item allows {} ".format(len(data), int(self.instance.item.itemName[:1])))


class CustomSubForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomSubForm, self).__init__(*args, **kwargs)
        
        self.fields["extra"].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = CustomItem
        fields = ["extra"]
    

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placed'].widget = HiddenInput()
    class Meta:
        model = Order
        fields = ['placed']
        
        
class SellingArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SellingArticleForm, self).__init__(*args, **kwargs)
        #self.fields["item"].disabled = True
        #self.fields["item"].widget.attrs = {'class': 'form-control'}
        self.fields["quantity"].widget.attrs = {'class': 'form-control'}
        self.fields["quantity"].min_value = 1

    class Meta:
        model = SellingArticle
        fields = ['quantity']

SellingArticleFormset = forms.modelformset_factory(SellingArticle, form=SellingArticleForm, extra=0)

class CustomItem_itemForm(forms.ModelForm):
    class Meta:
        model = CustomItem
        fields = ['item']