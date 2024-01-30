"use client";
import React, { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Click me</button>
      <p>You clicked {count} times.</p>
    </div>
  );
}

export default App;
