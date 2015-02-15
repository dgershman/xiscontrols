# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20150215202038) do

  create_table "active_admin_comments", force: :cascade do |t|
    t.string   "namespace"
    t.text     "body"
    t.string   "resource_id",   null: false
    t.string   "resource_type", null: false
    t.integer  "author_id"
    t.string   "author_type"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "active_admin_comments", ["author_type", "author_id"], name: "index_active_admin_comments_on_author_type_and_author_id"
  add_index "active_admin_comments", ["namespace"], name: "index_active_admin_comments_on_namespace"
  add_index "active_admin_comments", ["resource_type", "resource_id"], name: "index_active_admin_comments_on_resource_type_and_resource_id"

  create_table "admin_users", force: :cascade do |t|
    t.string   "email",                  default: "", null: false
    t.string   "encrypted_password",     default: "", null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,  null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string   "current_sign_in_ip"
    t.string   "last_sign_in_ip"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "admin_users", ["email"], name: "index_admin_users_on_email", unique: true
  add_index "admin_users", ["reset_password_token"], name: "index_admin_users_on_reset_password_token", unique: true

  create_table "bill_of_materials", force: :cascade do |t|
    t.integer  "product_id",             null: false
    t.integer  "parent"
    t.integer  "quantity",   default: 1, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "categories", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "categories_products", force: :cascade do |t|
    t.integer  "category_id", null: false
    t.integer  "product_id",  null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "companies", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "company_locations", force: :cascade do |t|
    t.string   "name",       null: false
    t.integer  "company_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "contacts", force: :cascade do |t|
    t.string   "first_name",          null: false
    t.string   "last_name",           null: false
    t.string   "email",               null: false
    t.string   "contact_type",        null: false
    t.integer  "company_location_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "documents", force: :cascade do |t|
    t.integer  "product_id", null: false
    t.string   "url",        null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "images", force: :cascade do |t|
    t.integer  "product_id", null: false
    t.string   "url",        null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "inventories", force: :cascade do |t|
    t.integer  "product_id",       null: false
    t.integer  "quantity_on_hand", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "invoice_line_items", force: :cascade do |t|
    t.integer  "invoice_id",         null: false
    t.integer  "order_line_item_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "invoices", force: :cascade do |t|
    t.integer  "sales_order_id",                                       null: false
    t.decimal  "amount",         precision: 8, scale: 2, default: 0.0, null: false
    t.date     "due_date",                                             null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "manufacturers", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "manufacturers_products", force: :cascade do |t|
    t.integer  "manufacturer_id", null: false
    t.integer  "product_id",      null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "payments", force: :cascade do |t|
    t.integer  "invoice_id",                                       null: false
    t.decimal  "amount",     precision: 8, scale: 2, default: 0.0, null: false
    t.string   "status",                                           null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_offer_components", force: :cascade do |t|
    t.integer  "product_offer_id",                                          null: false
    t.integer  "product_id",                                                null: false
    t.datetime "availability_starts",                                       null: false
    t.datetime "availability_ends"
    t.integer  "minimum_required"
    t.integer  "maximum_required"
    t.decimal  "price",               precision: 8, scale: 2, default: 0.0, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_offers", force: :cascade do |t|
    t.integer  "product_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "products", force: :cascade do |t|
    t.string "name"
    t.string "description"
  end

  create_table "products_styles", force: :cascade do |t|
    t.integer  "product_id", null: false
    t.integer  "style_id",   null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "products_suppliers", force: :cascade do |t|
    t.integer  "product_id",  null: false
    t.integer  "supplier_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "purchase_order_line_items", force: :cascade do |t|
    t.integer  "purchase_order_id",                                       null: false
    t.integer  "product_id",                                              null: false
    t.integer  "quantity_ordered",                                        null: false
    t.integer  "quantity_received",                         default: 0,   null: false
    t.integer  "quantity_rejected",                         default: 0,   null: false
    t.decimal  "price",             precision: 8, scale: 2, default: 0.0, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "purchase_orders", force: :cascade do |t|
    t.integer  "supplier_id", null: false
    t.string   "status",      null: false
    t.datetime "placed_at"
    t.date     "due_date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "sales_order_line_items", force: :cascade do |t|
    t.integer  "sales_order_id",             null: false
    t.integer  "variant_id",                 null: false
    t.integer  "quantity",       default: 1, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "sales_orders", force: :cascade do |t|
    t.integer  "company_id",          null: false
    t.string   "status",              null: false
    t.integer  "company_location_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "shipments", force: :cascade do |t|
    t.integer  "sales_order_id", null: false
    t.string   "status",         null: false
    t.date     "ship_date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "styles", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "suppliers", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "variants", force: :cascade do |t|
    t.integer  "product_id",                                        null: false
    t.string   "sku",                                               null: false
    t.string   "description"
    t.decimal  "weight",      precision: 8, scale: 2, default: 0.0, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "warehouse_locations", force: :cascade do |t|
    t.integer  "warehouse_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "warehouses", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
