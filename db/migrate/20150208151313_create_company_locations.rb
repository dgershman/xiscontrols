class CreateCompanyLocations < ActiveRecord::Migration
  def up
    create_table :company_locations do |t|
      t.string :name, null: false
      t.references :company, null: false          
      t.timestamps
    end
  end

  def down
    drop_table :company_locations
  end
end
