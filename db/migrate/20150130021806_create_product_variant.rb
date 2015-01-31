class CreateProductVariant < ActiveRecord::Migration
  def up
    create_table :product_variants do |t|
      t.references :products, null: false      
      t.string :sku, null: false, unique: true
      t.string :description
      t.decimal :price, precision: 8, scale: 2, default: 0.0, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_variants
  end
end
