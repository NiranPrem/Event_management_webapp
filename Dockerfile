# ---- Base Image ----
FROM python:3.12-slim

# ---- Working Directory ----
WORKDIR /app

# ---- Copy Project Files ----
COPY . /app

# ---- Install Dependencies ----
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---- Run Migrations & Collect Static ----
# NOTE: Using 'sh -c' so all commands run together properly
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput

# ---- Expose Port ----
EXPOSE 8000

# ---- Start Django Server (with runtime patch for /account → /accounts) ----
CMD ["sh", "-c", "\
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
sed -i 's|account/|accounts/|g' eventmanagementwebapp/urls.py || true && \
python manage.py runserver 0.0.0.0:8000"]
