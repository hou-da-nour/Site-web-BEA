import React, { useState } from 'react';

const MenuSvg = ({ openNavigation, toggleNavigation }) => {
  return (
    <div
      className={`w-[40px] h-[30px] cursor-pointer flex flex-col items-center justify-center gap-3 duration-500
        ${openNavigation ? 'rotate-180' : ''}`}
      onClick={toggleNavigation} // Cela ferme le menu lorsqu'on clique
    >
      <span
        className={`h-[6px] rounded-full bg-[#CAF0F8] duration-500 
        ${openNavigation ? 'w-full rotate-45 absolute' : 'w-[80%]'}`}
      />
      <span
        className={`h-[6px] rounded-full bg-[#CAF0F8] duration-500 
        ${openNavigation ? 'scale-x-0 absolute' : 'w-full'}`}
      />
      <span
        className={`h-[6px] rounded-full bg-[#CAF0F8] duration-500 
        ${openNavigation ? 'w-full -rotate-45 absolute' : 'w-[80%]'}`}
      />
    </div>
  );
};

export default MenuSvg;
