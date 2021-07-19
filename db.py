from flask import Flask,request,render_template
import pymongo as pm

client = pm.MongoClient('mongodb://127.0.0.1:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
app = Flask('database app')

@app.route('/home')
def main():
  main_page = render_template('main.html')
  return main_page

@app.route('/form')
def form():
  operation_name = request.args.get('operation_name')
  return render_template(operation_name)
  
@app.route('/database/rem')
def remdata():

  db = request.args.get('db')
  coll = request.args.get('coll')
  name = request.args.get('name')
  company = request.args.get('company')

  if db and coll == '' and name == '' and company == '':
    client.drop_database(db)
    return 'database removed !!'

  elif db and coll  and name == '' and company == '':
    datab = client[db]
    datab.drop_collection(coll)
    return 'collection removed !!'

  elif db and coll  and name  and company == '':
    datab  = client[db]
    collect = datab[coll]
    collect.delete_many({'name': name})
    return 'doc removed !!'

  elif db and coll  and name  and company :
    datab  = client[db]
    collect = datab[coll]
    collect.delete_many({'name': name,'company':company})
    return 'doc removed !!'

  elif db and coll  and name ==''  and company :
    datab  = client[db]
    collect = datab[coll]
    collect.delete_many({'company': company})
    return 'doc removed !!'


@app.route('/database/up')
def updata():

  db = request.args.get('db')
  coll = request.args.get('coll')
  Oname = request.args.get('Oname')
  Ncompany = request.args.get('Ncompany')
  Nname = request.args.get('Nname')
  Ocompany = request.args.get('Ocompany')
  datab = client[db]
  collect = datab[coll]

  if db and coll and Oname and Ocompany:

    if Nname and Ncompany =='':
      collect.update_many({'name': Oname,'company': Ocompany},{'$set': {'name': Nname}})
      return 'doc updated !!'

    elif Nname and Ncompany:
      collect.update_many({'name': Oname,'company': Ocompany},{'$set': {'name': Nname,'company': Ncompany}})
      return'doc updated !!'

    elif Nname == '' and Ncompany:
      collect.update_many({'name': Oname,'company': Ocompany},{'$set': {'company': Ncompany}})
      return 'doc updated !!'

  elif db and coll and Oname and Ocompany == '':
    collect.update_many({'name': Oname},{'$set': {'name': Nname}})
    return 'doc updated !!'

  elif db and coll and Oname == '' and Ocompany :
    collect.update_many({'company': Ocompany}, {'$set': {'company': Ncompany}})
    return 'doc updated !!'


@app.route('/database/get')
def searching():

  db = request.args.get('db')
  coll = request.args.get('coll')
  name = request.args.get('name')
  company = request.args.get('company')
  #out = render_template('db.html',name=name,company=company)
  
  if coll == '' and name == '' and company == '' and db =='':
    return '<h3>available databases :</h3>' + render_template('db.html',data=client.database_names())
  
  elif coll == '' and name == '' and company == '':
    datab = client[db]
    return '<h3>available collections :</h3>' + render_template('db.html',data=datab.list_collection_names())
  
  else:   
    datab = client[db]
    collect = datab[coll]
       
    if name =='' and company:
      data=collect.find({'company': company})
      return '<h3>OUTPUT</h3>' + render_template('db.html',data=list(data))
      #return reader(data)
      
    elif company == '' and name:
      data=collect.find({'name': name})
      return '<h3>OUTPUT</h3>' + render_template('db.html',data=list(data))
      #return reader(data)
      
    elif name and company:
      data=collect.find({'name': name, 'company': company})
      return '<h3>OUTPUT</h3>' + render_template('db.html',data=list(data)) 
      
  
  

@app.route('/database/in',methods=['POST','GET'])
def inserting():

  if request.method == 'POST':
    db = request.form.get('db')
    coll = request.form.get('coll')
    name = request.form.get('name')
    company = request.form.get('company')
    return data_in(db,coll,name,company)

  elif request.method == 'GET':
    db = request.args.get('db')
    coll = request.args.get('coll')
    name = request.args.get('name')
    company = request.args.get('company')
    return data_in(db,coll,name,company)


def data_in(db,coll,name,company):

  db = client[db]
  coll = db[coll]
  item = {'name': name, 'company': company}
  coll.insert_one(item)
  return '<h3>Created Successfully</h3>' + render_template('db.html',data = item)



app.run(host="192.168.29.78", port=1234 ,debug=True)


#for find function
#either can convert the mongodb cursor reference to list then show on next html page
#or use for loop and append each element(doc) in that collection , append to 1 list then show the list on next html page. eg -
'''
def reader(data):
  l =[]
  i = 1
  for doc in data:
    l.append(doc)
  return '<pre>' + render_template('db.html',data=l) + '</pre>'
  '''
#else can use dumping , bjson etc etc to directly convert and return the result inside flask path function only.
