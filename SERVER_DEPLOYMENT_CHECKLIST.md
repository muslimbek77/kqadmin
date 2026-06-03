# Server Deployment Checklist - Django + Gunicorn + Nginx

## 🔧 Serverda Bajarilishi Kerak Bo'lgan Qadamlar

### 1. **Static Files Collect Qilish** ⚠️ MUHIM
```bash
cd /home/muslim/projects/kqadmin
python manage.py collectstatic --noinput
```
**Sababi:** CSS, JS, admin paneli statik fayllar `staticfiles/` papkaga yig'ilishi kerak

### 2. **Database Migratsiyasini Tekshirish**
```bash
# Migratsiyalar qo'llanilganligini tekshirish
python manage.py migrate --dry-run

# Haqiqiy migratsiya
python manage.py migrate
```

### 3. **Gunicorn Restartni To'g'ri Qilish**
```bash
# Gunicorn process-ini topish
ps aux | grep gunicorn

# Eski process-ni to'xtatish va yangi start qilish
sudo systemctl restart gunicorn
# YOKI
pkill -f gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

### 4. **Nginx Konfiguratsiyasini Tekshirish**
```bash
# Nginx config syntaksisni tekshirish
sudo nginx -t

# Nginx restart
sudo systemctl restart nginx

# Nginx logs ni ko'rish
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### 5. **Permissions Tekshirish**
```bash
# Papkalar uchun ruhsatlar
sudo chown -R www-data:www-data /home/muslim/projects/kqadmin
sudo chmod -R 755 /home/muslim/projects/kqadmin
sudo chmod -R 755 /home/muslim/projects/kqadmin/staticfiles
sudo chmod -R 755 /home/muslim/projects/kqadmin/media

# SQLite db faylining ruhsatini tekshirish
sudo chmod 666 /home/muslim/projects/kqadmin/db.sqlite3
```

### 6. **Virtual Environment Faollashtirish**
```bash
# Agar virtual env ishlatayotgan bo'lsa
source /path/to/venv/bin/activate

# Keyin barcha buyruqlarni run qilish
python manage.py ...
```

### 7. **Requirements Tekshirish**
```bash
pip install -r requirements.txt
```

### 8. **Settings.py Deployment Uchun**
Quyidagilar to'g'ri set qilinganligini tekshirish:
- ✅ `DEBUG = False`
- ✅ `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']` (ALLOWED_HOSTS = ['*'] production uchun xavfli)
- ✅ SECRET_KEY xavfsiz va secret
- ✅ STATIC_ROOT va STATIC_URL to'g'ri
- ✅ MEDIA_ROOT va MEDIA_URL konfiguratsiyalangan

## 📋 Tez Ko'rikdan O'tish Uchun Script

```bash
#!/bin/bash
cd /home/muslim/projects/kqadmin

echo "1️⃣  Migrations check..."
python manage.py migrate

echo "2️⃣  Collecting static files..."
python manage.py collectstatic --noinput

echo "3️⃣  Checking permissions..."
sudo chown -R www-data:www-data .
sudo chmod -R 755 .
sudo chmod 666 db.sqlite3

echo "4️⃣  Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "5️⃣  Restarting Nginx..."
sudo systemctl restart nginx

echo "✅ Done!"
```

## 🔍 Problemalarni Debugging

### Static files ko'rinayotmasligi:
```bash
python manage.py findstatic admin/css/base.css -v2
ls -la /home/muslim/projects/kqadmin/staticfiles/
```

### Gunicorn problemasi:
```bash
# Logs ko'rish
sudo journalctl -u gunicorn -n 50 -f
```

### Database lock:
```bash
# SQLite db lock problemasi
rm db.sqlite3-journal
python manage.py migrate
```

---

**Server URL:** http://yourdomain.com/
**Admin:** http://yourdomain.com/admin
**API:** http://yourdomain.com/api/vacancies/
