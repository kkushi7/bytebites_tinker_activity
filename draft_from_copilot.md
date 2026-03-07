# UML-Style Class Diagram (Draft)


```mermaid
classDiagram
    class Customer {
        -name: String
        -purchaseHistory: List~FoodItem~
        +isRealUser(): Boolean
        +addPurchase(item: FoodItem): void
        +getPurchaseHistory(): List~FoodItem~
    }


    class FoodItem {
        -name: String
        -price: Price
        -category: Category
        -popularityRating: float
        +getDisplayName(): String
        +updatePopularity(newRating: float): void
    }


    class Price {
        -amount: decimal
        -currency: String
        +getAmount(): decimal
        +format(): String
    }


    class Category {
        -name: String
        +getName(): String
        +matches(filter: String): Boolean
    }


    Customer "1" o-- "0..*" FoodItem : purchaseHistory
    FoodItem "1" *-- "1" Price : has
    FoodItem "1" *-- "1" Category : belongsTo
```


## Notes
- This draft only models the four classes explicitly listed in `Candidate Classes`.
- Additional domain objects mentioned in the request (like `ItemCollection` and `Transaction`) can be added in a next iteration.
