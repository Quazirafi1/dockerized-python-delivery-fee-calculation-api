To run this project, follow these steps:


Prequisites 
-> Python
-> Flask

1. run "docker-compose up" to install and run the dependencies

Making Requests
Once the development server is running, please make a POST request to "http://localhost:5000/calculate-delivery-fee" with the following request body.

{
   "cart_value":1,
   "delivery_distance":9000,
   "number_of_items":4,
   "time":"2024-01-19T16:00:00Z"
}

Please feel free to modify the JSON values to test different scenarios.

