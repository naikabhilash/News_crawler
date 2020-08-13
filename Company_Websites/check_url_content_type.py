# import requests
#
# r = requests.get('https://www.itcportal.com/ReturnViewImage.aspx?fileid=1478')
# content_type = r.headers.get('content-type')
#
# if 'application/pdf' in content_type:
#  ext = '.pdf'
# elif 'text/html' in content_type:
#  ext = '.html'
# else:
#  ext = ''
# print('Unknown type: {}'.format(content_type))
#
# print('out',ext)

import requests

def check_content(url):

    r = requests.get(url)
    content_type = r.headers.get('content-type')

    if 'application/pdf' in content_type:
        ext = 'PDF'
    elif 'text/html' in content_type:
        ext = 'HTML'
    else:
        ext = ''

    return ext