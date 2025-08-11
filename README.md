# Instagram Auto Post

A FastAPI-based service for automated Instagram posting using the Facebook Graph API. This service provides endpoints to schedule and publish images and reels to Instagram.

## Features

- 📸 Post images to Instagram
- 🎥 Post reels/videos to Instagram  
- ⏰ Schedule posts for later publication
- 🔄 RESTful API with FastAPI
- 📖 Auto-generated API documentation
- 🚀 Easy deployment to Render
- 🔐 Secure environment variable management

## Setup

### Prerequisites

- Python 3.11+
- Instagram Business or Creator Account
- Facebook App with Instagram Graph API access
- Meta Business Account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/utsavmonpara/instagram-auto-post.git
   cd instagram-auto-post
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Environment Variables

Configure these environment variables in your `.env` file:

| Variable | Description | Required |
|----------|-------------|----------|
| `IG_APP_ID` | Your Instagram App ID from Facebook Developers | ✅ |
| `IG_APP_SECRET` | Your Instagram App Secret from Facebook Developers | ✅ |
| `IG_USER_ID` | Your Instagram Business Account User ID | ✅ |
| `IG_ACCESS_TOKEN` | Long-lived Instagram User Access Token | ✅ |
| `IG_PAGE_ID` | Your Facebook Page ID connected to Instagram | ✅ |
| `PORT` | Port number for the server (default: 8000) | ❌ |
| `ENVIRONMENT` | Environment (development/production) | ❌ |

### Getting Instagram API Credentials

1. **Create a Facebook App**
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create a new app with Instagram Graph API product

2. **Get User Access Token**
   - Use Graph API Explorer to generate a long-lived token
   - Required scopes: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`

3. **Get Instagram Business Account ID**
   - Use Graph API: `GET /{page-id}?fields=instagram_business_account`

## API Endpoints

### Health Check
```http
GET /health
```

### Schedule Post
```http
POST /schedule
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "caption": "Your post caption #hashtags",
  "scheduled_time": "2024-01-01T12:00:00Z" // Optional
}
```

### Root Endpoint
```http
GET /
```

## Instagram API Limitations

⚠️ **Important Limitations to be aware of:**

### Content Requirements
- **Images**: JPEG format, max 8MB, min 320px width
- **Videos**: MP4 format, max 100MB, 3-60 seconds duration
- **Aspect Ratios**: Square (1:1), Portrait (4:5), Landscape (1.91:1)

### Rate Limits
- **200 requests per hour** per app
- **25 posts per day** per Instagram account
- Rate limits reset every hour

### Account Requirements
- Must be an **Instagram Business or Creator Account**
- Account must be connected to a **Facebook Page**
- Requires **Instagram Graph API** permissions

### Content Restrictions
- No copyrighted content
- Follow Instagram Community Guidelines
- Some content may require manual review
- Scheduled posts are limited to 75 per account

### API Access
- Requires **App Review** for production use
- Development mode limited to app developers/testers
- Access tokens expire and need renewal

## Deployment

### Deploy to Render

1. **Connect Repository**
   - Fork this repository
   - Connect your GitHub account to Render
   - Create a new Web Service from your fork

2. **Configure Environment**
   - Set all required environment variables in Render dashboard
   - Use the provided `render.yaml` for automatic configuration

3. **Deploy**
   - Render will automatically deploy on push to main branch
   - GitHub Actions workflow will run tests and trigger deployment

### Manual Deployment

1. **Build the application**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### GitHub Actions

The repository includes a CI/CD workflow that:
- Runs on push to main branch
- Installs dependencies
- Runs tests (when available)
- Triggers deployment to Render

## Development

### Project Structure
```
instagram-auto-post/
├── main.py                 # FastAPI application
├── instagram_client.py     # Instagram Graph API client
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── render.yaml            # Render deployment config
├── .github/workflows/     # GitHub Actions
│   └── deploy.yml         # Deployment workflow
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore            # Git ignore rules
```

### Adding Features

1. Extend `instagram_client.py` for new Instagram API features
2. Add new endpoints in `main.py`
3. Update requirements.txt if adding new dependencies
4. Add tests for new functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api/)
- 🚀 [Render Documentation](https://render.com/docs)
- ⚡ [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Disclaimer

This tool is for educational and development purposes. Make sure to comply with Instagram's Terms of Service and API usage policies. The developers are not responsible for any misuse or violations.
