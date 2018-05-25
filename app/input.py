from pick import pick
from .utils import format_city, get_args

def choose_resource(resources):
  title = 'Please choose desired city: '

  if len(resources) == 0:
    print("Sorry, no cities were found with this name")
    exit(1)

  if len(resources) == 1:
    return resources[0]

  options = []
  items = {}
  for city in resources:
    formatted_address = format_city(city)
    options.append(formatted_address)
    items[formatted_address] = city

  (option, index) = pick(options, title)
  
  return items[option]

def get_city():
  args = get_args()
  if 'city' in args and args['city'] is not None:
    return args['city']

  while True:
    answer = input('Please provide a city\n > ')
    print("")

    if len(answer) > 2:
      return answer
    else:
      print("Sorry, name should be more than 2 letters\n")