from flask import Flask
from google.cloud import storage
import datetime


app = Flask(__name__)


@app.route('/')
def generate_download_signed_url_v4(bucket_name="my-bucket", blob_name="test.jpg"):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    #storage_client = storage.Client.from_service_account_json('acc-key.json') # had to add a key here
    #storage_client = storage.Client(project="dhauptman")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version='v4',
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method='GET')

    print('Generated GET signed URL:')
    print(url)
    print('You can use this URL with any user agent, for example:')
    print('curl \'{}\''.format(url))
    return url

@app.route('/_ah/warmup')
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

