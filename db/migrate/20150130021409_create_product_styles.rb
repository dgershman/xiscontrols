class CreateProductStyles < ActiveRecord::Migration
  def up
    create_table :product_styles do |t|
      t.references :products, null: false
      t.references :styles, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_styles
  end
end
