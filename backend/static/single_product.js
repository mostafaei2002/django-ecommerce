/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/js/single_product.js":
/*!***************************************!*\
  !*** ./frontend/js/single_product.js ***!
  \***************************************/
/***/ (() => {

eval("const navTabs = document.querySelector(\".nav-tabs\");\nconst tabBtns = document.querySelectorAll(\".nav-tabs .nav-link\");\nconst tabIDs = [\"tab-description\", \"tab-reviews\"];\n\nnavTabs.addEventListener(\"click\", (e) => {\n    const targetTabBtn = e.target.closest(\".nav-link\");\n    console.log(targetTabBtn);\n    tabBtns.forEach((tab) => tab.classList.remove(\"active\"));\n\n    targetTabBtn.classList.add(\"active\");\n    const targetTabID = targetTabBtn.dataset.target;\n    console.log(targetTabID);\n\n    tabIDs.forEach((tabID) => {\n        const tab = document.getElementById(tabID);\n        tab.classList.add(\"d-none\");\n    });\n\n    const targetTab = document.getElementById(targetTabID);\n    targetTab.classList.remove(\"d-none\");\n});\n\n\n//# sourceURL=webpack://django-ecommerce/./frontend/js/single_product.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./frontend/js/single_product.js"]();
/******/ 	
/******/ })()
;