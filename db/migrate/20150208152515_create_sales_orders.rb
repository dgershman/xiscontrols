class CreateSalesOrders < ActiveRecord::Migration
  def up
    create_table :sales_orders do |t|
      t.references :company, null: false
      t.string :status, null: false
      t.references :company_location, null: false
      t.timestamps
    end
  end

  def down
    drop_table :sales_orders
  end
end
