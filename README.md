# MathFlow Backend

A powerful FastAPI-based backend service that breaks down mathematical solutions into digestible steps and provides interactive visualizations using Plotly.js graphs.

## 🚀 Features

- **Solution Step Breaking**: Automatically breaks complex mathematical solutions into 3-7 logical main steps
- **Sub-step Analysis**: Provides detailed explanations for individual steps with mathematical theory and background
- **Interactive Graphs**: Generates contextual Plotly.js graphs based on mathematical content
- **AI-Powered**: Uses Google's Gemini 2.0 Flash model for intelligent mathematical analysis
- **LaTeX Support**: Full LaTeX rendering support for mathematical expressions
- **CORS Enabled**: Ready for frontend integration

## 📊 Graph Types

The system intelligently detects mathematical content and generates appropriate visualizations:

- **Quadratic Functions**: Parabolas and vertex forms
- **Trigonometric Functions**: Sine, cosine, and tangent waves
- **Exponential/Logarithmic**: Growth and decay functions
- **Linear Functions**: Lines and systems of equations
- **Calculus**: Functions with their derivatives
- **Statistics**: Normal distributions and sample data
- **Default**: Common mathematical functions overview

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with language models
- **LangGraph**: Advanced workflow orchestration
- **Google Gemini 2.0**: State-of-the-art AI model for mathematical reasoning
- **NumPy**: Numerical computing for graph generation
- **SymPy**: Symbolic mathematics library
- **Plotly**: Interactive graphing library

## 📋 Prerequisites

- Python 3.8+
- Google API Key for Gemini
- pip package manager

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/debjit-1004/MathFlow-Backend.git
   cd MathFlow-Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**
   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at `http://localhost:8000`

## 📚 API Documentation

### 1. Split Solution into Main Steps

**Endpoint**: `POST /split-solution`

Breaks a mathematical solution into main logical steps and provides a relevant graph.

**Request Body**:
```json
{
  "solution": "Solve the quadratic equation x² - 5x + 6 = 0 using the quadratic formula..."
}
```

**Response**:
```json
{
  "steps": [
    {
      "math": "$$ax^2 + bx + c = 0$$",
      "explanation": "Identify the standard form where a=1, b=-5, c=6"
    },
    {
      "math": "$$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$$",
      "explanation": "Apply the quadratic formula"
    }
  ],
  "graph": {
    "data": [...],
    "layout": {...}
  }
}
```

### 2. Split Step into Sub-steps

**Endpoint**: `POST /split-step`

Provides detailed conceptual explanation for a specific mathematical step.

**Request Body**:
```json
{
  "step": "Apply the quadratic formula to find the roots"
}
```

**Response**:
```json
{
  "substeps": [
    {
      "math": "$$\\Delta = b^2 - 4ac$$",
      "explanation": "The discriminant determines the nature of roots..."
    }
  ]
}
```

## 🧪 Example Usage

### Using curl

```bash
# Split a solution
curl -X POST "http://localhost:8000/split-solution" \
  -H "Content-Type: application/json" \
  -d '{"solution": "Find the derivative of f(x) = x³ + 2x² - x + 1"}'

# Get detailed step explanation
curl -X POST "http://localhost:8000/split-step" \
  -H "Content-Type: application/json" \
  -d '{"step": "Apply the power rule to each term"}'
```

### Frontend Integration

```javascript
// Split solution and get graph data
const response = await fetch('/split-solution', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    solution: "Solve the equation 2x + 5 = 13"
  })
});

const { steps, graph } = await response.json();

// Use Plotly.js to render the graph
Plotly.newPlot('graph-container', graph.data, graph.layout);
```

## 🏗️ Project Structure

```
MathFlow-Backend/
├── app.py              # FastAPI application and routes
├── chain.py            # Core logic for step breaking and graph generation
├── prompts.py          # LangChain prompt templates
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini models

### Model Settings

The Gemini model is configured with:
- **Model**: `gemini-2.0-flash`
- **Temperature**: `0.2` (for consistent mathematical reasoning)

## 🚀 Deployment

### Local Development
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Consider using a process manager like:
- **Gunicorn**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app`
- **Docker**: Create a Dockerfile for containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Google API Key Error**
   - Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
   - Check that the Gemini API is enabled in your Google Cloud Console

2. **Module Import Error**
   - Run `pip install -r requirements.txt` to install all dependencies
   - Ensure you're using Python 3.8+

3. **CORS Issues**
   - The current configuration allows all origins (`*`)
   - In production, update the CORS middleware to only allow your frontend domain

4. **Graph Generation Issues**
   - Ensure NumPy and SymPy are properly installed
   - Check that the mathematical content is properly formatted

## 🔮 Future Enhancements

- [ ] Support for more graph types (3D plots, complex functions)
- [ ] Integration with additional AI models
- [ ] Caching mechanism for improved performance
- [ ] WebSocket support for real-time step generation
- [ ] Support for multiple mathematical notation formats
- [ ] Advanced error handling and validation
- [ ] Rate limiting and authentication

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the maintainer: [debjit-1004](https://github.com/debjit-1004)

---

**Made with ❤️ for mathematics education**
