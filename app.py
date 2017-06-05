#!flask/bin/python
from flask import Flask, jsonify, json, make_response
from lxml import html
import requests

app = Flask(__name__)

requestUrl = 'https://poshmark.com/search?query=chanel&department=Women&category=Bags&sort_by=added_desc&price%5B%5D=500-&max_id='
dataArray = []

for val in range(1,2):
    page = requests.get(requestUrl + str(val))
    tree = html.fromstring(page.content)

    salePrice = tree.xpath('/html/body/main/div[@id="content"]/section/div/div/div/div/div[@class="item-details"]/div[@class="price"]/text()')
    originalPrice = tree.xpath('/html/body/main/div[@id="content"]/section/div/div/div/div/div[@class="item-details"]/div[@class="price"]/span[@class="original"]/text()')
    href = tree.xpath('/html/body/main/div[@id="content"]/section/div/div/div/div/a[@title]/@href')

    counter = 0
    idCounter = 0

    for x in salePrice:
        if (counter < len(salePrice) and int(salePrice[counter][1:]) <= 3000 and int(originalPrice[counter][1:]) > 0 and (float(salePrice[counter][1:])/float(originalPrice[counter][1:]) < .6)):
            data = {}
            data['id'] = idCounter
            data['originalPrice'] = float(originalPrice[counter].replace("$",""))
            data['salePrice'] = float(salePrice[counter].replace("$",""))
            data['href'] = "https://poshmark.com" + href[counter]
            data['percentOff'] = str(float("%.4f" % round((float(salePrice[counter][1:])/float(originalPrice[counter][1:])),4)) * 100.00) + '%'
            dataArray.append(data)
            idCounter = idCounter + 1
        counter = counter + 1

    # counter = 0
    # for x in salePrice:`
    #     if(counter < len(salePrice) and int(x[1:]) <= 3000 and int(originalPrice[counter][1:]) > 0 and (float(x[1:])/float(originalPrice[counter][1:]) < .6)):
    #         percent = ("%.2f" % round((float(x[1:])/float(originalPrice[counter][1:])),2))
    #         print (counter + 1),': ', originalPrice[counter], ' - ', salePrice[counter], ' percent off: ', (float(1) - float(percent)), ' href: ', ('https://poshmark.com' + href[counter])
    #     counter = counter + 1


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': dataArray})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
