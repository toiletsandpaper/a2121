from requests import post

token = "gff7e8df9bbd450c8a5c2gbd35762aa872g92e96e2chf9d0ahee3c9efd7bcge2fa2g98d01e4f4e267548a5"

response = post("http://127.0.0.1:8081/student/validate_identity", data={
    "access_token": token,
    "username": "Ar4ikov"
}, files={"photo.jpg": open("d1.jpg", "rb").read()})

print(response.json())
