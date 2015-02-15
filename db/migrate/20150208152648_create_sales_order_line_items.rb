class CreateSalesOrderLineItems < ActiveRecord::Migration
  def up
    create_table :sales_order_line_items do |t|
      t.references :sales_order, null: false
      t.references :variant, null: false
      t.integer :quantity, null: false, default: 1
      t.timestamps
    end
  end

  def down
    drop_table :sales_order_line_items
  end
end
