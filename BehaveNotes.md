Kong five steps
---
Service configuration
---
- New service

  curl -i -X POST \
  --url http://localhost:8001/services/ \
  --data 'name=example-service' \
  --data 'url=http://mockbin.org'
  
- New route for service 

  curl -i -X POST \
    --url http://localhost:8001/services/example-service/routes \
    --data 'hosts[]=example.com'
    
- Test:

  curl -i -X GET \
  --url http://localhost:8000/ \
  --header 'Host: example.com'
---
Add plugins
---  
- Configure Key-auth plugin for a service
  
  curl -i -X POST \
  --url http://localhost:8001/services/example-service/plugins/ \
  --data 'name=key-auth'
  
- Test (expects 401 code):
  
  curl -i -X GET \
  --url http://localhost:8000/ \
  --header 'Host: example.com'
  
---
Add consumers
---
 - Create a user (consumer == user)
 
 curl -i -X POST \
  --url http://localhost:8001/consumers/ \
  --data "username=Jason"
  
  - Associate an api key to a consumer
  
  curl -i -X POST \
  --url http://localhost:8001/consumers/Jason/key-auth/ \
  --data 'key=ENTER_KEY_HERE'
  
  - Control the api-key is usable for our service
  
  curl -i -X GET \
  --url http://localhost:8000 \
  --header "Host: example.com" \
  --header "apikey: ENTER_KEY_HERE"