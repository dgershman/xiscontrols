class CreateManufacturersProducts < ActiveRecord::Migration
  def up
    create_table :manufacturers_products do |t|
      t.references :manufacturer, null: false
      t.references :product, null: false      
      t.timestamps
    end
  end

  def down
    drop_table :manufacturers_products
  end
end
