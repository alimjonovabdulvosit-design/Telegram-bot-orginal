# Python rasmiy obrazidan foydalanamiz
FROM python:3.10-slim

# Ishchi papkani yaratamiz
WORKDIR /app

# Atrof-muhit o'zgaruvchilarini o'rnatamiz
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Talablar faylini ko'chirib o'tamiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chirib o'tamiz
COPY . .

# Ma'lumotlar saqlanishi uchun papka yaratamiz
RUN mkdir -p /app/data

# Botni ishga tushiramiz
CMD ["python", "main.py"]
