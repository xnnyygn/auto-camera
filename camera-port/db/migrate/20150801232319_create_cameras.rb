class CreateCameras < ActiveRecord::Migration
  def change
    create_table :cameras do |t|
      t.string :manufactor
      t.string :model

      t.timestamps
    end
  end
end
