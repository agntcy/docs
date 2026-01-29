performance.mark("js-parse-end:78298-4461f83ccb79.js");
"use strict";(globalThis.webpackChunk_github_ui_github_ui=globalThis.webpackChunk_github_ui_github_ui||[]).push([[78298],{913:(e,t,o)=>{o.r(t),o.d(t,{apply:()=>R,injectStyles:()=>C,isPolyfilled:()=>H,isSupported:()=>D});var n=class extends Event{oldState;newState;constructor(e,{oldState:t="",newState:o="",...n}={}){super(e,n),this.oldState=String(t||""),this.newState=String(o||"")}},r=new WeakMap;function i(e,t,o){r.set(e,setTimeout(()=>{r.has(e)&&e.dispatchEvent(new n("toggle",{cancelable:!1,oldState:t,newState:o}))},0))}var l=globalThis.ShadowRoot||function(){},a=globalThis.HTMLDialogElement||function(){},u=new WeakMap,p=new WeakMap,s=new WeakMap;function c(e){return s.get(e)||"hidden"}var f=new WeakMap;function d(e,t){return!("auto"!==e.popover&&"manual"!==e.popover||!e.isConnected||t&&"showing"!==c(e)||!t&&"hidden"!==c(e)||e instanceof a&&e.hasAttribute("open"))&&document.fullscreenElement!==e}function h(e){return e?Array.from(p.get(e.ownerDocument)||[]).indexOf(e)+1:0}function m(e){let t=p.get(e);for(let e of t||[])if(e.isConnected)return e;else t.delete(e);return null}function g(e){return"function"==typeof e.getRootNode?e.getRootNode():e.parentNode?g(e.parentNode):e}function v(e){for(;e;){if(e instanceof HTMLElement&&"auto"===e.popover&&"showing"===s.get(e))return e;if((e=e instanceof Element&&e.assignedSlot||e.parentElement||g(e))instanceof l&&(e=e.host),e instanceof Document)return}}var w=new WeakMap;function b(e){if(!d(e,!1))return;let t=e.ownerDocument;if(!e.dispatchEvent(new n("beforetoggle",{cancelable:!0,oldState:"closed",newState:"open"}))||!d(e,!1))return;let o=!1;if("auto"===e.popover){let o=e.getAttribute("popover");if(T(function(e){let t=new Map,o=0;for(let n of p.get(e.ownerDocument)||[])t.set(n,o),o+=1;t.set(e,o),o+=1;let n=null;return!function(e){let o=v(e);if(null===o)return;let r=t.get(o);(null===n||t.get(n)<r)&&(n=o)}(e.parentElement||g(e)),n}(e)||t,!1,!0),o!==e.getAttribute("popover")||!d(e,!1))return}m(t)||(o=!0),w.delete(e);let r=t.activeElement;e.classList.add(":popover-open"),s.set(e,"showing"),u.has(t)||u.set(t,new Set),u.get(t).add(e),(function(e){if(e.shadowRoot&&!0!==e.shadowRoot.delegatesFocus)return null;let t=e;t.shadowRoot&&(t=t.shadowRoot);let o=t.querySelector("[autofocus]");if(o)return o;for(let e of t.querySelectorAll("slot"))for(let t of e.assignedElements({flatten:!0}))if(t.hasAttribute("autofocus"))return t;else if(o=t.querySelector("[autofocus]"))return o;let n=e.ownerDocument.createTreeWalker(t,NodeFilter.SHOW_ELEMENT),r=n.currentNode;for(;r;){var i;if(!((i=r).hidden||i instanceof l||(i instanceof HTMLButtonElement||i instanceof HTMLInputElement||i instanceof HTMLSelectElement||i instanceof HTMLTextAreaElement||i instanceof HTMLOptGroupElement||i instanceof HTMLOptionElement||i instanceof HTMLFieldSetElement)&&i.disabled||i instanceof HTMLInputElement&&"hidden"===i.type||i instanceof HTMLAnchorElement&&""===i.href)&&"number"==typeof i.tabIndex&&-1!==i.tabIndex)return r;r=n.nextNode()}})(e)?.focus(),"auto"===e.popover&&(p.has(t)||p.set(t,new Set),p.get(t).add(e),A(f.get(e),!0)),o&&r&&"auto"===e.popover&&w.set(e,r),i(e,"closed","open")}function y(e,t=!1,o=!1){if(!d(e,!0))return;let r=e.ownerDocument;if("auto"===e.popover&&(T(e,t,o),!d(e,!0))||(A(f.get(e),!1),f.delete(e),o&&(e.dispatchEvent(new n("beforetoggle",{oldState:"open",newState:"closed"})),!d(e,!0))))return;u.get(r)?.delete(e),p.get(r)?.delete(e),e.classList.remove(":popover-open"),s.set(e,"hidden"),o&&i(e,"open","closed");let l=w.get(e);l&&(w.delete(e),t&&l.focus())}function E(e,t=!1,o=!1){let n=m(e);for(;n;)y(n,t,o),n=m(e)}function T(e,t,o){let n=e.ownerDocument||e;if(e instanceof Document)return E(n,t,o);let r=null,i=!1;for(let t of p.get(n)||[])if(t===e)i=!0;else if(i){r=t;break}if(!i)return E(n,t,o);for(;r&&"showing"===c(r)&&p.get(n)?.size;)y(r,t,o)}var S=new WeakMap;function M(e){let t,o;if(!e.isTrusted)return;let n=e.composedPath()[0];if(!n)return;let r=n.ownerDocument;if(!m(r))return;let i=(t=v(n),o=function(e){for(;e;){let t=e.popoverTargetElement;if(t instanceof HTMLElement)return t;if((e=e.parentElement||g(e))instanceof l&&(e=e.host),e instanceof Document)return}}(n),h(t)>h(o)?t:o);if(i&&"pointerdown"===e.type)S.set(r,i);else if("pointerup"===e.type){let e=S.get(r)===i;S.delete(r),e&&T(i||r,!1,!0)}}var L=new WeakMap;function A(e,t=!1){if(!e)return;L.has(e)||L.set(e,e.getAttribute("aria-expanded"));let o=e.popoverTargetElement;if(o instanceof HTMLElement&&"auto"===o.popover)e.setAttribute("aria-expanded",String(t));else{let t=L.get(e);t?e.setAttribute("aria-expanded",t):e.removeAttribute("aria-expanded")}}var k=globalThis.ShadowRoot||function(){};function D(){return"u">typeof HTMLElement&&"object"==typeof HTMLElement.prototype&&"popover"in HTMLElement.prototype}function H(){return!!(document.body?.showPopover&&!/native code/i.test(document.body.showPopover.toString()))}function x(e,t,o){let n=e[t];Object.defineProperty(e,t,{value(e){return n.call(this,o(e))}})}var P=/(^|[^\\]):popover-open\b/g,N=null;function C(e){let t,o=(t="function"==typeof globalThis.CSSLayerBlockRule,`
${t?"@layer popover-polyfill {":""}
  :where([popover]) {
    position: fixed;
    z-index: 2147483647;
    inset: 0;
    padding: 0.25em;
    width: fit-content;
    height: fit-content;
    border-width: initial;
    border-color: initial;
    border-image: initial;
    border-style: solid;
    background-color: canvas;
    color: canvastext;
    overflow: auto;
    margin: auto;
  }

  :where([popover]:not(.\\:popover-open)) {
    display: none;
  }

  :where(dialog[popover].\\:popover-open) {
    display: block;
  }

  :where(dialog[popover][open]) {
    display: revert;
  }

  :where([anchor].\\:popover-open) {
    inset: auto;
  }

  :where([anchor]:popover-open) {
    inset: auto;
  }

  @supports not (background-color: canvas) {
    :where([popover]) {
      background-color: white;
      color: black;
    }
  }

  @supports (width: -moz-fit-content) {
    :where([popover]) {
      width: -moz-fit-content;
      height: -moz-fit-content;
    }
  }

  @supports not (inset: 0) {
    :where([popover]) {
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
    }
  }
${t?"}":""}
`);if(null===N)try{(N=new CSSStyleSheet).replaceSync(o)}catch{N=!1}if(!1===N){let t=document.createElement("style");t.textContent=o,e instanceof Document?e.head.prepend(t):e.prepend(t)}else e.adoptedStyleSheets=[N,...e.adoptedStyleSheets]}function R(){var e;if("u"<typeof window)return;function t(e){return e?.includes(":popover-open")&&(e=e.replace(P,"$1.\\:popover-open")),e}window.ToggleEvent=window.ToggleEvent||n,x(Document.prototype,"querySelector",t),x(Document.prototype,"querySelectorAll",t),x(Element.prototype,"querySelector",t),x(Element.prototype,"querySelectorAll",t),x(Element.prototype,"matches",t),x(Element.prototype,"closest",t),x(DocumentFragment.prototype,"querySelectorAll",t),Object.defineProperties(HTMLElement.prototype,{popover:{enumerable:!0,configurable:!0,get(){if(!this.hasAttribute("popover"))return null;let e=(this.getAttribute("popover")||"").toLowerCase();return""===e||"auto"==e?"auto":"manual"},set(e){null===e?this.removeAttribute("popover"):this.setAttribute("popover",e)}},showPopover:{enumerable:!0,configurable:!0,value(){b(this)}},hidePopover:{enumerable:!0,configurable:!0,value(){y(this,!0,!0)}},togglePopover:{enumerable:!0,configurable:!0,value(e){"showing"===s.get(this)&&void 0===e||!1===e?y(this,!0,!0):(void 0===e||!0===e)&&b(this)}}});let o=Element.prototype.attachShadow;o&&Object.defineProperties(Element.prototype,{attachShadow:{enumerable:!0,configurable:!0,writable:!0,value(e){let t=o.call(this,e);return C(t),t}}});let r=HTMLElement.prototype.attachInternals;r&&Object.defineProperties(HTMLElement.prototype,{attachInternals:{enumerable:!0,configurable:!0,writable:!0,value(){let e=r.call(this);return e.shadowRoot&&C(e.shadowRoot),e}}});let i=new WeakMap;function l(e){Object.defineProperties(e.prototype,{popoverTargetElement:{enumerable:!0,configurable:!0,set(e){if(null===e)this.removeAttribute("popovertarget"),i.delete(this);else if(e instanceof Element)this.setAttribute("popovertarget",""),i.set(this,e);else throw TypeError("popoverTargetElement must be an element or null")},get(){if("button"!==this.localName&&"input"!==this.localName||"input"===this.localName&&"reset"!==this.type&&"image"!==this.type&&"button"!==this.type||this.disabled||this.form&&"submit"===this.type)return null;let e=i.get(this);if(e&&e.isConnected)return e;if(e&&!e.isConnected)return i.delete(this),null;let t=g(this),o=this.getAttribute("popovertarget");return(t instanceof Document||t instanceof k)&&o&&t.getElementById(o)||null}},popoverTargetAction:{enumerable:!0,configurable:!0,get(){let e=(this.getAttribute("popovertargetaction")||"").toLowerCase();return"show"===e||"hide"===e?e:"toggle"},set(e){this.setAttribute("popovertargetaction",e)}}})}l(HTMLButtonElement),l(HTMLInputElement);(e=document).addEventListener("click",e=>{let t=e.composedPath(),o=t[0];if(!(o instanceof Element)||o?.shadowRoot)return;let n=g(o);if(!(n instanceof k||n instanceof Document))return;let r=t.find(e=>e.matches?.("[popovertargetaction],[popovertarget]"));if(r){!function(e){let t=e.popoverTargetElement;if(!(t instanceof HTMLElement))return;let o=c(t);"show"===e.popoverTargetAction&&"showing"===o||("hide"!==e.popoverTargetAction||"hidden"!==o)&&("showing"===o?y(t,!0,!0):d(t,!1)&&(f.set(t,e),b(t)))}(r),e.preventDefault();return}}),e.addEventListener("keydown",e=>{let t=e.key,o=e.target;!e.defaultPrevented&&o&&("Escape"===t||"Esc"===t)&&T(o.ownerDocument,!0,!0)}),e.addEventListener("pointerdown",M),e.addEventListener("pointerup",M),C(document)}},5225:(e,t,o)=>{function n(...e){return JSON.stringify(e,(e,t)=>"object"==typeof t?t:String(t))}function r(e,t={}){let{hash:o=n,cache:i=new Map}=t;return function(...t){let n=o.apply(this,t);if(i.has(n))return i.get(n);let r=e.apply(this,t);return r instanceof Promise&&(r=r.catch(e=>{throw i.delete(n),e})),i.set(n,r),r}}o.d(t,{A:()=>r})},36301:(e,t,o)=>{let n;function r(){return`${Math.round(0x7fffffff*Math.random())}.${Math.round(Date.now()/1e3)}`}function i(){try{let e=function(){let e,t=document.cookie.match(/_octo=([^;]+)/g);if(!t)return;let o=[0,0];for(let n of t){let[,t]=n.split("="),[,r,...i]=t.split("."),l=r.split("-").map(Number);l>o&&(o=l,e=i.join("."))}return e}();if(e)return e;let t=r();return!function(e){let t=`GH1.1.${e}`,o=new Date(Date.now()+31536e6).toUTCString(),{domain:n}=document;n.endsWith(".github.com")&&(n="github.com"),document.cookie=`_octo=${t}; expires=${o}; path=/; domain=${n}; secure; samesite=lax`}(t),t}catch(e){return n||(n=r()),n}}o.d(t,{y:()=>i})},70170:(e,t,o)=>{function n(e,t=0,{start:o=!0,middle:r=!0,once:i=!1}={}){let l,a=o,u=0,p=!1;function s(...n){if(p)return;let c=Date.now()-u;u=Date.now(),o&&r&&c>=t&&(a=!0),a?(a=!1,e.apply(this,n),i&&s.cancel()):(r&&c<t||!r)&&(clearTimeout(l),l=setTimeout(()=>{u=Date.now(),e.apply(this,n),i&&s.cancel()},r?t-c:t))}return s.cancel=()=>{clearTimeout(l),p=!0},s}function r(e,t=0,{start:o=!1,middle:i=!1,once:l=!1}={}){return n(e,t,{start:o,middle:i,once:l})}o.d(t,{n:()=>n,s:()=>r})}}]);
//# sourceMappingURL=78298-c1240397d865.js.map