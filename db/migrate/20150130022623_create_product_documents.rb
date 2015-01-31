class CreateProductDocuments < ActiveRecord::Migration
  def up
    create_table :product_documents do |t|
      t.references :products, null: false
      t.string :document_url, null: false
      t.timestamps
    end
  end

  def down
    drop_table :product_documents    
  end
end
