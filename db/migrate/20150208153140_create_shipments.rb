class CreateShipments < ActiveRecord::Migration
  def up
    create_table :shipments do |t|
      t.references :sales_order, null: false
      t.string :status, null: false
      t.date :ship_date
      t.timestamps
    end
  end

  def down
    drop_table :shipments
  end
end
