# Стратегический DDD для платформы онлайн-аптеки и телемедицины



## 1. Домен

**Домен**: цифровое здравоохранение и фармацевтика

**Бизнес-возможности (5–10)**:

1. Регистрация и идентификация пациентов/врачей (с согласиями по ФЗ-152).
2. Видеоконсультация с врачом и ведение медкарты.
3. Выписка и проверка электронного рецепта.
4. Каталог лекарств и управление остатками.
5. Оформление заказа, оплата, страховое покрытие.
6. Сборка заказа фармацевтом и доставка курьером.
7. Обработка страховых выплат (взаимодействие со страховыми).
8. Уведомления и напоминания о приёме лекарств.


---

## 2. Поддомены

| Поддомен | Тип | Обоснование |
|----------|-----|-------------|
| **Телемедицинская консультация + электронный рецепт + связка «врач → рецепт → препарат»** | **Core** | Уникальная ценность: бесшовный путь «консультация → назначение → покупка». Конкуренты копируют по частям, но не целиком. Требует лучшей команды, глубокого DDD, event sourcing для медкарты. |
| Медкарта и история приёмов (клинические данные) | **Core** (второй, тесно связан с первым) | Регулируемая область (ФЗ-152, медтайна), определяет доверие и юридическую состоятельность. Ошибки критичны. Допустимо 1–2 core — здесь они образуют единое ядро «клинический путь». |
| Каталог лекарств и остатки | Supporting | Важно, но типово; есть готовые фарм-каталоги, но нужна кастомизация под рецептурность. |
| Оформление заказа и оплата | Supporting | Стандартная e-commerce логика, не даёт преимущества. |
| Доставка | Supporting | Логистика важна, но не уникальна (можно частично отдать на аутсорс курьерским сервисам). |
| Страховые выплаты | Supporting | Специфично, но регулируется внешними системами; интеграция, а не инновация. |
| Идентификация и доступ | Generic | Keycloak/Auth0. |
| Платежи | Generic | Stripe / ЮKassa. |
| Уведомления (email/SMS/push) | Generic | SendGrid, Twilio, Firebase. |
| Карты и геолокация | Generic | Google Maps / Яндекс.Карты. |
| Хранилище медданных по ФЗ-152 | Generic (инфраструктурный) | Специализированные провайдеры / облако с сертификацией. |


---

## 3. Bounded Contexts

| Контекст | Ответственность | Язык | Команда |
|----------|-----------------|-------------------|---------|
| **Identity & Consent** | Аккаунты, роли (пациент/врач/фармацевт/курьер), согласия по ФЗ-152 | `Account`, `Consent` | Platform team |
| **Teleconsultation** | Запись, видеосессия, статусы приёма | `Appointment`, `ConsultationSession` | Clinical core team |
| **Medical Record** | Медкарта, диагнозы, назначения, история | `PatientRecord`, `Diagnosis`, `Prescription` (черновик) | Clinical core team |
| **Prescribing** | Электронный рецепт: правила рецептурных препаратов, подпись врача, валидация фармацевтом | `Prescription` (Root), `PrescriptionLine` | Clinical core team |
| **Catalog & Inventory** | Карточки препаратов, цены, остатки, аналоги, рецептурность | `Drug`, `StockItem` | Pharmacy ops team |
| **Ordering** | Корзина, заказ, применение рецепта, оплата, страховое покрытие | `Order` (Root), `OrderLine`, `InsuranceClaim` (ссылка) | Commerce team |
| **Pharmacy Operations** | Сборка заказа, проверка рецепта фармацевтом, выдача | `DispensingTask` | Pharmacy ops team |
| **Delivery** | Слоты, курьеры, трекинг | `Delivery`, `Courier` | Logistics team |
| **Insurance** | Взаимодействие со страховыми, выплаты | `Claim`, `Coverage` | Commerce team |
| **Notifications** | Email/SMS/push, напоминания | `Notification` | Platform team |

**Обоснование границ**:

- **Язык**: «пациент» в Teleconsultation ≠ «покупатель» в Ordering ≠ «застрахованный» в Insurance; «рецепт» в Prescribing (юридический документ) ≠ «рецепт» в Ordering (ссылка-атрибут).
- **Транзакции**: рецепт и приём атомарны внутри клинического ядра; заказ и оплата — внутри Commerce.
- **Изменения**: клинические правила (мед. регламенты) меняются независимо от e-commerce правил (акции, слоты).
- **Команды**: Conway's Law — Clinical core, Commerce, Pharmacy ops, Logistics, Platform.

---

## 4. Ubiquitous Language

### Контекст: Teleconsultation (+ Prescribing, как продолжение клинического ядра)

| Термин | Значение | В коде |
|--------|----------|--------|
| Пациент (Patient) | Человек, получающий мед. помощь; в этом контексте — участник приёма | `class Patient` |
| Врач (Doctor) | Лицензированный специалист, проводящий приём | `class Doctor` |
| Приём (Appointment) | Запланированная консультация в слоте | `class Appointment` |
| Консультация (Consultation) | Состоявшаяся видеосессия с записью и итогом | `class ConsultationSession` |
| Назначение (Prescription) | Юридический документ: препарат, дозировка, срок | `class Prescription` (Root) |
| Рецептурный препарат (RxDrug) | Препарат, требующий рецепта | `enum DrugClass { RX, OTC }` |
| Подпись врача (DoctorSignature) | ЭЦП, придающая рецепту силу | VO `DoctorSignature` |
| Выписать рецепт (IssuePrescription) | Действие врача | `prescription.issue()` → `PrescriptionIssued` |
| Погасить рецепт (DispensePrescription) | Действие фармацевта при выдаче | `prescription.dispense()` → `PrescriptionDispensed` |

> Ключевое различие: в клиническом ядре «рецепт» = **юридический документ с инвариантами** (нельзя выписать без приёма, нельзя погасить дважды, срок действия). В Ordering «рецепт» = лишь **ссылка** `prescription_id` + признак валидности.

### Контекст: Ordering

| Термин | Значение | В коде |
|--------|----------|--------|
| Покупатель (Buyer) | Тот, кто оформляет заказ (может быть не пациентом — родственник) | `class Buyer` |
| Корзина (Cart) | Набор товаров до оформления | `class Cart` |
| Заказ (Order) | Оформленный заказ | `class Order` (Root) |
| Позиция заказа (OrderLine) | Строка заказа: препарат, кол-во, цена | `class OrderLine` |
| Ссылка на рецепт (PrescriptionRef) | ID рецепта + статус валидности (не сама модель рецепта!) | VO `PrescriptionRef` |
| Страховое покрытие (Coverage) | Доля, покрываемая страховой | VO `Coverage` |
| Оформить заказ (PlaceOrder) | Действие | `order.place()` → `OrderPlaced` |
| Подтвердить оплату (CapturePayment) | Действие платёжного шлюза | `payment.capture()` → `PaymentCaptured` |

> «Покупатель» ≠ «Пациент»: заказ может оформить родственник; в Ordering не нужны медданные. Это два разных контекста с разными моделями одного человека.

### Контекст: Catalog & Inventory

| Термин | Значение | В коде |
|--------|----------|--------|
| Препарат (Drug) | Карточка лекарства | `class Drug` |
| Класс препарата (DrugClass) | Rx/OTC | `enum DrugClass` |
| Остаток (StockItem) | Кол-во на складе/в аптеке | `class StockItem` |
| Аналог (Analog) | Заменяемый препарат | `class Drug.analogs` |
| Резерв (Reservation) | Забронированное кол-во под заказ | `class Reservation` |

---

## 5. Context Map

```text
                         ┌──────────────────────────┐
                         │  Identity & Consent      │
                         │  (OHS + PL)              │
                         └────────────┬─────────────┘
                                      │ OHS/PL (все контексты)
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌───────────────┐   Customer/Supplier   ┌───────────────┐   Customer/Supplier   ┌───────────────┐
│Teleconsultation│◀────────────────────▶│  Prescribing  │◀─────────────────────▶│ Medical Record│
│  (Customer)    │   Partnership + PL    │  (Supplier)   │   Partnership + PL     │  (Supplier)   │
└───────┬────────┘                       └───────┬───────┘                       └───────────────┘
        │                                        │ Published Language (события)
        │                                        ▼
        │                              ┌───────────────────┐
        │                              │  Ordering         │
        │                              │  (Customer)       │
        │                              └───┬───────────┬───┘
        │                                  │ ACL       │ C/S
        │                                  ▼           ▼
        │                          ┌───────────┐ ┌───────────────┐
        │                          │ Stripe    │ │Catalog & Inv. │
        │                          │ (внешн.)  │ │  (Supplier)   │
        │                          └───────────┘ └───────┬───────┘
        │                                                  │ Partnership
        │                                                  ▼
        │                                          ┌───────────────────┐
        │                                          │Pharmacy Operations│
        │                                          │  (Partnership)    │
        │                                          └─────────┬─────────┘
        │                                                    │ C/S
        │                                                    ▼
        │                                          ┌───────────────────┐
        │                                          │    Delivery       │
        │                                          │  (Customer)       │
        │                                          └─────────┬─────────┘
        │                                                    │ ACL
        │                                                    ▼
        │                                          ┌───────────────────┐
        │                                          │ Google Maps /     │
        │                                          │ курьерские API    │
        │                                          └───────────────────┘
        │
        │ C/S (события PrescriptionIssued → Insurance)
        ▼
┌───────────────────┐        ACL        ┌───────────────────┐
│    Insurance      │──────────────────▶│ Страховые системы │
│    (Customer)     │                   │   (внешние)       │
└───────────────────┘                   └───────────────────┘

   OHS = Open Host Service   PL = Published Language
   C/S = Customer/Supplier   ACL = Anticorruption Layer
```

**Hotspots на карте**:

1. **Prescribing ↔ Ordering**: как Ordering узнаёт о валидности рецепта? Через событие `PrescriptionIssued`/`PrescriptionRevoked` (PL) или синхронный запрос к Prescribing? Решение: **события + локальная проекция** `PrescriptionRef` в Ordering (eventual consistency).
2. **Teleconsultation ↔ Prescribing**: рецепт нельзя выписать без состоявшейся консультации. Это инвариант **клинического ядра**, значит Teleconsultation и Prescribing, возможно, должны быть **одним контекстом** или Partnership с сильной координацией. Оставлено как Hotspot для уточнения.
3. **Medical Record**: содержит те же `Prescription`, что Prescribing — риск дублирования. Решение: Medical Record хранит **ссылку и снапшот** рецепта, владелец модели — Prescribing.

---

## 6. Паттерны взаимодействия

| От | К | Паттерн | Обоснование |
|----|---|---------|-------------|
| Identity & Consent | Все контексты | **OHS + Published Language** | Много потребителей, стабильный API (JWT, роли, consent-флаги). |
| Teleconsultation | Prescribing | **Partnership** | Общие инварианты клинического ядра, релизы синхронны; возможно слияние — Hotspot. |
| Prescribing | Medical Record | **Partnership + PL** | Медкарта и рецепт меняются вместе, события `PrescriptionIssued` публикуются в PL. |
| Prescribing | Ordering | **Customer/Supplier + Published Language** | Ordering — Customer, потребляет события о рецептах; PL — схема событий (Avro). |
| Ordering | Catalog & Inventory | **Customer/Supplier** | Ordering может влиять на Catalog (запрос резерва, поле «рецептурность»). |
| Ordering | Payments (Stripe) | **ACL** | Изоляция от внешнего API, маппинг в `Money`, `PaymentStatus`. |
| Ordering | Pharmacy Operations | **Partnership** | Сборка заказа синхронна со статусами заказа, общие релизы. |
| Pharmacy Operations | Delivery | **Customer/Supplier** | Pharmacy ops — Customer (нужны слоты), Delivery — Supplier. |
| Delivery | Google Maps / курьеры | **ACL** | Внешние API, непредсказуемые изменения, нужен маппинг координат. |
| Ordering | Insurance | **Customer/Supplier + PL** | Ordering публикует `OrderPlaced`, Insurance реагирует; PL — схема claim. |
| Insurance | Страховые системы | **ACL** | Legacy/внешние, защита модели. |
| Все | Notifications | **Conformist** (к событиям) | Notifications подписан на события, не влияет на модель. |

---

## 7. Hotspots и открытые вопросы

1. **Граница Teleconsultation ↔ Prescribing**: один контекст или два? Инвариант «рецепт только после консультации» тянет к объединению; разные скорости изменений (клинические протоколы vs юридические правила рецептов) — к разделению. Требуется уточнение с бизнесом.
2. **Медкарта как отдельный контекст**: кто владеет `Prescription` — Medical Record или Prescribing? Черновик — решение: владелец Prescribing, Medical Record хранит снапшот.
3. **Синхронность валидации рецепта при оформлении заказа**: событийная (eventual) или синхронная проверка? Влияет на UX (нельзя оформить заказ с невалидным рецептом) и на доступность Prescribing.
4. **ФЗ-152 и хранение медданных**: где физически хранить (сертифицированное облако), как разделять PII и клинические данные между контекстами.
5. **Роль фармацевта**: в Pharmacy Operations или в Prescribing? Погашение рецепта — клиническое действие, но выполняется в аптеке. Сейчас — в Pharmacy Operations как `DispensingTask`, ссылающийся на Prescribing.
6. **Страховое покрытие**: рассчитывается в Ordering или Insurance? Сейчас — Insurance владеет `Coverage`, Ordering получает проекцию.

