import requests
import xmltodict
import json
from time import localtime, strftime

# Authentication for NS-API @ webservices.ns.nl
json_file = open("config.json", 'r')
json_data = json.load(json_file)
json_file.close

api_key = json_data['api_key']
api_username = json_data['api_username']

auth_details = (api_username, api_key)

# This function gets a station list. Useful for
# Autocompletion in the GUI.
def get_station_list():
	request_url = 'http://webservices.ns.nl/ns-api-stations-v2'
	response = requests.get(request_url, auth=auth_details)
	xml_reader = xmltodict.parse(response.text)

	# Add events for json file.
	event_list = {'last_query': request_url}
	event_list['last_query_time'] = strftime("%Y-%m-%d %H:%M:%S", localtime())
	json_handler(event_list)

	# Adding the long names and synonyms to a list.
	stations_namen = []
	for station in xml_reader['Stations']['Station']:
		stations_namen.append(station['Namen']['Lang'])

		# Really ugly hack to make sure there are no lists included 
		# inside the main list.
		if station['Synoniemen'] != None:
			if type(station['Synoniemen']['Synoniem']) is list:
				for synoniem in station['Synoniemen']['Synoniem']:
					stations_namen.append(synoniem)
			else:
				stations_namen.append(station['Synoniemen']['Synoniem'])

	return stations_namen
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

		if 'VertrekVertragingTekst' in item:
			return_dict['vertraging'] =  item['VertrekVertragingTekst']
		else:
			return_dict['vertraging'] = '0 min'
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
	tussen_stations = []
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
		print("1: Vraag stations namen op")
		print("2: Vraag vertrektijden op voor een station")
		print("3: Plan een reis bij de NS")
		print("4: Stoppen met script")

		s = int(input("> "))
		if s == 1:
			print(get_station_list())
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
