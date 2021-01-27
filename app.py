{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Imports\n",
    "import numpy as np\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "from flask import Flask, jsonify\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Database Setup\n",
    "engine = create_engine(\"sqlite:///hawaii1.sqlite\", echo=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['measurement', 'station']"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "Base.classes.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save reference to the table\n",
    "measurement = Base.classes.measurement\n",
    "station = Base.classes.station\n",
    "\n",
    "#create session\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flask Setup\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create routes for homepage, prcp, stations, tobs, start/start-end\n",
    "#Homepage:\n",
    "@app.route(\"/\")\n",
    "def homepage():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"/api/v1.0/<start>/<end>\"\n",
    "    ) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def prcp():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "    \n",
    "    # Query\n",
    "    results = session.query(measurement.date, measurement.prcp).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Create a dictionary from the row data and append to a list of all_passengers\n",
    "    date_prcp_dict = []\n",
    "    for date, prcp in results:\n",
    "        dpdict = {}\n",
    "        dpdict[\"precipitation\"] = prcp\n",
    "        dpdict[\"date\"] = date\n",
    "        date_prcp_dict.append(dpdict)\n",
    "\n",
    "    return jsonify(date_prcp_dict)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "\n",
    "    # Query \n",
    "    results = session.query(measurement.station).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    all_stations = list(np.ravel(results))\n",
    "\n",
    "    return jsonify(all_stations)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    # Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "   \n",
    "    # Query all passengers\n",
    "    results = session.query(measurement.date, measurement.tobs).\\\n",
    "    filter(measurement.date >= '2016-08-23').\\\n",
    "    filter(measurement.station == 'USC00519397').all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    lastyr = list(np.ravel(results))\n",
    "\n",
    "    return jsonify(lastyr)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/start/<start>\")\n",
    "def start(start):\n",
    "# Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "   \n",
    "    # Query all passengers\n",
    "    results = session.query(measurement.date, measurement.tobs).\\\n",
    "    filter(measurement.date >= start).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    oldf = pd.DataFrame(results[:], columns=['date', 'tobs'])\n",
    "    oldf.set_index('date', inplace=True, )\n",
    "    newwdf = oldf.dropna()\n",
    "    mean = newwdf['tobs'].mean()\n",
    "    lowest = newwdf['tobs'].min()\n",
    "    highest = newwdf['tobs'].max()\n",
    "    summs = [mean, lowest, highest]\n",
    "    stats = list(np.ravel(summs))\n",
    "\n",
    "    return jsonify(stats)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/start_end/<start>/<end>\")\n",
    "def start_end(start, end):\n",
    "# Create our session (link) from Python to the DB\n",
    "    session = Session(engine)\n",
    "\n",
    "   \n",
    "    # Query all passengers\n",
    "    results = session.query(measurement.date, measurement.tobs).\\\n",
    "    filter(measurement.date >= start, measurement.date <= end).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    # Convert list of tuples into normal list\n",
    "    oldf = pd.DataFrame(results[:], columns=['date', 'tobs'])\n",
    "    oldf.set_index('date', inplace=True, )\n",
    "    newwwdf = oldf.dropna()\n",
    "    mean = newwwdf['tobs'].mean()\n",
    "    lowest = newwwdf['tobs'].min()\n",
    "    highest = newwwdf['tobs'].max()\n",
    "    summs = [mean, lowest, highest]\n",
    "    stats = list(np.ravel(summs))\n",
    "\n",
    "    return jsonify(stats)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.debug = False\n",
    "    app.run()\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}