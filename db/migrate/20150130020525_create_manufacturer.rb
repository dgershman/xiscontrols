class CreateManufacturer < ActiveRecord::Migration
  def up
    create_table :manufacturers do |t|
      t.string :name, null: false, unique: true
      t.timestamps
    end
  end

  def down
    drop_table :manufacturers    
  end
end
