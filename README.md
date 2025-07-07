# ⚽ Talaganchester United

A modern web application for calculating team averages for football/soccer players. Built with Vite and vanilla JavaScript.

## Features

- **Team Management**: View and manage two teams (Equipo 1 Negro and Equipo 2 Rojo)
- **Player Ratings**: Display player ratings and calculate team averages automatically
- **New Players**: Add new players (Erik, Riky, Diego) to teams
- **Interactive Form**: Add additional players with custom ratings and positions
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with hover effects and smooth transitions

## Teams

### Equipo 1 (Negro)
- Nel: 8.8
- Willians: 8.6
- J. aguila: 8.1
- Marco: 6.3
- Pancho: 6.0
- Camilo: 5.2
- **Average: 7.17**

### Equipo 2 (Rojo)
- Luisito: 7.5
- Francisco H: 8.0
- Enrique: 8.0
- P. Lamilladonna: 7.0
- Iván: 7.5
- Maxi Vargas: 5.5
- **Average: 7.25**

### New Players
- **Erik**: 9.0 (Creador)
- **Riky**: 9.2 (Atacante)
- **Diego**: 7.8 (Mediocampo)

## Getting Started

### Prerequisites
- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## Usage

1. **View Teams**: See both teams with their current players and averages
2. **Assign New Players**: Use the dropdown menus to assign Erik, Riky, and Diego to teams
3. **Update Averages**: Click "Update Team Averages" to recalculate with new players
4. **Add Custom Players**: Use the form at the bottom to add more players

## Project Structure

```
fulito/
├── index.html          # Main HTML file
├── main.js            # Application logic
├── style.css          # Styles and design
├── vite.config.js     # Vite configuration
├── package.json       # Dependencies and scripts
└── README.md         # This file
```

## Technologies Used

- **Vite**: Fast build tool and development server
- **Vanilla JavaScript**: Pure JavaScript without frameworks
- **CSS3**: Modern styling with custom properties and grid layout
- **HTML5**: Semantic markup

## Development

To contribute to this project:

1. Make your changes
2. Test locally with `npm run dev`
3. Build for production with `npm run build`
4. Ensure all features work correctly

## License

This project is for educational and personal use.

## Deployment to Azure

### Prerequisites for Azure Deployment
- Azure account (free tier available)
- GitHub account
- Node.js installed locally

### Option 1: Azure Static Web Apps (Recommended)

1. **Push to GitHub** (see commands below)
2. **Create Azure Static Web App**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Static Web Apps" and click "Create"
   - Connect your GitHub repository
   - Configure build settings:
     - App location: `/`
     - Build location: `dist`
     - Build preset: Custom
     - Build command: `npm run build`
     - Output location: `dist`

3. **Automatic deployment**: Azure will automatically deploy when you push to your main branch

### Option 2: Manual Upload to Azure Blob Storage

1. Build the project locally: `npm run build`
2. Create Azure Storage Account with static website hosting enabled
3. Upload contents of `dist` folder to `$web` container

### GitHub Commands

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit - Talaganchester United app"

# Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/Camiiloh/talaganchester-united.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Live URL
Once deployed, your app will be available at: `https://your-app-name.azurestaticapps.net`
