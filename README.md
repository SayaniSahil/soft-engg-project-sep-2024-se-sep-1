<h1>
<img src="frontend-1\src\assets\logo.jpeg" width="30" style="border-radius:50%; vertical-align:middle; margin-bottom:5px; border:1px solid #ddd"/> 
Trackie
</h1>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive project management and tracking platform designed for academic and collaborative environments. Track project milestones, student submissions, GitHub commits, and get AI-powered insights using LLM integration.

## Table of Contents

- [What the Project Does](#what-the-project-does)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Support & Resources](#support--resources)
- [Maintainers](#maintainers)
- [License](#license)

## What the Project Does

Trackie is a full-stack web application that enables instructors and students to collaboratively manage project workflows. It provides a centralized platform for:

- **Project Management**: Create and organize projects with detailed descriptions
- **Milestone Tracking**: Define project milestones with dates, weightage, and submission tracking
- **GitHub Integration**: Monitor student commits and project progress via GitHub repositories
- **Progress Analytics**: View comprehensive statistics on project completion, student performance, and milestone progress
- **AI-Powered Insights**: Leverage LLM integration for intelligent project analysis and recommendations
- **Role-Based Access**: Separate dashboards for students, instructors, and administrators

## Key Features

### For Instructors

- Create and manage projects with multiple milestones
- Track student submissions and progress
- Monitor GitHub commit history for each student
- View detailed project statistics and milestone completion rates
- Access admin dashboards for comprehensive analytics

### For Students

- View assigned projects and their milestones
- Submit work for milestones with deadline tracking
- Link GitHub repositories for automatic commit tracking
- Monitor personal progress against project milestones

### General Features

- **Authentication**: Secure user authentication with role-based access control
- **Real-time Caching**: Redis-backed caching for optimized performance
- **Scalable Database**: SQLite (development) with SQLAlchemy ORM for easy migration
- **REST API**: Comprehensive API endpoints for all operations
- **Responsive UI**: Modern Vue 3 + TypeScript frontend with Bootstrap styling

## Getting Started

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and npm (for frontend)
- **Redis** (for caching - optional for development)
- **Git** (for version control)

### Installation

#### Backend Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/SayaniSahil/soft-engg-project-sep-2024-se-sep-1.git
   cd soft-engg-project-sep-2024-se-sep-1
   ```

2. **Set up Python virtual environment**

   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**
   - Edit `config.py` to adjust database URI and cache settings
   - Ensure Redis is running (if using cache in production)

#### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd ../frontend-1
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

### Running the Application

#### Start the Backend Server

```bash
cd backend
python -m flask run
```

The backend server runs on `http://localhost:5000` by default.

#### Start the Frontend Development Server

```bash
cd frontend-1
npm run dev
```

The frontend runs on `http://localhost:5173` by default.

#### Build for Production

```bash
# Frontend production build
cd frontend-1
npm run build
```

## Architecture

### Backend Stack

- **Framework**: Flask 3.0.3
- **Authentication**: Flask-Security-Too, Flask-Login, Flask-Bcrypt
- **Database**: SQLAlchemy with SQLite
- **Caching**: Flask-Caching with Redis
- **API Features**: CORS support, RESTful endpoints
- **LLM Integration**: AI-powered insights and analysis

### Frontend Stack

- **Framework**: Vue 3
- **Language**: TypeScript
- **Build Tool**: Vite
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js for analytics visualization
- **Routing**: Vue Router 4

### Key Components

**Backend Components** (`backend/components/`)

- `authentication.py` - User authentication and authorization
- `project.py` - Project management
- `submission.py` - Student submission handling
- `milestones.py` - Milestone tracking and management
- `student.py` - Student information and management
- `commit_history.py` - GitHub commit tracking
- `llm.py` - LLM integration for insights
- `admin_stats.py` - Admin dashboard and statistics
- `github_url.py` - GitHub repository integration

**Frontend Components** (`frontend-1/src/components/`)

- `NavBar.vue` - Application navigation
- `ProjectList.vue` - Project listing and management
- `MilestoneList.vue` - Milestone tracking interface
- `StudentList.vue` - Student information display
- `Statistics.vue` - Analytics and progress visualization
- `ProgressComponent.vue` - Progress tracking UI

**Views** (`frontend-1/src/views/`)

- `Login.vue` / `Register.vue` - Authentication pages
- `StudentDashboard.vue` - Student dashboard
- `InstructorDashboard.vue` - Instructor dashboard
- `AdminDashboard.vue` - Admin dashboard
- `AdminProjectStats.vue` - Detailed project statistics

## API Documentation

The backend provides RESTful API endpoints for:

- **Authentication**: User registration, login, token management
- **Projects**: CRUD operations for projects
- **Milestones**: Milestone creation, tracking, and submissions
- **Submissions**: Student submission management
- **Statistics**: Project and milestone analytics
- **GitHub Integration**: Commit history and repository management
- **Admin Operations**: User management, system statistics

For detailed API specifications, refer to component files in `backend/components/routes.py`.

## Testing

Run the test suite to validate functionality:

```bash
cd backend
pytest tests/
```

Test files are located in `backend/tests/` directory covering:

- Student management
- Project tracking
- Milestone submissions
- GitHub URL handling
- LLM integration
- Commit history retrieval

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

For detailed contribution guidelines, please see [CONTRIBUTING.md](CONTRIBUTING.md) (if available).

## Support & Resources

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/SayaniSahil/soft-engg-project-sep-2024-se-sep-1/issues)
- **Documentation**: Review component documentation in code comments
- **Architecture**: See `ERDDiagram1.svg` and `Main.svg` for system architecture

## Maintainers

This project was developed as part of the **IIT Madras BS in Data Science and Applications** program.

**Current Maintainers**: SayaniSahil and contributors

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated**: December 2024
**Project Status**: Active Development
