
from project.fb.Facebook import Facebook
from project.tw.process import TwitterProcess
from facepy import utils
from project.TextAnalyzer import TextAnalyzer

#ACCESS_TOKEN = utils.get_application_access_token(678384065623866, "93449010f3f539ab5fbcec9668f331ef")
# to get the token please go to 
ACCESS_TOKEN = "CAACEdEose0cBAGguOjAXE7ImefR0cv7jEP9x6maWumQ2oFb5sAExGF6N3OmwZCncicgWhEYotTfsB5yTVEHJgrVHFJFbzxrgyDynaaJlQzX08XHmARYBHw3Tmcpq2Mt9tEH3ZCxDQ26Ic2LxkS0rlxypFGY9KuZACWQLrKKndexEy8GtZBFYteZBEUZBBPBlk7yzlY1apMOIZCRrWdFjeN1"


print(ACCESS_TOKEN)

companies = ('pepsibolivia', 'orientalmirinda')
# companies = ['pepsibolivia']
analyzer = TextAnalyzer()

fb = Facebook(ACCESS_TOKEN, analyzer)
tw = TwitterProcess(analyzer)

for company in companies:
    print("starting process for company %s" % company)
    fb.get_gral_data_today(company)
    #fb.start_process(company)
    #tw.start_process(company)

