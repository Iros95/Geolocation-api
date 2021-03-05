1) How to aquire a token:

Send POST request to addres https://geo-api-python.herokuapp.com/login with JSON content with keys "username" and "password".
The value for password has to be "password".

Example:

{
 "username" : "user",
 "password" : "password"
}

2) How to add geolocation data:

Send POST request to adress https://geo-api-python.herokuapp.com/add_info with JSON content sepcifing type and address.
You also need to pass authentication token.
Type must be equalt to "ip" or "url" depending on what type of address have you send.

Example:

https://geo-api-python.herokuapp.com/add_info?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYxNDkzOTUxOX0.v9rxSL3tbt2BSc3APZRXwfjX3uVFGqJn0QyldRdWPtw POST

{ 
 "type" : "ip",
 "address" : "111.11.11.119"
}

 or

 { "type" : "url",
 "address" : "www.google.com"
 }

3) How to remove geolocation data:

Send POST request to adress https://geo-api-python.herokuapp.com/delete_info with JSON content sepcifing type and address.
You also need to pass authentication token.
Type must be equalt to "ip" or "url" depending on what type of address have you send.

Example:

https://geo-api-python.herokuapp.com/delete_info?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYxNDkzOTUxOX0.v9rxSL3tbt2BSc3APZRXwfjX3uVFGqJn0QyldRdWPtw POST

{ 
 "type" : "ip",
 "address" : "111.11.11.119"
}

4) How to displey geolocation data:

Send GET request to adress https://geo-api-python.herokuapp.com/get_info 
You need to pass authentication token and ip as parameters.

Example:

https://geo-api-python.herokuapp.com/get_info?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYxNDkzOTUxOX0.v9rxSL3tbt2BSc3APZRXwfjX3uVFGqJn0QyldRdWPtw&ip=111.11.11.119