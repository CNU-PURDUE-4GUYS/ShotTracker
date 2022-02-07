const PLAYER1 = "red";

const PLAYER2 = "yellow";

function createBoard(board) {
  // Inject stylesheet.
  const linkElement = document.createElement("link");
  linkElement.href = import.meta.url.replace(".js", ".css");
  linkElement.rel = "stylesheet";
  document.head.append(linkElement);
  // Generate board.
  for (let column = 0; column < 7; column++) {
    const columnElement = document.createElement("div");
    columnElement.className = "column";
    columnElement.dataset.column = column;
    for (let row = 0; row < 6; row++) {
      const cellElement = document.createElement("div");
      cellElement.className = "cell empty";
      cellElement.dataset.column = column;
      columnElement.append(cellElement);
    }
    board.append(columnElement);
  }
}
function send(){
  const event = {
    type: "play",
  };
  websocket.send(JSON.stringify(event));
}

export { PLAYER1, PLAYER2, createBoard };
