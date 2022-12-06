import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import "animate.css";
import "react-widgets/styles.css";
import BotMessage from "./components/BotMessage";
import UserMessage from "./components/UserMessage";
import Messages from "./components/Messages";
import Input from "./components/Input";

import API from "./ChatbotAPI";

import "./styles.css";
import Header from "./components/Header";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [userMessage, setuserMessage] = useState('')
  const [topic, settopic] = useState('')
  const [apiMessage, setapiMessage] = useState("");

  // useEffect(() => {
  //   async function loadWelcomeMessage() {
  //     setMessages([
  //       <BotMessage
  //         key="0"
  //         // fetchMessage={async () => await API.GetChatbotResponse("hi")}
  //         fetchMessage={API.GetChatbotResponse()}
  //       />,
  //     ]);
  //   }
  //   loadWelcomeMessage();
  // }, []);

  async function getAPIMessage() {
    if(userMessage){
    console.log("Message is ", userMessage);
    console.log("topic is ", topic);  
    const type = `Content-Type: application/json`;
    axios({
      method: "POST",
      url: "http://34.27.136.111:9999/bot",
      headers: { type },
      data: {
        query: userMessage,
        topic: topic?topic:"Polictics",
      },
    })
      .then((res) => {
        setapiMessage(res.data)
        console.log("Response Recorded");
        setMessages(
          [
            ...messages,
              <BotMessage
              key="0"
                // fetchMessage={async () => await API.GetChatbotResponse("hi")}
              fetchMessage={res.data}
          />
            ]);
      })
      .catch((err) => console.log("Erros in API, error is ", err));
    }
  }

  useEffect(() => {
     getAPIMessage().then().catch((err)=> console.log("Errors"));
  }, [topic,userMessage])
  
  const send = async (text) => {
    setuserMessage(text)
    const newMessages = messages.concat(
      <UserMessage key={messages.length + 1} text={text} />,
    );
    setMessages(newMessages);
  };
const topicMethod = async (text) => {
    settopic(text);

   
  };
  return (
    <div className="chatbot container">
      <Header />
      <Messages messages={messages} />
      <Input onSend={send} onTop={topicMethod} />
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Chatbot />, rootElement);
