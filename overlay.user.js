// ==UserScript==
// @name         OneShot Logo template
// @namespace    http://vilolentmonkey.net/
// @downloadURL  https://github.com/prezmop/oneshot-place2023/raw/trunk/overlay.user.js
// @updateURL    https://github.com/prezmop/oneshot-place2023/raw/trunk/overlay.user.js
// @version      0.3
// @description  protect niko
// @author       oralekin, LittleEndu, GrayTurtles, hurrikate, prezmop
// @match        https://garlic-bread.reddit.com/embed*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=reddit.com
// @grant        none
// ==/UserScript==
if (window.top !== window.self) {
    window.addEventListener('load', () => {
        document.getElementsByTagName("garlic-bread-embed")[0].shadowRoot.children[0].getElementsByTagName("garlic-bread-canvas")[0].shadowRoot.children[0].appendChild(
            (function () {
                const i = document.createElement("img");
                i.src = "https://raw.githubusercontent.com/prezmop/oneshot-place2023/trunk/template.png";
                i.onload = () => {
                    if (i.width === i.height) {
                        i.style = "position: absolute;left: 0;top: 0;image-rendering: pixelated;width: 2000px;height: 2000px;";
                    } else {
                        i.style = "position: absolute;left: 0;top: 0;image-rendering: pixelated;width: 2000px;height: 2000px;";
                    }
                };
                return i;
            })())
    }, false);
}
