class Photo < ActiveRecord::Base
  belongs_to :camera

  # aws key generated when saved
  def self.generate_aws_key(camera, extension)
    raise ArgumentError, 'camera cannot be nil' if camera.nil?
    "#{camera.name}-#{camera.id}/#{Date.today.to_s}/#{SecureRandom.uuid}#{extension}"
  end
end