import React from "react";

export default function UserMessage({ text }) {
  return (
    <div className="message-container">
      <div className="user-message animate__animated animate__bounceInUp">{text}</div>
    </div>
  );
}
