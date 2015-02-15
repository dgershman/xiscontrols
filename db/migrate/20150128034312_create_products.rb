class CreateProducts < ActiveRecord::Migration
  def up
    create_table :products do |t|      
      t.string :name
      t.string :description      
    	t.timestamp
    end
  end

  def down
  	drop_table :products  	
  end
end
