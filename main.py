from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Create database directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Database configuration
DATABASE_URL = "sqlite:///./data/transactions.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Valid currencies
VALID_CURRENCIES = ["USD", "MXN", "EUR"]

# Database model
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for validation
class TransactionCreate(BaseModel):
    amount: float
    currency: str

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be a positive number")
        return v

    @validator("currency")
    def currency_must_be_valid(cls, v):
        if v not in VALID_CURRENCIES:
            raise ValueError(f"Currency must be one of {VALID_CURRENCIES}")
        return v

class TransactionResponse(BaseModel):
    id: int
    amount: float
    currency: str

    class Config:
        orm_mode = True

# Create FastAPI application
app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/transactions/", response_model=TransactionResponse, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(amount=transaction.amount, currency=transaction.currency)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

@app.delete("/transactions/{transaction_id}", status_code=200)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted"}
