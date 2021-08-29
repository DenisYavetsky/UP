from django.shortcuts import render
from .models import *
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
from django.http import HttpResponse
from django.urls import reverse
from django.core import serializers
from .forms import OrderForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max, Min


def product_list(request):
    data = Product.objects.all()
    collection = Collection.objects.all()
    return render(request, 'up_app/main.html', context={'data': data, 'collection': collection})


def cart_delete(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if cart:
        cart.delete()
    return redirect('cart')


def plan(request):
    from up_app.custom_script import get_dates_of_week
    days = get_dates_of_week(0)

    orders = Order.objects.all()
    for o in orders:

        if o.extradition_date:

            a = o.extradition_date.strftime('%B %d')
            for i in range(len(days)):
                ext = {
                    'n_order': '',
                    'products': [
                    ]
                }
                carts = Cart.objects.all().filter(order=o)
                for cart in carts:
                    name = cart.product.name
                    count = cart.count

                    pr = {'name': '',
                          'count': ''}

                    if days[i]['month'] + ' ' + days[i]['day'] == a:
                        if ext['n_order'] != str(o.number):

                            ext['n_order'] = str(o.number)
                            pr['name'] = name
                            pr['count'] = count
                            ext['products'].append(pr)
                            days[i]['extraditions'].append(ext)  # = 'Выдача: Заказ №' + str(o.number)
                        else:

                            pr['name'] = name
                            pr['count'] = count
                            days[i]['extraditions'][0]['products'].append(pr)
    print(days)
    return render(request, 'up_app/plan.html', context={'days': days})


def cart(request):
    total = 0
    count = 0
    # При создании заказа корзинам надо прислоить id заказа
    # Если у корзины есть не нулевой статус то эти корзины считаются закрытыми и не выводятся пользователю
    form = OrderForm()
    # Корзины
    carts = Cart.objects.filter(session_key=request.session.session_key, order__number__isnull=True)
    print(request.session.session_key)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        number = Order.objects.all().aggregate(Max('number'))

        if form.is_valid():

            # статус - В обработке
            status = get_object_or_404(OrderStatus, pk=1)
            Ord = form.save(commit=False)
            Ord.status = status
            # номер новой заявки
            if str(number['number__max']) == 'None':
                Ord.number = 1
            else:
                Ord.number = number['number__max'] + 1
            # Ord.number = 1
            Ord.save()
            for cart in carts:
                cart.order = Ord
                cart.save()
            return redirect('catalog')

    for d in carts:
        total = total + (d.count * d.cost)
        count = count + d.count
    return render(request, 'up_app/cart.html', context={'data': carts, 'total': total, 'form': form, 'count': count})


def filter123(request):
    session_key = request.session.session_key

    if len(request.GET) > 0:
        val = []
        checkbox = request.GET
        for c in checkbox:
            if checkbox[c] == 'check':
                val.append(int(c[0]))
        if len(val) > 0:
            data = Product.objects.filter(collection__in=val)
        else:
            data = Product.objects.all()
    else:
        data = Product.objects.all()

    # collection = Collection.objects.all()
    cart = Cart.objects.all()
    # count = cart.filter(session_key=session_key).count()
    data = serializers.serialize('json', data)
    # return render(request, 'up_app/index.html', context={'data': data, 'count': count, 'collection': collection})
    return HttpResponse(data, content_type='application/json')


def catalog(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    data = Product.objects.all()

    collection = Collection.objects.all()
    cart = Cart.objects.all()

    count = cart.filter(session_key=session_key, order__number__isnull=True).count()

    return render(request, 'up_app/index.html', context={'data': data, 'count': count, 'collection': collection})


def product_change(request):
    cart = get_object_or_404(Cart, pk=request.POST['cartId'])
    cart.count = request.POST['count']
    cart.save()
    return redirect('cart')


def product_add(request):
    collection = Collection.objects.all()
    data = Product.objects.all()
    # получить по сессии есть ли такие корзины
    # найти товар с id в этих корзинах
    # если есть изменить количество
    # если нет создать новую корзину
    cart = Cart.objects.all()
    tmp = cart.filter(session_key=request.session.session_key, order__number__isnull=True)
    if tmp.count() >= 1:
        tmp2 = tmp.filter(product=request.POST['product'])
        if tmp2.count() > 0:
            # изменяем запись добавляя count
            c = tmp2.get(product=request.POST['product'])
            c.count += int(request.POST['count'])
            c.cost = data.get(pk=request.POST['product']).price
            c.save()
        else:
            # если не найдено создаем новыу корзину
            c = Cart()
            c.session_key = request.session.session_key
            c.count = int(request.POST['count'])
            c.cost = data.get(pk=request.POST['product']).price
            c.product = Product.objects.get(pk=request.POST['product'])
            c.save()

    else:
        # если нет корзин
        c = Cart()
        c.session_key = request.session.session_key
        c.count = int(request.POST['count'])
        c.cost = data.get(pk=request.POST['product']).price
        c.product = Product.objects.get(pk=request.POST['product'])
        c.save()

    cart = Cart.objects.all()

    return render(request, 'up_app/index.html', context={'data': data, 'cart': cart, 'collection': collection})


def parse(request):
    header = {'accept': '*/*',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(HTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

    # Адрес для парсинга
    url = 'https://www.livemaster.ru/ulicapryanikov'

    request = requests.get(url, headers=header)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        cards = soup.find_all('div', {'class': 'col-xs-6 col-sm-3 col-md-3'})
        # создание нового продукта

        for card in cards:
            p = Product()
            title = card.find('div', {'class': 'item-preview__info-container'}).find_all(['span'])
            p.name = title[0].text
            print(title[1].text)
            a = (title[1].text).split()
            b = ''.join(a)
            p.price = b[:-3]

            sss = str(card.find_all(['img'])[0])
            path = sss[sss.find('http'):sss.find('jpg') + 3]
            # print('media/' + (title[0].text).replace('"', '') + '.jpg')
            out = open(
                'C:/Users/User/PycharmProjects/ulicaPryanikov/media/' + (title[0].text).replace('"', '') + '.jpg',
                'wb')
            p.picture = (title[0].text).replace('"', '') + '.jpg'
            p.description = '123'
            p.save()

            resource = urllib.request.urlopen(path)
            out.write(resource.read())
            out.close()


def get_delivery(request, pk):
    if request.is_ajax():
        delivery = Delivery.objects.get(pk=pk)
        return HttpResponse(delivery.price)


def search(request):
    q = ''
    if request.is_ajax():
        q = request.GET.get('q')
    return render(request, 'up_app/res.html', {'q': q})


def test(request):
    # if request == 'POST':

    # param = request.GET.get('time','Fail')

    return render(request, 'up_app/test.html')
