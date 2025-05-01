# Digital Chitthi - A Heartfelt Letter Platform

## Project Description

Digital Chitthi is a modern web application that brings back the charm of traditional letter writing in a digital format. Users can write and send heartfelt messages (chitthis) to others—either anonymously or signed—with a visual and emotional experience that mimics the charm of traditional letter writing.

## Features

### ✨ Core Features

- **Write & Send a Chitthi**
  - Input fields for sender name (optional), receiver name, and letter content
  - Option to send anonymously
  - Stylized letter UI with old parchment-like design
  - Preview functionality before sending

- **View a Received Chitthi**
  - Each letter gets a unique URL for viewing
  - Beautifully styled letter display
  - View count tracking

- **Privacy Options**
  - Option to make letters public or private
  - Configurable expiry dates (7, 30, 90 days, or never)
  - Automatic deletion of expired letters

- **Styling & UX**
  - Letter-style background with paper texture
  - Handwritten fonts (Dancing Script and Patrick Hand)
  - Smooth animations for letter interactions
  - Paper rustling sound effects

## Technical Architecture

The application is built using a serverless architecture on AWS:

- **Frontend**: HTML, CSS, and JavaScript hosted on S3
- **Backend**: AWS Lambda functions for handling letter operations
- **Database**: DynamoDB for storing letters and metadata
- **API Gateway**: For handling HTTP requests
- **CloudFront**: For content delivery and caching

## Setup Instructions

1. **Prerequisites**
   - AWS Account
   - AWS CLI configured
   - Python 3.8 or later
   - Node.js and npm

2. **Backend Setup**
   - Create a DynamoDB table named `digital-chitthi-letters`
   - Deploy the Lambda function with the provided code
   - Set up API Gateway endpoints
   - Configure environment variables in Lambda

3. **Frontend Setup**
   - Upload the HTML, CSS, and JavaScript files to S3
   - Configure CloudFront distribution
   - Update the Lambda function URL in the JavaScript code

4. **Domain Setup**
   - Configure your domain in Route 53
   - Update the CloudFront distribution with your domain
   - Set up SSL certificate

## Project Structure

```
.
├── index.html          # Main application page
├── style.css          # Styling for the application
├── script.js          # Frontend JavaScript
├── lambda-function.py # Backend Lambda function
└── README.md          # Project documentation
```

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or suggestions, please reach out to us at:
- Email: amonkincloud@gmail.com
- Website: https://amonkincloud.com/
- YouTube: https://www.youtube.com/@amonkincloud
- Instagram: https://www.instagram.com/amonkincloud/




