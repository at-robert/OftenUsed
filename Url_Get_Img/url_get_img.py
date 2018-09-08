from lxml import html

# download & parse web page
doc = html.parse('http://apod.nasa.gov/apod/astropix.html')

# find the first <a href that ends with .png or .jpg or .jpeg ignoring case
ns = {'re': "http://exslt.org/regular-expressions"}
img_url = doc.xpath(r"//a[re:test(@href, '\.(?:png|jpg|jpeg)', 'i')]/@href",
                    namespaces=ns, smart_strings=False)[0]
print(img_url)