import axios from 'axios';
// import React, { useState, useEffect } from "react";
const API ={
  GetChatbotResponse,
  newFunction,
}

function GetChatbotResponse (message){
      console.log("Inside GetChatbotResponse")
       
const type =`Content-Type: application/json`;
axios({
  method: 'POST',
  url: 'http://127.0.0.1:9999/bot',
  headers: {type}, 
  data: {
    "query": message,
    "topic":"Technology"
  }
}).then((res)=>
console.log("API Response is ",res)).catch((err)=>
console.log("Erros in API, error is ",err));

    // return data;
}
function newFunction(params) {
  
}

export default API;
