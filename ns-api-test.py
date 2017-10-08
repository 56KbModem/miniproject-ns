import requests
import xmltodict
import datetime

auth_details = ('nick.snel@student.hu.nl', 'CHXwsKlQhEhr4REC2N_wqkS4oxI8SakCb4njn8tIPopejiHJZFj5Lw')


print("Dit is een testprogramma voor de NS-API")

def demo_request():
	url = 'http://webservices.ns.nl/ns-api-avt?station=ut'
	response = requests.get(url, auth=auth_details)

	print(response.text)

def aangepast_request():
	url = 'http://webservices.ns.nl/ns-api-avt?station='
	station = input("Geef aub een stationscode op: ")

	request_url = url + station
	response = requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	for item in xml_reader['ActueleVertrekTijden']['VertrekkendeTrein']:
		print("\nRitnr:\tBestemming")
		print("{0}:\t{1}".format(item['RitNummer'], item['EindBestemming']))
		print("Vertrek:")
		vertrek_tijd = item['VertrekTijd']
		datum , tijd = vertrek_tijd.split("T")
		print(datum)
		print(tijd)
while True:
	print("Maak A.U.B. een keuze")
	print("1: Demo request naar NS-API")
	print("2: Aangepast request naar NS-API")
	print("3: Stoppen met script")

	s = int(input("> "))
	if s == 1:
		demo_request()
	elif s == 2:
		aangepast_request()
	elif s == 3:
		print("Tot ziens!")
		exit()
	else:
		print("Geen geldige invoer")
