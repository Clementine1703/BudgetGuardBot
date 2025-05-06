from pydantic import BaseModel, Field


class ExpenseValidator(BaseModel):
    category: str = Field(None, min_length=1, max_length=50, description="Category of the expense")
    amount: int = Field(None, gt=0, lt=2147483647)
    comment: str = Field(None, min_length=1, max_length=500)
