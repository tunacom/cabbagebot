"""Simple functions to spread the joy of text based cabbage."""

import http.client
import random
import re

CABBAGE_IMAGE_PROBABILITY = 0.6
SPECIAL_CABBAGE_PROBABILITY = 0.3

SPECIAL_CABBAGES = [
    'brassica oleracea',
    'savoy',
    'radicchio',
    'napa cabbage',
    'bok choy',
    'brussels sprouts',
    'cabbages',
]

BAD_FLICKR_RESPONSE_ERROR = (
    'FLICKER HAS DENIED US OUR PRECIOUS CABBAGES. SHAME! SHAME!')
FLICKR_CABBAGE_REQUEST_FORMAT = (
    '/services/rest/?method=flickr.photos.search&tags=cabbage&'
    'page={page}&per_page=2000&api_key={api_key}')
FLICKR_CABBAGE_IMAGE_FORMAT = (
    'https://farm{farm}.staticflickr.com/{server}/{photo_id}_{secret}.jpg')
FLICKR_PHOTO_REGEX = re.compile(
    r'\s*<photo id="(\d+)" .* secret="(\w+)" server="(\w+)" farm="(\w+)" .*')


def bootstrap(flickr_api_key):
  """Perform initial cabbage setup, such as Flickr API key setup."""
  setattr(get_flickr_api_key, 'flickr_api_key', flickr_api_key)


def get_flickr_api_key():
  """Get the current Flickr API key for cabbage fetching."""
  return getattr(get_flickr_api_key, 'flickr_api_key')


def create_cabbage_text():
  """Spread the joy of the word "cabbage".

  Returns:
    Text-based joy.
  """
  cabbage_list = ['cabbage'] * random.randint(1, 16)

  if random.random() < SPECIAL_CABBAGE_PROBABILITY:
    special_cabbage = random.choice(SPECIAL_CABBAGES)
    cabbage_list[random.randint(0, len(cabbage_list) - 1)] = special_cabbage

  return ' '.join(cabbage_list)


def get_cached_cabbage():
  """Get a cabbage from the prepopulated cabbage cache."""
  if not hasattr(get_cached_cabbage, 'cabbage_cache'):
    return None

  cabbage_cache = getattr(get_cached_cabbage, 'cabbage_cache')
  cabbage_index = random.randint(0, len(cabbage_cache) - 1)
  cabbage = cabbage_cache.pop(cabbage_index)

  if not cabbage_cache:
    delattr(get_cached_cabbage, 'cabbage_cache')

  return cabbage


def create_cabbage_image():
  """Spread the joy of pictures of cabbages.

  Returns:
    A link to some cabbage. Pure joy.
  """
  cabbage_image = get_cached_cabbage()
  if cabbage_image:
    return cabbage_image

  # Connect to the Flickr API server.
  connection = http.client.HTTPSConnection('api.flickr.com')
  connection.request(
      'GET', FLICKR_CABBAGE_REQUEST_FORMAT.format(api_key=get_flickr_api_key(),
                                                  page=1))
  response = connection.getresponse()

  # If the HTTP response code was anything other than OK, yell at Flickr.
  if response.status != 200:
    return BAD_FLICKR_RESPONSE_ERROR

  result = response.read().decode('utf-8')
  photos = []
  for line in result.splitlines():
    # Proper xml parsing may be necessary at some point, but I'd rather not
    # bring in an XML parsing library just for this.
    match = FLICKR_PHOTO_REGEX.match(line)
    if match:
      photo_id = match.group(1)
      secret = match.group(2)
      server = match.group(3)
      farm = match.group(4)
      photo = FLICKR_CABBAGE_IMAGE_FORMAT.format(photo_id=photo_id,
                                                 secret=secret,
                                                 server=server,
                                                 farm=farm)
      photos.append(photo)

  # The parsing above is a bit brittle, so have some fallback.
  if not photos:
    return 'I HAD TROUBLE FIGURING OUT WHERE THE CABBAGE WAS. OOPS. TELL TUNA.'

  setattr(get_cached_cabbage, 'cabbage_cache', photos)
  return get_cached_cabbage()


def spread_joy():
  """Spread the joy of cabbage.

  Returns:
     Joy.
  """
  roll = random.random()
  if roll < CABBAGE_IMAGE_PROBABILITY:
    return create_cabbage_image()

  # By default, we return text based cabbage.
  return create_cabbage_text()