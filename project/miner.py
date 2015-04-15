
from project.fb.Facebook import Facebook
from facepy import utils
from project.TextAnalyzer import TextAnalyzer

#ACCESS_TOKEN = utils.get_application_access_token(678384065623866, "93449010f3f539ab5fbcec9668f331ef")
# to get the token please go to 
ACCESS_TOKEN = ""


print(ACCESS_TOKEN)

#companies = ('pepsibolivia', 'orientalmirinda')
companies = ['pepsibolivia']
analyzer = TextAnalyzer()

fb = Facebook(ACCESS_TOKEN, analyzer)

for company in companies:
    print("starting process for company %s" % company)
    fb.start_process(company)
