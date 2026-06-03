# Vacancy API - Frontend Integration Examples

## 1️⃣ List API - Filtrlash, Qidiruv, Saralash

### A) Barcha Vacancylarni Olish

```bash
GET /api/vacancies/
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [...]
}
```

---

### B) Filtrlanish

#### Company bo'yicha

```bash
GET /api/vacancies/?company=IT%20Park
```

#### Status bo'yicha

```bash
GET /api/vacancies/?status=active
```

#### Turi bo'yicha

```bash
GET /api/vacancies/?type=Full%20Time
```

#### Joylashuvi bo'yicha

```bash
GET /api/vacancies/?location=Tashkent
```

#### Ko'p filter qo'llash

```bash
GET /api/vacancies/?company=IT%20Park&type=Full%20Time&status=active
```

---

### C) Qidiruv

#### Sarlavha bo'yicha

```bash
GET /api/vacancies/?search=Backend
```

#### Company bo'yicha

```bash
GET /api/vacancies/?search=IT%20Park
```

#### Mas'uliyatlardan qidiruv

```bash
GET /api/vacancies/?search=API
```

---

### D) Saralash

#### Yangi yuborilganlar birinchi

```bash
GET /api/vacancies/?ordering=-published_date
```

#### Eski yuborilganlar birinchi

```bash
GET /api/vacancies/?ordering=published_date
```

#### Deadline bo'yicha (tezroq yopiladi birinchi)

```bash
GET /api/vacancies/?ordering=deadline
```

---

### E) Kombinatsiya (Filter + Search + Order)

```bash
GET /api/vacancies/?company=IT%20Park&search=Backend&ordering=-published_date&status=active
```

---

## 2️⃣ Frontend Examples

### React + Axios

```javascript
import axios from 'axios';
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

function VacancyList() {
  const { i18n } = useTranslation();
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    company: '',
    type: '',
    status: 'active',
    search: ''
  });

  useEffect(() => {
    fetchVacancies();
  }, [filters]);

  const fetchVacancies = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.company) params.append('company', filters.company);
      if (filters.type) params.append('type', filters.type);
      if (filters.status) params.append('status', filters.status);
      if (filters.search) params.append('search', filters.search);
      params.append('ordering', '-published_date');

      const response = await axios.get(`/api/vacancies/?${params}`);
      setVacancies(response.data.results);
    } catch (error) {
      console.error('API xatosi:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      {/* Filtrlar */}
      <div className="filters">
        <input
          type="text"
          name="search"
          placeholder="Qidiruv..."
          value={filters.search}
          onChange={handleFilterChange}
        />
        
        <select name="company" value={filters.company} onChange={handleFilterChange}>
          <option value="">Barcha Kompaniyalar</option>
          <option value="IT Park">IT Park</option>
          <option value="Univer Tech">Univer Tech</option>
          <option value="DataWay">DataWay</option>
        </select>

        <select name="type" value={filters.type} onChange={handleFilterChange}>
          <option value="">Ish Turi</option>
          <option value="Full Time">Full Time</option>
          <option value="Part Time">Part Time</option>
        </select>
      </div>

      {/* Vacancylar */}
      {loading ? (
        <p>Yuklanyapti...</p>
      ) : (
        vacancies.map(vacancy => (
          <div key={vacancy.id} className="vacancy-card">
            <h2>{vacancy.title_translations[i18n.language] || vacancy.title}</h2>
            <p><strong>Kompaniya:</strong> {vacancy.company}</p>
            <p><strong>Maosh:</strong> {vacancy.salary}</p>
            <p><strong>Joylashuv:</strong> {vacancy.location}</p>
            <p><strong>Tazhribasi:</strong> {vacancy.experience}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default VacancyList;
```

---

### Vue 3 + Fetch API

```vue
<template>
  <div class="vacancy-container">
    <!-- Filtrlar -->
    <div class="filter-section">
      <input
        v-model="filters.search"
        type="text"
        placeholder="Qidiruv..."
        @input="fetchVacancies"
      />
      
      <select v-model="filters.company" @change="fetchVacancies">
        <option value="">Barcha Kompaniyalar</option>
        <option value="IT Park">IT Park</option>
        <option value="Univer Tech">Univer Tech</option>
      </select>
    </div>

    <!-- Vacancylar -->
    <div v-if="loading" class="loading">Yuklanyapti...</div>
    <div v-else class="vacancies">
      <div v-for="vacancy in vacancies" :key="vacancy.id" class="vacancy-card">
        <h2>{{ vacancy.title_translations[$i18n.locale] || vacancy.title }}</h2>
        <p><strong>Kompaniya:</strong> {{ vacancy.company }}</p>
        <p><strong>Maosh:</strong> {{ vacancy.salary }}</p>
        <p><strong>Talablar:</strong></p>
        <ul>
          <li v-for="req in vacancy.requirements" :key="req">{{ req }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();
const vacancies = ref([]);
const loading = ref(false);
const filters = ref({
  search: '',
  company: '',
  status: 'active'
});

const fetchVacancies = async () => {
  loading.value = true;
  try {
    const params = new URLSearchParams({
      ...Object.fromEntries(
        Object.entries(filters.value).filter(([_, v]) => v)
      ),
      ordering: '-published_date'
    });

    const response = await fetch(`/api/vacancies/?${params}`);
    const data = await response.json();
    vacancies.value = data.results;
  } catch (error) {
    console.error('Xato:', error);
  } finally {
    loading.value = false;
  }
};

watch(filters, fetchVacancies, { deep: true });
fetchVacancies();
</script>
```

---

### Vanilla JavaScript + Fetch

```javascript
// API so'rovini yaratish
async function getVacancies(options = {}) {
  const params = new URLSearchParams();
  
  if (options.search) params.append('search', options.search);
  if (options.company) params.append('company', options.company);
  if (options.status) params.append('status', options.status);
  params.append('ordering', '-published_date');

  try {
    const response = await fetch(`/api/vacancies/?${params}`);
    if (!response.ok) throw new Error('API xatosi');
    return await response.json();
  } catch (error) {
    console.error(error);
  }
}

// Foydalanish
getVacancies({ search: 'Backend', status: 'active' }).then(data => {
  console.log(data.results);
  // Frontend ni yangilash
});
```

---

### cURL Misollar

#### Oddiy so'rov

```bash
curl http://localhost:8000/api/vacancies/
```

#### Filtrlanish

```bash
curl "http://localhost:8000/api/vacancies/?company=IT%20Park&status=active"
```

#### Qidiruv

```bash
curl "http://localhost:8000/api/vacancies/?search=Backend&ordering=-published_date"
```

---

## 3️⃣ Detali API

```bash
GET /api/vacancies/1/
```

**Response:**
```json
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
  "title_translations": {
    "uz": "Backend Dasturchi",
    "ru": "Backend разработчик",
    "en": "Backend Developer"
  },
  "created_at": "2026-06-03T07:39:52.320018Z",
  "updated_at": "2026-06-03T07:39:52.320057Z"
}
```

---

## 4️⃣ Pagination

API avtomatik ravishda 20 ta natija bo'yicha paginate qiladi.

```bash
GET /api/vacancies/?page=1
GET /api/vacancies/?page=2
```

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/vacancies/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 5️⃣ Error Handling

```javascript
async function getVacanciesWithErrorHandling(options = {}) {
  try {
    const params = new URLSearchParams(options);
    const response = await fetch(`/api/vacancies/?${params}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Vacancies topilmadi');
      } else if (response.status === 500) {
        throw new Error('Server xatosi. Keyinroq urinib ko\'ring');
      }
    }
    
    return await response.json();
  } catch (error) {
    console.error('Xato:', error.message);
    return null;
  }
}
```

---

## 6️⃣ Advanced Filter Tips

### Multiple values uchun filter (kelajakda qo'shish)

```python
# models.py
from django_filters import rest_framework as filters

class VacancyFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='type', lookup_expr='icontains')
    salary_min = filters.NumberFilter(field_name='salary', lookup_expr='gte')
    
    class Meta:
        model = Vacancy
        fields = ['company', 'status', 'type']

# views.py
class VacancyListAPIView(generics.ListAPIView):
    ...
    filterset_class = VacancyFilter
```

```bash
GET /api/vacancies/?salary_min=5000000
```

---

## 7️⃣ API Testing Tools

- **Postman** — Professional API testing
- **Insomnia** — REST Client
- **VS Code REST Client** — Inline testing
- **cURL** — Command line
- **Thunder Client** — VS Code extension

---

## 8️⃣ Production Tips

1. **Kešlash** — Cache eng ko'p request qilingan ma'lumotlarni
2. **Rate limiting** — API abuse ni oldini olish
3. **Pagination** — Katta dataset lar uchun
4. **Compression** — Gzip compression yoqish
5. **HTTPS** — Production da faqat HTTPS
6. **CORS** — Frontend domen ni qo'sh qo'yish

---

## Sample Requests (Postman)

```
# GET all vacancies
GET http://localhost:8000/api/vacancies/

# GET with filters
GET http://localhost:8000/api/vacancies/?company=IT%20Park&status=active

# GET single vacancy
GET http://localhost:8000/api/vacancies/1/

# Search
GET http://localhost:8000/api/vacancies/?search=Backend
```
