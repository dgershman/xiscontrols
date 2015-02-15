class CreateInventories < ActiveRecord::Migration
  def up
    create_table :inventories do |t|
      t.references :product, null: false
      t.integer :quantity_on_hand, null: false
      t.timestamps
    end
  end

  def down
    drop_table :inventories
  end
end
