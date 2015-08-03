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

  # generate s3 link then redirect to it
  def show_content
    # set_photo will raise exception if photo not found by id
    # so @photo never be null
    obj = S3_BUCKET_PHOTO.object(@photo.aws_key)
    if obj.exists?
      # https://docs.aws.amazon.com/AmazonS3/latest/dev/UploadObjSingleOpRuby.html
      # https://stackoverflow.com/questions/10811017/how-to-store-data-in-s3-and-allow-user-access-in-a-secure-way-with-rails-api-i
      # https://stackoverflow.com/questions/12279056/rails-allow-download-of-files-stored-on-s3-without-showing-the-actual-s3-url-to
      # https://docs.aws.amazon.com/sdkforruby/api/Aws/S3/Object.html#presigned_url-instance_method
      url = obj.presigned_url(:get, expires_in: 300) # 5 minutes
      redirect_to url
    else
      logger.warn "invalid photo s3 key #{@photo.aws_key}, redirect to list page"
      redirect_to photos_url
    end
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
    photo_file = params[:photo_file]
    # TODO refactor fill_photo_fields
    if fill_photo_fields(@photo, photo_params, photo_file)
      logger.info "receive photo, #{@photo.attributes}"
      obj = S3_BUCKET_PHOTO.object(@photo.aws_key)
      # TODO add log
      logger.info "upload to s3, bucket #{obj.bucket_name}, key #{obj.key}"
      obj.put(body: photo_file.tempfile)

      logger.debug "read EXIF from photo"
      # read exif and fill width and height
      photo_file.tempfile.rewind
      # EXIFR will cause closing of the temp file
      # so read EXIF after uploading photo
      exif = read_photo_exif(photo_file)
      logger.debug "got EXIF, #{exif}"
      @photo.width = exif.width
      @photo.height = exif.height

      # TODO remove response_to
      respond_to do |format|
        logger.debug "save photo"
        if @photo.save
          # save photo file to AWS
          format.html { redirect_to @photo, notice: 'Photo was successfully created.' }
          format.json { render :show, status: :created, location: @photo }
        else
          format.html { render :new }
          format.json { render json: @photo.errors, status: :unprocessable_entity }
        end
      end
    else
      render :new
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
      logger.debug "no such photo #{params[:id]}, redirect to list page"
      redirect_to photos_url
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def photo_params
      params.require(:photo).permit(:location, :camera_id)
    end

    def read_photo_exif(photo_file)
      content_type = photo_file.content_type
      if content_type == 'image/jpeg'
        EXIFR::JPEG.new(photo_file.tempfile)
      elsif content_type == 'image/tiff'
        EXIFR::TIFF.new(photo_file.tempfile)
      else
        raise ArgumentError, "unsupport photo content type #{content_Type}"
      end
    end

    def fill_photo_fields(photo, params, photo_file)
      camera_id = params[:camera_id]
      camera = Camera.find(camera_id)

      content_type = photo_file.content_type
      extension = PHOTO_EXTENSIONS[content_type]
      # TODO add errors to photo
      return false if camera.nil? || extension.nil?

      photo.camera = camera
      photo.content_type = content_type
      photo.file_size = photo_file.size
      photo.date_token = DateTime.now
      photo.aws_key = Photo.generate_aws_key(camera, extension.downcase)
      return true
    end

end
