class CreatePayments < ActiveRecord::Migration
  def up
    create_table :payments do |t|
      t.references :invoice, null: false
      t.decimal :amount, precision: 8, scale: 2, default: 0.0, null: false
      t.string :status, null: false
      t.timestamps
    end
  end

  def down
    drop_table :payments
  end
end
