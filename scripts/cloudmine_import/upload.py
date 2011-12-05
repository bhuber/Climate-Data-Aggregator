import sys
import requests

if len(sys.argv) != 2:
    print "usage: %s <msgpackfile>" % (sys.argv[0])

app_id = "789cd49e1e8e4c85883908e44fd65626"
api_key = "159c883c570e4123aed99eeadcde4c41"

url = "https://api.cloudmine.me/v1/app/%s/text" % app_id

ct = "application/json"
# ct = "application/x-msgpack"

headers = {'content-type': ct,
           'x-cloudmine-apikey': api_key}

fname = sys.argv[1]
print fname

data = open(fname).read()
# data = '{"key": "value"}'
print len(data)

r = requests.post(url, data=data, headers=headers)

print r
#print r.content

