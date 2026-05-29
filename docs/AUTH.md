# Authentication

MoneyMap uses JWT authentication.

## Get Token

POST `/api/auth/token/`

Request:

```json
{
  "email": "demo@example.com",
  "password": "DemoPassword123!"
}
```

Response:

```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

Use access token:

```text
Authorization: Bearer your_access_token
```