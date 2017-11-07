import requests
import xmltodict
import json
from time import localtime, strftime

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
def vertrek_tijden(station):
	url = 'http://webservices.ns.nl/ns-api-avt?station='

	request_url = url + station
	response = requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	# Add events for json file.
	event_list = {'last_query': request_url}
	event_list['last_query_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	json_handler(event_list)

	# This will return a list of all dictionaries
	# containing information about leaving trains.
	vertrekkende_treinen = []
	for item in xml_reader['ActueleVertrekTijden']['VertrekkendeTrein']:
		return_dict = {}
		return_dict['rit_nr'] = item['RitNummer']
		return_dict['eind_best'] = item['EindBestemming']
		return_dict['vertrek_tijd'] = time_formatting(item['VertrekTijd'])
		return_dict['trein_soort'] = item['TreinSoort']

		# Add a departuring train data to list of departures
		vertrekkende_treinen.append(return_dict)

	return vertrekkende_treinen

# This function returns a dictionary containing
# information about travel directions.
def reis_planner(from_station, to_station):
	url = "http://webservices.ns.nl/ns-api-treinplanner?"

	request_url = url + 'fromStation=' + from_station + '&toStation=' + to_station
	response =  requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	# Add events for json file.
	event_list = {'last_query': request_url}
	event_list['last_query_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	json_handler(event_list)

	mogelijke_reizen = []

	for item in xml_reader['ReisMogelijkheden']['ReisMogelijkheid']:
		if item['Optimaal'] == 'true': # Search for most optimal travel direction
			return_dict = {}
			return_dict['optimaal'] = True
			return_dict['aantal_overstappen'] = item['AantalOverstappen']
			return_dict['vertrek_tijd'] = time_formatting(item['ActueleVertrekTijd'])
			return_dict['aankomst_tijd'] = time_formatting(item['ActueleAankomstTijd'])

			# Add optimal direction to 'mogelijke_reizen'
			mogelijke_reizen.append(return_dict)

		elif item['Optimaal'] == 'false':
			return_dict = {}
			return_dict['optimaal'] = False
			return_dict['aantal_overstappen'] = item['AantalOverstappen']
			return_dict['vertrek_tijd'] = time_formatting(item['ActueleVertrekTijd'])
			return_dict['aankomst_tijd'] = time_formatting(item['ActueleAankomstTijd'])

			# Add additional travel directions to 'mogelijke_reizen'
			mogelijke_reizen.append(return_dict)

	return mogelijke_reizen

# This function takes a dict and update the json file
def json_handler(event):
	json_file = open("config.json", 'r')
	json_data = json.load(json_file)
	json_file.close()

	# Update json data
	json_data.update(event)
	json_data['requests'] += 1
	print("JSON DATA:")
	print(json_data)

	# write json data back
	json_file = open("config.json", 'w')
	json_object = json.dumps(json_data, sort_keys=True, indent=4)
	json_file.write(json_object)
	json_file.close

# This function formats the time stamp given
# by the API XML to a more user-friendly format.
def time_formatting(timestring):
	beg_datum, beg_tijd = timestring.split("T")
	beg_tijd = beg_tijd.split("+", 1)[0]
	formatted_time = beg_datum + " " + beg_tijd

	return formatted_time

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
			print(vertrek_tijden(station))
		elif s == 3:
			from_station = input("Waar kom je vandaan? ")
			to_station = input("Waar wil je naartoe? ")
			print(reis_planner(from_station, to_station))
		elif s == 4:
			print("Tot ziens")
			exit()
		else:
			print("Geen geldige invoer")
