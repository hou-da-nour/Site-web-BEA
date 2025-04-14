import React from 'react';

const ButtonNavbar = () => {
  return (
    <div className="w-fit mx-auto">
      <button className=" hidden lg:flex 
        px-10 py-3 cursor-pointer
        text-[12px]  tracking-[2.5px] font-semibold
        text-[#03045E] bg-[#ADE8F4] rounded-full 
        shadow-[0px_8px_15px_rgba(0,0,0,0.1)] 
        transition-all duration-300 ease-in-out 
        hover:bg-[#48CAE4]  hover:shadow-[0px_15px_20px_rgba(3,4,94,0.4)]] 
        hover:-translate-y-[7px] 
        active:translate-y-[-1px]
        outline-none
      ">
        Click me
      </button>
    </div>
  );
};

export default ButtonNavbar;
