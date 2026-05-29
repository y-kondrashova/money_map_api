# API Endpoints

## Authentication

| Method      | Endpoint                   | Description                                                                                           | Auth Required |
|-------------|----------------------------|-------------------------------------------------------------------------------------------------------|---------------|
| POST        | `/api/auth/register/`      | Register new user                                                                                     | No            |
| POST        | `/api-auth/login`          | Login user                                                                                            |               |
| POST        | `/api/auth/token/`         | Get JWT tokens                                                                                        | No            |
| POST        | `/api/auth/token/refresh/` | Refresh access token                                                                                  | No            |
| GET         | `/api/auth/profile`        | Get user's profile                                                                                    | Yes           |
| PUT / PATCH | `/api/auth/profile`        | Update user's profile. `PUT` replaces all editable fields, <br/>`PATCH` updates only provided fields. | Yes           |


## Categories

| Method      | Endpoint                | Description                                                                                     | Auth Required |
|-------------|-------------------------|-------------------------------------------------------------------------------------------------|---------------|
| GET         | `/api/categories/`      | List categories                                                                                 | Yes           |
| POST        | `/api/categories/`      | Create category                                                                                 | Yes           |
| GET         | `/api/categories/{id}/` | Retrieve category                                                                               | Yes           |
| PUT / PATCH | `/api/categories/{id}/` | Update category. `PUT` replaces all editable fields, <br/>`PATCH` updates only provided fields. | Yes           |
| DELETE      | `/api/categories/{id}/` | Delete category                                                                                 | Yes           |

## Budgets

| Method      | Endpoint             | Description                                                                                   | Auth Required |
|-------------|----------------------|-----------------------------------------------------------------------------------------------|---------------|
| GET         | `/api/budgets/`      | List budgets                                                                                  | Yes           |
| POST        | `/api/budgets/`      | Create budget                                                                                 | Yes           |
| GET         | `/api/budgets/{id}/` | Retrieve budget                                                                               | Yes           |
| PUT / PATCH | `/api/budgets/{id}/` | Update budget. `PUT` replaces all editable fields, <br/>`PATCH` updates only provided fields. | Yes           |
| DELETE      | `/api/budgets/{id}/` | Delete budget                                                                                 | Yes           |



## Wallets

| Method      | Endpoint                     | Description                                                                                   | Auth Required |
|-------------|------------------------------|-----------------------------------------------------------------------------------------------|---------------|
| GET         | `/api/wallets/`              | List user wallets                                                                             | Yes           |
| POST        | `/api/wallets/`              | Create wallet                                                                                 | Yes           |
| GET         | `/api/wallets/{id}/`         | Retrieve wallet                                                                               | Yes           |
| PUT / PATCH | `/api/wallets/{id}/`         | Update wallet. `PUT` replaces all editable fields, <br/>`PATCH` updates only provided fields. | Yes           |
| DELETE      | `/api/wallets/{id}/`         | Soft delete wallet                                                                            | Yes           |
| POST        | `/api/wallets/{id}/restore/` | Restore deleted wallet                                                                        | Yes           |
| GET         | `/api/wallets/deleted/`      | Get deleted wallets                                                                           | Yes           |

## Transactions

| Method      | Endpoint                  | Description                                                                                        | Auth Required |
|-------------|---------------------------|----------------------------------------------------------------------------------------------------|---------------|
| GET         | `/api/transactions/`      | List transactions                                                                                  | Yes           |
| POST        | `/api/transactions/`      | Create transaction                                                                                 | Yes           |
| GET         | `/api/transactions/{id}/` | Retrieve transaction                                                                               | Yes           |
| PUT / PATCH | `/api/transactions/{id}/` | Update transaction. `PUT` replaces all editable fields, <br/>`PATCH` updates only provided fields. | Yes           |
| DELETE      | `/api/transactions/{id}/` | Delete transaction                                                                                 | Yes           |