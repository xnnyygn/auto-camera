class Camera < ActiveRecord::Base
  validates :name, uniqueness: true
end