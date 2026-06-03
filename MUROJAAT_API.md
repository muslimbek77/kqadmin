# Murojaatlar API

Swagger hujjati:

- `/api/swagger/`
- `/api/schema/`

## Telegram sozlamalari

Environment o'zgaruvchilari:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DEFAULT_CHAT_ID`

Agar `assigned_telegram_chat_id` yuborilsa, shu chat ID ishlatiladi. Aks holda `TELEGRAM_DEFAULT_CHAT_ID` ishlatiladi.

## Endpointlar

### `POST /api/murojaatlar/`

Yangi murojaat yaratadi.

Form-data maydonlari:

- `phone_number`
- `address`
- `content`
- `attachment` (ixtiyoriy)
- `assigned_telegram_chat_id` (ixtiyoriy)

### `GET /api/murojaatlar/`

Murojaatlar ro'yxati.

Filterlar:

- `status`
- `assigned_telegram_chat_id`
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
- `telegram_sent`
- `telegram_failed`
