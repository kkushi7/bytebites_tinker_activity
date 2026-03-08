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


class ItemCatalog:
    def __init__(self, items: list["FoodItem"]) -> None:
        if not all(isinstance(item, FoodItem) for item in items):
            raise TypeError("All items must be FoodItem instances.")
        self.items = list(items)

    def filter_by_category(self, category_name: str) -> list["FoodItem"]:
        return [item for item in self.items if item.get_category().matches(category_name)]

    def filter_by_price_range(
        self, min_amount: Decimal, max_amount: Decimal
    ) -> list["FoodItem"]:
        if min_amount > max_amount:
            raise ValueError("min_amount cannot be greater than max_amount.")
        return [
            item
            for item in self.items
            if min_amount <= item.get_price().get_amount() <= max_amount
        ]

    def search_by_name(self, query: str) -> list["FoodItem"]:
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return list(self.items)
        return [
            item
            for item in self.items
            if normalized_query in item.get_name().casefold()
        ]

    def filter_by_popularity(self, min_rating: float) -> list["FoodItem"]:
        return [item for item in self.items if item.popularity_rating >= min_rating]

    def sort_by_price(self, ascending: bool = True) -> list["FoodItem"]:
        return sorted(
            self.items,
            key=lambda item: item.get_price().get_amount(),
            reverse=not ascending,
        )

    def sort_by_name(self, ascending: bool = True) -> list["FoodItem"]:
        return sorted(
            self.items,
            key=lambda item: item.get_name().casefold(),
            reverse=not ascending,
        )

    def sort_by_popularity(self, ascending: bool = False) -> list["FoodItem"]:
        return sorted(
            self.items,
            key=lambda item: item.popularity_rating,
            reverse=not ascending,
        )


class Transaction:
    def __init__(self, items: list["FoodItem"] | None = None) -> None:
        if items is None:
            items = []
        if not all(isinstance(item, FoodItem) for item in items):
            raise TypeError("All items must be FoodItem instances.")
        self.items = list(items)

    def add_item(self, item: "FoodItem") -> None:
        if not isinstance(item, FoodItem):
            raise TypeError("item must be a FoodItem instance.")
        self.items.append(item)

    def remove_item(self, item: "FoodItem") -> None:
        self.items.remove(item)

    def get_items(self) -> list["FoodItem"]:
        return list(self.items)

    def compute_subtotal(self) -> Decimal:
        return sum((item.get_price().get_amount() for item in self.items), Decimal("0"))

    def compute_tax(self, tax_rate: Decimal) -> Decimal:
        if tax_rate < Decimal("0"):
            raise ValueError("tax_rate cannot be negative.")
        return (self.compute_subtotal() * tax_rate).quantize(Decimal("0.01"))

    def compute_total(self, tax_rate: Decimal = Decimal("0")) -> Decimal:
        return self.compute_subtotal() + self.compute_tax(tax_rate)

    def total_formatted(self, tax_rate: Decimal = Decimal("0")) -> str:
        currency = self.items[0].get_price().currency if self.items else "USD"
        total = self.compute_total(tax_rate).quantize(Decimal("0.01"))
        return f"{currency} {total}"


if __name__ == "__main__":
    drinks = Category("Drinks")
    mains = Category("Mains")
    desserts = Category("Desserts")

    menu_items = [
        FoodItem("Spicy Burger", Price("8.99"), mains, 4.7),
        FoodItem("Large Soda", Price("2.49"), drinks, 4.1),
        FoodItem("Chocolate Cake", Price("4.50"), desserts, 4.6),
        FoodItem("Iced Tea", Price("2.99"), drinks, 3.8),
    ]

    catalog = ItemCatalog(menu_items)

    print("=== Filter: Drinks ===")
    for item in catalog.filter_by_category("Drinks"):
        print(f"- {item.get_name()} ({item.get_price().format()})")

    print("\n=== Sort: Price (Low to High) ===")
    for item in catalog.sort_by_price(ascending=True):
        print(f"- {item.get_name()} ({item.get_price().format()})")

    print("\n=== Sort: Popularity (High to Low) ===")
    for item in catalog.sort_by_popularity(ascending=False):
        print(f"- {item.get_name()} (rating: {item.popularity_rating})")

    order = Transaction()
    order.add_item(menu_items[0])
    order.add_item(menu_items[1])
    order.add_item(menu_items[2])

    tax_rate = Decimal("0.08")
    print("\n=== Order Total ===")
    print(
        f"Subtotal: USD {order.compute_subtotal().quantize(Decimal('0.01'))}")
    print(f"Tax (8%): USD {order.compute_tax(tax_rate)}")
    print(f"Total: {order.total_formatted(tax_rate)}")
