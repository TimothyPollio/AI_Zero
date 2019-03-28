// Generate winners list
horizontal = [0,  1,  2,  3];
vertical   = [0,  7,  14, 21];
diagonal1  = [0,  8,  16, 24];
diagonal2  = [21, 15, 9,  3];
quads = [horizontal, vertical, diagonal1, diagonal2];
winners = []
for (index=0; index<4; index++){
  for (i=0; i<[4,7,4,4][index]; i++){
    for (j=0; j<[6,3,3,3][index]; j++) {
      winners.push(quads[index].map(v => v + i + 7 * j));
    }
  }
}

function letter(d, i){
  if(i%2 == 0) {return "X"}
  return "O"
}

function color(d, i){
 if(i%2 == 0) {return "#a82312"}
 return "#1f3eaf"
}
