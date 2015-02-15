class CreateProductOffers < ActiveRecord::Migration
  def up
    create_table :product_offers do |t|
      t.references :product, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_offers
  end
end
