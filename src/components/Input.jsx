import React, { useState } from "react";
import Select from 'react-select';
export default function Input({ onSend, onTop }) {
const selectableOptions = [
  { value: 'Politics',label: 'Politics' },
  { value: 'Health care',label:'Healthcare' },
  { value: 'Education',label:'Education' },
  { value: 'Technology', label:'Technology' },
  { value: 'Environment', label:'Environment' },
  { value: 'All', label: 'All'},
  { value: 'Chitchat', label: 'Chitchat'}


]


  const [topic, setTopic] = useState("");

  const [text, setText] = useState("");
  // console.log(topic);
  const handleInputChange = e => {
    setText(e.target.value);
    
  };
  const handleSend = (e,f) => {
    e.preventDefault();
    onSend(text);
    setText("");  
    // e.preventDefault();
    onTop(topic);
    setTopic(""); 
    
  };
  // console.log(text, topic)
  return (
    <div className="input">
     
   
      <form onSubmit={handleSend}>
      <div className="drop" >
      <Select
        className="input-cont"
        menuPlacement="top"
        placeholder= "Select a topic"
        onChange={(e)=>setTopic(e.value)}
        options={selectableOptions}
        topic ={topic}
      />
    </div>
        <input
          type="text"
          onChange={handleInputChange}
          value={text}
          validator
          placeholder="Enter your message here"
        />
         
        <button>
      
          <svg
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 500 500"
          >
            <g>
              <g>
                <polygon points="0,497.25 535.5,267.75 0,38.25 0,216.75 382.5,267.75 0,318.75" />
              </g>
            </g>
          </svg>
        </button>
      </form>
    </div>
  );
}
