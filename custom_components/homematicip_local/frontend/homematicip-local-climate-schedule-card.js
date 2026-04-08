function t(t,e,i,s){var a,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var r=t.length-1;r>=0;r--)(a=t[r])&&(n=(o<3?a(n):o>3?a(e,i,n):a(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n}"function"==typeof SuppressedError&&SuppressedError;const e=globalThis,i=e.ShadowRoot&&(void 0===e.ShadyCSS||e.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),a=new WeakMap;let o=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(i&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=a.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&a.set(e,t))}return t}toString(){return this.cssText}};const n=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new o(i,t,s)},r=i?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new o("string"==typeof t?t:t+"",void 0,s))(e)})(t):t,{is:l,defineProperty:d,getOwnPropertyDescriptor:c,getOwnPropertyNames:h,getOwnPropertySymbols:p,getPrototypeOf:u}=Object,m=globalThis,g=m.trustedTypes,f=g?g.emptyScript:"",_=m.reactiveElementPolyfillSupport,v=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?f:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},b=(t,e)=>!l(t,e),x={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:b};Symbol.metadata??=Symbol("metadata"),m.litPropertyMetadata??=new WeakMap;let $=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=x){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&d(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:a}=c(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const o=s?.call(this);a?.call(this,e),this.requestUpdate(t,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??x}static _$Ei(){if(this.hasOwnProperty(v("elementProperties")))return;const t=u(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(v("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(v("properties"))){const t=this.properties,e=[...h(t),...p(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(r(t))}else void 0!==t&&e.push(r(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,s)=>{if(i)t.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const i of s){const s=document.createElement("style"),a=e.litNonce;void 0!==a&&s.setAttribute("nonce",a),s.textContent=i.cssText,t.appendChild(s)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const a=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(e,i.type);this._$Em=t,null==a?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),a="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=s;const o=a.fromAttribute(e,t.type);this[s]=o??this._$Ej?.get(s)??o,this._$Em=null}}requestUpdate(t,e,i,s=!1,a){if(void 0!==t){const o=this.constructor;if(!1===s&&(a=this[t]),i??=o.getPropertyOptions(t),!((i.hasChanged??b)(a,e)||i.useDefault&&i.reflect&&a===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:a},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),!0!==a||void 0!==o)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};$.elementStyles=[],$.shadowRootOptions={mode:"open"},$[v("elementProperties")]=new Map,$[v("finalized")]=new Map,_?.({ReactiveElement:$}),(m.reactiveElementVersions??=[]).push("2.1.2");const k=globalThis,w=t=>t,S=k.trustedTypes,E=S?S.createPolicy("lit-html",{createHTML:t=>t}):void 0,T="$lit$",A=`lit$${Math.random().toFixed(9).slice(2)}$`,M="?"+A,D=`<${M}>`,C=document,P=()=>C.createComment(""),I=t=>null===t||"object"!=typeof t&&"function"!=typeof t,L=Array.isArray,O="[ \t\n\f\r]",B=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,z=/-->/g,N=/>/g,U=RegExp(`>|${O}(?:([^\\s"'>=/]+)(${O}*=${O}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),W=/'/g,H=/"/g,R=/^(?:script|style|textarea|title)$/i,F=(t,...e)=>({_$litType$:1,strings:t,values:e}),j=Symbol.for("lit-noChange"),V=Symbol.for("lit-nothing"),Z=new WeakMap,Y=C.createTreeWalker(C,129);function q(t,e){if(!L(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==E?E.createHTML(e):e}class J{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let a=0,o=0;const n=t.length-1,r=this.parts,[l,d]=((t,e)=>{const i=t.length-1,s=[];let a,o=2===e?"<svg>":3===e?"<math>":"",n=B;for(let e=0;e<i;e++){const i=t[e];let r,l,d=-1,c=0;for(;c<i.length&&(n.lastIndex=c,l=n.exec(i),null!==l);)c=n.lastIndex,n===B?"!--"===l[1]?n=z:void 0!==l[1]?n=N:void 0!==l[2]?(R.test(l[2])&&(a=RegExp("</"+l[2],"g")),n=U):void 0!==l[3]&&(n=U):n===U?">"===l[0]?(n=a??B,d=-1):void 0===l[1]?d=-2:(d=n.lastIndex-l[2].length,r=l[1],n=void 0===l[3]?U:'"'===l[3]?H:W):n===H||n===W?n=U:n===z||n===N?n=B:(n=U,a=void 0);const h=n===U&&t[e+1].startsWith("/>")?" ":"";o+=n===B?i+D:d>=0?(s.push(r),i.slice(0,d)+T+i.slice(d)+A+h):i+A+(-2===d?e:h)}return[q(t,o+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]})(t,e);if(this.el=J.createElement(l,i),Y.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=Y.nextNode())&&r.length<n;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(T)){const e=d[o++],i=s.getAttribute(t).split(A),n=/([.?@])?(.*)/.exec(e);r.push({type:1,index:a,name:n[2],strings:i,ctor:"."===n[1]?tt:"?"===n[1]?et:"@"===n[1]?it:X}),s.removeAttribute(t)}else t.startsWith(A)&&(r.push({type:6,index:a}),s.removeAttribute(t));if(R.test(s.tagName)){const t=s.textContent.split(A),e=t.length-1;if(e>0){s.textContent=S?S.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],P()),Y.nextNode(),r.push({type:2,index:++a});s.append(t[e],P())}}}else if(8===s.nodeType)if(s.data===M)r.push({type:2,index:a});else{let t=-1;for(;-1!==(t=s.data.indexOf(A,t+1));)r.push({type:7,index:a}),t+=A.length-1}a++}}static createElement(t,e){const i=C.createElement("template");return i.innerHTML=t,i}}function K(t,e,i=t,s){if(e===j)return e;let a=void 0!==s?i._$Co?.[s]:i._$Cl;const o=I(e)?void 0:e._$litDirective$;return a?.constructor!==o&&(a?._$AO?.(!1),void 0===o?a=void 0:(a=new o(t),a._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=a:i._$Cl=a),void 0!==a&&(e=K(t,a._$AS(t,e.values),a,s)),e}class G{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??C).importNode(e,!0);Y.currentNode=s;let a=Y.nextNode(),o=0,n=0,r=i[0];for(;void 0!==r;){if(o===r.index){let e;2===r.type?e=new Q(a,a.nextSibling,this,t):1===r.type?e=new r.ctor(a,r.name,r.strings,this,t):6===r.type&&(e=new st(a,this,t)),this._$AV.push(e),r=i[++n]}o!==r?.index&&(a=Y.nextNode(),o++)}return Y.currentNode=C,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class Q{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=V,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=K(this,t,e),I(t)?t===V||null==t||""===t?(this._$AH!==V&&this._$AR(),this._$AH=V):t!==this._$AH&&t!==j&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>L(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==V&&I(this._$AH)?this._$AA.nextSibling.data=t:this.T(C.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=J.createElement(q(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new G(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=Z.get(t.strings);return void 0===e&&Z.set(t.strings,e=new J(t)),e}k(t){L(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const a of t)s===e.length?e.push(i=new Q(this.O(P()),this.O(P()),this,this.options)):i=e[s],i._$AI(a),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=w(t).nextSibling;w(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class X{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,a){this.type=1,this._$AH=V,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=a,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=V}_$AI(t,e=this,i,s){const a=this.strings;let o=!1;if(void 0===a)t=K(this,t,e,0),o=!I(t)||t!==this._$AH&&t!==j,o&&(this._$AH=t);else{const s=t;let n,r;for(t=a[0],n=0;n<a.length-1;n++)r=K(this,s[i+n],e,n),r===j&&(r=this._$AH[n]),o||=!I(r)||r!==this._$AH[n],r===V?t=V:t!==V&&(t+=(r??"")+a[n+1]),this._$AH[n]=r}o&&!s&&this.j(t)}j(t){t===V?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class tt extends X{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===V?void 0:t}}class et extends X{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==V)}}class it extends X{constructor(t,e,i,s,a){super(t,e,i,s,a),this.type=5}_$AI(t,e=this){if((t=K(this,t,e,0)??V)===j)return;const i=this._$AH,s=t===V&&i!==V||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,a=t!==V&&(i===V||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class st{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){K(this,t)}}const at={I:Q},ot=k.litHtmlPolyfillSupport;ot?.(J,Q),(k.litHtmlVersions??=[]).push("3.3.2");const nt=globalThis;let rt=class extends ${constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let a=s._$litPart$;if(void 0===a){const t=i?.renderBefore??null;s._$litPart$=a=new Q(e.insertBefore(P(),t),t,void 0,i??{})}return a._$AI(t),a})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return j}};rt._$litElement$=!0,rt.finalized=!0,nt.litElementHydrateSupport?.({LitElement:rt});const lt=nt.litElementPolyfillSupport;lt?.({LitElement:rt}),(nt.litElementVersions??=[]).push("4.2.2");const dt={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:b},ct=(t=dt,e,i)=>{const{kind:s,metadata:a}=i;let o=globalThis.litPropertyMetadata.get(a);if(void 0===o&&globalThis.litPropertyMetadata.set(a,o=new Map),"setter"===s&&((t=Object.create(t)).wrapped=!0),o.set(i.name,t),"accessor"===s){const{name:s}=i;return{set(i){const a=e.get.call(this);e.set.call(this,i),this.requestUpdate(s,a,t,!0,i)},init(e){return void 0!==e&&this.C(s,void 0,t,e),e}}}if("setter"===s){const{name:s}=i;return function(i){const a=this[s];e.call(this,i),this.requestUpdate(s,a,t,!0,i)}}throw Error("Unsupported decorator location: "+s)};function ht(t){return(e,i)=>"object"==typeof i?ct(t,e,i):((t,e,i)=>{const s=e.hasOwnProperty(i);return e.constructor.createProperty(i,t),s?Object.getOwnPropertyDescriptor(e,i):void 0})(t,e,i)}function pt(t){return ht({...t,state:!0,attribute:!1})}const ut=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"],mt=["fixed_time","astro","fixed_if_before_astro","astro_if_before_fixed","fixed_if_after_astro","astro_if_after_fixed","earliest","latest"],gt={switch:{levelType:"binary",hasLevel2:!1,hasDuration:!0,hasRampTime:!1},light:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!0},cover:{levelType:"percentage",hasLevel2:!0,hasDuration:!1,hasRampTime:!1},valve:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!1}},ft=["ms","s","min","h"];function _t(t){const[e,i]=t.split(":").map(Number);return 60*e+i}function vt(t){const e=t%60;return`${Math.floor(t/60).toString().padStart(2,"0")}:${e.toString().padStart(2,"0")}`}function yt(t,e="24"){if("24"===e)return t;const[i,s]=t.split(":");let a=parseInt(i,10);if(24===a)return"12:00 AM";const o=a>=12?"PM":"AM";return 0===a?a=12:a>12&&(a-=12),`${a}:${s||"00"} ${o}`}function bt(t){return t<10?"#2b9af9":t<14?"#40c4ff":t<17?"#26c6da":t<19?"#66bb6a":t<21?"#9ccc65":t<23?"#ffb74d":t<25?"#ff8100":"#f4511e"}function xt(t){const{base_temperature:e,periods:i}=t,s=[],a=[...i].sort((t,e)=>_t(t.starttime)-_t(e.starttime));for(let t=0;t<a.length;t++){const e=a[t];s.push({startTime:e.starttime,startMinutes:_t(e.starttime),endTime:e.endtime,endMinutes:_t(e.endtime),temperature:e.temperature,slot:t+1})}return{blocks:s,baseTemperature:e}}function $t(t,e){const i=[],s=[...t].sort((t,e)=>t.startMinutes-e.startMinutes);for(const t of s)i.push({starttime:t.startTime,endtime:t.endTime,temperature:t.temperature});return{base_temperature:e,periods:i}}function kt(t){if(0===t.length)return 20;const e=new Map;for(const i of t){const t=i.endMinutes-i.startMinutes,s=e.get(i.temperature)||0;e.set(i.temperature,s+t)}let i=0,s=20;for(const[t,a]of e.entries())a>i&&(i=a,s=t);return s}function wt(t){if(0===t.length)return[];const e=[...t].sort((t,e)=>t.startMinutes-e.startMinutes),i=[];let s={...e[0]};for(let t=1;t<e.length;t++){const a=e[t];s.endMinutes===a.startMinutes&&s.temperature===a.temperature?s={...s,endTime:a.endTime,endMinutes:a.endMinutes}:(i.push(s),s={...a})}return i.push(s),i.map((t,e)=>({...t,slot:e+1}))}function St(t,e){if(0===t.length)return[{startTime:"00:00",startMinutes:0,endTime:"24:00",endMinutes:1440,temperature:e,slot:1}];const i=[...t].sort((t,e)=>t.startMinutes-e.startMinutes),s=[];let a=0;for(const t of i)t.startMinutes>a&&s.push({startTime:vt(a),startMinutes:a,endTime:t.startTime,endMinutes:t.startMinutes,temperature:e,slot:s.length+1}),s.push({...t,slot:s.length+1}),a=t.endMinutes;return a<1440&&s.push({startTime:vt(a),startMinutes:a,endTime:"24:00",endMinutes:1440,temperature:e,slot:s.length+1}),wt(s)}function Et(t){return[...t].sort((t,e)=>t.startMinutes-e.startMinutes).map((t,e)=>({...t,slot:e+1}))}function Tt(t){return Boolean(Array.isArray(t.weekdays)&&t.weekdays.length>0&&Array.isArray(t.target_channels)&&t.target_channels.length>0)}function At(t){return"fixed_time"!==t}const Mt=/^(\d+(?:\.\d+)?)\s*(ms|s|min|h)$/;function Dt(t){const e=t.trim().match(Mt);return e?{value:parseFloat(e[1]),unit:e[2]}:null}function Ct(t,e){return`${t}${e}`}function Pt(t){return Mt.test(t.trim())}function It(t,e=5,i=30.5){const{base_temperature:s,periods:a}=t;if(s<e||s>i)return{key:"temperatureOutOfRange",params:{block:"base",min:`${e}`,max:`${i}`}};let o=0;for(let t=0;t<a.length;t++){const s=a[t];if(!s.starttime||!s.endtime||void 0===s.temperature)return{key:"slotMissingValues",params:{slot:`${t+1}`}};const n=_t(s.starttime),r=_t(s.endtime);if(r<=n)return{key:"blockEndBeforeStart",params:{block:`${t+1}`}};if(n<o)return{key:"slotTimeBackwards",params:{slot:`${t+1}`,time:s.starttime}};if(s.temperature<e||s.temperature>i)return{key:"temperatureOutOfRange",params:{block:`${t+1}`,min:`${e}`,max:`${i}`}};o=r}return null}const Lt=(t,e,i)=>{const s=new CustomEvent(e,{bubbles:!0,composed:!0,detail:i});t.dispatchEvent(s)};class Ot extends rt{constructor(){super(...arguments),this._expandedEntity=null,this._computeLabel=t=>({entities:"Entities",name:"Card Name (optional)",show_profile_selector:"Show profile selector",editable:"Allow editing",show_temperature:"Show temperature values",show_gradient:"Show color gradient",hour_format:"Time format"}[t.name]||t.name)}_getCompatibleEntityIds(){return this.hass?.states?Object.keys(this.hass.states).filter(t=>{if(!t.startsWith("climate."))return!1;const e=this.hass.states[t]?.attributes;return void 0!==e?.schedule_data}):[]}_buildEntitySchema(){return[{name:"entities",required:!0,selector:{entity:{multiple:!0,include_entities:this._getCompatibleEntityIds()}}}]}static{this.OPTIONS_SCHEMA=[{name:"name",selector:{text:{}}},{name:"show_profile_selector",selector:{boolean:{}},default:!0},{name:"editable",selector:{boolean:{}},default:!0},{name:"show_temperature",selector:{boolean:{}},default:!0},{name:"show_gradient",selector:{boolean:{}},default:!1},{name:"hour_format",selector:{select:{options:[{value:"24",label:"24h"},{value:"12",label:"12h (AM/PM)"}]}},default:"24"}]}setConfig(t){this._config=t}_getEntityId(t){return"string"==typeof t?t:t.entity}_getEntityName(t){return"string"==typeof t?"":t.name||""}_getEntityProfileNames(t){return"string"==typeof t?{}:t.profile_names||{}}_getEntityIds(){return this._config?.entities?this._config.entities.map(t=>this._getEntityId(t)):[]}_getAvailableProfiles(t){const e=this.hass?.states?.[t];return e?.attributes?.available_profiles?[...e.attributes.available_profiles].sort():[]}render(){if(!this.hass||!this._config)return V;const t={entities:this._getEntityIds()};return F`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${this._buildEntitySchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._entitiesChanged}
      ></ha-form>

      ${this._renderEntityConfig()}

      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${Ot.OPTIONS_SCHEMA}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._optionsChanged}
      ></ha-form>
    `}_renderEntityConfig(){const t=this._config?.entities||[];return 0===t.length?F``:F`
      <div class="entity-config">
        <div class="section-header">Entity Configuration</div>
        ${t.map((t,e)=>{const i=this._getEntityId(t),s=this._getEntityName(t),a=this._getEntityProfileNames(t),o=this.hass?.states?.[i]?.attributes.friendly_name||i,n=this._getAvailableProfiles(i),r=this._expandedEntity===i;return F`
            <div class="entity-section">
              <div class="entity-header" @click=${()=>this._toggleEntity(i)}>
                <span class="expand-icon">${r?"▼":"▶"}</span>
                <span class="entity-title" title=${i}>${o}</span>
              </div>

              ${r?F`
                    <div class="entity-details">
                      <div class="config-row">
                        <label>Display Name</label>
                        <input
                          type="text"
                          .value=${s}
                          placeholder=${o}
                          @input=${t=>this._entityNameChanged(e,t)}
                        />
                      </div>

                      ${n.length>0?F`
                            <div class="profile-names-section">
                              <div class="profile-names-header">Profile Names</div>
                              ${n.map(t=>F`
                                  <div class="config-row profile-row">
                                    <label>${t}</label>
                                    <input
                                      type="text"
                                      .value=${a[t]||""}
                                      placeholder=${t}
                                      @input=${i=>this._profileNameChanged(e,t,i)}
                                    />
                                  </div>
                                `)}
                            </div>
                          `:F`
                            <div class="no-profiles">No profiles available for this entity</div>
                          `}
                    </div>
                  `:""}
            </div>
          `})}
      </div>
    `}_toggleEntity(t){this._expandedEntity=this._expandedEntity===t?null:t}_entitiesChanged(t){t.stopPropagation();const e=(t.detail.value?.entities||[]).map(t=>{const e=this._config?.entities?.find(e=>this._getEntityId(e)===t);return e&&"string"!=typeof e&&(e.name||Object.keys(e.profile_names||{}).length>0)?{...e,entity:t}:t}),i={...this._config,entities:e};Lt(this,"config-changed",{config:i})}_getOrCreateEntityConfig(t,e){const i=t[e];return"string"==typeof i?{entity:i}:{...i}}_simplifyEntityConfig(t){const e=!!t.name,i=Object.keys(t.profile_names||{}).length>0;return e||i?t:t.entity}_entityNameChanged(t,e){const i=e.target.value.trim(),s=[...this._config?.entities||[]];if(t>=s.length)return;const a=this._getOrCreateEntityConfig(s,t);i?a.name=i:delete a.name,s[t]=this._simplifyEntityConfig(a);const o={...this._config,entities:s};Lt(this,"config-changed",{config:o})}_profileNameChanged(t,e,i){const s=i.target.value.trim(),a=[...this._config?.entities||[]];if(t>=a.length)return;const o=this._getOrCreateEntityConfig(a,t);o.profile_names||(o.profile_names={}),s?o.profile_names[e]=s:delete o.profile_names[e],0===Object.keys(o.profile_names).length&&delete o.profile_names,a[t]=this._simplifyEntityConfig(o);const n={...this._config,entities:a};Lt(this,"config-changed",{config:n})}_optionsChanged(t){t.stopPropagation();const e={...this._config,...t.detail.value,entities:this._config.entities};Lt(this,"config-changed",{config:e})}static{this.styles=n`
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
      font-size: 10px;
      color: var(--secondary-text-color);
      width: 12px;
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
  `}}function Bt(t){return e=>(customElements.get(t)||customElements.define(t,e),e)}t([ht({attribute:!1})],Ot.prototype,"hass",void 0),t([pt()],Ot.prototype,"_config",void 0),t([pt()],Ot.prototype,"_expandedEntity",void 0),customElements.get("homematicip-local-climate-schedule-card-editor")||customElements.define("homematicip-local-climate-schedule-card-editor",Ot);let zt=class{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}};const{I:Nt}=at,Ut=t=>t,Wt=()=>document.createComment(""),Ht=(t,e,i)=>{const s=t._$AA.parentNode,a=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=s.insertBefore(Wt(),a),o=s.insertBefore(Wt(),a);i=new Nt(e,o,t,t.options)}else{const e=i._$AB.nextSibling,o=i._$AM,n=o!==t;if(n){let e;i._$AQ?.(t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==o._$AU&&i._$AP(e)}if(e!==a||n){let t=i._$AA;for(;t!==e;){const e=Ut(t).nextSibling;Ut(s).insertBefore(t,a),t=e}}}return i},Rt=(t,e,i=t)=>(t._$AI(e,i),t),Ft={},jt=(t,e=Ft)=>t._$AH=e,Vt=t=>{t._$AR(),t._$AA.remove()},Zt=(t,e,i)=>{const s=new Map;for(let a=e;a<=i;a++)s.set(t[a],a);return s},Yt=(t=>(...e)=>({_$litDirective$:t,values:e}))(class extends zt{constructor(t){if(super(t),2!==t.type)throw Error("repeat() can only be used in text expressions")}dt(t,e,i){let s;void 0===i?i=e:void 0!==e&&(s=e);const a=[],o=[];let n=0;for(const e of t)a[n]=s?s(e,n):n,o[n]=i(e,n),n++;return{values:o,keys:a}}render(t,e,i){return this.dt(t,e,i).values}update(t,[e,i,s]){const a=(t=>t._$AH)(t),{values:o,keys:n}=this.dt(e,i,s);if(!Array.isArray(a))return this.ut=n,o;const r=this.ut??=[],l=[];let d,c,h=0,p=a.length-1,u=0,m=o.length-1;for(;h<=p&&u<=m;)if(null===a[h])h++;else if(null===a[p])p--;else if(r[h]===n[u])l[u]=Rt(a[h],o[u]),h++,u++;else if(r[p]===n[m])l[m]=Rt(a[p],o[m]),p--,m--;else if(r[h]===n[m])l[m]=Rt(a[h],o[m]),Ht(t,l[m+1],a[h]),h++,m--;else if(r[p]===n[u])l[u]=Rt(a[p],o[u]),Ht(t,a[h],a[p]),p--,u++;else if(void 0===d&&(d=Zt(n,u,m),c=Zt(r,h,p)),d.has(r[h]))if(d.has(r[p])){const e=c.get(n[u]),i=void 0!==e?a[e]:null;if(null===i){const e=Ht(t,a[h]);Rt(e,o[u]),l[u]=e}else l[u]=Rt(i,o[u]),Ht(t,a[h],i),a[e]=null;u++}else Vt(a[p]),p--;else Vt(a[h]),h++;for(;u<=m;){const e=Ht(t,l[m+1]);Rt(e,o[u]),l[u++]=e}for(;h<=p;){const t=a[h++];null!==t&&Vt(t)}return this.ut=n,jt(t,l),j}}),qt=n`
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
    opacity: 0.3;
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
`;var Jt=function(t,e,i,s){var a,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var r=t.length-1;r>=0;r--)(a=t[r])&&(n=(o<3?a(n):o>3?a(e,i,n):a(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n};let Kt=class extends rt{constructor(){super(...arguments),this.editable=!1,this.showTemperature=!0,this.showGradient=!1,this.temperatureUnit="°C",this.hourFormat="24",this.editorOpen=!1,this._currentTimePercent=0,this._currentTimeMinutes=0}connectedCallback(){super.connectedCallback(),this._updateCurrentTime(),this._timeUpdateInterval=window.setInterval(()=>{this._updateCurrentTime()},6e4)}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._timeUpdateInterval&&(clearInterval(this._timeUpdateInterval),this._timeUpdateInterval=void 0)}willUpdate(t){super.willUpdate(t)}_updateCurrentTime(){const t=new Date,e=60*t.getHours()+t.getMinutes();this._currentTimePercent=e/1440*100,this._currentTimeMinutes=e;const i=t.getDay();this._currentWeekday=["SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY"][i]}_isBlockActive(t,e){return!(!this._currentWeekday||this._currentWeekday!==t)&&this._currentTimeMinutes>=e.startMinutes&&this._currentTimeMinutes<e.endMinutes}_getTimeLabels(){const t=[];for(let e=0;e<=24;e+=3){const i=`${e.toString().padStart(2,"0")}:00`;t.push({hour:e,label:yt(i,this.hourFormat),position:e/24*100})}return t}_formatTimeDisplay(t){return yt(t,this.hourFormat)}_getBaseTemperature(t){if(this.scheduleData){const e=this.scheduleData[t];if(e){const{baseTemperature:t}=xt(e);return t}}return 20}_getParsedBlocks(t){if(this.scheduleData){const e=this.scheduleData[t];if(!e)return[];const{blocks:i}=xt(e);return i}return[]}_getWeekdayLabel(t){return this.translations?.weekdayShortLabels[t]??t.slice(0,2)}_handleWeekdayClick(t){this.editable&&this.dispatchEvent(new CustomEvent("weekday-click",{detail:{weekday:t},bubbles:!0,composed:!0}))}_handleCopy(t,e){e.stopPropagation(),this.dispatchEvent(new CustomEvent("copy-schedule",{detail:{weekday:t},bubbles:!0,composed:!0}))}_handlePaste(t,e){e.stopPropagation(),this.dispatchEvent(new CustomEvent("paste-schedule",{detail:{weekday:t},bubbles:!0,composed:!0}))}render(){return this.scheduleData?F`
      <div class="schedule-container">
        <!-- Empty cell for time-axis header alignment -->
        <div class="time-axis-header"></div>

        <!-- Weekday headers -->
        ${Yt(ut,t=>`header-${t}`,t=>{const e=this.copiedWeekday===t;return F`
              <div class="weekday-header">
                <div class="weekday-label">${this._getWeekdayLabel(t)}</div>
                ${this.editable?F`
                      <div class="weekday-actions">
                        <ha-icon-button
                          class="copy-btn ${e?"active":""}"
                          .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
                          @click=${e=>this._handleCopy(t,e)}
                          .label=${this.translations?.copySchedule??""}
                        ></ha-icon-button>
                        <ha-icon-button
                          class="paste-btn"
                          .path=${"M19,20H5V4H7V7H17V4H19M12,2A1,1 0 0,1 13,3A1,1 0 0,1 12,4A1,1 0 0,1 11,3A1,1 0 0,1 12,2M19,2H14.82C14.4,0.84 13.3,0 12,0C10.7,0 9.6,0.84 9.18,2H5A2,2 0 0,0 3,4V20A2,2 0 0,0 5,22H19A2,2 0 0,0 21,20V4A2,2 0 0,0 19,2Z"}
                          @click=${e=>this._handlePaste(t,e)}
                          .label=${this.translations?.pasteSchedule??""}
                          .disabled=${!this.copiedWeekday}
                        ></ha-icon-button>
                      </div>
                    `:""}
              </div>
            `})}

        <!-- Time axis labels -->
        <div class="time-axis-labels">
          ${Yt(this._getTimeLabels(),t=>t.hour,t=>F`
              <div class="time-label" style="top: ${t.position}%">${t.label}</div>
            `)}
        </div>

        <!-- Time blocks content wrapper (for correct indicator positioning) -->
        <div class="schedule-content">
          ${Yt(ut,t=>`${t}-${this.currentProfile}-${this.scheduleDataHash}`,t=>{const e=this._getParsedBlocks(t),i=this._getBaseTemperature(t),s=St(e,i);return F`
                <div
                  class="time-blocks ${this.editable?"editable":""}"
                  @click=${()=>this._handleWeekdayClick(t)}
                >
                  ${Yt(s,t=>`${t.slot}-${t.startMinutes}-${this.currentProfile}`,(a,o)=>{const n=this._isBlockActive(t,a),r=a.temperature===i&&!e.some(t=>t.startMinutes===a.startMinutes&&t.endMinutes===a.endMinutes);let l;if(r)l="background-color: var(--secondary-background-color, #e0e0e0);";else if(this.showGradient){l=`background: ${function(t,e,i){const s=bt(t);return null===e&&null===i?s:null!==e&&null===i?`linear-gradient(to bottom, ${bt(e)}, ${s})`:null===e&&null!==i?`linear-gradient(to bottom, ${s}, ${bt(i)})`:`linear-gradient(to bottom, ${bt(e)}, ${s} 50%, ${bt(i)})`}(a.temperature,o>0?s[o-1].temperature:null,o<s.length-1?s[o+1].temperature:null)};`}else l=`background-color: ${bt(a.temperature)};`;return F`
                        <div
                          class="time-block ${n?"active":""} ${r?"base-temp-block":""}"
                          style="
                              height: ${(a.endMinutes-a.startMinutes)/1440*100}%;
                              ${l}
                            "
                        >
                          ${this.showTemperature?F`<span class="temperature"
                                >${a.temperature.toFixed(1)}°</span
                              >`:""}
                          <div class="time-block-tooltip">
                            <div class="tooltip-time">
                              ${this._formatTimeDisplay(a.startTime)} -
                              ${this._formatTimeDisplay(a.endTime)}
                            </div>
                            <div class="tooltip-temp">
                              ${function(t,e="°C"){return`${t.toFixed(1)}${e}`}(a.temperature,this.temperatureUnit)}
                            </div>
                          </div>
                        </div>
                      `})}
                </div>
              `})}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen?"":F`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?F`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `:F``}static{this.styles=qt}};Jt([ht({attribute:!1})],Kt.prototype,"scheduleData",void 0),Jt([ht({type:Boolean})],Kt.prototype,"editable",void 0),Jt([ht({type:Boolean})],Kt.prototype,"showTemperature",void 0),Jt([ht({type:Boolean})],Kt.prototype,"showGradient",void 0),Jt([ht({type:String})],Kt.prototype,"temperatureUnit",void 0),Jt([ht({type:String})],Kt.prototype,"hourFormat",void 0),Jt([ht({attribute:!1})],Kt.prototype,"translations",void 0),Jt([ht({type:String})],Kt.prototype,"copiedWeekday",void 0),Jt([ht({type:Boolean})],Kt.prototype,"editorOpen",void 0),Jt([ht({type:String})],Kt.prototype,"currentProfile",void 0),Jt([ht({type:String})],Kt.prototype,"scheduleDataHash",void 0),Jt([pt()],Kt.prototype,"_currentTimePercent",void 0),Jt([pt()],Kt.prototype,"_currentTimeMinutes",void 0),Jt([pt()],Kt.prototype,"_currentWeekday",void 0),Kt=Jt([Bt("hmip-schedule-grid")],Kt);const Gt=n`
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
    opacity: 0.3;
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
    grid-template-columns: 100px 100px 90px 1fr 24px;
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
    grid-template-columns: 100px 100px 90px 1fr 24px;
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
    opacity: 0.3;
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
    min-width: 100px;
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
    opacity: 0.3;
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
      max-height: 200px;
    }
  }
`;var Qt=function(t,e,i,s){var a,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var r=t.length-1;r>=0;r--)(a=t[r])&&(n=(o<3?a(n):o>3?a(e,i,n):a(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n};let Xt=class extends rt{constructor(){super(),this.open=!1,this.minTemp=5,this.maxTemp=30.5,this.tempStep=.5,this.temperatureUnit="°C",this.hourFormat="24",this._validationWarnings=[],this._historyStack=[],this._historyIndex=-1,this._keyDownHandler=this._handleKeyDown.bind(this)}connectedCallback(){super.connectedCallback(),window.addEventListener("keydown",this._keyDownHandler)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("keydown",this._keyDownHandler)}willUpdate(t){if(super.willUpdate(t),(t.has("open")||t.has("weekday"))&&this.open&&this.weekday){const e=t.get("open"),i=t.get("weekday");(!e&&this.open||this.open&&i!==this.weekday)&&this._initializeEditor(this.weekday)}}_initializeEditor(t){this._editingWeekday=t,this._editingBlocks=this._getParsedBlocks(t),this._editingSlotIndex=void 0,this._editingSlotData=void 0;const e=this.scheduleData?.[t];if(e){const{baseTemperature:t}=xt(e);this._editingBaseTemperature=t}else this._editingBaseTemperature=20;this._historyStack=[JSON.parse(JSON.stringify(this._editingBlocks))],this._historyIndex=0,this._updateValidationWarnings()}_getParsedBlocks(t){if(this.scheduleData){const e=this.scheduleData[t];if(!e)return[];const{blocks:i}=xt(e);return i}return[]}_getWeekdayLabel(t,e){return"long"===e?this.translations?.weekdayLongLabels[t]??t:this.translations?.weekdayShortLabels[t]??t.slice(0,2)}_formatTimeDisplay(t){return yt(t,this.hourFormat)}_formatValidationParams(t){if(!t)return{};const e={};for(const[i,s]of Object.entries(t))"weekday"===i&&ut.includes(s)?e.weekday=this._getWeekdayLabel(s,"long"):e[i]=s;return e}_translateValidationMessage(t){const e=this.translations?.validationMessages[t.key]||t.key,i=this._formatValidationParams(t.params);t.nested&&(i.details=this._translateValidationMessage(t.nested));let s=e;for(const[t,e]of Object.entries(i))s=s.replace(`{${t}}`,e);return s}_saveHistoryState(){if(!this._editingBlocks)return;const t=JSON.parse(JSON.stringify(this._editingBlocks));this._historyStack=this._historyStack.slice(0,this._historyIndex+1),this._historyStack.push(t),this._historyIndex++,this._historyStack.length>50&&(this._historyStack.shift(),this._historyIndex--)}_undo(){this._historyIndex<=0||(this._historyIndex--,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_redo(){this._historyIndex>=this._historyStack.length-1||(this._historyIndex++,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_canUndo(){return this._historyIndex>0}_canRedo(){return this._historyIndex<this._historyStack.length-1}_handleKeyDown(t){if(!this.open||!this._editingWeekday||!this._editingBlocks)return;const e=t.ctrlKey||t.metaKey;e&&"z"===t.key&&!t.shiftKey?(t.preventDefault(),this._undo()):e&&("y"===t.key||"z"===t.key&&t.shiftKey)&&(t.preventDefault(),this._redo())}_updateValidationWarnings(){this._validationWarnings=this._editingBlocks?function(t,e=5,i=30.5){const s=[];if(0===t.length)return s;for(let e=0;e<t.length-1;e++){const i=t[e];i.endMinutes<i.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${e+1}`}}),i.endMinutes===i.startMinutes&&s.push({key:"blockZeroDuration",params:{block:`${e+1}`}})}const a=t[t.length-1];return a.endMinutes<a.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${t.length}`}}),t.forEach((t,a)=>{(t.startMinutes<0||t.startMinutes>1440)&&s.push({key:"invalidStartTime",params:{block:`${a+1}`}}),(t.endMinutes<0||t.endMinutes>1440)&&s.push({key:"invalidEndTime",params:{block:`${a+1}`}}),(t.temperature<e||t.temperature>i)&&s.push({key:"temperatureOutOfRange",params:{block:`${a+1}`,min:`${e}`,max:`${i}`}})}),s}(this._editingBlocks,this.minTemp,this.maxTemp):[]}_startSlotEdit(t){if(!this._editingBlocks||t<0||t>=this._editingBlocks.length)return;const e=this._editingBlocks[t];this._editingSlotIndex=t,this._editingSlotData={startTime:e.startTime,endTime:e.endTime,temperature:e.temperature}}_startSlotEditFromDisplay(t,e){if(!this._editingBlocks)return;const i=e[t],s=this._editingBlocks.findIndex(t=>t.startMinutes===i.startMinutes&&t.endMinutes===i.endMinutes&&t.temperature===i.temperature);-1!==s&&this._startSlotEdit(s)}_cancelSlotEdit(){this._editingSlotIndex=void 0,this._editingSlotData=void 0}_saveSlotEdit(){if(void 0===this._editingSlotIndex||!this._editingSlotData||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const t=this._editingSlotIndex,{startTime:e,endTime:i,temperature:s}=this._editingSlotData,a={startTime:e,startMinutes:_t(e),endTime:i,endMinutes:_t(i),temperature:s,slot:t+1},o=this._editingBlocks.filter((e,i)=>i!==t),n=function(t,e){const i=[],s=e.startMinutes,a=e.endMinutes,o=[...t].sort((t,e)=>t.startMinutes-e.startMinutes);for(const t of o){const e=t.startMinutes,o=t.endMinutes;o<=s||e>=a?i.push(t):(e<s&&i.push({...t,endTime:vt(s),endMinutes:s,slot:i.length+1}),o>a&&i.push({...t,startTime:vt(a),startMinutes:a,slot:i.length+1}))}i.push({...e,slot:i.length+1});const n=i.sort((t,e)=>t.startMinutes-e.startMinutes);return wt(n)}(o,a),r=wt(Et(n));this._saveHistoryState(),this._editingBlocks=r,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._updateValidationWarnings()}_addNewSlot(){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;if(this._editingBlocks.length>=12)return;let t=0,e=60;if(this._editingBlocks.length>0){const i=Et(this._editingBlocks),s=i[i.length-1];if(s.endMinutes<1440)t=s.endMinutes,e=Math.min(t+60,1440);else{let s=!1;for(let a=0;a<i.length;a++){const o=0===a?0:i[a-1].endMinutes;if(i[a].startMinutes>o){t=o,e=i[a].startMinutes,s=!0;break}}if(!s)return}}const i=Math.min(this._editingBaseTemperature+2,this.maxTemp),s={startTime:vt(t),startMinutes:t,endTime:vt(e),endMinutes:e,temperature:i,slot:this._editingBlocks.length+1};this._saveHistoryState();const a=Et([...this._editingBlocks,s]);this._editingBlocks=a;const o=a.findIndex(i=>i.startMinutes===t&&i.endMinutes===e);o>=0&&this._startSlotEdit(o),this._updateValidationWarnings()}_removeTimeBlockByIndex(t,e){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;const i=e[t],s=this._editingBlocks.findIndex(t=>t.startMinutes===i.startMinutes&&t.endMinutes===i.endMinutes&&t.temperature===i.temperature);if(-1===s)return;this._saveHistoryState();const a=this._editingBlocks.filter((t,e)=>e!==s);this._editingBlocks=wt(Et(a)),this._updateValidationWarnings()}_switchToWeekday(t){t!==this._editingWeekday&&this._initializeEditor(t)}_closeEditor(){this._editingWeekday=void 0,this._editingBlocks=void 0,this._editingBaseTemperature=void 0,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._historyStack=[],this._historyIndex=-1,this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_saveSchedule(){if(!this._editingWeekday||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const t=It($t(this._editingBlocks,this._editingBaseTemperature),this.minTemp,this.maxTemp);if(t){const e=this._translateValidationMessage(t);return void this.dispatchEvent(new CustomEvent("validation-failed",{detail:{error:e},bubbles:!0,composed:!0}))}this.dispatchEvent(new CustomEvent("save-schedule",{detail:{weekday:this._editingWeekday,blocks:this._editingBlocks,baseTemperature:this._editingBaseTemperature},bubbles:!0,composed:!0}))}render(){return this.open&&this._editingWeekday?F`
      <ha-dialog
        open
        @closed=${this._closeEditor}
        .heading=${this._formatEdit(this._editingWeekday)}
      >
        <div class="dialog-content">
          <!-- Weekday selector tabs -->
          <div class="weekday-tabs">
            ${ut.map(t=>F`
                <button
                  class="weekday-tab ${t===this._editingWeekday?"active":""}"
                  @click=${()=>this._switchToWeekday(t)}
                >
                  ${this._getWeekdayLabel(t,"short")}
                </button>
              `)}
          </div>

          <!-- Editor content in dialog -->
          <div class="dialog-editor">${this._renderEditor()}</div>
        </div>
      </ha-dialog>
    `:F``}_formatEdit(t){return(this.translations?.edit??"Edit {weekday}").replace("{weekday}",this._getWeekdayLabel(t,"long"))}_renderEditor(){if(!this._editingWeekday||!this._editingBlocks)return F``;const t=void 0!==this._editingBaseTemperature?St(this._editingBlocks,this._editingBaseTemperature):this._editingBlocks;return F`
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
              .label=${"Close"}
            ></ha-icon-button>
          </div>
        </div>

        ${this._validationWarnings.length>0?F`
              <ha-alert alert-type="warning" .title=${this.translations?.warningsTitle??""}>
                <ul class="warnings-list">
                  ${this._validationWarnings.map(t=>F`<li class="warning-item">
                        ${this._translateValidationMessage(t)}
                      </li>`)}
                </ul>
              </ha-alert>
            `:""}

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
              @change=${t=>{this._saveHistoryState(),this._editingBaseTemperature=parseFloat(t.target.value),this.requestUpdate()}}
            />
            <span class="temp-unit">${this.temperatureUnit}</span>
            <div
              class="color-indicator"
              style="background-color: ${bt(this._editingBaseTemperature||20)}"
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
          ${t.map((e,i)=>{const s=this._editingBlocks.findIndex(t=>t.startMinutes===e.startMinutes&&t.endMinutes===e.endMinutes),a=!(-1!==s);return void 0!==this._editingSlotIndex&&this._editingSlotIndex===s&&void 0!==this._editingSlotData&&this._editingSlotData?F`
                <div class="time-block-editor editing">
                  <input
                    type="time"
                    class="time-input"
                    .value=${this._editingSlotData.startTime}
                    @change=${t=>{this._editingSlotData&&(this._editingSlotData={...this._editingSlotData,startTime:t.target.value},this.requestUpdate())}}
                  />
                  <input
                    type="time"
                    class="time-input"
                    .value=${"24:00"===this._editingSlotData.endTime?"23:59":this._editingSlotData.endTime}
                    @change=${t=>{if(this._editingSlotData){let e=t.target.value;"23:59"===e&&(e="24:00"),this._editingSlotData={...this._editingSlotData,endTime:e},this.requestUpdate()}}}
                  />
                  <div class="temp-input-group">
                    <input
                      type="number"
                      class="temp-input"
                      .value=${this._editingSlotData.temperature.toString()}
                      step=${this.tempStep}
                      min=${this.minTemp}
                      max=${this.maxTemp}
                      @change=${t=>{this._editingSlotData&&(this._editingSlotData={...this._editingSlotData,temperature:parseFloat(t.target.value)},this.requestUpdate())}}
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
                    style="background-color: ${bt(this._editingSlotData.temperature)}"
                  ></div>
                </div>
              `:F`
              <div class="time-block-editor ${a?"base-temp-slot":""}">
                <span class="time-display">${this._formatTimeDisplay(e.startTime)}</span>
                <span class="time-display">${this._formatTimeDisplay(e.endTime)}</span>
                <div class="temp-display-group">
                  <span class="temp-display">${e.temperature.toFixed(1)}</span>
                  <span class="temp-unit">${this.temperatureUnit}</span>
                </div>
                <div class="slot-actions">
                  ${a?F``:F`
                        <ha-button
                          @click=${()=>this._startSlotEditFromDisplay(i,t)}
                          .disabled=${void 0!==this._editingSlotIndex}
                        >
                          ${this.translations?.editSlot??"Edit"}
                        </ha-button>
                        <ha-icon-button
                          class="remove-btn"
                          .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                          @click=${()=>this._removeTimeBlockByIndex(i,t)}
                          .disabled=${void 0!==this._editingSlotIndex}
                        ></ha-icon-button>
                      `}
                </div>
                <div
                  class="color-indicator"
                  style="background-color: ${bt(e.temperature)}"
                ></div>
              </div>
            `})}
          ${this._editingBlocks.length<12&&void 0===this._editingSlotIndex?F`
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
    `}static{this.styles=Gt}};Qt([ht({type:Boolean})],Xt.prototype,"open",void 0),Qt([ht({type:String})],Xt.prototype,"weekday",void 0),Qt([ht({attribute:!1})],Xt.prototype,"scheduleData",void 0),Qt([ht({type:Number})],Xt.prototype,"minTemp",void 0),Qt([ht({type:Number})],Xt.prototype,"maxTemp",void 0),Qt([ht({type:Number})],Xt.prototype,"tempStep",void 0),Qt([ht({type:String})],Xt.prototype,"temperatureUnit",void 0),Qt([ht({type:String})],Xt.prototype,"hourFormat",void 0),Qt([ht({attribute:!1})],Xt.prototype,"translations",void 0),Qt([pt()],Xt.prototype,"_editingWeekday",void 0),Qt([pt()],Xt.prototype,"_editingBlocks",void 0),Qt([pt()],Xt.prototype,"_editingBaseTemperature",void 0),Qt([pt()],Xt.prototype,"_validationWarnings",void 0),Qt([pt()],Xt.prototype,"_editingSlotIndex",void 0),Qt([pt()],Xt.prototype,"_editingSlotData",void 0),Xt=Qt([Bt("hmip-schedule-editor")],Xt);const te=n`
  :host {
    display: block;
  }

  .schedule-list {
    display: flex;
    flex-direction: column;
  }

  .toolbar {
    margin-bottom: 16px;
    display: flex;
    justify-content: flex-end;
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

  /* Touch device optimizations */
  @media (hover: none) and (pointer: coarse) {
    .event-card:hover {
      background-color: transparent;
    }

    .event-card:active {
      background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
    }
  }
`;var ee=function(t,e,i,s){var a,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var r=t.length-1;r>=0;r--)(a=t[r])&&(n=(o<3?a(n):o>3?a(e,i,n):a(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n};let ie=class extends rt{constructor(){super(...arguments),this.editable=!0}static{this.styles=te}_handleAdd(){this.dispatchEvent(new CustomEvent("add-event",{bubbles:!0,composed:!0}))}_handleEdit(t){this.dispatchEvent(new CustomEvent("edit-event",{bubbles:!0,composed:!0,detail:{entry:t}}))}_handleDelete(t){this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:t}}))}_getConditionDisplay(t){return function(t,e,i){const s=function(t,e,i){const s="sunset"===t?i.sunset:i.sunrise;return 0===e?s:`${s} ${e>0?"+":""}${e}min`}(t.astro_type,t.astro_offset_minutes,i),a=t.time;switch(t.condition){case"fixed_time":default:return{label:e,details:a};case"astro":return{label:e,details:s};case"earliest":case"latest":case"astro_if_before_fixed":case"astro_if_after_fixed":return{label:e,details:`${s} / ${a}`};case"fixed_if_before_astro":case"fixed_if_after_astro":return{label:e,details:`${a} / ${s}`}}}(t,this.translations.conditionLabels[t.condition]||t.condition,this.translations.conditionSummaryLabels)}render(){if(!this.scheduleData)return F`<div class="no-data">${this.translations.loading}</div>`;const t=function(t){const e=[];for(const[i,s]of Object.entries(t))e.push({...s,groupNo:i,isActive:Tt(s)});return e.sort((t,e)=>t.time.localeCompare(e.time)),e}(this.scheduleData);return 0===t.length?F`
        <div class="no-data">
          <p>${this.translations.noScheduleEvents}</p>
          ${this.editable?F`<ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>`:""}
        </div>
      `:F`
      <div class="schedule-list">
        ${this.editable?F`<div class="toolbar">
              <ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>
            </div>`:""}
        <div class="events-table">
          ${Yt(t,t=>t.groupNo,t=>this._renderEvent(t))}
        </div>
      </div>
    `}_renderEvent(t){const e=function(t,e,i){const s=e?gt[e]:void 0;if("binary"===s?.levelType){const e=i?.on??"On";return 0===t?i?.off??"Off":e}return`${Math.round(100*t)}%`}(t.level,this.domain,{on:this.translations.levelOn,off:this.translations.levelOff}),i=function(t){if(!t)return"-";const e=Dt(t);return e?`${e.value}${{ms:"ms",s:"s",min:"min",h:"h"}[e.unit]}`:t}(t.duration),{label:s,details:a}=this._getConditionDisplay(t);return F`
      <div class="event-card ${t.isActive?"active":"inactive"}">
        <div class="event-row-top">
          <div class="col-condition">${s}</div>
          ${this.editable?F`<div class="col-actions">
                <ha-icon-button
                  .path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}
                  @click=${()=>this._handleEdit(t)}
                ></ha-icon-button>
                <ha-icon-button
                  .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                  @click=${()=>this._handleDelete(t)}
                ></ha-icon-button>
              </div>`:""}
        </div>
        <div class="event-row-details">
          <span class="col-details-text">${a}</span>
        </div>
        <div class="event-row-bottom">
          <div class="col-weekdays">
            <div class="weekday-badges">
              ${ut.map(e=>{const i=t.weekdays.includes(e);return F`<span class="weekday-badge ${i?"active":"inactive"}"
                  >${this.translations.weekdayShortLabels[e]}</span
                >`})}
            </div>
          </div>
          <div class="col-details">
            <span class="col-state">
              ${e}
              ${null!==t.level_2?F`<span class="level-2"
                    >, ${this.translations.slat}: ${Math.round(100*t.level_2)}%</span
                  >`:""}
            </span>
            ${"-"!==i?F`<span class="col-duration">${i}</span>`:""}
          </div>
        </div>
      </div>
    `}};ee([ht({attribute:!1})],ie.prototype,"scheduleData",void 0),ee([ht({attribute:!1})],ie.prototype,"domain",void 0),ee([ht({type:Boolean})],ie.prototype,"editable",void 0),ee([ht({attribute:!1})],ie.prototype,"translations",void 0),ie=ee([Bt("hmip-device-schedule-list")],ie);const se=n`
  :host {
    display: block;
  }

  /* Dialog styles */
  ha-dialog {
    --ha-dialog-max-width: 500px;
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
`;var ae=function(t,e,i,s){var a,o=arguments.length,n=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var r=t.length-1;r>=0;r--)(a=t[r])&&(n=(o<3?a(n):o>3?a(e,i,n):a(e,i))||n);return o>3&&n&&Object.defineProperty(e,i,n),n};let oe=class extends rt{constructor(){super(...arguments),this.open=!1,this.isNewEvent=!1,this._validationErrors=[]}static{this.styles=se}willUpdate(t){(t.has("open")||t.has("entry"))&&(this.open&&this.entry?(this._editingEntry={...this.entry},this._validationErrors=[]):this.open||(this._editingEntry=void 0,this._validationErrors=[]))}_updateEditingEntry(t){this._editingEntry&&(this._editingEntry={...this._editingEntry,...t},this._validationErrors=[],this.requestUpdate())}_handleClose(){this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_handleSave(){if(!this._editingEntry||void 0===this.groupNo)return;const t=function(t,e){const i=[];(function(t){try{return function(t){const e=t.split(":");if(2!==e.length)throw new Error(`Invalid time format: ${t}`);const i=parseInt(e[0],10),s=parseInt(e[1],10);if(isNaN(i)||isNaN(s)||i<0||i>23||s<0||s>59)throw new Error(`Invalid time values: ${t}`)}(t),!0}catch{return!1}})(t.time)||i.push({field:"time",message:"Time must be in HH:MM format (00:00-23:59)"}),t.weekdays&&0!==t.weekdays.length||i.push({field:"weekdays",message:"At least one weekday must be selected"});const s=e?gt[e]:void 0;return"binary"===s?.levelType?0!==t.level&&1!==t.level&&i.push({field:"level",message:"Level must be 0 or 1 for switch"}):(t.level<0||t.level>1)&&i.push({field:"level",message:"Level must be between 0.0 and 1.0"}),"cover"===e&&null!==t.level_2&&(t.level_2<0||t.level_2>1)&&i.push({field:"level_2",message:"Slat position must be between 0.0 and 1.0"}),At(t.condition)&&(t.astro_offset_minutes<-720||t.astro_offset_minutes>720)&&i.push({field:"astro_offset_minutes",message:"Astro offset must be between -720 and 720 minutes"}),null===t.duration||Pt(t.duration)||i.push({field:"duration",message:"Invalid duration format"}),null===t.ramp_time||Pt(t.ramp_time)||i.push({field:"ramp_time",message:"Invalid ramp time format"}),i}(this._editingEntry,this.domain);t.length>0?this._validationErrors=t.map(t=>`${t.field}: ${t.message}`):this.dispatchEvent(new CustomEvent("save-event",{bubbles:!0,composed:!0,detail:{entry:{...this._editingEntry},groupNo:this.groupNo}}))}render(){return this.open&&this._editingEntry?F`
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
    `:F``}_renderValidationErrors(){return 0===this._validationErrors.length?F``:F`
      <ha-alert alert-type="error">
        <ul class="validation-list">
          ${this._validationErrors.map(t=>F`<li>${t}</li>`)}
        </ul>
      </ha-alert>
    `}_renderTimeFields(){return this._editingEntry?F`
      <div class="form-group">
        <label>${this.translations.time}</label>
        <input
          type="time"
          .value=${this._editingEntry.time}
          @change=${t=>{this._updateEditingEntry({time:t.target.value})}}
        />
      </div>
    `:F``}_renderConditionFields(){if(!this._editingEntry)return F``;const t=At(this._editingEntry.condition);return F`
      <div class="form-group">
        <label>${this.translations.condition}</label>
        <ha-select
          .value=${this._editingEntry.condition}
          .options=${mt.map(t=>({value:t,label:this.translations.conditionLabels[t]||t}))}
          @selected=${t=>{t.stopPropagation();const e=t.detail.value,i={condition:e};"fixed_time"===e?(i.astro_type=null,i.astro_offset_minutes=0):null===this._editingEntry.astro_type&&(i.astro_type="sunrise"),this._updateEditingEntry(i)}}
          @closed=${t=>t.stopPropagation()}
        ></ha-select>
      </div>
      ${t?F`
            <div class="form-group">
              <label>${this.translations.astroSunrise}/${this.translations.astroSunset}</label>
              <ha-select
                .value=${this._editingEntry.astro_type||"sunrise"}
                .options=${[{value:"sunrise",label:this.translations.astroSunrise},{value:"sunset",label:this.translations.astroSunset}]}
                @selected=${t=>{t.stopPropagation(),this._updateEditingEntry({astro_type:t.detail.value})}}
                @closed=${t=>t.stopPropagation()}
              ></ha-select>
            </div>
            <div class="form-group">
              <label>${this.translations.astroOffset}</label>
              <input
                type="number"
                min="-720"
                max="720"
                .value=${String(this._editingEntry.astro_offset_minutes)}
                @input=${t=>{const e=parseInt(t.target.value,10);isNaN(e)||this._updateEditingEntry({astro_offset_minutes:e})}}
              />
            </div>
          `:""}
    `}_renderWeekdayFields(){return this._editingEntry?F`
      <div class="form-group">
        <label>${this.translations.weekdaysLabel}</label>
        <div class="weekday-checkboxes">
          ${ut.map(t=>{const e=this._editingEntry.weekdays.includes(t);return F`
              <label class="checkbox-label">
                <ha-checkbox
                  .checked=${e}
                  @change=${e=>{const i=e.target.checked,s=[...this._editingEntry.weekdays];if(i&&!s.includes(t))s.push(t);else if(!i){const e=s.indexOf(t);e>-1&&s.splice(e,1)}this._updateEditingEntry({weekdays:s})}}
                ></ha-checkbox>
                ${this.translations.weekdayShortLabels[t]}
              </label>
            `})}
        </div>
      </div>
    `:F``}_renderLevelFields(){if(!this._editingEntry)return F``;const t=this.domain?gt[this.domain]:void 0;return F`
      <div class="form-group">
        <label>${this.translations.stateLabel}</label>
        ${"binary"===t?.levelType?F`
              <ha-select
                .value=${String(this._editingEntry.level)}
                .options=${[{value:"0",label:this.translations.levelOff},{value:"1",label:this.translations.levelOn}]}
                @selected=${t=>{t.stopPropagation();const e=parseInt(t.detail.value,10);this._updateEditingEntry({level:e})}}
                @closed=${t=>t.stopPropagation()}
              ></ha-select>
            `:F`
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*this._editingEntry.level)}
                  @change=${t=>{const e=Number(t.target.value);this._updateEditingEntry({level:e/100})}}
                ></ha-slider>
                <span class="slider-value">${Math.round(100*this._editingEntry.level)}%</span>
              </div>
            `}
      </div>
      ${t?.hasLevel2?F`
            <div class="form-group">
              <label>${this.translations.slat}</label>
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*(this._editingEntry.level_2||0))}
                  @change=${t=>{const e=Number(t.target.value);this._updateEditingEntry({level_2:e/100})}}
                ></ha-slider>
                <span class="slider-value"
                  >${Math.round(100*(this._editingEntry.level_2||0))}%</span
                >
              </div>
            </div>
          `:""}
    `}_renderDurationFields(){if(!this._editingEntry)return F``;const t=this.domain?gt[this.domain]:void 0;if(t&&!t.hasDuration)return F``;const e=this._editingEntry.duration?Dt(this._editingEntry.duration):null,i=e?.value??0,s=e?.unit??"s";return F`
      <div class="form-group">
        <label>${this.translations.duration}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${t=>{const e=parseFloat(t.target.value);!isNaN(e)&&e>0?this._updateEditingEntry({duration:Ct(e,s)}):this._updateEditingEntry({duration:null})}}
          />
          <ha-select
            .value=${s}
            .options=${ft.map(t=>({value:t,label:t}))}
            @selected=${t=>{t.stopPropagation(),i>0&&this._updateEditingEntry({duration:Ct(i,t.detail.value)})}}
            @closed=${t=>t.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderRampTimeFields(){if(!this._editingEntry)return F``;const t=this.domain?gt[this.domain]:void 0;if(t&&!t.hasRampTime)return F``;const e=this._editingEntry.ramp_time?Dt(this._editingEntry.ramp_time):null,i=e?.value??0,s=e?.unit??"s";return F`
      <div class="form-group">
        <label>${this.translations.rampTime}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${t=>{const e=parseFloat(t.target.value);!isNaN(e)&&e>0?this._updateEditingEntry({ramp_time:Ct(e,s)}):this._updateEditingEntry({ramp_time:null})}}
          />
          <ha-select
            .value=${s}
            .options=${ft.map(t=>({value:t,label:t}))}
            @selected=${t=>{t.stopPropagation(),i>0&&this._updateEditingEntry({ramp_time:Ct(i,t.detail.value)})}}
            @closed=${t=>t.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderChannelFields(){return this._editingEntry&&this.availableTargetChannels&&Object.keys(this.availableTargetChannels).length>0?F`
        <div class="form-group">
          <label>${this.translations.channels}</label>
          <div class="channel-checkboxes">
            ${Object.entries(this.availableTargetChannels).map(([t,e])=>{const i=this._editingEntry.target_channels.includes(t);return F`
                <label class="checkbox-label">
                  <ha-checkbox
                    .checked=${i}
                    @change=${e=>{const i=e.target.checked,s=[...this._editingEntry.target_channels];if(i&&!s.includes(t))s.push(t);else if(!i){const e=s.indexOf(t);e>-1&&s.splice(e,1)}this._updateEditingEntry({target_channels:s})}}
                  ></ha-checkbox>
                  ${e.name||t}
                </label>
              `})}
          </div>
        </div>
      `:F``}};ae([ht({type:Boolean})],oe.prototype,"open",void 0),ae([ht({attribute:!1})],oe.prototype,"entry",void 0),ae([ht()],oe.prototype,"groupNo",void 0),ae([ht({type:Boolean})],oe.prototype,"isNewEvent",void 0),ae([ht({attribute:!1})],oe.prototype,"domain",void 0),ae([ht({attribute:!1})],oe.prototype,"availableTargetChannels",void 0),ae([ht({attribute:!1})],oe.prototype,"translations",void 0),ae([pt()],oe.prototype,"_editingEntry",void 0),ae([pt()],oe.prototype,"_validationErrors",void 0),oe=ae([Bt("hmip-device-schedule-editor")],oe);const ne={en:{weekdays:{short:{monday:"Mo",tuesday:"Tu",wednesday:"We",thursday:"Th",friday:"Fr",saturday:"Sa",sunday:"Su"},long:{monday:"Monday",tuesday:"Tuesday",wednesday:"Wednesday",thursday:"Thursday",friday:"Friday",saturday:"Saturday",sunday:"Sunday"}},ui:{schedule:"Schedule",loading:"Loading schedule data...",entityNotFound:"Entity {entity} not found",clickToEdit:"Click on a time slot to edit the schedule",edit:"Edit {weekday}",cancel:"Cancel",save:"Save",addTimeBlock:"+ Add Time Block",copySchedule:"Copy schedule",pasteSchedule:"Paste schedule",undo:"Undo",redo:"Redo",undoShortcut:"Undo (Ctrl+Z)",redoShortcut:"Redo (Ctrl+Y)",exportSchedule:"Export",importSchedule:"Import",exportTooltip:"Export schedule to JSON file",importTooltip:"Import schedule from JSON file",exportSuccess:"Schedule exported successfully",importSuccess:"Schedule imported successfully",unsavedChanges:"Unsaved changes",saveAll:"Save all",discard:"Discard",confirmDiscardChanges:"You have unsaved changes. Do you want to discard them?",from:"From",to:"To",baseTemperature:"Base Temperature",baseTemperatureDescription:"Temperature for unscheduled periods",temperaturePeriods:"Temperature Periods",editSlot:"Edit",saveSlot:"Save",cancelSlotEdit:"Cancel",sensorNotSupported:"Sensor entity {entity} does not have a climate schedule type.",noScheduleData:"Entity {entity} does not provide schedule data."},errors:{failedToChangeProfile:"Failed to change profile: {error}",failedToSaveSchedule:"Failed to save schedule: {error}",failedToPasteSchedule:"Failed to paste schedule: {error}",invalidSchedule:"Invalid schedule: {error}",failedToExport:"Failed to export schedule: {error}",failedToImport:"Failed to import schedule: {error}",invalidImportFile:"Invalid file format. Please select a JSON file.",invalidImportFormat:"Invalid JSON format in file.",invalidImportData:"Invalid schedule data: {error}",insufficientPermissions:"You don't have permission to perform this action."},warnings:{title:"Validation Warnings",noWarnings:"No issues detected"},validationMessages:{blockEndBeforeStart:"Block {block}: End time is before start time",blockZeroDuration:"Block {block}: Block has zero duration",invalidStartTime:"Block {block}: Invalid start time",invalidEndTime:"Block {block}: Invalid end time",temperatureOutOfRange:"Block {block}: Temperature out of range ({min}-{max}°C)",invalidSlotCount:"Invalid number of slots: {count} (expected 13)",invalidSlotKey:"Invalid slot key: {key} (must be integer 1-13)",missingSlot:"Missing slot {slot}",slotMissingValues:"Slot {slot} missing ENDTIME or TEMPERATURE",slotTimeBackwards:"Slot {slot} time goes backwards: {time}",slotTimeExceedsDay:"Slot {slot} time exceeds 24:00: {time}",lastSlotMustEnd:"Last slot must end at 24:00",scheduleMustBeObject:"Schedule data must be an object",missingWeekday:"Missing weekday: {weekday}",invalidWeekdayData:"Invalid data for {weekday}",weekdayValidationError:"{weekday}: {details}"}},de:{weekdays:{short:{monday:"Mo",tuesday:"Di",wednesday:"Mi",thursday:"Do",friday:"Fr",saturday:"Sa",sunday:"So"},long:{monday:"Montag",tuesday:"Dienstag",wednesday:"Mittwoch",thursday:"Donnerstag",friday:"Freitag",saturday:"Samstag",sunday:"Sonntag"}},ui:{schedule:"Zeitplan",loading:"Zeitplandaten werden geladen...",entityNotFound:"Entität {entity} nicht gefunden",clickToEdit:"Klicken Sie auf einen Zeitabschnitt, um den Zeitplan zu bearbeiten",edit:"{weekday} bearbeiten",cancel:"Abbrechen",save:"Speichern",addTimeBlock:"+ Zeitblock hinzufügen",copySchedule:"Zeitplan kopieren",pasteSchedule:"Zeitplan einfügen",undo:"Rückgängig",redo:"Wiederholen",undoShortcut:"Rückgängig (Strg+Z)",redoShortcut:"Wiederholen (Strg+Y)",exportSchedule:"Exportieren",importSchedule:"Importieren",exportTooltip:"Zeitplan als JSON-Datei exportieren",importTooltip:"Zeitplan aus JSON-Datei importieren",exportSuccess:"Zeitplan erfolgreich exportiert",importSuccess:"Zeitplan erfolgreich importiert",unsavedChanges:"Ungespeicherte Änderungen",saveAll:"Alle speichern",discard:"Verwerfen",confirmDiscardChanges:"Sie haben ungespeicherte Änderungen. Möchten Sie diese verwerfen?",from:"Von",to:"Bis",baseTemperature:"Basistemperatur",baseTemperatureDescription:"Temperatur für nicht geplante Zeiträume",temperaturePeriods:"Temperaturperioden",editSlot:"Bearbeiten",saveSlot:"Speichern",cancelSlotEdit:"Abbrechen",sensorNotSupported:"Sensor-Entität {entity} hat keinen Klima-Zeitplantyp.",noScheduleData:"Entität {entity} stellt keine Zeitplandaten bereit."},errors:{failedToChangeProfile:"Fehler beim Wechseln des Profils: {error}",failedToSaveSchedule:"Fehler beim Speichern des Zeitplans: {error}",failedToPasteSchedule:"Fehler beim Einfügen des Zeitplans: {error}",invalidSchedule:"Ungültiger Zeitplan: {error}",failedToExport:"Fehler beim Exportieren des Zeitplans: {error}",failedToImport:"Fehler beim Importieren des Zeitplans: {error}",invalidImportFile:"Ungültiges Dateiformat. Bitte wählen Sie eine JSON-Datei.",invalidImportFormat:"Ungültiges JSON-Format in der Datei.",invalidImportData:"Ungültige Zeitplandaten: {error}",insufficientPermissions:"Sie haben keine Berechtigung für diese Aktion."},warnings:{title:"Validierungswarnungen",noWarnings:"Keine Probleme erkannt"},validationMessages:{blockEndBeforeStart:"Block {block}: Die Endzeit liegt vor der Startzeit",blockZeroDuration:"Block {block}: Der Block hat keine Dauer",invalidStartTime:"Block {block}: Ungültige Startzeit",invalidEndTime:"Block {block}: Ungültige Endzeit",temperatureOutOfRange:"Block {block}: Temperatur außerhalb des Bereichs ({min}-{max}°C)",invalidSlotCount:"Ungültige Anzahl an Slots: {count} (erwartet 13)",invalidSlotKey:"Ungültiger Slot-Schlüssel: {key} (muss eine Ganzzahl 1-13 sein)",missingSlot:"Slot {slot} fehlt",slotMissingValues:"Slot {slot} fehlt ENDTIME oder TEMPERATURE",slotTimeBackwards:"Slot {slot}: Zeit läuft rückwärts: {time}",slotTimeExceedsDay:"Slot {slot}: Zeit überschreitet 24:00: {time}",lastSlotMustEnd:"Der letzte Slot muss um 24:00 enden",scheduleMustBeObject:"Zeitplandaten müssen ein Objekt sein",missingWeekday:"Fehlender Wochentag: {weekday}",invalidWeekdayData:"Ungültige Daten für {weekday}",weekdayValidationError:"{weekday}: {details}"}}};function re(t){const e=t.toLowerCase().split("-")[0];return ne[e]||ne.en}function le(t,e){let i=t;for(const[t,s]of Object.entries(e))i=i.replace(`{${t}}`,s);return i}class de extends rt{constructor(){super(...arguments),this._availableProfiles=[],this._userSelectedProfile=!1,this._isLoading=!1,this._translations=re("en"),this._minTemp=5,this._maxTemp=30.5,this._tempStep=.5}static getConfigElement(){return document.createElement("homematicip-local-climate-schedule-card-editor")}static getStubConfig(t){const e=Object.keys(t.states).filter(e=>e.startsWith("climate.")&&void 0!==t.states[e].attributes?.schedule_data);return{type:"custom:homematicip-local-climate-schedule-card",entities:e.length>0?[e[0]]:[]}}get _isEditable(){return this._config?.editable??!0}setConfig(t){const e=[],i=t=>{if(!t)return;const i=t.trim();i&&(e.includes(i)||e.push(i))};if(i(t.entity),Array.isArray(t.entities)&&t.entities.forEach(t=>{i("string"==typeof t?t:t.entity)}),0===e.length)throw new Error("You need to define at least one entity");e.sort((t,e)=>t.localeCompare(e));const s=this._activeEntityId,a=e[0],o=s&&e.includes(s)?s:a;this._config={show_profile_selector:!0,editable:!0,show_temperature:!0,temperature_unit:"°C",hour_format:"24",...t,entity:a},this._activeEntityId=o,this._copiedSchedule=void 0,this._editingWeekday=void 0,this._updateLanguage()}_getPreferredLanguage(t){return t?.language||t?.locale?.language}_updateLanguage(){let t="en";if(this._config?.language)t=this._config.language;else{const e=this._getPreferredLanguage(this.hass);e&&(t=e)}this._translations=re(t),this._weekdayShortLabelMap=this._createWeekdayLabelMap("short"),this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")}_createWeekdayLabelMap(t){const e="short"===t?this._translations.weekdays.short:this._translations.weekdays.long;return{MONDAY:e.monday,TUESDAY:e.tuesday,WEDNESDAY:e.wednesday,THURSDAY:e.thursday,FRIDAY:e.friday,SATURDAY:e.saturday,SUNDAY:e.sunday}}_getWeekdayLabel(t,e="short"){return"long"===e?(this._weekdayLongLabelMap||(this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")),this._weekdayLongLabelMap[t]):(this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),this._weekdayShortLabelMap[t])}_getEntityId(t){return"string"==typeof t?t:t.entity}_getEntityOptions(){return this._config?this._config.entities?.length?this._config.entities.map(t=>this._getEntityId(t)).sort((t,e)=>t.localeCompare(e)):this._config.entity?[this._config.entity]:[]:[]}_getEntityDisplayName(t){if(this._config?.entities?.length){const e=this._config.entities.find(e=>this._getEntityId(e)===t);if(e&&"string"!=typeof e&&e.name)return e.name}return this.hass?.states?.[t]?.attributes.friendly_name||t}_getProfileDisplayName(t){const e=this._getActiveEntityId();if(e&&this._config?.entities?.length){const i=this._config.entities.find(t=>this._getEntityId(t)===e);if(i&&"string"!=typeof i&&i.profile_names?.[t])return`${t} - ${i.profile_names[t]}`}return t}_getActiveEntityId(){const t=this._getEntityOptions();if(0!==t.length)return this._activeEntityId&&t.includes(this._activeEntityId)?this._activeEntityId:t[0]}_needsManualReload(t){if(!t||!this.hass)return!1;const e=this.hass.states[t];if(!e?.attributes?.interface_id)return!1;const i=e.attributes.interface_id;return i.endsWith("BidCos-RF")||i.endsWith("BidCos-Wired")||i.endsWith("VirtualDevices")}_getDeviceAddress(t){const e=this.hass?.states[t];return function(t){if(!t)return;const e=t.split(":");return 2===e.length?e[0]:void 0}(e?.attributes?.address)}_requireDeviceAddress(t){const e=this._getDeviceAddress(t);if(!e)throw new Error(`Cannot resolve device_address for entity ${t}. Ensure the entity has a valid address attribute (format: "device_address:channel").`);return e}_requireConfigEntryId(t){const e=this.hass?.states[t],i=e?.attributes?.config_entry_id;if(!i)throw new Error(`Cannot resolve config_entry_id for entity ${t}. Ensure the entity has a valid config_entry_id attribute.`);return i}async _callSetActiveProfile(t,e){const i=this._requireConfigEntryId(t),s=this._requireDeviceAddress(t);await async function(t,e,i,s){return t.callWS({type:"homematicip_local/config/set_climate_active_profile",entry_id:e,device_address:i,profile:s})}(this.hass,i,s,e)}async _callSetScheduleWeekday(t,e,i,s,a){const o=this._requireConfigEntryId(t),n=this._requireDeviceAddress(t);await async function(t,e,i,s,a,o,n){return t.callWS({type:"homematicip_local/config/set_climate_schedule_weekday",entry_id:e,device_address:i,profile:s,weekday:a,base_temperature:o,simple_weekday_list:n})}(this.hass,o,n,e,i,s,a)}_scheduleReloadDeviceConfig(t){if(!this.hass)return;const e=this._getDeviceAddress(t);if(!e)return;const i=this.hass.states[t],s=i?.attributes?.config_entry_id;s&&setTimeout(async()=>{try{await async function(t,e,i){return t.callWS({type:"homematicip_local/config/reload_device_config",entry_id:e,device_address:i})}(this.hass,s,e)}catch{}},5e3)}_formatValidationParams(t){if(!t)return{};const e={};for(const[i,s]of Object.entries(t))"weekday"===i&&ut.includes(s)?e.weekday=this._getWeekdayLabel(s,"long"):e[i]=s;return e}_translateValidationMessage(t){const e=this._translations.validationMessages[t.key]||t.key,i=this._formatValidationParams(t.params);return t.nested&&(i.details=this._translateValidationMessage(t.nested)),le(e,i)}getCardSize(){return 12}willUpdate(t){if(super.willUpdate(t),t.has("hass")&&this._config){this._updateFromEntity();const e=t.get("hass");this._getPreferredLanguage(this.hass)!==this._getPreferredLanguage(e)&&this._updateLanguage()}}connectedCallback(){super.connectedCallback()}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0)}_updateFromEntity(){if(!this.hass||!this._config)return;const t=this._getActiveEntityId();if(!t)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const e=this.hass.states?.[t];if(!e)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const i=e.attributes;if(t.startsWith("sensor.")&&"climate"!==i.schedule_type)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);if(!i.schedule_data)return this._currentProfile=void 0,this._activeDeviceProfile=void 0,this._scheduleData=void 0,void(this._availableProfiles=[]);const s=function(t){if(null!=t)return`P${t}`}(i.device_active_profile_index);void 0!==s&&void 0!==this._activeDeviceProfile&&s!==this._activeDeviceProfile&&(this._userSelectedProfile=!1,this._reloadScheduleData(t,s)),this._activeDeviceProfile=s,this._userSelectedProfile||(this._currentProfile=this._config.profile||s||i.current_schedule_profile||i.active_profile),this._scheduleData=i.schedule_data,this._availableProfiles=(i.available_profiles||[]).slice().sort((t,e)=>t.localeCompare(e)),this._minTemp=i.min_temp??5,this._maxTemp=i.max_temp??30.5,this._tempStep=i.target_temp_step??.5,this._lastScheduleDataHash=i.schedule_data?JSON.stringify(i.schedule_data):void 0}_reloadScheduleData(t,e){this.hass&&this._callSetActiveProfile(t,e).catch(()=>{})}async _handleProfileChange(t){t.stopPropagation();const e=t.detail.value,i=this._getActiveEntityId();if(this._config&&this.hass&&i){this._userSelectedProfile=!0;try{await this._callSetActiveProfile(i,e),this._currentProfile=e}catch(t){const e=String(t);e.includes("unauthorized")||e.includes("Unauthorized")?alert(this._translations.errors.insufficientPermissions):alert(le(this._translations.errors.failedToChangeProfile,{error:e}))}}}_onWeekdayClick(t){this._isEditable&&this._scheduleData&&(this._editingWeekday=t.detail.weekday)}_onCopySchedule(t){const e=t.detail.weekday;if(!this._scheduleData)return;const i=this._getParsedBlocks(e);let s;const a=this._scheduleData[e];s=a?xt(a).baseTemperature:kt(i),this._copiedSchedule={weekday:e,blocks:JSON.parse(JSON.stringify(i)),baseTemperature:s}}async _onPasteSchedule(t){if(!this._isEditable)return;const e=t.detail.weekday;if(!(this._config&&this.hass&&this._currentProfile&&this._copiedSchedule))return;const i=this._getActiveEntityId();if(!i)return;const s=this._copiedSchedule.baseTemperature??kt(this._copiedSchedule.blocks),a=$t(this._copiedSchedule.blocks,s),o=It(a,this._minTemp,this._maxTemp);if(o){const t=this._translateValidationMessage(o);return void alert(le(this._translations.errors.invalidSchedule,{error:t}))}this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const{base_temperature:t,periods:s}=a;await this._callSetScheduleWeekday(i,this._currentProfile,e,t,s),this._scheduleData&&(this._scheduleData={...this._scheduleData,[e]:a}),this._updateFromEntity(),this.requestUpdate(),this._needsManualReload(i)&&this._scheduleReloadDeviceConfig(i)}catch(t){const e=String(t);e.includes("unauthorized")||e.includes("Unauthorized")?alert(this._translations.errors.insufficientPermissions):alert(le(this._translations.errors.failedToPasteSchedule,{error:e}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}async _onSaveSchedule(t){if(!this._config||!this.hass||!this._currentProfile)return;const e=this._getActiveEntityId();if(!e)return;const{weekday:i,blocks:s,baseTemperature:a}=t.detail,o=$t(s,a),n=It(o,this._minTemp,this._maxTemp);if(n){const t=this._translateValidationMessage(n);return void alert(le(this._translations.errors.invalidSchedule,{error:t}))}this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const{base_temperature:t,periods:s}=o;await this._callSetScheduleWeekday(e,this._currentProfile,i,t,s),this._scheduleData&&(this._scheduleData={...this._scheduleData,[i]:o}),this._updateFromEntity(),this.requestUpdate(),this._editingWeekday=void 0,this._needsManualReload(e)&&this._scheduleReloadDeviceConfig(e)}catch(t){const e=String(t);e.includes("unauthorized")||e.includes("Unauthorized")?alert(this._translations.errors.insufficientPermissions):alert(le(this._translations.errors.failedToSaveSchedule,{error:e}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}_onValidationFailed(t){alert(le(this._translations.errors.invalidSchedule,{error:t.detail.error}))}_onEditorClosed(){this._editingWeekday=void 0}_getParsedBlocks(t){if(this._scheduleData){const e=this._scheduleData[t];if(!e)return[];const{blocks:i}=xt(e);return i}return[]}_exportSchedule(){if(this._currentProfile&&this._scheduleData)try{const t={version:"2.0",profile:this._currentProfile,exported:(new Date).toISOString(),scheduleData:this._scheduleData,format:"simple"},e=JSON.stringify(t,null,2),i=new Blob([e],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s,a.download=`schedule-${this._currentProfile}-${(new Date).toISOString().split("T")[0]}.json`,document.body.appendChild(a),a.click(),document.body.removeChild(a),URL.revokeObjectURL(s)}catch(t){alert(le(this._translations.errors.failedToExport,{error:String(t)}))}}_importSchedule(){if(!this._isEditable)return;const t=document.createElement("input");t.type="file",t.accept=".json,application/json",t.onchange=async t=>{const e=t.target.files?.[0];if(e)if(e.name.endsWith(".json")||"application/json"===e.type)try{const t=await e.text();let i,s;try{i=JSON.parse(t)}catch{return void alert(this._translations.errors.invalidImportFormat)}if(!i||"object"!=typeof i)return void alert(this._translations.errors.invalidImportFormat);s="scheduleData"in i?i.scheduleData:i;const a=function(t){if(!t||"object"!=typeof t)return{key:"scheduleMustBeObject"};const e=t,i=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"];for(const t of i){if(!(t in e))return{key:"missingWeekday",params:{weekday:t}};const i=e[t];if(!i||"object"!=typeof i)return{key:"invalidWeekdayData",params:{weekday:t}};if(!("base_temperature"in i)||!("periods"in i))return{key:"invalidWeekdayData",params:{weekday:t}};const s=It(i);if(s)return{key:"weekdayValidationError",params:{weekday:t},nested:s}}return null}(s);if(a){const t=this._translateValidationMessage(a);return void alert(le(this._translations.errors.invalidImportData,{error:t}))}const o=this._getActiveEntityId();if(!(this._config&&this.hass&&this._currentProfile&&o))return;this._isLoading=!0,this._loadingTimeoutId=window.setTimeout(()=>{this._isLoading=!1,this._loadingTimeoutId=void 0},1e4);try{const t=s;for(const e of ut){const i=t[e];if(i){const{base_temperature:t,periods:s}=i;await this._callSetScheduleWeekday(o,this._currentProfile,e,t,s)}}this._scheduleData=t,this._updateFromEntity(),this.requestUpdate(),alert(this._translations.ui.importSuccess),this._needsManualReload(o)&&this._scheduleReloadDeviceConfig(o)}catch(t){alert(le(this._translations.errors.failedToImport,{error:String(t)}))}finally{void 0!==this._loadingTimeoutId&&(clearTimeout(this._loadingTimeoutId),this._loadingTimeoutId=void 0),this._isLoading=!1}}catch(t){alert(le(this._translations.errors.failedToImport,{error:String(t)}))}else alert(this._translations.errors.invalidImportFile)},t.click()}_buildGridTranslations(){return this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),{weekdayShortLabels:this._weekdayShortLabelMap,clickToEdit:this._translations.ui.clickToEdit,copySchedule:this._translations.ui.copySchedule,pasteSchedule:this._translations.ui.pasteSchedule}}_buildEditorTranslations(){return this._weekdayShortLabelMap||(this._weekdayShortLabelMap=this._createWeekdayLabelMap("short")),this._weekdayLongLabelMap||(this._weekdayLongLabelMap=this._createWeekdayLabelMap("long")),{weekdayShortLabels:this._weekdayShortLabelMap,weekdayLongLabels:this._weekdayLongLabelMap,edit:this._translations.ui.edit,cancel:this._translations.ui.cancel,save:this._translations.ui.save,addTimeBlock:this._translations.ui.addTimeBlock,from:this._translations.ui.from,to:this._translations.ui.to,baseTemperature:this._translations.ui.baseTemperature,baseTemperatureDescription:this._translations.ui.baseTemperatureDescription,temperaturePeriods:this._translations.ui.temperaturePeriods,editSlot:this._translations.ui.editSlot,saveSlot:this._translations.ui.saveSlot,cancelSlotEdit:this._translations.ui.cancelSlotEdit,undoShortcut:this._translations.ui.undoShortcut,redoShortcut:this._translations.ui.redoShortcut,warningsTitle:this._translations.warnings.title,validationMessages:this._translations.validationMessages}}_renderEntitySelector(t,e){const i=e&&t.includes(e)?e:t[0];return F`
      <ha-select
        class="entity-selector"
        .value=${i}
        .options=${[...t].sort((t,e)=>t.localeCompare(e)).map(t=>({value:t,label:this._getEntityDisplayName(t)}))}
        @selected=${this._handleEntitySelection}
        @closed=${t=>t.stopPropagation()}
      ></ha-select>
    `}_handleEntitySelection(t){t.stopPropagation();const e=t.detail.value;e&&e!==this._getActiveEntityId()&&(this._activeEntityId=e,this._editingWeekday=void 0,this._copiedSchedule=void 0,this._userSelectedProfile=!1,this._updateFromEntity())}render(){if(!this._config||!this.hass)return F``;const t=this._getEntityOptions(),e=t.length>1,i=this._getActiveEntityId(),s=i?this.hass.states?.[i]:void 0,a=this._config.name||(i?this._getEntityDisplayName(i):null)||this._translations.ui.schedule;return s?i?.startsWith("sensor.")&&"climate"!==s.attributes.schedule_type?F`
          <ha-card>
            <div class="card-header">
              <div class="name">${a}</div>
            </div>
            <div class="card-content">
              <div class="error">
                ${le(this._translations.ui.sensorNotSupported,{entity:i})}
              </div>
            </div>
          </ha-card>
        `:s.attributes.schedule_data?F`
      <ha-card>
        <div class="card-header">
          <div class="name">${a}</div>
        </div>
        <div class="header-controls">
          ${e?this._renderEntitySelector(t,i):""}
          ${this._config.show_profile_selector&&this._availableProfiles.length>0?F`
                <ha-select
                  class="profile-selector"
                  .value=${this._currentProfile||""}
                  .options=${this._availableProfiles.map(t=>({value:t,label:(t===this._activeDeviceProfile?"* ":"")+this._getProfileDisplayName(t)}))}
                  @selected=${this._handleProfileChange}
                  @closed=${t=>t.stopPropagation()}
                ></ha-select>
              `:""}
          <ha-icon-button
            .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
            @click=${this._exportSchedule}
            .label=${this._translations.ui.exportTooltip}
            .disabled=${!this._scheduleData}
          ></ha-icon-button>
          ${this._isEditable?F`<ha-icon-button
                .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
                @click=${this._importSchedule}
                .label=${this._translations.ui.importTooltip}
              ></ha-icon-button>`:""}
        </div>

        <div class="card-content">
          ${this._scheduleData?F`
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
              `:F`<div class="loading">${this._translations.ui.loading}</div>`}
        </div>

        ${this._isLoading?F`
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
    `:F`
        <ha-card>
          <div class="card-header">
            <div class="name">${a}</div>
          </div>
          <div class="card-content">
            <div class="error">
              ${le(this._translations.ui.noScheduleData,{entity:i||""})}
            </div>
          </div>
        </ha-card>
      `:F`
        <ha-card>
          <div class="card-header">
            <div class="name">${a}</div>
          </div>
          <div class="card-content">
            <div class="error">
              ${le(this._translations.ui.entityNotFound,{entity:i||this._translations.ui.schedule})}
            </div>
          </div>
        </ha-card>
      `}static get styles(){return n`
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
        opacity: 0.3;
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
    `}}t([ht({attribute:!1})],de.prototype,"hass",void 0),t([pt()],de.prototype,"_config",void 0),t([pt()],de.prototype,"_currentProfile",void 0),t([pt()],de.prototype,"_activeDeviceProfile",void 0),t([pt()],de.prototype,"_scheduleData",void 0),t([pt()],de.prototype,"_availableProfiles",void 0),t([pt()],de.prototype,"_activeEntityId",void 0),t([pt()],de.prototype,"_editingWeekday",void 0),t([pt()],de.prototype,"_copiedSchedule",void 0),t([pt()],de.prototype,"_isLoading",void 0),t([pt()],de.prototype,"_translations",void 0),t([pt()],de.prototype,"_minTemp",void 0),t([pt()],de.prototype,"_maxTemp",void 0),t([pt()],de.prototype,"_tempStep",void 0);const ce="homematicip-local-climate-schedule-card";customElements.get(ce)||customElements.define(ce,de),window.customCards=window.customCards||[],window.customCards.some(t=>t.type===ce)||window.customCards.push({type:ce,name:"Homematic(IP) Local Climate Schedule Card",description:"Display and edit Homematic thermostat schedules",preview:!0});export{de as HomematicScheduleCard};
