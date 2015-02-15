class CreateProductsSuppliers < ActiveRecord::Migration
  def up
    create_table :products_suppliers do |t|
      t.references :product, null: false
      t.references :supplier, null: false
      t.timestamps
    end
  end

  def down
    drop_table :products_suppliers
  end
end
