## Setup Instructions

1. **Clone the repository**

First, clone the repository containing the scripts to your local machine. You can do this by using the following command in your terminal:

```bash
git clone [<repository URL>](https://github.com/actuallyrizzn/matrixsearch)
```

Replace `<repository URL>` with the URL of your Git repository.

2. **Set up a virtual environment (optional, but recommended)**

To prevent your project's dependencies from interfering with your other Python projects, it's best to create a virtual environment. Here's how to do it:

```bash
python3 -m venv myenv
```

And then activate it with:

```bash
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

3. **Install necessary Python packages**

The scripts require several Python packages. Install them with:

```bash
pip install google-cloud-vision python-dotenv requests tqdm opencv-python Pillow beautifulsoup4
```

4. **Set up Google Cloud Vision API**

You need to set up a Google Cloud Project, enable the Cloud Vision API, and create an API key file (`.json` file):

- Follow the [Google Cloud Vision API Python Client documentation](https://cloud.google.com/vision/docs/libraries#client-libraries-usage-python) to set up a Google Cloud Project and enable the Cloud Vision API.
- Go to the API & Services → Credentials page on the Google Cloud Console, and create a new API key. This will download a `.json` file.

5. **Configure the API key file**

- Rename the downloaded file to `.google_creds.json` and move it into the main project folder.
- This file should have the following structure:

```json
{                                                                                                
    "type": "service_account",                                                                    
    "project_id": "your-project-id",                                                         
    "private_key_id": "your-private-key-id",                                  
    "private_key": "your-private-key",                                         
    "client_email": "your-client-email",              
    "client_id": "your-client-id",                                                            
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",                                       
    "token_uri": "https://oauth2.googleapis.com/token",                                            
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",                   
    "client_x509_cert_url": "your-client-cert-url",
    "universe_domain": "googleapis.com",                                                          
    "api_key":"your-api-key",                                            
    "cse_id":"your-cse-id"                                                                 
}
```

Replace all `"your-xxx"` parts with your actual credentials. 

6. **Configure input JSON files**

- The script `image_scraper.py` requires a JSON file formatted in the following way:

```json
{
  "name1": ["category1", "category2", ...],
  "name2": ["category1", "category2", ...],
  ...
}
```

- Save this file in the main project folder. The name of the person will be searched on Google Images along with each category.

7. **Run the scripts**

- Now you can run `image_scraper.py` to download images for each person, and `crop_faces.py` to crop faces from the downloaded images.
