class CreateProductOfferComponents < ActiveRecord::Migration
  def up
    create_table :product_offer_components do |t|
      t.references :product_offer, null: false
      t.references :product, null: false
      t.datetime :availability_starts, null: false
      t.datetime :availability_ends
      t.integer :minimum_required
      t.integer :maximum_required
      t.decimal :price, precision: 8, scale: 2, default: 0.0, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_offer_components
  end
end
