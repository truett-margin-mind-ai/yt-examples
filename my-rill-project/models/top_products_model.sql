-- Model SQL
-- Reference documentation: https://docs.rilldata.com/reference/project-files/models
-- @materialize: true

SELECT
  sale_timestamp,
  product_name,
  category_name,
  manufacturer_name,
  shop_name,
  quantity,
  unit_price,
  line_total,
  discount_amount
FROM top_products_source
