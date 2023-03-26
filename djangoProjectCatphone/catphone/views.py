from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import Catsphone, Supplier, Order, Pos_order, Chegue
from .forms import CatphoneForm, SupplierForm, RegistrationForm, LoginForm, ContactForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import Default_value
from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

from django.http import JsonResponse
from .serializers import OrderSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from basket.forms import BasketAddProductForm


# Create your views here.

def index(request):
    print(request)
    return HttpResponse('Привет в магазине котофонов')


def product(request):
    products = Catsphone.objects.all()
    responce = '<h1>Список котофонов</h1>'
    for item in products:
        responce += f'<div>\n<p>{item.name}</p>\n<p>{item.price}</p></div>'
    # responce += '<h3>Samsung</h3>'
    # responce += '<h4>Meizu</h4>'
    return HttpResponse(responce)


def index_template(request):
    return render(request, 'catphone/index.html')


def product_template(request):
    context = {'title': 'Котофоны'}
    products = Catsphone.objects.all()

    # context['product_list'] = products

    paginator = Paginator(products, 2)
    page_num = request.GET.get('page', 1)

    page_objects = paginator.get_page(page_num)
    context['page_obj'] = page_objects

    if request.method == "GET":
        product_id = request.GET.get('id', 1)
        try:
            product_one = Catsphone.objects.get(pk=product_id)
        except:
            pass
        else:
            context['product_one'] = product_one

        context['name'] = request.GET.get('name', 'iphone')
    elif request.method == "POST":
        product_id = request.POST.get('id', 1)
        try:
            product_one = Catsphone.objects.get(pk=product_id)
        except:
            pass
        else:
            context['product_one'] = product_one

        context['name'] = request.POST.get('name')

    # context ={
    #     'title': 'Фрукты',
    #     'fruit_list': fruits,
    #     'fruit_one': fruit_one,
    #     'name': name
    # }

    return render(
        request=request,
        template_name='catphone/product-all.html',
        context=context
    )


@permission_required('catphone.add_product')
def product_add(request):
    if request.method == "POST":
        context = dict()
        context['name'] = request.POST.get('name')
        context['description'] = request.POST.get('description')
        context['price'] = request.POST.get('price')
        context['date_update'] = request.POST.get('date_update')
        context['photo'] = request.POST.get('photo')

        Catsphone.objects.create(
            name=context['name'],
            description=context['description'],
            price=context['price'],
            date_update=context['date_update'],
            photo=context['photo'],
        )
        return HttpResponseRedirect('/catphone/productsList/')
    else:
        catphoneform = CatphoneForm()
        context = {'form': catphoneform}
        return render(request, 'catphone/product-add.html', context=context)


@login_required()
def product_detail(request, product_id):
    product = get_object_or_404(Catsphone, pk=product_id)
    basket_form = BasketAddProductForm()
    # context=dict()
    return render(request, 'catphone/product-info.html', {'product_item': product, 'basket_form': basket_form})


def supplier_list(request):
    suppliers = Supplier.objects.filter(exist=True).order_by('title')
    return render(request, 'catphone/supplier/supplier-list.html',
                  {'supplier': suppliers, 'title': 'Список поставщиков из функции'})


paginate_by = 1


class SupplierListView(ListView, Default_value):
    model = Supplier  # Определение таблицы для взаимодействия
    template_name = 'catphone/supplier/supplier-list.html'  # путь шаблона (<Имя приложения>/<Имя модели-list.html>)
    context_object_name = 'supplier'  # Отправка данных по заданному ключу
    extra_context = {'title': 'Список поставщиков из класса'}  # Доп. значения (статичные значения)

    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Получение атрибутов из класса
        print(context)
        # context['title'] = 'Главная страница поставщиков'  # Переопределение ключа title

        # Использование Миксина из utils
        # Dv = Default_value()
        # context = Dv.add_title_context(context=context, title_name='Страница поставщиков')

        context = self.add_title_context(context=context, title_name='Страница поставщиков')

        context['info'] = 'Страница поставщиков, которые с нами работают'  # Добавление ключа info
        return context  # возврат словаря значений

    def get_queryset(self):
        return Supplier.objects.filter(exist=True).order_by('title')


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'catphone/supplier/supplier-info.html'
    context_object_name = 'one_supplier'  # (object)
    pk_url_kwarg = 'supplier_id'  # Переопределение ключа ID при получении (pk)


def supplier_form(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            Supplier.objects.create(
                title=form.cleaned_data['title'],
                agent_name=form.cleaned_data['agent_name'],
                agent_firstname=form.cleaned_data['agent_firstname'],
                agent_patronymic=form.cleaned_data['agent_patronymic'],
                exist=form.cleaned_data['exist'],
            )

            return redirect('list_supp')
        else:
            context = {'form': form}
            return render(request, 'catphone/supplier/supplier-add.html', context)
    else:
        form = SupplierForm()
        context = {'form': form}
        return render(request, 'catphone/supplier/supplier-add.html', context)


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm  # Определение формы для взаимодействия
    template_name = 'catphone/supplier/supplier-add.html'

    context_object_name = 'form'  # Переопределение ключа формы
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'catphone/supplier/supplier-edit.html'
    context_object_name = 'from'

    @method_decorator(permission_required('catphone.change_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(permission_required('catphone.delete_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('index_Catphone')
    else:
        form = RegistrationForm()
    return render(request, 'catphone/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            login(request, user)
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)
            return redirect('index_Catphone')
    else:
        form = LoginForm()
    return render(request, 'catphone/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('log in')


def contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['dorofeikulakov89@mail.ru'],
                fail_silently=False
            )
            if mail:
                return redirect('index_Catphone')
    else:
        form = ContactForm()
    return render(request, 'catphone/email.html', {'form': form})


@api_view(['GET', 'POST'])
def product_api_list(request):
    if request.method == "GET":
        fruit_list = Order.objects.all()
        serializer = OrderSerializer(fruit_list, many=True)
        return Response({'product_list': serializer.data})
    elif request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_api_detail(request, pk, format=None):
    product_obj = get_object_or_404(Catsphone, pk=pk)
    if product_obj.exist:
        if request.method == 'GET':
            serializer = OrderSerializer(product_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OrderSerializer(product_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'product': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            product_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
