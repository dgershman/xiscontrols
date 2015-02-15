class CreateImages < ActiveRecord::Migration
  def up
    create_table :images do |t|
      t.references :product, null: false
      t.string :url, null: false
      t.timestamps
    end
  end

  def down
    drop_table :images
  end
end
