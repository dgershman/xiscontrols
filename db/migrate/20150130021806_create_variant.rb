class CreateVariant < ActiveRecord::Migration
  def up
    create_table :variants do |t|
      t.references :product, null: false      
      t.string :sku, null: false, unique: true
      t.string :description      
      t.decimal :weight, precision: 8, scale: 2, default: 0.0, null: false
      t.timestamps
    end
  end

  def down
    drop_table :variants
  end
end
