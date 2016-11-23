import arxiv
import pprint
results = arxiv.query('residual')

pp = pprint.PrettyPrinter(indent=1)

for i,item in enumerate(results):
    title = item['title']
    category = item['arxiv_primary_category']['term']
    summary = item['summary']
    published = item['published']
    updated = item['updated']
    print(title, category)
    



