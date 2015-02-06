class CreateCategoriesProducts < ActiveRecord::Migration
  def up
    create_table :categories_products do |t|
      t.references :category, null: false
      t.references :product, null: false
      t.timestamps
    end
  end

  def down
    drop_table :categories_products
  end
end
