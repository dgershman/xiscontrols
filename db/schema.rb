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

ActiveRecord::Schema.define(version: 20150130022623) do

  create_table "categories", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "manufacturers", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_categories", force: :cascade do |t|
    t.integer  "products_id",   null: false
    t.integer  "categories_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_documents", force: :cascade do |t|
    t.integer  "products_id",  null: false
    t.string   "document_url", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_images", force: :cascade do |t|
    t.integer  "products_id", null: false
    t.string   "image_url",   null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_manufacturers", force: :cascade do |t|
    t.integer  "products_id",      null: false
    t.integer  "manufacturers_id", null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_styles", force: :cascade do |t|
    t.integer  "products_id", null: false
    t.integer  "styles_id",   null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "product_variants", force: :cascade do |t|
    t.integer  "products_id",                                       null: false
    t.string   "sku",                                               null: false
    t.string   "description"
    t.decimal  "price",       precision: 8, scale: 2, default: 0.0, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "products", force: :cascade do |t|
    t.string "description"
  end

  create_table "styles", force: :cascade do |t|
    t.string   "name",       null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
