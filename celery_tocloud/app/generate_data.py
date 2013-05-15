for i in range(1,11):
	# Create 10 objects in the database
	o = URLUpload.objects.create(
		email='calvindlm@gmail.com',
		url='http://www.greenteapress.com/thinkstats/thinkstats.pdf',
		access_token=token)