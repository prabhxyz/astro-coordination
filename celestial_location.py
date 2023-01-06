from math import sin, cos, asin, atan2, tan, pi

def calculate_coordinates(year, month, day, hour, minute, second, longitude, ra, dec, lat):
    # Calculate the Julian date
    jd = 367 * year - int(7 * (year + int((month + 9) / 12)) / 4) + int(275 * month / 9) + day + 1721013.5 + (hour + minute / 60 + second / 3600) / 24

    # Calculate the Greenwich Mean Sidereal Time
    gmst = (280.4606 + 360.98564736629 * (jd - 2451545.0)) % 360

    # Calculate the Local Mean Sidereal Time
    lmst = (gmst + longitude) % 360

    # Calculate the hour angle
    ha = (lmst - ra) % 360

    # Convert hour angle, declination, and latitude to altitude and azimuth
    alt = asin(sin(dec) * sin(lat) + cos(dec) * cos(lat) * cos(ha))
    az = atan2(sin(ha), cos(ha) * sin(lat) - tan(dec) * cos(lat))

    return (alt * 180 / pi), (az * 180 / pi)

if __name__ == '__main__':
    # Example usage
    year = 2023
    month = 1
    day = 5
    hour = 8
    minute = 25
    second = 0
    longitude = 0
    # RA
    ra_hours = 17
    ra_minutes = 0
    ra_seconds = 0
    ra = (ra_hours + ra_minutes / 60 + ra_seconds / 3600) * 15
    # Dec
    dec_degrees = 65
    dec_minutes = 0
    dec_seconds = 0
    dec = dec_degrees + dec_minutes / 60 + dec_seconds / 3600
    lat = (0 * pi / 180)

    alt, az = calculate_coordinates(year, month, day, hour, minute, second, longitude, ra, dec, lat)
    print(f'Alt: {alt}, Az: {az}')
