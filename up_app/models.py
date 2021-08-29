from django.db import models


class Delivery(models.Model):
    '''Доставка'''
    '''
    Курьером в пределах МКАД      350
    Курьером за МКАД              500
    По стране (почта России)      500
    Самовывоз (Коммунарка)          0
    '''
    name = models.CharField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Collection(models.Model):
    '''Колекции пряников'''
    '''
    День учителя
    8 Марта
    и т.д.
    ...
    '''
    name = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.name)


class OrderStatus(models.Model):
    '''Статус заказа'''
    '''
    В обработке.     Принят, но не обработан оператором
    Принят.          Обработан оператором, подтвержден
    Доставка.        Собран, доставляется
    Завершен.        Доставлен, получен
    Отменен.         Отменен оператором
    '''
    name = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    collection = models.ForeignKey(Collection, blank=True, null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    #article = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='media/', blank=True)
    description = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return '{}'.format(self.name)

    def add(self):
        pass

    class Meta:
        pass


class Cost(models.Model):

    price = models.IntegerField(default=0)
    size = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.price)


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=200)
    tel = models.CharField(max_length=20)
    comment = models.TextField(max_length=500)
    number = models.IntegerField(default=0)
    order_date = models.DateField(auto_now_add=True)
    extradition_date = models.DateField(blank=True)
    status = models.ForeignKey(OrderStatus, blank=False, default=None, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)



    def __str__(self):
        return '{} {}'.format(self.number, self.status)


class Cart(models.Model):
    # Номер заказа. Если в корзине order не пустой, то товар уже заказан
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return '{}'.format(self.session_key)



