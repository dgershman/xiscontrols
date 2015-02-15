class CreateInvoices < ActiveRecord::Migration
  def up
    create_table :invoices do |t|
      t.references :sales_order, null: false
      t.decimal :amount, precision: 8, scale: 2, default: 0.0, null: false
      t.date :due_date, null: false
      t.timestamps
    end
  end

  def down
    drop_table :invoices
  end
end
