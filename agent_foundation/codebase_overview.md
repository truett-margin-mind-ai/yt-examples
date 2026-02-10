# Codebase Overview for AI Agent

## Project
- **Name:** `dbt_core`
- **Type:** dbt (data build tool) project
- **Data Source:** Lightspeed R-series POS system 

## Database Configuration
- **Project ID:** `inventory-analytics-475119`
- **Profile:** `dbt_core`

---

## Raw Data Schema

**Schema:** `lightspeed_raw`

### Tables

| Table | Description |
|-------|-------------|
| `categories` | Product categories |
| `item_matrices` | Item matrix/variant definitions |
| `item_shops` | Item availability and settings per shop |
| `items` | Product/item master data |
| `manufacturers` | Product manufacturers |
| `order_lines` | Individual line items on purchase orders |
| `orders` | Purchase orders to vendors |
| `sale_lines` | Individual line items on sales transactions |
| `sales` | Sales transactions |
| `shops` | Store/shop locations |
| `transfer_items` | Items included in inventory transfers |
| `transfers` | Inventory transfers between locations |
| `vendors` | Vendor/supplier master data |

---

## Query Reference

To query raw tables, use:
```sql
SELECT * FROM `inventory-analytics-475119.lightspeed_raw.<table_name>`
```

### Key Relationships
- `sales` → `sale_lines` (sales transactions and their line items)
- `orders` → `order_lines` (purchase orders and their line items)
- `transfers` → `transfer_items` (inventory transfers and items moved)
- `items` → `item_shops` (products and their per-shop settings)
- `items` → `categories`, `manufacturers`, `vendors` (product attributes)

### When returning data to the user
- do not include store names, use store_ids 
