class CreateProductsStyles < ActiveRecord::Migration
  def up
    create_table :products_styles do |t|
      t.references :product, null: false
      t.references :style, null: false
      t.timestamps
    end
  end

  def down
    drop_table :products_styles
  end
end
