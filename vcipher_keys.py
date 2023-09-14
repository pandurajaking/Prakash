import requests

# Replace this with your token (Smaller One)
token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6OTI1MzU1NzksIm9yZ0lkIjo0MDMwOTUsInR5cGUiOjEsIm1vYmlsZSI6IjkxNjM1OTE0NjE0NSIsIm5hbWUiOiJQcmFrYXNoIEJhcmFpeWEiLCJlbWFpbCI6InByYWthc2gxNTEwODNAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOmZhbHNlLCJvcmdDb2RlIjoib3hwYmgiLCJmaW5nZXJwcmludElkIjoiYTg0MjNkYjFlZjE5MjI3ZTMyOGFmNGEwMGRlODJlMTEiLCJpYXQiOjE2OTQwNzk1MjYsImV4cCI6MTY5NDY4NDMyNn0.3EatpR80XlzD2q9pImEnvYXieV3SfwckUExG_Y-4NtLk6CSm_dkKPfRKynp-Ed3F"

response = requests.post(
    "https://learnyst.devsrajput.com/free", 
    data={
        "link": token,
    }
)

if response.status_code != 200:
    print("Request Failed! reasons:\n\t1). Token Expired\n\t2). API Not Working")
    exit()

data = response.json()

if data is None:
    print("Failed to retrieve data from the API.")
    exit()

name = data.get("TITLE")
link = data.get("MPD")
keys = data.get("KEY_STRING")

if name is not None and link is not None and keys is not None:
    print(f"{name}\n{link}\n{token}\n\n{keys}")
else:
    print("Failed to retrieve all required data from the API.")
