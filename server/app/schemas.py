from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class ChannelEnum(str, Enum):
    online = "Online"
    atm = "ATM"
    branch = "Branch"


class TransactionTypeEnum(str, Enum):
    credit = "Credit"
    debit = "Debit"


class CustomerOccupationEnum(str, Enum):
    doctor = "Doctor"
    student = "Student"
    retired = "Retired"
    engineer = "Engineer"
    other = "Other"


class Transaction(BaseModel):
    TransactionID: str
    AccountID: str
    TransactionAmount: Annotated[float, Field(ge=0, le=1_000_000, description="Amount between 0 and 1,000,000")]
    TransactionDate: str
    TransactionType: TransactionTypeEnum
    Location: str
    DeviceID: str
    IPAddress: str
    MerchantID: str
    Channel: ChannelEnum
    CustomerAge: Annotated[int, Field(ge=18, le=120, description="Valid age range")]
    CustomerOccupation: CustomerOccupationEnum
    TransactionDuration: Annotated[int, Field(ge=0, le=10_000, description="Duration in seconds")]
    LoginAttempts: Annotated[int, Field(ge=0, le=10)]
    AccountBalance: Annotated[float, Field(ge=0, le=10_000_000)]
    PreviousTransactionDate: str
