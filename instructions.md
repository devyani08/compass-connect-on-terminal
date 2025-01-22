## Run the python file 
```python3 -u "/Users/outcomes/Documents/mongo-db/app.py"```
---
## Sample Data
```
Enter Guide Title: Distal Radius Fracture Rehabilitation
Enter Stage: Rehabilitation
Enter Disease Title: Fracture
Enter Specialty: orthopedics
Enter Job ID (mandatory): 6763dba418b2421cc4d15c63
106 documents found with Job ID 6763dba418b2421cc4d15c63.
JSON file generated: 6763dba418b2421cc4d15c63.json

```
---
## SSL Certification issues

### 1. Install Certificates on macOS
Run the following command in your terminal to install or update SSL certificates:
/Applications/Python\ 3.x/Install\ Certificates.command
Replace 3.x with your installed Python version (e.g., 3.9 or 3.10).

### 2. Modify Connection String to Disable SSL Verification
While not recommended for production, you can bypass SSL certificate verification by modifying your connection string. Update the URI in your .env file or the `mongo_uri` to include `tlsAllowInvalidCertificates=true` :

`mongodb+srv://<username>:<password>@cluster0.is2at.mongodb.net/?tlsAllowInvalidCertificates=true`

### 4. Use certifi for Certificates (skipped)
Install the certifi library and configure PyMongo to use it for SSL certificates:

```
pip install certifi (already in requirements.txt)
```
Update the code to pass the certificate explicitly (on main code, app.py):
```
import certifi
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
```


#### Refer this documentation([https://www.mongodb.com/docs/languages/python/pymongo-driver/troubleshooting/]) for any other pymongo errors