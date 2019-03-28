var squareSize = window.screen.width * 5 / 94;
var width = squareSize * 7;
var height = squareSize * 6;

var moveData = [];
var gameOver = false;
var fortyTwo = Array.from({length: 42}, i => 0)

// Create the board
d3.select("body")
  .append("svg")
  .attr("id", "board")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .selectAll("rect")
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
  .attr("id", (d,i) => "square" + String(i))
  .on("click", (d,i) => click(i))

function render() {

  var tr = d3.transition().duration(750)

  // Add/Update Xs & Os
  pieceSelection = d3.select('#board')
                     .selectAll('.piece')
                     .data(moveData)

  pieceSelection.enter()
                .append("text")
                .attr("class", "piece")
                .attr("x", d => ((d % 7) + 0.25) * squareSize)
                .attr("y", d => (~~(d / 7) + .75) * squareSize)
                .text(letter)
                .attr("stroke", color)
                .attr("stroke-width", 0.05 * squareSize)
                .attr("font-size", 0.8 * squareSize)

  pieceSelection.exit().remove()

  // Highlight latest move & remove previous highlight
  d3.select('#square' + String(moveData.slice(-1)[0]))
    .transition(tr)
    .attr('fill', '#ffff65')

  if (moveData.length > 1) {
    d3.select('#square' + String(moveData.slice(-2)[0]))
      .transition(tr)
      .attr('fill', 'white')
  }

  // Check for X wins
  Xs = moveData.filter((d,i) => (i+1) % 2)
  for (quad of winners) {
    if (quad.map(v => Xs.includes(v)).every(x => x)) {
      gameOver = true;
      for (v of quad) {
        d3.select('#square' + String(v))
          .transition(tr)
          .attr('fill', '#f98b8b')
      }
    }
  }

  // Check for O wins
  Os = moveData.filter((d,i) => i % 2)
  for (quad of winners) {
    if (quad.map(v => Os.includes(v)).every(x => x)) {
      gameOver = true;
      for (v of quad) {
        d3.select('#square' + String(v))
          .transition(tr)
          .attr('fill', '#93a0ed')
      }
    }
  }
}

function click(i){
  if (!gameOver){
    if (!moveData.includes(i+7) && i < 35) {
      click(i+7);
    } else if (!moveData.includes(i)) {
    moveData.push(i)
    render()
    }
  }
}

function AIplay() {
  if (moveData.length > 0) {
    game_history = moveData.join("-");
  } else {
    game_history = "START";
  }
  $.get('/get_move/' + game_history, move => click(Number(move)))
}

render();
