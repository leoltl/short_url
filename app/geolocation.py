import requests
from threading import Thread
from flask import current_app
from app.models import Visit
from app import db

def search_and_save_ip_geolocation(app, ip, visit_id):
  with app.app_context():
    # TODO: handle network request failure, save ip to a queue to 
    # geolate the visit at later time.
    data = requests.get(f'http://ip-api.com/json/{ip}').json()
    print(data)
    visit = Visit.query.get(visit_id)
    visit.set_geo_info(
      ip=ip,
      country_code=data.get('countryCode', 'N/A'),
      region_name=data.get('regionName', 'N/A'),
      city_name=data.get('city', 'N/A'),
      lon=data.get('lon', None),
      lat=data.get('lat', None)
    )
    db.session.add(visit)
    db.session.commit()
    db.session.remove()
    return

def locate(ip, visit_id):
  Thread(
    target=search_and_save_ip_geolocation, 
    args=(current_app._get_current_object(), ip, visit_id)
  ).start()