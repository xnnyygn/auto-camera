class AddExtensionToPhoto < ActiveRecord::Migration
  def change
    add_column :photos, :extension, :string
  end
end
