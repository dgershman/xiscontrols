class CreateContacts < ActiveRecord::Migration
  def up
    create_table :contacts do |t|
      t.string :first_name, null: false
      t.string :last_name, null: false
      t.string :email, null: false
      t.string :contact_type, null: false
      t.references :company_location, null: false
      t.timestamps
    end
  end

  def down
    drop_table :contacts
  end
end
