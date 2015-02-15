class CreateDocuments < ActiveRecord::Migration
  def up
    create_table :documents do |t|
      t.references :product, null: false
      t.string :url, null: false
      t.timestamps
    end
  end

  def down
    drop_table :documents    
  end
end
