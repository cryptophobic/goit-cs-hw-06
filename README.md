## Технічний опис завдання

Вам необхідно реалізувати найпростіший вебдодаток, не використовуючи вебфреймворк.

### Інструкція та вимоги до виконання

За аналогією до розглянутого в конспекті прикладу, створіть вебдодаток з маршрутизацією для двох html-сторінок: index.html та message.html. За основу візьміть наступні файли.

Також:

обробіть під час роботи програми статичні ресурси: style.css, logo.png;
організуйте роботу з формою на сторінці message.html;
у разі виникнення помилки 404 Not Found повертайте сторінку error.html .
ваш HTTP-сервер повинен працювати на порту 3000.

Для роботи з формою створіть Socket-сервер на порту 5000. Алгоритм роботи має бути такий:

вводите дані у форму,
вони потрапляють у вебдодаток, який пересилає його далі на обробку за допомогою socket (протокол UDP або TCP на ваш вибір) Socket-серверу,
Socket-сервер переводить отриманий байт-рядок у словник і зберігає його в базу даних MongoDb.

Формат запису документа MongoDB має бути наступного вигляду:

```JSON
{  
	"date": "2022-10-29 20:20:58.020261",    
	"username": "krabaton",    
	"message": "First message"  
},  
{ 
	"date": "2022-10-29 20:21:11.812177",
	"username": "Krabat",    
	"message": "Second message"  
}
```

Ключ "date" кожного повідомлення — це час отримання повідомлення: datetime.now(). Тобто кожне нове повідомлення від вебпрограми має дописуватися до бази даних з часом отримання.

Результат

https://github.com/user-attachments/assets/4c0aa341-6545-4c3f-a9dc-0795df5024e8



