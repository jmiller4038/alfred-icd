 # encoding: utf-8

import sys
import requests
from workflow import ICON_WARNING, Workflow

ENDPOINT = "https://icd.mediware.com/api/{0}?{0}Code={1}"

def get_term_result(icdType, term):
	r = requests.get(ENDPOINT.format(icdType, term))
	result = r.json()
	return result

def main(wf):
	icdType = wf.args[0]
	term = wf.args[1]
	result = wf.cached_data((icdType, term), lambda: get_term_result(icdType, term), max_age=3600)
	if result:
		wf.add_item(
			title = result["Description"], 
			subtitle = result["ICDCode"],
			arg = "{0} - {1}".format(result["ICDCode"], result["Description"]),
			valid = True
		)
	else:
		wf.add_item(
			title = "No terms found", 
			subtitle = "Try another term", 
			valid = False,
			icon = ICON_WARNING
		)	
	wf.send_feedback()

if __name__ == u"__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
