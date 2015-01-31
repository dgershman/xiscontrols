class CreateStyles < ActiveRecord::Migration
  def up
    create_table :styles do |t|
      t.string :name, null: false, unique: true
      t.timestamps
    end
  end

  def down
    drop_table :styles    
  end
end
