class CreatePurchaseOrders < ActiveRecord::Migration
  def up
    create_table :purchase_orders do |t|
      t.references :supplier, null: false
      t.string :status, null: false
      t.datetime :placed_at
      t.date :due_date
      t.timestamps
    end
  end

  def down
    drop_table :purchase_orders
  end
end
