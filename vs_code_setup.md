# SmartTransportAI - VS Code Setup Guide

This guide provides detailed instructions for setting up and developing the SmartTransportAI project in Visual Studio Code.

## Prerequisites

1. **Visual Studio Code**: Download and install from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. **Python 3.11+**: Install from [https://www.python.org/downloads/](https://www.python.org/downloads/)
3. **Git**: Install from [https://git-scm.com/downloads](https://git-scm.com/downloads)

## Required VS Code Extensions

Install the following extensions for optimal development experience:

- **Python** (Microsoft): Python language support
- **Pylance** (Microsoft): Python language server with type checking
- **Python Docstring Generator** (Nils Werner): Generate docstrings automatically
- **Jupyter** (Microsoft): Support for Jupyter notebooks
- **Prettier** (Prettier): Code formatter
- **GitLens** (GitKraken): Git integration
- **indent-rainbow** (oderwat): Makes indentation more readable
- **Streamlit Snippets** (sachaCR): Streamlit code snippets

## Project Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SmartTransportAI
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and configuration

## Running the Application

1. **Using VS Code Run Configuration**:
   - Open the Run/Debug view (Ctrl+Shift+D or Cmd+Shift+D)
   - Select "Streamlit: Run App" from the dropdown
   - Click the Play button

2. **Using Terminal**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Development Workflow

1. **Directory Structure**:
   - `app.py`: Main application entry point
   - `SmartTransportAI/`: Core application modules
   - `models/`: Data models and ML components
   - `api/`: External API integrations
   - `data/`: Data storage and processing
   - `utils/`: Utility functions and helpers
   - `tests/`: Test cases
   - `config/`: Configuration files

2. **Branching Strategy**:
   - `main`: Production-ready code
   - `dev`: Development branch
   - Feature branches: `feature/feature-name`
   - Bug fixes: `fix/bug-description`

3. **Code Style**:
   - Follow PEP 8 guidelines
   - Use docstrings for all functions and classes
   - Format code with autopep8 before committing

## Testing

1. **Running Tests**:
   - Use VS Code Test Explorer or
   - Terminal: `pytest tests/`

2. **Adding Tests**:
   - Create test files in the `tests/` directory
   - Name test files with `test_` prefix

## Deployment

1. **Local Development**:
   - Run Streamlit locally using VS Code configuration

2. **Production Deployment**:
   - Follow the deployment guide in `deployment.md`

## Troubleshooting

1. **Common Issues**:
   - **Module not found**: Ensure your virtual environment is activated
   - **API errors**: Check `.env` file for correct API keys
   - **Port already in use**: Change the port in `launch.json`

2. **Debugging**:
   - Use VS Code's debugging tools (F5)
   - Check logs in the `logs/` directory

## Additional Resources

- Streamlit Documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)
- VS Code Python Tutorial: [https://code.visualstudio.com/docs/python/python-tutorial](https://code.visualstudio.com/docs/python/python-tutorial)