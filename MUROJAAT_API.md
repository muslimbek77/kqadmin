# Murojaatlar API

Swagger hujjati:

- `/api/swagger/`
- `/api/schema/`

## Telegram sozlamalari

Asosiy usul:

- Django admin paneldagi `Telegram sozlamalari`
- `bot_token`
- `admin_chat_id`

Agar `assigned_telegram_chat_id` yuborilsa, shu chat ID ishlatiladi. Aks holda admin paneldagi `admin_chat_id` ishlatiladi.

Zaxira usul sifatida quyidagi environment o'zgaruvchilari ham ishlaydi:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DEFAULT_CHAT_ID`

Telegram yuborish logikasi:

- agar `attachment` bo'lsa, Telegramga fayl `sendDocument` orqali yuboriladi
- xabar tagida inline tugmalar chiqadi:
- `Tushuntirildi`
- `Qoniqtirildi`
- `Rad etildi`
- tugma bosilganda Telegram webhook orqali murojaat statusi yangilanadi

Webhook endpoint:

- `POST /api/telegram/webhook/`

## Endpointlar

### `POST /api/murojaatlar/`

Yangi murojaat yaratadi.

Form-data maydonlari:

- `phone_number`
- `address`
- `content`
- `attachment` (ixtiyoriy)

### `GET /api/murojaatlar/`

Murojaatlar ro'yxati.

Filterlar:

- `status`
- `search`
- `ordering`

### `GET /api/murojaatlar/{id}/`

Bitta murojaat tafsiloti.

### `PATCH /api/murojaatlar/{id}/status/`

Faqat statusni yangilaydi.

JSON:

```json
{
  "status": "tushuntirildi"
}
```

Mumkin qiymatlar:

- `new`
- `tushuntirildi`
- `qoniqtirildi`
- `rad_etildi`

### `GET /api/murojaatlar/statistics/`

Statistika qaytaradi:

- `total`
- `new`
- `tushuntirildi`
- `qoniqtirildi`
- `rad_etildi`
