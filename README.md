# RSACipher
Simple RSA cipher with FastAPI & Unittests

Title: Recruitment task\
Author: Hubert Knioła

Completed tasks:
- RSA Cipher - DONE
- Encode and decode methods - DONE
- Simple Unit Tests - DONE
- FastAPI Server with previous methods - DONE
- BasicAuth FastAPI - DONE
- Code documentations - DONE
- Dockerization - IN

Starting the server
```
uvicorn api:app --reload
```

Running tests
```
pytest tests_cipher.py
```

TESTS

<p align="center">
  <img src="Images/tests.PNG" title="Tests">
</p>

API ENDPOINTS & EFFECTS

REQUEST FORM /allinone
<p align="center">
  <img src="Images/allinone-req.PNG" title="All in one">
</p>

POST /allinone
<p align="center">
  <img src="Images/allinone.PNG" title="All in one">
</p>

GET /elements
<p align="center">
  <img src="Images/elements.PNG" title="Elements">
</p>

POST /element/{id}
<p align="center">
  <img src="Images/element.PNG" title="Element">
</p>

REQUEST FORM /encode
<p align="center">
  <img src="Images/encode-request.PNG" title="Encode">
</p>

POST /encode
<p align="center">
  <img src="Images/encode.PNG" title="Encode">
</p>

REQUEST FORM /decode
<p align="center">
  <img src="Images/decode-request.PNG" title="Encode">
</p>

POST /decode
<p align="center">
  <img src="Images/decode.PNG" title="Decode">
</p>




