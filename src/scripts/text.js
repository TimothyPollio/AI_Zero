function format(string) {
  if (string[0] == "-") {
    return string.slice(0, -1)
  }
  return " " + string
}

function addText(selection, attribute, yOffset) {
  selection.append("text")
           .attr("transform", "translate(0," + yOffset + ")")
           .text(d => attribute + ":" + format(d.data[attribute]))
}
