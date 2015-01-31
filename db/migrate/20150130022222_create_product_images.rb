class CreateProductImages < ActiveRecord::Migration
  def up
    create_table :product_images do |t|
      t.references :products, null: false
      t.string :image_url, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_images
  end
end
