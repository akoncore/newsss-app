
# Руководство по тестированию API в Postman

## Настройка окружения

### 1. Создание коллекции
1. Откройте Postman
2. Создайте новую коллекцию: `Django Blog API`
3. В настройках коллекции добавьте переменные:
   - `base_url`: `http://127.0.0.1:8000`
   - `access_token`: (будет заполнено автоматически)
   - `refresh_token`: (будет заполнено автоматически)
   - `user_id`: (будет заполнено автоматически)
   - `category_id`: (будет заполнено автоматически)
   - `category_slug`: (будет заполнено автоматически)
   - `post_id`: (будет заполнено автоматически)
   - `post_slug`: (будет заполнено автоматически)
   - `comment_id`: (будет заполнено автоматически)
   - `reply_comment_id`: (будет заполнено автоматически)
   - `subscription_id`: (будет заполнено автоматически)
   - `subscription_plan_id`: (будет заполнено автоматически)
   - `payment_id`: (будет заполнено автоматически)
   - `pinned_post_id`: (будет заполнено автоматически)

### 2. Настройка авторизации для коллекции
1. Перейдите в настройки коллекции → Authorization
2. Выберите Type: `Bearer Token`
3. В поле Token введите: `{{access_token}}`

## Тестирование аутентификации

### 1. Регистрация пользователя
**POST** `{{base_url}}/api/v1/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}
```

**Tests (вкладка Tests):**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response contains tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.expect(jsonData).to.have.property('refresh');
    pm.expect(jsonData).to.have.property('user');
    
    // Сохраняем токены и ID пользователя в переменные окружения
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
    pm.environment.set("user_id", jsonData.user.id);
});

pm.test("User data is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.user.email).to.eql("test@example.com");
    pm.expect(jsonData.user.username).to.eql("testuser");
});
```

### 2. Вход пользователя
**POST** `{{base_url}}/api/v1/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "email": "test@example.com",
    "password": "TestPassword123!"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Login successful", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.eql("User login successfully");
    
    // Обновляем токены и ID пользователя
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
    pm.environment.set("user_id", jsonData.user.id);
});
```

### 3. Получение профиля пользователя
**GET** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Profile data is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('email');
    pm.expect(jsonData).to.have.property('posts_count');
    pm.expect(jsonData).to.have.property('comments_count');
});
```

### 4. Обновление профиля
**PATCH** `{{base_url}}/api/v1/auth/profile/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my updated bio"
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Profile updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.first_name).to.eql("Updated");
    pm.expect(jsonData.last_name).to.eql("Name");
    pm.expect(jsonData.bio).to.eql("This is my updated bio");
});
```

## Тестирование тарифных планов подписок

### 1. Получение списка тарифных планов
**GET** `{{base_url}}/api/v1/subscribe/plans/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Subscription plans list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("Plan structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var plan = jsonData.results[0];
        pm.expect(plan).to.have.property('id');
        pm.expect(plan).to.have.property('name');
        pm.expect(plan).to.have.property('price');
        pm.expect(plan).to.have.property('duration_days');
        pm.expect(plan).to.have.property('features');
        pm.expect(plan).to.have.property('is_active');
        
        // Сохраняем ID плана для дальнейших тестов
        pm.environment.set("subscription_plan_id", plan.id);
    }
});
```

### 2. Получение детального плана подписки
**GET** `{{base_url}}/api/v1/subscribe/plans/{{subscription_plan_id}}/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Plan details are correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(pm.environment.get("subscription_plan_id"));
    pm.expect(jsonData).to.have.property('features');
    pm.expect(jsonData.features).to.be.an('object');
});
```

## Тестирование платежной системы

### 1. Создание Stripe Checkout сессии
**POST** `{{base_url}}/api/v1/payment/create-checkout-session/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "subscription_plan_id": {{subscription_plan_id}},
    "payment_method": "stripe",
    "success_url": "http://localhost:5173/payment/success?session_id={CHECKOUT_SESSION_ID}",
    "cancel_url": "http://localhost:5173/payment/cancel"
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Checkout session created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('checkout_url');
    pm.expect(jsonData).to.have.property('session_id');
    pm.expect(jsonData).to.have.property('payment_id');
    
    // Сохраняем ID платежа
    pm.environment.set("payment_id", jsonData.payment_id);
});

pm.test("Checkout URL is valid", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.checkout_url).to.include('checkout.stripe.com');
});
```

### 2. Получение статуса платежа
**GET** `{{base_url}}/api/v1/payment/payments/{{payment_id}}/status/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Payment status structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('payment_id');
    pm.expect(jsonData).to.have.property('status');
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData).to.have.property('subscription_activated');
});
```

### 3. Получение списка платежей пользователя
**GET** `{{base_url}}/api/v1/payment/payments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Payments list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("Payment structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var payment = jsonData.results[0];
        pm.expect(payment).to.have.property('id');
        pm.expect(payment).to.have.property('amount');
        pm.expect(payment).to.have.property('currency');
        pm.expect(payment).to.have.property('status');
        pm.expect(payment).to.have.property('payment_method');
        pm.expect(payment).to.have.property('user_info');
        pm.expect(payment).to.have.property('subscription_info');
        pm.expect(payment).to.have.property('is_successful');
        pm.expect(payment).to.have.property('can_be_refunded');
    }
});
```

### 4. Получение истории платежей
**GET** `{{base_url}}/api/v1/payment/payments/history/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Payment history is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});
```

### 5. Отмена платежа
**POST** `{{base_url}}/api/v1/payment/payments/{{payment_id}}/cancel/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Payment cancelled successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData.message).to.include('cancelled');
});
```

## Тестирование подписок

### 1. Получение статуса подписки пользователя
**GET** `{{base_url}}/api/v1/subscribe/status/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Subscription status structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('has_subscription');
    pm.expect(jsonData).to.have.property('is_active');
    pm.expect(jsonData).to.have.property('subscription');
    pm.expect(jsonData).to.have.property('pinned_post');
    pm.expect(jsonData).to.have.property('can_pin_posts');
});
```

### 2. Получение подписки пользователя
**GET** `{{base_url}}/api/v1/subscribe/my-subscription/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200 or 404", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 404]);
});

if (pm.response.code === 200) {
    pm.test("Subscription details are returned", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('id');
        pm.expect(jsonData).to.have.property('plan_info');
        pm.expect(jsonData).to.have.property('status');
        pm.expect(jsonData).to.have.property('is_active');
        pm.expect(jsonData).to.have.property('days_remaining');
        
        // Сохраняем ID подписки
        pm.environment.set("subscription_id", jsonData.id);
    });
}
```

### 3. Получение истории подписки
**GET** `{{base_url}}/api/v1/subscribe/history/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Subscription history is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("History entry structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var entry = jsonData.results[0];
        pm.expect(entry).to.have.property('id');
        pm.expect(entry).to.have.property('action');
        pm.expect(entry).to.have.property('description');
        pm.expect(entry).to.have.property('created_at');
    }
});
```

### 4. Отмена подписки
**POST** `{{base_url}}/api/v1/subscribe/cancel/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Subscription cancelled successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData.message).to.include('cancelled');
});
```

## Тестирование категорий

### 1. Получение списка категорий
**GET** `{{base_url}}/api/v1/posts/categories/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Categories list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});
```

### 2. Создание новой категории
**POST** `{{base_url}}/api/v1/posts/categories/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "name": "Technology",
    "description": "All about latest technology trends"
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Category created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.name).to.eql("Technology");
    pm.expect(jsonData.description).to.eql("All about latest technology trends");
    pm.expect(jsonData).to.have.property('slug');
    
    // Сохраняем ID и slug для последующих тестов
    pm.environment.set("category_id", jsonData.id);
    pm.environment.set("category_slug", jsonData.slug);
});
```

## Тестирование постов

### 1. Получение списка постов
**GET** `{{base_url}}/api/v1/posts/`

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Posts list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
    
    // Проверяем наличие информации о закрепленных постах
    if ('pinned_posts_count' in jsonData) {
        pm.expect(jsonData.pinned_posts_count).to.be.at.least(0);
    }
});

pm.test("Post structure includes pinning info", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var post = jsonData.results[0];
        pm.expect(post).to.have.property('is_pinned');
        pm.expect(post).to.have.property('pinned_info');
        pm.expect(post.pinned_info).to.have.property('is_pinned');
    }
});
```

### 2. Создание нового поста
**POST** `{{base_url}}/api/v1/posts/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post. It contains detailed information about various topics and provides valuable insights for readers.",
    "category": {{category_id}},
    "status": "published"
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Post created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.title).to.eql("My First Blog Post");
    pm.expect(jsonData.status).to.eql("published");
    pm.expect(jsonData).to.have.property('slug');
    pm.expect(jsonData).to.have.property('author');
    
    // Сохраняем ID и slug для последующих тестов
    pm.environment.set("post_id", jsonData.id);
    pm.environment.set("post_slug", jsonData.slug);
});
```

### 3. Получение детального поста (с информацией о закреплении)
**GET** `{{base_url}}/api/v1/posts/{{post_slug}}/`

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Post details include pinning information", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('is_pinned');
    pm.expect(jsonData).to.have.property('pinned_info');
    pm.expect(jsonData).to.have.property('can_pin');
    pm.expect(jsonData.pinned_info).to.have.property('is_pinned');
});

pm.test("Views count incremented", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.views_count).to.be.at.least(1);
});
```

### 4. Получение закрепленных постов
**GET** `{{base_url}}/api/v1/posts/pinned/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Pinned posts structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("All returned posts are pinned", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(post) {
            pm.expect(post.is_pinned).to.be.true;
        });
    }
});
```

### 5. Получение рекомендуемых постов
**GET** `{{base_url}}/api/v1/posts/featured/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Featured posts structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('pinned_posts');
    pm.expect(jsonData).to.have.property('popular_posts');
    pm.expect(jsonData).to.have.property('total_pinned');
    pm.expect(jsonData.pinned_posts).to.be.an('array');
    pm.expect(jsonData.popular_posts).to.be.an('array');
});

pm.test("Pinned posts limit is respected", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.pinned_posts.length).to.be.at.most(3);
});
```

## Тестирование закрепления постов

### 1. Проверка возможности закрепления поста
**GET** `{{base_url}}/api/v1/subscribe/can-pin/{{post_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Pin check response is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('post_id');
    pm.expect(jsonData).to.have.property('can_pin');
    pm.expect(jsonData).to.have.property('checks');
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData.post_id).to.eql(pm.environment.get("post_id"));
});

pm.test("Checks structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.checks).to.have.property('post_exists');
    pm.expect(jsonData.checks).to.have.property('is_own_post');
    pm.expect(jsonData.checks).to.have.property('has_subscription');
    pm.expect(jsonData.checks).to.have.property('subscription_active');
    pm.expect(jsonData.checks).to.have.property('can_pin');
});
```

### 2. Закрепление поста (требует активной подписки)
**POST** `{{base_url}}/api/v1/subscribe/pin-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post_id": {{post_id}}
}
```

**Tests:**
```javascript
pm.test("Status code is 201 or 403", function () {
    pm.expect(pm.response.code).to.be.oneOf([201, 403]);
});

if (pm.response.code === 201) {
    pm.test("Post pinned successfully", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('id');
        pm.expect(jsonData).to.have.property('post_info');
        pm.expect(jsonData).to.have.property('pinned_at');
        
        // Сохраняем ID закрепленного поста
        pm.environment.set("pinned_post_id", jsonData.id);
    });
} else {
    pm.test("Subscription required for pinning", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('error');
        pm.expect(jsonData.error).to.include('subscription');
    });
}
```

### 3. Получение закрепленного поста пользователя
**GET** `{{base_url}}/api/v1/subscribe/pinned-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200 or 404", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 404]);
});

if (pm.response.code === 200) {
    pm.test("Pinned post details are returned", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('id');
        pm.expect(jsonData).to.have.property('post_info');
        pm.expect(jsonData).to.have.property('pinned_at');
        pm.expect(jsonData.post_info).to.have.property('title');
        pm.expect(jsonData.post_info).to.have.property('slug');
    });
}
```

### 4. Получение списка всех закрепленных постов
**GET** `{{base_url}}/api/v1/subscribe/pinned-posts/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Pinned posts list structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("All posts have pinning information", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        jsonData.results.forEach(function(post) {
            pm.expect(post).to.have.property('is_pinned');
            pm.expect(post).to.have.property('pinned_at');
            pm.expect(post).to.have.property('author');
            pm.expect(post.is_pinned).to.be.true;
        });
    }
});
```

### 5. Открепление поста
**POST** `{{base_url}}/api/v1/subscribe/unpin-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200 or 404", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 404]);
});

if (pm.response.code === 200) {
    pm.test("Post unpinned successfully", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('message');
        pm.expect(jsonData.message).to.include('unpinned');
    });
}
```

## Тестирование комментариев

### 1. Получение списка всех комментариев
**GET** `{{base_url}}/api/v1/comments/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Comments list is returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results).to.be.an('array');
});

pm.test("Comment structure is correct", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        var comment = jsonData.results[0];
        pm.expect(comment).to.have.property('id');
        pm.expect(comment).to.have.property('content');
        pm.expect(comment).to.have.property('author_info');
        pm.expect(comment).to.have.property('replies_count');
        pm.expect(comment).to.have.property('is_reply');
    }
});
```

### 2. Создание основного комментария
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "content": "This is my first comment on this amazing blog post! Thank you for sharing such valuable information."
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Comment created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.content).to.eql("This is my first comment on this amazing blog post! Thank you for sharing such valuable information.");
    pm.expect(jsonData.post).to.eql(pm.environment.get("post_id"));
    pm.expect(jsonData.parent).to.be.null;
    pm.expect(jsonData.is_reply).to.be.false;
    pm.expect(jsonData.is_active).to.be.true;
    
    // Сохраняем ID комментария для дальнейших тестов
    pm.environment.set("comment_id", jsonData.id);
});
```

### 3. Создание ответа на комментарий
**POST** `{{base_url}}/api/v1/comments/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post": {{post_id}},
    "parent": {{comment_id}},
    "content": "Thank you for your comment! I'm glad you found the post helpful."
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Reply comment created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.parent).to.eql(pm.environment.get("comment_id"));
    pm.expect(jsonData.is_reply).to.be.true;
    
    // Сохраняем ID ответа
    pm.environment.set("reply_comment_id", jsonData.id);
});
```

### 4. Получение комментариев к конкретному посту
**GET** `{{base_url}}/api/v1/comments/post/{{post_id}}/`

**Headers:** (не требуется авторизация)

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Post comments data structure is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('post');
    pm.expect(jsonData).to.have.property('comments');
    pm.expect(jsonData).to.have.property('comments_count');
    pm.expect(jsonData.comments).to.be.an('array');
});

pm.test("Comments include replies", function () {
    var jsonData = pm.response.json();
    if (jsonData.comments.length > 0) {
        var mainComment = jsonData.comments.find(comment => comment.parent === null);
        if (mainComment) {
            pm.expect(mainComment).to.have.property('replies');
            pm.expect(mainComment.replies).to.be.an('array');
        }
    }
});
```

## Тестирование админской панели аналитики

### 1. Получение аналитики платежей (только для админов)
**GET** `{{base_url}}/api/v1/payment/analytics/`

**Headers:**
```
Authorization: Bearer {{admin_access_token}}
```

**Tests:**
```javascript
pm.test("Status code is 200 or 403", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 403]);
});

if (pm.response.code === 200) {
    pm.test("Payment analytics structure is correct", function () {
        var jsonData = pm.response.json();
        pm.expect(jsonData).to.have.property('total_payments');
        pm.expect(jsonData).to.have.property('successful_payments');
        pm.expect(jsonData).to.have.property('success_rate');
        pm.expect(jsonData).to.have.property('total_revenue');
        pm.expect(jsonData).to.have.property('monthly_revenue');
        pm.expect(jsonData).to.have.property('average_payment');
        pm.expect(jsonData).to.have.property('active_subscriptions');
    });
}
```

## Тестирование Webhook-ов (симуляция)

### 1. Симуляция успешного платежа через webhook
**POST** `{{base_url}}/api/v1/payment/webhooks/stripe/`

**Headers:**
```
Content-Type: application/json
Stripe-Signature: whsec_test_signature
```

**Body (JSON):**
```json
{
    "id": "evt_test_webhook",
    "object": "event",
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "id": "cs_test_session",
            "payment_status": "paid",
            "metadata": {
                "payment_id": "{{payment_id}}",
                "user_id": "{{user_id}}"
            }
        }
    }
}
```

**Tests:**
```javascript
pm.test("Status code is 200 or 400", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
});

// Примечание: Этот тест может не работать без правильной подписи Stripe
```

## Тестирование ошибок и валидации

### 1. Создание поста без авторизации
**POST** `{{base_url}}/api/v1/posts/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "title": "Unauthorized Post",
    "content": "This should fail"
}
```

**Tests:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Authentication error returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('detail');
});
```

### 2. Попытка закрепить пост без подписки
**POST** `{{base_url}}/api/v1/subscribe/pin-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post_id": {{post_id}}
}
```

**Tests:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});

pm.test("Subscription required error", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('error');
    pm.expect(jsonData.error).to.include('subscription');
});
```

### 3. Создание платежа с несуществующим планом
**POST** `{{base_url}}/api/v1/payment/create-checkout-session/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "subscription_plan_id": 999999,
    "payment_method": "stripe"
}
```

**Tests:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Plan not found error", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('subscription_plan_id');
});
```

### 4. Попытка закрепить чужой пост
**POST** `{{base_url}}/api/v1/subscribe/pin-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "post_id": {{other_user_post_id}}
}
```

**Tests:**
```javascript
pm.test("Status code is 400 or 403", function () {
    pm.expect(pm.response.code).to.be.oneOf([400, 403]);
});

pm.test("Permission error returned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('error');
});
```

## Расширенные тесты

### 1. Тест пагинации для постов с закрепленными
**GET** `{{base_url}}/api/v1/posts/?page=1&page_size=5`

**Tests:**
```javascript
pm.test("Posts pagination works with pinning", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
    pm.expect(jsonData.results.length).to.be.at.most(5);
    
    // Проверяем что закрепленные посты идут первыми
    if (jsonData.results.length > 0) {
        var pinnedPosts = jsonData.results.filter(post => post.is_pinned);
        var regularPosts = jsonData.results.filter(post => !post.is_pinned);
        
        // Если есть и закрепленные и обычные посты
        if (pinnedPosts.length > 0 && regularPosts.length > 0) {
            var lastPinnedIndex = jsonData.results.findLastIndex(post => post.is_pinned);
            var firstRegularIndex = jsonData.results.findIndex(post => !post.is_pinned);
            pm.expect(lastPinnedIndex).to.be.below(firstRegularIndex);
        }
    }
});
```

### 2. Тест фильтрации постов по категории с закрепленными
**GET** `{{base_url}}/api/v1/posts/categories/{{category_slug}}/posts/`

**Tests:**
```javascript
pm.test("Category posts include pinning information", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('category');
    pm.expect(jsonData).to.have.property('posts');
    pm.expect(jsonData).to.have.property('pinned_posts_count');
    
    if (jsonData.posts.length > 0) {
        jsonData.posts.forEach(function(post) {
            pm.expect(post).to.have.property('is_pinned');
            pm.expect(post).to.have.property('pinned_info');
        });
    }
});
```

### 3. Тест поиска по постам с учетом закрепленных
**GET** `{{base_url}}/api/v1/posts/?search=blog&ordering=-created_at`

**Tests:**
```javascript
pm.test("Search results maintain pinning priority", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 1) {
        var hasPinnedPosts = jsonData.results.some(post => post.is_pinned);
        var hasRegularPosts = jsonData.results.some(post => !post.is_pinned);
        
        // Если есть и закрепленные и обычные посты, закрепленные должны идти первыми
        if (hasPinnedPosts && hasRegularPosts) {
            var firstRegularIndex = jsonData.results.findIndex(post => !post.is_pinned);
            var lastPinnedIndex = jsonData.results.findLastIndex(post => post.is_pinned);
            pm.expect(lastPinnedIndex).to.be.below(firstRegularIndex);
        }
    }
});
```

### 4. Тест проверки истории подписки с закреплением постов
**GET** `{{base_url}}/api/v1/subscribe/history/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Subscription history includes pin actions", function () {
    var jsonData = pm.response.json();
    if (jsonData.results.length > 0) {
        // Проверяем возможные действия в истории
        var possibleActions = [
            'created', 'activated', 'renewed', 'cancelled', 
            'expired', 'payment_failed', 'post_pinned', 'post_unpinned'
        ];
        
        jsonData.results.forEach(function(entry) {
            pm.expect(possibleActions).to.include(entry.action);
            pm.expect(entry).to.have.property('description');
            pm.expect(entry).to.have.property('created_at');
        });
    }
});
```

## Комплексные интеграционные тесты

### 1. Полный цикл: регистрация → покупка подписки → закрепление поста
Этот тест следует запускать как последовательность запросов:

1. Регистрация пользователя
2. Получение списка планов
3. Создание checkout сессии
4. Симуляция успешного платежа (изменение статуса вручную в БД)
5. Создание поста
6. Закрепление поста
7. Проверка что пост отображается в закрепленных

### 2. Тест отмены подписки и автоматического открепления поста
**POST** `{{base_url}}/api/v1/subscribe/cancel/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

**Tests:**
```javascript
pm.test("Subscription cancelled and post unpinned", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.include('cancelled');
    
    // Проверяем что пост больше не закреплен
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/v1/subscribe/pinned-post/",
        method: 'GET',
        header: {
            'Authorization': 'Bearer ' + pm.environment.get("access_token")
        }
    }, function (err, response) {
        pm.expect(response.code).to.eql(404);
    });
});
```

## Тестирование производительности

### 1. Тест загрузки списка постов с большим количеством закрепленных
**GET** `{{base_url}}/api/v1/posts/?page_size=50`

**Tests:**
```javascript
pm.test("Large posts list loads within reasonable time", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000); // 2 секунды
});

pm.test("Response includes performance metadata", function () {
    var jsonData = pm.response.json();
    if ('pinned_posts_count' in jsonData) {
        pm.expect(jsonData.pinned_posts_count).to.be.a('number');
    }
});
```

## Очистка тестовых данных

### 1. Удаление закрепленного поста
**DELETE** `{{base_url}}/api/v1/subscribe/pinned-post/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

### 2. Отмена подписки
**POST** `{{base_url}}/api/v1/subscribe/cancel/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

### 3. Удаление комментариев
**DELETE** `{{base_url}}/api/v1/comments/{{comment_id}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

### 4. Удаление поста
**DELETE** `{{base_url}}/api/v1/posts/{{post_slug}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

### 5. Удаление категории
**DELETE** `{{base_url}}/api/v1/posts/categories/{{category_slug}}/`

**Headers:**
```
Authorization: Bearer {{access_token}}
```

### 6. Выход из системы
**POST** `{{base_url}}/api/v1/auth/logout/`

**Headers:**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "refresh_token": "{{refresh_token}}"
}
```

## Настройка администратора

### Создание суперпользователя для тестирования админских функций
```bash
# В терминале Django
python manage.py createsuperuser
```

### Получение админского токена
**POST** `{{base_url}}/api/v1/auth/login/`

**Body (JSON):**
```json
{
    "email": "admin@example.com",
    "password": "admin_password"
}
```

Сохраните полученный токен как `admin_access_token` в переменных окружения.

## Pre-request Scripts для коллекции

```javascript
// Проверяем доступность сервера
if (!pm.environment.get("base_url")) {
    pm.environment.set("base_url", "http://127.0.0.1:8000");
}

// Функция для генерации случайных данных
pm.globals.set("randomString", function() {
    return Math.random().toString(36).substring(2, 15);
});

// Проверяем что Django сервер запущен
if (pm.request.url.toString().includes(pm.environment.get("base_url"))) {
    pm.sendRequest({
        url: pm.environment.get("base_url"),
        method: 'GET'
    }, function (err, response) {
        if (err) {
            console.log("⚠️  Django server may not be running on " + pm.environment.get("base_url"));
        }
    });
}
```

## Рекомендуемый порядок выполнения тестов

1. **Настройка окружения и сервера**
2. **Аутентификация** (регистрация, вход)
3. **Тестирование тарифных планов**
4. **Создание тестовых данных** (категория, пост)
5. **Тестирование платежной системы**
6. **Тестирование подписок**
7. **Тестирование закрепления постов**
8. **Тестирование комментариев**
9. **Специальные эндпоинты** (популярные, закрепленные, рекомендуемые посты)
10. **Фильтрация и поиск с учетом закрепленных постов**
11. **Тестирование ошибок и edge cases**
12. **Интеграционные тесты**
13. **Админские функции** (аналитика, управление)
14. **Очистка тестовых данных**
15. **Выход из системы**

## Дополнительные переменные окружения

Добавьте в переменные окружения Postman:
- `admin_access_token`: токен администратора
- `other_user_token`: токен другого пользователя для тестов доступа
- `other_user_post_id`: ID поста другого пользователя
- `test_email`: email для тестирования
- `stripe_session_id`: ID Stripe сессии
- `webhook_secret`: секрет webhook для тестирования

## Запуск тестов

### Запуск Django сервера
```bash
python manage.py runserver
```

### Запуск Celery (для background задач)
```bash
celery -A config worker -l info
```

### Запуск Celery Beat (для периодических задач)
```bash
celery -A config beat -l info
```

### Создание тестовых планов подписки
```bash
python manage.py create_subscription_product
```

### Настройка Stripe интеграции
```bash
python manage.py fix_stripe_integration
```

## Collection Runner настройки

Для автоматического запуска:
1. Выберите коллекцию → Run collection
2. Установите задержку: 1000ms между запросами
3. Выберите окружение с переменными
4. Запустите в правильном порядке
5. Сохраните результаты тестирования

## Мониторинг и отладка

### Проверка логов Django
```bash
tail -f logs/django.log
```

### Мониторинг Celery задач
```bash
celery -A config events
```

### Проверка статуса Redis (если используется)
```bash
redis-cli ping
```

Это полное руководство поможет вам протестировать все функции вашего блог API с поддержкой подписок, платежей и закрепления постов.