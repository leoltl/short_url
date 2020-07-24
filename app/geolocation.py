from threading import Thread
from requests import request 
from app.models import Visit
from app import db

def search_and_save_ip_geolocation(ip, visit_id):
  # TODO: handle network request failure, save ip to a queue to 
  # geolate the visit at later time.
  data = request('GET', f'http://ip-api.com/json/{ip}').json()
  visit = Visit.query.get(visit_id)
  visit.set_geo_info(
    ip=ip,
    country_code=data.get('countryCode', 'N/A'),
    region_name=data.get('regionName', 'N/A'),
    city_name=data.get('city', 'N/A')
  )
  db.session.add(visit)
  db.session.commit()
  return

def locate(req, visit_id):
  ip = req.remote_addr
  if not ip:
    return
  Thread(target=search_and_save_ip_geolocation, args=(ip, visit_id)).start()