#! encoding=utf-8
import json
import copy
data = []

author_detail = {}
affiliation_detail = {}
keyword_detail = {} # keyword -> id at very begin
keyword_count = 0

def split_getid(text):
	a, _ = text.split(';')
	return int(a)

with open('visual.txt') as origin:
	lines = origin.readlines()[::-1]
	while len(lines):
		tmp = {}
		tmp['year'] = int(lines.pop().strip().strip('*'))
		# About Author
		author = {}
		while True:
			line = lines.pop().strip()
			if not line:
				break
			_id, name, weight = line.split('|')
			_id = int(_id)
			author_detail[_id] = name
			author[_id] = float(weight)
		tmp['author'] = author

		#About Affiliation
		affiliation = {}
		while True:
			line = lines.pop().strip()
			if not line:
				break
			_id, name, weight = line.split('|')
			_id = int(_id)
			affiliation_detail[_id] = name
			affiliation[_id] = float(weight)
		tmp['affiliation'] = affiliation

		#Keyword
		keyword = {}
		while True:
			line = lines.pop().strip()
			if not line:
				break
			name, weight = line.split('|')
			_id = keyword_detail.get(name, keyword_count + 1)
			if _id == keyword_count + 1:
				keyword_count += 1
				keyword_detail[name] = keyword_count
			keyword[_id] = float(weight)
		tmp['keyword'] = keyword

		#Co-authorship
		author_edge = []
		while True:
			line = lines.pop().strip()
			if not line:
				break
			p1, p2, weight = line.split('|')
			p1 = split_getid(p1)
			p2 = split_getid(p2)
			author_edge.append((p1, p2, float(weight)))
		tmp['author_edge'] = author_edge

		#Author-Affiliation
		author_affiliation = []
		while True:
			line = lines.pop().strip()
			if not line:
				break
			p1, p2, weight = line.split('|')
			p1 = split_getid(p1)
			p2 = split_getid(p2)
			author_affiliation.append((p1, p2, float(weight)))
		tmp['author_affiliation'] = author_affiliation

		#Author-Keyword
		affiliation_keyword = []
		while True:
			line = lines.pop().strip()
			if not line:
				break
			p1, p2, weight = line.split('|')
			p1 = split_getid(p1)
			p2 = keyword_detail[p2]
			affiliation_keyword.append((p1, p2, float(weight)))
		tmp['affiliation_keyword'] = affiliation_keyword
		data.append(tmp)

#reverse keyword_detail to get id -> keyword dict
keyword_detail = {v: k for k, v in keyword_detail.iteritems()}

#generate new node
nodes = []
links = []
global_id = 0

old_detail = [
	('author', author_detail),
	('affiliation', affiliation_detail),
	('keyword', keyword_detail),
]
mapping = {key: {} for key, _ in old_detail}
# meta node
meta = {}
for category, _ in old_detail:
	node = {
		'type': 'meta',
		'category': category,
		'name': '__' + category + '__',
	}
	nodes.append(node)
	meta[category] = global_id
	global_id += 1

for category, old_map in old_detail:
	for _id, name in old_map.iteritems():
		mapping[category][_id] = global_id
		node = {
			"type": 'normal',
			"category": category,
			"name": name,
		}
		nodes.append(node)
		links.append(
			{
				'source': meta[category],
				'target': global_id,
				'type': 'metalink',
			})
		global_id += 1

result = {
	"year_description": sorted(map(lambda x: x['year'], data)),
	"data": {
	},
}
for year_data in data:
	cur_nodes = copy.deepcopy(nodes)
	cur_links = copy.deepcopy(links)
	new_links = []
	for category, _ in old_detail:
		for old_id, weight in year_data[category].iteritems():
			new_id = mapping[category][old_id]
			cur_nodes[new_id]['rate'] = weight
	for author_edge in year_data['author_edge']:
		new_link = map(lambda x: mapping['author'][x], author_edge[0:2])
		new_link.append(author_edge[2])
		new_links.append(new_link)
	for source, target, weight in new_links:
		cur_links.append(
			{
				'source': source,
				'target': target,
				'type': 'inner',
				'rate': weight,
			}
		)
	new_links = []
	for (author_id, affiliation_id, weight) in year_data['author_affiliation']:
		author_id = mapping['author'][author_id]
		affiliation_id = mapping['affiliation'][affiliation_id]
		new_links.append((author_id, affiliation_id, weight))
	for (affiliation_id, keyword_id, weight) in year_data['affiliation_keyword']:
		affiliation_id = mapping['affiliation'][affiliation_id]
		keyword_id = mapping['keyword'][keyword_id]
		new_links.append((affiliation_id, keyword_id, weight))

	for source, target, weight in new_links:
		cur_links.append(
			{
				'source': source,
				'target': target,
				'type': 'outer',
				'rate': weight,
			}
		)
	result['data'][year_data['year']] = {
			'nodes': cur_nodes,
			'links': cur_links,
	}

print json.dumps(result, indent=2)
