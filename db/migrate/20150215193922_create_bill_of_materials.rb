class CreateBillOfMaterials < ActiveRecord::Migration
  def up
    create_table :bill_of_materials do |t|
      t.references :product, null: false
      t.integer :parent
      t.integer :quantity, null: false, default: 1    
      t.timestamps
    end
  end

  def down
    drop_table :bill_of_materials
  end
end
