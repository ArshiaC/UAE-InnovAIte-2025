let usernameRef = document.getElementById("username");
let passwordRef = document.getElementById("password");
let eyeL = document.querySelector(".eyeball-l");
let eyeR = document.querySelector(".eyeball-r");
let pawL = document.querySelector(".paw-l");
let pawR = document.querySelector(".paw-r");

let normalEyeStyle = () => {
  eyeL.style.cssText = `
    left: 0.45em;
    top: 0.3em;
  `;
  eyeR.style.cssText = `
    right: 0.45em;
    top: 0.3em;
  `;
};

let normalPawStyle = () => {
  pawL.style.cssText = `
        height: 3.5em;
        top: 8.4em;
        left: 7.5em;
        transform: rotate(0deg);
    `;
  pawR.style.cssText = `
        height: 3.5em;
        top: 8.4em;
        right: 7.5em;
        transform: rotate(0deg)
    `;
};

// When clicked on username input
usernameRef.addEventListener("focus", () => {
  eyeL.style.cssText = `
    left: 0.45em;
    top: 0.1em;  
  `;
  eyeR.style.cssText = `
    right: 0.45em;
    top: 0.1em;
  `;
  normalPawStyle();
});

// When clicked on password input
passwordRef.addEventListener("focus", () => {
  pawL.style.cssText = `
        height: 7.5em;
        top: 3.87em;
        left: 11.75em;
        transform: rotate(-155deg);    
    `;
  pawR.style.cssText = `
        height: 7.5em;
        top: 3.87em;
        right: 11.75em;
        transform: rotate(155deg);
    `;
  normalEyeStyle();
});

// When clicked outside username and password input
document.addEventListener("click", (e) => {
  let clickedElem = e.target;
  if (clickedElem != usernameRef && clickedElem != passwordRef) {
    normalEyeStyle();
    normalPawStyle();
  }
});

// Add ear wiggle on form load for cute effect
window.addEventListener("load", () => {
  const earL = document.querySelector(".ear-l");
  const earR = document.querySelector(".ear-r");
  
  setTimeout(() => {
    earL.style.transform = "rotate(-25deg)";
    earR.style.transform = "rotate(25deg)";
    
    setTimeout(() => {
      earL.style.transform = "rotate(-15deg)";
      earR.style.transform = "rotate(15deg)";
    }, 300);
  }, 500);
});