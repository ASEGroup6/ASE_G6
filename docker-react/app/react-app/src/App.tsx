import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

export default function MyApp() {
  return (
    <div>
      <MyContents />
    </div>
  );
}

function MyContents(){
  return (
    <div id='contents'>
      <h1></h1>
      <img src="/images/スタンプカード夏.png"
      style={{
        width: "1000px",
      }} />
      <h2></h2>
      <MyButton />
      <MyButton />
    </div>
  );
}

function MyButton() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}
