"""Simple functions to spread the joy of text based cabbage."""

import http.client
import random
import re

from cabbage import error

# TODO(tunacom): Docstring cleanup.
# TODO(tunacom): In general, the organization here is pretty craptastic.
# Restructure it in a cleaner way, avoid hasattr/setattr.

CABBAGE_IMAGE_PROBABILITY = 0.8
SPECIAL_CABBAGE_PROBABILITY = 0.9

CABBAGES_TO_REQUEST = 1500
CABBAGES_PER_PAGE = 500

SPECIAL_CABBAGES = [
    'I LIKE BUTTERFLIES',
    'what is love?',
    'NO MORE CABBAGE PLEASE, IT HURTS',
    'butterflies',
]

BAD_FLICKR_RESPONSE_ERROR = (
    'FLICKER HAS DENIED US OUR PRECIOUS CABBAGES. SHAME! SHAME!')
FLICKR_CABBAGE_REQUEST_FORMAT = (
    '/services/rest/?method=flickr.photos.search&tags=butterfly&'
    'page={page}&per_page={per_page}&api_key={api_key}')
FLICKR_CABBAGE_IMAGE_FORMAT = (
    'https://farm{farm}.staticflickr.com/{server}/{photo_id}_{secret}.jpg '
    '(title: {title})')
FLICKR_PHOTO_REGEX = re.compile(
    r'\s*<photo id="(\d+)" .* secret="(\w+)" server="(\w+)" farm="(\w+)" '
    r'title="(\w+)" .*')


def bootstrap(flickr_api_key):
  """Perform initial cabbage setup, such as Flickr API key setup."""
  setattr(get_flickr_api_key, 'flickr_api_key', flickr_api_key)


def get_flickr_api_key():
  """Get the current Flickr API key for cabbage fetching."""
  return getattr(get_flickr_api_key, 'flickr_api_key')


# TODO(tunacom): This should be more sophisticated.
def seems_like_cabbage(title):
  """Check to see if a title sounds like a cabbage title.

  Args:
    title: The potential cabbage image title. Expected to be lowercase.

  Returns:
    Boolean indicating whether or not this seems like cabbage.
  """
  # Cabbage butterflies are the main source of non-cabbage sadness.
  cabbage_butterfly_keywords = [
    'cabbage',
  ]
  for keyword in cabbage_butterfly_keywords:
    if keyword in title:
      return False

  return True


def load_cabbages(page=1):
  """Preload cabbages into the cabbage cache."""
  if page == 1:
    print('REPOPULATING THE CABBAGE CACHE WITH AMAZING CABBAGES!')

  # Connect to the Flickr API server.
  # TODO(tunacom): Looks like Flickr isn't returning the right number of results
  # per page, or the regex is screwing up on some things. Investigate this.
  connection = http.client.HTTPSConnection('api.flickr.com')
  path = FLICKR_CABBAGE_REQUEST_FORMAT.format(api_key=get_flickr_api_key(),
                                              per_page=CABBAGES_PER_PAGE,
                                              page=page)
  connection.request('GET', path)
  response = connection.getresponse()

  # If the HTTP response code was anything other than OK, yell at Flickr.
  if response.status != 200:
    raise error.RecoverableCabbageException(BAD_FLICKR_RESPONSE_ERROR)

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
      title = match.group(5).lower()
      photo = FLICKR_CABBAGE_IMAGE_FORMAT.format(photo_id=photo_id,
                                                 secret=secret,
                                                 server=server,
                                                 farm=farm,
                                                 title=title)

      if seems_like_cabbage(title):
        photos.append(photo)

  # The parsing above is a bit brittle, so have some fallback.
  if not photos:
    raise error.RecoverableCabbageException(
        'I HAD TROUBLE FIGURING OUT WHERE THE CABBAGE WAS. OOPS. TELL TUNA.')

  if not hasattr(get_cabbage, 'cabbage_cache'):
    setattr(get_cabbage, 'cabbage_cache', [])

  existing_cache = getattr(get_cabbage, 'cabbage_cache')
  existing_cache += photos

  print('PAGE {page}: KEPT {total}/{max} POTENTIAL CABBAGES.'.format(
      page=page, total=len(photos), max=CABBAGES_PER_PAGE))

  last_page = CABBAGES_TO_REQUEST / CABBAGES_PER_PAGE
  if page < last_page:
    load_cabbages(page=page + 1)


def get_cabbage():
  """Get a cabbage from the prepopulated cabbage cache, or populate it."""
  cabbage_cache = getattr(get_cabbage, 'cabbage_cache', [])
  if not cabbage_cache:
    load_cabbages()

  cabbage_index = random.randint(0, len(cabbage_cache) - 1)
  cabbage = cabbage_cache.pop(cabbage_index)

  return cabbage


def create_cabbage_image():
  """Spread the joy of pictures of cabbages.

  Returns:
    A link to some cabbage. Pure joy.
  """
  try:
    return get_cabbage()
  except error.RecoverableCabbageException as e:
    return str(e)


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
