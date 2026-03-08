from decimal import Decimal

from models import Category, FoodItem, ItemCatalog, Price, Transaction


def test_order_totals_with_tax() -> None:
    mains = Category("Mains")
    drinks = Category("Drinks")

    burger = FoodItem("Spicy Burger", Price("8.99"), mains, 4.7)
    soda = FoodItem("Large Soda", Price("2.49"), drinks, 4.1)
    cake = FoodItem("Chocolate Cake", Price("4.50"), Category("Desserts"), 4.6)

    order = Transaction([burger, soda, cake])
    tax_rate = Decimal("0.08")

    assert order.compute_subtotal() == Decimal("15.98")
    assert order.compute_tax(tax_rate) == Decimal("1.28")
    assert order.compute_total(tax_rate) == Decimal("17.26")


def test_empty_order_totals_are_zero() -> None:
    order = Transaction()

    assert order.compute_subtotal() == Decimal("0")
    assert order.compute_tax(Decimal("0.08")) == Decimal("0.00")
    assert order.compute_total(Decimal("0.08")) == Decimal("0.00")
    assert order.total_formatted(Decimal("0.08")) == "USD 0.00"


def test_filter_menu_items_by_category() -> None:
    drinks = Category("Drinks")
    mains = Category("Mains")

    menu = [
        FoodItem("Spicy Burger", Price("8.99"), mains, 4.7),
        FoodItem("Large Soda", Price("2.49"), drinks, 4.1),
        FoodItem("Iced Tea", Price("2.99"), drinks, 3.8),
    ]
    catalog = ItemCatalog(menu)

    drink_items = catalog.filter_by_category("drinks")

    assert len(drink_items) == 2
    assert [item.get_name() for item in drink_items] == [
        "Large Soda", "Iced Tea"]
