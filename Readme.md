The app has been dockerized and deployed in Azure App Services:

You can run this project locally or online.


To run Locally follow the following steps:
1. run "docker-compose up" to install and run the dependencies


2. Once the development server is running, please make a POST request to "http://localhost:5000/calculate-delivery-fee" with the following request body.

{
   "cart_value":1,
   "delivery_distance":9000,
   "number_of_items":4,
   "time":"2024-01-19T16:00:00Z"
}

Or, you can test the Azure deployment by make a POST request to "https://flaskdeliveryfeecalculator.azurewebsites.net/calculate-delivery-fee" with the following request body.

{
   "cart_value":1,
   "delivery_distance":9000,
   "number_of_items":4,
   "time":"2024-01-19T16:00:00Z"
}

Please feel free to modify the JSON values to test different scenarios.