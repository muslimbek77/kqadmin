# 🧪 Vacancy API - Testing & Verification Guide

## ✅ Quick Verification

Run these commands to verify everything is working:

### 1. Check Django Setup
```bash
cd /home/muslim/projects/kqadmin
python manage.py check
```

Expected output:
```
System check identified no issues (0 silenced).
```

### 2. Check Database
```bash
python manage.py dbshell
sqlite> SELECT COUNT(*) FROM korrupsiya_app_vacancy;
```

Expected output:
```
3
```

### 3. Start Server
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🔍 API Testing

### Basic Tests (cURL)

#### 1. List All Vacancies
```bash
curl http://localhost:8000/api/vacancies/
```

#### 2. Single Vacancy
```bash
curl http://localhost:8000/api/vacancies/1/
```

#### 3. Filter by Company
```bash
curl "http://localhost:8000/api/vacancies/?company=IT%20Park"
```

#### 4. Filter by Status
```bash
curl "http://localhost:8000/api/vacancies/?status=active"
```

#### 5. Search
```bash
curl "http://localhost:8000/api/vacancies/?search=Backend"
```

#### 6. Multiple Filters
```bash
curl "http://localhost:8000/api/vacancies/?company=IT%20Park&type=Full%20Time"
```

---

## 📊 Expected Test Results

### Test 1: List API
**Command:**
```bash
curl -s http://localhost:8000/api/vacancies/ | python -m json.tool
```

**Expected:**
- Status code: 200
- Response has `count`, `next`, `previous`, `results`
- Results array with at least 3 vacancies

### Test 2: Company Filter
**Command:**
```bash
curl -s "http://localhost:8000/api/vacancies/?company=IT%20Park" | python -m json.tool
```

**Expected:**
- Status code: 200
- `count`: 1
- First result has `"company": "IT Park"`

### Test 3: Search
**Command:**
```bash
curl -s "http://localhost:8000/api/vacancies/?search=Backend" | python -m json.tool
```

**Expected:**
- Status code: 200
- Results contain "Backend Developer"

### Test 4: Pagination
**Command:**
```bash
curl -s "http://localhost:8000/api/vacancies/?page=1" | python -m json.tool | head -20
```

**Expected:**
- `"count": 3` (total)
- `"next": null` (only 1 page)
- `"results": [...]` with vacancies

---

## 🎯 Frontend Integration Tests

### React Test Component
```javascript
// Test.jsx
import axios from 'axios';
import { useEffect, useState } from 'react';

export function VacancyTest() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get('http://localhost:8000/api/vacancies/')
      .then(res => {
        console.log('✅ API works!', res.data);
        setData(res.data);
      })
      .catch(err => console.error('❌ API Error:', err));
  }, []);

  return (
    <div>
      <h1>Vacancy Count: {data?.count}</h1>
      {data?.results?.map(v => (
        <div key={v.id}>
          <h2>{v.title}</h2>
          <p>{v.company}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## 🚨 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'django_filters'`

**Solution:**
```bash
pip install django-filter
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Kill the process
lsof -i :8000
kill -9 <PID>

# Or use different port
python manage.py runserver 0.0.0.0:8001
```

### Issue: API returns empty results

**Solution:**
```bash
# Check if vacancies exist
python manage.py shell
>>> from korrupsiya_app.models import Vacancy
>>> Vacancy.objects.all()
>>> Vacancy.objects.count()

# If empty, run:
python manage.py populate_vacancies
```

### Issue: Filter not working

**Solution:**
1. Check settings.py has `'django_filters'` in INSTALLED_APPS
2. Check REST_FRAMEWORK config has `DjangoFilterBackend`
3. Restart server after changes

---

## 📋 Manual Testing Checklist

- [ ] Server starts without errors
- [ ] `GET /api/vacancies/` returns 200
- [ ] Response has pagination info
- [ ] Response has at least 3 vacancies
- [ ] Company filter works
- [ ] Status filter works
- [ ] Search works
- [ ] Detail endpoint works
- [ ] Admin panel accessible
- [ ] Admin can create new vacancy
- [ ] Admin can edit vacancy
- [ ] Admin can delete vacancy

---

## 🔐 Security Tests

### CORS Test
```javascript
// From browser console (different domain)
fetch('http://localhost:8000/api/vacancies/')
  .then(r => r.json())
  .then(d => console.log(d))
```

Expected: ✅ Should work (CORS enabled)

### SQL Injection Test
```bash
# Try injection
curl "http://localhost:8000/api/vacancies/?search=Backend' OR '1'='1"
```

Expected: ✅ Should be safe (ORM uses parameterized queries)

---

## 📈 Performance Tests

### Load Test (10 requests)
```bash
for i in {1..10}; do
  curl -s http://localhost:8000/api/vacancies/ > /dev/null
  echo "Request $i completed"
done
```

### Large Response Test
```bash
# Get full response with measurements
time curl -s http://localhost:8000/api/vacancies/ | wc -c
```

---

## 🎓 API Response Structure

### Successful Response (200)
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "company": "IT Park",
      "title": "Backend Developer",
      ...
    }
  ]
}
```

### Error Response (400)
```json
{
  "detail": "Invalid filter value"
}
```

### Error Response (404)
```json
{
  "detail": "Not found."
}
```

---

## 🔄 Complete Integration Test

```bash
#!/bin/bash

echo "=== Vacancy API Integration Test ==="

# Test 1: List
echo "1. Testing list endpoint..."
curl -s http://localhost:8000/api/vacancies/ | grep -q "count" && echo "✅ List works" || echo "❌ List failed"

# Test 2: Search
echo "2. Testing search..."
curl -s "http://localhost:8000/api/vacancies/?search=Backend" | grep -q "Backend" && echo "✅ Search works" || echo "❌ Search failed"

# Test 3: Filter
echo "3. Testing filter..."
curl -s "http://localhost:8000/api/vacancies/?company=IT%20Park" | grep -q "IT Park" && echo "✅ Filter works" || echo "❌ Filter failed"

# Test 4: Detail
echo "4. Testing detail..."
curl -s http://localhost:8000/api/vacancies/1/ | grep -q "Backend Developer" && echo "✅ Detail works" || echo "❌ Detail failed"

echo "=== All tests completed ==="
```

Save as `test_api.sh` and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📊 Response Time Targets

- List endpoint: < 200ms
- Search: < 300ms
- Filter: < 200ms
- Detail: < 100ms

---

## 🔍 Database Query Optimization

### Current Queries
```bash
# Check active queries
python manage.py shell
>>> from django.db import connection
>>> from django.test.utils import override_settings
>>> # Run your query
>>> print(connection.queries)
```

### Add Indexes (if needed)
```python
# models.py
class Vacancy(models.Model):
    ...
    class Meta:
        indexes = [
            models.Index(fields=['company']),
            models.Index(fields=['status']),
            models.Index(fields=['published_date']),
        ]
```

---

## 📱 Testing Tools

### Postman Collection (JSON)
```json
{
  "info": {
    "name": "Vacancy API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "List All",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/vacancies/"
      }
    },
    {
      "name": "Filter by Company",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/vacancies/?company=IT%20Park"
      }
    }
  ]
}
```

### Thunder Client (VS Code)
```
# Create tests in Thunder Client UI
GET http://localhost:8000/api/vacancies/
GET http://localhost:8000/api/vacancies/?search=Backend
GET http://localhost:8000/api/vacancies/1/
```

---

## ✅ Final Verification

Run this command to verify everything:
```bash
python manage.py shell
```

Then in Python:
```python
from korrupsiya_app.models import Vacancy
from korrupsiya_app.serializers import VacancySerializer

# Test 1: Check model
vacancies = Vacancy.objects.all()
print(f"Total vacancies: {vacancies.count()}")

# Test 2: Check serializer
vacancy = vacancies.first()
serializer = VacancySerializer(vacancy)
print(f"Serialized: {serializer.data}")

# Test 3: Check fields
print(f"Has responsibilities: {'responsibilities' in serializer.data}")
print(f"Has translations: {'title_translations' in serializer.data}")
```

Expected output:
```
Total vacancies: 3
Serialized: {...full vacancy object...}
Has responsibilities: True
Has translations: True
```

---

## 🎉 Success Indicators

✅ All endpoints respond with 200 status  
✅ Filtering works correctly  
✅ Search returns expected results  
✅ Pagination works  
✅ JSON structure is valid  
✅ Admin panel shows vacancies  
✅ Frontend can integrate  

**Congratulations! Your API is ready for production!** 🚀
