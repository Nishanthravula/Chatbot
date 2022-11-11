import React, { useEffect, useRef } from "react";
import 'animate.css';


export default function Messages({ messages }) {
  const el = useRef(null);
  useEffect(() => {
    el.current.scrollIntoView({ block: "end", behavior: "smooth" });
  });
  return (
    <div className="messages animate__animated animate__bounceInLeft">
      {messages}
      <div id={"el"} ref={el} />
    </div>
  );
}
