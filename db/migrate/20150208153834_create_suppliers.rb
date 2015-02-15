class CreateSuppliers < ActiveRecord::Migration
  def up
    create_table :suppliers do |t|
      t.string :name, null: false, unique: true      
      t.timestamps
    end
  end

  def down
    drop_table :suppliers
  end
end
