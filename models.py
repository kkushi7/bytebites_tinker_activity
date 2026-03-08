# Created four classes focused on customer, food item, price, and category of food
from decimal import Decimal, InvalidOperation


MAX_POPULARITY_RATING = 5.0


class Customer:
    def __init__(self, name: str, purchase_history: list["FoodItem"] | None = None) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Customer name cannot be empty.")

        if purchase_history is None:
            purchase_history = []

        self.name = cleaned_name
        self.purchase_history = list(purchase_history)

    def add_purchase(self, item: "FoodItem") -> None:
        if not isinstance(item, FoodItem):
            raise TypeError("item must be a FoodItem instance.")
        self.purchase_history.append(item)

    def get_purchase_history(self) -> list["FoodItem"]:
        return list(self.purchase_history)

    def is_real_user(self) -> bool:
        return len(self.purchase_history) >= 1


class Price:
    def __init__(self, amount: Decimal | str | int | float, currency: str = "USD") -> None:
        try:
            decimal_amount = Decimal(str(amount))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("amount must be a valid number.") from exc

        if decimal_amount < Decimal("0"):
            raise ValueError("amount cannot be negative.")

        cleaned_currency = currency.strip().upper()
        if not cleaned_currency:
            raise ValueError("currency cannot be empty.")

        self.amount = decimal_amount
        self.currency = cleaned_currency

    def get_amount(self) -> Decimal:
        return self.amount

    def format(self) -> str:
        return f"{self.currency} {self.amount.quantize(Decimal('0.01'))}"


class FoodItem:
    def __init__(
        self,
        name: str,
        price: Price,
        category: "Category",
        popularity_rating: float = 0.0,
    ) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Food item name cannot be empty.")
        if not isinstance(price, Price):
            raise TypeError("price must be a Price instance.")
        if not isinstance(category, Category):
            raise TypeError("category must be a Category instance.")
        if not (0.0 <= popularity_rating <= MAX_POPULARITY_RATING):
            raise ValueError(
                f"popularity_rating must be between 0.0 and {MAX_POPULARITY_RATING}."
            )

        self.name = cleaned_name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> Price:
        return self.price

    def get_category(self) -> "Category":
        return self.category

    def update_popularity(self, new_rating: float) -> None:
        if not (0.0 <= new_rating <= MAX_POPULARITY_RATING):
            raise ValueError(
                f"new_rating must be between 0.0 and {MAX_POPULARITY_RATING}."
            )
        self.popularity_rating = new_rating


class Category:
    def __init__(self, name: str) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Category name cannot be empty.")
        self.name = cleaned_name

    def get_name(self) -> str:
        return self.name

    def matches(self, filter_value: str) -> bool:
        return self.name.casefold() == filter_value.strip().casefold()
