import requests

# Replace this with your token (Smaller One)
token = "eyJvdNjA......."

response = requests.post(
    "https://learnyst.devsrajput.com/free", 
    data={
        "link":token,
    }
)

if response.status_code != 200:
    print("Request Failed! reasons:\n\t1).Token Expired\n\t2). API Not Working")
    exit()

data = response.json()
name = data["TITLE"]
link = data["MPD"]
keys = data["KEY_STRING"]

print(f"{name}\n{link}\n{token}\n\n{keys}")