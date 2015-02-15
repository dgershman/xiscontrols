class CreateWarehouses < ActiveRecord::Migration
  def up
    create_table :warehouses do |t|
      t.string :name, null: false, unique: true          
      t.timestamps
    end
  end

  def down
    drop_table :warehouses
  end
end
