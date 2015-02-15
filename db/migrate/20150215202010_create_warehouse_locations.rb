class CreateWarehouseLocations < ActiveRecord::Migration
  def up
    create_table :warehouse_locations do |t|
      t.references :warehouse
      # add geographic location
      t.timestamps
    end
  end

  def down
    drop_table :warehouse_locations
  end
end
