class AddFileSizeToPhoto < ActiveRecord::Migration
  def change
    add_column :photos, :file_size, :int
  end
end
