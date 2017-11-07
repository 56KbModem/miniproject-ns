import requests
import xmltodict

# Authentication for NS-API @ webservices.ns.nl
auth_details = ('nick.snel@student.hu.nl', 'CHXwsKlQhEhr4REC2N_wqkS4oxI8SakCb4njn8tIPopejiHJZFj5Lw')


print("Dit is een testprogramma voor de NS-API")

# Test function: download raw xml from NS-API.
def test_request():
	url = 'http://webservices.ns.nl/ns-api-avt?station=ut'
	response = requests.get(url, auth=auth_details)

	print(response.text)

# This function returns a list of all known
# train departures from a given station.
def get_request(station):
	url = 'http://webservices.ns.nl/ns-api-avt?station='

	request_url = url + station
	response = requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	# This will return a list of all dictionaries
	# containing information about leaving trains.
	vertrekkende_treinen = []
	for item in xml_reader['ActueleVertrekTijden']['VertrekkendeTrein']:
		return_dict = {}
		return_dict['rit_nr'] = item['RitNummer']
		return_dict['eind_best'] = item['EindBestemming']

		datum, tijd = item['VertrekTijd'].split("T")
		tijd = tijd.split("+", 1)[0]

		return_dict['vertrek_tijd'] = datum + " " + tijd
		return_dict['trein_soort'] = item['TreinSoort']
		vertrekkende_treinen.append(return_dict)

	return vertrekkende_treinen

# This function returns a dictionary containing
# information about travel directions.
def reis_planner(from_station, to_station):
	url = "http://webservices.ns.nl/ns-api-treinplanner?"

	request_url = url + 'fromStation=' + from_station + '&toStation=' + to_station
	response =  requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	for item in xml_reader['ReisMogelijkheden']['ReisMogelijkheid']:
		if item['Optimaal'] == 'true':
			return_dict = {}
			return_dict['aantal_overstappen'] = item['AantalOverstappen']

			# Format 'vertrek_tijd'
			beg_datum, beg_tijd = item['ActueleVertrekTijd'].split("T")
			beg_tijd = beg_tijd.replace("+0200", "")
			return_dict['vertrek_tijd'] = beg_datum + " " + beg_tijd

			# Format 'aankomst_tijd'
			eind_datum, eind_tijd = item['ActueleAankomstTijd'].split("T")
			eind_tijd = eind_tijd.replace("+0200", "")
			return_dict['aankomst_tijd'] = eind_datum + " " + eind_tijd
		else:
			continue
	return return_dict

# Check if directly called by interpreter for prototyping,
# if not called directly but by script then the functions
# will be available for the caller.
if __name__ == "__main__":
	while True:
		print("Maak A.U.B. een keuze")
		print("1: Demo request naar NS-API")
		print("2: Vraag vertrektijden op voor een station")
		print("3: Plan een reis bij de NS")
		print("4: Stoppen met script")

		s = int(input("> "))
		if s == 1:
			test_request()
		elif s == 2:
			station = input("Geef a.u.b. een stationsnaam op: ")
			print(get_request(station))
		elif s == 3:
			from_station = input("Waar kom je vandaan? ")
			to_station = input("Waar wil je naartoe? ")
			print(reis_planner(from_station, to_station))
		elif s == 4:
			print("Tot ziens!")
			exit()
		else:
			print("Geen geldige invoer")
