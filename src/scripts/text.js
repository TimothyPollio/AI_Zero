function format(string) {
  if (string[0] == "-") {
    return string
  }
  return " " + string
}

function addText(selection, attribute, yOffset) {
  selection.append("text")
           .attr("transform", "translate(0," + yOffset + ")")
           .text(d => attribute + ":" + format(d.data[attribute]))
}
