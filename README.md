# 🧹 Smart Cleaning AI

An intelligent cleaning service platform powered by AI, built with FastAPI and LangChain. This system provides automated cleaning professional matching, intelligent scheduling, dynamic pricing, and AI-powered customer support.
<img width="1905" height="909" alt="image" src="https://github.com/user-attachments/assets/b269b630-1316-4d44-8862-76dff50c330f" />

## ✨ Features

- **🤖 AI Chatbot**: Intelligent customer support using OpenAI GPT models with conversation history
- **👥 Smart Matching**: Automatically matches customers with the best cleaning professionals based on location, availability, and ratings
- **📅 Intelligent Scheduling**: Dynamic scheduling system that prevents conflicts and optimizes worker availability
- **💰 Dynamic Pricing**: AI-powered pricing based on service type, area size, frequency, and urgency
- **🔄 RESTful API**: Clean and well-documented API endpoints for all operations

## 🚀 Tech Stack

- **Backend Framework**: FastAPI
- **AI/ML**: 
  - LangChain
  - OpenAI GPT-4
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Environment Management**: Python dotenv
- **API Documentation**: Swagger UI (auto-generated)

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API Key
- Git

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/riponalmamun/Smart_Cleaning-_AI.git
cd Smart_Cleaning-_AI
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔌 API Endpoints

### Matching Service
- `POST /match/find-professionals` - Find suitable cleaning professionals

### Scheduling Service
- `POST /schedule/book` - Book a cleaning appointment
- `GET /schedule/availability/{professional_id}` - Check professional availability

### Pricing Service
- `POST /pricing/calculate` - Calculate service pricing
- `POST /pricing/quote` - Get detailed quote

### Chatbot Service
- `POST /chatbot/chat` - Interact with AI assistant

## 💡 Usage Examples

### Calculate Pricing

```python
import requests

url = "http://127.0.0.1:8000/pricing/calculate"
data = {
    "service_type": "deep_cleaning",
    "area_sqft": 1500,
    "frequency": "weekly",
    "urgency": "standard"
}

response = requests.post(url, json=data)
print(response.json())
```

### Find Professionals

```python
import requests

url = "http://127.0.0.1:8000/match/find-professionals"
data = {
    "location": "Dhaka",
    "service_type": "regular_cleaning",
    "datetime": "2024-12-15T10:00:00"
}

response = requests.post(url, json=data)
print(response.json())
```

### Chat with AI

```python
import requests

url = "http://127.0.0.1:8000/chatbot/chat"
data = {
    "user_email": "customer@example.com",
    "user_message": "What cleaning services do you offer?"
}

response = requests.post(url, json=data)
print(response.json())
```

## 📁 Project Structure

```
smart_cleaning_ai/
├── main.py                 # Application entry point
├── routers/               # API route handlers
│   ├── chatbot.py         # Chatbot endpoints
│   ├── matching.py        # Matching endpoints
│   ├── pricing.py         # Pricing endpoints
│   └── scheduling.py      # Scheduling endpoints
├── services/              # Business logic
│   ├── chat_service.py    # AI chat service
│   ├── conversation_service.py
│   ├── prediction_service.py
│   └── route_service.py
├── schemas/               # Pydantic models
│   └── models.py
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables (not in repo)
```

## 🔐 Security

- Never commit `.env` file or API keys
- Use environment variables for sensitive data
- API key authentication recommended for production
- Input validation on all endpoints

## 🚧 Future Enhancements

- [ ] User authentication and authorization
- [ ] Payment gateway integration
- [ ] Real-time notifications
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Review and rating system
- [ ] Image upload for service requests

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ripon Al Mamun**

- GitHub: [@riponalmamun](https://github.com/riponalmamun)
- Project Link: [https://github.com/riponalmamun/Smart_Cleaning-_AI](https://github.com/riponalmamun/Smart_Cleaning-_AI)

## 🙏 Acknowledgments

- OpenAI for GPT models
- FastAPI framework
- LangChain community
- All contributors and users

## 📞 Support

For support, email riponalmamunrasel@gmail.com or open an issue in the GitHub repository.

---

⭐ Star this repo if you find it helpful!
