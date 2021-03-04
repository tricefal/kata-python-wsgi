from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
import codecs




def contentType(path: str) -> str:
	if path.endswith(".css"):
		print("content type : text/css")
		return 'text/css'
	else:
		print("content type : text/html")
		return 'text/html'


def application(environ, start_response):
	# for GET method :
	# d = parse_qs(environ['QUERY_STRING'])
	
	file = environ['PATH_INFO'].split('/')
	if not file[1]:
		file_name = "index.html"
	else:
		file_name = file[1]
	print("file name : ", file_name)

	# for POST method :
	try : 
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0
	request_body = environ['wsgi.input'].read(request_body_size)
	person_attributes = parse_qs(request_body)


	# print(d)

	
	# print(age, ' : ', hobbies)

	
	

	try:
		file = codecs.open(file_name, 'r').read()
		status = '200 OK'
	except:
		status = "404 Not Found"

	file_type = contentType(file_name)
	if file_type == "text/html":
		age = person_attributes.get(b"age", [b''])[0].decode('UTF8')
		hobbies = [elem.decode('UTF8') for elem in person_attributes.get(b"hobbies", [b''])]

		# escape to prevent script injection
		age = escape(age)
		hobbies = [escape(hobby) for hobby in hobbies]
		response_body = file % {
			'checked-software': ('', 'checked')['software' in hobbies], # Return True or false = 1 or 0 which become the index of tuple
			'checked-tunning': ('', 'checked')['tunning' in hobbies],
			'age': age or 'Empty',
			'hobbies': ', '.join([hobby for hobby in hobbies or ['No Hobbies ?']])
		}
	else : 
		
		response_body = file
	# response_body = "\n".join(response_body)

	# response_body = [
	# 	'The Beggining\n',
	# 	'*' * 30 + '\n',
	# 	response_body,
	# 	'\n' + '*' * 30,
	# 	'\nThe End',
	# ]


	content_length = len(response_body)

	response_headers = [
		("Content-Type", file_type),
		("Content-Length", str(content_length)),
	]

	start_response(status, response_headers)

	return [res.encode() for res in response_body]



httpd = make_server(
	'localhost',
	8051,
	application
)
httpd.serve_forever()
