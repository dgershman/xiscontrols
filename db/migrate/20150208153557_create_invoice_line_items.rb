class CreateInvoiceLineItems < ActiveRecord::Migration
  def up
    create_table :invoice_line_items do |t|
      t.references :invoice, null: false
      t.references :order_line_item, null: false
      t.timestamps
    end
  end

  def down
    drop_table :invoice_line_items
  end
end
