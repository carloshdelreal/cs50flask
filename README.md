# Project 3

Web Programming with Python and JavaScript

## Pizza Project

the pizza project is a web application that allows the customers of the **Pinocchio's Pizza & Subs restaurant** to order their favourite Pizza, Subs and other delicious dishes though the web. this web application, allows to the administrator of the restaurant to have a control of the orders and lists all the pending orders that have been realized.

### The orders Django Application

the orders application is basically a module in python that contains all of the classes variables methods and configurations that the project uses, it contains the following files:

1. [models.py](#models-py)
2. [admin.py](#admin-py)
3. [urls.py](#urls-py)
4. [forms.py](#forms-py)
5. [views.py](#views-py)

### models.py

it contains the definition of the models used for the application.

#### Item

The Item model defines the base caracteristics of an each item in the menu, It has the fields itemName, ItemGroup that classify the items, size in which the user can define empty value, small or large. Price that it is the base for each menu item and a boolean value that determines if an item is customizable or not.

#### ItemGroup

Its the model that contains the group name of items of the menu, those are: Regular Pizza, Sicilian Pizza, Subs, Pasta, Salad, And Dinner Platters

#### CustomItem

a custom item is defined by an user or author, item, extra and toppings, which are available if the item is customizable. this is a layer of interface that allows the user add extras or toppings to an ordered item dependin on the type of the item it is ordering and therefore calculate the value depending on the chosen extras. it defines the property getters full_name and total_price that compute the full name of the item (the name of the item plus the extras or toppings) and the total price, the price of the item plus the price of the toppings or extras.

the toppings and extras are defined with a many to many relation, for representing the possibility of several toppings or extras in the same CustomItem

#### Order

its an object created for representing a custom order, it has the user field, created_date, placed_date, placed, delivered and the items many to many relations though the Selling article model. this is used to represent several items in the same order and the possibility of adding the quantity of an item to be selled.

### admin.py

it contains the definition of the admin classes used for handling the models and it was used for adding the full menu to the mysql database, otherwise would be tremendously tedious.

### urls.py

it contains the definition of the links for the orders application and the relation between the views and the urls, as well as it contains the names given to each url for the use in the templates.

### forms.py

contains the forms used for structuring the web application, the login form, registration, MenuSelectedForm, customPizzaForm, CustomSubForm, OrderForm, SellingArticleForm, CustomItem_itemForm. 

in this module are also defined some of the methods used for the validation of the data.

### views.py

in this module are defined the views used for the web application.
