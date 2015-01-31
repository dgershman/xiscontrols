class CreateProductManufacturers < ActiveRecord::Migration
  def up
    create_table :product_manufacturers do |t|
      t.references :products, null: false
      t.references :manufacturers, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_manufacturers
  end
end
