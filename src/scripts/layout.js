var squareSize = window.screen.width / 94;
var boardWidth = squareSize * 7;
var boardHeight = squareSize * 6;

function listToTree(list) {
  var root, index = {};
  list.forEach(function(node){
    index[node.ID] = node;
    node.children = [];
  })
  list.forEach(function(node){
    if (node.parentID != 'None') {
      index[node.parentID].children.push(node);
    } else {
      root = node;
    }
  })
  return root;
}

function collapse(el){
  if (el.children) {
    el.collapsed = el.children.slice();
    el.children.forEach(collapse);
    el.children = null;
  }
}

function expand(el) {
  if (!el.children) {
    el.children = el.collapsed;
  } else {
    collapse(el);
  }
  render()
}

function parentCoords(d) {
  if (d.parent) {
    return d.parent.x + "," + d.parent.y
  } else {
    return d.x + "," + d.y
  }
}

var link = d3.linkVertical()
             .source(d => [d.source.x + boardWidth / 2, d.source.y + boardHeight + squareSize / 25])
             .target(d => [d.target.x + boardWidth / 2, d.target.y - squareSize / 25])
