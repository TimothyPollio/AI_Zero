buttonWidth = String(d3.select("#board").attr("width") * 0.48) + "px";

verticalOffset = String(d3.select("#board").attr("height") * 1.025 +
                        d3.select("#board").node().getBoundingClientRect().top)
                        + "px";

d3.select("body")
  .append("button")
  .text("AI MOVE")
  .style("top", verticalOffset)
  .style("width", buttonWidth)
  .attr("height", 150)
  .attr("id", "AIbutton")
  .on("click", AIplay)
