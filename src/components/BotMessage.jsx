import React, { useState, useEffect } from "react";

export default function BotMessage({ fetchMessage,fetchtopic }) {
  const [isLoading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  // const [topic, setTopic] = useState("");
  useEffect(() => {
    if(fetchMessage){
     async function loadMessage() {
      // const msg = await fetchMessage();
      
          setLoading(false);
          setMessage(fetchMessage);
    }
    loadMessage();
  }
  }, [fetchMessage]);
  // useEffect(() => {
  //   async function loadTopic() {
  //     const top = await fetchtopic();
  //     setLoading(false);
  //     setTopic(top);
  //   }
  //   loadTopic();
  // }, [fetchtopic]);
  

  // console.log({message})
  return (
   <>
     {/* {message?message.length>0?   */}
    <div className="message-container">
     <div className="bot-message">{message?message:null}</div>
    </div>

    {/* :null:null} */}
   </>
  );
}
