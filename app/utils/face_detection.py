from PIL import Image
import numpy as np
import requests

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def check_identity(customer_profile, identity_profile):
	customer_image = np.array(Image.open(requests.get(customer_profile, stream=True).raw))
	identity_image = np.array(Image.open(identity_profile))
	error = mse(customer_image, identity_image)
	print(error)
	return True