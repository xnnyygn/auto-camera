json.array!(@photos) do |photo|
  json.extract! photo, :id, :aws_key, :width, :height, :date_token, :location, :camera
  json.url photo_url(photo, format: :json)
end
