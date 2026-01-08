# ⚡ FixWatt – Electronics Store

![FixWatt Banner](docs/screenshots/home.png?v=2)

**FixWatt** is a modern online electronics and lighting store developed with Django. The project includes a powerful product catalog, logistics automation (Nova Poshta), an API for integrations, and a convenient admin panel.

---

## 🚀 Key Features

### 📦 Logistics & Nova Poshta
*   **Waybill Creation (TTN)**: Integration with the Nova Poshta API allows you to create express waybills (TTN) **directly from the admin panel**.
*   **Automation**: Sender details and cargo parameters are populated automatically.
*   **Client Database**: The `get_or_create_counterparty` function checks if a client exists in the Nova Poshta database and creates them if necessary.

### 📊 Product Import & Export
*   **Excel (.xlsx)**: Bulk upload and update of products via Excel files.
*   **SKU Support**: Product synchronization is based on the unique `sku` field. If a product is found, it updates; if not, a new one is created.
*   **Cyrillic URLs**: Full support for Ukrainian language in product URLs (`/product/світлодіодна-лампа-luxel/`) using custom slug handling.

### ⚡ Optimization & API
*   **Smart Image Resizing**: All uploaded photos are automatically compressed and resized to **800x600**, saving disk space and speeding up the site.
*   **REST API**: A full-fledged API for mobile apps and external systems.
    *   Documentation available at: `/swagger/` or `/redoc/`.
    *   Endpoints for retrieving products, categories, and creating orders.

### 🛒 User Experience (UX)
*   **Smart Cart**: Add products to the cart without page reloads (AJAX) featuring a confirmation modal.
*   **Dynamic Counters**: Instant update of the product count in the site header.
*   **Gallery**: Convenient image slider (Carousel) for viewing product photos.
*   **Global Banners**: A system of informational messages in the site header, managed via the admin panel.

---

## 🛠 Technologies

*   **Backend**: Python 3.9+, Django 4.2
*   **Database**: PostgreSQL
*   **API**: Django REST Framework, Drf-YASG (Swagger)
*   **Integration**: Nova Poshta API, Requests, OpenPyXL
*   **Frontend**: Bootstrap 5, jQuery, AJAX
*   **Image Processing**: Pillow

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kazna4eev/fixwatt.git
cd FixWatt
```

### 2. Environment Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables (.env)

Create a `.env` file in the project root (next to `manage.py`):

```ini
DEBUG=True
SECRET_KEY=your_secret_key_here

# Database Settings (PostgreSQL)
DB_NAME=fixwatt_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Nova Poshta API
NOVA_POSHTA_API_KEY=your_key
SENDER_CITY_REF=ref_city_sender
SENDER_REF=ref_sender
CONTACT_SENDER_REF=ref_contact_sender
SENDER_ADDRESS_REF=ref_warehouse_sender
SENDER_PHONE=380XXXXXXXXX
```

### 4. Database Preparation

Ensure PostgreSQL is running and the `fixwatt_db` database is created.

```bash
python manage.py migrate
python manage.py createsuperuser # Create admin user
```

### 5. Running the Server

```bash
python manage.py runserver
```

Open your browser: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---
© 2025 FixWatt Team
