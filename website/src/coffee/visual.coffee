color = d3.scale.category10()

getSvgBox = () ->
  el = document.querySelector '#svg-wrap'
  return el.getBoundingClientRect()

svg = d3.select("#main-view")
box = getSvgBox()

force = d3.layout.force()
  .charge(-900)
  .linkDistance(100)
  .size([box.width, box.height])
  .alpha(1)

graph = null
links = force.links()
nodes = force.nodes()
link = svg.selectAll(".link")
node = svg.selectAll(".node")
currentDataset = null
years = null
last_detail_node = 3

showLink = (data) ->
  html = ''
  if data
    html += '<table>'
    html += '<tr>'
    html += "<th>From</th>"
    html += "<td>#{data.source.name}</td>"
    html += '</tr>'
    html += '<tr>'
    html += "<th>To</th>"
    html += "<td>#{data.target.name}</td>"
    html += '</tr>'
    html += '<tr>'
    html += "<th>Weight</th>"
    html += "<td>#{data.rate || 0}</td>"
    html += '</tr>'
    html += '</table>'

  (document.getElementById 'explaination-link').innerHTML = html

showDetail = (data) ->
  last_detail_node = data.index
  html = '<table>'
  html += '<tr>'
  html += "<th>Category</th>"
  html += "<td>#{data.category}</td>"
  html += '</tr>'

  html += '<tr>'
  html += "<th>Name</th>"
  html += "<td>#{data.name}</td>"
  html += '</tr>'

  html += '<tr>'
  html += "<th>Weight</th>"
  html += "<td>#{data.rate || 0}</td>"
  html += '</tr>'
  html += '</table>'

  (document.getElementById 'explaination-node').innerHTML = html

setMetaAnchor = () ->
  box = getSvgBox()
  y = box.height * 0.5
  offset = box.width / 20
  nodes = currentDataset.nodes
  nodes[0].x = nodes[0].px = offset
  nodes[1].x = nodes[1].px = box.width / 2
  nodes[2].x = nodes[2].px = box.width - offset
  for i in [0...3]
    nodes[i].y = nodes[i].py = y
    nodes[i].fixed = true

loaded = []

lastChoice = 0
update = (_index) ->
  (document.getElementById 'year-title').innerText = years[_index]
  year = years[_index]
  last = graph[years[lastChoice]]
  lastChoice = _index
  cur = currentDataset = graph[year]
  for i in [0...last.nodes.length]
    d = cur.nodes[i]
    s = last.nodes[i]
    for key in ['index', 'x', 'y', 'px', 'py', 'fixed', 'weight']
      d[key] = s[key]
  setMetaAnchor()
  force
    .nodes(cur.nodes)
    .links(cur.links)
    .linkStrength( (d) ->
      if d.rate
        return d.rate / 200
      return .1
    )
    .linkDistance( (d) ->
      if d.type == "inner"
        return 50
      else if d.type == "outer"
        return 400
      else
        return 10
    )
  if not loaded[_index]
    force.start()
    loaded[_index] = true
  else
    force.resume()

  showDetail cur.nodes[last_detail_node]
  showLink()

  link = svg.selectAll(".link").data(cur.links)
  link.enter()
    .append("line")
    .attr("class", (d) ->
      switch d.type
        when "inner", "outer"
          return "link"
        when "metalink" then return "metalink link"
        else
          throw 'not support type'
    )
  link.exit().remove()
  link.transition()
    .duration(850)
    .style("stroke-width", (d) ->
      if d.rate
        return Math.sqrt(d.rate) / 2
      return 2
    )
    .attr("class", (d) ->
      switch d.type
        when "inner", "outer"
          return "link"
        when "metalink" then return "metalink link"
        else
          throw 'not support type'
    )

  node = svg.selectAll(".node").data(cur.nodes, (d) -> d.index)
  nodeG = node.enter()
    .append("g")
    .attr("class", (d) ->
      switch d.type
        when "normal" then return "node"
        when "meta" then return "meta node"
        else
          throw 'not support type'
    )
    .call(force.drag)

  nodeG
    .append("circle")
    .attr("r", 10)
    .style("opacity", 1)

  nodeG.append("text")
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text( (d) ->
      return d.name
    )
  nodeG.append("title")
    .text((d) ->
      d.name
    )
  node.exit().remove()

  node.transition()
    .duration(350)
    .select("circle")
      .attr("r", (d) ->
        #TODO map to a linear space
        if d.type is "meta"
          return 10
        if d.rate
          return d.rate * 50
        else
          return 10
      )
      .style("opacity", (d) ->
        if d.type == "meta"
          return 0.2
        else
          if d.rate
            return 1
          else
            return 0.5
      )
      .attr("fill", (d) ->
        return (color d.category)
      )
  node.on 'mouseenter', (d) ->
    showDetail d
  link.on 'mouseenter', (d) ->
    if d.type in ['inner', 'outer']
      showLink d

  priority = {
    inner: 0
    outer: 1
    normal: 10
    metalink: 0
  }
  svg.selectAll(".node, .link").sort( (a, b) ->
    if priority[a.type] > priority[b.type]
      return 1
    return -1
  )
  return

d3.json "graph.json", (error, graphJSON) ->
  years = graphJSON.year_description
  graph = graphJSON.data
  offset =
    author: -1
    affiliation: 0
    keyword: 1

  force.on "tick", (e) ->
    k = 3 * e.alpha
    currentDataset.nodes.forEach (o) ->
      o.x += offset[o.category] * k
      return

    link.attr("x1", (d) ->
      d.source.x
    ).attr("y1", (d) ->
      d.source.y
    ).attr("x2", (d) ->
      d.target.x
    ).attr "y2", (d) ->
      d.target.y

    node.attr("transform", (d) ->
      return "translate(#{d.x},#{d.y})"
    )
    return

  update 0
  scollbar = document.getElementById 'year-select'

  scollbar.onchange = (e) ->
    update parseInt @.value
    return false
  keymap =
    37: -1
    39: +1
  window.onkeydown = (e) ->
    if value = keymap[e.keyCode]
      newValue = parseInt(scollbar.value) + value
      if 0 <= newValue < years.length
        scollbar.value = newValue
        update newValue

  window.onresize = (e) ->
    box = getSvgBox()
    force.size([box.width, box.height])
    update lastChoice
  return
