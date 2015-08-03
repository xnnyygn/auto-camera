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

ActiveRecord::Schema.define(version: 20150803064911) do

  create_table "cameras", force: true do |t|
    t.string   "manufactor"
    t.string   "model"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "owner"
    t.string   "name"
  end

  add_index "cameras", ["name"], name: "index_cameras_on_name", unique: true

  create_table "photos", force: true do |t|
    t.string   "aws_key"
    t.integer  "width"
    t.integer  "height"
    t.datetime "date_token"
    t.string   "location"
    t.integer  "camera_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "content_type"
    t.integer  "file_size"
  end

  add_index "photos", ["camera_id"], name: "index_photos_on_camera_id"

end
