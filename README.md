# sqlalchemy-challenge
Submission for Challenge 10 - SQLAlchemy

## Climate Data Preparation
- Data was prepared according to challenge instructions.
- Code is included at the start of the jupyter notebooked titled 'climate_stater.ipynb'.
- Data is sourced from: 'Resources/hawaii.sqlite'.
## Precipitation Analysis
- Analysis is included in the jupyter notebooked titled 'climate_stater.ipynb' under the header 'Exploratory Precipitation Analysis'.
- Note that the query that collects the date and precipitation for the last year of data passes the most recent date as a variable, using the method datetime.strptime to pass the 'year', 'month' and 'day' to the date interval formula (variable 'year_back').
## Climate App
- App is included in the file 'app.py'.
- App includes the following four routes, with data sourced from 'Resources/hawaii.sqlite':
1. /api/v1.0/precipitation
2. /api/v1.0/stations
3. /api/v1.0/tobs
4. /api/v1.0/temp/start
5. /api/v1.0/temp/start/end
