# Contributing to EchoStory

Thank you for your interest in contributing to EchoStory! This project aims to help children with autism tell their stories through multimodal AI interaction.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize accessibility and user safety
- Keep the low-demand philosophy at the core

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Open an issue with tag `enhancement`
2. Describe the feature and its benefits
3. Consider how it aligns with low-demand principles
4. Discuss implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow existing code style
   - Add comments for complex logic
   - Write TypeScript types (frontend)
   - Add type hints (backend)

4. **Test your changes**:
   - Test locally with `docker-compose up`
   - Verify WebSocket connections
   - Test voice and vision features
   - Check error handling

5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add new emotion detection"
   ```

6. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

See [QUICKSTART.md](./QUICKSTART.md) for detailed setup instructions.

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Coding Standards

### Python (Backend)
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use async/await for I/O operations

### TypeScript (Frontend)
- Use TypeScript strict mode
- Define interfaces for props
- Use functional components
- Follow React hooks best practices

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Accessibility Guidelines

- Maintain sensory-friendly colors
- Keep animations smooth and non-jarring
- Support keyboard navigation
- Provide clear error messages
- Test with screen readers

## Responsible AI Principles

- Never pressure users for responses
- Validate all inputs positively
- Filter generated content for safety
- Respect privacy and data minimization
- Be transparent about AI limitations

## Pull Request Process

1. Update README if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Questions?

Open an issue or reach out to the maintainers.

Thank you for helping make EchoStory better! ✨
