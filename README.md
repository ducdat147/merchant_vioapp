# Merchant VioApp

Backend API cho ứng dụng quản lý merchant, sản phẩm và dịch vụ.

## Yêu cầu hệ thống

- Docker và Docker Compose
- hoặc:
  - Python 3.12+
  - PostgreSQL 15+
  - Memcached 1.6+

## Công nghệ sử dụng

- Django 5.1.3
- Django REST Framework 3.15.2
- PostgreSQL 15
- Memcached 1.6
- Docker & Docker Compose
- Simple JWT Authentication
- Swagger/OpenAPI Documentation
- pytest và Coverage.py cho testing

## Cài đặt và Chạy với Docker

1. Clone repository:

```bash
git clone https://github.com/ducdat147/merchant_vioapp.git
cd merchant-app
```

2. Tạo file .env từ .env.example:

```bash
cp .env.example .env
```

3. Build và chạy containers:

```bash
docker compose up --build
```

Ứng dụng sẽ chạy tại http://localhost:8000/

### Các lệnh Docker hữu ích

```bash
# Khởi động services
docker compose up -d
```

```bash
# Dừng services
docker compose down
```

```bash
# Xem logs
docker compose logs -f
```

```bash
# Chạy migrations
docker compose exec web python manage.py migrate
```

```bash
# Tạo superuser
docker compose exec web python manage.py createsuperuser
```

```bash
# Truy cập Django shell
docker compose exec web python manage.py shell
```

```bash
# Collect static files
docker compose exec web python manage.py collectstatic
```

```bash
# Restart services
docker compose restart
```

## Cài đặt môi trường phát triển (không dùng Docker)

1. Tạo môi trường ảo:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/MacOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Cài đặt các dependencies:

```bash
pip install -r requirements.txt
```

3. Tạo file .env trong thư mục gốc:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@localhost:5432/merchant_db
MEMCACHED_LOCATION=127.0.0.1:11211
```

4. Chạy migrations:

```bash
python manage.py migrate
```

## API Documentation

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Testing

1. Chạy toàn bộ test suite:

```bash
pytest
```

2. Chạy test với coverage report:

```bash
coverage run -m pytest
coverage report
```

3. Tạo HTML coverage report:

```bash
coverage html
```

Report sẽ được tạo trong thư mục htmlcov/

## Cấu trúc Project

```
merchant-app/
├── core/                   # Core application modules
│   ├── accounts/          # User authentication & management
│   ├── merchants/         # Merchant management
│   └── products/          # Products & services management
├── merchant_app/          # Project configuration
├── scripts/               # Utility scripts
├── docker compose.yml     # Docker compose configuration
├── Dockerfile            # Docker build configuration
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

Dat Truong - ducdat147@gmail.com

Project Link: https://github.com/ducdat147/merchant_vioapp