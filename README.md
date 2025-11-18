# Digital Chitthi - Serverless Web Application on AWS

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)

## 📖 Project Overview

**Digital Chitthi** is a serverless web application that enables users to send heartfelt digital letters in a beautifully designed interface. Built on AWS cloud infrastructure, this project demonstrates the implementation of a fully scalable, cost-effective serverless architecture using modern cloud services.

"Chitthi" means "letter" in Hindi/Urdu, bringing the nostalgic charm of handwritten letters to the digital age.

## ✨ Features

- **Send Personalized Letters**: Create and send custom digital letters to anyone
- **Anonymous Mode**: Option to send letters anonymously
- **Public/Private Letters**: Choose whether letters are publicly accessible
- **Expiration Settings**: Set letter expiration (7, 30, 90 days, or never)
- **View Counter**: Track how many times a letter has been viewed
- **Shareable URLs**: Each letter gets a unique URL for easy sharing
- **Preview Before Sending**: Preview letters before sending them
- **Beautiful UI**: Elegant, paper-inspired design with custom fonts
- **Fully Serverless**: Scalable architecture with no server management

## 🏗️ Architecture

This application follows a serverless architecture pattern using AWS services:

```
┌─────────────────┐
│   S3 Bucket     │  Static Website Hosting
│  (Frontend)     │  - index.html, style.css, script.js
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Gateway    │  RESTful API Endpoint
│  or App Runner  │  - Routes: POST /letter, GET /letter/{id}
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lambda Function │  Business Logic
│   (Python)      │  - Create/Retrieve letters
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DynamoDB      │  NoSQL Database
│   (Letters DB)  │  - Store letter data
└─────────────────┘
```

### AWS Services Used

- **Amazon S3**: Static website hosting for frontend files
- **AWS Lambda**: Serverless compute for backend logic
- **Amazon API Gateway**: RESTful API management
- **Amazon DynamoDB**: NoSQL database for storing letters
- **AWS App Runner**: Alternative deployment option for containerized application
- **Docker**: Containerization for local development and deployment

## 📁 Project Structure

```
Serverless-Web-Application-on-AWS/
│
├── index.html              # Main landing page (letter creation form)
├── letter.html             # Letter viewing page
├── error.html              # Error page for failed requests
├── style.css               # Styling for the application
├── script.js               # Frontend JavaScript logic
│
├── lambda-function.py      # AWS Lambda function (backend logic)
├── requirements.txt        # Python dependencies (boto3)
│
├── Dockerfile              # Docker configuration for containerization
├── docker-compose.yml      # Docker Compose for local development
├── nginx.conf              # Nginx web server configuration
│
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- AWS Account with appropriate permissions
- Python 3.9 or higher
- Docker and Docker Compose (for local development)
- AWS CLI configured with credentials
- Basic knowledge of AWS services

### Installation & Deployment

#### 1. Clone the Repository

```bash
git clone https://github.com/waliulrayhan/Serverless-Web-Application-on-AWS.git
cd Serverless-Web-Application-on-AWS
```

#### 2. Set Up DynamoDB Table

Create a DynamoDB table with the following configuration:

- **Table Name**: `digital-chitthi-letters`
- **Partition Key**: `letter_id` (String)
- **Billing Mode**: On-demand or Provisioned (as per your requirement)

```bash
aws dynamodb create-table \
    --table-name digital-chitthi-letters \
    --attribute-definitions AttributeName=letter_id,AttributeType=S \
    --key-schema AttributeName=letter_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

#### 3. Deploy Lambda Function

1. Create a new Lambda function in AWS Console
2. Choose **Python 3.9** as the runtime
3. Upload the `lambda-function.py` code
4. Install dependencies:
   ```bash
   pip install boto3 -t .
   zip -r function.zip .
   ```
5. Configure environment variables if needed
6. Set appropriate IAM role with DynamoDB permissions:
   - `dynamodb:PutItem`
   - `dynamodb:GetItem`
   - `dynamodb:UpdateItem`
   - `dynamodb:DeleteItem`

#### 4. Configure API Gateway

1. Create a new REST API in API Gateway
2. Create resources:
   - `POST /letter` - For creating new letters
   - `GET /letter/{letter_id}` - For retrieving letters
3. Enable CORS for all methods
4. Deploy the API to a stage (e.g., `prod`)
5. Note the API endpoint URL

#### 5. Deploy Frontend to S3

1. Create an S3 bucket for static website hosting
2. Enable static website hosting in bucket properties
3. Update the API URL in `script.js`:
   ```javascript
   const config = {
       apiUrl: 'YOUR_API_GATEWAY_URL'
   };
   ```
4. Upload files to S3:
   ```bash
   aws s3 sync . s3://your-bucket-name --exclude "*.py" --exclude "Dockerfile*" --exclude "docker-compose.yml"
   ```
5. Set appropriate bucket policy for public read access

#### 6. Local Development with Docker

For local testing and development:

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application at http://localhost:8000
```

Set environment variables in `.env` file:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## 🔧 Configuration

### Frontend Configuration (`script.js`)

Update the API endpoint:
```javascript
const config = {
    apiUrl: 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com'
};
```

### Backend Configuration (`lambda-function.py`)

Update the DynamoDB table name if different:
```python
table = dynamodb.Table('digital-chitthi-letters')
```

Update the base URL for letter sharing:
```python
base_url = 'your-s3-website-url.s3-website-us-east-1.amazonaws.com'
```

## 📊 API Endpoints

### Create Letter
**POST** `/letter`

Request Body:
```json
{
    "sender": "John Doe",
    "receiver": "Jane Smith",
    "content": "Your heartfelt message here...",
    "isAnonymous": false,
    "isPublic": true,
    "expiryDays": "7"
}
```

Response:
```json
{
    "success": true,
    "letterUrl": "http://your-domain.com/letter/uuid",
    "letter_id": "uuid"
}
```

### Get Letter
**GET** `/letter/{letter_id}`

Response:
```json
{
    "success": true,
    "letter": {
        "sender": "John Doe",
        "receiver": "Jane Smith",
        "content": "Your heartfelt message...",
        "created_at": "2025-11-19T10:30:00",
        "views": 5
    }
}
```

## 🗄️ Database Schema

### DynamoDB Table: `digital-chitthi-letters`

| Attribute      | Type    | Description                          |
|----------------|---------|--------------------------------------|
| letter_id      | String  | Unique identifier (Primary Key)      |
| sender         | String  | Sender's name or "Anonymous"         |
| receiver       | String  | Recipient's name                     |
| content        | String  | Letter content                       |
| is_anonymous   | Boolean | Whether the letter is anonymous      |
| is_public      | Boolean | Whether the letter is publicly viewable |
| created_at     | String  | ISO timestamp of creation            |
| expiry_date    | String  | ISO timestamp of expiration (nullable) |
| views          | Number  | Number of times letter was viewed    |

## 🎨 UI Features

- **Handwritten Font Style**: Uses Google Fonts (Dancing Script, Patrick Hand) for authentic letter feel
- **Paper Texture**: CSS-styled letter paper with realistic appearance
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modal Preview**: Preview letters before sending
- **Sound Effects**: Paper sound effect when sending letters
- **Loading States**: Visual feedback during API calls

## 🔐 Security Considerations

- **CORS Configuration**: Properly configured to allow frontend-backend communication
- **Input Validation**: Server-side validation of all user inputs
- **IAM Roles**: Least privilege principle for Lambda execution role
- **Expired Letter Cleanup**: Automatic deletion of expired letters
- **Environment Variables**: Sensitive data stored in environment variables
- **No Direct Database Access**: All database operations through Lambda functions

## 💰 Cost Optimization

This serverless architecture is highly cost-effective:

- **Lambda**: Pay only for compute time (first 1M requests/month free)
- **DynamoDB**: On-demand pricing or free tier (25GB storage, 25 read/write units)
- **S3**: Pay for storage and requests (first 5GB free)
- **API Gateway**: First 1M API calls free per month
- **No Server Maintenance**: Zero infrastructure management costs

## 🧪 Testing

### Local Testing

1. Run the application locally using Docker:
   ```bash
   docker-compose up
   ```

2. Test the Lambda function locally:
   ```bash
   python lambda-function.py
   ```

### API Testing

Use tools like Postman or curl to test endpoints:

```bash
# Test POST request
curl -X POST https://your-api-url/letter \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "Test User",
    "receiver": "Test Recipient",
    "content": "Test message",
    "isAnonymous": false,
    "isPublic": true,
    "expiryDays": "7"
  }'

# Test GET request
curl https://your-api-url/letter/{letter_id}
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure API Gateway has CORS enabled
   - Check Lambda function CORS headers

2. **Lambda Function Timeout**
   - Increase Lambda timeout setting (default: 3 seconds)
   - Optimize DynamoDB query performance

3. **DynamoDB Access Denied**
   - Verify IAM role has correct permissions
   - Check resource-based policies

4. **404 Errors**
   - Verify API Gateway resource paths
   - Check S3 bucket website hosting configuration

## 🔄 Future Enhancements

- [ ] User authentication with AWS Cognito
- [ ] Email notifications using Amazon SES
- [ ] Letter templates and themes
- [ ] Image attachments with S3 storage
- [ ] Letter history dashboard
- [ ] Search and filter functionality
- [ ] Mobile app version
- [ ] Social media sharing integration
- [ ] Multi-language support
- [ ] Advanced analytics with CloudWatch

## 📝 License

This project is open-source and available under the MIT License.

## 👤 Author

**Waliul Rayhan**

- GitHub: [@waliulrayhan](https://github.com/waliulrayhan)
- Repository: [Serverless-Web-Application-on-AWS](https://github.com/waliulrayhan/Serverless-Web-Application-on-AWS)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/waliulrayhan/Serverless-Web-Application-on-AWS/issues).

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- AWS Documentation for comprehensive guides
- Google Fonts for beautiful typography
- The serverless community for best practices
- All contributors and users of Digital Chitthi

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the repository owner.

---

**Made with ❤️ using AWS Serverless Technologies**
