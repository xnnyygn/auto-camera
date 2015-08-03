S3 = Aws::S3::Resource.new(region: 'ap-northeast-1')
S3_BUCKET_PHOTO = S3.bucket('xnnyygn-in-default')