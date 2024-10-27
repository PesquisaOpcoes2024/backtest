import React, { useState } from 'react';
import MenuPrincipal from './components/MenuPrincipal/MenuPrincipal';
import Grafico from './Grafico/Grafico';
import './App.css'

const App = () => {

  return (
    <div className="App">
      <MenuPrincipal/>
      <Grafico/>
    </div>
  );
}

export default App;
