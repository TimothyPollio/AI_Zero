var width = window.screen.width;
var height = window.screen.height;
var x_base = width / 2 - boardWidth * 1.5;
var y_base = squareSize;

var fortyTwo = Array.from({length: 42}, i => 0)
var treeData = listToTree(tree_data);
var root = d3.hierarchy(treeData);
var tree = d3.tree().nodeSize([boardWidth * 1.7, boardHeight * 1.25]);

// Setup canvas, scroll, zoom
var canvas = d3.select("body")
               .append("svg")
               .attr("width", width)
               .attr("height", height)
               .call(d3.zoom()
                       .on("zoom", function () { var k = d3.event.transform.k;
                                                 var xt = k * (d3.event.transform.x / k + x_base);
                                                 var yt = k * (d3.event.transform.y / k + y_base);
                                                 trans_string = "translate(" + xt +
                                                                "," + yt + ")" +
                                                                "scale(" + k + ")"
                                                 canvas.attr("transform", trans_string);}))
               .append("g");

d3.select("svg").on("dblclick.zoom", null);
d3.select("svg").select("g").attr("transform", "translate(" + x_base + "," + y_base + ")scale(1)");

function render() {

  var t = tree(root);
  var nodes = t.descendants();
  var links = t.links();
  var tr = d3.transition().duration(750);

  // Abstract nodes
  var nodeSelection = canvas.selectAll(".node")
                            .data(nodes, d => d.data.ID);

  var nodeEnter = nodeSelection.enter()
                               .append("g")
                               .attr("class", "node")
                               .attr("transform", d => "translate(" + parentCoords(d) + ")")
                               .attr("id", d => "BOARD" + d.data.ID)
                               .on("click", expand);

  nodeEnter.merge(nodeSelection)
           .transition(tr)
           .attr("transform", d => "translate(" + d.x + "," + d.y + ")");

  nodeSelection.exit().remove();

  // Text labels
  var text = nodeEnter.append("g")
                      .attr("stroke", "black")
                      .attr("stroke-width", 0.01 * squareSize)
                      .attr("font-family", "monospace")
                      .attr("font-size", 0.8 * squareSize)
                      .attr("transform",
                            "translate(" + (boardWidth + squareSize / 5) + ",0)");

  ["N", "Q", "V", "P", "U"].forEach((attr,i) => addText(text, attr, (i + 0.8) * squareSize));

  for (var d of nodes){
    // Boards
    d3.select('#BOARD' + d.data.ID)
      .selectAll('rect')
      .data(fortyTwo)
      .enter()
      .append("rect")
      .attr("x", (d,i) => (i % 7) * squareSize)
      .attr("y", (d,i) => ~~(i/7) * squareSize)
      .attr("width", squareSize)
      .attr("height", squareSize)
      .attr("fill", "transparent")
      .attr("stroke", "black")
      .attr("stroke-width", 0.6)

    // Pieces
    if (d.data.ID.length > 0){
      d3.select('#BOARD' + d.data.ID)
        .selectAll('.piece')
        .data(d.data.ID.split("-"))
        .enter()
        .append("text")
        .attr("class", "piece")
        .attr("x", d => ((d % 7) + 0.25) * squareSize)
        .attr("y", d => (~~(d / 7) + .75) * squareSize)
        .text(letter)
        .attr("stroke", color)
        .attr("stroke-width", 0.06 * squareSize)
        .attr("font-size", 0.8 * squareSize)
    }
  }

  // Links
  var linkSelection = canvas.selectAll(".link")
                            .data(links, d => d.target.data.ID)

  var linkEnter = linkSelection.enter()
                               .append("g")
                               .attr("class", "link")

  linkEnter.append("path")
           .attr("fill", "none")
           .attr("stroke", "white")
           .attr("stroke-width", 1)
           .attr("d", d => link({'source': d.source,
                                 'target': d.source}))

  linkEnter.merge(linkSelection)
           .select("path")
           .transition(tr)
           .attr("stroke", "#8591a3")
           .attr("d", link)

  linkSelection.exit().remove()
}

collapse(root);
expand(root);
