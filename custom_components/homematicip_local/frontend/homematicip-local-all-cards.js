import{setScheduleEnabled as e,setDeviceSchedule as t,reloadDeviceConfig as i,setClimateActiveProfile as s,setClimateScheduleWeekday as a,getSystemHealth as o,getDeviceStatistics as n,getIncidents as r,loadEntryEntityIds as l,getRadioLevels as d,dcLevelClass as c,csLevelClass as h,listDevices as p,getServiceMessages as u,getAlarmMessages as m,acknowledgeServiceMessage as g,acknowledgeAlarmMessage as _}from"@hmip/panel-api";function v(e,t,i,s){var a,o=arguments.length,n=o<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var r=e.length-1;r>=0;r--)(a=e[r])&&(n=(o<3?a(n):o>3?a(t,i,n):a(t,i))||n);return o>3&&n&&Object.defineProperty(t,i,n),n}"function"==typeof SuppressedError&&SuppressedError;
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const f=globalThis,y=f.ShadowRoot&&(void 0===f.ShadyCSS||f.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,b=Symbol(),x=new WeakMap;let w=class{constructor(e,t,i){if(this._$cssResult$=!0,i!==b)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(y&&void 0===e){const i=void 0!==t&&1===t.length;i&&(e=x.get(t)),void 0===e&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),i&&x.set(t,e))}return e}toString(){return this.cssText}};const $=(e,...t)=>{const i=1===e.length?e[0]:t.reduce((t,i,s)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[s+1],e[0]);return new w(i,e,b)},k=y?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>new w("string"==typeof e?e:e+"",void 0,b))(t)})(e):e,{is:S,defineProperty:E,getOwnPropertyDescriptor:T,getOwnPropertyNames:A,getOwnPropertySymbols:D,getPrototypeOf:C}=Object,M=globalThis,P=M.trustedTypes,L=P?P.emptyScript:"",I=M.reactiveElementPolyfillSupport,O=(e,t)=>e,N={toAttribute(e,t){switch(t){case Boolean:e=e?L:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},H=(e,t)=>!S(e,t),z={attribute:!0,type:String,converter:N,reflect:!1,useDefault:!1,hasChanged:H};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */Symbol.metadata??=Symbol("metadata"),M.litPropertyMetadata??=new WeakMap;let B=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=z){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(e,i,t);void 0!==s&&E(this.prototype,e,s)}}static getPropertyDescriptor(e,t,i){const{get:s,set:a}=T(this.prototype,e)??{get(){return this[t]},set(e){this[t]=e}};return{get:s,set(t){const o=s?.call(this);a?.call(this,t),this.requestUpdate(e,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??z}static _$Ei(){if(this.hasOwnProperty(O("elementProperties")))return;const e=C(this);e.finalize(),void 0!==e.l&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(O("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(O("properties"))){const e=this.properties,t=[...A(e),...D(e)];for(const i of t)this.createProperty(i,e[i])}const e=this[Symbol.metadata];if(null!==e){const t=litPropertyMetadata.get(e);if(void 0!==t)for(const[e,i]of t)this.elementProperties.set(e,i)}this._$Eh=new Map;for(const[e,t]of this.elementProperties){const i=this._$Eu(e,t);void 0!==i&&this._$Eh.set(i,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(k(e))}else void 0!==e&&t.push(k(e));return t}static _$Eu(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),void 0!==this.renderRoot&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){const e=new Map,t=this.constructor.elementProperties;for(const i of t.keys())this.hasOwnProperty(i)&&(e.set(i,this[i]),delete this[i]);e.size>0&&(this._$Ep=e)}createRenderRoot(){const e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((e,t)=>{if(y)e.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const i of t){const t=document.createElement("style"),s=f.litNonce;void 0!==s&&t.setAttribute("nonce",s),t.textContent=i.cssText,e.appendChild(t)}})(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,i){this._$AK(e,i)}_$ET(e,t){const i=this.constructor.elementProperties.get(e),s=this.constructor._$Eu(e,i);if(void 0!==s&&!0===i.reflect){const a=(void 0!==i.converter?.toAttribute?i.converter:N).toAttribute(t,i.type);this._$Em=e,null==a?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(e,t){const i=this.constructor,s=i._$Eh.get(e);if(void 0!==s&&this._$Em!==s){const e=i.getPropertyOptions(s),a="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==e.converter?.fromAttribute?e.converter:N;this._$Em=s;const o=a.fromAttribute(t,e.type);this[s]=o??this._$Ej?.get(s)??o,this._$Em=null}}requestUpdate(e,t,i,s=!1,a){if(void 0!==e){const o=this.constructor;if(!1===s&&(a=this[e]),i??=o.getPropertyOptions(e),!((i.hasChanged??H)(a,t)||i.useDefault&&i.reflect&&a===this._$Ej?.get(e)&&!this.hasAttribute(o._$Eu(e,i))))return;this.C(e,t,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(e,t,{useDefault:i,reflect:s,wrapped:a},o){i&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,o??t??this[e]),!0!==a||void 0!==o)||(this._$AL.has(e)||(this.hasUpdated||i||(t=void 0),this._$AL.set(e,t)),!0===s&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[e,t]of this._$Ep)this[e]=t;this._$Ep=void 0}const e=this.constructor.elementProperties;if(e.size>0)for(const[t,i]of e){const{wrapped:e}=i,s=this[t];!0!==e||this._$AL.has(t)||void 0===s||this.C(t,void 0,i,s)}}let e=!1;const t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(e=>e.hostUpdate?.()),this.update(t)):this._$EM()}catch(t){throw e=!1,this._$EM(),t}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(e){}firstUpdated(e){}};B.elementStyles=[],B.shadowRootOptions={mode:"open"},B[O("elementProperties")]=new Map,B[O("finalized")]=new Map,I?.({ReactiveElement:B}),(M.reactiveElementVersions??=[]).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const U=globalThis,W=e=>e,R=U.trustedTypes,F=R?R.createPolicy("lit-html",{createHTML:e=>e}):void 0,V="$lit$",j=`lit$${Math.random().toFixed(9).slice(2)}$`,Z="?"+j,Y=`<${Z}>`,q=document,J=()=>q.createComment(""),G=e=>null===e||"object"!=typeof e&&"function"!=typeof e,K=Array.isArray,X="[ \t\n\f\r]",Q=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,ee=/-->/g,te=/>/g,ie=RegExp(`>|${X}(?:([^\\s"'>=/]+)(${X}*=${X}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),se=/'/g,ae=/"/g,oe=/^(?:script|style|textarea|title)$/i,ne=(e,...t)=>({_$litType$:1,strings:e,values:t}),re=Symbol.for("lit-noChange"),le=Symbol.for("lit-nothing"),de=new WeakMap,ce=q.createTreeWalker(q,129);function he(e,t){if(!K(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==F?F.createHTML(t):t}class pe{constructor({strings:e,_$litType$:t},i){let s;this.parts=[];let a=0,o=0;const n=e.length-1,r=this.parts,[l,d]=((e,t)=>{const i=e.length-1,s=[];let a,o=2===t?"<svg>":3===t?"<math>":"",n=Q;for(let t=0;t<i;t++){const i=e[t];let r,l,d=-1,c=0;for(;c<i.length&&(n.lastIndex=c,l=n.exec(i),null!==l);)c=n.lastIndex,n===Q?"!--"===l[1]?n=ee:void 0!==l[1]?n=te:void 0!==l[2]?(oe.test(l[2])&&(a=RegExp("</"+l[2],"g")),n=ie):void 0!==l[3]&&(n=ie):n===ie?">"===l[0]?(n=a??Q,d=-1):void 0===l[1]?d=-2:(d=n.lastIndex-l[2].length,r=l[1],n=void 0===l[3]?ie:'"'===l[3]?ae:se):n===ae||n===se?n=ie:n===ee||n===te?n=Q:(n=ie,a=void 0);const h=n===ie&&e[t+1].startsWith("/>")?" ":"";o+=n===Q?i+Y:d>=0?(s.push(r),i.slice(0,d)+V+i.slice(d)+j+h):i+j+(-2===d?t:h)}return[he(e,o+(e[i]||"<?>")+(2===t?"</svg>":3===t?"</math>":"")),s]})(e,t);if(this.el=pe.createElement(l,i),ce.currentNode=this.el.content,2===t||3===t){const e=this.el.content.firstChild;e.replaceWith(...e.childNodes)}for(;null!==(s=ce.nextNode())&&r.length<n;){if(1===s.nodeType){if(s.hasAttributes())for(const e of s.getAttributeNames())if(e.endsWith(V)){const t=d[o++],i=s.getAttribute(e).split(j),n=/([.?@])?(.*)/.exec(t);r.push({type:1,index:a,name:n[2],strings:i,ctor:"."===n[1]?ve:"?"===n[1]?fe:"@"===n[1]?ye:_e}),s.removeAttribute(e)}else e.startsWith(j)&&(r.push({type:6,index:a}),s.removeAttribute(e));if(oe.test(s.tagName)){const e=s.textContent.split(j),t=e.length-1;if(t>0){s.textContent=R?R.emptyScript:"";for(let i=0;i<t;i++)s.append(e[i],J()),ce.nextNode(),r.push({type:2,index:++a});s.append(e[t],J())}}}else if(8===s.nodeType)if(s.data===Z)r.push({type:2,index:a});else{let e=-1;for(;-1!==(e=s.data.indexOf(j,e+1));)r.push({type:7,index:a}),e+=j.length-1}a++}}static createElement(e,t){const i=q.createElement("template");return i.innerHTML=e,i}}function ue(e,t,i=e,s){if(t===re)return t;let a=void 0!==s?i._$Co?.[s]:i._$Cl;const o=G(t)?void 0:t._$litDirective$;return a?.constructor!==o&&(a?._$AO?.(!1),void 0===o?a=void 0:(a=new o(e),a._$AT(e,i,s)),void 0!==s?(i._$Co??=[])[s]=a:i._$Cl=a),void 0!==a&&(t=ue(e,a._$AS(e,t.values),a,s)),t}class me{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){const{el:{content:t},parts:i}=this._$AD,s=(e?.creationScope??q).importNode(t,!0);ce.currentNode=s;let a=ce.nextNode(),o=0,n=0,r=i[0];for(;void 0!==r;){if(o===r.index){let t;2===r.type?t=new ge(a,a.nextSibling,this,e):1===r.type?t=new r.ctor(a,r.name,r.strings,this,e):6===r.type&&(t=new be(a,this,e)),this._$AV.push(t),r=i[++n]}o!==r?.index&&(a=ce.nextNode(),o++)}return ce.currentNode=q,s}p(e){let t=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(e,i,t),t+=i.strings.length-2):i._$AI(e[t])),t++}}class ge{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,i,s){this.type=2,this._$AH=le,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e?.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=ue(this,e,t),G(e)?e===le||null==e||""===e?(this._$AH!==le&&this._$AR(),this._$AH=le):e!==this._$AH&&e!==re&&this._(e):void 0!==e._$litType$?this.$(e):void 0!==e.nodeType?this.T(e):(e=>K(e)||"function"==typeof e?.[Symbol.iterator])(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==le&&G(this._$AH)?this._$AA.nextSibling.data=e:this.T(q.createTextNode(e)),this._$AH=e}$(e){const{values:t,_$litType$:i}=e,s="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=pe.createElement(he(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(t);else{const e=new me(s,this),i=e.u(this.options);e.p(t),this.T(i),this._$AH=e}}_$AC(e){let t=de.get(e.strings);return void 0===t&&de.set(e.strings,t=new pe(e)),t}k(e){K(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let i,s=0;for(const a of e)s===t.length?t.push(i=new ge(this.O(J()),this.O(J()),this,this.options)):i=t[s],i._$AI(a),s++;s<t.length&&(this._$AR(i&&i._$AB.nextSibling,s),t.length=s)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){const t=W(e).nextSibling;W(e).remove(),e=t}}setConnected(e){void 0===this._$AM&&(this._$Cv=e,this._$AP?.(e))}}class _e{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,i,s,a){this.type=1,this._$AH=le,this._$AN=void 0,this.element=e,this.name=t,this._$AM=s,this.options=a,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=le}_$AI(e,t=this,i,s){const a=this.strings;let o=!1;if(void 0===a)e=ue(this,e,t,0),o=!G(e)||e!==this._$AH&&e!==re,o&&(this._$AH=e);else{const s=e;let n,r;for(e=a[0],n=0;n<a.length-1;n++)r=ue(this,s[i+n],t,n),r===re&&(r=this._$AH[n]),o||=!G(r)||r!==this._$AH[n],r===le?e=le:e!==le&&(e+=(r??"")+a[n+1]),this._$AH[n]=r}o&&!s&&this.j(e)}j(e){e===le?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}}class ve extends _e{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===le?void 0:e}}class fe extends _e{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==le)}}class ye extends _e{constructor(e,t,i,s,a){super(e,t,i,s,a),this.type=5}_$AI(e,t=this){if((e=ue(this,e,t,0)??le)===re)return;const i=this._$AH,s=e===le&&i!==le||e.capture!==i.capture||e.once!==i.once||e.passive!==i.passive,a=e!==le&&(i===le||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}}class be{constructor(e,t,i){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(e){ue(this,e)}}const xe={I:ge},we=U.litHtmlPolyfillSupport;we?.(pe,ge),(U.litHtmlVersions??=[]).push("3.3.2");const $e=globalThis;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */let ke=class extends B{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,i)=>{const s=i?.renderBefore??t;let a=s._$litPart$;if(void 0===a){const e=i?.renderBefore??null;s._$litPart$=a=new ge(t.insertBefore(J(),e),e,void 0,i??{})}return a._$AI(e),a})(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return re}};ke._$litElement$=!0,ke.finalized=!0,$e.litElementHydrateSupport?.({LitElement:ke});const Se=$e.litElementPolyfillSupport;Se?.({LitElement:ke}),($e.litElementVersions??=[]).push("4.2.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Ee={attribute:!0,type:String,converter:N,reflect:!1,hasChanged:H},Te=(e=Ee,t,i)=>{const{kind:s,metadata:a}=i;let o=globalThis.litPropertyMetadata.get(a);if(void 0===o&&globalThis.litPropertyMetadata.set(a,o=new Map),"setter"===s&&((e=Object.create(e)).wrapped=!0),o.set(i.name,e),"accessor"===s){const{name:s}=i;return{set(i){const a=t.get.call(this);t.set.call(this,i),this.requestUpdate(s,a,e,!0,i)},init(t){return void 0!==t&&this.C(s,void 0,e,t),t}}}if("setter"===s){const{name:s}=i;return function(i){const a=this[s];t.call(this,i),this.requestUpdate(s,a,e,!0,i)}}throw Error("Unsupported decorator location: "+s)};function Ae(e){return(t,i)=>"object"==typeof i?Te(e,t,i):((e,t,i)=>{const s=t.hasOwnProperty(i);return t.constructor.createProperty(i,e),s?Object.getOwnPropertyDescriptor(t,i):void 0})(e,t,i)}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function De(e){return Ae({...e,state:!0,attribute:!1})}const Ce=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"],Me=["fixed_time","astro","fixed_if_before_astro","astro_if_before_fixed","fixed_if_after_astro","astro_if_after_fixed","earliest","latest"],Pe={switch:{levelType:"binary",hasLevel2:!1,hasDuration:!0,hasRampTime:!1},light:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!0},cover:{levelType:"percentage",hasLevel2:!0,hasDuration:!1,hasRampTime:!1},valve:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!1}},Le=["ms","s","min","h"];function Ie(e){const[t,i]=e.split(":").map(Number);return 60*t+i}function Oe(e){const t=e%60;return`${Math.floor(e/60).toString().padStart(2,"0")}:${t.toString().padStart(2,"0")}`}function Ne(e,t="24"){if("24"===t)return e;const[i,s]=e.split(":");let a=parseInt(i,10);if(24===a)return"12:00 AM";const o=a>=12?"PM":"AM";return 0===a?a=12:a>12&&(a-=12),`${a}:${s||"00"} ${o}`}function He(e){return e<10?"#2b9af9":e<14?"#40c4ff":e<17?"#26c6da":e<19?"#66bb6a":e<21?"#9ccc65":e<23?"#ffb74d":e<25?"#ff8100":"#f4511e"}function ze(e){if(!e)return;const t=e.split(":");return 2===t.length?t[0]:void 0}function Be(e){const{base_temperature:t,periods:i}=e,s=[],a=[...i].sort((e,t)=>Ie(e.starttime)-Ie(t.starttime));for(let e=0;e<a.length;e++){const t=a[e];s.push({startTime:t.starttime,startMinutes:Ie(t.starttime),endTime:t.endtime,endMinutes:Ie(t.endtime),temperature:t.temperature,slot:e+1})}return{blocks:s,baseTemperature:t}}function Ue(e,t){const i=[],s=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of s)i.push({starttime:e.startTime,endtime:e.endTime,temperature:e.temperature});return{base_temperature:t,periods:i}}function We(e){if(0===e.length)return 20;const t=new Map;for(const i of e){const e=i.endMinutes-i.startMinutes,s=t.get(i.temperature)||0;t.set(i.temperature,s+e)}let i=0,s=20;for(const[e,a]of t.entries())a>i&&(i=a,s=e);return s}function Re(e){if(0===e.length)return[];const t=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),i=[];let s={...t[0]};for(let e=1;e<t.length;e++){const a=t[e];s.endMinutes===a.startMinutes&&s.temperature===a.temperature?s={...s,endTime:a.endTime,endMinutes:a.endMinutes}:(i.push(s),s={...a})}return i.push(s),i.map((e,t)=>({...e,slot:t+1}))}function Fe(e,t){if(0===e.length)return[{startTime:"00:00",startMinutes:0,endTime:"24:00",endMinutes:1440,temperature:t,slot:1}];const i=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),s=[];let a=0;for(const e of i)e.startMinutes>a&&s.push({startTime:Oe(a),startMinutes:a,endTime:e.startTime,endMinutes:e.startMinutes,temperature:t,slot:s.length+1}),s.push({...e,slot:s.length+1}),a=e.endMinutes;return a<1440&&s.push({startTime:Oe(a),startMinutes:a,endTime:"24:00",endMinutes:1440,temperature:t,slot:s.length+1}),Re(s)}function Ve(e){return[...e].sort((e,t)=>e.startMinutes-t.startMinutes).map((e,t)=>({...e,slot:t+1}))}function je(e){return Boolean(Array.isArray(e.weekdays)&&e.weekdays.length>0&&Array.isArray(e.target_channels)&&e.target_channels.length>0)}function Ze(e){return"fixed_time"!==e}const Ye=/^(\d+(?:\.\d+)?)\s*(ms|s|min|h)$/;function qe(e){const t=e.trim().match(Ye);return t?{value:parseFloat(t[1]),unit:t[2]}:null}function Je(e,t){return`${e}${t}`}function Ge(e){return Ye.test(e.trim())}function Ke(e){const t={weekdays:e.weekdays,time:e.time,target_channels:e.target_channels,level:e.level};return"fixed_time"!==e.condition&&(t.condition=e.condition),null!==e.astro_type&&(t.astro_type=e.astro_type),0!==e.astro_offset_minutes&&(t.astro_offset_minutes=e.astro_offset_minutes),null!==e.level_2&&(t.level_2=e.level_2),null!==e.duration&&(t.duration=e.duration),null!==e.ramp_time&&(t.ramp_time=e.ramp_time),t}function Xe(e){const t={};for(const[i,s]of Object.entries(e))t[i]=Ke(s);return t}function Qe(e){return"default"===e.schedule_type}function et(e,t=5,i=30.5){const{base_temperature:s,periods:a}=e;if(s<t||s>i)return{key:"temperatureOutOfRange",params:{block:"base",min:`${t}`,max:`${i}`}};let o=0;for(let e=0;e<a.length;e++){const s=a[e];if(!s.starttime||!s.endtime||void 0===s.temperature)return{key:"slotMissingValues",params:{slot:`${e+1}`}};const n=Ie(s.starttime),r=Ie(s.endtime);if(r<=n)return{key:"blockEndBeforeStart",params:{block:`${e+1}`}};if(n<o)return{key:"slotTimeBackwards",params:{slot:`${e+1}`,time:s.starttime}};if(s.temperature<t||s.temperature>i)return{key:"temperatureOutOfRange",params:{block:`${e+1}`,min:`${t}`,max:`${i}`}};o=r}return null}const tt=(e,t,i)=>{const s=new CustomEvent(t,{bubbles:!0,composed:!0,detail:i});e.dispatchEvent(s)};let it=class e extends ke{constructor(){super(...arguments),this._computeLabel=e=>({entities:"Entities",name:"Card Name (optional)",editable:"Allow editing",show_import_export:"Show import/export buttons",schedule_domain:"Schedule Domain",hour_format:"Time format"}[e.name]||e.name)}_getScheduleEntityIds(){return this.hass?.states?Object.keys(this.hass.states).filter(e=>{if(!e.startsWith("sensor."))return!1;const t=this.hass?.states?.[e];return!!t&&Qe(t.attributes)}):[]}_buildEntitySchema(){return[{name:"entities",required:!0,selector:{entity:{multiple:!0,include_entities:this._getScheduleEntityIds()}}}]}static{this.OPTIONS_SCHEMA=[{name:"name",selector:{text:{}}},{name:"editable",selector:{boolean:{}},default:!0},{name:"show_import_export",selector:{boolean:{}},default:!1},{name:"schedule_domain",selector:{select:{options:[{value:"",label:"Auto (from entity)"},{value:"switch",label:"Switch"},{value:"light",label:"Light"},{value:"cover",label:"Cover"},{value:"valve",label:"Valve"}],mode:"dropdown"}},default:""},{name:"hour_format",selector:{select:{options:[{value:"24",label:"24h"},{value:"12",label:"12h (AM/PM)"}]}},default:"24"}]}setConfig(e){this._config=e}_getEntityIds(){return this._config?this._config.entities?this._config.entities:this._config.entity?[this._config.entity]:[]:[]}render(){if(!this.hass||!this._config)return le;const t={entities:this._getEntityIds()};return ne`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${this._buildEntitySchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._entitiesChanged}
      ></ha-form>

      <ha-form
        .hass=${this.hass}
        .data=${{...this._config,schedule_domain:this._config.schedule_domain||""}}
        .schema=${e.OPTIONS_SCHEMA}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._optionsChanged}
      ></ha-form>
    `}_entitiesChanged(e){e.stopPropagation();const t=e.detail.value?.entities||[],i={...this._config,entities:t};delete i.entity,tt(this,"config-changed",{config:i})}_optionsChanged(e){e.stopPropagation();const t=e.detail.value,i=t.schedule_domain,s={...this._config,...t,entities:this._config.entities};i||delete s.schedule_domain,tt(this,"config-changed",{config:s})}static{this.styles=$`
    ha-form {
      display: block;
    }
  `}};function st(e){return t=>(customElements.get(e)||customElements.define(e,t),t)}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */v([Ae({attribute:!1})],it.prototype,"hass",void 0),v([De()],it.prototype,"_config",void 0),customElements.get("homematicip-local-schedule-card-editor")||customElements.define("homematicip-local-schedule-card-editor",it);let at=class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,i){this._$Ct=e,this._$AM=t,this._$Ci=i}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}};
/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const{I:ot}=xe,nt=e=>e,rt=()=>document.createComment(""),lt=(e,t,i)=>{const s=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=s.insertBefore(rt(),a),o=s.insertBefore(rt(),a);i=new ot(t,o,e,e.options)}else{const t=i._$AB.nextSibling,o=i._$AM,n=o!==e;if(n){let t;i._$AQ?.(e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==o._$AU&&i._$AP(t)}if(t!==a||n){let e=i._$AA;for(;e!==t;){const t=nt(e).nextSibling;nt(s).insertBefore(e,a),e=t}}}return i},dt=(e,t,i=e)=>(e._$AI(t,i),e),ct={},ht=(e,t=ct)=>e._$AH=t,pt=e=>{e._$AR(),e._$AA.remove()},ut=(e,t,i)=>{const s=new Map;for(let a=t;a<=i;a++)s.set(e[a],a);return s},mt=(e=>(...t)=>({_$litDirective$:e,values:t}))(class extends at{constructor(e){if(super(e),2!==e.type)throw Error("repeat() can only be used in text expressions")}dt(e,t,i){let s;void 0===i?i=t:void 0!==t&&(s=t);const a=[],o=[];let n=0;for(const t of e)a[n]=s?s(t,n):n,o[n]=i(t,n),n++;return{values:o,keys:a}}render(e,t,i){return this.dt(e,t,i).values}update(e,[t,i,s]){const a=(e=>e._$AH)(e),{values:o,keys:n}=this.dt(t,i,s);if(!Array.isArray(a))return this.ut=n,o;const r=this.ut??=[],l=[];let d,c,h=0,p=a.length-1,u=0,m=o.length-1;for(;h<=p&&u<=m;)if(null===a[h])h++;else if(null===a[p])p--;else if(r[h]===n[u])l[u]=dt(a[h],o[u]),h++,u++;else if(r[p]===n[m])l[m]=dt(a[p],o[m]),p--,m--;else if(r[h]===n[m])l[m]=dt(a[h],o[m]),lt(e,l[m+1],a[h]),h++,m--;else if(r[p]===n[u])l[u]=dt(a[p],o[u]),lt(e,a[h],a[p]),p--,u++;else if(void 0===d&&(d=ut(n,u,m),c=ut(r,h,p)),d.has(r[h]))if(d.has(r[p])){const t=c.get(n[u]),i=void 0!==t?a[t]:null;if(null===i){const t=lt(e,a[h]);dt(t,o[u]),l[u]=t}else l[u]=dt(i,o[u]),lt(e,a[h],i),a[t]=null;u++}else pt(a[p]),p--;else pt(a[h]),h++;for(;u<=m;){const t=lt(e,l[m+1]);dt(t,o[u]),l[u++]=t}for(;h<=p;){const e=a[h++];null!==e&&pt(e)}return this.ut=n,ht(e,l),re}}),gt=$`
  :host {
    display: block;
  }

  .schedule-container {
    display: grid;
    grid-template-columns: auto repeat(7, minmax(0, 1fr));
    grid-template-rows: auto 1fr;
    gap: 8px;
    min-height: 400px;
    overflow: hidden;
    width: 100%;
    box-sizing: border-box;
  }

  .time-axis-header {
    /* Empty cell in row 1, col 1 - height matches weekday headers */
  }

  .time-axis-labels {
    position: relative;
    border-right: 2px solid var(--divider-color);
    min-width: 50px;
  }

  .time-label {
    position: absolute;
    right: 8px;
    transform: translateY(-50%);
    font-size: 11px;
    color: var(--secondary-text-color);
    white-space: nowrap;
  }

  .schedule-content {
    grid-column: 2 / -1;
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 8px;
    position: relative;
    min-height: 300px;
  }

  .current-time-indicator {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background-color: var(--error-color, #ff0000);
    border-top: 2px dashed var(--error-color, #ff0000);
    pointer-events: none;
    z-index: 10;
    transform: translateY(-50%);
    box-shadow: 0 0 4px rgba(255, 0, 0, 0.5);
    will-change: top;
  }

  .current-time-indicator::before {
    content: "";
    position: absolute;
    left: -6px;
    top: 50%;
    transform: translateY(-50%);
    width: 8px;
    height: 8px;
    background-color: var(--error-color, #ff0000);
    border-radius: 50%;
    box-shadow: 0 0 4px rgba(255, 0, 0, 0.7);
  }

  .weekday-header {
    padding: 4px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    background-color: var(--primary-color);
    color: var(--text-primary-color);
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    overflow: hidden;
    min-width: 0;
  }

  .weekday-label {
    font-weight: 500;
    font-size: 14px;
  }

  .weekday-actions {
    display: flex;
    gap: 2px;
    flex-shrink: 1;
    min-width: 0;
  }

  .weekday-actions ha-icon-button {
    --ha-icon-button-size: 28px;
    --ha-icon-button-icon-size: 16px;
    color: var(--text-primary-color, #fff);
    opacity: 0.7;
    flex-shrink: 0;
  }

  .weekday-actions ha-icon-button:hover {
    opacity: 1;
  }

  .copy-btn.active {
    opacity: 1;
    animation: pulse 1s ease-in-out;
    will-change: transform;
  }

  @keyframes pulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.1);
    }
  }

  ha-icon-button[disabled] {
    opacity: 0.5;
  }

  .time-blocks {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: visible;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
  }

  .time-blocks.editable {
    cursor: pointer;
    will-change: transform, box-shadow;
  }

  .time-blocks.editable:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .time-blocks.editable:focus-visible {
    outline: 2px solid var(--primary-color, #03a9f4);
    outline-offset: 2px;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .time-block {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 12px;
    font-weight: 500;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    transition: opacity 0.2s;
    cursor: pointer;
  }

  .time-block.base-temp-block {
    color: var(--secondary-text-color, #666);
    text-shadow: none;
    border-top: 1px dashed var(--divider-color, #ccc);
  }

  .time-block.base-temp-block:first-child {
    border-top: none;
  }

  .time-block:hover {
    opacity: 0.9;
  }

  .time-block:hover .time-block-tooltip {
    opacity: 1;
    visibility: visible;
  }

  .temperature {
    user-select: none;
    position: relative;
    z-index: 1;
  }

  /* Active block highlighting */
  .time-block.active {
    box-shadow:
      inset 0 0 0 3px rgba(255, 255, 255, 0.9),
      0 0 20px rgba(255, 255, 255, 0.6),
      0 0 30px rgba(255, 255, 255, 0.4);
    animation: pulse-glow 2s ease-in-out infinite;
    z-index: 10;
    will-change: box-shadow;
  }

  @keyframes pulse-glow {
    0%,
    100% {
      box-shadow:
        inset 0 0 0 3px rgba(255, 255, 255, 0.9),
        0 0 15px rgba(255, 255, 255, 0.5),
        0 0 25px rgba(255, 255, 255, 0.3);
    }
    50% {
      box-shadow:
        inset 0 0 0 3px rgba(255, 255, 255, 1),
        0 0 25px rgba(255, 255, 255, 0.8),
        0 0 40px rgba(255, 255, 255, 0.6);
    }
  }

  /* Tooltip styling */
  .time-block-tooltip {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0, 0, 0, 0.95);
    color: white;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 10px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition:
      opacity 0.2s,
      visibility 0.2s;
    z-index: 1000;
    pointer-events: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    min-width: 80px;
  }

  .tooltip-time {
    font-weight: 500;
    margin-bottom: 2px;
    text-align: center;
    font-size: 10px;
    line-height: 1.2;
  }

  .tooltip-temp {
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    line-height: 1.2;
  }

  .hint {
    margin-top: 12px;
    text-align: center;
    font-size: 12px;
    color: var(--secondary-text-color);
  }

  /* Mobile single-day view */
  .mobile-day-nav {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 4px 0;
    margin-bottom: 8px;
    background-color: var(--primary-color);
    color: var(--text-primary-color);
    border-radius: 4px;
  }

  .mobile-day-nav ha-icon-button {
    color: var(--text-primary-color, #fff);
    --ha-icon-button-size: 40px;
    --ha-icon-button-icon-size: 24px;
  }

  .mobile-day-name {
    font-size: 18px;
    font-weight: 500;
    min-width: 120px;
    text-align: center;
    user-select: none;
  }

  .mobile-schedule-container {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 8px;
    min-height: 400px;
    touch-action: pan-y;
  }

  .mobile-day-content {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 400px;
  }

  .mobile-day-content .time-blocks {
    flex: 1;
  }

  .mobile-day-content .time-block {
    font-size: 14px;
    min-height: 24px;
  }

  .mobile-day-content .temperature {
    font-size: 14px;
  }

  .mobile-day-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 8px;
    padding: 4px 0;
  }

  .mobile-day-actions ha-icon-button {
    --ha-icon-button-size: 44px;
    --ha-icon-button-icon-size: 22px;
    color: var(--primary-color);
  }

  .mobile-day-actions .copy-btn.active {
    color: var(--accent-color, var(--primary-color));
    opacity: 1;
    animation: pulse 1s ease-in-out;
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    .schedule-container {
      gap: 4px;
      min-height: 350px;
    }

    .time-axis-labels {
      min-width: 40px;
    }

    .time-label {
      font-size: 10px;
      right: 4px;
    }

    .schedule-content {
      gap: 4px;
    }

    .weekday-header {
      padding: 6px 4px;
    }

    .weekday-label {
      font-size: 12px;
    }

    .weekday-actions {
      gap: 0px;
    }

    .weekday-actions ha-icon-button {
      --ha-icon-button-size: 36px;
      --ha-icon-button-icon-size: 18px;
      min-width: 44px;
      min-height: 44px;
    }

    .temperature {
      font-size: 11px;
    }

    .time-block-tooltip {
      font-size: 11px;
      padding: 8px 12px;
    }

    .hint {
      font-size: 14px;
    }
  }

  /* Small mobile devices (portrait phones) */
  @media (max-width: 480px) {
    .schedule-container {
      gap: 2px;
      min-height: 300px;
    }

    .time-axis-labels {
      min-width: 35px;
    }

    .time-label {
      font-size: 9px;
      right: 2px;
    }

    .schedule-content {
      gap: 2px;
    }

    .weekday-header {
      padding: 4px 2px;
    }

    .weekday-label {
      font-size: 11px;
    }

    .weekday-actions ha-icon-button {
      --ha-icon-button-size: 32px;
      --ha-icon-button-icon-size: 16px;
      min-width: 44px;
      min-height: 44px;
    }

    .temperature {
      font-size: 10px;
    }
  }

  /* Touch-specific optimizations */
  @media (hover: none) and (pointer: coarse) {
    .time-blocks.editable:hover {
      transform: none;
      box-shadow: none;
    }

    .time-blocks.editable:active {
      transform: scale(0.98);
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .time-block:hover {
      opacity: 1;
    }

    .time-block:active {
      opacity: 0.85;
    }

    /* Show tooltip on tap instead of hover */
    .time-block:active .time-block-tooltip {
      opacity: 1;
      visibility: visible;
    }
  }
`;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var _t=function(e,t,i,s){var a,o=arguments.length,n=o<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var r=e.length-1;r>=0;r--)(a=e[r])&&(n=(o<3?a(n):o>3?a(t,i,n):a(t,i))||n);return o>3&&n&&Object.defineProperty(t,i,n),n};let vt=class extends ke{constructor(){super(...arguments),this.editable=!1,this.showTemperature=!0,this.showGradient=!1,this.temperatureUnit="°C",this.hourFormat="24",this.editorOpen=!1,this._currentTimePercent=0,this._currentTimeMinutes=0,this._isMobile=!1,this._mobileSelectedDayIndex=0,this._mediaHandler=e=>{this._isMobile=e.matches},this._touchStartX=0,this._touchStartY=0}connectedCallback(){super.connectedCallback(),this._updateCurrentTime(),this._timeUpdateInterval=window.setInterval(()=>{this._updateCurrentTime()},6e4),this._mediaQuery=window.matchMedia("(max-width: 600px)"),this._isMobile=this._mediaQuery.matches,this._mediaQuery.addEventListener("change",this._mediaHandler),this._initMobileSelectedDay()}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._timeUpdateInterval&&(clearInterval(this._timeUpdateInterval),this._timeUpdateInterval=void 0),this._mediaQuery&&(this._mediaQuery.removeEventListener("change",this._mediaHandler),this._mediaQuery=void 0)}willUpdate(e){super.willUpdate(e)}_updateCurrentTime(){const e=new Date,t=60*e.getHours()+e.getMinutes();this._currentTimePercent=t/1440*100,this._currentTimeMinutes=t;const i=e.getDay();this._currentWeekday=["SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY"][i]}_isBlockActive(e,t){return!(!this._currentWeekday||this._currentWeekday!==e)&&this._currentTimeMinutes>=t.startMinutes&&this._currentTimeMinutes<t.endMinutes}_getTimeLabels(){const e=[];for(let t=0;t<=24;t+=3){const i=`${t.toString().padStart(2,"0")}:00`;e.push({hour:t,label:Ne(i,this.hourFormat),position:t/24*100})}return e}_formatTimeDisplay(e){return Ne(e,this.hourFormat)}_getBaseTemperature(e){if(this.scheduleData){const t=this.scheduleData[e];if(t){const{baseTemperature:e}=Be(t);return e}}return 20}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=Be(t);return i}return[]}_getWeekdayLabel(e){return this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_handleWeekdayClick(e){this.editable&&this.dispatchEvent(new CustomEvent("weekday-click",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handleCopy(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("copy-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handlePaste(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("paste-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}_initMobileSelectedDay(){const e=(new Date).getDay();this._mobileSelectedDayIndex=0===e?6:e-1}_mobilePrevDay(){this._mobileSelectedDayIndex=(this._mobileSelectedDayIndex-1+Ce.length)%Ce.length}_mobileNextDay(){this._mobileSelectedDayIndex=(this._mobileSelectedDayIndex+1)%Ce.length}_getWeekdayLongLabel(e){return this.translations?.weekdayLongLabels?.[e]??e.charAt(0)+e.slice(1).toLowerCase()}_handleTouchStart(e){this._touchStartX=e.touches[0].clientX,this._touchStartY=e.touches[0].clientY}_handleTouchEnd(e){const t=e.changedTouches[0].clientX-this._touchStartX,i=e.changedTouches[0].clientY-this._touchStartY;Math.abs(t)>50&&Math.abs(t)>1.5*Math.abs(i)&&(t<0?this._mobileNextDay():this._mobilePrevDay())}_renderTimeBlocks(e){const t=this._getParsedBlocks(e),i=this._getBaseTemperature(e),s=Fe(t,i);return ne`
      <div
        class="time-blocks ${this.editable?"editable":""}"
        tabindex=${this.editable?"0":"-1"}
        role=${this.editable?"button":"presentation"}
        aria-label=${this._getWeekdayLabel(e)}
        @click=${()=>this._handleWeekdayClick(e)}
        @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._handleWeekdayClick(e))}}
      >
        ${mt(s,e=>`${e.slot}-${e.startMinutes}-${this.currentProfile}`,(a,o)=>{const n=this._isBlockActive(e,a),r=a.temperature===i&&!t.some(e=>e.startMinutes===a.startMinutes&&e.endMinutes===a.endMinutes);let l;if(r)l="background-color: var(--secondary-background-color, #e0e0e0);";else if(this.showGradient){const e=o>0?s[o-1].temperature:null,t=o<s.length-1?s[o+1].temperature:null,i=function(e,t,i){const s=He(e);return null===t&&null===i?s:null!==t&&null===i?`linear-gradient(to bottom, ${He(t)}, ${s})`:null===t&&null!==i?`linear-gradient(to bottom, ${s}, ${He(i)})`:`linear-gradient(to bottom, ${He(t)}, ${s} 50%, ${He(i)})`}(a.temperature,e,t);l=`background: ${i};`}else l=`background-color: ${He(a.temperature)};`;return ne`
              <div
                class="time-block ${n?"active":""} ${r?"base-temp-block":""}"
                style="
                    height: ${(a.endMinutes-a.startMinutes)/1440*100}%;
                    ${l}
                  "
              >
                ${this.showTemperature?ne`<span class="temperature">${a.temperature.toFixed(1)}°</span>`:""}
                <div class="time-block-tooltip">
                  <div class="tooltip-time">
                    ${this._formatTimeDisplay(a.startTime)} -
                    ${this._formatTimeDisplay(a.endTime)}
                  </div>
                  <div class="tooltip-temp">
                    ${function(e,t="°C"){return`${e.toFixed(1)}${t}`}(a.temperature,this.temperatureUnit)}
                  </div>
                </div>
              </div>
            `})}
      </div>
    `}_renderMobile(){const e=Ce[this._mobileSelectedDayIndex],t=this.copiedWeekday===e;return ne`
      <div class="mobile-day-nav">
        <ha-icon-button
          .path=${"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z"}
          @click=${()=>this._mobilePrevDay()}
          .label=${this.translations?.previousDay??"Previous day"}
        ></ha-icon-button>
        <span class="mobile-day-name">${this._getWeekdayLongLabel(e)}</span>
        <ha-icon-button
          .path=${"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}
          @click=${()=>this._mobileNextDay()}
          .label=${this.translations?.nextDay??"Next day"}
        ></ha-icon-button>
      </div>

      <div
        class="mobile-schedule-container"
        @touchstart=${e=>this._handleTouchStart(e)}
        @touchend=${e=>this._handleTouchEnd(e)}
      >
        <div class="time-axis-labels">
          ${mt(this._getTimeLabels(),e=>e.hour,e=>ne`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `)}
        </div>

        <div class="mobile-day-content">
          ${this._renderTimeBlocks(e)}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen||this._currentWeekday!==e?"":ne`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?ne`
            <div class="mobile-day-actions">
              <ha-icon-button
                class="copy-btn ${t?"active":""}"
                .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
                @click=${t=>this._handleCopy(e,t)}
                .label=${this.translations?.copySchedule??""}
              ></ha-icon-button>
              <ha-icon-button
                class="paste-btn"
                .path=${"M19,20H5V4H7V7H17V4H19M12,2A1,1 0 0,1 13,3A1,1 0 0,1 12,4A1,1 0 0,1 11,3A1,1 0 0,1 12,2M19,2H14.82C14.4,0.84 13.3,0 12,0C10.7,0 9.6,0.84 9.18,2H5A2,2 0 0,0 3,4V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V4A2,2 0 0,0 19,2Z"}
                @click=${t=>this._handlePaste(e,t)}
                .label=${this.translations?.pasteSchedule??""}
                .disabled=${!this.copiedWeekday}
              ></ha-icon-button>
            </div>
          `:""}
      ${this.editable?ne`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `}_renderDesktop(){return ne`
      <div class="schedule-container">
        <!-- Empty cell for time-axis header alignment -->
        <div class="time-axis-header"></div>

        <!-- Weekday headers -->
        ${mt(Ce,e=>`header-${e}`,e=>{const t=this.copiedWeekday===e;return ne`
              <div class="weekday-header">
                <div class="weekday-label">${this._getWeekdayLabel(e)}</div>
                ${this.editable?ne`
                      <div class="weekday-actions">
                        <ha-icon-button
                          class="copy-btn ${t?"active":""}"
                          .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
                          @click=${t=>this._handleCopy(e,t)}
                          .label=${this.translations?.copySchedule??""}
                        ></ha-icon-button>
                        <ha-icon-button
                          class="paste-btn"
                          .path=${"M19,20H5V4H7V7H17V4H19M12,2A1,1 0 0,1 13,3A1,1 0 0,1 12,4A1,1 0 0,1 11,3A1,1 0 0,1 12,2M19,2H14.82C14.4,0.84 13.3,0 12,0C10.7,0 9.6,0.84 9.18,2H5A2,2 0 0,0 3,4V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V4A2,2 0 0,0 19,2Z"}
                          @click=${t=>this._handlePaste(e,t)}
                          .label=${this.translations?.pasteSchedule??""}
                          .disabled=${!this.copiedWeekday}
                        ></ha-icon-button>
                      </div>
                    `:""}
              </div>
            `})}

        <!-- Time axis labels -->
        <div class="time-axis-labels">
          ${mt(this._getTimeLabels(),e=>e.hour,e=>ne`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `)}
        </div>

        <!-- Time blocks content wrapper (for correct indicator positioning) -->
        <div class="schedule-content">
          ${mt(Ce,e=>`${e}-${this.currentProfile}-${this.scheduleDataHash}`,e=>this._renderTimeBlocks(e))}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen?"":ne`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?ne`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `}render(){return this.scheduleData?this._isMobile?this._renderMobile():this._renderDesktop():ne``}static{this.styles=gt}};_t([Ae({attribute:!1})],vt.prototype,"scheduleData",void 0),_t([Ae({type:Boolean})],vt.prototype,"editable",void 0),_t([Ae({type:Boolean})],vt.prototype,"showTemperature",void 0),_t([Ae({type:Boolean})],vt.prototype,"showGradient",void 0),_t([Ae({type:String})],vt.prototype,"temperatureUnit",void 0),_t([Ae({type:String})],vt.prototype,"hourFormat",void 0),_t([Ae({attribute:!1})],vt.prototype,"translations",void 0),_t([Ae({type:String})],vt.prototype,"copiedWeekday",void 0),_t([Ae({type:Boolean})],vt.prototype,"editorOpen",void 0),_t([Ae({type:String})],vt.prototype,"currentProfile",void 0),_t([Ae({type:String})],vt.prototype,"scheduleDataHash",void 0),_t([De()],vt.prototype,"_currentTimePercent",void 0),_t([De()],vt.prototype,"_currentTimeMinutes",void 0),_t([De()],vt.prototype,"_currentWeekday",void 0),_t([De()],vt.prototype,"_isMobile",void 0),_t([De()],vt.prototype,"_mobileSelectedDayIndex",void 0),vt=_t([st("hmip-schedule-grid")],vt);const ft=$`
  :host {
    display: block;
  }

  /* Dialog styles */
  ha-dialog {
    --ha-dialog-max-width: 90vw;
    --ha-dialog-max-height: 90vh;
  }

  .dialog-content {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
    overflow-y: auto;
    max-height: calc(90vh - 200px);
  }

  .weekday-tabs {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .weekday-tab {
    padding: 8px 12px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
    cursor: pointer;
    transition:
      background-color 0.2s,
      border-color 0.2s;
    min-width: 40px;
    text-align: center;
  }

  .weekday-tab:hover {
    background-color: var(--divider-color);
  }

  .weekday-tab.active {
    background-color: var(--primary-color);
    color: var(--text-primary-color, #fff);
    border-color: var(--primary-color);
  }

  .dialog-editor {
    flex: 1;
    min-height: 0;
  }

  .dialog-editor .editor {
    box-shadow: none;
    border: none;
    padding: 0;
  }

  .dialog-editor .editor-header {
    display: none;
  }

  .dialog-editor .editor-footer {
    display: flex;
  }

  /* Editor Styles */
  .editor {
    background-color: var(--card-background-color);
  }

  .editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--divider-color);
  }

  .editor-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 500;
  }

  .editor-actions {
    display: flex;
    gap: 4px;
    align-items: center;
  }

  .editor-actions ha-icon-button {
    --ha-icon-button-size: 36px;
    color: var(--secondary-text-color);
  }

  .editor-actions ha-icon-button[disabled] {
    opacity: 0.5;
  }

  ha-alert {
    margin: 12px 0;
  }

  .warnings-list {
    margin: 0;
    padding-left: 20px;
    list-style-type: disc;
  }

  .warning-item {
    font-size: 13px;
    line-height: 1.6;
    margin: 4px 0;
  }

  /* Base Temperature Section */
  .base-temperature-section {
    background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    padding: 12px;
    margin: 12px 0;
  }

  .base-temperature-header {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 8px;
  }

  .base-temp-label {
    font-weight: 500;
    font-size: 14px;
    color: var(--primary-text-color);
  }

  .base-temp-description {
    font-size: 12px;
    color: var(--secondary-text-color);
  }

  .base-temperature-input {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .base-temp-input {
    width: 80px;
    font-weight: 500;
  }

  .editor-content-label {
    font-weight: 500;
    font-size: 14px;
    color: var(--primary-text-color);
    margin: 16px 0 8px 0;
    padding-left: 8px;
  }

  .editor-content {
    max-height: 500px;
    overflow-y: auto;
  }

  .time-block-header {
    display: grid;
    grid-template-columns: minmax(80px, 100px) minmax(80px, 100px) minmax(70px, 90px) 1fr 24px;
    gap: 8px;
    align-items: center;
    padding: 8px;
    border-bottom: 2px solid var(--divider-color);
    font-weight: 500;
    font-size: 12px;
    color: var(--secondary-text-color);
    text-transform: uppercase;
  }

  .header-cell {
    text-align: left;
  }

  .time-block-editor {
    display: grid;
    grid-template-columns: minmax(80px, 100px) minmax(80px, 100px) minmax(70px, 90px) 1fr 24px;
    gap: 8px;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid var(--divider-color);
  }

  .time-block-editor.editing {
    background-color: var(--primary-color-light, rgba(3, 169, 244, 0.1));
    border: 1px solid var(--primary-color);
    border-radius: 4px;
    margin: 4px 0;
  }

  .time-block-editor.base-temp-slot {
    opacity: 0.6;
    background-color: var(--divider-color);
  }

  .time-display {
    font-size: 14px;
    color: var(--primary-text-color);
    font-family: monospace;
  }

  .temp-display-group,
  .temp-input-group {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .temp-display {
    font-size: 14px;
    color: var(--primary-text-color);
    font-weight: 500;
  }

  .slot-actions {
    display: flex;
    gap: 4px;
    justify-content: flex-end;
  }

  .slot-actions ha-button {
    font-size: 12px;
  }

  ha-button[disabled] {
    opacity: 0.5;
  }

  .block-number {
    font-weight: 500;
    color: var(--secondary-text-color);
  }

  .time-input,
  .temp-input {
    padding: 6px 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
    width: 100%;
    box-sizing: border-box;
  }

  .time-input {
    min-width: 70px;
    max-width: 120px;
  }

  .temp-input {
    max-width: 60px;
  }

  .temp-unit {
    color: var(--secondary-text-color);
    font-size: 14px;
  }

  .remove-btn {
    --ha-icon-button-size: 32px;
    color: var(--secondary-text-color);
  }

  .remove-btn[disabled] {
    opacity: 0.5;
  }

  .color-indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid var(--divider-color);
    flex-shrink: 0;
  }

  .add-btn {
    margin: 12px 0;
    width: 100%;
    --ha-button-color: var(--primary-color);
  }

  .editor-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--divider-color);
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    ha-dialog {
      --ha-dialog-max-width: 100vw;
      --ha-dialog-max-height: 100vh;
    }

    .dialog-content {
      max-height: calc(100vh - 150px);
    }

    .editor-header h3 {
      font-size: 18px;
    }

    .editor-actions ha-icon-button {
      --ha-icon-button-size: 44px;
    }

    .editor-content {
      max-height: 400px;
    }

    .time-block-editor {
      grid-template-columns: 30px 1fr 70px 40px 44px 20px;
      gap: 6px;
      padding: 10px 6px;
    }

    .block-number {
      font-size: 13px;
    }

    .time-input,
    .temp-input {
      padding: 10px 8px;
      font-size: 16px;
      min-height: 44px;
    }

    .temp-unit {
      font-size: 13px;
    }

    .editor-footer {
      flex-direction: column-reverse;
      gap: 8px;
    }

    .editor-footer ha-button {
      width: 100%;
    }

    .warning-item {
      font-size: 12px;
    }
  }

  /* Small mobile devices (portrait phones) */
  @media (max-width: 480px) {
    .time-block-editor {
      grid-template-columns: 25px 1fr 60px 35px 44px 16px;
      gap: 4px;
      padding: 8px 4px;
    }

    .block-number {
      font-size: 12px;
    }

    .editor-header h3 {
      font-size: 16px;
    }
  }

  /* Landscape mobile optimization */
  @media (max-width: 768px) and (orientation: landscape) {
    .editor-content {
      max-height: calc(100vh - 200px);
    }
  }
`;var yt=function(e,t,i,s){var a,o=arguments.length,n=o<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var r=e.length-1;r>=0;r--)(a=e[r])&&(n=(o<3?a(n):o>3?a(t,i,n):a(t,i))||n);return o>3&&n&&Object.defineProperty(t,i,n),n};let bt=class extends ke{constructor(){super(),this.open=!1,this.minTemp=5,this.maxTemp=30.5,this.tempStep=.5,this.temperatureUnit="°C",this.hourFormat="24",this._validationWarnings=[],this._historyStack=[],this._historyIndex=-1,this._keyDownHandler=this._handleKeyDown.bind(this)}connectedCallback(){super.connectedCallback(),window.addEventListener("keydown",this._keyDownHandler)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("keydown",this._keyDownHandler)}willUpdate(e){if(super.willUpdate(e),(e.has("open")||e.has("weekday"))&&this.open&&this.weekday){const t=e.get("open"),i=e.get("weekday");(!t&&this.open||this.open&&i!==this.weekday)&&this._initializeEditor(this.weekday)}}updated(e){super.updated(e),e.has("open")&&this.open&&!e.get("open")&&this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector(".weekday-tab, .base-temp-input, ha-button");e?.focus()})}_initializeEditor(e){this._editingWeekday=e,this._editingBlocks=this._getParsedBlocks(e),this._editingSlotIndex=void 0,this._editingSlotData=void 0;const t=this.scheduleData?.[e];if(t){const{baseTemperature:e}=Be(t);this._editingBaseTemperature=e}else this._editingBaseTemperature=20;this._historyStack=[JSON.parse(JSON.stringify(this._editingBlocks))],this._historyIndex=0,this._updateValidationWarnings()}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=Be(t);return i}return[]}_getWeekdayLabel(e,t){return"long"===t?this.translations?.weekdayLongLabels[e]??e:this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_formatTimeDisplay(e){return Ne(e,this.hourFormat)}_formatValidationParams(e){if(!e)return{};const t={};for(const[i,s]of Object.entries(e))"weekday"===i&&Ce.includes(s)?t.weekday=this._getWeekdayLabel(s,"long"):t[i]=s;return t}_translateValidationMessage(e){const t=this.translations?.validationMessages[e.key]||e.key,i=this._formatValidationParams(e.params);e.nested&&(i.details=this._translateValidationMessage(e.nested));let s=t;for(const[e,t]of Object.entries(i))s=s.replace(`{${e}}`,t);return s}_saveHistoryState(){if(!this._editingBlocks)return;const e=JSON.parse(JSON.stringify(this._editingBlocks));this._historyStack=this._historyStack.slice(0,this._historyIndex+1),this._historyStack.push(e),this._historyIndex++,this._historyStack.length>50&&(this._historyStack.shift(),this._historyIndex--)}_undo(){this._historyIndex<=0||(this._historyIndex--,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_redo(){this._historyIndex>=this._historyStack.length-1||(this._historyIndex++,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_canUndo(){return this._historyIndex>0}_canRedo(){return this._historyIndex<this._historyStack.length-1}_handleKeyDown(e){if(!this.open||!this._editingWeekday||!this._editingBlocks)return;const t=e.ctrlKey||e.metaKey;t&&"z"===e.key&&!e.shiftKey?(e.preventDefault(),this._undo()):t&&("y"===e.key||"z"===e.key&&e.shiftKey)&&(e.preventDefault(),this._redo())}_updateValidationWarnings(){this._editingBlocks?this._validationWarnings=function(e,t=5,i=30.5){const s=[];if(0===e.length)return s;for(let t=0;t<e.length-1;t++){const i=e[t];i.endMinutes<i.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${t+1}`}}),i.endMinutes===i.startMinutes&&s.push({key:"blockZeroDuration",params:{block:`${t+1}`}})}const a=e[e.length-1];return a.endMinutes<a.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${e.length}`}}),e.forEach((e,a)=>{(e.startMinutes<0||e.startMinutes>1440)&&s.push({key:"invalidStartTime",params:{block:`${a+1}`}}),(e.endMinutes<0||e.endMinutes>1440)&&s.push({key:"invalidEndTime",params:{block:`${a+1}`}}),(e.temperature<t||e.temperature>i)&&s.push({key:"temperatureOutOfRange",params:{block:`${a+1}`,min:`${t}`,max:`${i}`}})}),s}(this._editingBlocks,this.minTemp,this.maxTemp):this._validationWarnings=[]}_startSlotEdit(e){if(!this._editingBlocks||e<0||e>=this._editingBlocks.length)return;const t=this._editingBlocks[e];this._editingSlotIndex=e,this._editingSlotData={startTime:t.startTime,endTime:t.endTime,temperature:t.temperature}}_startSlotEditFromDisplay(e,t){if(!this._editingBlocks)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);-1!==s&&this._startSlotEdit(s)}_cancelSlotEdit(){this._editingSlotIndex=void 0,this._editingSlotData=void 0}_saveSlotEdit(){if(void 0===this._editingSlotIndex||!this._editingSlotData||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=this._editingSlotIndex,{startTime:t,endTime:i,temperature:s}=this._editingSlotData,a={startTime:t,startMinutes:Ie(t),endTime:i,endMinutes:Ie(i),temperature:s,slot:e+1},o=this._editingBlocks.filter((t,i)=>i!==e),n=function(e,t){const i=[],s=t.startMinutes,a=t.endMinutes,o=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of o){const t=e.startMinutes,o=e.endMinutes;o<=s||t>=a?i.push(e):(t<s&&i.push({...e,endTime:Oe(s),endMinutes:s,slot:i.length+1}),o>a&&i.push({...e,startTime:Oe(a),startMinutes:a,slot:i.length+1}))}i.push({...t,slot:i.length+1});const n=i.sort((e,t)=>e.startMinutes-t.startMinutes);return Re(n)}(o,a,this._editingBaseTemperature),r=Re(Ve(n));this._saveHistoryState(),this._editingBlocks=r,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._updateValidationWarnings()}_addNewSlot(){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;if(this._editingBlocks.length>=12)return;let e=0,t=60;if(this._editingBlocks.length>0){const i=Ve(this._editingBlocks),s=i[i.length-1];if(s.endMinutes<1440)e=s.endMinutes,t=Math.min(e+60,1440);else{let s=!1;for(let a=0;a<i.length;a++){const o=0===a?0:i[a-1].endMinutes;if(i[a].startMinutes>o){e=o,t=i[a].startMinutes,s=!0;break}}if(!s)return}}const i=Math.min(this._editingBaseTemperature+2,this.maxTemp),s={startTime:Oe(e),startMinutes:e,endTime:Oe(t),endMinutes:t,temperature:i,slot:this._editingBlocks.length+1};this._saveHistoryState();const a=Ve([...this._editingBlocks,s]);this._editingBlocks=a;const o=a.findIndex(i=>i.startMinutes===e&&i.endMinutes===t);o>=0&&this._startSlotEdit(o),this._updateValidationWarnings()}_removeTimeBlockByIndex(e,t){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);if(-1===s)return;this._saveHistoryState();const a=this._editingBlocks.filter((e,t)=>t!==s);this._editingBlocks=Re(Ve(a)),this._updateValidationWarnings()}_switchToWeekday(e){e!==this._editingWeekday&&this._initializeEditor(e)}_closeEditor(){this._editingWeekday=void 0,this._editingBlocks=void 0,this._editingBaseTemperature=void 0,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._historyStack=[],this._historyIndex=-1,this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_saveSchedule(){if(!this._editingWeekday||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=et(Ue(this._editingBlocks,this._editingBaseTemperature),this.minTemp,this.maxTemp);if(e){const t=this._translateValidationMessage(e);return void this.dispatchEvent(new CustomEvent("validation-failed",{detail:{error:t},bubbles:!0,composed:!0}))}this.dispatchEvent(new CustomEvent("save-schedule",{detail:{weekday:this._editingWeekday,blocks:this._editingBlocks,baseTemperature:this._editingBaseTemperature},bubbles:!0,composed:!0}))}render(){return this.open&&this._editingWeekday?ne`
      <ha-dialog
        open
        @closed=${this._closeEditor}
        .heading=${this._formatEdit(this._editingWeekday)}
      >
        <div class="dialog-content">
          <!-- Weekday selector tabs -->
          <div class="weekday-tabs">
            ${Ce.map(e=>ne`
                <button
                  class="weekday-tab ${e===this._editingWeekday?"active":""}"
                  @click=${()=>this._switchToWeekday(e)}
                >
                  ${this._getWeekdayLabel(e,"short")}
                </button>
              `)}
          </div>

          <!-- Editor content in dialog -->
          <div class="dialog-editor">${this._renderEditor()}</div>
        </div>
      </ha-dialog>
    `:ne``}_formatEdit(e){return(this.translations?.edit??"Edit {weekday}").replace("{weekday}",this._getWeekdayLabel(e,"long"))}_renderEditor(){if(!this._editingWeekday||!this._editingBlocks)return ne``;const e=void 0!==this._editingBaseTemperature?Fe(this._editingBlocks,this._editingBaseTemperature):this._editingBlocks;return ne`
      <div class="editor">
        <div class="editor-header">
          <h3>${this._formatEdit(this._editingWeekday)}</h3>
          <div class="editor-actions">
            <ha-icon-button
              .path=${"M12.5,8C9.85,8 7.45,9 5.6,10.6L2,7V16H11L7.38,12.38C8.77,11.22 10.54,10.5 12.5,10.5C16.04,10.5 19.05,12.81 20.1,16L22.47,15.22C21.08,11.03 17.15,8 12.5,8Z"}
              @click=${this._undo}
              .disabled=${!this._canUndo()}
              .label=${this.translations?.undoShortcut??"Undo"}
            ></ha-icon-button>
            <ha-icon-button
              .path=${"M18.4,10.6C16.55,9 14.15,8 11.5,8C6.85,8 2.92,11.03 1.54,15.22L3.9,16C4.95,12.81 7.95,10.5 11.5,10.5C13.45,10.5 15.23,11.22 16.62,12.38L13,16H22V7L18.4,10.6Z"}
              @click=${this._redo}
              .disabled=${!this._canRedo()}
              .label=${this.translations?.redoShortcut??"Redo"}
            ></ha-icon-button>
            <ha-icon-button
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              @click=${this._closeEditor}
              .label=${this.translations?.close??"Close"}
            ></ha-icon-button>
          </div>
        </div>

        <div aria-live="polite">
          ${this._validationWarnings.length>0?ne`
                <ha-alert alert-type="warning" .title=${this.translations?.warningsTitle??""}>
                  <ul class="warnings-list">
                    ${this._validationWarnings.map(e=>ne`<li class="warning-item">
                          ${this._translateValidationMessage(e)}
                        </li>`)}
                  </ul>
                </ha-alert>
              `:""}
        </div>

        <!-- Base Temperature Section -->
        <div class="base-temperature-section">
          <div class="base-temperature-header">
            <span class="base-temp-label">${this.translations?.baseTemperature??""}</span>
            <span class="base-temp-description"
              >${this.translations?.baseTemperatureDescription??""}</span
            >
          </div>
          <div class="base-temperature-input">
            <input
              type="number"
              class="temp-input base-temp-input"
              .value=${this._editingBaseTemperature?.toString()||"20.0"}
              step=${this.tempStep}
              min=${this.minTemp}
              max=${this.maxTemp}
              @change=${e=>{this._saveHistoryState(),this._editingBaseTemperature=parseFloat(e.target.value),this.requestUpdate()}}
            />
            <span class="temp-unit">${this.temperatureUnit}</span>
            <div
              class="color-indicator"
              style="background-color: ${He(this._editingBaseTemperature||20)}"
            ></div>
          </div>
        </div>

        <div class="editor-content-label">${this.translations?.temperaturePeriods??""}</div>
        <div class="editor-content">
          <div class="time-block-header">
            <span class="header-cell header-from">${this.translations?.from??""}</span>
            <span class="header-cell header-to">${this.translations?.to??""}</span>
            <span class="header-cell header-temp">Temp</span>
            <span class="header-cell header-actions"></span>
          </div>
          ${e.map((t,i)=>{const s=this._editingBlocks.findIndex(e=>e.startMinutes===t.startMinutes&&e.endMinutes===t.endMinutes),a=!(-1!==s);return void 0!==this._editingSlotIndex&&this._editingSlotIndex===s&&void 0!==this._editingSlotData&&this._editingSlotData?ne`
                <div class="time-block-editor editing">
                  <input
                    type="time"
                    class="time-input"
                    .value=${this._editingSlotData.startTime}
                    @change=${e=>{this._editingSlotData&&(this._editingSlotData={...this._editingSlotData,startTime:e.target.value},this.requestUpdate())}}
                  />
                  <input
                    type="time"
                    class="time-input"
                    .value=${"24:00"===this._editingSlotData.endTime?"23:59":this._editingSlotData.endTime}
                    @change=${e=>{if(this._editingSlotData){let t=e.target.value;"23:59"===t&&(t="24:00"),this._editingSlotData={...this._editingSlotData,endTime:t},this.requestUpdate()}}}
                  />
                  <div class="temp-input-group">
                    <input
                      type="number"
                      class="temp-input"
                      .value=${this._editingSlotData.temperature.toString()}
                      step=${this.tempStep}
                      min=${this.minTemp}
                      max=${this.maxTemp}
                      @change=${e=>{this._editingSlotData&&(this._editingSlotData={...this._editingSlotData,temperature:parseFloat(e.target.value)},this.requestUpdate())}}
                    />
                    <span class="temp-unit">${this.temperatureUnit}</span>
                  </div>
                  <div class="slot-actions">
                    <ha-button @click=${this._saveSlotEdit}>
                      ${this.translations?.saveSlot??"Save"}
                    </ha-button>
                    <ha-button @click=${this._cancelSlotEdit}>
                      ${this.translations?.cancelSlotEdit??"Cancel"}
                    </ha-button>
                  </div>
                  <div
                    class="color-indicator"
                    style="background-color: ${He(this._editingSlotData.temperature)}"
                  ></div>
                </div>
              `:ne`
              <div class="time-block-editor ${a?"base-temp-slot":""}">
                <span class="time-display">${this._formatTimeDisplay(t.startTime)}</span>
                <span class="time-display">${this._formatTimeDisplay(t.endTime)}</span>
                <div class="temp-display-group">
                  <span class="temp-display">${t.temperature.toFixed(1)}</span>
                  <span class="temp-unit">${this.temperatureUnit}</span>
                </div>
                <div class="slot-actions">
                  ${a?ne``:ne`
                        <ha-button
                          @click=${()=>this._startSlotEditFromDisplay(i,e)}
                          .disabled=${void 0!==this._editingSlotIndex}
                        >
                          ${this.translations?.editSlot??"Edit"}
                        </ha-button>
                        <ha-icon-button
                          class="remove-btn"
                          .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                          @click=${()=>this._removeTimeBlockByIndex(i,e)}
                          .disabled=${void 0!==this._editingSlotIndex}
                          .label=${this.translations?.removeSlot??"Remove"}
                        ></ha-icon-button>
                      `}
                </div>
                <div
                  class="color-indicator"
                  style="background-color: ${He(t.temperature)}"
                ></div>
              </div>
            `})}
          ${this._editingBlocks.length<12&&void 0===this._editingSlotIndex?ne`
                <ha-button class="add-btn" @click=${this._addNewSlot}>
                  ${this.translations?.addTimeBlock??"+ Add Time Block"}
                </ha-button>
              `:""}
        </div>

        <div class="editor-footer">
          <ha-button @click=${this._closeEditor}>
            ${this.translations?.cancel??"Cancel"}
          </ha-button>
          <ha-button @click=${this._saveSchedule}> ${this.translations?.save??"Save"} </ha-button>
        </div>
      </div>
    `}static{this.styles=ft}};yt([Ae({type:Boolean})],bt.prototype,"open",void 0),yt([Ae({type:String})],bt.prototype,"weekday",void 0),yt([Ae({attribute:!1})],bt.prototype,"scheduleData",void 0),yt([Ae({type:Number})],bt.prototype,"minTemp",void 0),yt([Ae({type:Number})],bt.prototype,"maxTemp",void 0),yt([Ae({type:Number})],bt.prototype,"tempStep",void 0),yt([Ae({type:String})],bt.prototype,"temperatureUnit",void 0),yt([Ae({type:String})],bt.prototype,"hourFormat",void 0),yt([Ae({attribute:!1})],bt.prototype,"translations",void 0),yt([De()],bt.prototype,"_editingWeekday",void 0),yt([De()],bt.prototype,"_editingBlocks",void 0),yt([De()],bt.prototype,"_editingBaseTemperature",void 0),yt([De()],bt.prototype,"_validationWarnings",void 0),yt([De()],bt.prototype,"_editingSlotIndex",void 0),yt([De()],bt.prototype,"_editingSlotData",void 0),bt=yt([st("hmip-schedule-editor")],bt);const xt=$`
  :host {
    display: block;
  }

  .schedule-list {
    display: flex;
    flex-direction: column;
  }

  .toolbar {
    margin-top: 12px;
    display: flex;
    justify-content: flex-end;
  }

  .collapse-toggle {
    display: flex;
    justify-content: center;
    margin-top: 8px;
  }

  .collapse-toggle ha-button {
    --ha-button-color: var(--secondary-text-color);
    font-size: 13px;
  }

  ha-button {
    --ha-button-color: var(--primary-color);
  }

  .no-data {
    text-align: center;
    padding: 32px;
    color: var(--secondary-text-color);
  }

  .events-table {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .event-card {
    border: 1px solid var(--divider-color);
    border-radius: 8px;
    overflow: hidden;
    transition: background-color 0.2s;
  }

  .event-card.inactive {
    opacity: 0.5;
  }

  .event-card:hover {
    background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.05);
  }

  .event-row-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px 4px;
    gap: 8px;
  }

  .col-condition {
    font-weight: 500;
    font-size: 14px;
    color: var(--primary-text-color);
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .col-actions {
    display: flex;
    gap: 0;
    flex-shrink: 0;
  }

  ha-icon-button {
    --ha-icon-button-size: 36px;
    color: var(--secondary-text-color);
  }

  .event-row-details {
    padding: 0 16px 4px;
  }

  .col-details-text {
    font-size: 13px;
    color: var(--secondary-text-color);
  }

  .event-row-bottom {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px 10px;
    gap: 12px;
  }

  .col-weekdays {
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }

  .weekday-badges {
    display: flex;
    gap: 3px;
    flex-wrap: wrap;
  }

  .weekday-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 26px;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    line-height: 1;
  }

  .weekday-badge.active {
    background-color: var(--primary-color);
    color: var(--text-primary-color);
  }

  .weekday-badge.inactive {
    background-color: var(--divider-color);
    color: var(--disabled-text-color, var(--secondary-text-color));
    opacity: 0.5;
  }

  .col-details {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    font-size: 13px;
  }

  .col-state {
    color: var(--primary-text-color);
  }

  .col-state .level-2 {
    color: var(--secondary-text-color);
    font-size: 0.9em;
  }

  .col-duration {
    color: var(--secondary-text-color);
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    .event-row-top {
      padding: 8px 12px 4px;
    }

    .event-row-details {
      padding: 0 12px 4px;
    }

    .event-row-bottom {
      padding: 0 12px 8px;
      flex-wrap: wrap;
    }

    ha-icon-button {
      --ha-icon-button-size: 44px;
    }

    .weekday-badge {
      min-width: 22px;
      padding: 2px 3px;
      font-size: 10px;
    }
  }

  @media (max-width: 480px) {
    .col-condition {
      font-size: 13px;
    }

    .weekday-badge {
      min-width: 20px;
      padding: 1px 2px;
      font-size: 9px;
    }
  }

  /* Swipe-to-delete wrapper */
  .event-card-wrapper {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
  }

  .swipe-delete-bg {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 80px;
    background: var(--error-color, #db4437);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    border-radius: 0 8px 8px 0;
  }

  .swipe-delete-bg ha-icon {
    --ha-icon-display-size: 24px;
    color: white;
  }

  .event-card.swiping {
    transition: none !important;
  }

  /* Touch device optimizations */
  @media (hover: none) and (pointer: coarse) {
    .event-card:hover {
      background-color: transparent;
    }

    .event-card:active {
      background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
    }

    .event-card:not(.swiping) {
      transition:
        transform 0.2s ease-out,
        background-color 0.2s;
    }
  }
`;var wt=function(e,t,i,s){var a,o=arguments.length,n=o<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var r=e.length-1;r>=0;r--)(a=e[r])&&(n=(o<3?a(n):o>3?a(t,i,n):a(t,i))||n);return o>3&&n&&Object.defineProperty(t,i,n),n};let $t=class extends ke{constructor(){super(...arguments),this.editable=!0,this.collapseAfter=0,this._expanded=!1,this._swipeX=0,this._touchStartX=0,this._touchStartY=0,this._isSwiping=!1,this._isScrolling=!1}static{this.styles=xt}_onTouchStart(e,t){if(!this.editable)return;const i=e.touches[0];this._touchStartX=i.clientX,this._touchStartY=i.clientY,this._isSwiping=!1,this._isScrolling=!1,this._swipingGroupNo=t,this._swipeX=0}_onTouchMove(e){if(!this._swipingGroupNo)return;const t=e.touches[0],i=t.clientX-this._touchStartX,s=t.clientY-this._touchStartY;if(!this._isSwiping&&!this._isScrolling){if(Math.abs(s)>10)return this._isScrolling=!0,this._swipingGroupNo=void 0,void(this._swipeX=0);Math.abs(i)>10&&(this._isSwiping=!0)}this._isScrolling||this._isSwiping&&(e.preventDefault(),this._swipeX=Math.min(0,i))}_onTouchEnd(e){this._swipingGroupNo&&this._isSwiping?Math.abs(this._swipeX)>=120?(this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:e}})),this._resetSwipe()):(this._swipeX=0,setTimeout(()=>this._resetSwipe(),200)):this._resetSwipe()}_resetSwipe(){this._swipingGroupNo=void 0,this._swipeX=0,this._isSwiping=!1,this._isScrolling=!1}_handleAdd(){this.dispatchEvent(new CustomEvent("add-event",{bubbles:!0,composed:!0}))}_handleEdit(e){this.dispatchEvent(new CustomEvent("edit-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}_handleDelete(e){this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}_getConditionDisplay(e){return function(e,t,i){const s=function(e,t,i){const s="sunset"===e?i.sunset:i.sunrise;return 0===t?s:`${s} ${t>0?"+":""}${t}min`}(e.astro_type,e.astro_offset_minutes,i),a=e.time;switch(e.condition){case"fixed_time":default:return{label:t,details:a};case"astro":return{label:t,details:s};case"earliest":case"latest":case"astro_if_before_fixed":case"astro_if_after_fixed":return{label:t,details:`${s} / ${a}`};case"fixed_if_before_astro":case"fixed_if_after_astro":return{label:t,details:`${a} / ${s}`}}}(e,this.translations.conditionLabels[e.condition]||e.condition,this.translations.conditionSummaryLabels)}_toggleExpanded(){this._expanded=!this._expanded}render(){if(!this.scheduleData)return ne`<div class="no-data">${this.translations.loading}</div>`;const e=function(e){const t=[];for(const[i,s]of Object.entries(e))t.push({...s,groupNo:i,isActive:je(s)});return t.sort((e,t)=>e.time.localeCompare(t.time)),t}(this.scheduleData);if(0===e.length)return ne`
        <div class="no-data">
          <p>${this.translations.noScheduleEvents}</p>
          ${this.editable?ne`<ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>`:""}
        </div>
      `;const t=this.collapseAfter>0&&e.length>this.collapseAfter,i=t&&!this._expanded?e.slice(0,this.collapseAfter):e,s=e.length-this.collapseAfter;return ne`
      <div class="schedule-list">
        <div class="events-table">
          ${mt(i,e=>e.groupNo,e=>this._renderEvent(e))}
        </div>
        ${t?ne`<div class="collapse-toggle">
              <ha-button @click=${this._toggleExpanded}>
                ${this._expanded?this.translations.showLess:`${this.translations.showMore} (${s})`}
              </ha-button>
            </div>`:""}
        ${this.editable?ne`<div class="toolbar">
              <ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>
            </div>`:""}
      </div>
    `}_renderEvent(e){const t=function(e,t,i){const s=t?Pe[t]:void 0;if("binary"===s?.levelType){const t=i?.on??"On";return 0===e?i?.off??"Off":t}const a=100*e;return`${Math.round(a)}%`}(e.level,this.domain,{on:this.translations.levelOn,off:this.translations.levelOff}),i=function(e){if(!e)return"-";const t=qe(e);return t?`${t.value}${{ms:"ms",s:"s",min:"min",h:"h"}[t.unit]}`:e}(e.duration),{label:s,details:a}=this._getConditionDisplay(e),o=this._swipingGroupNo===e.groupNo,n=o?this._swipeX:0;return ne`
      <div class="event-card-wrapper">
        ${o&&n<-40?ne`<div class="swipe-delete-bg">
              <ha-icon .icon=${"mdi:delete"}></ha-icon>
            </div>`:""}
        <div
          class="event-card ${e.isActive?"active":"inactive"} ${o&&this._isSwiping?"swiping":""}"
          style=${o&&this._isSwiping?`transform: translateX(${n}px)`:""}
          @touchstart=${t=>this._onTouchStart(t,e.groupNo)}
          @touchmove=${e=>this._onTouchMove(e)}
          @touchend=${()=>this._onTouchEnd(e)}
        >
          <div class="event-row-top">
            <div class="col-condition">${s}</div>
            ${this.editable?ne`<div class="col-actions">
                  <ha-icon-button
                    .path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}
                    @click=${()=>this._handleEdit(e)}
                    .label=${this.translations?.editEvent??"Edit"}
                  ></ha-icon-button>
                  <ha-icon-button
                    .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                    @click=${()=>this._handleDelete(e)}
                    .label=${this.translations?.deleteEvent??"Delete"}
                  ></ha-icon-button>
                </div>`:""}
          </div>
          <div class="event-row-details">
            <span class="col-details-text">${a}</span>
          </div>
          <div class="event-row-bottom">
            <div class="col-weekdays">
              <div class="weekday-badges">
                ${Ce.map(t=>{const i=e.weekdays.includes(t);return ne`<span class="weekday-badge ${i?"active":"inactive"}"
                    >${this.translations.weekdayShortLabels[t]}</span
                  >`})}
              </div>
            </div>
            <div class="col-details">
              <span class="col-state">
                ${t}
                ${null!==e.level_2?ne`<span class="level-2"
                      >, ${this.translations.slat}: ${Math.round(100*e.level_2)}%</span
                    >`:""}
              </span>
              ${"-"!==i?ne`<span class="col-duration">${i}</span>`:""}
            </div>
          </div>
        </div>
      </div>
    `}};wt([Ae({attribute:!1})],$t.prototype,"scheduleData",void 0),wt([Ae({attribute:!1})],$t.prototype,"domain",void 0),wt([Ae({type:Boolean})],$t.prototype,"editable",void 0),wt([Ae({type:Number})],$t.prototype,"collapseAfter",void 0),wt([Ae({attribute:!1})],$t.prototype,"translations",void 0),wt([De()],$t.prototype,"_expanded",void 0),wt([De()],$t.prototype,"_swipingGroupNo",void 0),wt([De()],$t.prototype,"_swipeX",void 0),$t=wt([st("hmip-device-schedule-list")],$t);const kt=$`
  :host {
    display: block;
  }

  /* Dialog styles */
  ha-dialog {
    --ha-dialog-max-width: min(500px, 95vw);
    --ha-dialog-max-height: 90vh;
  }

  .editor-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
    max-height: calc(90vh - 200px);
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .form-group label {
    font-weight: 500;
    font-size: 14px;
    color: var(--primary-text-color);
  }

  .form-group input[type="time"],
  .form-group input[type="text"],
  .form-group input[type="number"] {
    padding: 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
  }

  ha-select {
    width: 100%;
  }

  ha-slider {
    width: 100%;
  }

  .slider-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .slider-group ha-slider {
    flex: 1;
  }

  .slider-value {
    min-width: 40px;
    text-align: right;
    font-size: 14px;
    color: var(--primary-text-color);
  }

  .duration-row {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .duration-row input[type="number"] {
    flex: 1;
    padding: 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
  }

  .duration-row ha-select {
    min-width: 80px;
    flex: 0 0 auto;
  }

  .weekday-checkboxes,
  .channel-checkboxes {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .validation-list {
    margin: 0;
    padding-left: 20px;
    list-style-type: disc;
  }

  .validation-list li {
    font-size: 13px;
    line-height: 1.6;
    margin: 4px 0;
  }

  .editor-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 8px;
    padding-top: 16px;
    border-top: 1px solid var(--divider-color);
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    ha-dialog {
      --ha-dialog-max-width: 100vw;
      --ha-dialog-max-height: 100vh;
    }

    .editor-content {
      max-height: calc(100vh - 150px);
    }

    .editor-footer {
      flex-direction: column-reverse;
      gap: 8px;
      position: sticky;
      bottom: 0;
      background-color: var(--card-background-color, #fff);
      margin: 0 -16px -16px;
      padding: 16px;
      z-index: 1;
    }

    .editor-footer ha-button {
      width: 100%;
    }

    .form-group input[type="time"],
    .form-group input[type="text"],
    .form-group input[type="number"] {
      font-size: 16px;
      min-height: 44px;
    }
  }
`;var St=function(e,t,i,s){var a,o=arguments.length,n=o<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var r=e.length-1;r>=0;r--)(a=e[r])&&(n=(o<3?a(n):o>3?a(t,i,n):a(t,i))||n);return o>3&&n&&Object.defineProperty(t,i,n),n};let Et=class extends ke{constructor(){super(...arguments),this.open=!1,this.isNewEvent=!1,this._validationErrors=[]}static{this.styles=kt}willUpdate(e){(e.has("open")||e.has("entry"))&&(this.open&&this.entry?(this._editingEntry={...this.entry},this._validationErrors=[]):this.open||(this._editingEntry=void 0,this._validationErrors=[]))}updated(e){super.updated(e),e.has("open")&&this.open&&!e.get("open")&&this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector("input[type='time'], ha-select, input");e?.focus()})}_updateEditingEntry(e){this._editingEntry&&(this._editingEntry={...this._editingEntry,...e},this._validationErrors=[],this.requestUpdate())}_handleClose(){this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_handleSave(){if(!this._editingEntry||void 0===this.groupNo)return;const e=function(e,t){const i=[];(function(e){try{return function(e){const t=e.split(":");if(2!==t.length)throw new Error(`Invalid time format: ${e}`);const i=parseInt(t[0],10),s=parseInt(t[1],10);if(isNaN(i)||isNaN(s)||i<0||i>23||s<0||s>59)throw new Error(`Invalid time values: ${e}`)}(e),!0}catch{return!1}})(e.time)||i.push({field:"time",message:"Time must be in HH:MM format (00:00-23:59)"}),e.weekdays&&0!==e.weekdays.length||i.push({field:"weekdays",message:"At least one weekday must be selected"});const s=t?Pe[t]:void 0;return"binary"===s?.levelType?0!==e.level&&1!==e.level&&i.push({field:"level",message:"Level must be 0 or 1 for switch"}):(e.level<0||e.level>1)&&i.push({field:"level",message:"Level must be between 0.0 and 1.0"}),"cover"===t&&null!==e.level_2&&(e.level_2<0||e.level_2>1)&&i.push({field:"level_2",message:"Slat position must be between 0.0 and 1.0"}),Ze(e.condition)&&(e.astro_offset_minutes<-720||e.astro_offset_minutes>720)&&i.push({field:"astro_offset_minutes",message:"Astro offset must be between -720 and 720 minutes"}),null===e.duration||Ge(e.duration)||i.push({field:"duration",message:"Invalid duration format"}),null===e.ramp_time||Ge(e.ramp_time)||i.push({field:"ramp_time",message:"Invalid ramp time format"}),i}(this._editingEntry,this.domain);e.length>0?this._validationErrors=e.map(e=>`${e.field}: ${e.message}`):this.dispatchEvent(new CustomEvent("save-event",{bubbles:!0,composed:!0,detail:{entry:{...this._editingEntry},groupNo:this.groupNo}}))}render(){return this.open&&this._editingEntry?ne`
      <ha-dialog
        open
        @closed=${this._handleClose}
        .heading=${this.isNewEvent?this.translations.addEvent:this.translations.editEvent}
      >
        <div class="editor-content">
          ${this._renderTimeFields()} ${this._renderConditionFields()}
          ${this._renderWeekdayFields()} ${this._renderLevelFields()}
          ${this._renderDurationFields()} ${this._renderRampTimeFields()}
          ${this._renderChannelFields()} ${this._renderValidationErrors()}
          <div class="editor-footer">
            <ha-button @click=${this._handleClose}> ${this.translations.cancel} </ha-button>
            <ha-button @click=${this._handleSave}> ${this.translations.save} </ha-button>
          </div>
        </div>
      </ha-dialog>
    `:ne``}_renderValidationErrors(){return ne`
      <div aria-live="polite">
        ${this._validationErrors.length>0?ne`
              <ha-alert alert-type="error">
                <ul class="validation-list">
                  ${this._validationErrors.map(e=>ne`<li>${e}</li>`)}
                </ul>
              </ha-alert>
            `:""}
      </div>
    `}_renderTimeFields(){return this._editingEntry?ne`
      <div class="form-group">
        <label>${this.translations.time}</label>
        <input
          type="time"
          .value=${this._editingEntry.time}
          @change=${e=>{const t=e.target;this._updateEditingEntry({time:t.value})}}
        />
      </div>
    `:ne``}_renderConditionFields(){if(!this._editingEntry)return ne``;const e=Ze(this._editingEntry.condition);return ne`
      <div class="form-group">
        <label>${this.translations.condition}</label>
        <ha-select
          .value=${this._editingEntry.condition}
          .options=${Me.map(e=>({value:e,label:this.translations.conditionLabels[e]||e}))}
          @selected=${e=>{e.stopPropagation();const t=e.detail.value,i={condition:t};"fixed_time"===t?(i.astro_type=null,i.astro_offset_minutes=0):null===this._editingEntry.astro_type&&(i.astro_type="sunrise"),this._updateEditingEntry(i)}}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>
      ${e?ne`
            <div class="form-group">
              <label>${this.translations.astroSunrise}/${this.translations.astroSunset}</label>
              <ha-select
                .value=${this._editingEntry.astro_type||"sunrise"}
                .options=${[{value:"sunrise",label:this.translations.astroSunrise},{value:"sunset",label:this.translations.astroSunset}]}
                @selected=${e=>{e.stopPropagation();const t=e.detail.value;this._updateEditingEntry({astro_type:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            </div>
            <div class="form-group">
              <label>${this.translations.astroOffset}</label>
              <input
                type="number"
                min="-720"
                max="720"
                .value=${String(this._editingEntry.astro_offset_minutes)}
                @input=${e=>{const t=parseInt(e.target.value,10);isNaN(t)||this._updateEditingEntry({astro_offset_minutes:t})}}
              />
            </div>
          `:""}
    `}_renderWeekdayFields(){return this._editingEntry?ne`
      <div class="form-group">
        <label>${this.translations.weekdaysLabel}</label>
        <div class="weekday-checkboxes">
          ${Ce.map(e=>{const t=this._editingEntry.weekdays.includes(e);return ne`
              <label class="checkbox-label">
                <ha-checkbox
                  .checked=${t}
                  @change=${t=>{const i=t.target.checked,s=[...this._editingEntry.weekdays];if(i&&!s.includes(e))s.push(e);else if(!i){const t=s.indexOf(e);t>-1&&s.splice(t,1)}this._updateEditingEntry({weekdays:s})}}
                ></ha-checkbox>
                ${this.translations.weekdayShortLabels[e]}
              </label>
            `})}
        </div>
      </div>
    `:ne``}_renderLevelFields(){if(!this._editingEntry)return ne``;const e=this.domain?Pe[this.domain]:void 0,t="binary"===e?.levelType;return ne`
      <div class="form-group">
        <label>${this.translations.stateLabel}</label>
        ${t?ne`
              <ha-select
                .value=${String(this._editingEntry.level)}
                .options=${[{value:"0",label:this.translations.levelOff},{value:"1",label:this.translations.levelOn}]}
                @selected=${e=>{e.stopPropagation();const t=parseInt(e.detail.value,10);this._updateEditingEntry({level:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            `:ne`
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*this._editingEntry.level)}
                  @change=${e=>{const t=Number(e.target.value);this._updateEditingEntry({level:t/100})}}
                ></ha-slider>
                <span class="slider-value">${Math.round(100*this._editingEntry.level)}%</span>
              </div>
            `}
      </div>
      ${e?.hasLevel2?ne`
            <div class="form-group">
              <label>${this.translations.slat}</label>
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*(this._editingEntry.level_2||0))}
                  @change=${e=>{const t=Number(e.target.value);this._updateEditingEntry({level_2:t/100})}}
                ></ha-slider>
                <span class="slider-value"
                  >${Math.round(100*(this._editingEntry.level_2||0))}%</span
                >
              </div>
            </div>
          `:""}
    `}_renderDurationFields(){if(!this._editingEntry)return ne``;const e=this.domain?Pe[this.domain]:void 0;if(e&&!e.hasDuration)return ne``;const t=this._editingEntry.duration?qe(this._editingEntry.duration):null,i=t?.value??0,s=t?.unit??"s";return ne`
      <div class="form-group">
        <label>${this.translations.duration}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({duration:Je(t,s)}):this._updateEditingEntry({duration:null})}}
          />
          <ha-select
            .value=${s}
            .options=${Le.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation();const t=e.detail.value;i>0&&this._updateEditingEntry({duration:Je(i,t)})}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderRampTimeFields(){if(!this._editingEntry)return ne``;const e=this.domain?Pe[this.domain]:void 0;if(e&&!e.hasRampTime)return ne``;const t=this._editingEntry.ramp_time?qe(this._editingEntry.ramp_time):null,i=t?.value??0,s=t?.unit??"s";return ne`
      <div class="form-group">
        <label>${this.translations.rampTime}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({ramp_time:Je(t,s)}):this._updateEditingEntry({ramp_time:null})}}
          />
          <ha-select
            .value=${s}
            .options=${Le.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation();const t=e.detail.value;i>0&&this._updateEditingEntry({ramp_time:Je(i,t)})}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderChannelFields(){return this._editingEntry&&this.availableTargetChannels&&Object.keys(this.availableTargetChannels).length>0?ne`
        <div class="form-group">
          <label>${this.translations.channels}</label>
          <div class="channel-checkboxes">
            ${Object.entries(this.availableTargetChannels).map(([e,t])=>{const i=this._editingEntry.target_channels.includes(e);return ne`
                <label class="checkbox-label">
                  <ha-checkbox
                    .checked=${i}
                    @change=${t=>{const i=t.target.checked,s=[...this._editingEntry.target_channels];if(i&&!s.includes(e))s.push(e);else if(!i){const t=s.indexOf(e);t>-1&&s.splice(t,1)}this._updateEditingEntry({target_channels:s})}}
                  ></ha-checkbox>
                  ${t.name||e}
                </label>
              `})}
          </div>
        </div>
      `:ne``}};St([Ae({type:Boolean})],Et.prototype,"open",void 0),St([Ae({attribute:!1})],Et.prototype,"entry",void 0),St([Ae()],Et.prototype,"groupNo",void 0),St([Ae({type:Boolean})],Et.prototype,"isNewEvent",void 0),St([Ae({attribute:!1})],Et.prototype,"domain",void 0),St([Ae({attribute:!1})],Et.prototype,"availableTargetChannels",void 0),St([Ae({attribute:!1})],Et.prototype,"translations",void 0),St([De()],Et.prototype,"_editingEntry",void 0),St([De()],Et.prototype,"_validationErrors",void 0),Et=St([st("hmip-device-schedule-editor")],Et);const Tt={en:{weekdays:{short:{monday:"Mo",tuesday:"Tu",wednesday:"We",thursday:"Th",friday:"Fr",saturday:"Sa",sunday:"Su"},long:{monday:"Monday",tuesday:"Tuesday",wednesday:"Wednesday",thursday:"Thursday",friday:"Friday",saturday:"Saturday",sunday:"Sunday"}},domains:{switch:"Switch",light:"Light",cover:"Cover",valve:"Valve"},conditions:{fixed_time:"Fixed Time",astro:"Astro",fixed_if_before_astro:"Fixed if before Astro",astro_if_before_fixed:"Astro if before Fixed",fixed_if_after_astro:"Fixed if after Astro",astro_if_after_fixed:"Astro if after Fixed",earliest:"Earliest",latest:"Latest"},ui:{schedule:"Schedule",loading:"Loading schedule data...",entityNotFound:"Entity {entity} not found",clickToEdit:"Click on a day to edit its schedule",edit:"Edit {weekday}",cancel:"Cancel",save:"Save",addTimeBlock:"+ Add Time Block",copySchedule:"Copy schedule",pasteSchedule:"Paste schedule",undo:"Undo",redo:"Redo",undoShortcut:"Undo (Ctrl+Z)",redoShortcut:"Redo (Ctrl+Y)",toggleCompactView:"Compact view",toggleFullView:"Full view",exportSchedule:"Export",importSchedule:"Import",exportTooltip:"Export schedule to JSON file",importTooltip:"Import schedule from JSON file",exportSuccess:"Schedule exported successfully",importSuccess:"Schedule imported successfully",unsavedChanges:"Unsaved changes",saveAll:"Save all",discard:"Discard",enableDragDrop:"Enable drag & drop mode",disableDragDrop:"Disable drag & drop mode",confirmDiscardChanges:"You have unsaved changes. Do you want to discard them?",close:"Close",level:"Level",levelOn:"On",levelOff:"Off",slat:"Slat Position",addEvent:"Add Event",editEvent:"Edit Event",deleteEvent:"Delete Event",time:"Time",duration:"Duration",rampTime:"Ramp Time",state:"State",weekdays:"Weekdays",channels:"Target Channels",condition:"Condition",astroSunrise:"Sunrise",astroSunset:"Sunset",astroOffset:"Astro Offset (min)",or:"or",ifBefore:"if before",ifAfter:"if after",maxEntriesReached:"Maximum number of entries reached ({max})",showMore:"Show more",showLess:"Show less",confirmDelete:"Are you sure you want to delete this event?",weeklyProgram:"Weekly program",weeklyProgramEnabled:"Weekly program active",weeklyProgramDisabled:"Weekly program inactive",weeklyProgramEnableFailed:"Failed to enable/disable weekly program."},errors:{failedToChangeProfile:"Failed to change profile: {error}",failedToSaveSchedule:"Failed to save schedule: {error}",failedToPasteSchedule:"Failed to paste schedule: {error}",invalidSchedule:"Invalid schedule: {error}",failedToExport:"Failed to export schedule: {error}",failedToImport:"Failed to import schedule: {error}",invalidImportFile:"Invalid file format. Please select a JSON file.",invalidImportFormat:"Invalid JSON format in file.",invalidImportData:"Invalid schedule data: {error}",incompatibleEntity:"Entity {entity} is not a compatible schedule entity (requires schedule_type 'default')",insufficientPermissions:"You don't have permission to perform this action."},warnings:{title:"Validation Warnings",noWarnings:"No issues detected"}},de:{weekdays:{short:{monday:"Mo",tuesday:"Di",wednesday:"Mi",thursday:"Do",friday:"Fr",saturday:"Sa",sunday:"So"},long:{monday:"Montag",tuesday:"Dienstag",wednesday:"Mittwoch",thursday:"Donnerstag",friday:"Freitag",saturday:"Samstag",sunday:"Sonntag"}},domains:{switch:"Schalter",light:"Licht",cover:"Rollladen",valve:"Ventil"},conditions:{fixed_time:"Feste Zeit",astro:"Astro",fixed_if_before_astro:"Fest wenn vor Astro",astro_if_before_fixed:"Astro wenn vor Fest",fixed_if_after_astro:"Fest wenn nach Astro",astro_if_after_fixed:"Astro wenn nach Fest",earliest:"Frühester",latest:"Spätester"},ui:{schedule:"Zeitplan",loading:"Zeitplandaten werden geladen...",entityNotFound:"Entität {entity} nicht gefunden",clickToEdit:"Klicken Sie auf einen Tag, um den Zeitplan zu bearbeiten",edit:"{weekday} bearbeiten",cancel:"Abbrechen",save:"Speichern",addTimeBlock:"+ Zeitblock hinzufügen",copySchedule:"Zeitplan kopieren",pasteSchedule:"Zeitplan einfügen",undo:"Rückgängig",redo:"Wiederholen",undoShortcut:"Rückgängig (Strg+Z)",redoShortcut:"Wiederholen (Strg+Y)",toggleCompactView:"Kompaktansicht",toggleFullView:"Vollansicht",exportSchedule:"Exportieren",importSchedule:"Importieren",exportTooltip:"Zeitplan als JSON-Datei exportieren",importTooltip:"Zeitplan aus JSON-Datei importieren",exportSuccess:"Zeitplan erfolgreich exportiert",importSuccess:"Zeitplan erfolgreich importiert",unsavedChanges:"Ungespeicherte Änderungen",saveAll:"Alle speichern",discard:"Verwerfen",enableDragDrop:"Drag & Drop Modus aktivieren",disableDragDrop:"Drag & Drop Modus deaktivieren",confirmDiscardChanges:"Sie haben ungespeicherte Änderungen. Möchten Sie diese verwerfen?",close:"Schließen",level:"Stufe",levelOn:"Ein",levelOff:"Aus",slat:"Lamellenposition",addEvent:"Ereignis hinzufügen",editEvent:"Ereignis bearbeiten",deleteEvent:"Ereignis löschen",time:"Zeit",duration:"Dauer",rampTime:"Rampenzeit",state:"Zustand",weekdays:"Wochentage",channels:"Zielkanäle",condition:"Bedingung",astroSunrise:"Sonnenaufgang",astroSunset:"Sonnenuntergang",astroOffset:"Astro-Offset (Min.)",or:"oder",ifBefore:"wenn vor",ifAfter:"wenn nach",maxEntriesReached:"Maximale Anzahl an Einträgen erreicht ({max})",showMore:"Mehr anzeigen",showLess:"Weniger anzeigen",confirmDelete:"Möchten Sie dieses Ereignis wirklich löschen?",weeklyProgram:"Wochenprogramm",weeklyProgramEnabled:"Wochenprogramm aktiv",weeklyProgramDisabled:"Wochenprogramm inaktiv",weeklyProgramEnableFailed:"Fehler beim Aktivieren/Deaktivieren des Wochenprogramms."},errors:{failedToChangeProfile:"Fehler beim Wechseln des Profils: {error}",failedToSaveSchedule:"Fehler beim Speichern des Zeitplans: {error}",failedToPasteSchedule:"Fehler beim Einfügen des Zeitplans: {error}",invalidSchedule:"Ungültiger Zeitplan: {error}",failedToExport:"Fehler beim Exportieren des Zeitplans: {error}",failedToImport:"Fehler beim Importieren des Zeitplans: {error}",invalidImportFile:"Ungültiges Dateiformat. Bitte wählen Sie eine JSON-Datei.",invalidImportFormat:"Ungültiges JSON-Format in der Datei.",invalidImportData:"Ungültige Zeitplandaten: {error}",incompatibleEntity:"Entität {entity} ist keine kompatible Zeitplan-Entität (erfordert schedule_type 'default')",insufficientPermissions:"Sie haben keine Berechtigung für diese Aktion."},warnings:{title:"Validierungswarnungen",noWarnings:"Keine Probleme erkannt"}}};function At(e){const t=e.toLowerCase().split("-")[0];return Tt[t]||Tt.en}function Dt(e,t){let i=e;for(const[e,s]of Object.entries(t))i=i.replace(`{${e}}`,s);return i}let Ct=class extends ke{constructor(){super(...arguments),this._isLoading=!1,this._translations=At("en"),this._showEditor=!1,this._isNewEvent=!1,this._alertType="error"}get _isEditable(){return this._config?.editable??!0}setConfig(e){const t=[],i=e=>{if(!e)return;const i=e.trim();i&&(t.includes(i)||t.push(i))};if(i(e.entity),Array.isArray(e.entities)&&e.entities.forEach(e=>i(e)),0===t.length)return this._config={editable:!0,hour_format:"24",...e,entity:"",entities:[]},this._activeEntityId=void 0,void(this._scheduleData=void 0);t.sort((e,t)=>e.localeCompare(t));const s=this._activeEntityId,a=t[0],o=s&&t.includes(s)?s:a;this._config={editable:!0,hour_format:"24",...e,entity:a,entities:[...t]},this._activeEntityId=o,this._editingEntry=void 0,this._editingGroupNo=void 0,this._showEditor=!1,this._updateLanguage()}_updateLanguage(){let e="en";this._config?.language?e=this._config.language:this.hass?.language?e=this.hass.language:this.hass?.locale?.language&&(e=this.hass.locale.language),this._translations=At(e)}shouldUpdate(e){if(e.has("hass")){const t=e.get("hass");if(this.hass&&t){if(this.hass.language===t.language&&this.hass.locale?.language===t.locale?.language||this._updateLanguage(),this._activeEntityId&&!this._isLoading){const e=t.states?.[this._activeEntityId],i=this.hass.states?.[this._activeEntityId];e!==i&&this._updateScheduleData()}}else this.hass&&!t&&(this._updateLanguage(),this._updateScheduleData())}return e.has("_activeEntityId")&&this._updateScheduleData(),!0}_isValidScheduleEntity(e){const t=this.hass?.states?.[e];return!!t&&Qe(t.attributes)}_updateScheduleData(){if(!this._activeEntityId||!this.hass?.states)return this._scheduleData=void 0,this._domain=void 0,this._availableTargetChannels=void 0,this._maxEntries=void 0,void(this._scheduleEnabled=void 0);const e=this.hass.states[this._activeEntityId];if(!e)return this._scheduleData=void 0,this._domain=void 0,this._availableTargetChannels=void 0,this._maxEntries=void 0,void(this._scheduleEnabled=void 0);const t=e.attributes;if(!Qe(t))return this._scheduleData=void 0,this._domain=void 0,this._availableTargetChannels=void 0,this._maxEntries=void 0,void(this._scheduleEnabled=void 0);this._scheduleData=t.schedule_data?.entries,this._availableTargetChannels=t.available_target_channels,this._maxEntries=t.max_entries,this._scheduleEnabled=t.schedule_enabled,t.schedule_domain?this._domain=t.schedule_domain:this._config?.schedule_domain?this._domain=this._config.schedule_domain:this._domain=void 0}_getEntityName(e){const t=this.hass?.states?.[e];return t?.attributes?.friendly_name||e}_handleEntityChange(e){e.stopPropagation(),this._activeEntityId=e.detail.value,this._closeEditor()}_getDeviceAddress(e){const t=this.hass?.states?.[e];if(t)return ze(t.attributes.address)}_requireDeviceAddress(e){const t=this._getDeviceAddress(e);if(!t)throw new Error(`Cannot determine device address for entity ${e}`);return t}_requireConfigEntryId(e){const t=this.hass?.states?.[e],i=t?.attributes?.config_entry_id;if(!i)throw new Error(`Cannot resolve config_entry_id for entity ${e}. Ensure the entity has a valid config_entry_id attribute.`);return i}_showAlert(e,t="error"){this._alertMessage=e,this._alertType=t}_dismissAlert(){this._alertMessage=void 0}_onAddEvent(){if(this._maxEntries&&this._scheduleData&&Object.keys(this._scheduleData).length>=this._maxEntries)return void this._showAlert(Dt(this._translations.ui.maxEntriesReached,{max:String(this._maxEntries)}),"warning");const e=function(e){const t={weekdays:[],time:"00:00",condition:"fixed_time",astro_type:null,astro_offset_minutes:0,target_channels:[],level:0,level_2:null,duration:null,ramp_time:null};return"cover"===e&&(t.level_2=0),t}(this._domain);if(this._availableTargetChannels){const t=Object.keys(this._availableTargetChannels)[0];t&&(e.target_channels=[t])}const t=this._scheduleData?Object.keys(this._scheduleData).map(e=>parseInt(e,10)):[],i=t.length>0?Math.max(...t):0;this._editingGroupNo=String(i+1),this._editingEntry={...e},this._isNewEvent=!0,this._showEditor=!0}_onEditEvent(e){const t=e.detail.entry;this._editingGroupNo=t.groupNo,this._editingEntry={...t},this._isNewEvent=!1,this._showEditor=!0}_onDeleteEvent(e){if(!confirm(this._translations.ui.confirmDelete||"Delete this event?"))return;const t={...this._scheduleData};delete t[e.detail.entry.groupNo],this._saveSchedule(t)}_onSaveEvent(e){const{entry:t,groupNo:i}=e.detail,s={...this._scheduleData,[i]:t};this._saveSchedule(s),this._closeEditor()}_onEditorClosed(){this._closeEditor()}_closeEditor(){this._showEditor=!1,this._editingEntry=void 0,this._editingGroupNo=void 0,this._isNewEvent=!1}async _handleScheduleEnabledToggle(t){if(!this._activeEntityId||!this.hass||void 0===this._scheduleEnabled)return;const i=this._activeEntityId,s=!this._scheduleEnabled[t];this._startLoading();try{const a=this._requireConfigEntryId(i),o=this._requireDeviceAddress(i);await e(this.hass,a,o,s,t),this._scheduleEnabled={...this._scheduleEnabled,[t]:s}}catch(e){const t=String(e);t.includes("unauthorized")||t.includes("Unauthorized")?this._showAlert(this._translations.errors.insufficientPermissions):this._showAlert(this._translations.ui.weeklyProgramEnableFailed)}finally{this._stopLoading()}}async _saveSchedule(e){if(!this._activeEntityId||!this.hass)return;const i=this._activeEntityId;this._startLoading();try{const s=this._requireConfigEntryId(i),a=this._requireDeviceAddress(i);await t(this.hass,s,a,{entries:Xe(e)}),this._scheduleData=e,this._needsManualReload(i)&&this._scheduleReloadDeviceConfig(i)}catch(e){const t=String(e);t.includes("unauthorized")||t.includes("Unauthorized")?this._showAlert(this._translations.errors.insufficientPermissions):this._showAlert(Dt(this._translations.errors.failedToSaveSchedule,{error:t}))}finally{this._stopLoading()}}_startLoading(){this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1},1e4)}_stopLoading(){this._isLoading=!1,void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0)}_exportSchedule(){if(this._scheduleData&&this._activeEntityId)try{const e=this._getEntityName(this._activeEntityId),t={version:"2.0",entity:this._activeEntityId,schedule_domain:this._domain,exportDate:(new Date).toISOString(),schedule:this._scheduleData},i=new Blob([JSON.stringify(t,null,2)],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s;const o=(new Date).toISOString().split("T")[0];a.download=`schedule-${e.replace(/[^a-zA-Z0-9]/g,"_")}-${o}.json`,document.body.appendChild(a),a.click(),document.body.removeChild(a),URL.revokeObjectURL(s)}catch(e){this._showAlert(Dt(this._translations.errors.failedToExport,{error:String(e)}))}}_importSchedule(){if(!this._isEditable)return;const e=document.createElement("input");e.type="file",e.accept=".json",e.onchange=async e=>{const t=e.target.files?.[0];if(t)try{const e=await t.text(),i=JSON.parse(e);if(!i.schedule||"object"!=typeof i.schedule)throw new Error(this._translations.errors.invalidImportData);if(i.schedule_domain&&i.schedule_domain!==this._domain&&!confirm(`Warning: The imported schedule is for a ${i.schedule_domain} device, but the current entity is a ${this._domain} device. Continue anyway?`))return;await this._saveSchedule(i.schedule)}catch(e){e instanceof SyntaxError?this._showAlert(this._translations.errors.invalidImportFormat):this._showAlert(Dt(this._translations.errors.failedToImport,{error:String(e)}))}},e.click()}_needsManualReload(e){if(!e||!this.hass)return!1;const t=this.hass.states[e];if(!t?.attributes?.interface_id)return!1;const i=t.attributes.interface_id;return i.endsWith("BidCos-RF")||i.endsWith("BidCos-Wired")||i.endsWith("VirtualDevices")}_scheduleReloadDeviceConfig(e){if(!this.hass)return;const t=this._getDeviceAddress(e);if(!t)return void console.warn("Cannot reload device config: address attribute missing");const s=this.hass.states[e],a=s?.attributes?.config_entry_id;a?setTimeout(async()=>{try{await i(this.hass,a,t)}catch{}},5e3):console.warn("Cannot reload device config: config_entry_id missing")}_buildListTranslations(){const e=this._translations;return{weekdayShortLabels:{MONDAY:e.weekdays.short.monday,TUESDAY:e.weekdays.short.tuesday,WEDNESDAY:e.weekdays.short.wednesday,THURSDAY:e.weekdays.short.thursday,FRIDAY:e.weekdays.short.friday,SATURDAY:e.weekdays.short.saturday,SUNDAY:e.weekdays.short.sunday},condition:e.ui.condition,time:e.ui.time,weekdays:e.ui.weekdays,duration:e.ui.duration,state:e.ui.state,addEvent:e.ui.addEvent,editEvent:e.ui.editEvent,deleteEvent:e.ui.deleteEvent,slat:e.ui.slat,noScheduleEvents:"No schedule events configured",loading:e.ui.loading,showMore:e.ui.showMore,showLess:e.ui.showLess,conditionLabels:e.conditions,levelOn:e.ui.levelOn,levelOff:e.ui.levelOff,conditionSummaryLabels:{sunrise:e.ui.astroSunrise,sunset:e.ui.astroSunset,or:e.ui.or,ifBefore:e.ui.ifBefore,ifAfter:e.ui.ifAfter}}}_buildEditorTranslations(){const e=this._translations;return{weekdayShortLabels:{MONDAY:e.weekdays.short.monday,TUESDAY:e.weekdays.short.tuesday,WEDNESDAY:e.weekdays.short.wednesday,THURSDAY:e.weekdays.short.thursday,FRIDAY:e.weekdays.short.friday,SATURDAY:e.weekdays.short.saturday,SUNDAY:e.weekdays.short.sunday},addEvent:e.ui.addEvent,editEvent:e.ui.editEvent,cancel:e.ui.cancel,save:e.ui.save,time:e.ui.time,condition:e.ui.condition,weekdaysLabel:e.ui.weekdays,stateLabel:e.ui.state,duration:e.ui.duration,rampTime:e.ui.rampTime,channels:e.ui.channels,levelOn:e.ui.levelOn,levelOff:e.ui.levelOff,slat:e.ui.slat,astroSunrise:e.ui.astroSunrise,astroSunset:e.ui.astroSunset,astroOffset:e.ui.astroOffset,confirmDelete:e.ui.confirmDelete,conditionLabels:e.conditions}}_renderEntitySelector(){if(!this._config?.entities||this._config.entities.length<=1)return ne``;const e=this._config.entities.filter(e=>this._isValidScheduleEntity(e));return 0===e.length?ne``:ne`
      <ha-select
        class="entity-selector-dropdown"
        .value=${this._activeEntityId||""}
        .options=${e.map(e=>({value:e,label:this._getEntityName(e)}))}
        @selected=${this._handleEntityChange}
        @closed=${e=>e.stopPropagation()}
      ></ha-select>
    `}get _showImportExport(){return this._config?.show_import_export??!1}_renderHeaderControls(){const e=this._config?.entities&&this._config.entities.length>1,t=this._showImportExport;return e||t?ne`
      <div class="header-controls">
        ${e?this._renderEntitySelector():""}
        ${t?ne`<ha-icon-button
                .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
                @click=${this._exportSchedule}
                .label=${this._translations.ui.exportTooltip}
                .disabled=${!this._scheduleData}
              ></ha-icon-button>
              ${this._isEditable?ne`<ha-icon-button
                    .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
                    @click=${this._importSchedule}
                    .label=${this._translations.ui.importTooltip}
                  ></ha-icon-button>`:""}`:""}
      </div>
    `:ne``}render(){if(!this._config||!this.hass)return ne``;const e=this._activeEntityId?this.hass.states?.[this._activeEntityId]:void 0,t=this._config.name||e?.attributes?.friendly_name||this._translations.ui.schedule;return e?this._isValidScheduleEntity(this._activeEntityId)?ne`
      <ha-card>
        <div class="card-header">
          <div class="header-left">
            <div class="card-title">${t}</div>
          </div>
        </div>
        ${this._renderHeaderControls()}
        <div class="card-content">
          ${this._alertMessage?ne`<ha-alert
                .alertType=${this._alertType}
                dismissable
                @alert-dismissed-clicked=${this._dismissAlert}
                >${this._alertMessage}</ha-alert
              >`:""}
          ${void 0!==this._scheduleEnabled?ne`<div class="schedule-enabled-bar">
                <span class="schedule-enabled-title">${this._translations.ui.weeklyProgram}:</span>
                <div class="channel-chips">
                  ${Object.entries(this._scheduleEnabled).map(([e,t])=>ne` <button
                        class="channel-chip ${t?"active":"inactive"}"
                        .disabled=${!this._isEditable||this._isLoading}
                        @click=${()=>this._handleScheduleEnabledToggle(e)}
                        title="${this._availableTargetChannels?.[e]?.name??e}: ${t?this._translations.ui.weeklyProgramEnabled:this._translations.ui.weeklyProgramDisabled}"
                      >
                        ${this._availableTargetChannels?.[e]?.name??e}
                      </button>`)}
                </div>
              </div>`:""}
          ${this._scheduleData?ne`
                <hmip-device-schedule-list
                  .scheduleData=${this._scheduleData}
                  .domain=${this._domain}
                  .editable=${this._isEditable}
                  .collapseAfter=${5}
                  .translations=${this._buildListTranslations()}
                  @add-event=${this._onAddEvent}
                  @edit-event=${this._onEditEvent}
                  @delete-event=${this._onDeleteEvent}
                ></hmip-device-schedule-list>
              `:ne`<div class="loading">${this._translations.ui.loading}</div>`}
          ${this._isEditable?ne`<div class="hint">${this._translations.ui.clickToEdit}</div>`:""}
        </div>
        ${this._isLoading?ne`
              <div class="loading-overlay">
                <ha-circular-progress indeterminate></ha-circular-progress>
              </div>
            `:""}
      </ha-card>
      <hmip-device-schedule-editor
        .open=${this._showEditor}
        .entry=${this._editingEntry}
        .groupNo=${this._editingGroupNo}
        .isNewEvent=${this._isNewEvent}
        .domain=${this._domain}
        .availableTargetChannels=${this._availableTargetChannels}
        .translations=${this._buildEditorTranslations()}
        @save-event=${this._onSaveEvent}
        @editor-closed=${this._onEditorClosed}
      ></hmip-device-schedule-editor>
    `:ne`
        <ha-card>
          <div class="card-header">
            <div class="header-left">
              <div class="card-title">${t}</div>
            </div>
          </div>
          ${this._renderHeaderControls()}
          <div class="card-content">
            <div class="error">
              ${Dt(this._translations.errors.incompatibleEntity,{entity:this._activeEntityId})}
            </div>
          </div>
        </ha-card>
      `:ne`
        <ha-card>
          <div class="card-header">
            <div class="header-left">
              <div class="card-title">${t}</div>
            </div>
          </div>
          <div class="card-content">
            <div class="error">
              ${Dt(this._translations.ui.entityNotFound,{entity:this._activeEntityId||this._translations.ui.schedule})}
            </div>
          </div>
        </ha-card>
      `}static get styles(){return $`
      :host {
        display: block;
      }

      ha-card {
        padding: 16px;
        position: relative;
      }

      .card-header {
        display: block;
        margin-bottom: 8px;
      }

      .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .card-title {
        font-size: 16px;
        font-weight: 500;
        color: var(--primary-text-color);
        line-height: 1.3;
      }

      .header-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-bottom: 16px;
      }

      .entity-selector-dropdown {
        flex: 1;
        max-width: 300px;
      }

      ha-icon-button[disabled] {
        opacity: 0.5;
      }

      .schedule-enabled-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
      }

      .schedule-enabled-title {
        font-size: 13px;
        font-weight: 500;
        color: var(--secondary-text-color);
        white-space: nowrap;
      }

      .channel-chips {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
      }

      .channel-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 28px;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        line-height: 1;
        border: none;
        cursor: pointer;
        transition:
          background-color 0.2s,
          opacity 0.2s;
      }

      .channel-chip.active {
        background-color: var(--primary-color);
        color: var(--text-primary-color);
      }

      .channel-chip.inactive {
        background-color: var(--divider-color);
        color: var(--disabled-text-color, var(--secondary-text-color));
        opacity: 0.6;
      }

      .channel-chip:hover:not([disabled]) {
        opacity: 0.8;
      }

      .channel-chip[disabled] {
        cursor: not-allowed;
        opacity: 0.4;
      }

      .card-content {
        position: relative;
      }

      .loading {
        padding: 20px;
        text-align: center;
        color: var(--secondary-text-color);
      }

      .hint {
        margin-top: 12px;
        text-align: center;
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .error {
        padding: 20px;
        text-align: center;
        color: var(--error-color, #e74c3c);
      }

      /* Loading Overlay */
      .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        border-radius: 4px;
      }

      ha-circular-progress {
        color: var(--primary-color);
      }

      /* Mobile Optimization */
      @media (max-width: 768px) {
        ha-card {
          padding: 12px;
        }

        .card-header {
          margin-bottom: 12px;
        }

        .header-left {
          justify-content: center;
        }

        .card-title {
          font-size: 14px;
        }

        .header-controls {
          flex-wrap: wrap;
          justify-content: center;
        }

        .entity-selector-dropdown {
          max-width: none;
          flex: 1 1 100%;
        }
      }
    `}getCardSize(){return 4}static getConfigElement(){return document.createElement("homematicip-local-schedule-card-editor")}static getStubConfig(){return{entity:"",editable:!0,hour_format:"24"}}};v([Ae({attribute:!1})],Ct.prototype,"hass",void 0),v([De()],Ct.prototype,"_config",void 0),v([De()],Ct.prototype,"_scheduleData",void 0),v([De()],Ct.prototype,"_activeEntityId",void 0),v([De()],Ct.prototype,"_domain",void 0),v([De()],Ct.prototype,"_isLoading",void 0),v([De()],Ct.prototype,"_translations",void 0),v([De()],Ct.prototype,"_editingEntry",void 0),v([De()],Ct.prototype,"_editingGroupNo",void 0),v([De()],Ct.prototype,"_showEditor",void 0),v([De()],Ct.prototype,"_isNewEvent",void 0),v([De()],Ct.prototype,"_availableTargetChannels",void 0),v([De()],Ct.prototype,"_maxEntries",void 0),v([De()],Ct.prototype,"_scheduleEnabled",void 0),v([De()],Ct.prototype,"_alertMessage",void 0),v([De()],Ct.prototype,"_alertType",void 0);const Mt="homematicip-local-schedule-card";customElements.get(Mt)?console.warn(`%c HOMEMATICIP LOCAL %c The standalone HACS card "${Mt}" is already loaded. This card is now included with the integration and the HACS version can be removed. Go to HACS → Frontend → remove the schedule card resource.`,"color: white; background: #e67e22; font-weight: 700;","color: #e67e22; background: white; font-weight: 700;"):customElements.define(Mt,Ct),window.customCards=window.customCards||[],window.customCards.some(e=>e.type===Mt)||window.customCards.push({type:Mt,name:"HomematicIP Local Scheduler Card",description:"A custom card for Homematic(IP) Local schedules (switch, valve, cover, light)"});const Pt=(e,t,i)=>{const s=new CustomEvent(t,{bubbles:!0,composed:!0,detail:i});e.dispatchEvent(s)};class Lt extends ke{constructor(){super(...arguments),this._expandedEntity=null,this._computeLabel=e=>({entities:"Entities",name:"Card Name (optional)",show_profile_selector:"Show profile selector",editable:"Allow editing",show_temperature:"Show temperature values",show_gradient:"Show color gradient",hour_format:"Time format"}[e.name]||e.name)}_getCompatibleEntityIds(){return this.hass?.states?Object.keys(this.hass.states).filter(e=>{if(!e.startsWith("climate."))return!1;const t=this.hass.states[e]?.attributes;return void 0!==t?.schedule_data}):[]}_buildEntitySchema(){return[{name:"entities",required:!0,selector:{entity:{multiple:!0,include_entities:this._getCompatibleEntityIds()}}}]}static{this.OPTIONS_SCHEMA=[{name:"name",selector:{text:{}}},{name:"show_profile_selector",selector:{boolean:{}},default:!0},{name:"editable",selector:{boolean:{}},default:!0},{name:"show_temperature",selector:{boolean:{}},default:!0},{name:"show_gradient",selector:{boolean:{}},default:!1},{name:"hour_format",selector:{select:{options:[{value:"24",label:"24h"},{value:"12",label:"12h (AM/PM)"}]}},default:"24"}]}setConfig(e){this._config=e}_getEntityId(e){return"string"==typeof e?e:e.entity}_getEntityName(e){return"string"==typeof e?"":e.name||""}_getEntityProfileNames(e){return"string"==typeof e?{}:e.profile_names||{}}_getEntityIds(){return this._config?.entities?this._config.entities.map(e=>this._getEntityId(e)):[]}_getAvailableProfiles(e){const t=this.hass?.states?.[e];return t?.attributes?.available_profiles?[...t.attributes.available_profiles].sort():[]}render(){if(!this.hass||!this._config)return le;const e={entities:this._getEntityIds()};return ne`
      <ha-form
        .hass=${this.hass}
        .data=${e}
        .schema=${this._buildEntitySchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._entitiesChanged}
      ></ha-form>

      ${this._renderEntityConfig()}

      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${Lt.OPTIONS_SCHEMA}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._optionsChanged}
      ></ha-form>
    `}_renderEntityConfig(){const e=this._config?.entities||[];return 0===e.length?ne``:ne`
      <div class="entity-config">
        <div class="section-header">Entity Configuration</div>
        ${e.map((e,t)=>{const i=this._getEntityId(e),s=this._getEntityName(e),a=this._getEntityProfileNames(e),o=this.hass?.states?.[i]?.attributes.friendly_name||i,n=this._getAvailableProfiles(i),r=this._expandedEntity===i;return ne`
            <div class="entity-section">
              <div class="entity-header" @click=${()=>this._toggleEntity(i)}>
                <ha-icon
                  class="expand-icon"
                  .icon=${r?"mdi:chevron-down":"mdi:chevron-right"}
                ></ha-icon>
                <span class="entity-title" title=${i}>${o}</span>
              </div>

              ${r?ne`
                    <div class="entity-details">
                      <div class="config-row">
                        <label>Display Name</label>
                        <input
                          type="text"
                          .value=${s}
                          placeholder=${o}
                          @input=${e=>this._entityNameChanged(t,e)}
                        />
                      </div>

                      ${n.length>0?ne`
                            <div class="profile-names-section">
                              <div class="profile-names-header">Profile Names</div>
                              ${n.map(e=>ne`
                                  <div class="config-row profile-row">
                                    <label>${e}</label>
                                    <input
                                      type="text"
                                      .value=${a[e]||""}
                                      placeholder=${e}
                                      @input=${i=>this._profileNameChanged(t,e,i)}
                                    />
                                  </div>
                                `)}
                            </div>
                          `:ne`
                            <div class="no-profiles">No profiles available for this entity</div>
                          `}
                    </div>
                  `:""}
            </div>
          `})}
      </div>
    `}_toggleEntity(e){this._expandedEntity=this._expandedEntity===e?null:e}_entitiesChanged(e){e.stopPropagation();const t=(e.detail.value?.entities||[]).map(e=>{const t=this._config?.entities?.find(t=>this._getEntityId(t)===e);return t&&"string"!=typeof t&&(t.name||Object.keys(t.profile_names||{}).length>0)?{...t,entity:e}:e}),i={...this._config,entities:t};Pt(this,"config-changed",{config:i})}_getOrCreateEntityConfig(e,t){const i=e[t];return"string"==typeof i?{entity:i}:{...i}}_simplifyEntityConfig(e){const t=!!e.name,i=Object.keys(e.profile_names||{}).length>0;return t||i?e:e.entity}_entityNameChanged(e,t){const i=t.target.value.trim(),s=[...this._config?.entities||[]];if(e>=s.length)return;const a=this._getOrCreateEntityConfig(s,e);i?a.name=i:delete a.name,s[e]=this._simplifyEntityConfig(a);const o={...this._config,entities:s};Pt(this,"config-changed",{config:o})}_profileNameChanged(e,t,i){const s=i.target.value.trim(),a=[...this._config?.entities||[]];if(e>=a.length)return;const o=this._getOrCreateEntityConfig(a,e);o.profile_names||(o.profile_names={}),s?o.profile_names[t]=s:delete o.profile_names[t],0===Object.keys(o.profile_names).length&&delete o.profile_names,a[e]=this._simplifyEntityConfig(o);const n={...this._config,entities:a};Pt(this,"config-changed",{config:n})}_optionsChanged(e){e.stopPropagation();const t=e.detail.value,i={...this._config,...t,entities:this._config.entities};Pt(this,"config-changed",{config:i})}static{this.styles=$`
    ha-form {
      display: block;
    }

    .entity-config {
      margin: 16px 0;
      padding: 12px;
      background: var(--card-background-color, #fff);
      border: 1px solid var(--divider-color, #e0e0e0);
      border-radius: 8px;
    }

    .section-header {
      font-weight: 500;
      margin-bottom: 12px;
      color: var(--primary-text-color);
    }

    .entity-section {
      border: 1px solid var(--divider-color, #e0e0e0);
      border-radius: 6px;
      margin-bottom: 8px;
      overflow: hidden;
    }

    .entity-section:last-child {
      margin-bottom: 0;
    }

    .entity-header {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 12px;
      cursor: pointer;
      background: var(--secondary-background-color, #f5f5f5);
      user-select: none;
    }

    .entity-header:hover {
      background: var(--primary-color-light, #e3f2fd);
    }

    .expand-icon {
      --ha-icon-display-size: 18px;
      color: var(--secondary-text-color);
      flex-shrink: 0;
    }

    .entity-title {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 14px;
      color: var(--primary-text-color);
    }

    .entity-details {
      padding: 12px;
      border-top: 1px solid var(--divider-color, #e0e0e0);
    }

    .config-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }

    .config-row:last-child {
      margin-bottom: 0;
    }

    .config-row label {
      min-width: 100px;
      color: var(--secondary-text-color);
      font-size: 14px;
    }

    .config-row input {
      flex: 1;
      min-width: 0;
      padding: 8px 12px;
      border: 1px solid var(--divider-color, #e0e0e0);
      border-radius: 4px;
      font-size: 14px;
      background: var(--input-fill-color, var(--secondary-background-color));
      color: var(--primary-text-color);
    }

    .config-row input:focus {
      outline: none;
      border-color: var(--primary-color);
    }

    .config-row input::placeholder {
      color: var(--secondary-text-color);
      opacity: 0.7;
    }

    .profile-names-section {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--divider-color, #e0e0e0);
    }

    .profile-names-header {
      font-size: 13px;
      font-weight: 500;
      color: var(--secondary-text-color);
      margin-bottom: 8px;
    }

    .profile-row label {
      min-width: 60px;
      font-family: monospace;
    }

    .no-profiles {
      font-size: 13px;
      color: var(--secondary-text-color);
      font-style: italic;
      margin-top: 8px;
    }
  `}}v([Ae({attribute:!1})],Lt.prototype,"hass",void 0),v([De()],Lt.prototype,"_config",void 0),v([De()],Lt.prototype,"_expandedEntity",void 0),customElements.get("homematicip-local-climate-schedule-card-editor")||customElements.define("homematicip-local-climate-schedule-card-editor",Lt);const It={en:{weekdays:{short:{monday:"Mo",tuesday:"Tu",wednesday:"We",thursday:"Th",friday:"Fr",saturday:"Sa",sunday:"Su"},long:{monday:"Monday",tuesday:"Tuesday",wednesday:"Wednesday",thursday:"Thursday",friday:"Friday",saturday:"Saturday",sunday:"Sunday"}},ui:{schedule:"Schedule",loading:"Loading schedule data...",entityNotFound:"Entity {entity} not found",clickToEdit:"Click on a time slot to edit the schedule",edit:"Edit {weekday}",cancel:"Cancel",save:"Save",addTimeBlock:"+ Add Time Block",copySchedule:"Copy schedule",pasteSchedule:"Paste schedule",undo:"Undo",redo:"Redo",undoShortcut:"Undo (Ctrl+Z)",redoShortcut:"Redo (Ctrl+Y)",exportSchedule:"Export",importSchedule:"Import",exportTooltip:"Export schedule to JSON file",importTooltip:"Import schedule from JSON file",exportSuccess:"Schedule exported successfully",importSuccess:"Schedule imported successfully",unsavedChanges:"Unsaved changes",saveAll:"Save all",discard:"Discard",confirmDiscardChanges:"You have unsaved changes. Do you want to discard them?",close:"Close",from:"From",to:"To",baseTemperature:"Base Temperature",baseTemperatureDescription:"Temperature for unscheduled periods",temperaturePeriods:"Temperature Periods",editSlot:"Edit",saveSlot:"Save",cancelSlotEdit:"Cancel",removeSlot:"Remove",sensorNotSupported:"Sensor entity {entity} does not have a climate schedule type.",noScheduleData:"Entity {entity} does not provide schedule data."},errors:{failedToChangeProfile:"Failed to change profile: {error}",failedToSaveSchedule:"Failed to save schedule: {error}",failedToPasteSchedule:"Failed to paste schedule: {error}",invalidSchedule:"Invalid schedule: {error}",failedToExport:"Failed to export schedule: {error}",failedToImport:"Failed to import schedule: {error}",invalidImportFile:"Invalid file format. Please select a JSON file.",invalidImportFormat:"Invalid JSON format in file.",invalidImportData:"Invalid schedule data: {error}",insufficientPermissions:"You don't have permission to perform this action."},warnings:{title:"Validation Warnings",noWarnings:"No issues detected"},validationMessages:{blockEndBeforeStart:"Block {block}: End time is before start time",blockZeroDuration:"Block {block}: Block has zero duration",invalidStartTime:"Block {block}: Invalid start time",invalidEndTime:"Block {block}: Invalid end time",temperatureOutOfRange:"Block {block}: Temperature out of range ({min}-{max}°C)",invalidSlotCount:"Invalid number of slots: {count} (expected 13)",invalidSlotKey:"Invalid slot key: {key} (must be integer 1-13)",missingSlot:"Missing slot {slot}",slotMissingValues:"Slot {slot} missing ENDTIME or TEMPERATURE",slotTimeBackwards:"Slot {slot} time goes backwards: {time}",slotTimeExceedsDay:"Slot {slot} time exceeds 24:00: {time}",lastSlotMustEnd:"Last slot must end at 24:00",scheduleMustBeObject:"Schedule data must be an object",missingWeekday:"Missing weekday: {weekday}",invalidWeekdayData:"Invalid data for {weekday}",weekdayValidationError:"{weekday}: {details}"}},de:{weekdays:{short:{monday:"Mo",tuesday:"Di",wednesday:"Mi",thursday:"Do",friday:"Fr",saturday:"Sa",sunday:"So"},long:{monday:"Montag",tuesday:"Dienstag",wednesday:"Mittwoch",thursday:"Donnerstag",friday:"Freitag",saturday:"Samstag",sunday:"Sonntag"}},ui:{schedule:"Zeitplan",loading:"Zeitplandaten werden geladen...",entityNotFound:"Entität {entity} nicht gefunden",clickToEdit:"Klicken Sie auf einen Zeitabschnitt, um den Zeitplan zu bearbeiten",edit:"{weekday} bearbeiten",cancel:"Abbrechen",save:"Speichern",addTimeBlock:"+ Zeitblock hinzufügen",copySchedule:"Zeitplan kopieren",pasteSchedule:"Zeitplan einfügen",undo:"Rückgängig",redo:"Wiederholen",undoShortcut:"Rückgängig (Strg+Z)",redoShortcut:"Wiederholen (Strg+Y)",exportSchedule:"Exportieren",importSchedule:"Importieren",exportTooltip:"Zeitplan als JSON-Datei exportieren",importTooltip:"Zeitplan aus JSON-Datei importieren",exportSuccess:"Zeitplan erfolgreich exportiert",importSuccess:"Zeitplan erfolgreich importiert",unsavedChanges:"Ungespeicherte Änderungen",saveAll:"Alle speichern",discard:"Verwerfen",confirmDiscardChanges:"Sie haben ungespeicherte Änderungen. Möchten Sie diese verwerfen?",close:"Schließen",from:"Von",to:"Bis",baseTemperature:"Basistemperatur",baseTemperatureDescription:"Temperatur für nicht geplante Zeiträume",temperaturePeriods:"Temperaturperioden",editSlot:"Bearbeiten",saveSlot:"Speichern",cancelSlotEdit:"Abbrechen",removeSlot:"Entfernen",sensorNotSupported:"Sensor-Entität {entity} hat keinen Klima-Zeitplantyp.",noScheduleData:"Entität {entity} stellt keine Zeitplandaten bereit."},errors:{failedToChangeProfile:"Fehler beim Wechseln des Profils: {error}",failedToSaveSchedule:"Fehler beim Speichern des Zeitplans: {error}",failedToPasteSchedule:"Fehler beim Einfügen des Zeitplans: {error}",invalidSchedule:"Ungültiger Zeitplan: {error}",failedToExport:"Fehler beim Exportieren des Zeitplans: {error}",failedToImport:"Fehler beim Importieren des Zeitplans: {error}",invalidImportFile:"Ungültiges Dateiformat. Bitte wählen Sie eine JSON-Datei.",invalidImportFormat:"Ungültiges JSON-Format in der Datei.",invalidImportData:"Ungültige Zeitplandaten: {error}",insufficientPermissions:"Sie haben keine Berechtigung für diese Aktion."},warnings:{title:"Validierungswarnungen",noWarnings:"Keine Probleme erkannt"},validationMessages:{blockEndBeforeStart:"Block {block}: Die Endzeit liegt vor der Startzeit",blockZeroDuration:"Block {block}: Der Block hat keine Dauer",invalidStartTime:"Block {block}: Ungültige Startzeit",invalidEndTime:"Block {block}: Ungültige Endzeit",temperatureOutOfRange:"Block {block}: Temperatur außerhalb des Bereichs ({min}-{max}°C)",invalidSlotCount:"Ungültige Anzahl an Slots: {count} (erwartet 13)",invalidSlotKey:"Ungültiger Slot-Schlüssel: {key} (muss eine Ganzzahl 1-13 sein)",missingSlot:"Slot {slot} fehlt",slotMissingValues:"Slot {slot} fehlt ENDTIME oder TEMPERATURE",slotTimeBackwards:"Slot {slot}: Zeit läuft rückwärts: {time}",slotTimeExceedsDay:"Slot {slot}: Zeit überschreitet 24:00: {time}",lastSlotMustEnd:"Der letzte Slot muss um 24:00 enden",scheduleMustBeObject:"Zeitplandaten müssen ein Objekt sein",missingWeekday:"Fehlender Wochentag: {weekday}",invalidWeekdayData:"Ungültige Daten für {weekday}",weekdayValidationError:"{weekday}: {details}"}}};function Ot(e){const t=e.toLowerCase().split("-")[0];return It[t]||It.en}function Nt(e,t){let i=e;for(const[e,s]of Object.entries(t))i=i.replace(`{${e}}`,s);return i}class Ht extends ke{constructor(){super(...arguments),this._availableProfiles=[],this._userSelectedProfile=!1,this._isLoading=!1,this._translations=Ot("en"),this._minTemp=5,this._maxTemp=30.5,this._tempStep=.5,this._alertType="error"}static getConfigElement(){return document.createElement("homematicip-local-climate-schedule-card-editor")}static getStubConfig(e){const t=Object.keys(e.states).filter(t=>t.startsWith("climate.")&&void 0!==e.states[t].attributes?.schedule_data);return{type:"custom:homematicip-local-climate-schedule-card",entities:t.length>0?[t[0]]:[]}}_showAlert(e,t="error"){this._alertMessage=e,this._alertType=t}_dismissAlert(){this._alertMessage=void 0}get _isEditable(){return this._config?.editable??!0}setConfig(e){const t=[],i=e=>{if(!e)return;const i=e.trim();i&&(t.includes(i)||t.push(i))};if(i(e.entity),Array.isArray(e.entities)&&e.entities.forEach(e=>{const t="string"==typeof e?e:e.entity;i(t)}),0===t.length)return this._config={show_profile_selector:!0,editable:!0,show_temperature:!0,show_gradient:!1,hour_format:"24",...e,entities:[]},this._activeEntityId=void 0,void(this._scheduleData=void 0);t.sort((e,t)=>e.localeCompare(t));const s=this._activeEntityId,a=t[0],o=s&&t.includes(s)?s:a;this._config={show_profile_selector:!0,editable:!0,show_temperature:!0,temperature_unit:"°C",hour_format:"24",...e,entity:a},this._activeEntityId=o,this._copiedSchedule=void 0,this._editingWeekday=void 0,this._updateLanguage()}_getPreferredLanguage(e){return e?.language||e?.locale?.language}_updateLanguage(){let e="en";if(this._config?.language)e=this._config.language;else{const t=this._getPreferredLanguage(this.hass);t&&(e=t)}this._translations=Ot(e),this._weekdayShortLabelMap=this._createWeekdayLabelMap("short"),this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")}_createWeekdayLabelMap(e){const t="short"===e?this._translations.weekdays.short:this._translations.weekdays.long;return{MONDAY:t.monday,TUESDAY:t.tuesday,WEDNESDAY:t.wednesday,THURSDAY:t.thursday,FRIDAY:t.friday,SATURDAY:t.saturday,SUNDAY:t.sunday}}_getWeekdayLabel(e,t="short"){return"long"===t?(this._weekdayLongLabelMap||(this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")),this._weekdayLongLabelMap[e]):(this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),this._weekdayShortLabelMap[e])}_getEntityId(e){return"string"==typeof e?e:e.entity}_getEntityOptions(){return this._config?this._config.entities?.length?this._config.entities.map(e=>this._getEntityId(e)).sort((e,t)=>e.localeCompare(t)):this._config.entity?[this._config.entity]:[]:[]}_getEntityDisplayName(e){if(this._config?.entities?.length){const t=this._config.entities.find(t=>this._getEntityId(t)===e);if(t&&"string"!=typeof t&&t.name)return t.name}return this.hass?.states?.[e]?.attributes.friendly_name||e}_getProfileDisplayName(e){const t=this._getActiveEntityId();if(t&&this._config?.entities?.length){const i=this._config.entities.find(e=>this._getEntityId(e)===t);if(i&&"string"!=typeof i&&i.profile_names?.[e])return`${e} - ${i.profile_names[e]}`}return e}_getActiveEntityId(){const e=this._getEntityOptions();if(0!==e.length)return this._activeEntityId&&e.includes(this._activeEntityId)?this._activeEntityId:e[0]}_needsManualReload(e){if(!e||!this.hass)return!1;const t=this.hass.states[e];if(!t?.attributes?.interface_id)return!1;const i=t.attributes.interface_id;return i.endsWith("BidCos-RF")||i.endsWith("BidCos-Wired")||i.endsWith("VirtualDevices")}_getDeviceAddress(e){const t=this.hass?.states[e];return ze(t?.attributes?.address)}_requireDeviceAddress(e){const t=this._getDeviceAddress(e);if(!t)throw new Error(`Cannot resolve device_address for entity ${e}. Ensure the entity has a valid address attribute (format: "device_address:channel").`);return t}_requireConfigEntryId(e){const t=this.hass?.states[e],i=t?.attributes?.config_entry_id;if(!i)throw new Error(`Cannot resolve config_entry_id for entity ${e}. Ensure the entity has a valid config_entry_id attribute.`);return i}async _callSetActiveProfile(e,t){const i=this._requireConfigEntryId(e),a=this._requireDeviceAddress(e);await s(this.hass,i,a,t)}async _callSetScheduleWeekday(e,t,i,s,o){const n=this._requireConfigEntryId(e),r=this._requireDeviceAddress(e);await a(this.hass,n,r,t,i,s,o)}_scheduleReloadDeviceConfig(e){if(!this.hass)return;const t=this._getDeviceAddress(e);if(!t)return;const s=this.hass.states[e],a=s?.attributes?.config_entry_id;a&&setTimeout(async()=>{try{await i(this.hass,a,t)}catch{}},5e3)}_formatValidationParams(e){if(!e)return{};const t={};for(const[i,s]of Object.entries(e))"weekday"===i&&Ce.includes(s)?t.weekday=this._getWeekdayLabel(s,"long"):t[i]=s;return t}_translateValidationMessage(e){const t=this._translations.validationMessages[e.key]||e.key,i=this._formatValidationParams(e.params);return e.nested&&(i.details=this._translateValidationMessage(e.nested)),Nt(t,i)}getCardSize(){return 12}willUpdate(e){if(super.willUpdate(e),e.has("hass")&&this._config){this._updateFromEntity();const t=e.get("hass");this._getPreferredLanguage(this.hass)!==this._getPreferredLanguage(t)&&this._updateLanguage()}}connectedCallback(){super.connectedCallback()}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0)}_updateFromEntity(){if(!this.hass||!this._config)return;const e=this._getActiveEntityId();if(!e)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const t=this.hass.states?.[e];if(!t)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const i=t.attributes;if(e.startsWith("sensor.")&&"climate"!==i.schedule_type)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);if(!i.schedule_data)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const s=function(e){if(null!=e)return`P${e}`}(i.device_active_profile_index);void 0!==s&&void 0!==this._activeDeviceProfile&&s!==this._activeDeviceProfile&&(this._userSelectedProfile=!1,this._reloadScheduleData(e,s)),this._activeDeviceProfile=s;const a=i.current_schedule_profile||i.active_profile;this._userSelectedProfile||(this._currentProfile=this._config.profile||s||a),this._scheduleData=i.schedule_data,this._availableProfiles=(i.available_profiles||[]).slice().sort((e,t)=>e.localeCompare(t)),this._minTemp=i.min_temp??5,this._maxTemp=i.max_temp??30.5,this._tempStep=i.target_temp_step??.5,this._lastScheduleDataHash=i.schedule_data?JSON.stringify(i.schedule_data):void 0}_reloadScheduleData(e,t){this.hass&&this._callSetActiveProfile(e,t).catch(()=>{})}async _handleProfileChange(e){e.stopPropagation();const t=e.detail.value,i=this._getActiveEntityId();if(this._config&&this.hass&&i){if(this._editingWeekday){if(!confirm(this._translations.ui.confirmDiscardChanges))return;this._editingWeekday=void 0}this._userSelectedProfile=!0;try{await this._callSetActiveProfile(i,t),this._currentProfile=t}catch(e){console.error("Failed to load profile data:",e);const t=String(e);t.includes("unauthorized")||t.includes("Unauthorized")?this._showAlert(this._translations.errors.insufficientPermissions):this._showAlert(Nt(this._translations.errors.failedToChangeProfile,{error:t}))}}}_onWeekdayClick(e){this._isEditable&&this._scheduleData&&(this._editingWeekday=e.detail.weekday)}_onCopySchedule(e){const t=e.detail.weekday;if(!this._scheduleData)return;const i=this._getParsedBlocks(t);let s;const a=this._scheduleData[t];s=a?Be(a).baseTemperature:We(i),this._copiedSchedule={weekday:t,blocks:JSON.parse(JSON.stringify(i)),baseTemperature:s},console.info(`Copied schedule from ${t}`)}async _onPasteSchedule(e){if(!this._isEditable)return;const t=e.detail.weekday;if(!(this._config&&this.hass&&this._currentProfile&&this._copiedSchedule))return;const i=this._getActiveEntityId();if(!i)return;const s=this._copiedSchedule.baseTemperature??We(this._copiedSchedule.blocks),a=Ue(this._copiedSchedule.blocks,s),o=et(a,this._minTemp,this._maxTemp);if(o){const e=this._translateValidationMessage(o);return void this._showAlert(Nt(this._translations.errors.invalidSchedule,{error:e}))}this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const{base_temperature:e,periods:s}=a;await this._callSetScheduleWeekday(i,this._currentProfile,t,e,s),this._scheduleData&&(this._scheduleData={...this._scheduleData,[t]:a}),this._updateFromEntity(),this.requestUpdate(),console.info(`Pasted schedule to ${t}`),this._needsManualReload(i)&&this._scheduleReloadDeviceConfig(i)}catch(e){console.error("Failed to paste schedule:",e);const t=String(e);t.includes("unauthorized")||t.includes("Unauthorized")?this._showAlert(this._translations.errors.insufficientPermissions):this._showAlert(Nt(this._translations.errors.failedToPasteSchedule,{error:t}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}async _onSaveSchedule(e){if(!this._config||!this.hass||!this._currentProfile)return;const t=this._getActiveEntityId();if(!t)return;const{weekday:i,blocks:s,baseTemperature:a}=e.detail,o=Ue(s,a),n=et(o,this._minTemp,this._maxTemp);if(n){const e=this._translateValidationMessage(n);return void this._showAlert(Nt(this._translations.errors.invalidSchedule,{error:e}))}this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const{base_temperature:e,periods:s}=o;await this._callSetScheduleWeekday(t,this._currentProfile,i,e,s),this._scheduleData&&(this._scheduleData={...this._scheduleData,[i]:o}),this._updateFromEntity(),this.requestUpdate(),this._editingWeekday=void 0,this._needsManualReload(t)&&this._scheduleReloadDeviceConfig(t)}catch(e){console.error("Failed to save schedule:",e);const t=String(e);t.includes("unauthorized")||t.includes("Unauthorized")?this._showAlert(this._translations.errors.insufficientPermissions):this._showAlert(Nt(this._translations.errors.failedToSaveSchedule,{error:t}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}_onValidationFailed(e){this._showAlert(Nt(this._translations.errors.invalidSchedule,{error:e.detail.error}))}_onEditorClosed(){this._editingWeekday=void 0}_getParsedBlocks(e){if(this._scheduleData){const t=this._scheduleData[e];if(!t)return[];const{blocks:i}=Be(t);return i}return[]}_exportSchedule(){if(this._currentProfile&&this._scheduleData)try{const e={version:"2.0",profile:this._currentProfile,exported:(new Date).toISOString(),scheduleData:this._scheduleData,format:"simple"},t=JSON.stringify(e,null,2),i=new Blob([t],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s,a.download=`schedule-${this._currentProfile}-${(new Date).toISOString().split("T")[0]}.json`,document.body.appendChild(a),a.click(),document.body.removeChild(a),URL.revokeObjectURL(s),console.info("Schedule exported successfully")}catch(e){console.error("Failed to export schedule:",e),this._showAlert(Nt(this._translations.errors.failedToExport,{error:String(e)}))}}_importSchedule(){if(!this._isEditable)return;const e=document.createElement("input");e.type="file",e.accept=".json,application/json",e.onchange=async e=>{const t=e.target.files?.[0];if(t)if(t.name.endsWith(".json")||"application/json"===t.type)try{const e=await t.text();let i,s;try{i=JSON.parse(e)}catch{return void this._showAlert(this._translations.errors.invalidImportFormat)}if(!i||"object"!=typeof i)return void this._showAlert(this._translations.errors.invalidImportFormat);s="scheduleData"in i?i.scheduleData:i;const a=function(e){if(!e||"object"!=typeof e)return{key:"scheduleMustBeObject"};const t=e,i=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"];for(const e of i){if(!(e in t))return{key:"missingWeekday",params:{weekday:e}};const i=t[e];if(!i||"object"!=typeof i)return{key:"invalidWeekdayData",params:{weekday:e}};if(!("base_temperature"in i)||!("periods"in i))return{key:"invalidWeekdayData",params:{weekday:e}};const s=et(i);if(s)return{key:"weekdayValidationError",params:{weekday:e},nested:s}}return null}(s);if(a){const e=this._translateValidationMessage(a);return void this._showAlert(Nt(this._translations.errors.invalidImportData,{error:e}))}const o=this._getActiveEntityId();if(!(this._config&&this.hass&&this._currentProfile&&o))return;this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const e=s;for(const t of Ce){const i=e[t];if(i){const{base_temperature:e,periods:s}=i;await this._callSetScheduleWeekday(o,this._currentProfile,t,e,s)}}this._scheduleData=e,this._updateFromEntity(),this.requestUpdate(),console.info("Schedule imported successfully"),this._showAlert(this._translations.ui.importSuccess,"success"),this._needsManualReload(o)&&this._scheduleReloadDeviceConfig(o)}catch(e){console.error("Failed to import schedule:",e),this._showAlert(Nt(this._translations.errors.failedToImport,{error:String(e)}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}catch(e){console.error("Failed to read import file:",e),this._showAlert(Nt(this._translations.errors.failedToImport,{error:String(e)}))}else this._showAlert(this._translations.errors.invalidImportFile)},e.click()}_buildGridTranslations(){return this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),this._weekdayLongLabelMap||(this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")),{weekdayShortLabels:this._weekdayShortLabelMap,weekdayLongLabels:this._weekdayLongLabelMap,clickToEdit:this._translations.ui.clickToEdit,copySchedule:this._translations.ui.copySchedule,pasteSchedule:this._translations.ui.pasteSchedule}}_buildEditorTranslations(){return this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),this._weekdayLongLabelMap||(this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")),{weekdayShortLabels:this._weekdayShortLabelMap,weekdayLongLabels:this._weekdayLongLabelMap,edit:this._translations.ui.edit,cancel:this._translations.ui.cancel,save:this._translations.ui.save,addTimeBlock:this._translations.ui.addTimeBlock,from:this._translations.ui.from,to:this._translations.ui.to,baseTemperature:this._translations.ui.baseTemperature,baseTemperatureDescription:this._translations.ui.baseTemperatureDescription,temperaturePeriods:this._translations.ui.temperaturePeriods,editSlot:this._translations.ui.editSlot,saveSlot:this._translations.ui.saveSlot,cancelSlotEdit:this._translations.ui.cancelSlotEdit,removeSlot:this._translations.ui.removeSlot,close:this._translations.ui.close,undoShortcut:this._translations.ui.undoShortcut,redoShortcut:this._translations.ui.redoShortcut,warningsTitle:this._translations.warnings.title,validationMessages:this._translations.validationMessages}}_renderEntitySelector(e,t){const i=t&&e.includes(t)?t:e[0];return ne`
      <ha-select
        class="entity-selector"
        .value=${i}
        .options=${[...e].sort((e,t)=>e.localeCompare(t)).map(e=>({value:e,label:this._getEntityDisplayName(e)}))}
        @selected=${this._handleEntitySelection}
        @closed=${e=>e.stopPropagation()}
      ></ha-select>
    `}_handleEntitySelection(e){e.stopPropagation();const t=e.detail.value;t&&t!==this._getActiveEntityId()&&(this._activeEntityId=t,this._editingWeekday=void 0,this._copiedSchedule=void 0,this._userSelectedProfile=!1,this._updateFromEntity())}render(){if(!this._config||!this.hass)return ne``;const e=this._getEntityOptions(),t=e.length>1,i=this._getActiveEntityId(),s=i?this.hass.states?.[i]:void 0,a=this._config.name||(i?this._getEntityDisplayName(i):null)||this._translations.ui.schedule;return s?i?.startsWith("sensor.")&&"climate"!==s.attributes.schedule_type?ne`
          <ha-card>
            <div class="card-header">
              <div class="name">${a}</div>
            </div>
            <div class="card-content">
              <div class="error">
                ${Nt(this._translations.ui.sensorNotSupported,{entity:i})}
              </div>
            </div>
          </ha-card>
        `:s.attributes.schedule_data?ne`
      <ha-card>
        <div class="card-header">
          <div class="name">${a}</div>
        </div>
        <div class="header-controls">
          ${t?this._renderEntitySelector(e,i):""}
          ${this._config.show_profile_selector&&this._availableProfiles.length>0?ne`
                <ha-select
                  class="profile-selector"
                  .value=${this._currentProfile||""}
                  .options=${this._availableProfiles.map(e=>({value:e,label:(e===this._activeDeviceProfile?"* ":"")+this._getProfileDisplayName(e)}))}
                  @selected=${this._handleProfileChange}
                  @closed=${e=>e.stopPropagation()}
                ></ha-select>
              `:""}
          <ha-icon-button
            .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
            @click=${this._exportSchedule}
            .label=${this._translations.ui.exportTooltip}
            .disabled=${!this._scheduleData}
          ></ha-icon-button>
          ${this._isEditable?ne`<ha-icon-button
                .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
                @click=${this._importSchedule}
                .label=${this._translations.ui.importTooltip}
              ></ha-icon-button>`:""}
        </div>

        <div class="card-content">
          ${this._alertMessage?ne`<ha-alert
                .alertType=${this._alertType}
                dismissable
                @alert-dismissed-clicked=${this._dismissAlert}
                >${this._alertMessage}</ha-alert
              >`:""}
          ${this._scheduleData?ne`
                <hmip-schedule-grid
                  .scheduleData=${this._scheduleData}
                  .editable=${this._isEditable}
                  .showTemperature=${this._config.show_temperature??!0}
                  .showGradient=${this._config.show_gradient??!1}
                  .temperatureUnit=${this._config.temperature_unit||"°C"}
                  .hourFormat=${this._config.hour_format||"24"}
                  .translations=${this._buildGridTranslations()}
                  .copiedWeekday=${this._copiedSchedule?.weekday}
                  .editorOpen=${!!this._editingWeekday}
                  .currentProfile=${this._currentProfile}
                  .scheduleDataHash=${this._lastScheduleDataHash}
                  @weekday-click=${this._onWeekdayClick}
                  @copy-schedule=${this._onCopySchedule}
                  @paste-schedule=${this._onPasteSchedule}
                ></hmip-schedule-grid>
              `:ne`<div class="loading">${this._translations.ui.loading}</div>`}
        </div>

        ${this._isLoading?ne`
              <div class="loading-overlay">
                <ha-circular-progress indeterminate></ha-circular-progress>
              </div>
            `:""}
      </ha-card>

      <hmip-schedule-editor
        .open=${!!this._editingWeekday}
        .weekday=${this._editingWeekday}
        .scheduleData=${this._scheduleData}
        .minTemp=${this._minTemp}
        .maxTemp=${this._maxTemp}
        .tempStep=${this._tempStep}
        .temperatureUnit=${this._config.temperature_unit||"°C"}
        .hourFormat=${this._config.hour_format||"24"}
        .translations=${this._buildEditorTranslations()}
        @save-schedule=${this._onSaveSchedule}
        @validation-failed=${this._onValidationFailed}
        @editor-closed=${this._onEditorClosed}
      ></hmip-schedule-editor>
    `:ne`
        <ha-card>
          <div class="card-header">
            <div class="name">${a}</div>
          </div>
          <div class="card-content">
            <div class="error">
              ${Nt(this._translations.ui.noScheduleData,{entity:i||""})}
            </div>
          </div>
        </ha-card>
      `:ne`
        <ha-card>
          <div class="card-header">
            <div class="name">${a}</div>
          </div>
          <div class="card-content">
            <div class="error">
              ${Nt(this._translations.ui.entityNotFound,{entity:i||this._translations.ui.schedule})}
            </div>
          </div>
        </ha-card>
      `}static get styles(){return $`
      :host {
        display: block;
      }

      ha-card {
        padding: 16px;
        overflow: hidden;
      }

      .card-header {
        display: block;
        margin-bottom: 8px;
      }

      .name {
        font-size: 24px;
        font-weight: 400;
        color: var(--primary-text-color);
        margin-bottom: 8px;
      }

      .header-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-bottom: 24px;
        flex-wrap: wrap;
        max-width: 100%;
      }

      .profile-selector {
        flex-shrink: 0;
        max-width: 200px;
      }

      .entity-selector {
        flex: 1 1 auto;
        min-width: 150px;
        max-width: 100%;
      }

      ha-icon-button[disabled] {
        opacity: 0.5;
      }

      .card-content {
        position: relative;
        overflow: hidden;
      }

      .loading,
      .error {
        padding: 20px;
        text-align: center;
        color: var(--secondary-text-color);
      }

      .error {
        color: var(--error-color);
      }

      /* Loading overlay */
      .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        border-radius: 4px;
      }

      ha-circular-progress {
        color: var(--primary-color);
      }

      /* Mobile Optimization */
      @media (max-width: 768px) {
        ha-card {
          padding: 12px;
        }

        .card-header {
          flex-direction: column;
          align-items: stretch;
          gap: 12px;
          margin-bottom: 12px;
        }

        .name {
          font-size: 20px;
          text-align: center;
        }

        .header-controls {
          justify-content: center;
          flex-wrap: wrap;
        }

        .profile-selector {
          max-width: 100%;
        }
      }

      /* Small mobile devices (portrait phones) */
      @media (max-width: 480px) {
        ha-card {
          padding: 8px;
        }

        .name {
          font-size: 18px;
        }
      }
    `}}v([Ae({attribute:!1})],Ht.prototype,"hass",void 0),v([De()],Ht.prototype,"_config",void 0),v([De()],Ht.prototype,"_currentProfile",void 0),v([De()],Ht.prototype,"_activeDeviceProfile",void 0),v([De()],Ht.prototype,"_scheduleData",void 0),v([De()],Ht.prototype,"_availableProfiles",void 0),v([De()],Ht.prototype,"_activeEntityId",void 0),v([De()],Ht.prototype,"_editingWeekday",void 0),v([De()],Ht.prototype,"_copiedSchedule",void 0),v([De()],Ht.prototype,"_isLoading",void 0),v([De()],Ht.prototype,"_translations",void 0),v([De()],Ht.prototype,"_minTemp",void 0),v([De()],Ht.prototype,"_maxTemp",void 0),v([De()],Ht.prototype,"_tempStep",void 0),v([De()],Ht.prototype,"_alertMessage",void 0),v([De()],Ht.prototype,"_alertType",void 0);const zt="homematicip-local-climate-schedule-card";customElements.get(zt)?console.warn(`%c HOMEMATICIP LOCAL %c The standalone HACS card "${zt}" is already loaded. This card is now included with the integration and the HACS version can be removed. Go to HACS → Frontend → remove the climate schedule card resource.`,"color: white; background: #e67e22; font-weight: 700;","color: #e67e22; background: white; font-weight: 700;"):customElements.define(zt,Ht),window.customCards=window.customCards||[],window.customCards.some(e=>e.type===zt)||window.customCards.push({type:zt,name:"Homematic(IP) Local Climate Schedule Card",description:"Display and edit Homematic thermostat schedules"});const Bt=$`
  :host {
    display: block;
    font-family: var(--paper-font-body1_-_font-family, "Roboto", sans-serif);
    color: var(--primary-text-color);
  }

  ha-card {
    overflow: hidden;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 16px 0;
    font-size: 16px;
    font-weight: 500;
  }

  .card-content {
    padding: 12px 16px 16px;
  }

  .badges {
    display: flex;
    gap: 6px;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
  }

  .badge.ok {
    background: var(--success-color, #4caf50);
    color: #fff;
  }

  .badge.warning {
    background: var(--warning-color, #ff9800);
    color: #fff;
  }

  .badge.error {
    background: var(--error-color, #db4437);
    color: #fff;
  }

  .badge.info {
    background: var(--info-color, var(--primary-color, #03a9f4));
    color: #fff;
  }

  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 12px;
    padding: 8px 0;
  }

  .stat-item {
    text-align: center;
    padding: 8px;
    border-radius: 8px;
    background: var(--card-background-color, var(--ha-card-background, #fff));
    border: 1px solid var(--divider-color, #e0e0e0);
  }

  .stat-value {
    font-size: 24px;
    font-weight: 600;
    line-height: 1.2;
  }

  .stat-label {
    font-size: 11px;
    color: var(--secondary-text-color);
    margin-top: 2px;
  }

  .stat-item.warning {
    border-color: var(--warning-color, #ff9800);
    background: color-mix(in srgb, var(--warning-color, #ff9800) 8%, transparent);
  }

  .stat-item.error {
    border-color: var(--error-color, #db4437);
    background: color-mix(in srgb, var(--error-color, #db4437) 8%, transparent);
  }

  .item-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .item-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px;
    border-radius: 8px;
    background: var(--card-background-color, var(--ha-card-background, #fff));
    border: 1px solid var(--divider-color, #e0e0e0);
  }

  .item-row.warning {
    border-color: var(--warning-color, #ff9800);
    background: color-mix(in srgb, var(--warning-color, #ff9800) 6%, transparent);
  }

  .item-row.error {
    border-color: var(--error-color, #db4437);
    background: color-mix(in srgb, var(--error-color, #db4437) 6%, transparent);
  }

  .item-row.ok .item-icon {
    color: var(--success-color, #4caf50);
  }

  .item-secondary .warning {
    color: var(--warning-color, #ff9800);
    font-weight: 500;
  }

  .item-secondary .error {
    color: var(--error-color, #db4437);
    font-weight: 500;
  }

  .item-icon {
    flex: 0 0 auto;
    color: var(--secondary-text-color);
  }

  .item-content {
    flex: 1;
    min-width: 0;
  }

  .item-primary {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .item-secondary {
    font-size: 12px;
    color: var(--secondary-text-color);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .item-action {
    flex: 0 0 auto;
  }

  .status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .status-dot.online {
    background: var(--success-color, #4caf50);
  }

  .status-dot.offline {
    background: var(--error-color, #db4437);
  }

  .section-title {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--secondary-text-color);
    padding: 8px 0 4px;
  }

  .empty-state {
    text-align: center;
    padding: 24px;
    color: var(--secondary-text-color);
    font-size: 14px;
  }

  .loading {
    display: flex;
    justify-content: center;
    padding: 24px;
  }

  .error-msg {
    color: var(--error-color, #db4437);
    padding: 16px;
    font-size: 14px;
  }

  .summary-line {
    font-size: 13px;
    color: var(--secondary-text-color);
    padding-top: 8px;
    text-align: center;
  }

  /* ---- Responsive: mobile (< 600px) ---- */
  @media (max-width: 600px) {
    .stat-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
`,Ut={en:{systemHealth:"System Health",centralState:"Status",healthScore:"Health",devices:"Devices",unreachable:"Unreachable",firmwareUpdates:"FW Updates",incidents:"Incidents",noIncidents:"No incidents",throttleActive:"Throttle active",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Device Status",problems:"Problems",allDevicesOk:"All devices OK",notReachable:"Not reachable",lowBattery:"Low battery",configPending:"Config pending",devicesOk:"{count} devices OK",noDevices:"No devices found",messages:"Messages",alarms:"Alarms",serviceMessages:"Service",acknowledge:"Acknowledge",noMessages:"No service messages",noAlarms:"No alarms",loading:"Loading...",error:"Error loading data",refresh:"Refresh"},de:{systemHealth:"Systemstatus",centralState:"Status",healthScore:"Zustand",devices:"Geräte",unreachable:"Nicht erreichbar",firmwareUpdates:"FW-Updates",incidents:"Vorfälle",noIncidents:"Keine Vorfälle",throttleActive:"Drosselung aktiv",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Gerätestatus",problems:"Probleme",allDevicesOk:"Alle Geräte OK",notReachable:"Nicht erreichbar",lowBattery:"Batterie niedrig",configPending:"Konfiguration ausstehend",devicesOk:"{count} Geräte OK",noDevices:"Keine Geräte gefunden",messages:"Meldungen",alarms:"Alarme",serviceMessages:"Service",acknowledge:"Quittieren",noMessages:"Keine Servicemeldungen",noAlarms:"Keine Alarme",loading:"Laden...",error:"Fehler beim Laden",refresh:"Aktualisieren"}};function Wt(e){return Ut[e]||Ut.en}class Rt extends ke{constructor(){super(...arguments),this._loading=!0,this._error=""}static{this.styles=Bt}setConfig(e){this._config={show_incidents:!1,max_incidents:5,show_throttle:!1,poll_interval:30,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=Wt(this.hass.config.language))}_startPolling(e){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),e)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(!this.hass||!this._config||!this._config.entry_id)return void(this._loading=!1);try{const e=this._config.show_incidents?this._config.max_incidents:0,[t,i,s]=await Promise.all([o(this.hass,this._config.entry_id),n(this.hass,this._config.entry_id),e>0?r(this.hass,this._config.entry_id,e):Promise.resolve(void 0)]);this._health=t,this._deviceStats=i,s&&(this._incidents=s),this._entryEntityIds||await this._loadEntryEntityIds(),this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}const e="running"===this._health?.central_state?.toLowerCase(),t=1e3*(this._config.poll_interval??30);this._startPolling(e?Math.max(t,3e4):5e3)}render(){if(!this._config||!this._t)return le;const e=this._config.title??this._t.systemHealth;return this._loading?ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&!this._health?ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:ne`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">${this._renderStatusBadge()}</div>
        </div>
        <div class="card-content">
          ${this._renderStats()} ${this._renderRadioLevels()} ${this._renderIncidents()}
        </div>
      </ha-card>
    `}_renderStatusBadge(){if(!this._health)return le;const e=this._health.central_state,t="running"===e?.toLowerCase(),i=Math.round(100*this._health.overall_health_score);return ne` <span class="badge ${t?"ok":"error"}">${i}%</span> `}_renderStats(){if(!this._deviceStats)return le;const e=this._deviceStats;return ne`
      <div class="stat-grid">
        <div class="stat-item">
          <div class="stat-value">${e.total_devices}</div>
          <div class="stat-label">${this._t.devices}</div>
        </div>
        <div class="stat-item ${e.unreachable_devices>0?"error":""}">
          <div class="stat-value">${e.unreachable_devices}</div>
          <div class="stat-label">${this._t.unreachable}</div>
        </div>
        <div class="stat-item ${e.firmware_updatable_devices>0?"warning":""}">
          <div class="stat-value">${e.firmware_updatable_devices}</div>
          <div class="stat-label">${this._t.firmwareUpdates}</div>
        </div>
      </div>
    `}async _loadEntryEntityIds(){this.hass&&this._config&&(this._entryEntityIds=await l(this.hass,this._config.entry_id))}_renderRadioLevels(){const e=d(this.hass?.states,this._entryEntityIds);return 0===e.length?le:ne`
      <div class="section-title">${this._t.dutyCycle} / ${this._t.carrierSense}</div>
      <div class="item-list">
        ${e.map(e=>ne`
            <div class="item-row">
              <ha-icon class="item-icon" .icon=${"mdi:radio-tower"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.name}</div>
                <div class="item-secondary">
                  ${null!==e.dutyCycle?ne`<span class="${c(e.dutyCycle)}">DC: ${e.dutyCycle}%</span>`:le}
                  ${null!==e.dutyCycle&&null!==e.carrierSense?" · ":le}
                  ${null!==e.carrierSense?ne`<span class="${h(e.carrierSense)}"
                        >CS: ${e.carrierSense}%</span
                      >`:le}
                </div>
              </div>
            </div>
          `)}
      </div>
    `}_renderIncidents(){if(!this._config?.show_incidents||!this._incidents)return le;const e=this._incidents.incidents,t=this._incidents.summary.total_incidents;return 0===t?ne`<div class="empty-state">${this._t.noIncidents}</div>`:ne`
      <div class="section-title">
        ${this._t.incidents}
        <span class="badge warning">${t}</span>
      </div>
      <div class="item-list">
        ${e.map(e=>ne`
            <div class="item-row ${this._incidentSeverity(e)}">
              <ha-icon class="item-icon" .icon=${this._incidentIcon(e)}></ha-icon>
              <div class="item-content">
                <div class="item-primary">
                  ${e.message||e.type}
                </div>
                <div class="item-secondary">
                  ${this._formatTimestamp(e.timestamp)}
                </div>
              </div>
            </div>
          `)}
      </div>
    `}_incidentSeverity(e){const t=String(e.severity||"info").toLowerCase();return"error"===t||"critical"===t?"error":"warning"===t?"warning":""}_incidentIcon(e){const t=String(e.severity||"info").toLowerCase();return"error"===t||"critical"===t?"mdi:alert-circle":"warning"===t?"mdi:alert":"mdi:information"}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return e}}static getConfigElement(){return document.createElement("homematicip-system-health-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}v([Ae({attribute:!1})],Rt.prototype,"hass",void 0),v([De()],Rt.prototype,"_config",void 0),v([De()],Rt.prototype,"_health",void 0),v([De()],Rt.prototype,"_deviceStats",void 0),v([De()],Rt.prototype,"_incidents",void 0),v([De()],Rt.prototype,"_entryEntityIds",void 0),v([De()],Rt.prototype,"_loading",void 0),v([De()],Rt.prototype,"_error",void 0);const Ft="homematicip-system-health-card";async function Vt(e){try{return(await e.callWS({type:"config_entries/get",domain:"homematicip_local"})).map(e=>({value:e.entry_id,label:e.title}))}catch{return[]}}customElements.get(Ft)||customElements.define(Ft,Rt);class jt extends ke{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",show_incidents:"Show incidents",max_incidents:"Max incidents",poll_interval:"Poll interval"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await Vt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_incidents",selector:{boolean:{}},default:!1},{name:"max_incidents",selector:{number:{min:1,max:50,mode:"box"}},default:5},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?ne`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:le}_valueChanged(e){var t;e.stopPropagation(),t={config:{...this._config,...e.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:t}))}static{this.styles=$`
    ha-form {
      display: block;
    }
  `}}v([Ae({attribute:!1})],jt.prototype,"hass",void 0),v([De()],jt.prototype,"_config",void 0),v([De()],jt.prototype,"_entryOptions",void 0);const Zt="homematicip-system-health-editor";customElements.get(Zt)||customElements.define(Zt,jt);class Yt extends ke{constructor(){super(...arguments),this._devices=[],this._totalDevices=0,this._problemCount=0,this._loading=!0,this._error=""}static{this.styles=Bt}setConfig(e){this._config={filter:"problems",show_model:!0,max_devices:10,poll_interval:60,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=Wt(this.hass.config.language))}_startPolling(){this._stopPolling();const e=1e3*(this._config?.poll_interval??60);this._pollTimer=setTimeout(()=>this._fetchData(),e)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{let e=await p(this.hass,this._config.entry_id);this._config.interface_filter&&(e=e.filter(e=>e.interface_id===this._config.interface_filter)),this._totalDevices=e.length,this._devices=this._filterDevices(e),this._problemCount=this._devices.filter(e=>"ok"!==e.severity).length,this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}this._startPolling()}else this._loading=!1}_filterDevices(e){const t=this._config?.filter??"problems",i=[];for(const s of e){const e=s.maintenance,a=[];let o="ok";!e.unreach||"all"!==t&&"problems"!==t&&"unreachable"!==t||(a.push(this._t?.notReachable??"Not reachable"),o="error"),!e.low_bat||"all"!==t&&"problems"!==t&&"low_battery"!==t||(a.push(this._t?.lowBattery??"Low battery"),"ok"===o&&(o="warning")),!e.config_pending||"all"!==t&&"problems"!==t&&"config_pending"!==t||(a.push(this._t?.configPending??"Config pending"),"ok"===o&&(o="warning")),("all"===t||a.length>0)&&i.push({device:s,issues:a,severity:o})}const s={error:0,warning:1,ok:2};i.sort((e,t)=>{const i=s[e.severity]-s[t.severity];return 0!==i?i:e.device.name.localeCompare(t.device.name)});const a=this._config?.max_devices??10;return a>0?i.slice(0,a):i}render(){if(!this._config||!this._t)return le;const e=this._config.title??this._t.deviceStatus;return this._loading?ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&0===this._totalDevices?ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:ne`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">
            ${this._problemCount>0?ne`<span class="badge error">${this._problemCount} ${this._t.problems}</span>`:ne`<span class="badge ok">OK</span>`}
          </div>
        </div>
        <div class="card-content">
          ${this._devices.length>0?this._renderDevices():this._renderAllOk()}
        </div>
      </ha-card>
    `}_deviceIcon(e){return"error"===e?"mdi:close-circle":"warning"===e?"mdi:alert":"mdi:check-circle"}_renderDevices(){const e=this._devices.length,t=this._totalDevices-e;return ne`
      <div class="item-list">
        ${this._devices.map(e=>ne`
            <div class="item-row ${e.severity}">
              <ha-icon class="item-icon" .icon=${this._deviceIcon(e.severity)}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.device.name}</div>
                <div class="item-secondary">
                  ${this._config?.show_model?`${e.device.model}`:""}${e.issues.length>0?`${this._config?.show_model?" · ":""}${e.issues.join(", ")}`:""}
                </div>
              </div>
            </div>
          `)}
      </div>
      ${t>0?ne`<div class="summary-line">+ ${t} ${this._t.devices}</div>`:le}
    `}_renderAllOk(){return ne`<div class="empty-state">${this._t.allDevicesOk}</div>`}static getConfigElement(){return document.createElement("homematicip-device-status-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}v([Ae({attribute:!1})],Yt.prototype,"hass",void 0),v([De()],Yt.prototype,"_config",void 0),v([De()],Yt.prototype,"_devices",void 0),v([De()],Yt.prototype,"_totalDevices",void 0),v([De()],Yt.prototype,"_problemCount",void 0),v([De()],Yt.prototype,"_loading",void 0),v([De()],Yt.prototype,"_error",void 0);const qt="homematicip-device-status-card";customElements.get(qt)||customElements.define(qt,Yt);class Jt extends ke{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",filter:"Filter",show_model:"Show device model",max_devices:"Max devices (0 = all)",poll_interval:"Poll interval",interface_filter:"Interface filter (optional)"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await Vt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"filter",selector:{select:{options:[{value:"problems",label:"Problems only"},{value:"all",label:"All devices"},{value:"unreachable",label:"Unreachable"},{value:"low_battery",label:"Low battery"},{value:"config_pending",label:"Config pending"}],mode:"dropdown"}},default:"problems"},{name:"show_model",selector:{boolean:{}},default:!0},{name:"max_devices",selector:{number:{min:0,max:100,mode:"box"}},default:10},{name:"poll_interval",selector:{number:{min:10,max:600,mode:"box",unit_of_measurement:"s"}},default:60},{name:"interface_filter",selector:{text:{}}}]}render(){return this.hass&&this._config?ne`
      <ha-form
        .hass=${this.hass}
        .data=${{...this._config,filter:this._config.filter||"problems"}}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:le}_valueChanged(e){e.stopPropagation();const t={...this._config,...e.detail.value};var i;t.interface_filter||delete t.interface_filter,i={config:t},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:i}))}static{this.styles=$`
    ha-form {
      display: block;
    }
  `}}v([Ae({attribute:!1})],Jt.prototype,"hass",void 0),v([De()],Jt.prototype,"_config",void 0),v([De()],Jt.prototype,"_entryOptions",void 0);const Gt="homematicip-device-status-editor";customElements.get(Gt)||customElements.define(Gt,Jt);class Kt extends ke{constructor(){super(...arguments),this._serviceMessages=[],this._alarmMessages=[],this._loading=!0,this._error=""}static{this.styles=Bt}setConfig(e){this._config={show_service:!0,show_alarms:!0,max_messages:10,show_timestamp:!0,compact:!1,poll_interval:30,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=Wt(this.hass.config.language))}_startPolling(){this._stopPolling();const e=1e3*(this._config?.poll_interval??30);this._pollTimer=setTimeout(()=>this._fetchData(),e)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{const e=[];this._config.show_service&&e.push(u(this.hass,this._config.entry_id).then(e=>this._serviceMessages=e)),this._config.show_alarms&&e.push(m(this.hass,this._config.entry_id).then(e=>this._alarmMessages=e)),await Promise.all(e),this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}this._startPolling()}else this._loading=!1}async _acknowledgeService(e){if(this.hass&&this._config)try{await g(this.hass,this._config.entry_id,e),this._serviceMessages=this._serviceMessages.filter(t=>t.msg_id!==e)}catch{}}async _acknowledgeAlarm(e){if(this.hass&&this._config)try{await _(this.hass,this._config.entry_id,e),this._alarmMessages=this._alarmMessages.filter(t=>t.alarm_id!==e)}catch{}}render(){if(!this._config||!this._t)return le;const e=this._config.title??this._t.messages;if(this._loading)return ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `;if(this._error&&0===this._serviceMessages.length&&0===this._alarmMessages.length)return ne`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `;const t=this._alarmMessages.length,i=this._serviceMessages.length;return ne`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">
            ${t>0?ne`<span class="badge error">${t}</span>`:le}
            ${i>0?ne`<span class="badge warning">${i}</span>`:le}
            ${0===t&&0===i?ne`<span class="badge ok">OK</span>`:le}
          </div>
        </div>
        <div class="card-content">
          ${this._renderAlarms()} ${this._renderServiceMessages()}
          ${0===t&&0===i?ne`<div class="empty-state">${this._t.noMessages}</div>`:le}
        </div>
      </ha-card>
    `}_renderAlarms(){if(!this._config?.show_alarms||0===this._alarmMessages.length)return le;const e=this._config.max_messages??10,t=this._alarmMessages.slice(0,e);return ne`
      <div class="section-title">${this._t.alarms}</div>
      <div class="item-list">
        ${t.map(e=>ne`
            <div class="item-row error">
              <ha-icon class="item-icon" .icon=${"mdi:bell-alert"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.device_name||e.name}</div>
                <div class="item-secondary">
                  ${e.display_name}${e.counter>1?` · ${e.counter}x`:""}${this._config?.show_timestamp?` · ${this._formatTimestamp(e.timestamp)}`:""}
                </div>
              </div>
              <div class="item-action">
                <ha-icon-button
                  .label=${this._t.acknowledge}
                  @click=${()=>this._acknowledgeAlarm(e.alarm_id)}
                >
                  <ha-icon .icon=${"mdi:check"}></ha-icon>
                </ha-icon-button>
              </div>
            </div>
          `)}
      </div>
    `}_renderServiceMessages(){if(!this._config?.show_service||0===this._serviceMessages.length)return le;const e=this._config.max_messages??10,t=this._serviceMessages.slice(0,e);return ne`
      <div class="section-title">${this._t.serviceMessages}</div>
      <div class="item-list">
        ${t.map(e=>ne`
            <div class="item-row warning">
              <ha-icon class="item-icon" .icon=${"mdi:alert"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.device_name||e.name}</div>
                <div class="item-secondary">
                  ${e.message_code}${e.counter>1?` · ${e.counter}x`:""}${this._config?.show_timestamp?` · ${this._formatTimestamp(e.timestamp)}`:""}
                </div>
              </div>
              ${e.quittable?ne`
                    <div class="item-action">
                      <ha-icon-button
                        .label=${this._t.acknowledge}
                        @click=${()=>this._acknowledgeService(e.msg_id)}
                      >
                        <ha-icon .icon=${"mdi:check"}></ha-icon>
                      </ha-icon-button>
                    </div>
                  `:le}
            </div>
          `)}
      </div>
    `}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return e}}static getConfigElement(){return document.createElement("homematicip-messages-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}v([Ae({attribute:!1})],Kt.prototype,"hass",void 0),v([De()],Kt.prototype,"_config",void 0),v([De()],Kt.prototype,"_serviceMessages",void 0),v([De()],Kt.prototype,"_alarmMessages",void 0),v([De()],Kt.prototype,"_loading",void 0),v([De()],Kt.prototype,"_error",void 0);const Xt="homematicip-messages-card";customElements.get(Xt)||customElements.define(Xt,Kt);class Qt extends ke{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",show_alarms:"Show alarms",show_service:"Show service messages",max_messages:"Max messages",show_timestamp:"Show timestamps",poll_interval:"Poll interval"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await Vt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_alarms",selector:{boolean:{}},default:!0},{name:"show_service",selector:{boolean:{}},default:!0},{name:"max_messages",selector:{number:{min:1,max:50,mode:"box"}},default:10},{name:"show_timestamp",selector:{boolean:{}},default:!0},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?ne`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:le}_valueChanged(e){var t;e.stopPropagation(),t={config:{...this._config,...e.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:t}))}static{this.styles=$`
    ha-form {
      display: block;
    }
  `}}v([Ae({attribute:!1})],Qt.prototype,"hass",void 0),v([De()],Qt.prototype,"_config",void 0),v([De()],Qt.prototype,"_entryOptions",void 0);const ei="homematicip-messages-editor";customElements.get(ei)||customElements.define(ei,Qt),window.customCards=window.customCards||[];const ti=(e,t,i)=>{window.customCards.some(t=>t.type===e)||window.customCards.push({type:e,name:t,description:i})};ti("homematicip-local-climate-schedule-card","Homematic(IP) Local Climate Schedule Card","Display and edit Homematic thermostat schedules"),ti("homematicip-local-schedule-card","HomematicIP Local Scheduler Card","A custom card for Homematic(IP) Local schedules (switch, valve, cover, light)"),ti("homematicip-system-health-card","HomematicIP System Health","System health, device statistics, and incidents for HomematicIP Local"),ti("homematicip-device-status-card","HomematicIP Device Status","Device status overview with problem highlighting for HomematicIP Local"),ti("homematicip-messages-card","HomematicIP Messages","Service messages and alarms with acknowledgment for HomematicIP Local");const ii=new Set(["homematicip-local-climate-schedule-card","homematicip-local-schedule-card","homematicip-system-health-card","homematicip-device-status-card","homematicip-messages-card"]),si=new Map;for(const e of ii){const t=customElements.get(e);t&&si.set(e,t)}function ai(){let e=0;for(const[t,i]of si)if(!customElements.get(t))try{customElements.define(t,i),e++,console.info(`[HMIP] Re-registered: ${t}`)}catch{try{customElements.define(t,class extends i{}),e++,console.info(`[HMIP] Re-registered (subclass): ${t}`)}catch{console.warn(`[HMIP] Failed to re-register: ${t}`)}}return e}function oi(e,t){for(const i of Array.from(e.querySelectorAll("*")))t(i),i.shadowRoot&&oi(i.shadowRoot,t)}function ni(){let e=0;return oi(document,t=>{if("hui-card"!==t.tagName.toLowerCase())return;const i=null!==t.querySelector("hui-error-card"),s=t._element,a="hui-error-card"===s?.tagName?.toLowerCase();if(!i&&!a)return;const o=t.config;if(!o?.type)return;const n=o.type.startsWith("custom:")?o.type.slice(7):o.type;if(!ii.has(n))return;if(!customElements.get(n))return;const r=t._loadElement;"function"==typeof r&&(console.info(`[HMIP] Recovering error card: ${n}`),r.call(t,o),e++)}),e}for(const e of[100,500,1500,3e3,5e3])setTimeout(()=>{const t=ai(),i=ni();(t>0||i>0)&&console.info(`[HMIP] Recovery @${e}ms: ${t} re-registered, ${i} error cards recovered`)},e);
