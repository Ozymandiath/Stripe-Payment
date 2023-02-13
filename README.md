<h2> Запуск проекта </h2>
<hr>

Сначала загрузите проект: `git clone https://github.com/Ozymandiath/Stripe-Payment.git`

После загрузки выполните команду: `pip install -r requirements.txt`

Далее выполните: `python manage.py migrate` 

Теперь нам нужно получить доступ в админку.

Для того чтобы добавить данные в нашу базу данных, для этого выполним эту команду: `python manage.py createsuperuser`

После входа в админку и заполнения данных, можно приступать к работе.

<h2> Функционал проекта </h2>
<hr>

В доступе имеется несколько GET запросов.
Первый запрос: `/item/{id}` он нужен, чтобы выбрать конкретную позиция и оплатить ее.

Второй запрос: `/order` он используется после того как в админке объединили несколько позиций в один заказ.


<h2> Проект в живую </h2>
<hr>

По этим ссылкам можно понять как функционирует проект, прежде чем запускать его у себя.

Вход в админку:

[http://ozymandiath.pythonanywhere.com/admin/](http://ozymandiath.pythonanywhere.com/admin/)

Просмотр группы заказов:

[http://ozymandiath.pythonanywhere.com/order/](http://ozymandiath.pythonanywhere.com/order/)

Просмотр одного товара:

[http://ozymandiath.pythonanywhere.com/item/1](http://ozymandiath.pythonanywhere.com/item/1)