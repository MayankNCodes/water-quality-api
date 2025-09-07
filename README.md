# Water Quality Analysis API

A Django REST API for analyzing water quality samples with heavy metal concentrations and generating comprehensive PDF reports.

## Features

- ✅ Store water quality samples with heavy metal concentrations
- ✅ Automatic calculation of 7 water quality indices (HMPI, HPI, HEI, HCI, Cd, PI, PLI)
- ✅ Generate professional PDF reports with location data
- ✅ RESTful API endpoints
- ✅ Admin interface for data management
- ✅ Ready for cloud deployment (Railway, Render, Heroku)

## Quick Deploy

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/django)

### Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## API Endpoints

- `POST /api/water-quality/samples/` - Create new water quality sample
- `GET /api/water-quality/samples/` - List all samples  
- `GET /api/water-quality/samples/{sample_id}/` - Get specific sample
- `GET /api/water-quality/samples/{sample_id}/pdf/` - Download PDF report
- `GET /api/water-quality/samples/{sample_id}/indices/` - Get calculated indices only
- `POST /api/water-quality/create-and-report/` - Create sample and get PDF in one request

## Sample Request

```json
POST /api/water-quality/samples/
{
    "sample_id": "WQ001",
    "sampling_date": "2024-01-15",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "well_depth": 150.5,
    "lead": 0.02,
    "cadmium": 0.005,
    "chromium": 0.08,
    "arsenic": 0.015,
    "mercury": 0.001,
    "nickel": 0.03,
    "copper": 1.2,
    "zinc": 2.5,
    "iron": 0.45,
    "manganese": 0.25,
    "cobalt": 0.02
}
```

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd water-quality-api
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Environment Variables

- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `DATABASE_URL` - Database connection string (automatically configured on most platforms)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Water Quality Indices

The API automatically calculates these indices based on WHO/EPA standards:

- **HMPI** (Heavy Metal Pollution Index): Overall pollution level
- **HPI** (Health Risk Index): Health impact assessment  
- **HEI** (Heavy Metal Evaluation Index): Environmental evaluation
- **HCI** (Heavy Metal Contamination Index): Contamination level
- **Cd** (Contamination Degree): Degree of contamination
- **PI** (Pollution Index): Maximum pollution indicator
- **PLI** (Pollution Load Index): Overall pollution load

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
