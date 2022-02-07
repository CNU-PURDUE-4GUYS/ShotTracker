import { createBoard } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".app");
  const websocket = new WebSocket("ws://localhost:8888/");
  createBoard(board);
  
});