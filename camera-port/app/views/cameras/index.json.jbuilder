json.array!(@cameras) do |camera|
  json.extract! camera, :id, :manufactor, :model
  json.url camera_url(camera, format: :json)
end
