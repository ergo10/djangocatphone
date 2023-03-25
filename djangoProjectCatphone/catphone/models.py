from django.db import models
from django.urls import reverse, reverse_lazy


class Catsphone(models.Model):
    name = models.CharField(max_length=120, default='котофон', verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Цена')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Фотография')
    exist = models.BooleanField(default=True, verbose_name='В каталоге?')

    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True, verbose_name='Поставщик')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Котофон'
        verbose_name_plural = 'Котофоны'
    # ordering = ['name']


# ID (Django автоматически создаст)
# name
# description
# price
# date_create
# date_update
# photo
# exist (Логическое удаление)

class Supplier(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название поставщика')
    agent_name = models.CharField(max_length=100, verbose_name='Имя агента поставщика')
    agent_firstname = models.CharField(max_length=100, verbose_name='Фамилия агента поставщика')
    agent_patronymic = models.CharField(max_length=100, verbose_name='Отчество агента поставщика')
    exist = models.BooleanField(default=True, verbose_name='Сотрудничаем?')

    def get_absolute_url(self):
        return reverse('info_supp_view', kwargs={'supplier_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:  # Класс для названия нашей модельки в админке
        verbose_name = 'Поставщик'  # Надпись в единственном числе
        verbose_name_plural = 'Поставщики'  # Надпись во множественном числе
        ordering = ['title']  # Сортировка полей


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')
    price = models.FloatField(null=True, verbose_name='Стоимость заказа')
    address_delivery = models.CharField(max_length=150, verbose_name='Адрес доставки')
    status = models.CharField(max_length=150, verbose_name='Статус',
                              choices=[
                                  ('1', 'Создан'),
                                  ('2', 'Отменён'),
                                  ('3', 'Согласован'),
                                  ('4', 'В пути'),
                                  ('5', 'Завершён')
                              ]
                              )

    products = models.ManyToManyField(Catsphone, through='Pos_order')

    def __str__(self):
        return f"{self.date_create} {self.status} {self.price}"

    class Meta:  # Класс для названия нашей модельки в админке
        verbose_name = 'Заказ'  # Надпись в единственном числе
        verbose_name_plural = 'Заказы'  # Надпись во множественном числе
        ordering = ['date_create']  # Сортировка полей


class Pos_order(models.Model):
    product = models.ForeignKey(Catsphone, on_delete=models.CASCADE, verbose_name='Котофон')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    count_product = models.IntegerField(verbose_name='Количество котфонов')
    price = models.FloatField(verbose_name='Общая цена котофонов')

    def __str__(self):
        return self.product.name + " " + self.order.address_delivery + " " + self.order.status

    class Meta:  # Класс для названия нашей модельки в админке
        verbose_name = 'Позиция'  # Надпись в единственном числе
        verbose_name_plural = 'Позиции'  # Надпись во множественном числе
        ordering = ['product', 'order', 'price']  # Сортировка полей


class Chegue(models.Model):
    date_print = models.DateTimeField(auto_now_add=True, verbose_name='Дата распечатки')
    address_print = models.CharField(max_length=150, verbose_name='Место создания чека')
    terminal = models.CharField(max_length=10, verbose_name='Код терминала')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, verbose_name='Заказ')

    def __str__(self):
        return str(self.date_print) + " " + self.terminal

    class Meta:  # Класс для названия нашей модельки в админке
        verbose_name = 'Чек'  # Надпись в единственном числе
        verbose_name_plural = 'Чеки'  # Надпись во множественном числе
        ordering = ['terminal', 'date_print']  # Сортировка полей
