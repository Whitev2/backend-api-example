<hr/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=40&pause=1000&color=373737&background=91C5F4&center=true&vCenter=true&multiline=true&width=1080&height=80&lines=WALLET+TEST+API)](https://git.io/typing-svg)
<hr/>

## Технологии
- Python 3.8;
- AioHttp ( Web framework for building client/server APIs );
- Docker and Docker Compose ( containerization );
- PostgreSQL ( database );
- Alembic ( database migrations made easy );
- Pydantic ( models )

<hr/>

## Установка и запуск:

1. Клонировать проект в удобное место:

```sh
git clone https://github.com/Whitev2/backend-api-example.git
```

2. Собрать и запустить контейнеры:
```sh
docker-compose up -d --build
```
<hr/>

## Информация:

- Модели баз данных создаются вместе с сборкой проекта в starter.sh
- В тестах был дабавлен параметр hash - его имитирует uuid
- Транзакции привязыватся к пользователю по uid
- Был исправлен url в тестах assert_balance
- Расширены тесты для проверки одинаковых транзакций - many_transaction

## Дополнительная часть:

- Dockerfile собирает проект и позволяет развертывать его в k8s
- Чтобы гарантировать транзакцию один раз, достаточно сделать проверку по hash, это реализовано в коде. Еще можно сделать проверка по hash + uid если есть вероятность повторного hash
- Уведомления для других сервисов - отличным решением будет служить брокер сообщений
- Для контроля качества работы сервиса можно обернуть его тестами и при деплое запускать их, если тесты не прошли - деплой будет отклонен. Сохранять аналитические данные и в дальнейшем обрабатывать их с целью выявления аномалий в работе сервиса
- В случае если пользователь попытается вывести сумму больше чем позволяет его баланс - сервис вызовет ошибку BadBalance и вернет 402 код