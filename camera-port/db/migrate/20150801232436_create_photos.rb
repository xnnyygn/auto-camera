class CreatePhotos < ActiveRecord::Migration
  def change
    create_table :photos do |t|
      t.string :aws_key
      t.integer :width
      t.integer :height
      t.datetime :date_token
      t.string :location
      t.references :camera, index: true

      t.timestamps
    end
  end
end
