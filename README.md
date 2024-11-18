# Merchant VioApp

Backend API cho ứng dụng quản lý merchant, sản phẩm và dịch vụ.

## Yêu cầu hệ thống

- Python 3.12+
- Django 5.1.3

## Công nghệ sử dụng

- Django REST Framework 3.15.2
- Simple JWT Authentication
- Swagger/OpenAPI Documentation
- pytest và Coverage.py cho testing

## Cài đặt môi trường phát triển

1. Tạo môi trường ảo:

##### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

##### Linux/MacOS

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
```

4. Chạy migrations:

```bash
python manage.py migrate
```

## Chạy development server

```bash
python manage.py runserver
```

Server sẽ chạy tại http://localhost:8000/

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

## Cấu trúc project

```
merchant_vioapp/
├── core/
│   ├── accounts/         # User authentication và authorization
│   ├── merchants/        # Merchant management
│   ├── products/         # Products, services và promotions
│   └── tests/           # Test suites
├── merchant_app/         # Project settings
└── requirements.txt      # Project dependencies
```

## API Endpoints

### Authentication
- POST /api/auth/register/ - Đăng ký user mới
- POST /api/auth/login/ - Đăng nhập và lấy token
- POST /api/auth/token/refresh/ - Refresh token

### Merchants
- POST /api/merchants/create/ - Tạo merchant mới
- GET /api/merchants/{id}/ - Lấy thông tin merchant
- PUT /api/merchants/{id}/ - Cập nhật thông tin merchant
- DELETE /api/merchants/{id}/ - Xóa merchant

### Products
- GET /api/products/ - Danh sách sản phẩm
- POST /api/products/ - Tạo sản phẩm mới
- GET /api/products/{id}/ - Chi tiết sản phẩm
- PUT /api/products/{id}/ - Cập nhật sản phẩm
- DELETE /api/products/{id}/ - Xóa sản phẩm

### Services
- GET /api/services/ - Danh sách dịch vụ
- POST /api/services/ - Tạo dịch vụ mới
- GET /api/services/{id}/ - Chi tiết dịch vụ
- PUT /api/services/{id}/ - Cập nhật dịch vụ
- DELETE /api/services/{id}/ - Xóa dịch vụ

### Promotions
- GET /api/promotions/ - Danh sách khuyến mãi
- POST /api/promotions/ - Tạo khuyến mãi mới
- GET /api/promotions/{id}/ - Chi tiết khuyến mãi
- PUT /api/promotions/{id}/ - Cập nhật khuyến mãi
- DELETE /api/promotions/{id}/ - Xóa khuyến mãi

## Contributing

1. Fork project
2. Tạo feature branch (git checkout -b feature/AmazingFeature)
3. Commit changes (git commit -m 'Add some AmazingFeature')
4. Push to branch (git push origin feature/AmazingFeature)
5. Tạo Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

Dat Truong - ducdat147@gmail.com

Project Link: https://github.com/ducdat147/merchant_vioapp