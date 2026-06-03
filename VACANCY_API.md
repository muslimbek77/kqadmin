# Vacancy API Dokumentatsiya

## API Endpoints

### 1. Barcha Vacancylarni Olish (GET)
```
GET /api/vacancies/
```

**Javob:**
```json
[
  {
    "id": 1,
    "company": "IT Park",
    "title": "Backend Developer",
    "type": "Full Time",
    "work_hours": "09:00 - 18:00",
    "location": "Tashkent",
    "salary": "10,000,000 - 15,000,000 UZS",
    "experience": "2-3 yil",
    "education": "Bachelor",
    "published_date": "2026-06-03",
    "deadline": "2026-07-03",
    "status": "active",
    "responsibilities": [
      "RESTful API yozish",
      "Database design",
      "Kod review qilish",
      "Team bilan hamkorlik"
    ],
    "requirements": [
      "Python 3.9+",
      "Django / DRF",
      "PostgreSQL",
      "Git"
    ],
    "languages": ["Uzbek", "English", "Russian"],
    "conditions": [
      "Health insurance",
      "Professional development",
      "Remote work available",
      "Competitive salary"
    ],
    "positions": 1,
    "extra": {},
    "title_translations": {
      "uz": "Backend Dasturchi",
      "ru": "Backend разработчик",
      "en": "Backend Developer"
    },
    "description_translations": {},
    "created_at": "2026-06-03T10:30:00Z",
    "updated_at": "2026-06-03T10:30:00Z"
  },
  ...
]
```

### 2. Bitta Vacancy Tafsiloti (GET)
```
GET /api/vacancies/{id}/
```

**Misol:**
```
GET /api/vacancies/1/
```

**Javob:**
```json
{
  "id": 1,
  "company": "IT Park",
  "title": "Backend Developer",
  ...
}
```

---

## Frontend Integratsiyasi

### React Misol (i18next bilan)

```javascript
import axios from 'axios';
import { useTranslation } from 'react-i18next';

function VacancyList() {
  const { i18n } = useTranslation();
  const [vacancies, setVacancies] = useState([]);

  useEffect(() => {
    axios.get('/api/vacancies/')
      .then(res => setVacancies(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      {vacancies.map(vacancy => (
        <div key={vacancy.id}>
          {/* Agar title_translations bor bo'lsa */}
          <h2>{vacancy.title_translations[i18n.language] || vacancy.title}</h2>
          
          <p>Kompaniya: {vacancy.company}</p>
          <p>Turi: {vacancy.type}</p>
          <p>Maosh: {vacancy.salary}</p>
          
          <h3>Mas'uliyatlar:</h3>
          <ul>
            {vacancy.responsibilities.map((resp, i) => (
              <li key={i}>{resp}</li>
            ))}
          </ul>
          
          <h3>Talablar:</h3>
          <ul>
            {vacancy.requirements.map((req, i) => (
              <li key={i}>{req}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

---

## Moslashtirilgan So'rovlar

### Filtrlanish (kelajakda qo'shish mumkin)

```python
# views.py ga filter qo'shish:
from django_filters import rest_framework as filters

class VacancyFilter(filters.FilterSet):
    class Meta:
        model = Vacancy
        fields = ['company', 'type', 'status']

class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filterset_class = VacancyFilter
```

**Foydalanish:**
```
GET /api/vacancies/?company=IT%20Park&status=active
```

---

## Model Tuzilishi

### Moslashtirilgan Maydonlar

1. **JSONField (Massivlar)**
   - `responsibilities` — Mas'uliyatlar ro'yxati
   - `requirements` — Talablar ro'yxati
   - `languages` — Tillar
   - `conditions` — Ish shartlari
   - `positions` — Bo'sh o'rinlar soni

2. **Ko'p til Qo'llash**
   - `title_translations` — Sarlavha tarjimalari
   - `description_translations` — Tavsif tarjimalari

3. **Qo'shimcha Maydon**
   - `extra` — Boshqa ma'lumotlar uchun

---

## Texnik Tavsiflar

### Ish Shartlari
- **type** — Ish turi (Full Time, Part Time, Contract, Freelance)
- **work_hours** — Ish vaqti
- **location** — Joylashuv
- **status** — Holati (active, closed, draft)

### Tarjimalar
Backend tarjimalari saqlaydi, shuning uchun frontend tili ko'rsatgichiga qarab to'g'ri tilni oladi:

```javascript
const title = vacancy.title_translations[i18n.language] || vacancy.title;
```

---

## Keyingi Bosqichlar

1. **Pagination qo'shish** — Katta saylarni paginate qilish
2. **Search qo'shish** — Title, company bo'yicha izlash
3. **Filtrlanish** — Type, status, location bo'yicha filtrlash
4. **Sorting** — Sana bo'yicha saralash
5. **Authentication** — Agar faqat authenticated foydalanuvchilar qo'sh bo'lsa

---

## Foydalanish

Sample ma'lumotni qo'shish:
```bash
python manage.py populate_vacancies
```
