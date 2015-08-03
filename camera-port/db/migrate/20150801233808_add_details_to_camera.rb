class AddDetailsToCamera < ActiveRecord::Migration
  def change
    add_column :cameras, :owner, :string
    add_column :cameras, :name, :string
    add_index :cameras, :name, unique: true
  end
end
