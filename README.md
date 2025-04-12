# 🚀 ALX Connect Hub

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.68+-green.svg" alt="FastAPI Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</div>

<br>

A cutting-edge mentor matching and interview coaching platform powered by modern AI technologies. ALX Connect Hub revolutionizes the way mentors and mentees connect, learn, and grow together.

## ✨ Features

### 🤝 Intelligent Mentor Matching
- **Experience-based Pairing**: Smart algorithms that consider years of experience
- **Domain Expertise Matching**: Precise matching based on industry domains
- **Skill Alignment**: Advanced skill matching using semantic analysis
- **Compatibility Scoring**: Multi-factor scoring system for optimal matches

### 🎯 AI-Powered Interview Coaching
- **Real-time Chat Interface**: Seamless communication with AI coach
- **Context-Aware Responses**: Intelligent conversation flow
- **Industry-Specific Guidance**: Tailored advice for different sectors
- **Progress Tracking**: Monitor your interview preparation journey

### 📄 Resume Analysis
- **Automated Review**: Instant feedback on your resume
- **Skill Extraction**: Identify and highlight key competencies
- **Experience Analysis**: Detailed breakdown of work history
- **Improvement Suggestions**: Actionable recommendations

## 🛠️ Tech Stack

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
        <br>Backend Framework
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
        <br>Programming Language
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/LangChain-FF6B6B?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
        <br>AI Framework
      </td>
    </tr>
    <tr>
      <td align="center">
        <img src="https://img.shields.io/badge/Groq-00A67E?style=for-the-badge&logo=groq&logoColor=white" alt="Groq">
        <br>LLM Provider
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/FAISS-FFD700?style=for-the-badge&logo=faiss&logoColor=black" alt="FAISS">
        <br>Vector Database
      </td>
      <td align="center">
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
        <br>Containerization
      </td>
    </tr>
  </table>
</div>

## 📦 Project Structure

```
alx_connect/
├── api/
│   ├── __init__.py
│   └── routes.py           # API endpoints and route handlers
├── models/
│   ├── __init__.py
│   ├── profile.py          # Profile data models
│   └── chat.py             # Chat and conversation models
├── services/
│   ├── __init__.py
│   ├── matching.py         # Mentor matching service
│   └── interview_coach.py  # Interview coaching service
├── config/
│   ├── __init__.py
│   └── config.py           # Application configuration
├── main.py                 # Application entry point
├── pyproject.toml          # Project dependencies and metadata
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker (optional)
- Groq API key

### Installation

#### Using pip
```bash
# Clone the repository
git clone https://github.com/yourusername/alx-connect.git
cd alx-connect

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

#### Using Docker
```bash
# Build the Docker image
docker build -t alx-connect .

# Run the container
docker run -p 8000:8000 alx-connect
```

### Configuration

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/mentor-matching/` | POST | Match mentors and mentees |
| `/api/v1/ask-question/` | POST | Get interview coaching |
| `/api/v1/ws/chat/{conversation_id}` | WS | Real-time chat |
| `/api/v1/generate_summary` | POST | Generate resume summary |

## 🛠️ Development

### Code Style
This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

```bash
# Format code
black .
isort .

# Run linter
flake8
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=alx_connect
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **ALX Connect Team** - *Initial work* - [ALX Connect](https://github.com/yourusername)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the ALX community for their support and feedback
```

This README provides clear, structured information for users to understand and utilize each endpoint.