# Backend Developer Challenge

This project implements a simple REST API to manage user transactions using FastAPI, SQLite, and Docker Compose.

## Features

- **POST /transactions/**  
  Create a new transaction.  
  **Validations:**  
  - `amount` must be a positive number.  
  - `currency` must be one of the following: USD, MXN, EUR.

- **GET /transactions/**  
  Retrieve all transactions.

- **DELETE /transactions/{transaction_id}**  
  Delete the transaction specified by `transaction_id`.

## Project Structure

 * DockerFile
 * main.py
 * requirements.txt
 * docker-compose.yml
 * README.md

## Prerequisites

- Docker and Docker Compose must be installed on your system.
## How to Run the Project

1. Clone this repository or extract the compressed file.
2. Navigate to the project directory.
3. Build and start the containers with:

docker-compose up --build

4. The API will be accessible at `http://localhost:8000/`.

## Example Usage

### Create a Transaction

Send a POST request to `http://localhost:8000/transactions/` with the following JSON:

```json
{
 "amount": 100,
 "currency": "USD"
}
```

###  Retrieve All Transactions

Send a GET request to `http://localhost:8000/transactions/`.

Expected Response (HTTP 200):

```json

[
    {
        "id": 1,
        "amount": 100,
        "currency": "USD"
    }
]
```

###  Delete a Transaction

Send a DELETE request to /transactions/{transaction_id}. For example, to delete the transaction with ID 1:

`http://localhost:8000/transactions/1`
```json
{
    "message": "Transaction deleted"
}
 ```

#### Error Response
```
{
    "detail": "Transaction not found"
}
```
