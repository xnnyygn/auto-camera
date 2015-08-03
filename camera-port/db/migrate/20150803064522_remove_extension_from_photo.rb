class RemoveExtensionFromPhoto < ActiveRecord::Migration
  def change
    remove_column :photos, :extension
  end
end
