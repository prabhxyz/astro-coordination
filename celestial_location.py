import datetime
import numpy as np
import requests
import urllib.parse

# Get the current date and time
currentDateAndTime = datetime.datetime.now()
year=currentDateAndTime.year
month=currentDateAndTime.month
day=currentDateAndTime.day
hour=currentDateAndTime.hour
minute=currentDateAndTime.minute
second=currentDateAndTime.second
longitude=-0
latitude=0

# Set the longitude and latitude of the location (Normally)
location = input("Observer Location (Address): ")
def lonlat(address):
    global longitude
    global latitude
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    longitude = float(response[0]["lon"])
    latitude = float(response[0]["lat"])
lonlat(location)

def calculate_lst(longitude: float, date: datetime.date, time: datetime.time) -> datetime.time:
    # Convert the date and time to a datetime object
    dt = datetime.datetime.combine(date, time)
    # Convert the datetime object to UTC
    dt_utc = dt.astimezone(datetime.timezone.utc)
    # Calculate the number of days since J2000
    jd = 367 * dt_utc.year - int((7 * (dt_utc.year + int((dt_utc.month + 9) / 12))) / 4) + int((275 * dt_utc.month) / 9) + dt_utc.day - 730530
    # Calculate the Greenwich mean sidereal time (GMST) in hours
    gmst = 6.697375 + 0.0657098242 * jd + dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    # Shift GMST to LST using the local longitude
    lst = gmst + longitude / 15 
    # Normalize LST to the range [0, 24)
    lst = lst % 24
    # Convert LST to a time object, used for debugging purposes
    lst_time = datetime.time(hour=int(lst), minute=int((lst - int(lst)) * 60), second=int((((lst - int(lst)) * 60) - int((lst - int(lst)) * 60)) * 60))
    return lst

# Dictionary of RA and Dec for constellations
ra_dict = {
    "Andromeda": "00h 43m 31s",
    "Antlia": "10h 00m 35s",
    "Apus": "16h 01m 14s",
    "Aquarius": "22h 26m 57s",
    "Aquila": "19h 36m 15s",
    "Ara": "17h 17m 54s",
    "Aries": "02h 39m 30s",
    "Auriga": "05h 54m 23s",
    "Bootes": "14h 37m 39s",
    "Caelum": "04h 46m 16s",
    "Camelopardalis": "06h 04m 53s",
    "Cancer": "08h 37m 36s",
    "Canes Venatici": "13h 14m 23s",
    "Canis Major": "06h 54m 29s",
    "Canis Minor": "07h 36m 31s",
    "Capricornus": "21h 02m 20s",
    "Carina": "09h 14m 28s",
    "Cassiopeia": "00h 56m 24s",
    "Centaurus": "13h 09m 29s",
    "Cepheus": "22h 57m 08s",
    "Cetus": "01h 37m 15s",
    "Chamaeleon": "10h 41m 09s",
    "Circinus": "14h 45m 18s",
    "Columba": "05h 55m 44s",
    "Coma Berenices": "12h 40m 30s",
    "Corona Australis": "18h 46m 23s",
    "Corona Borealis": "15h 52m 11s",
    "Corvus": "12h 25m 40s",
    "Crater": "11h 23m 53s",
    "Crux": "12h 29m 25s",
    "Cygnus": "20h 30m 42s",
    "Delphinus": "20h 40m 30s",
    "Dorado": "05h 20m 27s",
    "Draco": "17h 02m 06s",
    "Equuleus": "21h 11m 22s",
    "Eridanus": "03h 50m 46s",
    "Fornax": "02h 50m 25s",
    "Gemini": "07h 06m 47s",
    "Grus": "22h 40m 54s",
    "Hercules": "17h 26m 58s",
    "Horologium": "03h 11m 40s",
    "Hydra": "10h 36m 00s",
    "Hydrus": "02h 04m 24s",
    "Indus": "21h 47m 40s",
    "Lacerta": "22h 33m 49s",
    "Leo": "10h 39m 11s",
    "Leo Minor": "10h 18m 35s",
    "Lepus": "05h 35m 45s",
    "Libra": "15h 17m 26s",
    "Lupus": "15h 17m 53s",
    "Lynx": "07h 57m 42s",
    "Lyra": "18h 54m 58s",
    "Mensa": "05h 17m 26s",
    "Microscopium": "20h 59m 03s",
    "Monoceros": "06h 50m 50s",
    "Musca": "12h 33m 38s",
    "Norma": "16h 07m 46s",
    "Octans": "21h 07m 06s",
    "Ophiuchus" : "17h 23m 03s",
    "Orion": "05h 37m 01s",
    "Pavo": "19h 36m 15s",
    "Pegasus" : "22h 38m 41s",
    "Perseus": "03h 23m 34s",
    "Phoenix": "00h 54m 44s",
    "Pictor": "05h 49m 32s",
    "Pisces": "00h 37m 12s",
    "Piscis Austrinus": "22h 23m 07s",
    "Puppis": "07h 38m 48s",
    "Pyxis": "08h 47m 04s",
    "Reticulum": "03h 56m 43s",
    "Sagitta": "19h 40m 41s",
    "Sagittarius": "19h 02m 31s",
    "Scorpius": "16h 52m 38s",
    "Sculptor": "00h 31m 13s",
    "Scutum": "18h 38m 53s",
    "Serpens Caput": "16h 38m 33s",
    "Serpens Cauda": "16h 38m 33s",
    "Sextans": "10h 18m 18s",
    "Taurus": "04h 32m 11s",
    "Telescopium": "19h 13m 55s",
    "Triangulum": "02h 13m 30s",
    "Triangulum Australe": "16h 03m 35s",
    "Tucana": "23h 52m 35s",
    "Ursa Major": "10h 58m 57s",
    "Ursa Minor": "15h 48m 59s",
    "Vela": "09h 19m 39s",
    "Virgo": "13h 18m 09s",
    "Volans": "07h 56m 08s",
    "Vulpecula": "20h 04m 58s"
}

dec_dict = {
    "Andromeda": "+41 00 36",
    "Antlia": "-33 58 52",
    "Apus": "-75 35 03",
    "Aquarius": "-09 59 15",
    "Aquila": "+03 22 16",
    "Ara": "-53 47 04",
    "Aries": "+21 13 02",
    "Auriga": "+39 48 10",
    "Bootes": "+30 20 38",
    "Caelum": "-39 11 28",
    "Camelopardalis": "+67 03 01",
    "Cancer": "+19 48 24",
    "Canes Venatici": "+40 01 44",
    "Canis Major": "-22 59 32",
    "Canis Minor": "+06 03 36",
    "Capricornus": "-18 18 16",
    "Carina": "-60 40 51",
    "Cassiopeia": "+61 29 33",
    "Centaurus": "-46 36 02",
    "Cepheus": "+69 13 32",
    "Cetus": "-08 25 54",
    "Chamaeleon": "-79 08 23",
    "Circinus": "-63 38 14",
    "Columba": "-35 44 19",
    "Coma Berenices": "+22 53 48",
    "Corona Australis": "-40 18 50",
    "Corona Borealis": "+32 12 59",
    "Corvus": "-18 55 27",
    "Crater": "-15 39 10",
    "Crux": "-60 09 36",
    "Cygnus": "+42 45 37",
    "Delphinus": "+13 23 31",
    "Dorado": "-62 23 49",
    "Draco": "+68 22 03",
    "Equuleus": "+07 08 29",
    "Eridanus": "-18 47 26",
    "Fornax": "-31 05 11",
    "Gemini": "+22 52 52",
    "Grus": "-44 48 14",
    "Hercules": "+27 37 02",
    "Horologium": "-53 27 13",
    "Hydra": "-17 02 05",
    "Hydrus": "-70 58 44",
    "Indus": "-58 32 01",
    "Lacerta": "+45 35 30",
    "Leo": "+13 55 27",
    "Leo Minor": "+33 05 22",
    "Lepus": "-18 58 41",
    "Libra": "-16 30 15",
    "Lupus": "-42 01 17",
    "Lynx": "+47 43 10",
    "Lyra": "+35 37 59",
    "Mensa": "-77 32 14",
    "Microscopium": "-35 55 03",
    "Monoceros": "-01 37 39",
    "Musca": "-69 12 27",
    "Norma": "-51 51 03",
    "Octans": "-81 45 27",
    "Ophiuchus": "-05 00 40",
    "Orion": "+03 43 49",
    "Pavo": "-64 51 02",
    "Pegasus": "+20 03 16",
    "Perseus": "+44 36 25",
    "Phoenix": "-46 54 27",
    "Pictor": "-54 09 22",
    "Pisces": "+10 59 34",
    "Piscis Austrinus": "-30 08 44",
    "Puppis": "-34 29 01",
    "Pyxis": "-28 45 07",
    "Reticulum": "-62 17 09",
    "Sagitta": "+18 38 54",
    "Sagittarius": "-26 33 03",
    "Scorpius": "-32 50 33",
    "Sculptor": "-31 17 54",
    "Scutum": "-09 52 21",
    "Serpens Caput": "+04 49 45",
    "Serpens Cauda": "+04 49 45",
    "Sextans": "-02 50 56",
    "Taurus": "+17 31 36",
    "Telescopium": "-50 29 15",
    "Triangulum": "+32 23 18",
    "Triangulum Australe": "-65 55 49",
    "Tucana": "-63 29 32",   
    "Ursa Major": "+53 57 29",
    "Ursa Minor": "+76 51 19",
    "Vela": "-47 25 06",
    "Virgo": "-02 30 05",
    "Volans": "-69 27 01",
    "Vulpecula": "+24 06 55"
}

# Constellations Name Input
constellation_name = input("Name of the Constellation: ").lower().strip().title()
if (constellation_name in ra_dict) == False:
    while (constellation_name in ra_dict) == False:
        print("Please enter a valid constellation name.")
        constellation_name = input("Name of the Constellation: ").lower().strip().title()

# Required parameters for the main functions
# Local Sidereal Time
lst = 15*(calculate_lst(longitude, datetime.date(currentDateAndTime.year, currentDateAndTime.month, currentDateAndTime.day), datetime.time(currentDateAndTime.hour, currentDateAndTime.minute, currentDateAndTime.second)))
# Right Ascension
ra_hour = float(ra_dict[constellation_name][0:2])
ra_minute = float(ra_dict[constellation_name][4:6])
ra_second = float(ra_dict[constellation_name][8:10])
ra = 15 * (ra_hour + ra_minute/60 + ra_second/3600)
# Declination
dec_hour = float(dec_dict[constellation_name][0:3])
dec_minute = float(dec_dict[constellation_name][4:6])
dec_second = float(dec_dict[constellation_name][8:10])
dec = dec_hour + (dec_minute/60) + (dec_second/3600)

def calc_alt(latitude, ra, lst, dec):
    ha = lst - ra  # hour angle
    alt = np.arcsin(np.sin(dec*np.pi/180) * np.sin(latitude*np.pi/180) + np.cos(dec*np.pi/180) * np.cos(latitude*np.pi/180) * np.cos(ha*np.pi/180))
    return alt*180/np.pi

def calc_az(latitude, ra, lst, dec, alt):
    sinDec = np.sin(dec*np.pi/180)
    sinLat = np.sin(latitude*np.pi/180)
    sinAlt = np.sin(alt*np.pi/180)
    cosAlt = np.cos(alt*np.pi/180)
    cosLat = np.cos(latitude*np.pi/180)
    a = np.arccos((sinDec - sinAlt * sinLat) / (cosAlt * cosLat))
    if np.sin(lst - ra) > 0:
        return a*180/np.pi
    elif np.sin(lst - ra) < 0:
        return (360 - (a*180/np.pi))

# Print Altitude and Azimuth
alt = calc_alt(latitude, ra, lst, dec)
az = calc_az(latitude, ra, lst, dec, alt)

print(f"Altitude: {alt}")
print(f"Azimuth: {az}")
