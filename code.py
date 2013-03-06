import web
from web import form
from searcher import Search

render = web.template.render('templates/')
urls = (
	'/', 'index'
)
app = web.application(urls, globals())


query_form = form.Form(
	form.Textbox('QueryItems',
		form.notnull,
		class_='query_entry',
		value=''))
		
page_form = form.Form(
	form.Textbox('page',
		form.notnull,
		form.regexp('\d+', 'Must be a digit'),
		form.Validator('Must be more than 0', lambda x: int(x)>0),
		class_='go',
		value='1'),
		form.Button('>>',
		class_='go_next',
		value='2'),
		form.Button('<<',
		class_='go_last',
		value='0'))

class index:
	def GET(self):
		query_f = query_form()
		page_f = page_form()
		return render.index(query_f, page_f, "")

	def POST(self):
		query_f = query_form()
		page_f = page_form()
		# validation of query string and page number.
		if (not query_f.validates()) or (not page_f.validates()):
			return render.index(query_f, page_f, "")
		else:
			search = Search()
			results = search.search_pg(query_f['QueryItems'].value, 1)
			return render.index(query_f, page_f, results)
#			return "query: %s \tfound: %s\n" % (form['QueryItems'].value.encode('gbk'), hits[1].encode('gbk'))

if __name__ == "__main__":
	web.internalerror = web.debugerror
	app.run()
