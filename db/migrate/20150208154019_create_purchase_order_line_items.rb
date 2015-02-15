class CreatePurchaseOrderLineItems < ActiveRecord::Migration
  def up
    create_table :purchase_order_line_items do |t|
      t.references :purchase_order, null: false
      t.references :product, null: false
      t.integer :quantity_ordered, null: false
      t.integer :quantity_received, null: false, default: 0
      t.integer :quantity_rejected, null: false, default: 0
      t.decimal :price, precision: 8, scale: 2, default: 0.0, null: false
      t.timestamps
    end
  end

  def down
    drop_table :purchase_order_line_items
  end
end
