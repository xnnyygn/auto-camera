class PhotosController < ApplicationController
  before_action :set_photo, only: [:show, :show_content, :edit, :update, :destroy]

  # GET /photos
  # GET /photos.json
  def index
    @photos = Photo.all
  end

  # GET /photos/1
  # GET /photos/1.json
  def show
  end

  def show_content
    if @photo
      obj = S3_BUCKET_PHOTO.object(@photo.aws_key)
      if obj.exists?
      # https://docs.aws.amazon.com/AmazonS3/latest/dev/UploadObjSingleOpRuby.html
      # https://stackoverflow.com/questions/10811017/how-to-store-data-in-s3-and-allow-user-access-in-a-secure-way-with-rails-api-i
      # https://stackoverflow.com/questions/12279056/rails-allow-download-of-files-stored-on-s3-without-showing-the-actual-s3-url-to
      # https://docs.aws.amazon.com/sdkforruby/api/Aws/S3/Object.html#presigned_url-instance_method
        url = obj.presigned_url(:get, expires_in: 300) # 5 minutes
        redirect_to url
        return
      end
    end
    
    render plain: "404 Not Found", status: 404
  end

  # GET /photos/new
  def new
    @photo = Photo.new
  end

  # GET /photos/1/edit
  def edit
  end

  # POST /photos
  # POST /photos.json
  def create
    @photo = Photo.new(photo_params)
    if !fill_photo_fields(@photo, photo_params)
      render :new
      return
    end

    # TODO remove response_to
    respond_to do |format|
      if @photo.save
        format.html { redirect_to @photo, notice: 'Photo was successfully created.' }
        format.json { render :show, status: :created, location: @photo }
      else
        format.html { render :new }
        format.json { render json: @photo.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /photos/1
  # PATCH/PUT /photos/1.json
  def update
    # TODO camera id
    respond_to do |format|
      if @photo.update(photo_params)
        format.html { redirect_to @photo, notice: 'Photo was successfully updated.' }
        format.json { render :show, status: :ok, location: @photo }
      else
        format.html { render :edit }
        format.json { render json: @photo.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /photos/1
  # DELETE /photos/1.json
  def destroy
    @photo.destroy
    respond_to do |format|
      format.html { redirect_to photos_url, notice: 'Photo was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_photo
      @photo = Photo.find(params[:id])
    rescue ActiveRecord::RecordNotFound
      redirect_to photos_url
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def photo_params
      params.require(:photo).permit(:width, :height, :location, :extension, :camera_id)
    end

    def fill_photo_fields(photo, params)
      camera_id = params[:camera_id]
      camera = Camera.find(camera_id)
      extension = params[:extension]
      # TODO validate extension, whitelist?
      return false if camera.nil? || extension.blank?

      photo.camera = camera
      photo.date_token = DateTime.now
      photo.aws_key = Photo.generate_aws_key(camera, extension.downcase)
      return true
    end

end
