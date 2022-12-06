import React, { useState, useEffect } from "react";


export default function UserMessage({ text }) {
  // const [isLoading, setLoading] = useState(true);
  // const [text, setText] = useState("");

  // useEffect(() => {
  //   async function loadMessage() {
  //     const txt = await fetchText();
  //     setLoading(false);
  //     setText(txt);
  //   }
  //   loadMessage();
  // }, [fetchText]);
  return (
    <div className="message-container">
      <div className="user-message animate__animated animate__bounceInUp">{text}</div>
    </div>
  );
}
