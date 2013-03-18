import sys
import os
import operator
import whoosh.index as index
from collections import Counter
from whoosh.qparser import MultifieldParser
from whoosh.reading import IndexReader
from whoosh.highlight import *

class Search:
	""" search class to response the query request."""
	
	def html_wrap(self, results):
		""" For the web search interface, we supply the html format
		wraping for format display.
		
		Args:
			results: the search resultsPage object return by
			the search_page() function.
		Returns:
			simple html wrapped string.
		"""
		
		html_str = ""
		for hit in results:
			html_str += '\n<div class=\"docitem\">\n'
			html_str += '<div class=\"title\">' + hit['Title'] + '</div>'
			html_str += '<div class=\"author\">' + hit['Author'] + '</div>'
			html_str += '<div class=\"abstract\">' + hit['Abstract'] + '</div>'
			html_str += '<div class=\"keywords\">' + hit['Keywords'] + '</div>'
			html_str += '<div class=\"year_volumn\">' + hit['Year_volumn'] + '</div>'
			html_str += '\n</div>\n'
			
		return html_str
#		print("Page %d of %d" % (results.pagenum, results.pagecount))
#		print("Showing results %d-%d of %d"
#			% (results.offset + 1, results.offset + results.pagelen,
#				len(results)))
#		for hits in results:
#			print hits.highlights("Abstract")
#			print("%s: %s\n" % (hits.rank+1, hits['Title'].encode('gbk')))
			
	def search_pg(self, query, page_num):
		""" return query results object accroding to the query string.
		
		Args:
			query: query string to do the search.
			page_num: the current pagenum of results to delivery.
		Returns:
			A list contains hits documents, and its every element is a
			dictionary which corresponding to every field and value of documents.
		"""
		hits = {}	#hits result and all information to return.
		index_dir = "D:/bjstinfo_index"		# deprecated. we should use variable or configure file.
		if not os.path.exists(index_dir):
			print "Error: indexer doesn't exist!"
			sys.exit(1)
		ix = index.open_dir(index_dir)
		
		# For keywords query, we search multi-fields of documents as:
		# Title, Keywords, Abstract. give the query-time fieldsboost:
		# {"Title": 1.2, "Keywords": 1.1, "Abstract": 1.0}
		
		query_fields = ['Title', 'Keywords', 'Abstract']
		field_boosts = {'Title':1.2, 'Keywords':1.1, 'Abstract':1.0}
		qp = MultifieldParser(query_fields, schema=ix.schema, fieldboosts=field_boosts)
		q = qp.parse(query)
		with ix.searcher() as s:
			results = s.search_page(q, page_num, terms=True)
			docs = []	#hits documents result.
			for hit in results:
				docs.append(hit.fields())
			hits['docs'] = docs
			hits['cur_page'] = results.pagenum
			hits['tot_page'] = results.pagecount
			hits['cur_start'] = results.offset + 1
			hits['cur_end'] = results.offset + results.pagelen
			hits['tot_docs'] = len(results)
		return hits
	
	def search(self, query):
		""" general search function for a query string """
		
		hit_docs = []
		index_dir = "D:/bjstinfo_index"		# deprecated. we should use variable or configure file.
		if not os.path.exists(index_dir):
			print "Error: indexer doesn't exist!"
			sys.exit(1)
		ix = index.open_dir(index_dir)
		
		# For keywords query, we search multi-fields of documents as:
		# Title, Keywords, Abstract. give the query-time fieldsboost:
		# {"Title": 1.2, "Keywords": 1.1, "Abstract": 1.0}
		
		query_fields = ['Title', 'Keywords', 'Abstract']
		field_boosts = {'Title':1.2, 'Keywords':1.1, 'Abstract':1.0}
		qp = MultifieldParser(query_fields, schema=ix.schema, fieldboosts=field_boosts)
		q = qp.parse(query)
		with ix.searcher() as s:
			results = s.search(q, limit=50, terms=True)
#			my_cf = ContextFragmenter(maxchars=100, surround=30)	#custome fragmenter.
#			results.fragmenter = my_cf
#			my_score = StandarDeviationScorer(my_cf)	#custome scorer.
#			results.scorer = my_score
#			results.formatter = HtmlFormatter()
			for hit in results:
#				print hit.fields()
				hit_docs.append(hit.fields())
				
				# why just cannot implement the highlight function?
#				print hit.highlights('Abstract', top=20)
		
		return hit_docs
		
	def search_author(self, query):
		""" search author information, with Author keywords """
		
		pass
		
	def search_journals(self, query):
		""" search with keywords about the journals """
		
		pass
	
	def fre_rank(self, results):
		""" ranking the keywords frequency in the search results 
		
		Args:
		       results: return by search function(formatted like sequence, every element
		       is also dictionary: {"Title": title, "Abstract": abstract} like
		Return:
		       sorted list(also with key, value): descent by the keyword frequency.
		"""
		
		kw_freq = {}
		words = []
		
		# construct words list, and invoke the Counter class.
		for hit in results:
			keywords = hit["Keywords"].strip()
			if keywords:
				words.extend(keywords.split())
		print "total words: " + str(len(words))
		kw_freq = Counter(words)
		sorted_kw_freq = sorted(kw_freq.iteritems(), key=operator.itemgetter(1),reverse=True)
		
		return sorted_kw_freq
	
		
def main():
	search = Search()
	results = search.search_pg(u'公司', 1)
	print results['docs']
#	print results['cur_page']
#	print results['tot_page']
#	print results['cur_start']
#	print results['cur_end']

if __name__ == '__main__':
	main()