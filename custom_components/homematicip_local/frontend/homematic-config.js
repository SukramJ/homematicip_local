function e(e,t,i,s){var a,r=arguments.length,n=r<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n}"function"==typeof SuppressedError&&SuppressedError;const t=globalThis,i=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),a=new WeakMap;let r=class{constructor(e,t,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(i&&void 0===e){const i=void 0!==t&&1===t.length;i&&(e=a.get(t)),void 0===e&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),i&&a.set(t,e))}return e}toString(){return this.cssText}};const n=(e,...t)=>{const i=1===e.length?e[0]:t.reduce((t,i,s)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[s+1],e[0]);return new r(i,e,s)},o=i?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>new r("string"==typeof e?e:e+"",void 0,s))(t)})(e):e,{is:l,defineProperty:d,getOwnPropertyDescriptor:c,getOwnPropertyNames:h,getOwnPropertySymbols:p,getPrototypeOf:_}=Object,u=globalThis,v=u.trustedTypes,m=v?v.emptyScript:"",g=u.reactiveElementPolyfillSupport,f=(e,t)=>e,b={toAttribute(e,t){switch(t){case Boolean:e=e?m:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},y=(e,t)=>!l(e,t),x={attribute:!0,type:String,converter:b,reflect:!1,useDefault:!1,hasChanged:y};Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;let $=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=x){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(e,i,t);void 0!==s&&d(this.prototype,e,s)}}static getPropertyDescriptor(e,t,i){const{get:s,set:a}=c(this.prototype,e)??{get(){return this[t]},set(e){this[t]=e}};return{get:s,set(t){const r=s?.call(this);a?.call(this,t),this.requestUpdate(e,r,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??x}static _$Ei(){if(this.hasOwnProperty(f("elementProperties")))return;const e=_(this);e.finalize(),void 0!==e.l&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(f("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(f("properties"))){const e=this.properties,t=[...h(e),...p(e)];for(const i of t)this.createProperty(i,e[i])}const e=this[Symbol.metadata];if(null!==e){const t=litPropertyMetadata.get(e);if(void 0!==t)for(const[e,i]of t)this.elementProperties.set(e,i)}this._$Eh=new Map;for(const[e,t]of this.elementProperties){const i=this._$Eu(e,t);void 0!==i&&this._$Eh.set(i,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(o(e))}else void 0!==e&&t.push(o(e));return t}static _$Eu(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),void 0!==this.renderRoot&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){const e=new Map,t=this.constructor.elementProperties;for(const i of t.keys())this.hasOwnProperty(i)&&(e.set(i,this[i]),delete this[i]);e.size>0&&(this._$Ep=e)}createRenderRoot(){const e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((e,s)=>{if(i)e.adoptedStyleSheets=s.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const i of s){const s=document.createElement("style"),a=t.litNonce;void 0!==a&&s.setAttribute("nonce",a),s.textContent=i.cssText,e.appendChild(s)}})(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,i){this._$AK(e,i)}_$ET(e,t){const i=this.constructor.elementProperties.get(e),s=this.constructor._$Eu(e,i);if(void 0!==s&&!0===i.reflect){const a=(void 0!==i.converter?.toAttribute?i.converter:b).toAttribute(t,i.type);this._$Em=e,null==a?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(e,t){const i=this.constructor,s=i._$Eh.get(e);if(void 0!==s&&this._$Em!==s){const e=i.getPropertyOptions(s),a="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==e.converter?.fromAttribute?e.converter:b;this._$Em=s;const r=a.fromAttribute(t,e.type);this[s]=r??this._$Ej?.get(s)??r,this._$Em=null}}requestUpdate(e,t,i,s=!1,a){if(void 0!==e){const r=this.constructor;if(!1===s&&(a=this[e]),i??=r.getPropertyOptions(e),!((i.hasChanged??y)(a,t)||i.useDefault&&i.reflect&&a===this._$Ej?.get(e)&&!this.hasAttribute(r._$Eu(e,i))))return;this.C(e,t,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(e,t,{useDefault:i,reflect:s,wrapped:a},r){i&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,r??t??this[e]),!0!==a||void 0!==r)||(this._$AL.has(e)||(this.hasUpdated||i||(t=void 0),this._$AL.set(e,t)),!0===s&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[e,t]of this._$Ep)this[e]=t;this._$Ep=void 0}const e=this.constructor.elementProperties;if(e.size>0)for(const[t,i]of e){const{wrapped:e}=i,s=this[t];!0!==e||this._$AL.has(t)||void 0===s||this.C(t,void 0,i,s)}}let e=!1;const t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(e=>e.hostUpdate?.()),this.update(t)):this._$EM()}catch(t){throw e=!1,this._$EM(),t}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(e){}firstUpdated(e){}};$.elementStyles=[],$.shadowRootOptions={mode:"open"},$[f("elementProperties")]=new Map,$[f("finalized")]=new Map,g?.({ReactiveElement:$}),(u.reactiveElementVersions??=[]).push("2.1.2");const k=globalThis,w=e=>e,S=k.trustedTypes,C=S?S.createPolicy("lit-html",{createHTML:e=>e}):void 0,E="$lit$",A=`lit$${Math.random().toFixed(9).slice(2)}$`,I="?"+A,D=`<${I}>`,T=document,M=()=>T.createComment(""),P=e=>null===e||"object"!=typeof e&&"function"!=typeof e,L=Array.isArray,z="[ \t\n\f\r]",N=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,R=/-->/g,V=/>/g,B=RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),U=/'/g,H=/"/g,W=/^(?:script|style|textarea|title)$/i,F=(e,...t)=>({_$litType$:1,strings:e,values:t}),O=Symbol.for("lit-noChange"),j=Symbol.for("lit-nothing"),K=new WeakMap,Y=T.createTreeWalker(T,129);function G(e,t){if(!L(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==C?C.createHTML(t):t}class Z{constructor({strings:e,_$litType$:t},i){let s;this.parts=[];let a=0,r=0;const n=e.length-1,o=this.parts,[l,d]=((e,t)=>{const i=e.length-1,s=[];let a,r=2===t?"<svg>":3===t?"<math>":"",n=N;for(let t=0;t<i;t++){const i=e[t];let o,l,d=-1,c=0;for(;c<i.length&&(n.lastIndex=c,l=n.exec(i),null!==l);)c=n.lastIndex,n===N?"!--"===l[1]?n=R:void 0!==l[1]?n=V:void 0!==l[2]?(W.test(l[2])&&(a=RegExp("</"+l[2],"g")),n=B):void 0!==l[3]&&(n=B):n===B?">"===l[0]?(n=a??N,d=-1):void 0===l[1]?d=-2:(d=n.lastIndex-l[2].length,o=l[1],n=void 0===l[3]?B:'"'===l[3]?H:U):n===H||n===U?n=B:n===R||n===V?n=N:(n=B,a=void 0);const h=n===B&&e[t+1].startsWith("/>")?" ":"";r+=n===N?i+D:d>=0?(s.push(o),i.slice(0,d)+E+i.slice(d)+A+h):i+A+(-2===d?t:h)}return[G(e,r+(e[i]||"<?>")+(2===t?"</svg>":3===t?"</math>":"")),s]})(e,t);if(this.el=Z.createElement(l,i),Y.currentNode=this.el.content,2===t||3===t){const e=this.el.content.firstChild;e.replaceWith(...e.childNodes)}for(;null!==(s=Y.nextNode())&&o.length<n;){if(1===s.nodeType){if(s.hasAttributes())for(const e of s.getAttributeNames())if(e.endsWith(E)){const t=d[r++],i=s.getAttribute(e).split(A),n=/([.?@])?(.*)/.exec(t);o.push({type:1,index:a,name:n[2],strings:i,ctor:"."===n[1]?ee:"?"===n[1]?te:"@"===n[1]?ie:J}),s.removeAttribute(e)}else e.startsWith(A)&&(o.push({type:6,index:a}),s.removeAttribute(e));if(W.test(s.tagName)){const e=s.textContent.split(A),t=e.length-1;if(t>0){s.textContent=S?S.emptyScript:"";for(let i=0;i<t;i++)s.append(e[i],M()),Y.nextNode(),o.push({type:2,index:++a});s.append(e[t],M())}}}else if(8===s.nodeType)if(s.data===I)o.push({type:2,index:a});else{let e=-1;for(;-1!==(e=s.data.indexOf(A,e+1));)o.push({type:7,index:a}),e+=A.length-1}a++}}static createElement(e,t){const i=T.createElement("template");return i.innerHTML=e,i}}function q(e,t,i=e,s){if(t===O)return t;let a=void 0!==s?i._$Co?.[s]:i._$Cl;const r=P(t)?void 0:t._$litDirective$;return a?.constructor!==r&&(a?._$AO?.(!1),void 0===r?a=void 0:(a=new r(e),a._$AT(e,i,s)),void 0!==s?(i._$Co??=[])[s]=a:i._$Cl=a),void 0!==a&&(t=q(e,a._$AS(e,t.values),a,s)),t}class X{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){const{el:{content:t},parts:i}=this._$AD,s=(e?.creationScope??T).importNode(t,!0);Y.currentNode=s;let a=Y.nextNode(),r=0,n=0,o=i[0];for(;void 0!==o;){if(r===o.index){let t;2===o.type?t=new Q(a,a.nextSibling,this,e):1===o.type?t=new o.ctor(a,o.name,o.strings,this,e):6===o.type&&(t=new se(a,this,e)),this._$AV.push(t),o=i[++n]}r!==o?.index&&(a=Y.nextNode(),r++)}return Y.currentNode=T,s}p(e){let t=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(e,i,t),t+=i.strings.length-2):i._$AI(e[t])),t++}}class Q{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,i,s){this.type=2,this._$AH=j,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e?.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=q(this,e,t),P(e)?e===j||null==e||""===e?(this._$AH!==j&&this._$AR(),this._$AH=j):e!==this._$AH&&e!==O&&this._(e):void 0!==e._$litType$?this.$(e):void 0!==e.nodeType?this.T(e):(e=>L(e)||"function"==typeof e?.[Symbol.iterator])(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==j&&P(this._$AH)?this._$AA.nextSibling.data=e:this.T(T.createTextNode(e)),this._$AH=e}$(e){const{values:t,_$litType$:i}=e,s="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=Z.createElement(G(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(t);else{const e=new X(s,this),i=e.u(this.options);e.p(t),this.T(i),this._$AH=e}}_$AC(e){let t=K.get(e.strings);return void 0===t&&K.set(e.strings,t=new Z(e)),t}k(e){L(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let i,s=0;for(const a of e)s===t.length?t.push(i=new Q(this.O(M()),this.O(M()),this,this.options)):i=t[s],i._$AI(a),s++;s<t.length&&(this._$AR(i&&i._$AB.nextSibling,s),t.length=s)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){const t=w(e).nextSibling;w(e).remove(),e=t}}setConnected(e){void 0===this._$AM&&(this._$Cv=e,this._$AP?.(e))}}class J{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,i,s,a){this.type=1,this._$AH=j,this._$AN=void 0,this.element=e,this.name=t,this._$AM=s,this.options=a,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=j}_$AI(e,t=this,i,s){const a=this.strings;let r=!1;if(void 0===a)e=q(this,e,t,0),r=!P(e)||e!==this._$AH&&e!==O,r&&(this._$AH=e);else{const s=e;let n,o;for(e=a[0],n=0;n<a.length-1;n++)o=q(this,s[i+n],t,n),o===O&&(o=this._$AH[n]),r||=!P(o)||o!==this._$AH[n],o===j?e=j:e!==j&&(e+=(o??"")+a[n+1]),this._$AH[n]=o}r&&!s&&this.j(e)}j(e){e===j?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}}class ee extends J{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===j?void 0:e}}class te extends J{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==j)}}class ie extends J{constructor(e,t,i,s,a){super(e,t,i,s,a),this.type=5}_$AI(e,t=this){if((e=q(this,e,t,0)??j)===O)return;const i=this._$AH,s=e===j&&i!==j||e.capture!==i.capture||e.once!==i.once||e.passive!==i.passive,a=e!==j&&(i===j||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}}class se{constructor(e,t,i){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(e){q(this,e)}}const ae={I:Q},re=k.litHtmlPolyfillSupport;re?.(Z,Q),(k.litHtmlVersions??=[]).push("3.3.2");const ne=globalThis;let oe=class extends ${constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,i)=>{const s=i?.renderBefore??t;let a=s._$litPart$;if(void 0===a){const e=i?.renderBefore??null;s._$litPart$=a=new Q(t.insertBefore(M(),e),e,void 0,i??{})}return a._$AI(e),a})(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return O}};oe._$litElement$=!0,oe.finalized=!0,ne.litElementHydrateSupport?.({LitElement:oe});const le=ne.litElementPolyfillSupport;le?.({LitElement:oe}),(ne.litElementVersions??=[]).push("4.2.2");const de={attribute:!0,type:String,converter:b,reflect:!1,hasChanged:y},ce=(e=de,t,i)=>{const{kind:s,metadata:a}=i;let r=globalThis.litPropertyMetadata.get(a);if(void 0===r&&globalThis.litPropertyMetadata.set(a,r=new Map),"setter"===s&&((e=Object.create(e)).wrapped=!0),r.set(i.name,e),"accessor"===s){const{name:s}=i;return{set(i){const a=t.get.call(this);t.set.call(this,i),this.requestUpdate(s,a,e,!0,i)},init(t){return void 0!==t&&this.C(s,void 0,e,t),t}}}if("setter"===s){const{name:s}=i;return function(i){const a=this[s];t.call(this,i),this.requestUpdate(s,a,e,!0,i)}}throw Error("Unsupported decorator location: "+s)};function he(e){return(t,i)=>"object"==typeof i?ce(e,t,i):((e,t,i)=>{const s=t.hasOwnProperty(i);return t.constructor.createProperty(i,e),s?Object.getOwnPropertyDescriptor(t,i):void 0})(e,t,i)}function pe(e){return he({...e,state:!0,attribute:!1})}const _e=e=>(...t)=>({_$litDirective$:e,values:t});let ue=class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,i){this._$Ct=e,this._$AM=t,this._$Ci=i}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}};const{I:ve}=ae,me=e=>e,ge=()=>document.createComment(""),fe=(e,t,i)=>{const s=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=s.insertBefore(ge(),a),r=s.insertBefore(ge(),a);i=new ve(t,r,e,e.options)}else{const t=i._$AB.nextSibling,r=i._$AM,n=r!==e;if(n){let t;i._$AQ?.(e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==r._$AU&&i._$AP(t)}if(t!==a||n){let e=i._$AA;for(;e!==t;){const t=me(e).nextSibling;me(s).insertBefore(e,a),e=t}}}return i},be=(e,t,i=e)=>(e._$AI(t,i),e),ye={},xe=(e,t=ye)=>e._$AH=t,$e=e=>{e._$AR(),e._$AA.remove()},ke=_e(class extends ue{constructor(){super(...arguments),this.key=j}render(e,t){return this.key=e,t}update(e,[t,i]){return t!==this.key&&(xe(e),this.key=t),i}});function we(e){return t=>(customElements.get(e)||customElements.define(e,t),t)}const Se=n`
  :host {
    display: block;
    font-family: var(--paper-font-body1_-_font-family, "Roboto", sans-serif);
    color: var(--primary-text-color);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    font-size: 18px;
    font-weight: 500;
  }

  .card-content {
    padding: 0 16px 16px;
  }

  .device-info {
    color: var(--secondary-text-color);
    font-size: 14px;
    margin-top: 4px;
  }

  .back-button {
    --ha-icon-button-size: 48px;
    --ha-icon-button-icon-size: 24px;
    color: var(--primary-color);
    margin-left: -12px;
    margin-bottom: 4px;
  }

  .loading {
    display: flex;
    justify-content: center;
    padding: 32px;
  }

  .empty-state {
    text-align: center;
    padding: 32px;
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color, #db4437);
    padding: 16px;
  }

  .action-bar {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 16px;
    border-top: 1px solid var(--divider-color);
  }

  .modified-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--primary-color);
    margin-left: 8px;
  }

  .section-header {
    font-size: 16px;
    font-weight: 500;
    padding: 16px 0 8px;
    border-bottom: 1px solid var(--divider-color);
    margin-bottom: 8px;
  }

  .parameter-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    min-height: 48px;
  }

  .parameter-label {
    font-size: 14px;
    flex: 1;
    min-width: 0;
  }

  .parameter-unit {
    color: var(--secondary-text-color);
    font-size: 12px;
    margin-left: 4px;
  }

  .parameter-control {
    flex: 0 0 auto;
    max-width: 280px;
  }

  .validation-error {
    color: var(--error-color, #db4437);
    font-size: 12px;
    margin-top: 4px;
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px;
    padding: 8px 0;
  }

  .status-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
  }

  .status-icon {
    width: 20px;
    text-align: center;
  }

  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 12px;
    white-space: nowrap;
  }
  .badge.success {
    background: rgba(var(--rgb-green, 76, 175, 80), 0.15);
    color: var(--success-color, #4caf50);
  }
  .badge.warning {
    background: rgba(var(--rgb-amber, 255, 152, 0), 0.15);
    color: var(--warning-color, #ff9800);
  }
  .badge.error {
    background: rgba(var(--rgb-red, 244, 67, 54), 0.15);
    color: var(--error-color, #db4437);
  }
  .badge.info {
    background: rgba(var(--rgb-blue, 33, 150, 243), 0.15);
    color: var(--info-color, #2196f3);
  }

  /* ---- Responsive: mobile (< 600px) ---- */
  @media (max-width: 600px) {
    .parameter-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }

    .parameter-control {
      max-width: 100%;
      width: 100%;
    }

    .action-bar {
      flex-direction: column;
      gap: 8px;
    }

    .action-bar ha-button {
      width: 100%;
    }

    .status-grid {
      grid-template-columns: 1fr;
    }

    .action-bar-sticky {
      position: sticky;
      bottom: 0;
      background: var(--card-background-color, #fff);
      z-index: 1;
      box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
    }
  }
`,Ce=new Set(["BidCos-RF","BidCos-Wired","HmIP-RF"]);function Ee(e,t){return`/api/homematicip_local/${e}/device_icon/${t}`}async function Ae(e,t){return(await e.callWS({type:"homematicip_local/config/list_devices",entry_id:t})).devices}async function Ie(e,t,i,s,a="",r="MASTER"){return e.callWS({type:"homematicip_local/config/get_form_schema",entry_id:t,interface_id:i,channel_address:s,channel_type:a,paramset_key:r})}async function De(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/session_open",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}async function Te(e,t,i,s,a,r="MASTER"){return e.callWS({type:"homematicip_local/config/session_set",entry_id:t,channel_address:i,parameter:s,value:a,paramset_key:r})}async function Me(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_discard",entry_id:t,channel_address:i,paramset_key:s})}async function Pe(e,t,i,s,a){return e.callWS({type:"homematicip_local/config/get_link_form_schema",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a})}async function Le(e,t,i,s,a,r){return e.callWS({type:"homematicip_local/config/put_link_paramset",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a,values:r})}async function ze(e,t,i,s,a){try{return await e.callWS({type:"homematicip_local/config/get_link_profiles",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a})}catch{return null}}async function Ne(e,t){return(await e.callWS({type:"homematicip_local/config/list_schedule_devices",entry_id:t})).devices}async function Re(e,t,i,s){return e.callWS({type:"homematicip_local/config/get_climate_schedule",entry_id:t,device_address:i,...s&&{profile:s}})}async function Ve(e,t,i,s,a,r,n){return e.callWS({type:"homematicip_local/config/set_climate_schedule_weekday",entry_id:t,device_address:i,profile:s,weekday:a,base_temperature:r,simple_weekday_list:n})}async function Be(e,t,i,s){return e.callWS({type:"homematicip_local/config/set_device_schedule",entry_id:t,device_address:i,schedule_data:s})}async function Ue(e,t){return e.callWS({type:"homematicip_local/integration/get_system_health",entry_id:t})}async function He(e,t){return(await e.callWS({type:"homematicip_local/integration/get_command_throttle_stats",entry_id:t})).throttle_stats}async function We(e,t,i=50,s){return e.callWS({type:"homematicip_local/integration/get_incidents",entry_id:t,limit:i,...s})}async function Fe(e,t){return e.callWS({type:"homematicip_local/integration/get_device_statistics",entry_id:t})}async function Oe(e,t){return e.callWS({type:"homematicip_local/ccu/get_system_information",entry_id:t})}async function je(e,t){return e.callWS({type:"homematicip_local/ccu/get_install_mode_status",entry_id:t})}async function Ke(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_signal_quality",entry_id:t})).devices}async function Ye(e,t){return e.callWS({type:"homematicip_local/ccu/get_firmware_overview",entry_id:t})}async function Ge(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_inbox_devices",entry_id:t})).devices}async function Ze(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_service_messages",entry_id:t})).messages}async function qe(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_alarm_messages",entry_id:t})).alarms}const Xe={en:{common:{back:"Back",loading:"Loading...",save:"Save",cancel:"Cancel",yes:"Yes",no:"No",retry:"Retry",close:"Close",error_loading:"Failed to load."},device_list:{title:"Homematic Device Configuration",select_ccu:"CCU",select_placeholder:"Select a CCU...",search_placeholder:"Search devices...",no_entry_selected:"Please select a CCU to view devices.",no_entry_hint:"Select a CCU above to view its devices.",no_devices:"No configurable devices found.",channels:"channels",unreachable:"Unreachable",reachable:"Reachable",low_battery:"Low battery",config_pending:"Configuration pending",sort_by:"Sort by",sort_name:"Name",sort_address:"Address",sort_model:"Model"},device_detail:{address:"Address",firmware:"Firmware",channel:"Channel",configure_master:"Configure MASTER",no_master_config:"No MASTER configuration available.",not_found:"Device not found.",yes:"Yes",no:"No",reachable:"Reachable",unreachable:"Unreachable",export:"Export",import:"Import",export_success:"Configuration exported successfully.",export_failed:"Failed to export configuration.",import_confirm_title:"Import Configuration",import_confirm_text:"Import and apply configuration to channel {channel}?",import_success:"Configuration imported successfully.",import_failed:"Failed to import configuration.",import_validation_failed:"Import validation failed.",show_history:"Change History",show_links:"Direct Links",show_schedules:"Schedules",rssi_device:"RSSI Device",rssi_peer:"RSSI Peer",dutycycle:"DC Limit",low_bat:"Low Battery",unreach:"Reachability",config_pending_label:"Config Pending",device_config:"Device Configuration",virtual:"Virtual",copy:"Copy",copied:"Copied to clipboard.",copy_failed:"Failed to copy.",schedule_channel_hint:"Managed via schedules",edit_schedule:"Edit Schedule"},form_parameter:{toggle_on:"On",toggle_off:"Off",custom_value:"Custom value",auto_detect:"Auto-detect",detecting:"Detecting...",detect_failed:"Detection failed"},time_selector:{base:"Base",factor:"Factor",unit:"Time unit",value:"Value",unit_inactive:"Not active",unit_100ms:"100 milliseconds",unit_seconds:"Seconds",unit_5seconds:"5-second steps",unit_10seconds:"10-second steps",unit_minutes:"Minutes",unit_10minutes:"10-minute steps",unit_hours:"Hours",permanent:"Permanent"},channel_config:{save:"Save",saving:"Saving...",discard:"Discard Changes",reset_defaults:"Reset to Defaults",confirm_save_title:"Save Changes",confirm_save_text:"Apply {count} change(s) to the device?",unsaved_title:"Unsaved Changes",unsaved_warning:"You have unsaved changes. Discard them and go back?",save_success:"Changes saved successfully.",save_failed:"Failed to save changes.",validation_failed:"Validation failed. Please check the highlighted fields.",undo:"Undo",redo:"Redo",session_expiring:"Session expiring soon, refreshing automatically...",expert_mode:"Expert mode",expert_mode_hint:"Show advanced parameters"},change_history:{title:"Change History",empty:"No configuration changes recorded.",source_manual_hint:"Changed manually via the configuration UI",source_import_hint:"Applied via a configuration import",source_copy_hint:"Copied from another channel",clear:"Clear History",clear_confirm_title:"Clear History",clear_confirm_text:"Delete all history entries? This cannot be undone.",clear_success:"History cleared ({count} entries removed).",clear_failed:"Failed to clear history.",source_manual:"Manual",source_import:"Import",source_copy:"Copy",parameters_changed:"{count} parameter(s) changed"},device_links:{title:"Direct Links",subtitle:"Direct links for {device}",empty:"No direct links configured.",empty_hint:"Create a new link to connect devices directly.",add_link:"New Link",outgoing:"Outgoing",incoming:"Incoming",configure:"Configure",delete:"Delete",delete_confirm_title:"Delete Link",delete_confirm_text:"Remove the direct link from {sender} to {receiver}? The devices will no longer communicate directly.",delete_success:"Link deleted successfully.",delete_failed:"Failed to delete link.",channel_group:"Channel {channel}",sort_by:"Sort by",sort_channel:"Channel",sort_sender:"Sender",sort_receiver:"Receiver"},link_config:{title:"Link Configuration",sender:"Sender",receiver:"Receiver",save_success:"Link configuration saved.",save_failed:"Failed to save link configuration.",discard:"Discard Changes",confirm_save_title:"Save Link Changes",confirm_save_text:"Apply {count} change(s) to this link?",unsaved_title:"Unsaved Changes",unsaved_warning:"You have unsaved changes. Discard them and go back?",receiver_params:"Receiver Parameters",sender_params:"Sender Parameters",no_params:"No configurable parameters for this link.",profile:"Profile",short_keypress:"Short keypress",long_keypress:"Long keypress",last_value:"Last value",custom_time:"Custom",test_profile:"Test profile",test_profile_success:"Profile applied successfully",test_profile_failed:"Failed to apply profile"},device_schedule:{title:"Schedules",subtitle:"Schedules for {device}",select_device:"Select a device...",no_devices:"No devices with schedule support found.",schedule_type_climate:"Climate",schedule_type_default:"Device",profile:"Profile",active_profile:"Active profile",weekdays:"Mon,Tue,Wed,Thu,Fri,Sat,Sun",weekday_monday:"Monday",weekday_tuesday:"Tuesday",weekday_wednesday:"Wednesday",weekday_thursday:"Thursday",weekday_friday:"Friday",weekday_saturday:"Saturday",weekday_sunday:"Sunday",base_temperature:"Base temperature",temperature:"Temperature",time:"Time",from:"From",to:"To",add_period:"Add period",delete_period:"Delete",save:"Save",saving:"Saving...",save_success:"Schedule saved successfully.",save_failed:"Failed to save schedule.",load_failed:"Failed to load schedule.",reload:"Reload from device",reload_success:"Device configuration reloaded.",reload_failed:"Failed to reload device configuration.",export:"Export",import:"Import",import_confirm_title:"Import Schedule",import_confirm_text:"Import and apply this schedule?",import_success:"Schedule imported.",import_failed:"Failed to import schedule.",no_schedule_data:"No schedule data available.",click_to_edit:"Click on a time slot to edit the schedule",copy_schedule:"Copy schedule",paste_schedule:"Paste schedule",edit:"Edit {weekday}",add_time_block:"+ Add Time Block",edit_slot:"Edit",save_slot:"Save",cancel_slot_edit:"Cancel",remove_slot:"Remove",undo_shortcut:"Undo (Ctrl+Z)",redo_shortcut:"Redo (Ctrl+Y)",warnings_title:"Validation Warnings",base_temperature_description:"Temperature for unscheduled periods",temperature_periods:"Temperature Periods",invalid_schedule:"Invalid schedule: {error}",validation_block_end_before_start:"Block {block}: End time is before start time",validation_block_zero_duration:"Block {block}: Block has zero duration",validation_invalid_start_time:"Block {block}: Invalid start time",validation_invalid_end_time:"Block {block}: Invalid end time",validation_temp_out_of_range:"Block {block}: Temperature out of range ({min}-{max}°C)",validation_invalid_slot_count:"Invalid number of slots: {count} (expected 13)",validation_invalid_slot_key:"Invalid slot key: {key} (must be integer 1-13)",validation_missing_slot:"Missing slot {slot}",validation_slot_missing_values:"Slot {slot} missing ENDTIME or TEMPERATURE",validation_slot_time_backwards:"Slot {slot} time goes backwards: {time}",validation_slot_time_exceeds_day:"Slot {slot} time exceeds 24:00: {time}",validation_last_slot_must_end:"Last slot must end at 24:00",validation_schedule_must_be_object:"Schedule data must be an object",validation_missing_weekday:"Missing weekday: {weekday}",validation_invalid_weekday_data:"Invalid data for {weekday}",validation_weekday_error:"{weekday}: {details}",entries:"{count} entries",max_entries:"Max entries: {max}",level:"Level",duration:"Duration",condition:"Condition",target_channel:"Target channel",add_event:"Add Event",edit_event:"Edit Event",delete_event:"Delete Event",confirm_delete:"Are you sure you want to delete this event?",weekdays_label:"Weekdays",level_on:"On",level_off:"Off",permanent_on:"Permanent",show_more:"Show more",show_less:"Show less",slat:"Slat Position",ramp_time:"Ramp Time",astro_sunrise:"Sunrise",astro_sunset:"Sunset",astro_offset:"Astro Offset (min)",condition_fixed_time:"Fixed Time",condition_astro:"Astro",condition_fixed_if_before_astro:"Fixed if before Astro",condition_astro_if_before_fixed:"Astro if before Fixed",condition_fixed_if_after_astro:"Fixed if after Astro",condition_astro_if_after_fixed:"Astro if after Fixed",condition_earliest:"Earliest",condition_latest:"Latest",or:"or",if_before:"if before",if_after:"if after",device_mode_hint_bsl:"This device supports Switch and Status LED color modes via the CCU WebUI.",device_mode_hint_rgbw:"This device supports RGBW color modes via the CCU WebUI.",device_mode_hint_lock:"This device supports door lock modes via the CCU WebUI.",weekly_program:"Weekly Program",weekly_program_enabled:"Weekly program is active",weekly_program_disabled:"Weekly program is inactive",weekly_program_enable_failed:"Failed to enable/disable weekly program.",weekly_program_enabled_toast:"Weekly program enabled.",weekly_program_disabled_toast:"Weekly program disabled.",lock_mode:"Entry Type",lock_mode_door_lock:"Door Lock Drive",lock_mode_user_permission:"User Permission",lock_action:"Action",lock_action_lock_autorelock_end:"Lock + Auto-Relock end",lock_action_lock_autorelock_start:"Lock + Auto-Relock start",lock_action_unlock_autorelock_end:"Unlock + Auto-Relock end",lock_action_autorelock_end:"Auto-Relock end",lock_permission:"Permission",permission_granted:"Granted",permission_not_granted:"Not granted",schedule_enabled:"Enabled",schedule_disabled:"Disabled"},add_link:{title:"New Direct Link",step_channel:"Step 1/3 — Select Channel",step_peer:"Step 2/3 — Select Partner",step_confirm:"Step 3/3 — Confirm",select_channel:"Select a channel from this device:",select_role:"Role of selected channel:",role_sender:"Sender (sends commands)",role_receiver:"Receiver (receives commands)",search_devices:"Search devices...",no_compatible:"No compatible channels found.",link_name:"Link name (optional)",create:"Create Link",create_success:"Link created successfully.",create_failed:"Failed to create link.",next:"Next",back:"Back"},tabs:{devices:"Devices",integration:"Integration",ccu:"OpenCCU"},integration:{system_health:"System Health",central_state:"Central State",health_score:"Health Score",device_statistics:"Device Statistics",total_devices:"Total Devices",unreachable:"Unreachable",firmware_updatable:"Firmware Updatable",total_short:"total",unreachable_short:"unreachable",radio_levels:"Duty Cycle / Carrier Sense",command_throttle:"Command Throttle",enabled:"Enabled",interval:"Interval",queue_size:"Queue Size",throttled:"Throttled",burst_count:"Burst Count",incidents:"Incidents",no_incidents:"No incidents recorded.",clear_incidents:"Clear Incidents",clear_incidents_title:"Clear Incidents",clear_incidents_text:"Delete all recorded incidents? This cannot be undone.",incidents_cleared:"Incidents cleared.",clear:"Clear",clear_cache:"Clear Cache",clear_cache_title:"Clear Cache",clear_cache_text:"Clear all cached data? The integration will re-fetch data from the CCU.",cache_cleared:"Cache cleared.",actions:"Actions",refresh:"Refresh",action_failed:"Action failed."},ccu:{tab_general:"General",tab_pairing:"Device Pairing",tab_messages:"Messages",tab_signal:"Signal Quality",tab_firmware:"Firmware",no_inbox_devices:"No new devices in inbox.",no_service_messages:"No service messages.",no_alarm_messages:"No alarm messages.",system_information:"System Information",name:"Name",model:"Model",version:"Version",serial:"Serial",hostname:"Hostname",ccu_type:"CCU Type",interfaces:"Interfaces",auth_enabled:"Authentication",backup_exists:"Backup available",hub_messages:"Hub Messages",service_messages:"Service Messages",alarm_messages:"Alarm Messages",inbox:"Inbox",address:"Address",device_type:"Device Type",device_name:"Device Name",accept:"Accept",accept_device_title:"Accept Device",accept_device_text:"Accept device {device} into the system?",accept_device_success:"Device {device} accepted.",message:"Message",msg_type:"Type",timestamp:"Timestamp",counter_label:"Count",acknowledge:"Acknowledge",message_acknowledged:"Message acknowledged.",description:"Description",last_trigger:"Last Trigger",install_mode:"Install Mode",active:"Active",inactive:"Inactive",remaining_seconds:"{seconds}s remaining",activate:"Activate",install_mode_title:"Activate Install Mode",install_mode_text:"Activate install mode for {interface}? The CCU will accept new devices for 60 seconds.",install_mode_activated:"Install mode activated for {interface}.",signal_quality:"Signal Quality",device:"Device",interface:"Interface",reachable:"Reachable",signal:"Signal",battery:"Battery",low:"Low",ok:"OK",firmware_overview:"Firmware Overview",updatable:"updatable",current_fw:"Current",available_fw:"Available",state:"State",refresh_firmware:"Refresh Firmware Data",firmware_refreshed:"Firmware data refreshed.",actions:"Actions",refresh:"Refresh",create_backup:"Create Backup",create_backup_title:"Create CCU Backup",create_backup_text:"Create a backup of the CCU configuration? This may take a moment.",backup_running:"Creating backup...",backup_success:"Backup created: {filename} ({size} MB)",backup_failed:"Failed to create backup.",action_failed:"Action failed.",filter_devices:"Filter devices...",filter_all:"All",filter_result:"{count} of {total} devices",update_firmware:"Update",update_firmware_confirm:"Update firmware for {device}?",update_firmware_success:"Firmware update triggered for {device}",update_firmware_failed:"Firmware update failed"},permissions:{read_only_notice:"You have read-only access. Contact an admin for edit permissions.",schedule_edit_required:"Schedule editing permission required.",device_config_required:"Device configuration permission required.",device_links_required:"Device link management permission required."},config_form:{dst_start:"Start of daylight saving time",dst_end:"End of daylight saving time"},cross_validation:{max_must_be_gte_min:"Maximum must be greater than or equal to minimum.",level_must_be_in_range:"Level must be between minimum and maximum.",hi_must_be_gte_lo:"Upper threshold must be greater than or equal to lower threshold."}},de:{common:{back:"Zurück",loading:"Laden...",save:"Speichern",cancel:"Abbrechen",yes:"Ja",no:"Nein",retry:"Erneut versuchen",close:"Schließen",error_loading:"Fehler beim Laden."},device_list:{title:"Homematic Gerätekonfiguration",select_ccu:"CCU",select_placeholder:"CCU auswählen...",search_placeholder:"Geräte suchen...",no_entry_selected:"Bitte eine CCU auswählen, um Geräte anzuzeigen.",no_entry_hint:"Wählen Sie oben eine CCU aus, um deren Geräte anzuzeigen.",no_devices:"Keine konfigurierbaren Geräte gefunden.",channels:"Kanäle",unreachable:"Nicht erreichbar",reachable:"Erreichbar",low_battery:"Batterie schwach",config_pending:"Konfiguration ausstehend",sort_by:"Sortieren nach",sort_name:"Name",sort_address:"Adresse",sort_model:"Modell"},device_detail:{address:"Adresse",firmware:"Firmware",channel:"Kanal",configure_master:"MASTER konfigurieren",no_master_config:"Keine MASTER-Konfiguration verfügbar.",not_found:"Gerät nicht gefunden.",yes:"Ja",no:"Nein",reachable:"Erreichbar",unreachable:"Nicht erreichbar",export:"Exportieren",import:"Importieren",export_success:"Konfiguration erfolgreich exportiert.",export_failed:"Export der Konfiguration fehlgeschlagen.",import_confirm_title:"Konfiguration importieren",import_confirm_text:"Konfiguration importieren und auf Kanal {channel} anwenden?",import_success:"Konfiguration erfolgreich importiert.",import_failed:"Import der Konfiguration fehlgeschlagen.",import_validation_failed:"Import-Validierung fehlgeschlagen.",show_history:"Änderungsverlauf",show_links:"Direktverknüpfungen",show_schedules:"Zeitpläne",rssi_device:"RSSI Gerät",rssi_peer:"RSSI Peer",dutycycle:"DC-Limit",low_bat:"Batterie schwach",unreach:"Erreichbarkeit",config_pending_label:"Konfig. ausstehend",device_config:"Gerätekonfiguration",virtual:"Virtuell",copy:"Kopieren",copied:"In die Zwischenablage kopiert.",copy_failed:"Kopieren fehlgeschlagen.",schedule_channel_hint:"Wird über Zeitpläne verwaltet",edit_schedule:"Zeitplan bearbeiten"},form_parameter:{toggle_on:"Ein",toggle_off:"Aus",custom_value:"Wert eingeben",auto_detect:"Auto-Erkennung",detecting:"Erkennung läuft...",detect_failed:"Erkennung fehlgeschlagen"},time_selector:{base:"Basis",factor:"Faktor",unit:"Zeiteinheit",value:"Wert",unit_inactive:"Nicht aktiv",unit_100ms:"100 Millisekunden",unit_seconds:"Sekunden",unit_5seconds:"5-Sekunden-Schritte",unit_10seconds:"10-Sekunden-Schritte",unit_minutes:"Minuten",unit_10minutes:"10-Minuten-Schritte",unit_hours:"Stunden",permanent:"Dauerhaft"},channel_config:{save:"Speichern",saving:"Speichern...",discard:"Änderungen verwerfen",reset_defaults:"Standardwerte laden",confirm_save_title:"Änderungen speichern",confirm_save_text:"{count} Änderung(en) auf das Gerät anwenden?",unsaved_title:"Ungespeicherte Änderungen",unsaved_warning:"Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",save_success:"Änderungen erfolgreich gespeichert.",save_failed:"Fehler beim Speichern der Änderungen.",validation_failed:"Validierung fehlgeschlagen. Bitte die markierten Felder prüfen.",undo:"Rückgängig",redo:"Wiederherstellen",session_expiring:"Sitzung läuft bald ab, wird automatisch erneuert...",expert_mode:"Expertenmodus",expert_mode_hint:"Erweiterte Parameter anzeigen"},change_history:{title:"Änderungsverlauf",empty:"Keine Konfigurationsänderungen aufgezeichnet.",source_manual_hint:"Manuell über die Konfigurationsoberfläche geändert",source_import_hint:"Über einen Konfigurationsimport eingespielt",source_copy_hint:"Von einem anderen Kanal kopiert",clear:"Verlauf löschen",clear_confirm_title:"Verlauf löschen",clear_confirm_text:"Alle Verlaufseinträge löschen? Dies kann nicht rückgängig gemacht werden.",clear_success:"Verlauf gelöscht ({count} Einträge entfernt).",clear_failed:"Fehler beim Löschen des Verlaufs.",source_manual:"Manuell",source_import:"Import",source_copy:"Kopie",parameters_changed:"{count} Parameter geändert"},device_links:{title:"Direktverknüpfungen",subtitle:"Direktverknüpfungen für {device}",empty:"Keine Direktverknüpfungen konfiguriert.",empty_hint:"Erstellen Sie eine neue Verknüpfung, um Geräte direkt miteinander zu verbinden.",add_link:"Neue Verknüpfung",outgoing:"Ausgehend",incoming:"Eingehend",configure:"Konfigurieren",delete:"Löschen",delete_confirm_title:"Verknüpfung löschen",delete_confirm_text:"Direktverknüpfung von {sender} nach {receiver} entfernen? Die Geräte kommunizieren dann nicht mehr direkt.",delete_success:"Verknüpfung erfolgreich gelöscht.",delete_failed:"Fehler beim Löschen der Verknüpfung.",channel_group:"Kanal {channel}",sort_by:"Sortieren nach",sort_channel:"Kanal",sort_sender:"Sender",sort_receiver:"Empfänger"},link_config:{title:"Link-Konfiguration",sender:"Sender",receiver:"Empfänger",save_success:"Link-Konfiguration gespeichert.",save_failed:"Fehler beim Speichern der Link-Konfiguration.",discard:"Änderungen verwerfen",confirm_save_title:"Link-Änderungen speichern",confirm_save_text:"{count} Änderung(en) auf diese Verknüpfung anwenden?",unsaved_title:"Ungespeicherte Änderungen",unsaved_warning:"Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",receiver_params:"Empfänger-Parameter",sender_params:"Sender-Parameter",no_params:"Keine konfigurierbaren Parameter für diese Verknüpfung.",profile:"Profil",short_keypress:"Kurzer Tastendruck",long_keypress:"Langer Tastendruck",last_value:"Letzter Wert",custom_time:"Benutzerdefiniert",test_profile:"Profil testen",test_profile_success:"Profil erfolgreich angewendet",test_profile_failed:"Profil konnte nicht angewendet werden"},device_schedule:{title:"Zeitpläne",subtitle:"Zeitpläne für {device}",select_device:"Gerät auswählen...",no_devices:"Keine Geräte mit Zeitplan-Unterstützung gefunden.",schedule_type_climate:"Heizung",schedule_type_default:"Gerät",profile:"Profil",active_profile:"Aktives Profil",weekdays:"Mo,Di,Mi,Do,Fr,Sa,So",weekday_monday:"Montag",weekday_tuesday:"Dienstag",weekday_wednesday:"Mittwoch",weekday_thursday:"Donnerstag",weekday_friday:"Freitag",weekday_saturday:"Samstag",weekday_sunday:"Sonntag",base_temperature:"Basistemperatur",temperature:"Temperatur",time:"Uhrzeit",from:"Von",to:"Bis",add_period:"Zeitraum hinzufügen",delete_period:"Löschen",save:"Speichern",saving:"Speichern...",save_success:"Zeitplan erfolgreich gespeichert.",save_failed:"Fehler beim Speichern des Zeitplans.",load_failed:"Fehler beim Laden des Zeitplans.",reload:"Vom Gerät laden",reload_success:"Gerätekonfiguration neu geladen.",reload_failed:"Fehler beim Laden der Gerätekonfiguration.",export:"Exportieren",import:"Importieren",import_confirm_title:"Zeitplan importieren",import_confirm_text:"Diesen Zeitplan importieren und anwenden?",import_success:"Zeitplan importiert.",import_failed:"Fehler beim Importieren des Zeitplans.",no_schedule_data:"Keine Zeitplan-Daten verfügbar.",click_to_edit:"Klicken Sie auf einen Zeitabschnitt, um den Zeitplan zu bearbeiten",copy_schedule:"Zeitplan kopieren",paste_schedule:"Zeitplan einfügen",edit:"{weekday} bearbeiten",add_time_block:"+ Zeitblock hinzufügen",edit_slot:"Bearbeiten",save_slot:"Speichern",cancel_slot_edit:"Abbrechen",remove_slot:"Entfernen",undo_shortcut:"Rückgängig (Strg+Z)",redo_shortcut:"Wiederholen (Strg+Y)",warnings_title:"Validierungswarnungen",base_temperature_description:"Temperatur für nicht geplante Zeiträume",temperature_periods:"Temperaturperioden",invalid_schedule:"Ungültiger Zeitplan: {error}",validation_block_end_before_start:"Block {block}: Die Endzeit liegt vor der Startzeit",validation_block_zero_duration:"Block {block}: Der Block hat keine Dauer",validation_invalid_start_time:"Block {block}: Ungültige Startzeit",validation_invalid_end_time:"Block {block}: Ungültige Endzeit",validation_temp_out_of_range:"Block {block}: Temperatur außerhalb des Bereichs ({min}-{max}°C)",validation_invalid_slot_count:"Ungültige Anzahl an Slots: {count} (erwartet 13)",validation_invalid_slot_key:"Ungültiger Slot-Schlüssel: {key} (muss eine Ganzzahl 1-13 sein)",validation_missing_slot:"Slot {slot} fehlt",validation_slot_missing_values:"Slot {slot} fehlt ENDTIME oder TEMPERATURE",validation_slot_time_backwards:"Slot {slot}: Zeit läuft rückwärts: {time}",validation_slot_time_exceeds_day:"Slot {slot}: Zeit überschreitet 24:00: {time}",validation_last_slot_must_end:"Der letzte Slot muss um 24:00 enden",validation_schedule_must_be_object:"Zeitplandaten müssen ein Objekt sein",validation_missing_weekday:"Fehlender Wochentag: {weekday}",validation_invalid_weekday_data:"Ungültige Daten für {weekday}",validation_weekday_error:"{weekday}: {details}",entries:"{count} Einträge",max_entries:"Max. Einträge: {max}",level:"Wert",duration:"Dauer",condition:"Bedingung",target_channel:"Zielkanal",add_event:"Ereignis hinzufügen",edit_event:"Ereignis bearbeiten",delete_event:"Ereignis löschen",confirm_delete:"Möchten Sie dieses Ereignis wirklich löschen?",weekdays_label:"Wochentage",level_on:"Ein",level_off:"Aus",permanent_on:"Dauerhaft",show_more:"Mehr anzeigen",show_less:"Weniger anzeigen",slat:"Lamellenposition",ramp_time:"Rampenzeit",astro_sunrise:"Sonnenaufgang",astro_sunset:"Sonnenuntergang",astro_offset:"Astro-Offset (Min.)",condition_fixed_time:"Feste Zeit",condition_astro:"Astro",condition_fixed_if_before_astro:"Fest wenn vor Astro",condition_astro_if_before_fixed:"Astro wenn vor Fest",condition_fixed_if_after_astro:"Fest wenn nach Astro",condition_astro_if_after_fixed:"Astro wenn nach Fest",condition_earliest:"Frühester",condition_latest:"Spätester",or:"oder",if_before:"wenn vor",if_after:"wenn nach",device_mode_hint_bsl:"Dieses Gerät unterstützt Schalt- und Status-LED-Farbmodi über die CCU-WebUI.",device_mode_hint_rgbw:"Dieses Gerät unterstützt RGBW-Farbmodi über die CCU-WebUI.",device_mode_hint_lock:"Dieses Gerät unterstützt Türschloss-Modi über die CCU-WebUI.",weekly_program:"Wochenprogramm",weekly_program_enabled:"Wochenprogramm ist aktiv",weekly_program_disabled:"Wochenprogramm ist inaktiv",weekly_program_enable_failed:"Fehler beim Aktivieren/Deaktivieren des Wochenprogramms.",weekly_program_enabled_toast:"Wochenprogramm aktiviert.",weekly_program_disabled_toast:"Wochenprogramm deaktiviert.",lock_mode:"Zeitpunkt-Typ",lock_mode_door_lock:"Türschlossantrieb",lock_mode_user_permission:"Benutzerberechtigung",lock_action:"Aktion",lock_action_lock_autorelock_end:"Verriegeln + Auto-Relock Ende",lock_action_lock_autorelock_start:"Verriegeln + Auto-Relock Beginn",lock_action_unlock_autorelock_end:"Entriegeln + Auto-Relock Ende",lock_action_autorelock_end:"Auto-Relock Ende",lock_permission:"Berechtigung",permission_granted:"Erteilt",permission_not_granted:"Nicht erteilt",schedule_enabled:"Aktiviert",schedule_disabled:"Deaktiviert"},add_link:{title:"Neue Direktverknüpfung",step_channel:"Schritt 1/3 — Kanal wählen",step_peer:"Schritt 2/3 — Partner wählen",step_confirm:"Schritt 3/3 — Bestätigen",select_channel:"Kanal dieses Geräts auswählen:",select_role:"Rolle des gewählten Kanals:",role_sender:"Sender (sendet Kommandos)",role_receiver:"Empfänger (empfängt Kommandos)",search_devices:"Geräte suchen...",no_compatible:"Keine kompatiblen Kanäle gefunden.",link_name:"Verknüpfungsname (optional)",create:"Verknüpfung erstellen",create_success:"Verknüpfung erfolgreich erstellt.",create_failed:"Fehler beim Erstellen der Verknüpfung.",next:"Weiter",back:"Zurück"},tabs:{devices:"Geräte",integration:"Integration",ccu:"OpenCCU"},integration:{system_health:"Systemzustand",central_state:"Zentralenstatus",health_score:"Gesundheitswert",device_statistics:"Gerätestatistik",total_devices:"Geräte gesamt",unreachable:"Nicht erreichbar",firmware_updatable:"Firmware aktualisierbar",total_short:"gesamt",unreachable_short:"nicht erreichbar",radio_levels:"Duty Cycle / Carrier Sense",command_throttle:"Befehlsdrosselung",enabled:"Aktiviert",interval:"Intervall",queue_size:"Warteschlange",throttled:"Gedrosselt",burst_count:"Burst-Anzahl",incidents:"Vorfälle",no_incidents:"Keine Vorfälle aufgezeichnet.",clear_incidents:"Vorfälle löschen",clear_incidents_title:"Vorfälle löschen",clear_incidents_text:"Alle aufgezeichneten Vorfälle löschen? Dies kann nicht rückgängig gemacht werden.",incidents_cleared:"Vorfälle gelöscht.",clear:"Löschen",clear_cache:"Cache leeren",clear_cache_title:"Cache leeren",clear_cache_text:"Alle zwischengespeicherten Daten löschen? Die Integration holt die Daten erneut von der CCU.",cache_cleared:"Cache geleert.",actions:"Aktionen",refresh:"Aktualisieren",action_failed:"Aktion fehlgeschlagen."},ccu:{tab_general:"Allgemein",tab_pairing:"Geräte anlernen",tab_messages:"Meldungen",tab_signal:"Signalqualität",tab_firmware:"Firmware",no_inbox_devices:"Keine neuen Geräte im Posteingang.",no_service_messages:"Keine Servicemeldungen.",no_alarm_messages:"Keine Alarmmeldungen.",system_information:"Systeminformationen",name:"Name",model:"Modell",version:"Version",serial:"Seriennummer",hostname:"Hostname",ccu_type:"CCU-Typ",interfaces:"Schnittstellen",auth_enabled:"Authentifizierung",backup_exists:"Backup vorhanden",hub_messages:"Hub-Meldungen",service_messages:"Servicemeldungen",alarm_messages:"Alarmmeldungen",inbox:"Posteingang",address:"Adresse",device_type:"Gerätetyp",device_name:"Gerätename",accept:"Annehmen",accept_device_title:"Gerät annehmen",accept_device_text:"Gerät {device} in das System übernehmen?",accept_device_success:"Gerät {device} angenommen.",message:"Meldung",msg_type:"Typ",timestamp:"Zeitstempel",counter_label:"Anzahl",acknowledge:"Quittieren",message_acknowledged:"Meldung quittiert.",description:"Beschreibung",last_trigger:"Letzter Auslöser",install_mode:"Anlernmodus",active:"Aktiv",inactive:"Inaktiv",remaining_seconds:"Noch {seconds}s",activate:"Aktivieren",install_mode_title:"Anlernmodus aktivieren",install_mode_text:"Anlernmodus für {interface} aktivieren? Die CCU akzeptiert 60 Sekunden lang neue Geräte.",install_mode_activated:"Anlernmodus für {interface} aktiviert.",signal_quality:"Signalqualität",device:"Gerät",interface:"Schnittstelle",reachable:"Erreichbar",signal:"Signal",battery:"Batterie",low:"Schwach",ok:"OK",firmware_overview:"Firmware-Übersicht",updatable:"aktualisierbar",current_fw:"Aktuell",available_fw:"Verfügbar",state:"Status",refresh_firmware:"Firmware-Daten aktualisieren",firmware_refreshed:"Firmware-Daten aktualisiert.",actions:"Aktionen",refresh:"Aktualisieren",create_backup:"Backup erstellen",create_backup_title:"CCU-Backup erstellen",create_backup_text:"Ein Backup der CCU-Konfiguration erstellen? Dies kann einen Moment dauern.",backup_running:"Backup wird erstellt...",backup_success:"Backup erstellt: {filename} ({size} MB)",backup_failed:"Fehler beim Erstellen des Backups.",action_failed:"Aktion fehlgeschlagen.",filter_devices:"Geräte filtern...",filter_all:"Alle",filter_result:"{count} von {total} Geräten",update_firmware:"Aktualisieren",update_firmware_confirm:"Firmware für {device} aktualisieren?",update_firmware_success:"Firmware-Update für {device} gestartet",update_firmware_failed:"Firmware-Update fehlgeschlagen"},permissions:{read_only_notice:"Sie haben nur Lesezugriff. Wenden Sie sich an einen Administrator für Bearbeitungsrechte.",schedule_edit_required:"Berechtigung zur Zeitplanbearbeitung erforderlich.",device_config_required:"Berechtigung zur Gerätekonfiguration erforderlich.",device_links_required:"Berechtigung zur Verwaltung von Direktverknüpfungen erforderlich."},config_form:{dst_start:"Beginn der Sommerzeit",dst_end:"Ende der Sommerzeit"},cross_validation:{max_must_be_gte_min:"Maximum muss größer oder gleich dem Minimum sein.",level_must_be_in_range:"Level muss zwischen Minimum und Maximum liegen.",hi_must_be_gte_lo:"Oberer Schwellwert muss größer oder gleich dem unteren Schwellwert sein."}}};function Qe(e,t=""){const i={};for(const[s,a]of Object.entries(e)){const e=t?`${t}.${s}`:s;"string"==typeof a?i[e]=a:"object"==typeof a&&null!==a&&Object.assign(i,Qe(a,e))}return i}const Je=new Map;function et(e){if(Je.has(e))return Je.get(e);const t=Qe(Xe[e]??Xe.en);return Je.set(e,t),t}function tt(e,t,i){const s=et(e.config.language??"en");let a=s[t]??s[t.replace(/^panel\./,"")]??t;if(i)for(const[e,t]of Object.entries(i))a=a.replace(`{${e}}`,String(t));return a}let it=class extends oe{constructor(){super(...arguments),this.entryId="",this._devices=[],this._loading=!1,this._searchQuery="",this._sortColumn="name",this._sortAsc=!0,this._error=""}updated(e){e.has("entryId")&&this.entryId&&this._fetchDevices(),e.has("hass")&&this.hass&&this._updateDarkMode()}_updateDarkMode(){this.classList.toggle("dark-theme",this.hass?.themes?.darkMode??!1)}async _fetchDevices(){if(this.entryId){this._loading=!0,this._error="";try{this._devices=await Ae(this.hass,this.entryId)}catch(e){this._error=e instanceof Error?e.message:String(e),this._devices=[]}finally{this._loading=!1}}}_l(e,t){return tt(this.hass,e,t)}get _filteredDevices(){if(!this._searchQuery)return this._devices;const e=this._searchQuery.toLowerCase();return this._devices.filter(t=>t.name.toLowerCase().includes(e)||t.address.toLowerCase().includes(e)||t.model.toLowerCase().includes(e))}_setSortColumn(e){this._sortColumn===e?this._sortAsc=!this._sortAsc:(this._sortColumn=e,this._sortAsc=!0)}get _groupedDevices(){const e=this._sortAsc?1:-1,t=this._sortColumn,i=[...this._filteredDevices].sort((i,s)=>e*i[t].localeCompare(s[t])),s=new Map;for(const e of i){const t=e.interface_id.split("-").slice(1).join("-")||e.interface_id;s.has(t)||s.set(t,[]),s.get(t).push(e)}return s}_handleDeviceClick(e){this.dispatchEvent(new CustomEvent("device-selected",{detail:{device:e.address,interfaceId:e.interface_id},bubbles:!0,composed:!0}))}_handleIconError(e){e.target.style.display="none"}_renderMaintenanceIcons(e){return e&&0!==Object.keys(e).length?F`
      <div class="device-status">
        ${!0===e.unreach?F`<ha-icon
              class="status-badge unreachable"
              .icon=${"mdi:close-circle"}
              title="${this._l("device_list.unreachable")}"
              aria-label="${this._l("device_list.unreachable")}"
            ></ha-icon>`:!1===e.unreach?F`<ha-icon
                class="status-badge reachable"
                .icon=${"mdi:check-circle"}
                title="${this._l("device_list.reachable")}"
                aria-label="${this._l("device_list.reachable")}"
              ></ha-icon>`:j}
        ${!0===e.low_bat?F`<ha-icon
              class="status-badge low-bat"
              .icon=${"mdi:battery-alert"}
              title="${this._l("device_list.low_battery")}"
              aria-label="${this._l("device_list.low_battery")}"
            ></ha-icon>`:j}
        ${!0===e.config_pending?F`<ha-icon
              class="status-badge config-pending"
              .icon=${"mdi:clock-alert-outline"}
              title="${this._l("device_list.config_pending")}"
              aria-label="${this._l("device_list.config_pending")}"
            ></ha-icon>`:j}
      </div>
    `:j}render(){return F`
      <div class="panel-header">
        <h1>${this._l("device_list.title")}</h1>
      </div>

      ${this.entryId?F`
            <div class="search-bar">
              <ha-input
                .value=${this._searchQuery}
                @input=${e=>{this._searchQuery=e.target.value}}
                .placeholder=${this._l("device_list.search_placeholder")}
                aria-label=${this._l("device_list.search_placeholder")}
              ></ha-input>
            </div>
            <div class="sort-bar">
              <span class="sort-label">${this._l("device_list.sort_by")}:</span>
              <button
                class="sort-button ${"name"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("name")}
              >
                ${this._l("device_list.sort_name")}
                ${"name"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
              <button
                class="sort-button ${"address"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("address")}
              >
                ${this._l("device_list.sort_address")}
                ${"address"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
              <button
                class="sort-button ${"model"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("model")}
              >
                ${this._l("device_list.sort_model")}
                ${"model"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
            </div>
          `:j}
      ${this._loading?F`<div class="skeleton-container">
            ${[1,2,3,4,5].map(()=>F`<div class="skeleton-card"></div>`)}
          </div>`:this._error?F`<div class="error">
              ${this._error}
              <br />
              <ha-button outlined @click=${this._fetchDevices}>
                ${this._l("common.retry")}
              </ha-button>
            </div>`:this.entryId?0===this._filteredDevices.length?F`<div class="empty-state">${this._l("device_list.no_devices")}</div>`:this._renderDeviceGroups():F`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}
    `}_renderDeviceGroups(){return F`
      ${Array.from(this._groupedDevices.entries()).map(([e,t])=>F`
          <div class="interface-group">
            <div class="interface-header">${e}</div>
            ${t.map(e=>F`
                <div
                  class="device-card"
                  role="button"
                  tabindex="0"
                  @click=${()=>this._handleDeviceClick(e)}
                  @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._handleDeviceClick(e))}}
                >
                  ${e.device_icon?F`<img
                        class="device-icon"
                        src=${Ee(this.entryId,e.device_icon)}
                        alt=""
                        @error=${this._handleIconError}
                      />`:j}
                  <div class="device-main">
                    <div class="device-name">${e.name}</div>
                    <div class="device-model">${e.model}</div>
                  </div>
                  <div class="device-meta">
                    <span class="device-address">${e.address}</span>
                    <span class="device-channels">
                      ${e.channels.length} ${this._l("device_list.channels")}
                    </span>
                  </div>
                  ${this._renderMaintenanceIcons(e.maintenance)}
                  <ha-icon class="device-arrow" .icon=${"mdi:chevron-right"}></ha-icon>
                </div>
              `)}
          </div>
        `)}
    `}static{this.styles=[Se,n`
      .panel-header h1 {
        margin: 0 0 16px;
        font-size: 24px;
        font-weight: 400;
      }

      .search-bar {
        margin-bottom: 16px;
      }

      .search-bar ha-input {
        display: block;
        width: 100%;
      }

      .sort-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
      }

      .sort-label {
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .sort-button {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 16px;
        background: none;
        color: var(--primary-text-color);
        font-size: 13px;
        cursor: pointer;
        transition:
          background-color 0.1s,
          border-color 0.1s;
      }

      .sort-button:hover {
        background-color: var(--secondary-background-color, #f5f5f5);
      }

      .sort-button.active {
        border-color: var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        font-weight: 500;
      }

      .sort-button ha-icon {
        --ha-icon-display-size: 14px;
      }

      .interface-group {
        margin-bottom: 16px;
      }

      .interface-header {
        position: sticky;
        top: 0;
        z-index: 1;
        background: var(--primary-background-color, #fff);
        font-size: 14px;
        font-weight: 500;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        padding: 8px 0;
        border-bottom: 1px solid var(--divider-color);
        margin-bottom: 4px;
      }

      .device-card {
        display: flex;
        align-items: center;
        padding: 12px 8px;
        cursor: pointer;
        border-bottom: 1px solid var(--divider-color, #e0e0e0);
        transition: background-color 0.1s;
      }

      .device-card:hover,
      .device-card:focus-visible {
        background-color: var(--secondary-background-color, #f5f5f5);
      }

      .device-card:focus-visible {
        outline: 2px solid var(--primary-color, #03a9f4);
        outline-offset: -2px;
      }

      .device-icon {
        height: 32px;
        width: 32px;
        object-fit: contain;
        flex-shrink: 0;
        margin-right: 4px;
      }

      :host(.dark-theme) .device-icon {
        filter: invert(1) hue-rotate(180deg);
      }

      .device-main {
        flex: 1;
      }

      .device-name {
        font-size: 14px;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .device-model {
        font-size: 13px;
        color: var(--secondary-text-color);
        margin-top: 2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .device-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        margin-right: 12px;
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .device-status {
        display: flex;
        gap: 4px;
        align-items: center;
        margin-right: 8px;
      }

      .status-badge {
        --ha-icon-display-size: 18px;
        cursor: default;
      }

      .status-badge.unreachable {
        color: var(--error-color, #db4437);
      }

      .status-badge.reachable {
        color: var(--success-color, #4caf50);
      }

      .status-badge.low-bat {
        color: var(--warning-color, #ff9800);
      }

      .status-badge.config-pending {
        color: var(--warning-color, #ff9800);
      }

      .device-arrow {
        --ha-icon-display-size: 18px;
        color: var(--secondary-text-color);
      }

      .skeleton-container {
        padding: 8px 0;
      }

      .skeleton-card {
        height: 56px;
        border-radius: 4px;
        background: linear-gradient(
          90deg,
          var(--divider-color) 25%,
          var(--secondary-background-color) 50%,
          var(--divider-color) 75%
        );
        background-size: 200% 100%;
        animation: skeleton-pulse 1.5s ease-in-out infinite;
        margin-bottom: 4px;
      }

      @keyframes skeleton-pulse {
        0% {
          background-position: 200% 0;
        }
        100% {
          background-position: -200% 0;
        }
      }

      @media (max-width: 600px) {
        .device-card {
          flex-wrap: wrap;
        }

        .device-meta {
          flex-direction: row;
          gap: 8px;
          margin-right: 0;
          width: 100%;
          margin-top: 4px;
        }

        .device-arrow {
          display: none;
        }
      }
    `]}};function st(e,t){return new Promise(e=>{const i=document.activeElement,s=document.createElement("dialog");s.style.cssText=["border: none","border-radius: var(--ha-card-border-radius, 12px)","padding: 24px","max-width: 450px","width: calc(100% - 48px)","max-height: 90vh","overflow-y: auto","box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3)","font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif)","background: var(--card-background-color, var(--ha-card-background, #fff))","color: var(--primary-text-color, #212121)"].join("; ");const a=t.title?`<h2 style="margin: 0 0 16px; font-size: 18px; font-weight: 500;">${at(t.title)}</h2>`:"",r=t.text?`<p style="margin: 0 0 24px; white-space: pre-line; line-height: 1.5; color: var(--secondary-text-color, #727272);">${at(t.text)}</p>`:"",n=t.destructive?"var(--error-color, #db4437)":"var(--primary-color, #03a9f4)";s.innerHTML=`\n      ${a}\n      ${r}\n      <div style="display: flex; justify-content: flex-end; gap: 8px;">\n        <button class="dismiss" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: transparent;\n          color: var(--primary-text-color, #212121);\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${at(t.dismissText||"Cancel")}</button>\n        <button class="confirm" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: ${n};\n          color: #fff;\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${at(t.confirmText||"OK")}</button>\n      </div>\n    `;const o=t=>{s.close(),s.remove(),i?.focus(),e(t)};s.querySelector(".confirm").addEventListener("click",()=>o(!0)),s.querySelector(".dismiss").addEventListener("click",()=>o(!1)),s.addEventListener("cancel",e=>{e.preventDefault(),o(!1)}),document.body.appendChild(s),s.showModal()})}function at(e){const t=document.createElement("div");return t.textContent=e,t.innerHTML}function rt(e,t){const i=new CustomEvent("hass-notification",{bubbles:!0,composed:!0,detail:t});e.dispatchEvent(i)}e([he({attribute:!1})],it.prototype,"hass",void 0),e([he()],it.prototype,"entryId",void 0),e([pe()],it.prototype,"_devices",void 0),e([pe()],it.prototype,"_loading",void 0),e([pe()],it.prototype,"_searchQuery",void 0),e([pe()],it.prototype,"_sortColumn",void 0),e([pe()],it.prototype,"_sortAsc",void 0),e([pe()],it.prototype,"_error",void 0),it=e([we("hm-device-list")],it);let nt=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this._device=null,this._hasSchedule=!1,this._loading=!0,this._error=""}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this.deviceAddress&&this._fetchDevice(),e.has("hass")&&this.hass&&this.classList.toggle("dark-theme",this.hass.themes?.darkMode??!1)}async _fetchDevice(){this._loading=!0,this._error="";try{const[e,t]=await Promise.all([Ae(this.hass,this.entryId),Ne(this.hass,this.entryId).catch(()=>[])]);this._device=e.find(e=>e.address===this.deviceAddress)??null,this._hasSchedule=t.some(e=>e.address===this.deviceAddress)}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_handleChannelClick(e){this.dispatchEvent(new CustomEvent("channel-selected",{detail:{channel:e.address,interfaceId:this.interfaceId,channelType:e.channel_type,paramsetKey:"MASTER",deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowHistory(){this.dispatchEvent(new CustomEvent("show-history",{detail:{device:this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowLinks(){this.dispatchEvent(new CustomEvent("show-links",{detail:{device:this.deviceAddress,interfaceId:this.interfaceId,deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowSchedules(){this.dispatchEvent(new CustomEvent("show-schedules",{detail:{device:this.deviceAddress,interfaceId:this.interfaceId,deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}async _handleExport(e){try{const t=await async function(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/export_paramset",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}(this.hass,this.entryId,this.interfaceId,e.address,"MASTER"),i=new Blob([t.json_data],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s,a.download=`${e.address.replace(/:/g,"_")}_MASTER.json`,a.click(),URL.revokeObjectURL(s),rt(this,{message:this._l("device_detail.export_success")})}catch{rt(this,{message:this._l("device_detail.export_failed")})}}async _handleImport(e){const t=document.createElement("input");t.type="file",t.accept=".json",t.onchange=async()=>{const i=t.files?.[0];if(i)try{const t=await i.text();if(!await st(0,{title:this._l("device_detail.import_confirm_title"),text:this._l("device_detail.import_confirm_text",{channel:e.address}),confirmText:this._l("device_detail.import"),dismissText:this._l("common.cancel")}))return;const s=await async function(e,t,i,s,a,r="MASTER"){return e.callWS({type:"homematicip_local/config/import_paramset",entry_id:t,interface_id:i,channel_address:s,json_data:a,paramset_key:r})}(this.hass,this.entryId,this.interfaceId,e.address,t,"MASTER");rt(this,s.success?{message:this._l("device_detail.import_success")}:{message:this._l("device_detail.import_validation_failed")})}catch{rt(this,{message:this._l("device_detail.import_failed")})}},t.click()}async _copyToClipboard(e){try{await navigator.clipboard.writeText(e),rt(this,{message:this._l("device_detail.copied")})}catch{rt(this,{message:this._l("device_detail.copy_failed")})}}_isVirtualChannel(e){return parseInt(e.address.split(":").pop()??"0")>=50}_isWeekProgramChannel(e){return e.channel_type.endsWith("WEEK_PROFILE")}_handleIconError(e){e.target.style.display="none"}render(){if(this._loading)return F`<div class="loading">${this._l("common.loading")}</div>`;if(this._error)return F`<div class="error">
        ${this._error}
        <br />
        <ha-button outlined @click=${this._fetchDevice}> ${this._l("common.retry")} </ha-button>
      </div>`;if(!this._device)return F`<div class="empty-state">${this._l("device_detail.not_found")}</div>`;const e=this._device,t=e.channels.find(e=>!e.address.includes(":")),i=e.channels.find(e=>e.address.endsWith(":0")),s=e.channels.filter(e=>e.address.includes(":")&&!e.address.endsWith(":0")).sort((e,t)=>parseInt(e.address.split(":").pop()??"0",10)-parseInt(t.address.split(":").pop()??"0",10));return F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="device-header">
        ${e.device_icon?F`<img
              class="device-icon"
              src=${Ee(this.entryId,e.device_icon)}
              alt=""
              @error=${this._handleIconError}
            />`:j}
        <div class="device-header-text">
          <h2>${e.model} — ${e.name}</h2>
          <div class="device-info">
            ${this._l("device_detail.address")}: ${e.address}
            <ha-icon-button
              class="copy-btn"
              .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
              @click=${()=>this._copyToClipboard(e.address)}
              .label=${this._l("device_detail.copy")}
            ></ha-icon-button>
            | ${this._l("device_detail.firmware")}: ${e.firmware}
            <ha-icon-button
              class="copy-btn"
              .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
              @click=${()=>this._copyToClipboard(e.firmware)}
              .label=${this._l("device_detail.copy")}
            ></ha-icon-button>
          </div>
        </div>
        <div class="header-actions">
          ${Ce.has(e.interface)?F`
                <ha-button outlined @click=${this._handleShowLinks}>
                  ${this._l("device_detail.show_links")}
                </ha-button>
              `:j}
          ${this._hasSchedule?F`
                <ha-button outlined @click=${this._handleShowSchedules}>
                  ${this._l("device_detail.show_schedules")}
                </ha-button>
              `:j}
          <ha-button outlined @click=${this._handleShowHistory}>
            ${this._l("device_detail.show_history")}
          </ha-button>
        </div>
      </div>

      ${t?this._renderDeviceChannel(t):j}
      ${i?this._renderMaintenanceChannel(i,e.maintenance):j}
      ${s.map(e=>this._renderChannel(e))}
    `}_renderDeviceChannel(e){return e.paramset_keys.includes("MASTER")?F`
      <div class="channel-card device-channel">
        <div class="channel-header">
          ${this._l("device_detail.device_config")}: ${e.channel_type_label}
        </div>
        <div class="channel-actions">
          <ha-button outlined @click=${()=>this._handleChannelClick(e)}>
            <ha-icon slot="icon" .icon=${"mdi:cog"}></ha-icon>
            ${this._l("device_detail.configure_master")}
          </ha-button>
          <ha-icon-button
            .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
            @click=${()=>this._handleExport(e)}
            .label=${this._l("device_detail.export")}
          ></ha-icon-button>
          <ha-icon-button
            .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
            @click=${()=>this._handleImport(e)}
            .label=${this._l("device_detail.import")}
          ></ha-icon-button>
        </div>
      </div>
    `:j}_renderMaintenanceChannel(e,t){const i=t&&Object.keys(t).length>0,s=e.paramset_keys.includes("MASTER");return i||s?F`
      <div class="channel-card maintenance">
        <div class="channel-header">
          ${this._l("device_detail.channel")} 0: ${e.channel_type_label}
        </div>
        ${i?this._renderStatusSummary(t):j}
        ${s?F`
              <div class="channel-actions">
                <ha-button outlined @click=${()=>this._handleChannelClick(e)}>
                  <ha-icon slot="icon" .icon=${"mdi:cog"}></ha-icon>
                  ${this._l("device_detail.configure_master")}
                </ha-button>
                <ha-icon-button
                  .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
                  @click=${()=>this._handleExport(e)}
                  .label=${this._l("device_detail.export")}
                ></ha-icon-button>
                <ha-icon-button
                  .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
                  @click=${()=>this._handleImport(e)}
                  .label=${this._l("device_detail.import")}
                ></ha-icon-button>
              </div>
            `:j}
      </div>
    `:j}_renderStatusSummary(e){const t=[];return void 0!==e.rssi_device&&t.push({label:this._l("device_detail.rssi_device"),value:`${e.rssi_device} dBm`,icon:"mdi:signal"}),t.push({label:this._l("device_detail.rssi_peer"),value:null!=e.rssi_peer?`${e.rssi_peer} dBm`:"—",icon:"mdi:signal"}),void 0!==e.dutycycle&&t.push({label:this._l("device_detail.dutycycle"),value:this._l(e.dutycycle?"device_detail.yes":"device_detail.no"),icon:"mdi:timer-outline"}),void 0!==e.low_bat&&t.push({label:this._l("device_detail.low_bat"),value:this._l(e.low_bat?"device_detail.yes":"device_detail.no"),icon:"mdi:battery-alert"}),void 0!==e.unreach&&t.push({label:this._l("device_detail.unreach"),value:this._l(e.unreach?"device_detail.no":"device_detail.yes"),icon:e.unreach?"mdi:close-circle":"mdi:check-circle"}),void 0!==e.config_pending&&t.push({label:this._l("device_detail.config_pending_label"),value:this._l(e.config_pending?"device_detail.yes":"device_detail.no"),icon:"mdi:information-outline"}),0===t.length?j:F`
      <div class="status-grid">
        ${t.map(e=>F`
            <div class="status-item">
              <ha-icon class="status-icon" .icon=${e.icon}></ha-icon>
              <span>${e.label}: ${e.value}</span>
            </div>
          `)}
      </div>
    `}_renderChannel(e){const t=e.address.split(":").pop()??"",i=e.paramset_keys.includes("MASTER"),s=this._isVirtualChannel(e);return this._isWeekProgramChannel(e)&&this._hasSchedule?this._renderWeekProgramChannel(e,t,s):F`
      <div class="channel-card ${s?"virtual":""}">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${e.channel_type_label}
          ${s?F`<span class="virtual-badge">${this._l("device_detail.virtual")}</span>`:j}
        </div>
        ${i?F`
              <div class="channel-actions">
                <ha-button outlined @click=${()=>this._handleChannelClick(e)}>
                  <ha-icon slot="icon" .icon=${"mdi:cog"}></ha-icon>
                  ${this._l("device_detail.configure_master")}
                </ha-button>
                <ha-icon-button
                  .path=${"M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"}
                  @click=${()=>this._handleExport(e)}
                  .label=${this._l("device_detail.export")}
                ></ha-icon-button>
                <ha-icon-button
                  .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"}
                  @click=${()=>this._handleImport(e)}
                  .label=${this._l("device_detail.import")}
                ></ha-icon-button>
              </div>
            `:F`
              <div class="channel-no-config">${this._l("device_detail.no_master_config")}</div>
            `}
      </div>
    `}_renderWeekProgramChannel(e,t,i){return F`
      <div class="channel-card week-program ${i?"virtual":""}">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${e.channel_type_label}
          ${i?F`<span class="virtual-badge">${this._l("device_detail.virtual")}</span>`:j}
        </div>
        <div class="channel-actions">
          <ha-button outlined @click=${this._handleShowSchedules}>
            <ha-icon slot="icon" .icon=${"mdi:calendar-clock"}></ha-icon>
            ${this._l("device_detail.edit_schedule")}
          </ha-button>
          <span class="schedule-hint">${this._l("device_detail.schedule_channel_hint")}</span>
        </div>
      </div>
    `}static{this.styles=[Se,n`
      .back-button {
        margin-bottom: 8px;
      }

      .device-header {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 16px;
        flex-wrap: wrap;
      }

      .device-icon {
        height: 48px;
        width: 48px;
        object-fit: contain;
        flex-shrink: 0;
      }

      :host(.dark-theme) .device-icon {
        filter: invert(1) hue-rotate(180deg);
      }

      .device-header-text {
        flex: 1;
        min-width: 0;
      }

      .device-header-text h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .header-actions {
        display: flex;
        gap: 8px;
        margin-top: 8px;
        flex-wrap: wrap;
      }

      .channel-card {
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        margin-bottom: 12px;
        overflow: hidden;
      }

      .channel-card.device-channel {
        border-color: var(--primary-color, #03a9f4);
      }

      .channel-card.maintenance {
        border-color: var(--primary-color, #03a9f4);
      }

      .channel-header {
        font-size: 14px;
        font-weight: 500;
        padding: 12px 16px;
        background: var(--secondary-background-color, #fafafa);
        border-bottom: 1px solid var(--divider-color, #e0e0e0);
      }

      .channel-actions {
        padding: 8px 16px;
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        align-items: center;
      }

      .channel-no-config {
        padding: 8px 16px;
        color: var(--secondary-text-color);
        font-size: 13px;
      }

      .status-icon {
        --ha-icon-display-size: 20px;
        color: var(--secondary-text-color);
      }

      .copy-btn {
        --ha-icon-button-size: 28px;
        --ha-icon-button-icon-size: 16px;
        color: var(--secondary-text-color);
        vertical-align: middle;
      }

      .channel-card.week-program {
        border-color: var(--secondary-text-color, #888);
        opacity: 0.8;
      }

      .schedule-hint {
        color: var(--secondary-text-color);
        font-size: 13px;
        font-style: italic;
      }

      .channel-card.virtual {
        border-style: dashed;
      }

      .virtual-badge {
        display: inline-block;
        font-size: 11px;
        padding: 1px 8px;
        border-radius: 12px;
        background: var(--secondary-text-color, #888);
        color: #fff;
        margin-left: 8px;
        vertical-align: middle;
        font-weight: 400;
      }
    `]}};e([he({attribute:!1})],nt.prototype,"hass",void 0),e([he()],nt.prototype,"entryId",void 0),e([he()],nt.prototype,"interfaceId",void 0),e([he()],nt.prototype,"deviceAddress",void 0),e([pe()],nt.prototype,"_device",void 0),e([pe()],nt.prototype,"_hasSchedule",void 0),e([pe()],nt.prototype,"_loading",void 0),e([pe()],nt.prototype,"_error",void 0),nt=e([we("hm-device-detail")],nt);let ot=class extends oe{constructor(){super(...arguments),this.presets=[],this.allowCustom=!1,this.value=null,this.parameterId="",this._isCustom=!1}firstUpdated(){this._isCustom=!this._isPresetValue(this.value)}render(){const e=this._isCustom?"__custom__":String(this.value??""),t=[...this.presets.map(e=>({value:String(e.value),label:e.label})),...this.allowCustom?[{value:"__custom__",label:"Custom..."}]:[]];return F`
      <div class="preset-select">
        <ha-select
          .value=${e}
          .options=${t}
          @selected=${this._handlePresetSelected}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
        ${this._isCustom?F`
              <input
                type="number"
                class="custom-input"
                .value=${String(this.value??"")}
                @change=${this._handleCustomChange}
              />
            `:j}
      </div>
    `}_isPresetValue(e){return null!=e&&this.presets.some(t=>t.value===e)}_handlePresetSelected(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if("__custom__"===t)return void(this._isCustom=!0);this._isCustom=!1;const i=parseFloat(t);this._dispatchChange(isNaN(i)?t:i)}_handleCustomChange(e){const t=e.target,i=parseFloat(t.value);this._dispatchChange(isNaN(i)?t.value:i)}_dispatchChange(e){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:this.parameterId,value:e,currentValue:this.value},bubbles:!0,composed:!0}))}static{this.styles=n`
    .preset-select {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    ha-select {
      min-width: 150px;
    }
    .custom-input {
      width: 80px;
      padding: 8px;
      border: 1px solid var(--divider-color, #e0e0e0);
      border-radius: 4px;
      font-size: 14px;
    }
  `}};function lt(e,t){return e.option_labels?.[t]??t}function dt(e,t,i){return t.options&&"number"==typeof i&&i>=0&&i<t.options.length?lt(t,t.options[i]):"toggle"===t.widget?tt(e,i?"form_parameter.toggle_on":"form_parameter.toggle_off"):String(i??"")}e([he({attribute:!1})],ot.prototype,"hass",void 0),e([he({attribute:!1})],ot.prototype,"presets",void 0),e([he({type:Boolean})],ot.prototype,"allowCustom",void 0),e([he()],ot.prototype,"value",void 0),e([he()],ot.prototype,"parameterId",void 0),e([pe()],ot.prototype,"_isCustom",void 0),ot=e([we("hm-form-preset-select")],ot);let ct=class extends oe{constructor(){super(...arguments),this.value=null,this.modified=!1,this.validationError="",this.entryId="",this.interfaceId="",this.channelAddress="",this._helpExpanded=!1,this._detecting=!1}_getDisplayValue(e){return dt(this.hass,this.parameter,e)}_emitChange(e){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:this.parameter.id,value:e,currentValue:this.parameter.current_value},bubbles:!0,composed:!0}))}get _supportsAutoDetect(){return Boolean(this.parameter.operations&&8&this.parameter.operations)}async _handleAutoDetect(){if(!this._detecting&&this.entryId&&this.interfaceId&&this.channelAddress){this._detecting=!0;try{const e=await async function(e,t,i,s,a){return e.callWS({type:"homematicip_local/config/determine_parameter",entry_id:t,interface_id:i,channel_address:s,parameter_id:a})}(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.parameter.id);e.success?this._emitChange(e.value):rt(this,{message:tt(this.hass,"form_parameter.detect_failed")})}catch{rt(this,{message:tt(this.hass,"form_parameter.detect_failed")})}finally{this._detecting=!1}}}_renderAutoDetectButton(){return this._supportsAutoDetect?this._detecting?F`<ha-circular-progress indeterminate size="small"></ha-circular-progress>`:F`
      <ha-icon-button
        class="auto-detect-icon"
        .path=${"M7.5,5.6L5,7L6.4,4.5L5,2L7.5,3.4L10,2L8.6,4.5L10,7L7.5,5.6M19.5,15.4L22,14L20.6,16.5L22,19L19.5,17.6L17,19L18.4,16.5L17,14L19.5,15.4M22,2L20.6,4.5L22,7L19.5,5.6L17,7L18.4,4.5L17,2L19.5,3.4L22,2M13.34,12.78L15.78,10.34L13.66,8.22L11.22,10.66L13.34,12.78M14.37,7.29L16.71,9.63C17.1,10 17.1,10.65 16.71,11.04L5.04,22.71C4.65,23.1 4,23.1 3.63,22.71L1.29,20.37C0.9,20 0.9,19.35 1.29,18.96L12.96,7.29C13.35,6.9 14,6.9 14.37,7.29Z"}
        @click=${this._handleAutoDetect}
        .label=${tt(this.hass,"form_parameter.auto_detect")}
      ></ha-icon-button>
    `:j}render(){const e=this.parameter,t=!e.writable;return F`
      <div class="parameter-row ${t?"read-only":""}">
        <div class="parameter-label">
          ${e.label}
          ${e.unit?F`<span class="parameter-unit">(${e.unit})</span>`:j}
          ${e.description?F`<ha-icon-button
                class="help-icon"
                .path=${"M11,18H13V16H11V18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,6A4,4 0 0,0 8,10H10A2,2 0 0,1 12,8A2,2 0 0,1 14,10C14,12 11,11.75 11,14H13C13,12.5 16,12.25 16,10A4,4 0 0,0 12,6Z"}
                @click=${()=>{this._helpExpanded=!this._helpExpanded}}
                .label=${"Info"}
              ></ha-icon-button>`:j}
          ${this.modified?F`<span class="modified-dot"></span>`:j}
        </div>
        <div class="parameter-control">
          ${this._renderWidget(e,t)}${this._renderAutoDetectButton()}
        </div>
      </div>
      ${this._helpExpanded&&e.description?F`<ha-markdown
            .content=${e.description}
            class="parameter-description"
          ></ha-markdown>`:j}
      ${this._renderRangeHint(e)}
      ${this.validationError?F`<ha-alert alert-type="error" id="error-${this.parameter.id}">
            ${this.validationError}
          </ha-alert>`:j}
    `}_renderRangeHint(e){if("toggle"===e.widget||"dropdown"===e.widget||"radio_group"===e.widget||"button"===e.widget||"read_only"===e.widget)return j;if(null==e.min&&null==e.max)return j;const t=[];return null!=e.min&&t.push(`Min: ${e.min}`),null!=e.max&&t.push(`Max: ${e.max}`),F`<div class="range-hint">${t.join(" · ")}</div>`}_renderWidget(e,t){if(e.presets&&e.presets.length>0&&!t)return F`
        <hm-form-preset-select
          .hass=${this.hass}
          .presets=${e.presets}
          .allowCustom=${e.allow_custom_value??!1}
          .value=${this.value}
          .parameterId=${e.id}
          @value-changed=${e=>{e.stopPropagation(),this._emitChange(e.detail.value)}}
        ></hm-form-preset-select>
      `;switch(e.widget){case"toggle":return F`
          <ha-switch
            .checked=${Boolean(this.value)}
            .disabled=${t}
            @change=${e=>{this._emitChange(e.target.checked)}}
          ></ha-switch>
        `;case"slider_with_input":return F`
          <div class="slider-group">
            <ha-slider
              .min=${e.min??0}
              .max=${e.max??100}
              .step=${e.step??1}
              .value=${Number(this.value??e.min??0)}
              .disabled=${t}
              @change=${t=>{const i=Number(t.target.value),s="integer"===e.type?Math.round(i):i;s!==this.value&&this._emitChange(s)}}
            ></ha-slider>
            <input
              type="number"
              class="number-input"
              .min=${String(e.min??"")}
              .max=${String(e.max??"")}
              .step=${String(e.step??1)}
              .value=${String(this.value??"")}
              ?disabled=${t}
              @change=${t=>{const i=Number(t.target.value);this._emitChange("integer"===e.type?Math.round(i):i)}}
            />
          </div>
        `;case"number_input":return F`
          <input
            type="number"
            class="number-input"
            .min=${String(e.min??"")}
            .max=${String(e.max??"")}
            .step=${String(e.step??1)}
            .value=${String(this.value??"")}
            ?disabled=${t}
            @change=${t=>{const i=Number(t.target.value);this._emitChange("integer"===e.type?Math.round(i):i)}}
          />
        `;case"dropdown":return F`
          <ha-select
            .value=${String(this.value??0)}
            .disabled=${t}
            .options=${(e.options??[]).map((t,i)=>({value:String(i),label:lt(e,t)}))}
            @selected=${e=>{e.stopPropagation();const t=parseInt(e.detail.value,10);Number.isNaN(t)||t===this.value||this._emitChange(t)}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        `;case"radio_group":return F`
          <div class="radio-group">
            ${(e.options??[]).map((i,s)=>F`
                <label class="radio-item">
                  <ha-radio
                    name=${e.id}
                    .checked=${this.value===s}
                    .disabled=${t}
                    @change=${()=>this._emitChange(s)}
                  ></ha-radio>
                  ${lt(e,i)}
                </label>
              `)}
          </div>
        `;case"text_input":return F`
          <input
            type="text"
            .value=${String(this.value??"")}
            ?disabled=${t}
            @change=${e=>{this._emitChange(e.target.value)}}
          />
        `;case"button":return F`
          <ha-button outlined .disabled=${t} @click=${()=>this._emitChange(!0)}>
            ${e.label}
          </ha-button>
        `;default:return F`<span class="read-only-value">${this._getDisplayValue(this.value)}</span>`}}static{this.styles=[Se,n`
      .read-only {
        opacity: 0.7;
      }

      .help-icon {
        --ha-icon-button-size: 28px;
        --ha-icon-button-icon-size: 16px;
        color: var(--secondary-text-color);
        opacity: 0.6;
        margin: -4px 0;
      }

      .help-icon:hover {
        opacity: 1;
        color: var(--primary-color, #03a9f4);
      }

      .auto-detect-icon {
        --ha-icon-button-size: 28px;
        --ha-icon-button-icon-size: 16px;
        color: var(--secondary-text-color);
        opacity: 0.7;
        margin: -4px 0;
        flex-shrink: 0;
      }

      .auto-detect-icon:hover {
        opacity: 1;
        color: var(--primary-color, #03a9f4);
      }

      .slider-group {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .slider-group ha-slider {
        flex: 1;
        min-width: 80px;
      }

      .number-input {
        width: 80px;
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      ha-select {
        min-width: 120px;
      }

      input[type="text"] {
        padding: 6px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
        min-width: 120px;
      }

      .radio-group {
        display: flex;
        flex-direction: column;
        gap: 4px;
      }

      .radio-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        cursor: pointer;
      }

      .read-only-value {
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      .range-hint {
        font-size: 11px;
        color: var(--secondary-text-color);
        margin: 2px 0 4px;
        opacity: 0.8;
      }

      .parameter-description {
        display: block;
        font-size: 12px;
        color: var(--secondary-text-color);
        margin: 0 0 4px;
        padding: 8px 12px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 4px;
        line-height: 1.4;
        animation: fadeIn 0.15s ease-out;
      }

      @keyframes fadeIn {
        from {
          opacity: 0;
        }
        to {
          opacity: 1;
        }
      }

      @media (max-width: 600px) {
        .slider-group {
          width: 100%;
        }

        .number-input {
          width: 100%;
          box-sizing: border-box;
          font-size: 16px;
          min-height: 44px;
        }

        ha-select {
          width: 100%;
          box-sizing: border-box;
        }

        input[type="text"] {
          width: 100%;
          box-sizing: border-box;
          font-size: 16px;
          min-height: 44px;
        }

        .radio-item {
          min-height: 44px;
        }
      }
    `]}};e([he({attribute:!1})],ct.prototype,"hass",void 0),e([he({attribute:!1})],ct.prototype,"parameter",void 0),e([he()],ct.prototype,"value",void 0),e([he({type:Boolean})],ct.prototype,"modified",void 0),e([he()],ct.prototype,"validationError",void 0),e([he()],ct.prototype,"entryId",void 0),e([he()],ct.prototype,"interfaceId",void 0),e([he()],ct.prototype,"channelAddress",void 0),e([pe()],ct.prototype,"_helpExpanded",void 0),e([pe()],ct.prototype,"_detecting",void 0),ct=e([we("hm-form-parameter")],ct);let ht=class extends oe{render(){const e=this.subsetGroup,t=e.current_option_id,i=e.options.map(e=>({value:String(e.id),label:e.label}));return F`
      <div class="subset-select">
        <div class="subset-label">${e.label}</div>
        <ha-select
          .value=${null!=t?String(t):""}
          .options=${i}
          @selected=${this._handleSelected}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>
    `}_handleSelected(e){e.stopPropagation();const t=e.detail.value;if(!t)return;const i=parseInt(t,10),s=this.subsetGroup.options.find(e=>e.id===i);if(s)for(const[e,t]of Object.entries(s.values))this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:e,value:t},bubbles:!0,composed:!0}))}static{this.styles=n`
    .subset-select {
      margin: 8px 0;
    }
    .subset-label {
      font-weight: 500;
      margin-bottom: 4px;
      color: var(--primary-text-color);
    }
    ha-select {
      min-width: 200px;
    }
  `}};e([he({attribute:!1})],ht.prototype,"hass",void 0),e([he({attribute:!1})],ht.prototype,"subsetGroup",void 0),ht=e([we("hm-form-subset-select")],ht);const pt=[{unit:0,value:0,label_en:"Not active",label_de:"Nicht aktiv"},{unit:0,value:1,label_en:"100ms",label_de:"100ms"},{unit:0,value:3,label_en:"300ms",label_de:"300ms"},{unit:0,value:5,label_en:"500ms",label_de:"500ms"},{unit:0,value:15,label_en:"1500ms",label_de:"1500ms"},{unit:1,value:1,label_en:"1 second",label_de:"1 Sekunde"},{unit:1,value:2,label_en:"2 seconds",label_de:"2 Sekunden"},{unit:1,value:3,label_en:"3 seconds",label_de:"3 Sekunden"},{unit:1,value:30,label_en:"30 seconds",label_de:"30 Sekunden"},{unit:2,value:1,label_en:"1 minute",label_de:"1 Minute"},{unit:2,value:2,label_en:"2 minutes",label_de:"2 Minuten"},{unit:2,value:4,label_en:"4 minutes",label_de:"4 Minuten"},{unit:2,value:15,label_en:"15 minutes",label_de:"15 Minuten"}];let _t=class extends oe{constructor(){super(...arguments),this.pendingChanges=new Map,this.validationErrors={},this.expertMode=!1,this.entryId="",this.interfaceId="",this.channelAddress="",this._customModePairs=new Set}_isDstParam(e){return e.startsWith("DST_START_")||e.startsWith("DST_END_")}_detectDstGroups(e){const t=[],i=[],s=new Set;for(const a of e.parameters)a.id.startsWith("DST_START_")?(t.push(a),s.add(a.id)):a.id.startsWith("DST_END_")&&(i.push(a),s.add(a.id));return{startParams:t,endParams:i,dstIds:s}}_formatMinutesAsTime(e){const t=Math.floor(e/60),i=e%60;return`${String(t).padStart(2,"0")}:${String(i).padStart(2,"0")}`}_renderDstGroup(e,t){return F`
      <div class="dst-group">
        <div class="dst-group-header">${e}</div>
        ${t.map(e=>{const t=this._getEffectiveValue(e);if(e.id.endsWith("_TIME")){const i=Number(t??0);return F`
              <div class="parameter-row">
                <div class="parameter-label">
                  ${e.label}
                  ${this._isModified(e)?F`<span class="modified-dot"></span>`:j}
                </div>
                <div class="parameter-control">
                  <input
                    type="time"
                    .value=${this._formatMinutesAsTime(i)}
                    ?disabled=${!e.writable}
                    @change=${t=>{const i=t.target,[s,a]=i.value.split(":").map(Number);this._dispatchValueChanged(e.id,60*s+a,e.current_value)}}
                  />
                </div>
              </div>
            `}return F`
            <hm-form-parameter
              .hass=${this.hass}
              .parameter=${e}
              .value=${t}
              .modified=${this._isModified(e)}
              .validationError=${this.validationErrors[e.id]??""}
              .entryId=${this.entryId}
              .interfaceId=${this.interfaceId}
              .channelAddress=${this.channelAddress}
              @value-changed=${this._handleValueChanged}
            ></hm-form-parameter>
          `})}
      </div>
    `}_getEffectiveValue(e){return this.pendingChanges.has(e.id)?this.pendingChanges.get(e.id):e.current_value}_isModified(e){return this.pendingChanges.has(e.id)}_detectPairs(e){const t=new Map,i=new Set;for(const s of e.parameters){if(s.id.endsWith("_UNIT")){const a=s.id.slice(0,-5),r=e.parameters.find(e=>e.id===`${a}_VALUE`);r&&(t.set(a,{unitParam:s,valueParam:r}),i.add(s.id),i.add(r.id))}if(s.id.endsWith("_TIME_BASE")){const a=s.id.slice(0,-10),r=e.parameters.find(e=>e.id===`${a}_TIME_FACTOR`);r&&(t.set(`${a}_TIME`,{unitParam:s,valueParam:r}),i.add(s.id),i.add(r.id))}}return{pairs:t,pairedIds:i}}_derivePairLabel(e,t){if("de"===t){if(e.startsWith("Wert "))return e.slice(5)}else if(e.endsWith(" Value"))return e.slice(0,-6);return e}render(){if(!this.schema||!this.schema.sections)return j;const e=new Set,t=this.schema.subset_groups??[];for(const i of t)for(const t of i.member_params)e.add(t);const i=new Set;return F`
      ${this.schema.sections.map(s=>{const{pairs:a,pairedIds:r}=this._detectPairs(s),{startParams:n,endParams:o,dstIds:l}=this._detectDstGroups(s),d=new Set;return F`
          <div class="form-section">
            <div class="section-header">${s.title}</div>
            ${s.parameters.map(s=>{if(d.has(s.id))return j;if(s.hidden_by_default&&!this.expertMode)return j;if(l.has(s.id)&&l.size>0){for(const e of l)d.add(e);return F`
                  ${n.length?this._renderDstGroup(tt(this.hass,"config_form.dst_start"),n):j}
                  ${o.length?this._renderDstGroup(tt(this.hass,"config_form.dst_end"),o):j}
                `}if(e.has(s.id)){const e=t.find(e=>e.member_params.includes(s.id));return e&&!i.has(e.id)?(i.add(e.id),F`
                    <hm-form-subset-select
                      .hass=${this.hass}
                      .subsetGroup=${e}
                      @value-changed=${this._handleValueChanged}
                    ></hm-form-subset-select>
                  `):j}if(s.visible_when){const e=this._getEffectiveValue({id:s.visible_when.trigger_param,current_value:this._getCurrentParamValue(s.visible_when.trigger_param)})===s.visible_when.trigger_value;if(!(s.visible_when.invert?!e:e))return j}if(r.has(s.id)){const e=[...a.entries()].find(([,e])=>e.unitParam.id===s.id||e.valueParam.id===s.id);if(e)return d.add(e[1].unitParam.id),d.add(e[1].valueParam.id),this._renderTimePair(e[0],e[1])}return F`
                <hm-form-parameter
                  .hass=${this.hass}
                  .parameter=${s}
                  .value=${this._getEffectiveValue(s)}
                  .modified=${this._isModified(s)}
                  .validationError=${this.validationErrors[s.id]??""}
                  .entryId=${this.entryId}
                  .interfaceId=${this.interfaceId}
                  .channelAddress=${this.channelAddress}
                  @value-changed=${this._handleValueChanged}
                ></hm-form-parameter>
              `})}
          </div>
        `})}
    `}_getCurrentParamValue(e){if(this.pendingChanges.has(e))return this.pendingChanges.get(e);for(const t of this.schema?.sections??[]){const i=t.parameters.find(t=>t.id===e);if(i)return i.current_value}}_renderTimePair(e,t){const{unitParam:i,valueParam:s}=t,a=this.hass.config.language??"en",r=Number(this._getEffectiveValue(i)??0),n=Number(this._getEffectiveValue(s)??0),o=this._isModified(i)||this._isModified(s),l=!i.writable||!s.writable,d=this._derivePairLabel(s.label,a),c=pt.findIndex(e=>e.unit===r&&e.value===n),h=this._customModePairs.has(e)||c<0,p=h?"custom":String(c);return F`
      <div class="parameter-row ${l?"read-only":""}">
        <div class="parameter-label">
          ${d} ${o?F`<span class="modified-dot"></span>`:j}
        </div>
        <div class="parameter-control">
          <ha-select
            .value=${p}
            .disabled=${l}
            .options=${[...pt.map((e,t)=>({value:String(t),label:"de"===a?e.label_de:e.label_en})),{value:"custom",label:tt(this.hass,"form_parameter.custom_value")}]}
            @selected=${t=>this._handlePresetSelected(t,e,i,s)}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
      ${this._renderPairValidationErrors(i,s)}
      ${h?this._renderCustomFields(i,s):j}
    `}_renderPairValidationErrors(e,t){const i=this.validationErrors[e.id],s=this.validationErrors[t.id];return i||s?F`
      ${i?F`<ha-alert alert-type="error">${i}</ha-alert>`:j}
      ${s?F`<ha-alert alert-type="error">${s}</ha-alert>`:j}
    `:j}_renderCustomFields(e,t){return F`
      <div class="custom-fields">
        <hm-form-parameter
          .hass=${this.hass}
          .parameter=${e}
          .value=${this._getEffectiveValue(e)}
          .modified=${this._isModified(e)}
          .validationError=${""}
          .entryId=${this.entryId}
          .interfaceId=${this.interfaceId}
          .channelAddress=${this.channelAddress}
          @value-changed=${this._handleValueChanged}
        ></hm-form-parameter>
        <hm-form-parameter
          .hass=${this.hass}
          .parameter=${t}
          .value=${this._getEffectiveValue(t)}
          .modified=${this._isModified(t)}
          .validationError=${""}
          .entryId=${this.entryId}
          .interfaceId=${this.interfaceId}
          .channelAddress=${this.channelAddress}
          @value-changed=${this._handleValueChanged}
        ></hm-form-parameter>
      </div>
    `}_handlePresetSelected(e,t,i,s){e.stopPropagation();const a=e.detail.value;if(!a||"custom"===a)return this._customModePairs.add(t),void this.requestUpdate();this._customModePairs.delete(t);const r=pt[parseInt(a,10)];if(r){const e=Number(this._getEffectiveValue(i)??0),t=Number(this._getEffectiveValue(s)??0);if(r.unit===e&&r.value===t)return;this._dispatchValueChanged(i.id,r.unit,i.current_value),this._dispatchValueChanged(s.id,r.value,s.current_value)}}_dispatchValueChanged(e,t,i){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:e,value:t,currentValue:i},bubbles:!0,composed:!0}))}_handleValueChanged(e){this.dispatchEvent(new CustomEvent("value-changed",{detail:e.detail,bubbles:!0,composed:!0}))}static{this.styles=[Se,n`
      .form-section {
        margin-bottom: 16px;
      }

      .custom-fields {
        padding-left: 16px;
        border-left: 2px solid var(--divider-color, #e0e0e0);
        margin: 0 0 8px;
      }

      .dst-group {
        margin: 8px 0;
        padding-left: 16px;
        border-left: 2px solid var(--divider-color, #e0e0e0);
      }

      .dst-group-header {
        font-weight: 500;
        margin-bottom: 4px;
        color: var(--primary-text-color);
      }

      .dst-group input[type="time"] {
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      @media (max-width: 600px) {
        .custom-fields,
        .dst-group {
          padding-left: 8px;
        }

        .dst-group input[type="time"] {
          font-size: 16px;
          min-height: 44px;
          width: 100%;
          box-sizing: border-box;
        }
      }
    `]}};var ut;e([he({attribute:!1})],_t.prototype,"hass",void 0),e([he({attribute:!1})],_t.prototype,"schema",void 0),e([he({attribute:!1})],_t.prototype,"pendingChanges",void 0),e([he({attribute:!1})],_t.prototype,"validationErrors",void 0),e([he({type:Boolean})],_t.prototype,"expertMode",void 0),e([he()],_t.prototype,"entryId",void 0),e([he()],_t.prototype,"interfaceId",void 0),e([he()],_t.prototype,"channelAddress",void 0),_t=e([we("hm-config-form")],_t);let vt=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.channelAddress="",this.channelType="",this.paramsetKey="MASTER",this.deviceName="",this.editable=!0,this._schema=null,this._pendingChanges=new Map,this._loading=!0,this._saving=!1,this._error="",this._validationErrors={},this._expertMode=!1,this._sessionActive=!1,this._canUndo=!1,this._canRedo=!1}static{ut=this}static{this._SESSION_WARNING_SECONDS=270}disconnectedCallback(){super.disconnectedCallback(),this._clearSessionTimer()}_startSessionTimer(){this._clearSessionTimer(),this._sessionTimerId=setTimeout(()=>{this._sessionActive&&(rt(this,{message:this._l("channel_config.session_expiring")}),this._refreshSession())},1e3*ut._SESSION_WARNING_SECONDS)}_clearSessionTimer(){void 0!==this._sessionTimerId&&(clearTimeout(this._sessionTimerId),this._sessionTimerId=void 0)}async _refreshSession(){if(this._sessionActive)try{await De(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey),this._startSessionTimer()}catch{this._sessionActive=!1,this._clearSessionTimer()}}updated(e){(e.has("channelAddress")||e.has("entryId"))&&this.entryId&&this.channelAddress&&this._fetchSchema(),e.has("hass")&&this.hass&&this.classList.toggle("dark-theme",this.hass.themes?.darkMode??!1)}async _fetchSchema(){this._loading=!0,this._error="",this._pendingChanges=new Map,this._validationErrors={},this._canUndo=!1,this._canRedo=!1;try{this._schema=await Ie(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.channelType,this.paramsetKey),await De(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey),this._sessionActive=!0,this._startSessionTimer()}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}get _isDirty(){return this._pendingChanges.size>0}async _handleValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;if(i===s?this._pendingChanges.delete(t):this._pendingChanges.set(t,i),this._pendingChanges=new Map(this._pendingChanges),this._sessionActive)try{const e=await Te(this.hass,this.entryId,this.channelAddress,t,i,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,this._validationErrors=e.validation_errors}catch{try{await De(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey),this._sessionActive=!0,this._startSessionTimer();const e=await Te(this.hass,this.entryId,this.channelAddress,t,i,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,this._validationErrors=e.validation_errors}catch{this._sessionActive=!1}}}async _handleUndo(){if(this._sessionActive)try{const e=await async function(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_undo",entry_id:t,channel_address:i,paramset_key:s})}(this.hass,this.entryId,this.channelAddress,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,e.performed&&await this._refreshSchemaValues()}catch(e){this._error=String(e)}}async _handleRedo(){if(this._sessionActive)try{const e=await async function(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_redo",entry_id:t,channel_address:i,paramset_key:s})}(this.hass,this.entryId,this.channelAddress,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,e.performed&&await this._refreshSchemaValues()}catch(e){this._error=String(e)}}async _refreshSchemaValues(){try{this._schema=await Ie(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.channelType,this.paramsetKey),this._pendingChanges=new Map}catch(e){this._error=String(e)}}_handleDiscard(){this._pendingChanges=new Map,this._validationErrors={},this._sessionActive&&Me(this.hass,this.entryId,this.channelAddress,this.paramsetKey).then(()=>(this._canUndo=!1,this._canRedo=!1,De(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey))).then(()=>{this._startSessionTimer()}).catch(()=>{})}_handleResetDefaults(){if(this._schema){this._pendingChanges=new Map;for(const e of this._schema.sections)for(const t of e.parameters)t.writable&&void 0!==t.default&&t.default!==t.current_value&&this._pendingChanges.set(t.id,t.default);this._pendingChanges=new Map(this._pendingChanges)}}async _handleSave(){if(!this._isDirty||this._saving)return;const e=this._pendingChanges.size,t=[...this._pendingChanges.entries()].map(([e,t])=>{const i=this._findParameter(e);return`${i?.label??e}: ${i?dt(this.hass,i,i.current_value):"?"} → ${i?dt(this.hass,i,t):String(t)}`}).join("\n");if(await st(0,{title:this._l("channel_config.confirm_save_title"),text:`${this._l("channel_config.confirm_save_text",{count:e})}\n\n${t}`,confirmText:this._l("common.save"),dismissText:this._l("common.cancel")})){this._saving=!0,this._validationErrors={};try{if(this._sessionActive){const e=await async function(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/session_save",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey);e.success?(this._pendingChanges=new Map,this._sessionActive=!1,this._clearSessionTimer(),rt(this,{message:this._l("channel_config.save_success")}),await this._fetchSchema()):Object.keys(e.validation_errors).length>0?(this._validationErrors=e.validation_errors,rt(this,{message:this._l("channel_config.validation_failed")})):rt(this,{message:this._l("channel_config.save_failed")})}else{const e=Object.fromEntries(this._pendingChanges),t=await async function(e,t,i,s,a,r="MASTER",n=!0){return e.callWS({type:"homematicip_local/config/put_paramset",entry_id:t,interface_id:i,channel_address:s,paramset_key:r,values:a,validate:n})}(this.hass,this.entryId,this.interfaceId,this.channelAddress,e,this.paramsetKey);t.success?(this._pendingChanges=new Map,rt(this,{message:this._l("channel_config.save_success")}),await this._fetchSchema()):Object.keys(t.validation_errors).length>0?(this._validationErrors=t.validation_errors,rt(this,{message:this._l("channel_config.validation_failed")})):rt(this,{message:this._l("channel_config.save_failed")})}}catch(e){this._error=String(e),rt(this,{message:this._l("channel_config.save_failed")})}finally{this._saving=!1}}}_findParameter(e){if(this._schema)for(const t of this._schema.sections){const i=t.parameters.find(t=>t.id===e);if(i)return i}}async _handleBack(){if(!this._isDirty||await st(0,{title:this._l("channel_config.unsaved_title"),text:this._l("channel_config.unsaved_warning"),confirmText:this._l("channel_config.discard"),dismissText:this._l("common.cancel"),destructive:!0})){if(this._sessionActive){try{await Me(this.hass,this.entryId,this.channelAddress,this.paramsetKey)}catch{}this._sessionActive=!1,this._clearSessionTimer()}this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}}_handleExpertModeToggle(e){this._expertMode=e.target.checked}_handleIconError(e){e.target.style.display="none"}render(){return this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:this._error&&!this._schema?F`<div class="error">
        ${this._error}
        <br />
        <ha-button outlined @click=${this._fetchSchema}> ${this._l("common.retry")} </ha-button>
      </div>`:F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="config-header">
        ${this._schema?.device_icon?F`<img
              class="device-icon"
              src=${Ee(this.entryId,this._schema.device_icon)}
              alt=""
              @error=${this._handleIconError}
            />`:j}
        <div class="config-header-text">
          ${this.deviceName?F`<h2>${this.deviceName}</h2>`:j}
          <div class="device-info">
            ${this.channelAddress} —
            ${this._schema?.channel_type_label||this._schema?.channel_type||""} —
            ${this.paramsetKey}
          </div>
        </div>
      </div>

      <div class="expert-toggle">
        <label class="expert-label">
          <ha-switch
            .checked=${this._expertMode}
            @change=${this._handleExpertModeToggle}
          ></ha-switch>
          <span>${this._l("channel_config.expert_mode")}</span>
        </label>
        <span class="expert-hint">${this._l("channel_config.expert_mode_hint")}</span>
      </div>

      <div aria-live="polite">
        ${this._error?F`<div class="error">${this._error}</div>`:j}
      </div>
      ${this._schema?F`
            <hm-config-form
              .hass=${this.hass}
              .schema=${this._schema}
              .pendingChanges=${this._pendingChanges}
              .validationErrors=${this._validationErrors}
              .expertMode=${this._expertMode}
              .entryId=${this.entryId}
              .interfaceId=${this.interfaceId}
              .channelAddress=${this.channelAddress}
              @value-changed=${this._handleValueChanged}
            ></hm-config-form>
          `:j}
      ${this.editable?F`
            <div class="action-bar-split action-bar-sticky">
              <div class="action-bar-left">
                <ha-icon-button
                  @click=${this._handleUndo}
                  .disabled=${!this._canUndo||this._saving}
                  .label=${this._l("channel_config.undo")}
                  .path=${"M12.5,8C9.85,8 7.45,9 5.6,10.6L2,7V16H11L7.38,12.38C8.77,11.22 10.54,10.5 12.5,10.5C16.04,10.5 19.05,12.81 20.1,16L22.47,15.22C21.08,11.03 17.15,8 12.5,8Z"}
                ></ha-icon-button>
                <ha-icon-button
                  @click=${this._handleRedo}
                  .disabled=${!this._canRedo||this._saving}
                  .label=${this._l("channel_config.redo")}
                  .path=${"M18.4,10.6C16.55,9 14.15,8 11.5,8C6.85,8 2.92,11.03 1.54,15.22L3.9,16C4.95,12.81 7.95,10.5 11.5,10.5C13.45,10.5 15.23,11.22 16.62,12.38L13,16H22V7L18.4,10.6Z"}
                ></ha-icon-button>
              </div>
              <div class="action-bar-right">
                <ha-button outlined @click=${this._handleResetDefaults} .disabled=${this._saving}>
                  ${this._l("channel_config.reset_defaults")}
                </ha-button>
                <ha-button
                  outlined
                  @click=${this._handleDiscard}
                  .disabled=${!this._isDirty||this._saving}
                >
                  ${this._l("channel_config.discard")}
                </ha-button>
                <ha-button
                  raised
                  @click=${this._handleSave}
                  .disabled=${!this._isDirty||this._saving}
                >
                  ${this._l(this._saving?"channel_config.saving":"channel_config.save")}
                </ha-button>
              </div>
            </div>
          `:j}
    `}static{this.styles=[Se,n`
      .config-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 16px;
      }

      .device-icon {
        height: 48px;
        width: 48px;
        object-fit: contain;
        flex-shrink: 0;
      }

      :host(.dark-theme) .device-icon {
        filter: invert(1) hue-rotate(180deg);
      }

      .config-header-text h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      ha-icon-button[disabled] {
        opacity: 0.5;
      }

      .expert-toggle {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
      }

      .expert-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: var(--primary-text-color);
        cursor: pointer;
      }

      .expert-hint {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .action-bar-split {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
        border-top: 1px solid var(--divider-color);
      }

      .action-bar-left,
      .action-bar-right {
        display: flex;
        gap: 8px;
      }

      @media (max-width: 600px) {
        .action-bar-split {
          flex-direction: column;
          gap: 12px;
        }

        .action-bar-left,
        .action-bar-right {
          width: 100%;
          justify-content: stretch;
        }

        .action-bar-right {
          flex-direction: column;
        }

        .action-bar-right ha-button {
          width: 100%;
        }
      }
    `]}};e([he({attribute:!1})],vt.prototype,"hass",void 0),e([he()],vt.prototype,"entryId",void 0),e([he()],vt.prototype,"interfaceId",void 0),e([he()],vt.prototype,"channelAddress",void 0),e([he()],vt.prototype,"channelType",void 0),e([he()],vt.prototype,"paramsetKey",void 0),e([he()],vt.prototype,"deviceName",void 0),e([he({type:Boolean})],vt.prototype,"editable",void 0),e([pe()],vt.prototype,"_schema",void 0),e([pe()],vt.prototype,"_pendingChanges",void 0),e([pe()],vt.prototype,"_loading",void 0),e([pe()],vt.prototype,"_saving",void 0),e([pe()],vt.prototype,"_error",void 0),e([pe()],vt.prototype,"_validationErrors",void 0),e([pe()],vt.prototype,"_expertMode",void 0),e([pe()],vt.prototype,"_sessionActive",void 0),e([pe()],vt.prototype,"_canUndo",void 0),e([pe()],vt.prototype,"_canRedo",void 0),vt=ut=e([we("hm-channel-config")],vt);let mt=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this.deviceName="",this.editable=!0,this._links=[],this._loading=!0,this._error="",this._sortColumn="channel",this._sortAsc=!0,this._swipeX=0,this._touchStartX=0,this._touchStartY=0,this._isSwiping=!1,this._isScrolling=!1}updated(e){(e.has("entryId")||e.has("deviceAddress")||e.has("interfaceId"))&&this.entryId&&this.deviceAddress&&this.interfaceId&&this._fetchLinks()}async _fetchLinks(){this._loading=!0,this._error="";try{this._links=await async function(e,t,i,s){return(await e.callWS({type:"homematicip_local/config/list_device_links",entry_id:t,interface_id:i,device_address:s})).links}(this.hass,this.entryId,this.interfaceId,this.deviceAddress)}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_handleAddLink(){this.dispatchEvent(new CustomEvent("add-link",{detail:{deviceAddress:this.deviceAddress,interfaceId:this.interfaceId},bubbles:!0,composed:!0}))}_handleConfigure(e){this.dispatchEvent(new CustomEvent("configure-link",{detail:{senderAddress:e.sender_address,receiverAddress:e.receiver_address,interfaceId:this.interfaceId,senderDeviceName:e.sender_device_name,senderDeviceModel:e.sender_device_model,senderChannelTypeLabel:e.sender_channel_type_label,receiverDeviceName:e.receiver_device_name,receiverDeviceModel:e.receiver_device_model,receiverChannelTypeLabel:e.receiver_channel_type_label},bubbles:!0,composed:!0}))}async _handleDelete(e){if(await st(0,{title:this._l("device_links.delete_confirm_title"),text:this._l("device_links.delete_confirm_text",{sender:e.sender_address,receiver:e.receiver_address}),confirmText:this._l("device_links.delete"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t,i,s){return e.callWS({type:"homematicip_local/config/remove_link",entry_id:t,sender_channel_address:i,receiver_channel_address:s})}(this.hass,this.entryId,e.sender_address,e.receiver_address),rt(this,{message:this._l("device_links.delete_success")}),await this._fetchLinks()}catch{rt(this,{message:this._l("device_links.delete_failed")})}}_onTouchStart(e,t){if(!this.editable)return;const i=e.touches[0];this._touchStartX=i.clientX,this._touchStartY=i.clientY,this._isSwiping=!1,this._isScrolling=!1,this._swipingLinkKey=t,this._swipeX=0}_onTouchMove(e){if(!this._swipingLinkKey)return;const t=e.touches[0],i=t.clientX-this._touchStartX;if(!this._isSwiping&&!this._isScrolling){if(Math.abs(t.clientY-this._touchStartY)>10)return this._isScrolling=!0,this._swipingLinkKey=void 0,void(this._swipeX=0);Math.abs(i)>10&&(this._isSwiping=!0)}this._isScrolling||this._isSwiping&&(e.preventDefault(),this._swipeX=Math.min(0,i))}_onTouchEnd(e){this._swipingLinkKey&&this._isSwiping?Math.abs(this._swipeX)>=120?(this._handleDelete(e),this._resetSwipe()):(this._swipeX=0,setTimeout(()=>this._resetSwipe(),200)):this._resetSwipe()}_resetSwipe(){this._swipingLinkKey=void 0,this._swipeX=0,this._isSwiping=!1,this._isScrolling=!1}_setSortColumn(e){this._sortColumn===e?this._sortAsc=!this._sortAsc:(this._sortColumn=e,this._sortAsc=!0)}get _sortedLinks(){const e=this._sortAsc?1:-1;return[...this._links].sort((t,i)=>{switch(this._sortColumn){case"sender":return e*t.sender_device_name.localeCompare(i.sender_device_name);case"receiver":return e*t.receiver_device_name.localeCompare(i.receiver_device_name);case"channel":{const s=t.sender_address.startsWith(this.deviceAddress)?t.sender_address:t.receiver_address,a=i.sender_address.startsWith(this.deviceAddress)?i.sender_address:i.receiver_address,r=parseInt(s.split(":").pop()??"0"),n=parseInt(a.split(":").pop()??"0");return e*(r-n)}default:return 0}})}_groupByChannel(){const e=new Map;for(const t of this._sortedLinks){const i=(t.sender_address.startsWith(this.deviceAddress)?t.sender_address:t.receiver_address).split(":").pop()??"";e.has(i)||e.set(i,[]),e.get(i).push(t)}return e}render(){return F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="links-header">
        <h2>${this._l("device_links.title")}</h2>
        <div class="device-info">
          ${this._l("device_links.subtitle",{device:this.deviceName||this.deviceAddress})}
        </div>
      </div>

      ${this.editable?F`
            <ha-button class="add-link-btn" @click=${this._handleAddLink}>
              <ha-icon slot="icon" .icon=${"mdi:plus"}></ha-icon>
              ${this._l("device_links.add_link")}
            </ha-button>
          `:j}
      ${this._links.length>0?F`
            <div class="sort-bar">
              <span class="sort-label">${this._l("device_links.sort_by")}:</span>
              <button
                class="sort-button ${"channel"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("channel")}
              >
                ${this._l("device_links.sort_channel")}
                ${"channel"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
              <button
                class="sort-button ${"sender"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("sender")}
              >
                ${this._l("device_links.sort_sender")}
                ${"sender"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
              <button
                class="sort-button ${"receiver"===this._sortColumn?"active":""}"
                @click=${()=>this._setSortColumn("receiver")}
              >
                ${this._l("device_links.sort_receiver")}
                ${"receiver"===this._sortColumn?F`<ha-icon
                      .icon=${this._sortAsc?"mdi:arrow-up":"mdi:arrow-down"}
                    ></ha-icon>`:j}
              </button>
            </div>
          `:j}
      ${this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:this._error?F`<div class="error">
              ${this._error}
              <br />
              <ha-button outlined @click=${this._fetchLinks}>
                ${this._l("common.retry")}
              </ha-button>
            </div>`:0===this._links.length?F`<div class="empty-state">
                <ha-icon class="empty-icon" .icon=${"mdi:link-off"}></ha-icon>
                <div class="empty-message">${this._l("device_links.empty")}</div>
                <span class="empty-hint">${this._l("device_links.empty_hint")}</span>
                ${this.editable?F`
                      <ha-button class="empty-action" @click=${this._handleAddLink}>
                        <ha-icon slot="icon" .icon=${"mdi:plus"}></ha-icon>
                        ${this._l("device_links.add_link")}
                      </ha-button>
                    `:j}
              </div>`:this._renderGroupedLinks()}
    `}_renderGroupedLinks(){const e=this._groupByChannel(),t=[...e.keys()].sort((e,t)=>parseInt(e)-parseInt(t));return F`
      ${t.map(t=>{const i=e.get(t);return F`
          <div class="link-channel-group">
            <div class="link-channel-header">
              ${this._l("device_links.channel_group",{channel:t})}
            </div>
            ${i.map(e=>this._renderLinkCard(e))}
          </div>
        `})}
    `}_renderLinkCard(e){const t="outgoing"===e.direction,i=`${e.sender_address}-${e.receiver_address}`,s=this._swipingLinkKey===i,a=s?this._swipeX:0;return F`
      <div class="link-card-wrapper">
        ${s&&a<-40?F`<div class="swipe-delete-bg">
              <ha-icon .icon=${"mdi:delete"}></ha-icon>
            </div>`:""}
        <div
          class="link-card ${t?"outgoing":"incoming"} ${s&&this._isSwiping?"swiping":""}"
          style=${s&&this._isSwiping?`transform: translateX(${a}px)`:""}
          @touchstart=${e=>this._onTouchStart(e,i)}
          @touchmove=${e=>this._onTouchMove(e)}
          @touchend=${()=>this._onTouchEnd(e)}
        >
          <div class="link-direction">
            <span class="direction-badge ${e.direction}">
              ${this._l(t?"device_links.outgoing":"device_links.incoming")}
            </span>
          </div>
          <div class="link-info">
            <div class="link-endpoints">
              <div class="link-endpoint-info">
                <span class="link-device-name">
                  ${e.sender_channel_name||e.sender_channel_type_label||e.sender_device_name}
                </span>
                <span class="link-device-detail">
                  ${e.sender_device_name} · ${e.sender_device_model}
                </span>
                <span class="link-endpoint-address">${e.sender_address}</span>
              </div>
              <ha-icon class="link-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
              <div class="link-endpoint-info">
                <span class="link-device-name">
                  ${e.receiver_channel_name||e.receiver_channel_type_label||e.receiver_device_name}
                </span>
                <span class="link-device-detail">
                  ${e.receiver_device_name} · ${e.receiver_device_model}
                </span>
                <span class="link-endpoint-address">${e.receiver_address}</span>
              </div>
            </div>
            ${e.name?F`<div class="link-name">"${e.name}"</div>`:j}
          </div>
          ${this.editable?F`
                <div class="link-actions">
                  <ha-button outlined @click=${()=>this._handleConfigure(e)}>
                    ${this._l("device_links.configure")}
                  </ha-button>
                  <ha-button outlined class="destructive" @click=${()=>this._handleDelete(e)}>
                    ${this._l("device_links.delete")}
                  </ha-button>
                </div>
              `:j}
        </div>
      </div>
    `}static{this.styles=[Se,n`
      .links-header {
        margin-bottom: 16px;
      }

      .links-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .add-link-btn {
        margin-bottom: 16px;
      }

      .sort-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
      }

      .sort-label {
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .sort-button {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 16px;
        background: none;
        color: var(--primary-text-color);
        font-size: 13px;
        cursor: pointer;
        transition:
          background-color 0.1s,
          border-color 0.1s;
      }

      .sort-button:hover {
        background-color: var(--secondary-background-color, #f5f5f5);
      }

      .sort-button.active {
        border-color: var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        font-weight: 500;
      }

      .sort-button ha-icon {
        --ha-icon-display-size: 14px;
      }

      .link-channel-group {
        margin-bottom: 16px;
      }

      .link-channel-header {
        font-size: 14px;
        font-weight: 500;
        color: var(--secondary-text-color);
        padding: 8px 0;
        border-bottom: 1px solid var(--divider-color);
        margin-bottom: 8px;
      }

      /* Swipe-to-delete wrapper */
      .link-card-wrapper {
        position: relative;
        overflow: hidden;
        border-radius: 8px;
        margin-bottom: 8px;
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

      .link-card.swiping {
        transition: none !important;
      }

      .link-card {
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        padding: 12px 16px;
      }

      .link-card.outgoing {
        border-left: 3px solid var(--primary-color, #03a9f4);
      }

      .link-card.incoming {
        border-left: 3px solid var(--secondary-text-color, #888);
      }

      .direction-badge {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 12px;
        text-transform: uppercase;
      }

      .direction-badge.outgoing {
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }

      .direction-badge.incoming {
        background: var(--secondary-text-color, #888);
        color: #fff;
      }

      .link-endpoints {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 8px 0 4px;
      }

      .link-endpoint-info {
        display: flex;
        flex-direction: column;
        gap: 1px;
        min-width: 0;
      }

      .link-device-name {
        font-size: 14px;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .link-device-detail {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .link-endpoint-address {
        font-family: monospace;
        font-size: 12px;
        color: var(--secondary-text-color);
        overflow-wrap: break-word;
        word-break: break-all;
      }

      .empty-icon {
        --ha-icon-display-size: 48px;
        color: var(--secondary-text-color);
        opacity: 0.5;
        margin-bottom: 12px;
      }

      .empty-message {
        font-size: 16px;
        margin-bottom: 4px;
      }

      .empty-hint {
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .empty-action {
        margin-top: 16px;
      }

      .link-arrow {
        --ha-icon-display-size: 20px;
        color: var(--secondary-text-color);
        flex-shrink: 0;
      }

      .link-name {
        font-size: 12px;
        font-style: italic;
        color: var(--secondary-text-color);
        margin-top: 4px;
      }

      .link-actions {
        display: flex;
        gap: 8px;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid var(--divider-color, #e0e0e0);
      }

      .destructive {
        --ha-button-color: var(--error-color, #db4437);
      }

      @media (max-width: 600px) {
        .link-endpoints {
          flex-direction: column;
          align-items: flex-start;
          gap: 4px;
        }

        .link-arrow {
          align-self: center;
        }

        .link-actions {
          flex-direction: column;
        }

        .link-actions ha-button {
          width: 100%;
        }
      }

      /* Touch device optimizations */
      @media (hover: none) and (pointer: coarse) {
        .link-card:not(.swiping) {
          transition: transform 0.2s ease-out;
        }
      }
    `]}};e([he({attribute:!1})],mt.prototype,"hass",void 0),e([he()],mt.prototype,"entryId",void 0),e([he()],mt.prototype,"interfaceId",void 0),e([he()],mt.prototype,"deviceAddress",void 0),e([he()],mt.prototype,"deviceName",void 0),e([he({type:Boolean})],mt.prototype,"editable",void 0),e([pe()],mt.prototype,"_links",void 0),e([pe()],mt.prototype,"_loading",void 0),e([pe()],mt.prototype,"_error",void 0),e([pe()],mt.prototype,"_sortColumn",void 0),e([pe()],mt.prototype,"_sortAsc",void 0),e([pe()],mt.prototype,"_swipingLinkKey",void 0),e([pe()],mt.prototype,"_swipeX",void 0),mt=e([we("hm-device-links")],mt);const gt=[{base:0,multiplierSeconds:0,labelKey:"time_selector.unit_inactive"},{base:1,multiplierSeconds:.1,labelKey:"time_selector.unit_100ms"},{base:2,multiplierSeconds:1,labelKey:"time_selector.unit_seconds"},{base:3,multiplierSeconds:5,labelKey:"time_selector.unit_5seconds"},{base:4,multiplierSeconds:10,labelKey:"time_selector.unit_10seconds"},{base:5,multiplierSeconds:60,labelKey:"time_selector.unit_minutes"},{base:6,multiplierSeconds:600,labelKey:"time_selector.unit_10minutes"},{base:7,multiplierSeconds:3600,labelKey:"time_selector.unit_hours"}];let ft=class extends oe{constructor(){super(...arguments),this.baseValue=0,this.factorValue=0,this.presets=[],this.modified=!1,this._isCustom=!1}_l(e){return tt(this.hass,e)}get _lang(){return this.hass?.config?.language??"en"}get _effectivePresets(){const e=[...this.presets],t=e.some(e=>0===e.base&&0===e.factor),i=e.some(e=>7===e.base&&31===e.factor);return t||e.unshift({base:0,factor:0,label:this._l("time_selector.unit_inactive")}),i||e.push({base:7,factor:31,label:this._l("time_selector.permanent")}),e}get _matchesPreset(){return this._effectivePresets.some(e=>e.base===this.baseValue&&e.factor===this.factorValue)}_getDurationText(e,t){const i=gt.find(t=>t.base===e);return i&&0!==i.multiplierSeconds&&0!==t?function(e,t){if(e<=0)return"";const i="de"===t,s=Math.floor(e/3600),a=Math.floor(e%3600/60),r=e%60,n=Math.round(e%1*1e3),o=[];return s>0&&o.push(i?`${s} Std.`:`${s}h`),a>0&&o.push(i?`${a} Min.`:`${a}min`),r>=1?o.push(i?`${Math.floor(r)} Sek.`:`${Math.floor(r)}s`):n>0&&0===s&&0===a&&o.push(`${n}ms`),o.length>0?`= ${o.join(" ")}`:""}(i.multiplierSeconds*t,this._lang):""}_emitChange(e,t,i){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:e,value:t,currentValue:i},bubbles:!0,composed:!0}))}_handlePresetChange(e){e.stopPropagation();const t=e.detail.value;if(!t||"custom"===t)return void(this._isCustom=!0);this._isCustom=!1;const[i,s]=t.split("-"),a=Number(i),r=Number(s);a===this.baseValue&&r===this.factorValue||(this._emitChange(this.baseParam.id,a,this.baseParam.current_value),this._emitChange(this.factorParam.id,r,this.factorParam.current_value))}_handleUnitChange(e){e.stopPropagation();const t=e.detail.value;if(null==t)return;const i=Number(t);i!==this.baseValue&&this._emitChange(this.baseParam.id,i,this.baseParam.current_value)}_handleValueChange(e){const t=Number(e.target.value);this._emitChange(this.factorParam.id,t,this.factorParam.current_value)}render(){const e=this.baseParam.label.replace(/ Base$/,"").replace(/ Basis$/,""),t=this._matchesPreset,i=this._isCustom&&!t,s=this._getDurationText(this.baseValue,this.factorValue);return F`
      <div class="time-selector">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e} ${this.modified?F`<span class="modified-dot"></span>`:j}
          </div>
          <div class="parameter-control">
            <ha-select
              .value=${t?`${this.baseValue}-${this.factorValue}`:"custom"}
              .options=${[...this._effectivePresets.map(e=>({value:`${e.base}-${e.factor}`,label:e.label})),{value:"custom",label:this._l("link_config.custom_time")}]}
              @selected=${this._handlePresetChange}
              @closed=${e=>e.stopPropagation()}
            ></ha-select>
          </div>
        </div>
        ${t&&s?F`<div class="duration-hint">${s}</div>`:j}
        ${i||!t?F`
              <div class="custom-time-inputs">
                <div class="custom-field">
                  <label class="custom-label">${this._l("time_selector.unit")}:</label>
                  <ha-select
                    .value=${String(this.baseValue)}
                    .options=${gt.map(e=>({value:String(e.base),label:this._l(e.labelKey)}))}
                    @selected=${this._handleUnitChange}
                    @closed=${e=>e.stopPropagation()}
                  ></ha-select>
                </div>
                ${this.baseValue>0?F`
                      <div class="custom-field">
                        <label class="custom-label">${this._l("time_selector.value")}:</label>
                        <input
                          type="number"
                          min="0"
                          max="31"
                          .value=${String(this.factorValue)}
                          @change=${this._handleValueChange}
                        />
                      </div>
                    `:j}
                ${s?F`<div class="duration-hint">${s}</div>`:j}
              </div>
            `:j}
      </div>
    `}static{this.styles=[Se,n`
      .time-selector {
        margin-bottom: 4px;
      }

      ha-select {
        min-width: 120px;
      }

      .custom-time-inputs {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 8px 0 4px;
        margin-left: 16px;
      }

      .custom-field {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .custom-label {
        font-size: 13px;
        color: var(--secondary-text-color);
        min-width: 70px;
      }

      .custom-field ha-select {
        min-width: 160px;
      }

      .custom-time-inputs input[type="number"] {
        width: 70px;
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      .duration-hint {
        font-size: 13px;
        color: var(--secondary-text-color);
        padding: 4px 0 0 16px;
        font-style: italic;
      }

      @media (max-width: 600px) {
        ha-select {
          width: 100%;
          box-sizing: border-box;
        }
      }
    `]}};e([he({attribute:!1})],ft.prototype,"hass",void 0),e([he({attribute:!1})],ft.prototype,"baseParam",void 0),e([he({attribute:!1})],ft.prototype,"factorParam",void 0),e([he({type:Number})],ft.prototype,"baseValue",void 0),e([he({type:Number})],ft.prototype,"factorValue",void 0),e([he({attribute:!1})],ft.prototype,"presets",void 0),e([he({type:Boolean})],ft.prototype,"modified",void 0),e([pe()],ft.prototype,"_isCustom",void 0),ft=e([we("hm-time-selector")],ft);let bt=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.senderAddress="",this.receiverAddress="",this.senderDeviceName="",this.senderDeviceModel="",this.senderChannelTypeLabel="",this.receiverDeviceName="",this.receiverDeviceModel="",this.receiverChannelTypeLabel="",this.editable=!0,this._receiverSchema=null,this._senderSchema=null,this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._loading=!0,this._saving=!1,this._error="",this._validationErrors={},this._senderValidationErrors={},this._profiles=null,this._activeProfileId=0,this._selectedProfileId=0,this._testing=!1,this._activeKeypressTab="short"}updated(e){(e.has("senderAddress")||e.has("receiverAddress")||e.has("entryId"))&&this.entryId&&this.senderAddress&&this.receiverAddress&&this._fetchSchemas()}async _fetchSchemas(){this._loading=!0,this._error="",this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._validationErrors={},this._senderValidationErrors={};try{const[e,t,i]=await Promise.all([Pe(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress),Pe(this.hass,this.entryId,this.interfaceId,this.receiverAddress,this.senderAddress).catch(()=>null),ze(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress)]);this._receiverSchema=e,this._senderSchema=t,this._profiles=i?.profiles??null,this._activeProfileId=i?.active_profile_id??0,this._selectedProfileId=this._activeProfileId}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}get _isDirty(){return this._receiverPendingChanges.size>0||this._senderPendingChanges.size>0}get _filteredReceiverSchema(){if(!this._receiverSchema||!this._profiles||0===this._selectedProfileId)return this._receiverSchema;const e=this._profiles.find(e=>e.id===this._selectedProfileId);if(!e)return this._receiverSchema;const t=new Set(e.editable_params),i=this._receiverSchema.sections.map(e=>({...e,parameters:e.parameters.filter(e=>t.has(e.id))})).filter(e=>e.parameters.length>0);return{...this._receiverSchema,sections:i}}get _groupedReceiverParams(){const e=this._filteredReceiverSchema;if(!e)return null;const t=e.sections.flatMap(e=>e.parameters);return t.some(e=>e.keypress_group)?{short:t.filter(e=>"short"===e.keypress_group),long:t.filter(e=>"long"===e.keypress_group),common:t.filter(e=>"common"===e.keypress_group||!e.keypress_group)}:null}_getEffectiveValue(e){return this._receiverPendingChanges.has(e.id)?this._receiverPendingChanges.get(e.id):e.current_value}_isModified(e){return this._receiverPendingChanges.has(e.id)}_emitReceiverChange(e,t){const i=this._findParameter(e),s=i?.current_value;t===s?this._receiverPendingChanges.delete(e):this._receiverPendingChanges.set(e,t),this._receiverPendingChanges=new Map(this._receiverPendingChanges)}_handleProfileChange(e){e.stopPropagation();const t=parseInt(e.detail.value,10);if(Number.isNaN(t)||t===this._selectedProfileId)return;if(this._selectedProfileId=t,0===t||!this._profiles)return;const i=this._profiles.find(e=>e.id===t);if(!i)return;const s=new Map;for(const[e,t]of Object.entries(i.fixed_params)){const i=this._findParameter(e);i&&i.current_value!==t&&s.set(e,t)}for(const[e,t]of Object.entries(i.default_values)){const i=this._findParameter(e);i&&i.current_value!==t&&s.set(e,t)}this._receiverPendingChanges=s}async _handleTestProfile(){if(!this._testing&&0!==this._selectedProfileId){this._testing=!0;try{await async function(e,t,i,s,a,r){return e.callWS({type:"homematicip_local/config/test_link_profile",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a,profile_id:r})}(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress,this._selectedProfileId),rt(this,{message:this._l("link_config.test_profile_success")})}catch{rt(this,{message:this._l("link_config.test_profile_failed")})}finally{this._testing=!1}}}_handleReceiverValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;i===s?this._receiverPendingChanges.delete(t):this._receiverPendingChanges.set(t,i),this._receiverPendingChanges=new Map(this._receiverPendingChanges)}_handleSenderValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;i===s?this._senderPendingChanges.delete(t):this._senderPendingChanges.set(t,i),this._senderPendingChanges=new Map(this._senderPendingChanges)}_handleDiscard(){this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._validationErrors={},this._senderValidationErrors={},this._selectedProfileId=this._activeProfileId}async _handleSave(){if(!this._isDirty||this._saving)return;const e=[...this._receiverPendingChanges.entries(),...this._senderPendingChanges.entries()],t=e.length,i=e.map(([e,t])=>{const i=this._findParameter(e);return`${i?.label??e}: ${i?.current_value??"?"} → ${t}`}).join("\n");if(await st(0,{title:this._l("link_config.confirm_save_title"),text:`${this._l("link_config.confirm_save_text",{count:t})}\n\n${i}`,confirmText:this._l("common.save"),dismissText:this._l("common.cancel")})){this._saving=!0,this._validationErrors={},this._senderValidationErrors={};try{const e=[];this._receiverPendingChanges.size>0&&e.push(Le(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress,Object.fromEntries(this._receiverPendingChanges))),this._senderPendingChanges.size>0&&e.push(Le(this.hass,this.entryId,this.interfaceId,this.receiverAddress,this.senderAddress,Object.fromEntries(this._senderPendingChanges))),await Promise.all(e),this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,rt(this,{message:this._l("link_config.save_success")}),await this._fetchSchemas()}catch(e){this._error=String(e),rt(this,{message:this._l("link_config.save_failed")})}finally{this._saving=!1}}}_findParameter(e){for(const t of[this._receiverSchema,this._senderSchema])if(t)for(const i of t.sections){const t=i.parameters.find(t=>t.id===e);if(t)return t}}async _handleBack(){this._isDirty&&!await st(0,{title:this._l("link_config.unsaved_title"),text:this._l("link_config.unsaved_warning"),confirmText:this._l("link_config.discard"),dismissText:this._l("common.cancel"),destructive:!0})||this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_hasReceiverParams(){return(this._filteredReceiverSchema?.sections.length??0)>0}_hasSenderParams(){return(this._senderSchema?.sections.length??0)>0}_renderProfileSelector(){if(!this._profiles)return j;const e=this._profiles.find(e=>e.id===this._selectedProfileId),t=e?.description||"";return F`
      <div class="profile-selector">
        <div class="profile-selector-row">
          <ha-select
            .label=${this._l("link_config.profile")}
            .value=${String(this._selectedProfileId)}
            .options=${this._profiles.map(e=>({value:String(e.id),label:e.name}))}
            @selected=${this._handleProfileChange}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
          ${this._selectedProfileId>0?F`
                <ha-button @click=${this._handleTestProfile} .disabled=${this._testing}>
                  ${this._l(this._testing?"common.loading":"link_config.test_profile")}
                </ha-button>
              `:j}
        </div>
        ${t?F`<p class="profile-description">${t}</p>`:j}
      </div>
    `}_renderParamList(e){const t=new Map,i=[];for(const s of e)if(s.time_pair_id&&s.id.toUpperCase().endsWith("_TIME_BASE")){const e=t.get(s.time_pair_id)??{};e.base=s,t.set(s.time_pair_id,e)}else if(s.time_pair_id&&s.id.toUpperCase().endsWith("_TIME_FACTOR")){const e=t.get(s.time_pair_id)??{};e.factor=s,t.set(s.time_pair_id,e)}else s.hidden_by_default&&0!==this._selectedProfileId||i.push(s);return F`
      ${[...t.entries()].map(([,e])=>e.base&&e.factor?F`
              <hm-time-selector
                .hass=${this.hass}
                .baseParam=${e.base}
                .factorParam=${e.factor}
                .baseValue=${this._getEffectiveValue(e.base)}
                .factorValue=${this._getEffectiveValue(e.factor)}
                .presets=${e.base.time_presets??[]}
                .modified=${this._isModified(e.base)||this._isModified(e.factor)}
                @value-changed=${this._handleReceiverValueChanged}
              ></hm-time-selector>
            `:j)}
      ${i.map(e=>e.display_as_percent&&e.has_last_value?this._renderLevelParam(e):F`
              <hm-form-parameter
                .hass=${this.hass}
                .parameter=${e}
                .value=${this._getEffectiveValue(e)}
                .modified=${this._isModified(e)}
                @value-changed=${this._handleReceiverValueChanged}
              ></hm-form-parameter>
            `)}
    `}_renderLevelParam(e){const t=this._getEffectiveValue(e),i=t>1,s=i?100:Math.round(100*t);return F`
      <div class="level-param">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e.label}
            ${this._isModified(e)?F`<span class="modified-dot"></span>`:j}
          </div>
          <div class="parameter-control level-controls">
            <label class="last-value-toggle">
              <ha-checkbox
                .checked=${i}
                @change=${t=>{this._emitReceiverChange(e.id,t.target.checked?1.005:1)}}
              ></ha-checkbox>
              ${this._l("link_config.last_value")}
            </label>
            ${i?j:F`
                  <div class="slider-group">
                    <input
                      type="range"
                      min="0"
                      max="100"
                      step="1"
                      .value=${String(s)}
                      @input=${t=>{const i=Number(t.target.value);this._emitReceiverChange(e.id,i/100)}}
                    />
                    <span class="percent-display">${s}%</span>
                  </div>
                `}
          </div>
        </div>
      </div>
    `}_renderReceiverParams(){const e=this._groupedReceiverParams;if(e){const t=e.short.length>0,i=e.long.length>0,s=t&&i;return F`
        <div class="param-section">
          <h3>${this._l("link_config.receiver_params")}</h3>
          ${s?F`
                <div class="keypress-tabs" role="tablist">
                  <div
                    class="tab ${"short"===this._activeKeypressTab?"active":""}"
                    role="tab"
                    tabindex=${"short"===this._activeKeypressTab?"0":"-1"}
                    aria-selected=${"short"===this._activeKeypressTab}
                    @click=${()=>{this._activeKeypressTab="short"}}
                    @keydown=${e=>{"ArrowRight"!==e.key&&"ArrowLeft"!==e.key||(e.preventDefault(),this._activeKeypressTab="short"===this._activeKeypressTab?"long":"short",this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector('.tab[aria-selected="true"]');e?.focus()}))}}
                  >
                    ${this._l("link_config.short_keypress")}
                  </div>
                  <div
                    class="tab ${"long"===this._activeKeypressTab?"active":""}"
                    role="tab"
                    tabindex=${"long"===this._activeKeypressTab?"0":"-1"}
                    aria-selected=${"long"===this._activeKeypressTab}
                    @click=${()=>{this._activeKeypressTab="long"}}
                    @keydown=${e=>{"ArrowRight"!==e.key&&"ArrowLeft"!==e.key||(e.preventDefault(),this._activeKeypressTab="short"===this._activeKeypressTab?"long":"short",this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector('.tab[aria-selected="true"]');e?.focus()}))}}
                  >
                    ${this._l("link_config.long_keypress")}
                  </div>
                </div>
                <div class="keypress-params" role="tabpanel">
                  ${this._renderParamList("short"===this._activeKeypressTab?e.short:e.long)}
                </div>
              `:t?this._renderParamList(e.short):i?this._renderParamList(e.long):j}
          ${e.common.length>0?F` <div class="common-params">${this._renderParamList(e.common)}</div> `:j}
        </div>
      `}return F`
      <div class="param-section">
        <h3>${this._l("link_config.receiver_params")}</h3>
        <hm-config-form
          .hass=${this.hass}
          .schema=${this._filteredReceiverSchema}
          .pendingChanges=${this._receiverPendingChanges}
          .validationErrors=${this._validationErrors}
          @value-changed=${this._handleReceiverValueChanged}
        ></hm-config-form>
      </div>
    `}render(){return this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:!this._error||this._receiverSchema||this._senderSchema?F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="config-header">
        <h2>${this._l("link_config.title")}</h2>
        <div class="link-info-bar">
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.sender")}</span>
            <span class="link-device-name">
              ${this.senderChannelTypeLabel||this.senderDeviceName}
            </span>
            ${this.senderDeviceName?F`<span class="link-device-detail">
                  ${this.senderDeviceName} &middot; ${this.senderDeviceModel}
                </span>`:j}
            <span class="link-address">${this.senderAddress}</span>
          </div>
          <ha-icon class="link-direction-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.receiver")}</span>
            <span class="link-device-name">
              ${this.receiverChannelTypeLabel||this.receiverDeviceName}
            </span>
            ${this.receiverDeviceName?F`<span class="link-device-detail">
                  ${this.receiverDeviceName} &middot; ${this.receiverDeviceModel}
                </span>`:j}
            <span class="link-address">${this.receiverAddress}</span>
          </div>
        </div>
      </div>

      ${this._error?F`<div class="error">${this._error}</div>`:j}
      ${this._renderProfileSelector()}
      ${this._hasReceiverParams()?this._renderReceiverParams():j}
      ${this._hasSenderParams()?F`
            <div class="param-section">
              <h3>${this._l("link_config.sender_params")}</h3>
              <hm-config-form
                .hass=${this.hass}
                .schema=${this._senderSchema}
                .pendingChanges=${this._senderPendingChanges}
                .validationErrors=${this._senderValidationErrors}
                @value-changed=${this._handleSenderValueChanged}
              ></hm-config-form>
            </div>
          `:j}
      ${this._hasReceiverParams()||this._hasSenderParams()?j:F`<div class="empty-state">${this._l("link_config.no_params")}</div>`}
      ${this.editable?F`
            <div class="action-bar action-bar-sticky">
              <ha-button
                outlined
                @click=${this._handleDiscard}
                .disabled=${!this._isDirty||this._saving}
              >
                ${this._l("link_config.discard")}
              </ha-button>
              <ha-button
                raised
                @click=${this._handleSave}
                .disabled=${!this._isDirty||this._saving}
              >
                ${this._l(this._saving?"channel_config.saving":"common.save")}
              </ha-button>
            </div>
          `:j}
    `:F`<div class="error">
        ${this._error}
        <br />
        <ha-button outlined @click=${this._fetchSchemas}> ${this._l("common.retry")} </ha-button>
      </div>`}static{this.styles=[Se,n`
      .config-header {
        margin-bottom: 16px;
      }

      .config-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .link-info-bar {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 8px;
        margin-top: 8px;
      }

      .link-endpoint {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .link-label {
        font-size: 11px;
        text-transform: uppercase;
        color: var(--secondary-text-color);
        font-weight: 500;
      }

      .link-device-name {
        font-size: 14px;
        font-weight: 500;
      }

      .link-device-detail {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .link-address {
        font-family: monospace;
        font-size: 13px;
        color: var(--secondary-text-color);
        overflow-wrap: break-word;
        word-break: break-all;
      }

      .link-direction-arrow {
        --ha-icon-display-size: 24px;
        color: var(--primary-color, #03a9f4);
        flex-shrink: 0;
      }

      .profile-selector {
        margin: 16px 0;
        padding: 12px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 8px;
      }

      .profile-selector-row {
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .profile-selector-row ha-select {
        flex: 1;
      }

      .profile-description {
        margin: 8px 0 0;
        font-size: 13px;
        color: var(--secondary-text-color);
        line-height: 1.4;
      }

      .param-section {
        margin-bottom: 24px;
      }

      .param-section h3 {
        font-size: 16px;
        font-weight: 500;
        margin: 16px 0 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--divider-color, #e0e0e0);
      }

      .empty-state {
        padding: 24px;
        text-align: center;
        color: var(--secondary-text-color);
      }

      /* Keypress tabs */
      .keypress-tabs {
        display: flex;
        gap: 0;
        margin-bottom: 16px;
        border-bottom: 2px solid var(--divider-color, #e0e0e0);
      }

      .tab {
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 500;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        cursor: pointer;
        color: var(--secondary-text-color);
        transition:
          color 0.2s,
          border-color 0.2s;
        user-select: none;
      }

      .tab:hover,
      .tab:focus-visible {
        color: var(--primary-text-color);
      }

      .tab:focus-visible {
        outline: 2px solid var(--primary-color, #03a9f4);
        outline-offset: -2px;
      }

      .tab.active {
        color: var(--primary-color, #03a9f4);
        border-bottom-color: var(--primary-color, #03a9f4);
      }

      .keypress-params {
        padding: 4px 0;
        animation: fadeIn 0.15s ease-out;
      }

      @keyframes fadeIn {
        from {
          opacity: 0;
        }
        to {
          opacity: 1;
        }
      }

      .common-params {
        margin-top: 16px;
        padding-top: 12px;
        border-top: 1px solid var(--divider-color, #e0e0e0);
      }

      /* Level parameter */
      .level-param .level-controls {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: none;
      }

      .last-value-toggle {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        cursor: pointer;
      }

      .last-value-toggle ha-checkbox {
        margin: -8px 0;
      }

      .slider-group {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .slider-group input[type="range"] {
        flex: 1;
        min-width: 80px;
      }

      .percent-display {
        font-size: 14px;
        font-weight: 500;
        min-width: 40px;
        text-align: right;
      }

      @media (max-width: 600px) {
        .link-info-bar {
          flex-direction: column;
          align-items: flex-start;
          gap: 8px;
        }

        .link-direction-arrow {
          align-self: center;
        }

        .keypress-tabs {
          width: 100%;
        }

        .tab {
          flex: 1;
          text-align: center;
        }
      }
    `]}};e([he({attribute:!1})],bt.prototype,"hass",void 0),e([he()],bt.prototype,"entryId",void 0),e([he()],bt.prototype,"interfaceId",void 0),e([he()],bt.prototype,"senderAddress",void 0),e([he()],bt.prototype,"receiverAddress",void 0),e([he()],bt.prototype,"senderDeviceName",void 0),e([he()],bt.prototype,"senderDeviceModel",void 0),e([he()],bt.prototype,"senderChannelTypeLabel",void 0),e([he()],bt.prototype,"receiverDeviceName",void 0),e([he()],bt.prototype,"receiverDeviceModel",void 0),e([he()],bt.prototype,"receiverChannelTypeLabel",void 0),e([he({type:Boolean})],bt.prototype,"editable",void 0),e([pe()],bt.prototype,"_receiverSchema",void 0),e([pe()],bt.prototype,"_senderSchema",void 0),e([pe()],bt.prototype,"_receiverPendingChanges",void 0),e([pe()],bt.prototype,"_senderPendingChanges",void 0),e([pe()],bt.prototype,"_loading",void 0),e([pe()],bt.prototype,"_saving",void 0),e([pe()],bt.prototype,"_error",void 0),e([pe()],bt.prototype,"_validationErrors",void 0),e([pe()],bt.prototype,"_senderValidationErrors",void 0),e([pe()],bt.prototype,"_profiles",void 0),e([pe()],bt.prototype,"_activeProfileId",void 0),e([pe()],bt.prototype,"_selectedProfileId",void 0),e([pe()],bt.prototype,"_testing",void 0),e([pe()],bt.prototype,"_activeKeypressTab",void 0),bt=e([we("hm-link-config")],bt);let yt=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this._step="select-channel",this._device=null,this._selectedChannel="",this._selectedRole="sender",this._selectedPeer="",this._linkName="",this._linkableChannels=[],this._filteredChannels=[],this._searchQuery="",this._loading=!1,this._error=""}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this.deviceAddress&&this._fetchDevice()}async _fetchDevice(){this._loading=!0;try{const e=await Ae(this.hass,this.entryId);this._device=e.find(e=>e.address===this.deviceAddress)??null}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}_getStepIndex(){switch(this._step){case"select-channel":return 0;case"select-peer":return 1;case"confirm":return 2}}_renderProgressSteps(){const e=this._getStepIndex();return F`${[1,2,3].map((t,i)=>F`
        ${i>0?F`<div class="progress-line ${i<e?"completed":""}"></div>`:j}
        <div class="progress-step ${i<e?"completed":i===e?"active":""}">
          <span class="progress-dot">${t}</span>
        </div>
      `)}`}_handleBack(){if("select-peer"===this._step)return this._step="select-channel",this._selectedPeer="",this._linkableChannels=[],this._filteredChannels=[],void(this._searchQuery="");"confirm"!==this._step?this._handleCancel():this._step="select-peer"}_handleCancel(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_getLinkableChannels(){return this._device?this._device.channels.filter(e=>!e.address.endsWith(":0")&&e.paramset_keys.includes("LINK")):[]}_handleSelectChannel(e){this._selectedChannel=e}async _handleNextToSelectPeer(){this._selectedChannel&&(this._step="select-peer",await this._fetchLinkableChannels())}async _fetchLinkableChannels(){this._loading=!0,this._error="",this._linkableChannels=[],this._filteredChannels=[],this._searchQuery="";try{this._linkableChannels=await async function(e,t,i,s,a){return(await e.callWS({type:"homematicip_local/config/get_linkable_channels",entry_id:t,interface_id:i,channel_address:s,role:a})).channels}(this.hass,this.entryId,this.interfaceId,this._selectedChannel,this._selectedRole),this._filteredChannels=this._linkableChannels}catch(e){this._error=String(e)}finally{this._loading=!1}}async _handleRoleChange(e){this._selectedRole=e,this._selectedPeer="",await this._fetchLinkableChannels()}_handleSearchInput(e){const t=e.target.value.toLowerCase();this._searchQuery=t,this._filteredChannels=t?this._linkableChannels.filter(e=>e.address.toLowerCase().includes(t)||e.device_name.toLowerCase().includes(t)||e.device_model.toLowerCase().includes(t)||e.channel_type.toLowerCase().includes(t)||e.channel_name&&e.channel_name.toLowerCase().includes(t)):this._linkableChannels}_handleSelectPeer(e){this._selectedPeer=e}_handleNextToConfirm(){this._selectedPeer&&(this._linkName="",this._step="confirm")}async _handleCreate(){this._loading=!0;try{const e="sender"===this._selectedRole?this._selectedChannel:this._selectedPeer,t="sender"===this._selectedRole?this._selectedPeer:this._selectedChannel;await async function(e,t,i,s,a){return e.callWS({type:"homematicip_local/config/add_link",entry_id:t,sender_channel_address:i,receiver_channel_address:s,...a&&{name:a}})}(this.hass,this.entryId,e,t,this._linkName||void 0),rt(this,{message:this._l("add_link.create_success")}),this.dispatchEvent(new CustomEvent("link-created",{bubbles:!0,composed:!0}))}catch{rt(this,{message:this._l("add_link.create_failed")})}finally{this._loading=!1}}render(){return this._loading&&!this._device?F`<div class="loading">${this._l("common.loading")}</div>`:F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("select-channel"===this._step?"common.back":"add_link.back")}
      ></ha-icon-button>

      <div class="wizard-header">
        <h2>${this._l("add_link.title")}</h2>
        <div class="wizard-progress">${this._renderProgressSteps()}</div>
      </div>

      ${this._error?F`<div class="error">${this._error}</div>`:j}
      ${"select-channel"===this._step?this._renderStepChannel():"select-peer"===this._step?this._renderStepPeer():this._renderStepConfirm()}
    `}_renderStepChannel(){const e=this._getLinkableChannels();return F`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_channel")}</div>
        <div class="step-description">${this._l("add_link.select_channel")}</div>

        <div class="radio-list">
          ${0===e.length?F`<div class="empty-state">${this._l("add_link.no_compatible")}</div>`:e.map(e=>{const t=this._selectedChannel===e.address,i=e.address.split(":").pop()??"",s=e.channel_name&&e.channel_name!==e.channel_type_label;return F`
                  <div
                    class="radio-option ${t?"selected":""}"
                    role="radio"
                    tabindex="0"
                    aria-checked=${t}
                    @click=${()=>this._handleSelectChannel(e.address)}
                    @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._handleSelectChannel(e.address))}}
                  >
                    <ha-radio name="channel" .checked=${t}></ha-radio>
                    <div class="radio-content">
                      <div class="radio-title">
                        ${s?e.channel_name:`${e.channel_type_label} :${i}`}
                      </div>
                      <div class="radio-subtitle">
                        ${s?`${e.channel_type_label} · `:""}${e.address}
                      </div>
                    </div>
                  </div>
                `})}
        </div>

        ${e.length>0?F`
              <div class="wizard-actions">
                <ha-button
                  raised
                  .disabled=${!this._selectedChannel}
                  @click=${this._handleNextToSelectPeer}
                >
                  ${this._l("add_link.next")}
                  <ha-icon slot="trailingIcon" .icon=${"mdi:chevron-right"}></ha-icon>
                </ha-button>
              </div>
            `:j}
      </div>
    `}_renderStepPeer(){return F`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_peer")}</div>

        <div class="role-selector">
          <span class="role-label">${this._l("add_link.select_role")}</span>
          <div class="role-buttons">
            <ha-button
              .raised=${"sender"===this._selectedRole}
              .outlined=${"sender"!==this._selectedRole}
              @click=${()=>this._handleRoleChange("sender")}
            >
              ${this._l("add_link.role_sender")}
            </ha-button>
            <ha-button
              .raised=${"receiver"===this._selectedRole}
              .outlined=${"receiver"!==this._selectedRole}
              @click=${()=>this._handleRoleChange("receiver")}
            >
              ${this._l("add_link.role_receiver")}
            </ha-button>
          </div>
        </div>

        ${this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:F`
              <div class="search-box">
                <input
                  type="text"
                  .value=${this._searchQuery}
                  @input=${this._handleSearchInput}
                  placeholder="${this._l("add_link.search_devices")}"
                  aria-label="${this._l("add_link.search_devices")}"
                />
              </div>

              <div class="radio-list">
                ${0===this._filteredChannels.length?F`<div class="empty-state">${this._l("add_link.no_compatible")}</div>`:this._filteredChannels.map(e=>{const t=this._selectedPeer===e.address,i=e.address.split(":").pop()??"";return F`
                        <div
                          class="radio-option ${t?"selected":""}"
                          role="radio"
                          tabindex="0"
                          aria-checked=${t}
                          @click=${()=>this._handleSelectPeer(e.address)}
                          @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._handleSelectPeer(e.address))}}
                        >
                          <ha-radio name="peer" .checked=${t}></ha-radio>
                          <div class="radio-content">
                            <div class="radio-title">
                              ${e.channel_name&&e.channel_name!==e.channel_type_label?e.channel_name:`${e.channel_type_label} :${i}`}
                              — ${e.device_name}
                            </div>
                            <div class="radio-subtitle">${e.device_model} · ${e.address}</div>
                          </div>
                        </div>
                      `})}
              </div>

              ${this._filteredChannels.length>0?F`
                    <div class="wizard-actions">
                      <ha-button outlined @click=${this._handleCancel}>
                        ${this._l("common.cancel")}
                      </ha-button>
                      <ha-button
                        raised
                        .disabled=${!this._selectedPeer}
                        @click=${this._handleNextToConfirm}
                      >
                        ${this._l("add_link.next")}
                        <ha-icon slot="trailingIcon" .icon=${"mdi:chevron-right"}></ha-icon>
                      </ha-button>
                    </div>
                  `:j}
            `}
      </div>
    `}_renderStepConfirm(){const e="sender"===this._selectedRole?this._selectedChannel:this._selectedPeer,t="sender"===this._selectedRole?this._selectedPeer:this._selectedChannel,i=this._resolveName(e),s=this._resolveName(t);return F`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_confirm")}</div>

        <div class="link-summary">
          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l("link_config.sender")}</div>
            <div class="link-endpoint-name">${i}</div>
            <div class="link-endpoint-address">${e}</div>
          </div>

          <ha-icon class="link-direction-arrow" .icon=${"mdi:arrow-right"}></ha-icon>

          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l("link_config.receiver")}</div>
            <div class="link-endpoint-name">${s}</div>
            <div class="link-endpoint-address">${t}</div>
          </div>
        </div>

        <div class="name-input">
          <label for="link-name">${this._l("add_link.link_name")}</label>
          <input
            id="link-name"
            type="text"
            .value=${this._linkName}
            @input=${e=>{this._linkName=e.target.value}}
            placeholder="${e} -> ${t}"
          />
        </div>

        <div class="wizard-actions">
          <ha-button outlined @click=${this._handleCancel}> ${this._l("common.cancel")} </ha-button>
          <ha-button raised .disabled=${this._loading} @click=${this._handleCreate}>
            ${this._l(this._loading?"common.loading":"add_link.create")}
          </ha-button>
        </div>
      </div>
    `}_resolveName(e){const t=e.split(":").pop()??"";if(this._device&&e.startsWith(this.deviceAddress)){const i=this._device.channels.find(t=>t.address===e);return`${i?.channel_name&&i.channel_name!==i.channel_type_label?i.channel_name:`${i?.channel_type_label||"?"} :${t}`} — ${this._device.name}`}const i=this._linkableChannels.find(t=>t.address===e);return i?`${i.channel_name&&i.channel_name!==i.channel_type_label?i.channel_name:`${i.channel_type_label} :${t}`} — ${i.device_name}`:e}static{this.styles=[Se,n`
      .wizard-header {
        margin-bottom: 16px;
      }

      .wizard-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .wizard-progress {
        display: flex;
        align-items: center;
        gap: 0;
        margin-top: 12px;
        margin-bottom: 8px;
      }

      .progress-step {
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .progress-dot {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 500;
        border: 2px solid var(--divider-color, #e0e0e0);
        background: var(--card-background-color, #fff);
        color: var(--secondary-text-color);
        transition: all 0.2s;
      }

      .progress-step.active .progress-dot {
        border-color: var(--primary-color, #03a9f4);
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }

      .progress-step.completed .progress-dot {
        border-color: var(--primary-color, #03a9f4);
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }

      .progress-line {
        flex: 1;
        height: 2px;
        background: var(--divider-color, #e0e0e0);
        transition: background 0.2s;
      }

      .progress-line.completed {
        background: var(--primary-color, #03a9f4);
      }

      .wizard-step {
        padding: 0;
      }

      .step-indicator {
        font-size: 13px;
        color: var(--secondary-text-color);
        margin-bottom: 4px;
        font-weight: 500;
      }

      .step-description {
        font-size: 14px;
        margin-bottom: 16px;
      }

      .role-selector {
        margin-bottom: 16px;
      }

      .role-label {
        font-size: 14px;
        display: block;
        margin-bottom: 8px;
      }

      .role-buttons {
        display: flex;
        gap: 8px;
      }

      .role-buttons ha-button {
        flex: 1;
      }

      .search-box {
        margin-bottom: 12px;
      }

      .search-box input {
        width: 100%;
        box-sizing: border-box;
        padding: 10px 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        font-family: inherit;
        background: var(--primary-background-color);
        color: var(--primary-text-color);
      }

      .search-box input:focus {
        outline: none;
        border-color: var(--primary-color, #03a9f4);
      }

      .radio-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 400px;
        overflow-y: auto;
      }

      .radio-option {
        display: flex;
        align-items: center;
        padding: 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        cursor: pointer;
        transition: border-color 0.15s;
      }

      .radio-option:hover,
      .radio-option:focus-visible {
        border-color: var(--primary-color, #03a9f4);
      }

      .radio-option:focus-visible {
        outline: 2px solid var(--primary-color, #03a9f4);
        outline-offset: -2px;
      }

      .radio-option.selected {
        border-color: var(--primary-color, #03a9f4);
        background: rgba(3, 169, 244, 0.05);
      }

      .radio-option ha-radio {
        margin-right: 4px;
        flex-shrink: 0;
      }

      .radio-content {
        min-width: 0;
      }

      .radio-title {
        font-size: 14px;
        font-weight: 500;
      }

      .radio-subtitle {
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 2px;
        font-family: monospace;
      }

      .link-summary {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding: 24px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 8px;
        margin-bottom: 16px;
      }

      .link-endpoint {
        text-align: center;
      }

      .link-endpoint-label {
        font-size: 11px;
        text-transform: uppercase;
        color: var(--secondary-text-color);
        font-weight: 500;
        margin-bottom: 4px;
      }

      .link-endpoint-address {
        font-family: monospace;
        font-size: 15px;
        font-weight: 500;
      }

      .link-endpoint-name {
        font-size: 13px;
        color: var(--secondary-text-color);
        margin-top: 2px;
      }

      .link-direction-arrow {
        --ha-icon-display-size: 28px;
        color: var(--primary-color, #03a9f4);
      }

      .name-input {
        margin-bottom: 16px;
      }

      .name-input label {
        display: block;
        font-size: 14px;
        margin-bottom: 6px;
        color: var(--secondary-text-color);
      }

      .name-input input {
        width: 100%;
        box-sizing: border-box;
        padding: 10px 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        font-family: inherit;
        background: var(--primary-background-color);
        color: var(--primary-text-color);
      }

      .name-input input:focus {
        outline: none;
        border-color: var(--primary-color, #03a9f4);
      }

      .wizard-actions {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid var(--divider-color, #e0e0e0);
      }

      @media (max-width: 600px) {
        .role-buttons {
          flex-direction: column;
        }

        .link-summary {
          padding: 16px;
        }
      }
    `]}};function xt(e){return t=>(customElements.get(e)||customElements.define(e,t),t)}e([he({attribute:!1})],yt.prototype,"hass",void 0),e([he()],yt.prototype,"entryId",void 0),e([he()],yt.prototype,"interfaceId",void 0),e([he()],yt.prototype,"deviceAddress",void 0),e([pe()],yt.prototype,"_step",void 0),e([pe()],yt.prototype,"_device",void 0),e([pe()],yt.prototype,"_selectedChannel",void 0),e([pe()],yt.prototype,"_selectedRole",void 0),e([pe()],yt.prototype,"_selectedPeer",void 0),e([pe()],yt.prototype,"_linkName",void 0),e([pe()],yt.prototype,"_linkableChannels",void 0),e([pe()],yt.prototype,"_filteredChannels",void 0),e([pe()],yt.prototype,"_searchQuery",void 0),e([pe()],yt.prototype,"_loading",void 0),e([pe()],yt.prototype,"_error",void 0),yt=e([we("hm-add-link")],yt);const $t=(e,t,i)=>{const s=new Map;for(let a=t;a<=i;a++)s.set(e[a],a);return s},kt=_e(class extends ue{constructor(e){if(super(e),2!==e.type)throw Error("repeat() can only be used in text expressions")}dt(e,t,i){let s;void 0===i?i=t:void 0!==t&&(s=t);const a=[],r=[];let n=0;for(const t of e)a[n]=s?s(t,n):n,r[n]=i(t,n),n++;return{values:r,keys:a}}render(e,t,i){return this.dt(e,t,i).values}update(e,[t,i,s]){const a=(e=>e._$AH)(e),{values:r,keys:n}=this.dt(t,i,s);if(!Array.isArray(a))return this.ut=n,r;const o=this.ut??=[],l=[];let d,c,h=0,p=a.length-1,_=0,u=r.length-1;for(;h<=p&&_<=u;)if(null===a[h])h++;else if(null===a[p])p--;else if(o[h]===n[_])l[_]=be(a[h],r[_]),h++,_++;else if(o[p]===n[u])l[u]=be(a[p],r[u]),p--,u--;else if(o[h]===n[u])l[u]=be(a[h],r[u]),fe(e,l[u+1],a[h]),h++,u--;else if(o[p]===n[_])l[_]=be(a[p],r[_]),fe(e,a[h],a[p]),p--,_++;else if(void 0===d&&(d=$t(n,_,u),c=$t(o,h,p)),d.has(o[h]))if(d.has(o[p])){const t=c.get(n[_]),i=void 0!==t?a[t]:null;if(null===i){const t=fe(e,a[h]);be(t,r[_]),l[_]=t}else l[_]=be(i,r[_]),fe(e,a[h],i),a[t]=null;_++}else $e(a[p]),p--;else $e(a[h]),h++;for(;_<=u;){const t=fe(e,l[u+1]);be(t,r[_]),l[_++]=t}for(;h<=p;){const e=a[h++];null!==e&&$e(e)}return this.ut=n,xe(e,l),O}}),wt=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"],St=["fixed_time","astro","fixed_if_before_astro","astro_if_before_fixed","fixed_if_after_astro","astro_if_after_fixed","earliest","latest"],Ct=["lock_autorelock_end","lock_autorelock_start","unlock_autorelock_end","autorelock_end"];function Et(e,t){return!t||0===t.length||t.includes(e)}const At={switch:{levelType:"binary",hasLevel2:!1,hasDuration:!0,hasRampTime:!1},light:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!0},cover:{levelType:"percentage",hasLevel2:!0,hasDuration:!1,hasRampTime:!1},valve:{levelType:"binary",hasLevel2:!1,hasDuration:!0,hasRampTime:!1},lock:{levelType:"binary",hasLevel2:!1,hasDuration:!1,hasRampTime:!1}},It=["ms","s","min","h"];function Dt(e){const[t,i]=e.split(":").map(Number);return 60*t+i}function Tt(e){const t=e%60;return`${Math.floor(e/60).toString().padStart(2,"0")}:${t.toString().padStart(2,"0")}`}function Mt(e,t="24"){if("24"===t)return e;const[i,s]=e.split(":");let a=parseInt(i,10);if(24===a)return"12:00 AM";const r=a>=12?"PM":"AM";return 0===a?a=12:a>12&&(a-=12),`${a}:${s||"00"} ${r}`}function Pt(e){return e<10?"#2b9af9":e<14?"#40c4ff":e<17?"#26c6da":e<19?"#66bb6a":e<21?"#9ccc65":e<23?"#ffb74d":e<25?"#ff8100":"#f4511e"}function Lt(e){const{base_temperature:t,periods:i}=e,s=[],a=[...i].sort((e,t)=>Dt(e.starttime)-Dt(t.starttime));for(let e=0;e<a.length;e++){const t=a[e];s.push({startTime:t.starttime,startMinutes:Dt(t.starttime),endTime:t.endtime,endMinutes:Dt(t.endtime),temperature:t.temperature,slot:e+1})}return{blocks:s,baseTemperature:t}}function zt(e,t){const i=[],s=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of s)i.push({starttime:e.startTime,endtime:e.endTime,temperature:e.temperature});return{base_temperature:t,periods:i}}function Nt(e){if(0===e.length)return[];const t=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),i=[];let s={...t[0]};for(let e=1;e<t.length;e++){const a=t[e];s.endMinutes===a.startMinutes&&s.temperature===a.temperature?s={...s,endTime:a.endTime,endMinutes:a.endMinutes}:(i.push(s),s={...a})}return i.push(s),i.map((e,t)=>({...e,slot:t+1}))}function Rt(e,t){if(0===e.length)return[{startTime:"00:00",startMinutes:0,endTime:"24:00",endMinutes:1440,temperature:t,slot:1}];const i=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),s=[];let a=0;for(const e of i)e.startMinutes>a&&s.push({startTime:Tt(a),startMinutes:a,endTime:e.startTime,endMinutes:e.startMinutes,temperature:t,slot:s.length+1}),s.push({...e,slot:s.length+1}),a=e.endMinutes;return a<1440&&s.push({startTime:Tt(a),startMinutes:a,endTime:"24:00",endMinutes:1440,temperature:t,slot:s.length+1}),Nt(s)}function Vt(e){return[...e].sort((e,t)=>e.startMinutes-t.startMinutes).map((e,t)=>({...e,slot:t+1}))}function Bt(e){return Boolean(Array.isArray(e.weekdays)&&e.weekdays.length>0&&Array.isArray(e.target_channels)&&e.target_channels.length>0)}function Ut(e){return"fixed_time"!==e}const Ht=/^(\d+(?:\.\d+)?)\s*(ms|s|min|h)$/,Wt={ms:3e3,s:30,min:30,h:30};function Ft(e){return{max:Wt[e],step:"ms"===e?100:1}}function Ot(e){const t=e.trim().match(Ht);return t?{value:parseFloat(t[1]),unit:t[2]}:null}function jt(e,t){return`${e}${t}`}function Kt(e){const t=Ot(e);return!!t&&!(t.value<0)&&t.value<=Wt[t.unit]}function Yt(e){const t={weekdays:e.weekdays,time:e.time,target_channels:e.target_channels,level:e.level};return"fixed_time"!==e.condition&&(t.condition=e.condition),null!==e.astro_type&&(t.astro_type=e.astro_type),0!==e.astro_offset_minutes&&(t.astro_offset_minutes=e.astro_offset_minutes),null!==e.level_2&&(t.level_2=e.level_2),null!==e.duration&&(t.duration=e.duration),null!==e.ramp_time&&(t.ramp_time=e.ramp_time),null!==e.lock_mode&&(t.lock_mode=e.lock_mode),null!==e.lock_action&&(t.lock_action=e.lock_action),null!==e.permission&&(t.permission=e.permission),t}function Gt(e){const t={};for(const[i,s]of Object.entries(e))t[i]=Yt(s);return t}function Zt(e,t=5,i=30.5){const{base_temperature:s,periods:a}=e;if(s<t||s>i)return{key:"temperatureOutOfRange",params:{block:"base",min:`${t}`,max:`${i}`}};let r=0;for(let e=0;e<a.length;e++){const s=a[e];if(!s.starttime||!s.endtime||void 0===s.temperature)return{key:"slotMissingValues",params:{slot:`${e+1}`}};const n=Dt(s.starttime),o=Dt(s.endtime);if(o<=n)return{key:"blockEndBeforeStart",params:{block:`${e+1}`}};if(n<r)return{key:"slotTimeBackwards",params:{slot:`${e+1}`,time:s.starttime}};if(s.temperature<t||s.temperature>i)return{key:"temperatureOutOfRange",params:{block:`${e+1}`,min:`${t}`,max:`${i}`}};r=o}return null}const qt=n`
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
`;var Xt=function(e,t,i,s){var a,r=arguments.length,n=r<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n};let Qt=class extends oe{constructor(){super(...arguments),this.editable=!1,this.showTemperature=!0,this.showGradient=!1,this.temperatureUnit="°C",this.hourFormat="24",this.editorOpen=!1,this._currentTimePercent=0,this._currentTimeMinutes=0,this._isMobile=!1,this._mobileSelectedDayIndex=0,this._mediaHandler=e=>{this._isMobile=e.matches},this._touchStartX=0,this._touchStartY=0}connectedCallback(){super.connectedCallback(),this._updateCurrentTime(),this._timeUpdateInterval=window.setInterval(()=>{this._updateCurrentTime()},6e4),this._mediaQuery=window.matchMedia("(max-width: 600px)"),this._isMobile=this._mediaQuery.matches,this._mediaQuery.addEventListener("change",this._mediaHandler),this._initMobileSelectedDay()}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._timeUpdateInterval&&(clearInterval(this._timeUpdateInterval),this._timeUpdateInterval=void 0),this._mediaQuery&&(this._mediaQuery.removeEventListener("change",this._mediaHandler),this._mediaQuery=void 0)}willUpdate(e){super.willUpdate(e)}_updateCurrentTime(){const e=new Date,t=60*e.getHours()+e.getMinutes();this._currentTimePercent=t/1440*100,this._currentTimeMinutes=t;const i=e.getDay();this._currentWeekday=["SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY"][i]}_isBlockActive(e,t){return!(!this._currentWeekday||this._currentWeekday!==e)&&this._currentTimeMinutes>=t.startMinutes&&this._currentTimeMinutes<t.endMinutes}_getTimeLabels(){const e=[];for(let t=0;t<=24;t+=3){const i=`${t.toString().padStart(2,"0")}:00`;e.push({hour:t,label:Mt(i,this.hourFormat),position:t/24*100})}return e}_formatTimeDisplay(e){return Mt(e,this.hourFormat)}_getBaseTemperature(e){if(this.scheduleData){const t=this.scheduleData[e];if(t){const{baseTemperature:e}=Lt(t);return e}}return 20}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=Lt(t);return i}return[]}_getWeekdayLabel(e){return this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_handleWeekdayClick(e){this.editable&&this.dispatchEvent(new CustomEvent("weekday-click",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handleCopy(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("copy-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handlePaste(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("paste-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}_initMobileSelectedDay(){const e=(new Date).getDay();this._mobileSelectedDayIndex=0===e?6:e-1}_mobilePrevDay(){this._mobileSelectedDayIndex=(this._mobileSelectedDayIndex-1+wt.length)%wt.length}_mobileNextDay(){this._mobileSelectedDayIndex=(this._mobileSelectedDayIndex+1)%wt.length}_getWeekdayLongLabel(e){return this.translations?.weekdayLongLabels?.[e]??e.charAt(0)+e.slice(1).toLowerCase()}_handleTouchStart(e){this._touchStartX=e.touches[0].clientX,this._touchStartY=e.touches[0].clientY}_handleTouchEnd(e){const t=e.changedTouches[0].clientX-this._touchStartX,i=e.changedTouches[0].clientY-this._touchStartY;Math.abs(t)>50&&Math.abs(t)>1.5*Math.abs(i)&&(t<0?this._mobileNextDay():this._mobilePrevDay())}_renderTimeBlocks(e){const t=this._getParsedBlocks(e),i=this._getBaseTemperature(e),s=Rt(t,i);return F`
      <div
        class="time-blocks ${this.editable?"editable":""}"
        tabindex=${this.editable?"0":"-1"}
        role=${this.editable?"button":"presentation"}
        aria-label=${this._getWeekdayLabel(e)}
        @click=${()=>this._handleWeekdayClick(e)}
        @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._handleWeekdayClick(e))}}
      >
        ${kt(s,e=>`${e.slot}-${e.startMinutes}-${this.currentProfile}`,(a,r)=>{const n=this._isBlockActive(e,a),o=a.temperature===i&&!t.some(e=>e.startMinutes===a.startMinutes&&e.endMinutes===a.endMinutes);let l;if(o)l="background-color: var(--secondary-background-color, #e0e0e0);";else if(this.showGradient){l=`background: ${function(e,t,i){const s=Pt(e);return null===t&&null===i?s:null!==t&&null===i?`linear-gradient(to bottom, ${Pt(t)}, ${s})`:null===t&&null!==i?`linear-gradient(to bottom, ${s}, ${Pt(i)})`:`linear-gradient(to bottom, ${Pt(t)}, ${s} 50%, ${Pt(i)})`}(a.temperature,r>0?s[r-1].temperature:null,r<s.length-1?s[r+1].temperature:null)};`}else l=`background-color: ${Pt(a.temperature)};`;return F`
              <div
                class="time-block ${n?"active":""} ${o?"base-temp-block":""}"
                style="
                    height: ${(a.endMinutes-a.startMinutes)/1440*100}%;
                    ${l}
                  "
              >
                ${this.showTemperature?F`<span class="temperature">${a.temperature.toFixed(1)}°</span>`:""}
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
    `}_renderMobile(){const e=wt[this._mobileSelectedDayIndex],t=this.copiedWeekday===e;return F`
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
          ${kt(this._getTimeLabels(),e=>e.hour,e=>F`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `)}
        </div>

        <div class="mobile-day-content">
          ${this._renderTimeBlocks(e)}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen||this._currentWeekday!==e?"":F`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?F`
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
      ${this.editable?F`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `}_renderDesktop(){return F`
      <div class="schedule-container">
        <!-- Empty cell for time-axis header alignment -->
        <div class="time-axis-header"></div>

        <!-- Weekday headers -->
        ${kt(wt,e=>`header-${e}`,e=>{const t=this.copiedWeekday===e;return F`
              <div class="weekday-header">
                <div class="weekday-label">${this._getWeekdayLabel(e)}</div>
                ${this.editable?F`
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
          ${kt(this._getTimeLabels(),e=>e.hour,e=>F`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `)}
        </div>

        <!-- Time blocks content wrapper (for correct indicator positioning) -->
        <div class="schedule-content">
          ${kt(wt,e=>`${e}-${this.currentProfile}-${this.scheduleDataHash}`,e=>this._renderTimeBlocks(e))}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen?"":F`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?F`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `}render(){return this.scheduleData?this._isMobile?this._renderMobile():this._renderDesktop():F``}static{this.styles=qt}};Xt([he({attribute:!1})],Qt.prototype,"scheduleData",void 0),Xt([he({type:Boolean})],Qt.prototype,"editable",void 0),Xt([he({type:Boolean})],Qt.prototype,"showTemperature",void 0),Xt([he({type:Boolean})],Qt.prototype,"showGradient",void 0),Xt([he({type:String})],Qt.prototype,"temperatureUnit",void 0),Xt([he({type:String})],Qt.prototype,"hourFormat",void 0),Xt([he({attribute:!1})],Qt.prototype,"translations",void 0),Xt([he({type:String})],Qt.prototype,"copiedWeekday",void 0),Xt([he({type:Boolean})],Qt.prototype,"editorOpen",void 0),Xt([he({type:String})],Qt.prototype,"currentProfile",void 0),Xt([he({type:String})],Qt.prototype,"scheduleDataHash",void 0),Xt([pe()],Qt.prototype,"_currentTimePercent",void 0),Xt([pe()],Qt.prototype,"_currentTimeMinutes",void 0),Xt([pe()],Qt.prototype,"_currentWeekday",void 0),Xt([pe()],Qt.prototype,"_isMobile",void 0),Xt([pe()],Qt.prototype,"_mobileSelectedDayIndex",void 0),Qt=Xt([xt("hmip-schedule-grid")],Qt);const Jt=n`
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
`;var ei=function(e,t,i,s){var a,r=arguments.length,n=r<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n};let ti=class extends oe{constructor(){super(),this.open=!1,this.minTemp=5,this.maxTemp=30.5,this.tempStep=.5,this.temperatureUnit="°C",this.hourFormat="24",this._validationWarnings=[],this._historyStack=[],this._historyIndex=-1,this._keyDownHandler=this._handleKeyDown.bind(this)}connectedCallback(){super.connectedCallback(),window.addEventListener("keydown",this._keyDownHandler)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("keydown",this._keyDownHandler)}willUpdate(e){if(super.willUpdate(e),(e.has("open")||e.has("weekday"))&&this.open&&this.weekday){const t=e.get("open"),i=e.get("weekday");(!t&&this.open||this.open&&i!==this.weekday)&&this._initializeEditor(this.weekday)}}updated(e){super.updated(e),e.has("open")&&this.open&&!e.get("open")&&this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector(".weekday-tab, .base-temp-input, ha-button");e?.focus()})}_initializeEditor(e){this._editingWeekday=e,this._editingBlocks=this._getParsedBlocks(e),this._editingSlotIndex=void 0,this._editingSlotData=void 0;const t=this.scheduleData?.[e];if(t){const{baseTemperature:e}=Lt(t);this._editingBaseTemperature=e}else this._editingBaseTemperature=20;this._historyStack=[JSON.parse(JSON.stringify(this._editingBlocks))],this._historyIndex=0,this._updateValidationWarnings()}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=Lt(t);return i}return[]}_getWeekdayLabel(e,t){return"long"===t?this.translations?.weekdayLongLabels[e]??e:this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_formatTimeDisplay(e){return Mt(e,this.hourFormat)}_formatValidationParams(e){if(!e)return{};const t={};for(const[i,s]of Object.entries(e))"weekday"===i&&wt.includes(s)?t.weekday=this._getWeekdayLabel(s,"long"):t[i]=s;return t}_translateValidationMessage(e){const t=this.translations?.validationMessages[e.key]||e.key,i=this._formatValidationParams(e.params);e.nested&&(i.details=this._translateValidationMessage(e.nested));let s=t;for(const[e,t]of Object.entries(i))s=s.replace(`{${e}}`,t);return s}_saveHistoryState(){if(!this._editingBlocks)return;const e=JSON.parse(JSON.stringify(this._editingBlocks));this._historyStack=this._historyStack.slice(0,this._historyIndex+1),this._historyStack.push(e),this._historyIndex++,this._historyStack.length>50&&(this._historyStack.shift(),this._historyIndex--)}_undo(){this._historyIndex<=0||(this._historyIndex--,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_redo(){this._historyIndex>=this._historyStack.length-1||(this._historyIndex++,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_canUndo(){return this._historyIndex>0}_canRedo(){return this._historyIndex<this._historyStack.length-1}_handleKeyDown(e){if(!this.open||!this._editingWeekday||!this._editingBlocks)return;const t=e.ctrlKey||e.metaKey;t&&"z"===e.key&&!e.shiftKey?(e.preventDefault(),this._undo()):t&&("y"===e.key||"z"===e.key&&e.shiftKey)&&(e.preventDefault(),this._redo())}_updateValidationWarnings(){this._validationWarnings=this._editingBlocks?function(e,t=5,i=30.5){const s=[];if(0===e.length)return s;for(let t=0;t<e.length-1;t++){const i=e[t];i.endMinutes<i.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${t+1}`}}),i.endMinutes===i.startMinutes&&s.push({key:"blockZeroDuration",params:{block:`${t+1}`}})}const a=e[e.length-1];return a.endMinutes<a.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${e.length}`}}),e.forEach((e,a)=>{(e.startMinutes<0||e.startMinutes>1440)&&s.push({key:"invalidStartTime",params:{block:`${a+1}`}}),(e.endMinutes<0||e.endMinutes>1440)&&s.push({key:"invalidEndTime",params:{block:`${a+1}`}}),(e.temperature<t||e.temperature>i)&&s.push({key:"temperatureOutOfRange",params:{block:`${a+1}`,min:`${t}`,max:`${i}`}})}),s}(this._editingBlocks,this.minTemp,this.maxTemp):[]}_startSlotEdit(e){if(!this._editingBlocks||e<0||e>=this._editingBlocks.length)return;const t=this._editingBlocks[e];this._editingSlotIndex=e,this._editingSlotData={startTime:t.startTime,endTime:t.endTime,temperature:t.temperature}}_startSlotEditFromDisplay(e,t){if(!this._editingBlocks)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);-1!==s&&this._startSlotEdit(s)}_cancelSlotEdit(){this._editingSlotIndex=void 0,this._editingSlotData=void 0}_saveSlotEdit(){if(void 0===this._editingSlotIndex||!this._editingSlotData||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=this._editingSlotIndex,{startTime:t,endTime:i,temperature:s}=this._editingSlotData,a={startTime:t,startMinutes:Dt(t),endTime:i,endMinutes:Dt(i),temperature:s,slot:e+1},r=this._editingBlocks.filter((t,i)=>i!==e),n=function(e,t){const i=[],s=t.startMinutes,a=t.endMinutes,r=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of r){const t=e.startMinutes,r=e.endMinutes;r<=s||t>=a?i.push(e):(t<s&&i.push({...e,endTime:Tt(s),endMinutes:s,slot:i.length+1}),r>a&&i.push({...e,startTime:Tt(a),startMinutes:a,slot:i.length+1}))}i.push({...t,slot:i.length+1});const n=i.sort((e,t)=>e.startMinutes-t.startMinutes);return Nt(n)}(r,a),o=Nt(Vt(n));this._saveHistoryState(),this._editingBlocks=o,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._updateValidationWarnings()}_addNewSlot(){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;if(this._editingBlocks.length>=12)return;let e=0,t=60;if(this._editingBlocks.length>0){const i=Vt(this._editingBlocks),s=i[i.length-1];if(s.endMinutes<1440)e=s.endMinutes,t=Math.min(e+60,1440);else{let s=!1;for(let a=0;a<i.length;a++){const r=0===a?0:i[a-1].endMinutes;if(i[a].startMinutes>r){e=r,t=i[a].startMinutes,s=!0;break}}if(!s)return}}const i=Math.min(this._editingBaseTemperature+2,this.maxTemp),s={startTime:Tt(e),startMinutes:e,endTime:Tt(t),endMinutes:t,temperature:i,slot:this._editingBlocks.length+1};this._saveHistoryState();const a=Vt([...this._editingBlocks,s]);this._editingBlocks=a;const r=a.findIndex(i=>i.startMinutes===e&&i.endMinutes===t);r>=0&&this._startSlotEdit(r),this._updateValidationWarnings()}_removeTimeBlockByIndex(e,t){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);if(-1===s)return;this._saveHistoryState();const a=this._editingBlocks.filter((e,t)=>t!==s);this._editingBlocks=Nt(Vt(a)),this._updateValidationWarnings()}_switchToWeekday(e){e!==this._editingWeekday&&this._initializeEditor(e)}_closeEditor(){this._editingWeekday=void 0,this._editingBlocks=void 0,this._editingBaseTemperature=void 0,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._historyStack=[],this._historyIndex=-1,this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_saveSchedule(){if(!this._editingWeekday||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=Zt(zt(this._editingBlocks,this._editingBaseTemperature),this.minTemp,this.maxTemp);if(e){const t=this._translateValidationMessage(e);return void this.dispatchEvent(new CustomEvent("validation-failed",{detail:{error:t},bubbles:!0,composed:!0}))}this.dispatchEvent(new CustomEvent("save-schedule",{detail:{weekday:this._editingWeekday,blocks:this._editingBlocks,baseTemperature:this._editingBaseTemperature},bubbles:!0,composed:!0}))}render(){return this.open&&this._editingWeekday?F`
      <ha-dialog
        open
        @closed=${this._closeEditor}
        .heading=${this._formatEdit(this._editingWeekday)}
      >
        <div class="dialog-content">
          <!-- Weekday selector tabs -->
          <div class="weekday-tabs">
            ${wt.map(e=>F`
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
    `:F``}_formatEdit(e){return(this.translations?.edit??"Edit {weekday}").replace("{weekday}",this._getWeekdayLabel(e,"long"))}_renderEditor(){if(!this._editingWeekday||!this._editingBlocks)return F``;const e=void 0!==this._editingBaseTemperature?Rt(this._editingBlocks,this._editingBaseTemperature):this._editingBlocks;return F`
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
          ${this._validationWarnings.length>0?F`
                <ha-alert alert-type="warning" .title=${this.translations?.warningsTitle??""}>
                  <ul class="warnings-list">
                    ${this._validationWarnings.map(e=>F`<li class="warning-item">
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
              style="background-color: ${Pt(this._editingBaseTemperature||20)}"
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
          ${e.map((t,i)=>{const s=this._editingBlocks.findIndex(e=>e.startMinutes===t.startMinutes&&e.endMinutes===t.endMinutes),a=!(-1!==s);return void 0!==this._editingSlotIndex&&this._editingSlotIndex===s&&void 0!==this._editingSlotData&&this._editingSlotData?F`
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
                    style="background-color: ${Pt(this._editingSlotData.temperature)}"
                  ></div>
                </div>
              `:F`
              <div class="time-block-editor ${a?"base-temp-slot":""}">
                <span class="time-display">${this._formatTimeDisplay(t.startTime)}</span>
                <span class="time-display">${this._formatTimeDisplay(t.endTime)}</span>
                <div class="temp-display-group">
                  <span class="temp-display">${t.temperature.toFixed(1)}</span>
                  <span class="temp-unit">${this.temperatureUnit}</span>
                </div>
                <div class="slot-actions">
                  ${a?F``:F`
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
                  style="background-color: ${Pt(t.temperature)}"
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
    `}static{this.styles=Jt}};ei([he({type:Boolean})],ti.prototype,"open",void 0),ei([he({type:String})],ti.prototype,"weekday",void 0),ei([he({attribute:!1})],ti.prototype,"scheduleData",void 0),ei([he({type:Number})],ti.prototype,"minTemp",void 0),ei([he({type:Number})],ti.prototype,"maxTemp",void 0),ei([he({type:Number})],ti.prototype,"tempStep",void 0),ei([he({type:String})],ti.prototype,"temperatureUnit",void 0),ei([he({type:String})],ti.prototype,"hourFormat",void 0),ei([he({attribute:!1})],ti.prototype,"translations",void 0),ei([pe()],ti.prototype,"_editingWeekday",void 0),ei([pe()],ti.prototype,"_editingBlocks",void 0),ei([pe()],ti.prototype,"_editingBaseTemperature",void 0),ei([pe()],ti.prototype,"_validationWarnings",void 0),ei([pe()],ti.prototype,"_editingSlotIndex",void 0),ei([pe()],ti.prototype,"_editingSlotData",void 0),ti=ei([xt("hmip-schedule-editor")],ti);const ii=n`
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
`;var si=function(e,t,i,s){var a,r=arguments.length,n=r<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n};let ai=class extends oe{constructor(){super(...arguments),this.editable=!0,this.collapseAfter=0,this._expanded=!1,this._swipeX=0,this._touchStartX=0,this._touchStartY=0,this._isSwiping=!1,this._isScrolling=!1}static{this.styles=ii}_onTouchStart(e,t){if(!this.editable)return;const i=e.touches[0];this._touchStartX=i.clientX,this._touchStartY=i.clientY,this._isSwiping=!1,this._isScrolling=!1,this._swipingGroupNo=t,this._swipeX=0}_onTouchMove(e){if(!this._swipingGroupNo)return;const t=e.touches[0],i=t.clientX-this._touchStartX;if(!this._isSwiping&&!this._isScrolling){if(Math.abs(t.clientY-this._touchStartY)>10)return this._isScrolling=!0,this._swipingGroupNo=void 0,void(this._swipeX=0);Math.abs(i)>10&&(this._isSwiping=!0)}this._isScrolling||this._isSwiping&&(e.preventDefault(),this._swipeX=Math.min(0,i))}_onTouchEnd(e){this._swipingGroupNo&&this._isSwiping?Math.abs(this._swipeX)>=120?(this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:e}})),this._resetSwipe()):(this._swipeX=0,setTimeout(()=>this._resetSwipe(),200)):this._resetSwipe()}_resetSwipe(){this._swipingGroupNo=void 0,this._swipeX=0,this._isSwiping=!1,this._isScrolling=!1}_handleAdd(){this.dispatchEvent(new CustomEvent("add-event",{bubbles:!0,composed:!0}))}_handleEdit(e){this.dispatchEvent(new CustomEvent("edit-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}_handleDelete(e){this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}_getConditionDisplay(e){return function(e,t,i){const s=function(e,t,i){const s="sunset"===e?i.sunset:i.sunrise;return 0===t?s:`${s} ${t>0?"+":""}${t}min`}(e.astro_type,e.astro_offset_minutes,i),a=e.time;switch(e.condition){case"fixed_time":default:return{label:t,details:a};case"astro":return{label:t,details:s};case"earliest":case"latest":case"astro_if_before_fixed":case"astro_if_after_fixed":return{label:t,details:`${s} / ${a}`};case"fixed_if_before_astro":case"fixed_if_after_astro":return{label:t,details:`${a} / ${s}`}}}(e,this.translations.conditionLabels[e.condition]||e.condition,this.translations.conditionSummaryLabels)}_toggleExpanded(){this._expanded=!this._expanded}render(){if(!this.scheduleData)return F`<div class="no-data">${this.translations.loading}</div>`;const e=function(e){const t=[];for(const[i,s]of Object.entries(e))t.push({...s,groupNo:i,isActive:Bt(s)});return t.sort((e,t)=>e.time.localeCompare(t.time)),t}(this.scheduleData);if(0===e.length)return F`
        <div class="no-data">
          <p>${this.translations.noScheduleEvents}</p>
          ${this.editable?F`<ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>`:""}
        </div>
      `;const t=this.collapseAfter>0&&e.length>this.collapseAfter,i=t&&!this._expanded?e.slice(0,this.collapseAfter):e,s=e.length-this.collapseAfter;return F`
      <div class="schedule-list">
        <div class="events-table">
          ${kt(i,e=>e.groupNo,e=>this._renderEvent(e))}
        </div>
        ${t?F`<div class="collapse-toggle">
              <ha-button @click=${this._toggleExpanded}>
                ${this._expanded?this.translations.showLess:`${this.translations.showMore} (${s})`}
              </ha-button>
            </div>`:""}
        ${this.editable?F`<div class="toolbar">
              <ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>
            </div>`:""}
      </div>
    `}_formatLockEntry(e){return"door_lock"===e.lock_mode&&e.lock_action?{lock_autorelock_end:this.translations.lockActionLockAutorelockEnd??"Lock + AR end",lock_autorelock_start:this.translations.lockActionLockAutorelockStart??"Lock + AR start",unlock_autorelock_end:this.translations.lockActionUnlockAutorelockEnd??"Unlock + AR end",autorelock_end:this.translations.lockActionAutorelockEnd??"AR end"}[e.lock_action]??e.lock_action:"user_permission"===e.lock_mode&&e.permission?"granted"===e.permission?this.translations.permissionGranted??"Granted":this.translations.permissionNotGranted??"Not granted":"-"}_renderEvent(e){const t="lock"===this.domain?this._formatLockEntry(e):function(e,t,i){const s=t?At[t]:void 0;if("binary"===s?.levelType){const t=i?.on??"On";return 0===e?i?.off??"Off":t}return`${Math.round(100*e)}%`}(e.level,this.domain,{on:this.translations.levelOn,off:this.translations.levelOff}),i=this.domain?At[this.domain]:void 0,s=null===e.duration&&i?.hasDuration?this.translations.permanentOn:function(e){if(!e)return"-";const t=Ot(e);return t?`${t.value}${{ms:"ms",s:"s",min:"min",h:"h"}[t.unit]}`:e}(e.duration),{label:a,details:r}=this._getConditionDisplay(e),n=this._swipingGroupNo===e.groupNo,o=n?this._swipeX:0;return F`
      <div class="event-card-wrapper">
        ${n&&o<-40?F`<div class="swipe-delete-bg">
              <ha-icon .icon=${"mdi:delete"}></ha-icon>
            </div>`:""}
        <div
          class="event-card ${e.isActive?"active":"inactive"} ${n&&this._isSwiping?"swiping":""}"
          style=${n&&this._isSwiping?`transform: translateX(${o}px)`:""}
          @touchstart=${t=>this._onTouchStart(t,e.groupNo)}
          @touchmove=${e=>this._onTouchMove(e)}
          @touchend=${()=>this._onTouchEnd(e)}
        >
          <div class="event-row-top">
            <div class="col-condition">${a}</div>
            ${this.editable?F`<div class="col-actions">
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
            <span class="col-details-text">${r}</span>
          </div>
          <div class="event-row-bottom">
            <div class="col-weekdays">
              <div class="weekday-badges">
                ${wt.map(t=>{const i=e.weekdays.includes(t);return F`<span class="weekday-badge ${i?"active":"inactive"}"
                    >${this.translations.weekdayShortLabels[t]}</span
                  >`})}
              </div>
            </div>
            <div class="col-details">
              <span class="col-state">
                ${t}
                ${null!==e.level_2?F`<span class="level-2"
                      >, ${this.translations.slat}: ${Math.round(100*e.level_2)}%</span
                    >`:""}
              </span>
              ${s&&"-"!==s?F`<span class="col-duration">${s}</span>`:""}
            </div>
          </div>
        </div>
      </div>
    `}};si([he({attribute:!1})],ai.prototype,"scheduleData",void 0),si([he({attribute:!1})],ai.prototype,"domain",void 0),si([he({type:Boolean})],ai.prototype,"editable",void 0),si([he({type:Number})],ai.prototype,"collapseAfter",void 0),si([he({attribute:!1})],ai.prototype,"translations",void 0),si([pe()],ai.prototype,"_expanded",void 0),si([pe()],ai.prototype,"_swipingGroupNo",void 0),si([pe()],ai.prototype,"_swipeX",void 0),ai=si([xt("hmip-device-schedule-list")],ai);const ri=n`
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

  .duration-row input[type="number"]:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .permanent-label {
    margin-bottom: 6px;
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
`;var ni=function(e,t,i,s){var a,r=arguments.length,n=r<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(n=(r<3?a(n):r>3?a(t,i,n):a(t,i))||n);return r>3&&n&&Object.defineProperty(t,i,n),n};let oi=class extends oe{constructor(){super(...arguments),this.open=!1,this.isNewEvent=!1,this._validationErrors=[]}static{this.styles=ri}willUpdate(e){(e.has("open")||e.has("entry"))&&(this.open&&this.entry?(this._editingEntry={...this.entry},this._validationErrors=[]):this.open||(this._editingEntry=void 0,this._validationErrors=[]))}updated(e){super.updated(e),e.has("open")&&this.open&&!e.get("open")&&this.updateComplete.then(()=>{const e=this.shadowRoot?.querySelector("input[type='time'], ha-select, input");e?.focus()})}_updateEditingEntry(e){this._editingEntry&&(this._editingEntry={...this._editingEntry,...e},this._validationErrors=[],this.requestUpdate())}_handleClose(){this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_handleSave(){if(!this._editingEntry||void 0===this.groupNo)return;const e=function(e,t){const i=[];if(function(e){try{return function(e){const t=e.split(":");if(2!==t.length)throw new Error(`Invalid time format: ${e}`);const i=parseInt(t[0],10),s=parseInt(t[1],10);if(isNaN(i)||isNaN(s)||i<0||i>23||s<0||s>59)throw new Error(`Invalid time values: ${e}`)}(e),!0}catch{return!1}}(e.time)||i.push({field:"time",message:"Time must be in HH:MM format (00:00-23:59)"}),e.weekdays&&0!==e.weekdays.length||i.push({field:"weekdays",message:"At least one weekday must be selected"}),"lock"===t)e.lock_mode?"door_lock"===e.lock_mode?e.lock_action||i.push({field:"lock_action",message:"Lock action must be selected"}):"user_permission"===e.lock_mode&&(e.permission||i.push({field:"permission",message:"Permission must be selected"})):i.push({field:"lock_mode",message:"Lock mode must be selected"});else{const s=t?At[t]:void 0;"binary"===s?.levelType?0!==e.level&&1!==e.level&&i.push({field:"level",message:"Level must be 0 or 1"}):(e.level<0||e.level>1)&&i.push({field:"level",message:"Level must be between 0.0 and 1.0"})}return"cover"===t&&null!==e.level_2&&(e.level_2<0||e.level_2>1)&&i.push({field:"level_2",message:"Slat position must be between 0.0 and 1.0"}),Ut(e.condition)&&(e.astro_offset_minutes<-128||e.astro_offset_minutes>127)&&i.push({field:"astro_offset_minutes",message:"Astro offset must be between -128 and +127 minutes"}),null!==e.duration&&(null===Ot(e.duration)?i.push({field:"duration",message:"Invalid duration format"}):Kt(e.duration)||i.push({field:"duration",message:"Duration factor must be between 0 and 30 per unit (use the next-larger unit)"})),null!==e.ramp_time&&(null===Ot(e.ramp_time)?i.push({field:"ramp_time",message:"Invalid ramp time format"}):Kt(e.ramp_time)||i.push({field:"ramp_time",message:"Ramp time factor must be between 0 and 30 per unit (use the next-larger unit)"})),i}(this._editingEntry,this.domain);e.length>0?this._validationErrors=e.map(e=>`${e.field}: ${e.message}`):this.dispatchEvent(new CustomEvent("save-event",{bubbles:!0,composed:!0,detail:{entry:{...this._editingEntry},groupNo:this.groupNo}}))}render(){return this.open&&this._editingEntry?F`
      <ha-dialog
        open
        @closed=${this._handleClose}
        .heading=${this.isNewEvent?this.translations.addEvent:this.translations.editEvent}
      >
        <div class="editor-content">
          ${this._renderTimeFields()} ${this._renderConditionFields()}
          ${this._renderWeekdayFields()}
          ${"lock"===this.domain?this._renderLockFields():this._renderLevelFields()}
          ${this._renderDurationFields()} ${this._renderRampTimeFields()}
          ${this._renderChannelFields()} ${this._renderValidationErrors()}
          <div class="editor-footer">
            <ha-button @click=${this._handleClose}> ${this.translations.cancel} </ha-button>
            <ha-button @click=${this._handleSave}> ${this.translations.save} </ha-button>
          </div>
        </div>
      </ha-dialog>
    `:F``}_renderValidationErrors(){return F`
      <div aria-live="polite">
        ${this._validationErrors.length>0?F`
              <ha-alert alert-type="error">
                <ul class="validation-list">
                  ${this._validationErrors.map(e=>F`<li>${e}</li>`)}
                </ul>
              </ha-alert>
            `:""}
      </div>
    `}_renderTimeFields(){return this._editingEntry?F`
      <div class="form-group">
        <label>${this.translations.time}</label>
        <input
          type="time"
          .value=${this._editingEntry.time}
          @change=${e=>{this._updateEditingEntry({time:e.target.value})}}
        />
      </div>
    `:F``}_renderConditionFields(){if(!this._editingEntry)return F``;if(!Et("CONDITION",this.supportedScheduleFields))return F``;const e=Ut(this._editingEntry.condition)&&Et("ASTRO_TYPE",this.supportedScheduleFields)&&Et("ASTRO_OFFSET",this.supportedScheduleFields);return F`
      <div class="form-group">
        <label>${this.translations.condition}</label>
        <ha-select
          .value=${this._editingEntry.condition}
          .options=${St.map(e=>({value:e,label:this.translations.conditionLabels[e]||e}))}
          @selected=${e=>{e.stopPropagation();const t=e.detail.value,i={condition:t};"fixed_time"===t?(i.astro_type=null,i.astro_offset_minutes=0):null===this._editingEntry.astro_type&&(i.astro_type="sunrise"),this._updateEditingEntry(i)}}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>
      ${e?F`
            <div class="form-group">
              <label>${this.translations.astroSunrise}/${this.translations.astroSunset}</label>
              <ha-select
                .value=${this._editingEntry.astro_type||"sunrise"}
                .options=${[{value:"sunrise",label:this.translations.astroSunrise},{value:"sunset",label:this.translations.astroSunset}]}
                @selected=${e=>{e.stopPropagation(),this._updateEditingEntry({astro_type:e.detail.value})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            </div>
            <div class="form-group">
              <label>${this.translations.astroOffset}</label>
              <input
                type="number"
                min="-128"
                max="127"
                .value=${String(this._editingEntry.astro_offset_minutes)}
                @input=${e=>{const t=parseInt(e.target.value,10);isNaN(t)||this._updateEditingEntry({astro_offset_minutes:t})}}
              />
            </div>
          `:""}
    `}_renderWeekdayFields(){return this._editingEntry?F`
      <div class="form-group">
        <label>${this.translations.weekdaysLabel}</label>
        <div class="weekday-checkboxes">
          ${wt.map(e=>{const t=this._editingEntry.weekdays.includes(e);return F`
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
    `:F``}_renderLevelFields(){if(!this._editingEntry)return F``;const e=this.domain?At[this.domain]:void 0;return F`
      <div class="form-group">
        <label>${this.translations.stateLabel}</label>
        ${"binary"===e?.levelType?F`
              <ha-select
                .value=${String(this._editingEntry.level)}
                .options=${[{value:"0",label:this.translations.levelOff},{value:"1",label:this.translations.levelOn}]}
                @selected=${e=>{e.stopPropagation();const t=parseInt(e.detail.value,10);this._updateEditingEntry({level:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            `:F`
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
      ${e?.hasLevel2&&Et("LEVEL_2",this.supportedScheduleFields)?F`
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
    `}_renderLockFields(){if(!this._editingEntry)return F``;const e=this._editingEntry.lock_mode||"door_lock",t=[{value:"door_lock",label:this.translations.lockModeDoorLock},{value:"user_permission",label:this.translations.lockModeUserPermission}],i=Ct.map(e=>({value:e,label:{lock_autorelock_end:this.translations.lockActionLockAutorelockEnd,lock_autorelock_start:this.translations.lockActionLockAutorelockStart,unlock_autorelock_end:this.translations.lockActionUnlockAutorelockEnd,autorelock_end:this.translations.lockActionAutorelockEnd}[e]}));return F`
      <div class="form-group">
        <label>${this.translations.lockMode}</label>
        <ha-select
          .value=${e}
          .options=${t}
          @selected=${e=>{e.stopPropagation();const t=e.detail.value;t&&this._updateEditingEntry("door_lock"===t?{lock_mode:t,lock_action:"lock_autorelock_end",permission:null,level:0}:{lock_mode:t,lock_action:null,permission:"granted",level:1})}}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>

      ${"door_lock"===e?F`
            <div class="form-group">
              <label>${this.translations.lockAction}</label>
              <ha-select
                .value=${this._editingEntry.lock_action||"lock_autorelock_end"}
                .options=${i}
                @selected=${e=>{e.stopPropagation();const t=e.detail.value;t&&this._updateEditingEntry({lock_action:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            </div>
          `:F`
            <div class="form-group">
              <label>${this.translations.lockPermission}</label>
              <ha-select
                .value=${this._editingEntry.permission||"granted"}
                .options=${[{value:"granted",label:this.translations.permissionGranted},{value:"not_granted",label:this.translations.permissionNotGranted}]}
                @selected=${e=>{e.stopPropagation();const t=e.detail.value;t&&this._updateEditingEntry({permission:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            </div>
          `}
    `}_renderDurationFields(){if(!this._editingEntry)return F``;const e=this.domain?At[this.domain]:void 0;if(e&&!e.hasDuration)return F``;if(!Et("DURATION_BASE",this.supportedScheduleFields))return F``;const t=this._editingEntry.duration?Ot(this._editingEntry.duration):null,i=null===this._editingEntry.duration,s=t?.value??0,a=t?.unit??"s",r=Ft(a);return F`
      <div class="form-group">
        <label>${this.translations.duration}</label>
        <label class="checkbox-label permanent-label">
          <ha-checkbox
            .checked=${i}
            @change=${e=>{this._updateEditingEntry(e.target.checked?{duration:null}:{duration:jt(1,a)})}}
          ></ha-checkbox>
          ${this.translations.permanentOn}
        </label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            max=${r.max}
            step=${r.step}
            .value=${String(s)}
            ?disabled=${i}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({duration:jt(t,a)}):this._updateEditingEntry({duration:null})}}
          />
          <ha-select
            .value=${a}
            .disabled=${i}
            .options=${It.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation();const t=e.detail.value;if(s>0){const e=Ft(t),i=Math.min(s,e.max);this._updateEditingEntry({duration:jt(i,t)})}}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderRampTimeFields(){if(!this._editingEntry)return F``;const e=this.domain?At[this.domain]:void 0;if(e&&!e.hasRampTime)return F``;if(!Et("RAMP_TIME_BASE",this.supportedScheduleFields))return F``;const t=this._editingEntry.ramp_time?Ot(this._editingEntry.ramp_time):null,i=t?.value??0,s=t?.unit??"s",a=Ft(s);return F`
      <div class="form-group">
        <label>${this.translations.rampTime}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            max=${a.max}
            step=${a.step}
            .value=${String(i)}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({ramp_time:jt(t,s)}):this._updateEditingEntry({ramp_time:null})}}
          />
          <ha-select
            .value=${s}
            .options=${It.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation();const t=e.detail.value;if(i>0){const e=Ft(t),s=Math.min(i,e.max);this._updateEditingEntry({ramp_time:jt(s,t)})}}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderChannelFields(){return this._editingEntry&&this.availableTargetChannels&&Object.keys(this.availableTargetChannels).length>0?F`
        <div class="form-group">
          <label>${this.translations.channels}</label>
          <div class="channel-checkboxes">
            ${Object.entries(this.availableTargetChannels).map(([e,t])=>{const i=this._editingEntry.target_channels.includes(e);return F`
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
      `:F``}};ni([he({type:Boolean})],oi.prototype,"open",void 0),ni([he({attribute:!1})],oi.prototype,"entry",void 0),ni([he()],oi.prototype,"groupNo",void 0),ni([he({type:Boolean})],oi.prototype,"isNewEvent",void 0),ni([he({attribute:!1})],oi.prototype,"domain",void 0),ni([he({attribute:!1})],oi.prototype,"availableTargetChannels",void 0),ni([he({attribute:!1})],oi.prototype,"supportedScheduleFields",void 0),ni([he({attribute:!1})],oi.prototype,"translations",void 0),ni([pe()],oi.prototype,"_editingEntry",void 0),ni([pe()],oi.prototype,"_validationErrors",void 0),oi=ni([xt("hmip-device-schedule-editor")],oi);const li={"HmIP-BSL":"device_schedule.device_mode_hint_bsl","HmIP-RGBW":"device_schedule.device_mode_hint_rgbw","HmIP-DLD":"device_schedule.device_mode_hint_lock","HmIP-FLC":"device_schedule.device_mode_hint_lock","HmIP-DLP":"device_schedule.device_mode_hint_lock"};let di=class extends oe{constructor(){super(...arguments),this.entryId="",this.deviceAddress="",this.deviceName="",this.editable=!0,this._devices=[],this._selectedDevice=null,this._climateData=null,this._deviceData=null,this._selectedProfile="",this._loading=!0,this._saving=!1,this._error="",this._deviceShowEditor=!1,this._deviceIsNewEvent=!1}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this._fetchDevices(),e.has("hass")&&this._selectedDevice&&this._deviceData&&this._syncScheduleEnabledFromEntity()}_findScheduleEntityId(){if(!this._selectedDevice||!this.hass?.states)return;const e=this._selectedDevice.channel_address;for(const[t,i]of Object.entries(this.hass.states)){const s=i.attributes;if(s.address===e&&"schedule_enabled"in s)return t}}_syncScheduleEnabledFromEntity(){if(!this._deviceData||!this.hass?.states)return;if(this._scheduleEntityId||(this._scheduleEntityId=this._findScheduleEntityId()),!this._scheduleEntityId)return;const e=this.hass.states[this._scheduleEntityId];if(!e)return;const t=e.attributes.schedule_enabled;t&&JSON.stringify(t)!==JSON.stringify(this._deviceData.schedule_enabled)&&(this._deviceData={...this._deviceData,schedule_enabled:t})}async _fetchDevices(){this._loading=!0,this._error="";try{let e;this._devices=await Ne(this.hass,this.entryId),this.deviceAddress&&(e=this._devices.find(e=>e.address===this.deviceAddress)),!e&&this._devices.length>0&&(e=this._devices[0]),e&&(this._selectedDevice=e,await this._loadSchedule(e))}catch(e){this._error=String(e)}finally{this._loading=!1}}async _loadSchedule(e){this._loading=!0,this._error="",this._climateData=null,this._deviceData=null;try{if("climate"===e.schedule_type){let t=this._selectedProfile||void 0;if(!t){const i=await Re(this.hass,this.entryId,e.address);t=i.active_profile,this._selectedProfile=t;const s=Object.keys(i.schedule_data).some(e=>"MONDAY"===e||"TUESDAY"===e||"WEDNESDAY"===e||"THURSDAY"===e||"FRIDAY"===e||"SATURDAY"===e||"SUNDAY"===e);s&&(this._climateData=i)}if(!this._climateData){const i=await Re(this.hass,this.entryId,e.address,t);this._climateData=i,!this._selectedProfile&&i.active_profile&&(this._selectedProfile=i.active_profile)}}else this._deviceData=await async function(e,t,i){return e.callWS({type:"homematicip_local/config/get_device_schedule",entry_id:t,device_address:i})}(this.hass,this.entryId,e.address)}catch{this._error=this._l("device_schedule.load_failed")}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}async _handleDeviceSelect(e){e.stopPropagation();const t=e.detail.value;if(!t||t===this._selectedDevice?.address)return;const i=this._devices.find(e=>e.address===t);i&&(this._selectedDevice=i,this._scheduleEntityId=void 0,this._selectedProfile="",this._editingWeekday=void 0,this._copiedSchedule=void 0,this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1,await this._loadSchedule(i))}async _handleProfileChange(e){e.stopPropagation();const t=e.detail.value;if(t&&t!==this._selectedProfile&&(this._selectedProfile=t,this._selectedDevice)){try{await async function(e,t,i,s){return e.callWS({type:"homematicip_local/config/set_climate_active_profile",entry_id:t,device_address:i,profile:s})}(this.hass,this.entryId,this._selectedDevice.address,t)}catch{return void rt(this,{message:this._l("device_schedule.save_failed")})}await this._loadSchedule(this._selectedDevice)}}_onWeekdayClick(e){this._editingWeekday=e.detail.weekday}_onCopySchedule(e){const t=e.detail.weekday;if(!this._climateData)return;const i=this._climateData.schedule_data[t];if(!i)return;const{blocks:s,baseTemperature:a}=Lt(i);this._copiedSchedule={weekday:t,blocks:JSON.parse(JSON.stringify(s)),baseTemperature:a}}async _onPasteSchedule(e){const t=e.detail.weekday;if(!this._selectedDevice||!this._copiedSchedule||!this._climateData)return;const i=this._copiedSchedule.baseTemperature??function(e){if(0===e.length)return 20;const t=new Map;for(const i of e){const e=i.endMinutes-i.startMinutes,s=t.get(i.temperature)||0;t.set(i.temperature,s+e)}let i=0,s=20;for(const[e,a]of t.entries())a>i&&(i=a,s=e);return s}(this._copiedSchedule.blocks),s=zt(this._copiedSchedule.blocks,i);if(Zt(s,this._climateData.min_temp??5,this._climateData.max_temp??30.5))rt(this,{message:this._l("device_schedule.invalid_schedule")});else{this._saving=!0;try{const{base_temperature:e,periods:i}=s;await Ve(this.hass,this.entryId,this._selectedDevice.address,this._selectedProfile,t,e,i.map(e=>({...e}))),rt(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}}async _onSaveSchedule(e){if(!this._selectedDevice||!this._climateData)return;const{weekday:t,blocks:i,baseTemperature:s}=e.detail,a=zt(i,s);if(Zt(a,this._climateData.min_temp??5,this._climateData.max_temp??30.5))rt(this,{message:this._l("device_schedule.invalid_schedule")});else{this._saving=!0;try{const{base_temperature:e,periods:i}=a;await Ve(this.hass,this.entryId,this._selectedDevice.address,this._selectedProfile,t,e,i.map(e=>({...e}))),rt(this,{message:this._l("device_schedule.save_success")}),this._editingWeekday=void 0,await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}}_onValidationFailed(e){rt(this,{message:this._l("device_schedule.invalid_schedule",{error:e.detail.error})})}_onEditorClosed(){this._editingWeekday=void 0}async _handleReload(){if(this._selectedDevice)try{await async function(e,t,i){return e.callWS({type:"homematicip_local/config/reload_device_config",entry_id:t,device_address:i})}(this.hass,this.entryId,this._selectedDevice.address),rt(this,{message:this._l("device_schedule.reload_success")}),await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.reload_failed")})}}async _handleExport(){const e=this._climateData?.schedule_data??this._deviceData?.schedule_data;if(!e)return;const t=JSON.stringify(e,null,2),i=new Blob([t],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s;const r=this._selectedDevice?.address.replace(/:/g,"_")??"schedule";a.download=`${r}_schedule.json`,a.click(),URL.revokeObjectURL(s)}async _handleImport(){const e=document.createElement("input");e.type="file",e.accept=".json",e.onchange=async()=>{const t=e.files?.[0];if(t&&this._selectedDevice)try{const e=await t.text(),i=JSON.parse(e);if(!await st(0,{title:this._l("device_schedule.import_confirm_title"),text:this._l("device_schedule.import_confirm_text"),confirmText:this._l("device_schedule.import"),dismissText:this._l("common.cancel")}))return;"climate"===this._selectedDevice.schedule_type?(this._climateData={...this._climateData,schedule_data:i},rt(this,{message:this._l("device_schedule.import_success")})):(await Be(this.hass,this.entryId,this._selectedDevice.address,i),rt(this,{message:this._l("device_schedule.import_success")}),await this._loadSchedule(this._selectedDevice))}catch{rt(this,{message:this._l("device_schedule.import_failed")})}},e.click()}_buildGridTranslations(){return{weekdayShortLabels:{MONDAY:this._l("device_schedule.weekdays").split(",")[0],TUESDAY:this._l("device_schedule.weekdays").split(",")[1],WEDNESDAY:this._l("device_schedule.weekdays").split(",")[2],THURSDAY:this._l("device_schedule.weekdays").split(",")[3],FRIDAY:this._l("device_schedule.weekdays").split(",")[4],SATURDAY:this._l("device_schedule.weekdays").split(",")[5],SUNDAY:this._l("device_schedule.weekdays").split(",")[6]},weekdayLongLabels:{MONDAY:this._l("device_schedule.weekday_monday"),TUESDAY:this._l("device_schedule.weekday_tuesday"),WEDNESDAY:this._l("device_schedule.weekday_wednesday"),THURSDAY:this._l("device_schedule.weekday_thursday"),FRIDAY:this._l("device_schedule.weekday_friday"),SATURDAY:this._l("device_schedule.weekday_saturday"),SUNDAY:this._l("device_schedule.weekday_sunday")},clickToEdit:this._l("device_schedule.click_to_edit"),copySchedule:this._l("device_schedule.copy_schedule"),pasteSchedule:this._l("device_schedule.paste_schedule")}}_buildEditorTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},weekdayLongLabels:{MONDAY:this._l("device_schedule.weekday_monday"),TUESDAY:this._l("device_schedule.weekday_tuesday"),WEDNESDAY:this._l("device_schedule.weekday_wednesday"),THURSDAY:this._l("device_schedule.weekday_thursday"),FRIDAY:this._l("device_schedule.weekday_friday"),SATURDAY:this._l("device_schedule.weekday_saturday"),SUNDAY:this._l("device_schedule.weekday_sunday")},edit:this._l("device_schedule.edit"),cancel:this._l("common.cancel"),save:this._l("device_schedule.save"),addTimeBlock:this._l("device_schedule.add_time_block"),from:this._l("device_schedule.from"),to:this._l("device_schedule.to"),baseTemperature:this._l("device_schedule.base_temperature"),baseTemperatureDescription:this._l("device_schedule.base_temperature_description"),temperaturePeriods:this._l("device_schedule.temperature_periods"),editSlot:this._l("device_schedule.edit_slot"),saveSlot:this._l("device_schedule.save_slot"),cancelSlotEdit:this._l("device_schedule.cancel_slot_edit"),removeSlot:this._l("device_schedule.remove_slot"),close:this._l("common.close"),undoShortcut:this._l("device_schedule.undo_shortcut"),redoShortcut:this._l("device_schedule.redo_shortcut"),warningsTitle:this._l("device_schedule.warnings_title"),validationMessages:{blockEndBeforeStart:this._l("device_schedule.validation_block_end_before_start"),blockZeroDuration:this._l("device_schedule.validation_block_zero_duration"),invalidStartTime:this._l("device_schedule.validation_invalid_start_time"),invalidEndTime:this._l("device_schedule.validation_invalid_end_time"),temperatureOutOfRange:this._l("device_schedule.validation_temp_out_of_range"),invalidSlotCount:this._l("device_schedule.validation_invalid_slot_count"),invalidSlotKey:this._l("device_schedule.validation_invalid_slot_key"),missingSlot:this._l("device_schedule.validation_missing_slot"),slotMissingValues:this._l("device_schedule.validation_slot_missing_values"),slotTimeBackwards:this._l("device_schedule.validation_slot_time_backwards"),slotTimeExceedsDay:this._l("device_schedule.validation_slot_time_exceeds_day"),lastSlotMustEnd:this._l("device_schedule.validation_last_slot_must_end"),scheduleMustBeObject:this._l("device_schedule.validation_schedule_must_be_object"),missingWeekday:this._l("device_schedule.validation_missing_weekday"),invalidWeekdayData:this._l("device_schedule.validation_invalid_weekday_data"),weekdayValidationError:this._l("device_schedule.validation_weekday_error")}}}render(){return this._loading&&0===this._devices.length?F`<div class="loading">${this._l("common.loading")}</div>`:this._error&&0===this._devices.length?F`<div class="error">
        ${this._error}
        <br />
        <ha-button outlined @click=${this._fetchDevices}> ${this._l("common.retry")} </ha-button>
      </div>`:F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="schedule-header">
        <h2>${this._l("device_schedule.title")}</h2>

        <div class="device-selector">
          <ha-select
            .label=${this._l("device_schedule.select_device")}
            .value=${this._selectedDevice?.address??""}
            .options=${[...this._devices].sort((e,t)=>e.name.localeCompare(t.name)).map(e=>({value:e.address,label:`${e.name} (${e.model}) - ${this._l(`device_schedule.schedule_type_${e.schedule_type}`)}`}))}
            @selected=${this._handleDeviceSelect}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
        ${this._selectedDevice&&li[this._selectedDevice.model]?F`<ha-alert alert-type="info">
              ${this._l(li[this._selectedDevice.model])}
            </ha-alert>`:j}
      </div>

      ${0===this._devices.length?F`<div class="empty-state">${this._l("device_schedule.no_devices")}</div>`:j}
      ${this._selectedDevice&&this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:j}
      ${this._error&&this._selectedDevice?F`<div class="error">
            ${this._error}
            <br />
            <ha-button outlined @click=${()=>this._loadSchedule(this._selectedDevice)}>
              ${this._l("common.retry")}
            </ha-button>
          </div>`:j}
      ${"climate"===this._selectedDevice?.schedule_type&&this._climateData?this._renderClimateSchedule():j}
      ${"default"===this._selectedDevice?.schedule_type&&this._deviceData?this._renderDeviceSchedule():j}
    `}_renderClimateSchedule(){const e=this._climateData,t=e.schedule_data;return F`
      <div class="schedule-content">
        <div class="toolbar">
          <div class="profile-selector">
            <ha-select
              .label=${this._l("device_schedule.profile")}
              .value=${this._selectedProfile}
              .options=${e.available_profiles.map((t,i)=>({value:t,label:e.device_active_profile_index===i+1?`${t} (${this._l("device_schedule.active_profile")})`:t}))}
              @selected=${this._handleProfileChange}
              @closed=${e=>e.stopPropagation()}
            ></ha-select>
          </div>
          <div class="toolbar-actions">
            <ha-button outlined @click=${this._handleExport}>
              ${this._l("device_schedule.export")}
            </ha-button>
            ${this.editable?F`
                  <ha-button outlined @click=${this._handleImport}>
                    ${this._l("device_schedule.import")}
                  </ha-button>
                  <ha-button outlined @click=${this._handleReload}>
                    ${this._l("device_schedule.reload")}
                  </ha-button>
                `:j}
          </div>
        </div>

        <div class="climate-grid-container">
          <hmip-schedule-grid
            .scheduleData=${t}
            .editable=${this.editable}
            .showTemperature=${!0}
            .showGradient=${!1}
            temperatureUnit="°C"
            hourFormat="24"
            .translations=${this._buildGridTranslations()}
            .copiedWeekday=${this._copiedSchedule?.weekday}
            .editorOpen=${!!this._editingWeekday}
            .currentProfile=${this._selectedProfile}
            @weekday-click=${this._onWeekdayClick}
            @copy-schedule=${this._onCopySchedule}
            @paste-schedule=${this._onPasteSchedule}
          ></hmip-schedule-grid>
        </div>

        <hmip-schedule-editor
          .open=${!!this._editingWeekday}
          .weekday=${this._editingWeekday}
          .scheduleData=${t}
          .minTemp=${e.min_temp??5}
          .maxTemp=${e.max_temp??30.5}
          .tempStep=${e.step??.5}
          temperatureUnit="°C"
          hourFormat="24"
          .translations=${this._buildEditorTranslations()}
          @save-schedule=${this._onSaveSchedule}
          @validation-failed=${this._onValidationFailed}
          @editor-closed=${this._onEditorClosed}
        ></hmip-schedule-editor>
      </div>

      ${this._saving?F`<div class="saving-overlay">${this._l("device_schedule.saving")}</div>`:j}
    `}_onDeviceAddEvent(){if(!this._deviceData)return;const e=this._deviceData.schedule_data?.entries??{},t=this._deviceData.max_entries;if(t&&Object.keys(e).length>=t)return void rt(this,{message:this._l("device_schedule.max_entries",{max:t})});const i=function(e){const t={weekdays:[],time:"00:00",condition:"fixed_time",astro_type:null,astro_offset_minutes:0,target_channels:[],level:0,level_2:null,duration:null,ramp_time:null,lock_mode:null,lock_action:null,permission:null};return"cover"===e&&(t.level_2=0),"lock"===e&&(t.lock_mode="door_lock",t.lock_action="lock_autorelock_end"),t}(this._deviceData.schedule_domain??void 0),s=this._deviceData.available_target_channels;if(s){const e=Object.keys(s)[0];e&&(i.target_channels=[e])}const a=Object.keys(e).map(e=>parseInt(e,10)),r=a.length>0?Math.max(...a):0;this._deviceEditingGroupNo=String(r+1),this._deviceEditingEntry={...i},this._deviceIsNewEvent=!0,this._deviceShowEditor=!0}_onDeviceEditEvent(e){const t=e.detail.entry;this._deviceEditingGroupNo=t.groupNo,this._deviceEditingEntry={...t},this._deviceIsNewEvent=!1,this._deviceShowEditor=!0}async _onDeviceDeleteEvent(e){if(!confirm(this._l("device_schedule.confirm_delete")))return;if(!this._deviceData||!this._selectedDevice)return;const t={...this._deviceData.schedule_data?.entries??{}};delete t[e.detail.entry.groupNo],this._saving=!0;try{await Be(this.hass,this.entryId,this._selectedDevice.address,{entries:Gt(t)}),rt(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}async _onDeviceSaveEvent(e){if(!this._deviceData||!this._selectedDevice)return;const{entry:t,groupNo:i}=e.detail,s={...this._deviceData.schedule_data?.entries??{},[i]:t};this._saving=!0,this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1;try{await Be(this.hass,this.entryId,this._selectedDevice.address,{entries:Gt(s)}),rt(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}_onDeviceEditorClosed(){this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1}async _handleScheduleEnabledToggle(e){if(!this._selectedDevice||!this._deviceData||null===this._deviceData.schedule_enabled)return;const t=!this._deviceData.schedule_enabled[e];this._saving=!0;try{await async function(e,t,i,s,a){const r={type:"homematicip_local/config/set_schedule_enabled",entry_id:t,device_address:i,enabled:s};return void 0!==a&&(r.channel_key=a),e.callWS(r)}(this.hass,this.entryId,this._selectedDevice.address,t,e),rt(this,{message:this._l(t?"device_schedule.weekly_program_enabled_toast":"device_schedule.weekly_program_disabled_toast")}),await this._loadSchedule(this._selectedDevice)}catch{rt(this,{message:this._l("device_schedule.weekly_program_enable_failed")})}finally{this._saving=!1}}_buildDeviceListTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},condition:this._l("device_schedule.condition"),time:this._l("device_schedule.time"),weekdays:this._l("device_schedule.weekdays_label"),duration:this._l("device_schedule.duration"),state:this._l("device_schedule.level"),addEvent:this._l("device_schedule.add_event"),editEvent:this._l("device_schedule.edit_event"),deleteEvent:this._l("device_schedule.delete_event"),slat:this._l("device_schedule.slat"),noScheduleEvents:this._l("device_schedule.no_schedule_data"),loading:this._l("common.loading"),conditionLabels:{fixed_time:this._l("device_schedule.condition_fixed_time"),astro:this._l("device_schedule.condition_astro"),fixed_if_before_astro:this._l("device_schedule.condition_fixed_if_before_astro"),astro_if_before_fixed:this._l("device_schedule.condition_astro_if_before_fixed"),fixed_if_after_astro:this._l("device_schedule.condition_fixed_if_after_astro"),astro_if_after_fixed:this._l("device_schedule.condition_astro_if_after_fixed"),earliest:this._l("device_schedule.condition_earliest"),latest:this._l("device_schedule.condition_latest")},levelOn:this._l("device_schedule.level_on"),levelOff:this._l("device_schedule.level_off"),permanentOn:this._l("device_schedule.permanent_on"),showMore:this._l("device_schedule.show_more"),showLess:this._l("device_schedule.show_less"),conditionSummaryLabels:{sunrise:this._l("device_schedule.astro_sunrise"),sunset:this._l("device_schedule.astro_sunset"),or:this._l("device_schedule.or"),ifBefore:this._l("device_schedule.if_before"),ifAfter:this._l("device_schedule.if_after")},lockActionLockAutorelockEnd:this._l("device_schedule.lock_action_lock_autorelock_end"),lockActionLockAutorelockStart:this._l("device_schedule.lock_action_lock_autorelock_start"),lockActionUnlockAutorelockEnd:this._l("device_schedule.lock_action_unlock_autorelock_end"),lockActionAutorelockEnd:this._l("device_schedule.lock_action_autorelock_end"),permissionGranted:this._l("device_schedule.permission_granted"),permissionNotGranted:this._l("device_schedule.permission_not_granted")}}_buildDeviceEditorTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},addEvent:this._l("device_schedule.add_event"),editEvent:this._l("device_schedule.edit_event"),cancel:this._l("common.cancel"),save:this._l("device_schedule.save"),time:this._l("device_schedule.time"),condition:this._l("device_schedule.condition"),weekdaysLabel:this._l("device_schedule.weekdays_label"),stateLabel:this._l("device_schedule.level"),duration:this._l("device_schedule.duration"),rampTime:this._l("device_schedule.ramp_time"),channels:this._l("device_schedule.target_channel"),levelOn:this._l("device_schedule.level_on"),levelOff:this._l("device_schedule.level_off"),permanentOn:this._l("device_schedule.permanent_on"),slat:this._l("device_schedule.slat"),astroSunrise:this._l("device_schedule.astro_sunrise"),astroSunset:this._l("device_schedule.astro_sunset"),astroOffset:this._l("device_schedule.astro_offset"),confirmDelete:this._l("device_schedule.confirm_delete"),conditionLabels:{fixed_time:this._l("device_schedule.condition_fixed_time"),astro:this._l("device_schedule.condition_astro"),fixed_if_before_astro:this._l("device_schedule.condition_fixed_if_before_astro"),astro_if_before_fixed:this._l("device_schedule.condition_astro_if_before_fixed"),fixed_if_after_astro:this._l("device_schedule.condition_fixed_if_after_astro"),astro_if_after_fixed:this._l("device_schedule.condition_astro_if_after_fixed"),earliest:this._l("device_schedule.condition_earliest"),latest:this._l("device_schedule.condition_latest")},lockMode:this._l("device_schedule.lock_mode"),lockModeDoorLock:this._l("device_schedule.lock_mode_door_lock"),lockModeUserPermission:this._l("device_schedule.lock_mode_user_permission"),lockAction:this._l("device_schedule.lock_action"),lockActionLockAutorelockEnd:this._l("device_schedule.lock_action_lock_autorelock_end"),lockActionLockAutorelockStart:this._l("device_schedule.lock_action_lock_autorelock_start"),lockActionUnlockAutorelockEnd:this._l("device_schedule.lock_action_unlock_autorelock_end"),lockActionAutorelockEnd:this._l("device_schedule.lock_action_autorelock_end"),lockPermission:this._l("device_schedule.lock_permission"),permissionGranted:this._l("device_schedule.permission_granted"),permissionNotGranted:this._l("device_schedule.permission_not_granted")}}_renderDeviceSchedule(){const e=this._deviceData,t=e.schedule_data,i=t?.entries??{},s=Object.keys(i).length,a=e.schedule_domain??void 0,r=e.available_target_channels;return F`
      <div class="schedule-content">
        <div class="toolbar">
          <div class="schedule-info">
            ${this._l("device_schedule.entries",{count:s})} |
            ${this._l("device_schedule.max_entries",{max:e.max_entries})}
            ${e.schedule_domain?F` | ${e.schedule_domain}`:j}
          </div>
          <div class="toolbar-actions">
            <ha-button outlined @click=${this._handleExport}>
              ${this._l("device_schedule.export")}
            </ha-button>
            ${this.editable?F`
                  <ha-button outlined @click=${this._handleImport}>
                    ${this._l("device_schedule.import")}
                  </ha-button>
                  <ha-button outlined @click=${this._handleReload}>
                    ${this._l("device_schedule.reload")}
                  </ha-button>
                `:j}
          </div>
        </div>

        ${null!==e.schedule_enabled?F`<div class="schedule-enabled-bar">
              <span class="schedule-enabled-title"
                >${this._l("device_schedule.weekly_program")}:</span
              >
              <div class="channel-chips">
                ${Object.entries(e.schedule_enabled).map(([t,i])=>{const s=1===Object.keys(e.schedule_enabled).length?this._l(i?"device_schedule.schedule_enabled":"device_schedule.schedule_disabled"):e.available_target_channels?.[t]?.name??t;return F` <button
                    class="channel-chip ${i?"active":"inactive"}"
                    .disabled=${!this.editable||this._saving}
                    @click=${()=>this._handleScheduleEnabledToggle(t)}
                    title="${e.available_target_channels?.[t]?.name??t}: ${this._l(i?"device_schedule.weekly_program_enabled":"device_schedule.weekly_program_disabled")}"
                  >
                    ${s}
                  </button>`})}
              </div>
            </div>`:j}

        <div class="device-schedule-container">
          <hmip-device-schedule-list
            .scheduleData=${i}
            .domain=${a}
            .editable=${this.editable}
            .translations=${this._buildDeviceListTranslations()}
            @add-event=${this._onDeviceAddEvent}
            @edit-event=${this._onDeviceEditEvent}
            @delete-event=${this._onDeviceDeleteEvent}
          ></hmip-device-schedule-list>
        </div>

        <hmip-device-schedule-editor
          .open=${this._deviceShowEditor}
          .entry=${this._deviceEditingEntry}
          .groupNo=${this._deviceEditingGroupNo}
          .isNewEvent=${this._deviceIsNewEvent}
          .domain=${a}
          .availableTargetChannels=${r}
          .supportedScheduleFields=${e.supported_schedule_fields}
          .translations=${this._buildDeviceEditorTranslations()}
          @save-event=${this._onDeviceSaveEvent}
          @editor-closed=${this._onDeviceEditorClosed}
        ></hmip-device-schedule-editor>
      </div>

      ${this._saving?F`<div class="saving-overlay">${this._l("device_schedule.saving")}</div>`:j}
    `}static{this.styles=[Se,n`
      .schedule-header {
        margin-bottom: 16px;
      }

      .schedule-header h2 {
        margin: 8px 0 12px;
        font-size: 20px;
        font-weight: 400;
      }

      .device-selector ha-select {
        width: 100%;
      }

      .schedule-header ha-alert {
        margin-top: 8px;
      }

      .schedule-content {
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        overflow: hidden;
      }

      .toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: var(--secondary-background-color, #fafafa);
        border-bottom: 1px solid var(--divider-color, #e0e0e0);
        flex-wrap: wrap;
        gap: 8px;
      }

      .profile-selector {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .profile-selector label {
        font-size: 14px;
        font-weight: 500;
      }

      .profile-selector ha-select {
        min-width: 150px;
      }

      .toolbar-actions {
        display: flex;
        gap: 8px;
      }

      .schedule-info {
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      .climate-grid-container {
        padding: 16px;
      }

      .saving-overlay {
        text-align: center;
        padding: 12px;
        color: var(--secondary-text-color);
        font-style: italic;
      }

      .schedule-enabled-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        border-bottom: 1px solid var(--divider-color, #e0e0e0);
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

      .device-schedule-container {
        padding: 16px;
      }

      @media (max-width: 600px) {
        .toolbar {
          flex-direction: column;
          align-items: stretch;
        }

        .toolbar-actions {
          flex-wrap: wrap;
        }
      }
    `]}};e([he({attribute:!1})],di.prototype,"hass",void 0),e([he()],di.prototype,"entryId",void 0),e([he()],di.prototype,"deviceAddress",void 0),e([he()],di.prototype,"deviceName",void 0),e([he({type:Boolean})],di.prototype,"editable",void 0),e([pe()],di.prototype,"_devices",void 0),e([pe()],di.prototype,"_selectedDevice",void 0),e([pe()],di.prototype,"_climateData",void 0),e([pe()],di.prototype,"_deviceData",void 0),e([pe()],di.prototype,"_selectedProfile",void 0),e([pe()],di.prototype,"_editingWeekday",void 0),e([pe()],di.prototype,"_copiedSchedule",void 0),e([pe()],di.prototype,"_loading",void 0),e([pe()],di.prototype,"_saving",void 0),e([pe()],di.prototype,"_error",void 0),e([pe()],di.prototype,"_deviceEditingEntry",void 0),e([pe()],di.prototype,"_deviceEditingGroupNo",void 0),e([pe()],di.prototype,"_deviceShowEditor",void 0),e([pe()],di.prototype,"_deviceIsNewEvent",void 0),di=e([we("hm-device-schedule")],di);let ci=class extends oe{constructor(){super(...arguments),this.items=[]}_handleClick(e){e.view&&this.dispatchEvent(new CustomEvent("breadcrumb-navigate",{detail:{view:e.view,...e.detail},bubbles:!0,composed:!0}))}render(){return this.items.length<=1?j:F`
      <nav class="breadcrumb" aria-label="Navigation">
        ${this.items.map((e,t)=>F`
            ${t>0?F`<span class="separator" aria-hidden="true">›</span>`:j}
            ${t===this.items.length-1?F`<span class="current" aria-current="page">${e.label}</span>`:F`<a
                  class="link"
                  href="#"
                  @click=${t=>{t.preventDefault(),this._handleClick(e)}}
                  >${e.label}</a
                >`}
          `)}
      </nav>
    `}static{this.styles=n`
    .breadcrumb {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 4px;
      font-size: 13px;
      padding: 4px 0 8px;
      color: var(--secondary-text-color);
    }

    .link {
      color: var(--primary-color, #03a9f4);
      text-decoration: none;
      cursor: pointer;
    }

    .link:hover {
      text-decoration: underline;
    }

    .link:focus-visible {
      outline: 2px solid var(--primary-color, #03a9f4);
      outline-offset: 2px;
      border-radius: 2px;
    }

    .separator {
      color: var(--secondary-text-color);
      user-select: none;
    }

    .current {
      color: var(--primary-text-color);
      font-weight: 500;
    }

    @media (max-width: 600px) {
      .breadcrumb {
        font-size: 12px;
      }
    }
  `}};var hi;e([he({attribute:!1})],ci.prototype,"items",void 0),ci=e([we("hm-breadcrumb")],ci);let pi=class extends oe{constructor(){super(...arguments),this.narrow=!1,this._tab="devices",this._view="device-list",this._entryId="",this._entries=[],this._selectedDevice="",this._selectedInterfaceId="",this._selectedChannel="",this._selectedChannelType="",this._selectedParamsetKey="MASTER",this._selectedDeviceName="",this._selectedSenderAddress="",this._selectedReceiverAddress="",this._senderDeviceName="",this._senderDeviceModel="",this._senderChannelTypeLabel="",this._receiverDeviceName="",this._receiverDeviceModel="",this._receiverChannelTypeLabel="",this._onPopState=()=>{this._parseUrlHash()}}static{hi=this}connectedCallback(){super.connectedCallback(),this._resolveEntryId().then(()=>{this._loadPermissions(),this._parseUrlHash()}),window.addEventListener("popstate",this._onPopState)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("popstate",this._onPopState)}_parseUrlHash(){const e=window.location.hash.slice(1);if(!e)return;const t=new URLSearchParams(e),i=t.get("tab"),s=t.get("view"),a=t.get("entry")||this._entryId,r=t.get("device")||"",n=t.get("interface")||"",o=t.get("channel")||"",l=t.get("channel_type")||"",d=t.get("paramset")||"MASTER",c=t.get("sender")||"",h=t.get("receiver")||"";a&&(this._entryId=a),i&&(this._tab=i),s?this._navigateTo(s,{device:r,interfaceId:n,channel:o,channelType:l,paramsetKey:d,senderAddress:c,receiverAddress:h}):i&&this._switchTab(i)}_updateUrlHash(){const e=new URLSearchParams;e.set("tab",this._tab),e.set("view",this._view),this._entryId&&e.set("entry",this._entryId),"device-list"!==this._view&&(this._selectedDevice&&e.set("device",this._selectedDevice),this._selectedInterfaceId&&e.set("interface",this._selectedInterfaceId)),"channel-config"===this._view&&(this._selectedChannel&&e.set("channel",this._selectedChannel),this._selectedChannelType&&e.set("channel_type",this._selectedChannelType),"MASTER"!==this._selectedParamsetKey&&e.set("paramset",this._selectedParamsetKey)),"link-config"===this._view&&(this._selectedSenderAddress&&e.set("sender",this._selectedSenderAddress),this._selectedReceiverAddress&&e.set("receiver",this._selectedReceiverAddress)),"add-link"===this._view&&this._selectedChannel&&e.set("channel",this._selectedChannel);const t=e.toString();window.history.pushState(null,"",`#${t}`)}static{this._STORAGE_KEY="hmip_selected_entry_id"}async _resolveEntryId(){const e=(await this.hass.callWS({type:"config_entries/get",domain:"homematicip_local"})).filter(e=>"loaded"===e.state).map(e=>({entry_id:e.entry_id,title:e.title}));if(this._entries=e,1===this._entries.length)this._entryId=this._entries[0].entry_id;else if(this._entries.length>1){const e=localStorage.getItem(hi._STORAGE_KEY);e&&this._entries.some(t=>t.entry_id===e)&&(this._entryId=e)}}async _loadPermissions(){if(this._entryId)try{this._permissions=await async function(e,t){return e.callWS({type:"homematicip_local/config/get_user_permissions",entry_id:t})}(this.hass,this._entryId)}catch{this._permissions={is_admin:!0,permissions:[],backend:null}}}_hasPermission(e){return!!this._permissions&&(this._permissions.is_admin||this._permissions.permissions.includes(e))}async _ensureView(e){switch(e){case"ccu-dashboard":await Promise.resolve().then(function(){return mi});break;case"integration-dashboard":await Promise.resolve().then(function(){return fi});break;case"change-history":await Promise.resolve().then(function(){return yi})}}_navigateTo(e,t){this._ensureView(e),this._view=e,void 0!==t?.device&&(this._selectedDevice=t.device),void 0!==t?.interfaceId&&(this._selectedInterfaceId=t.interfaceId),void 0!==t?.channel&&(this._selectedChannel=t.channel),void 0!==t?.channelType&&(this._selectedChannelType=t.channelType),void 0!==t?.paramsetKey&&(this._selectedParamsetKey=t.paramsetKey),void 0!==t?.deviceName&&(this._selectedDeviceName=t.deviceName),void 0!==t?.senderAddress&&(this._selectedSenderAddress=t.senderAddress),void 0!==t?.receiverAddress&&(this._selectedReceiverAddress=t.receiverAddress),void 0!==t?.senderDeviceName&&(this._senderDeviceName=t.senderDeviceName),void 0!==t?.senderDeviceModel&&(this._senderDeviceModel=t.senderDeviceModel),void 0!==t?.senderChannelTypeLabel&&(this._senderChannelTypeLabel=t.senderChannelTypeLabel),void 0!==t?.receiverDeviceName&&(this._receiverDeviceName=t.receiverDeviceName),void 0!==t?.receiverDeviceModel&&(this._receiverDeviceModel=t.receiverDeviceModel),void 0!==t?.receiverChannelTypeLabel&&(this._receiverChannelTypeLabel=t.receiverChannelTypeLabel),this._updateUrlHash()}_switchTab(e){switch(this._tab=e,e){case"devices":this._view="device-list";break;case"integration":this._view="integration-dashboard";break;case"ccu":this._view="ccu-dashboard"}this._ensureView(this._view),this._updateUrlHash()}_l(e,t){return tt(this.hass,e,t)}_renderTabs(){const e=[{id:"devices",label:this._l("tabs.devices")}];return this._hasPermission("system_admin")&&(e.push({id:"integration",label:this._l("tabs.integration")}),"CCU"===this._permissions?.backend&&e.push({id:"ccu",label:this._l("tabs.ccu")})),F`
      <div class="tab-bar">
        ${e.map(e=>F`
            <button
              class="tab ${this._tab===e.id?"active":""}"
              @click=${()=>this._switchTab(e.id)}
            >
              ${e.label}
            </button>
          `)}
      </div>
    `}_getBreadcrumbItems(){const e=[],t=this._l("tabs.devices");if("device-list"===this._view||"devices"!==this._tab)return e;e.push({label:t,view:"device-list"});const i=this._selectedDeviceName||this._selectedDevice||"...";if("device-detail"===this._view)return e.push({label:i}),e;switch(e.push({label:i,view:"device-detail",detail:{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}}),this._view){case"channel-config":e.push({label:this._selectedChannel||"..."});break;case"change-history":e.push({label:this._l("change_history.title")});break;case"device-links":e.push({label:this._l("device_links.title")});break;case"link-config":e.push({label:this._l("device_links.title"),view:"device-links",detail:{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}}),e.push({label:this._l("link_config.title")});break;case"add-link":e.push({label:this._l("device_links.title"),view:"device-links",detail:{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}}),e.push({label:this._l("add_link.title")});break;case"device-schedule":e.push({label:this._l("device_schedule.title")})}return e}_handleBreadcrumbNavigate(e){const{view:t,...i}=e.detail;t&&this._navigateTo(t,i)}_renderBreadcrumb(){const e=this._getBreadcrumbItems();return 0===e.length?j:F`
      <hm-breadcrumb
        .items=${e}
        @breadcrumb-navigate=${this._handleBreadcrumbNavigate}
      ></hm-breadcrumb>
    `}_renderToolbar(){return F`
      <div class="toolbar">
        <ha-menu-button .hass=${this.hass} .narrow=${this.narrow}></ha-menu-button>
        <div class="main-title">${this._l("device_list.title")}</div>
      </div>
    `}_renderEntrySelector(){return this._entries.length<=1?j:F`
      <div class="entry-selector">
        <ha-select
          .label=${this._l("device_list.select_ccu")}
          .value=${this._entryId}
          .options=${this._entries.map(e=>({value:e.entry_id,label:e.title}))}
          @selected=${e=>{e.stopPropagation();const t=e.detail.value;t&&t!==this._entryId&&(this._entryId=t,localStorage.setItem(hi._STORAGE_KEY,t),this._loadPermissions(),this._updateUrlHash())}}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>
    `}render(){if("integration-dashboard"===this._view)return F`
        ${this._renderToolbar()} ${this._renderEntrySelector()} ${this._renderTabs()}
        ${ke(this._view,F`<div class="view-content">
            <hm-integration-dashboard
              .hass=${this.hass}
              .entryId=${this._entryId}
            ></hm-integration-dashboard>
          </div>`)}
      `;if("ccu-dashboard"===this._view)return F`
        ${this._renderToolbar()} ${this._renderEntrySelector()} ${this._renderTabs()}
        ${ke(this._view,F`<div class="view-content">
            <hm-ccu-dashboard .hass=${this.hass} .entryId=${this._entryId}></hm-ccu-dashboard>
          </div>`)}
      `;switch(this._view){case"device-list":return F`
          ${this._renderToolbar()} ${this._renderEntrySelector()} ${this._renderTabs()}
          ${ke(this._view,F`<div class="view-content">
              <hm-device-list
                .hass=${this.hass}
                .entryId=${this._entryId}
                @device-selected=${e=>this._navigateTo("device-detail",e.detail)}
              ></hm-device-list>
            </div>`)}
        `;case"device-detail":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-device-detail
                .hass=${this.hass}
                .entryId=${this._entryId}
                .interfaceId=${this._selectedInterfaceId}
                .deviceAddress=${this._selectedDevice}
                @channel-selected=${e=>this._navigateTo("channel-config",e.detail)}
                @show-history=${e=>this._navigateTo("change-history",e.detail)}
                @show-links=${e=>this._navigateTo("device-links",e.detail)}
                @show-schedules=${e=>this._navigateTo("device-schedule",e.detail)}
                @back=${()=>this._navigateTo("device-list")}
              ></hm-device-detail>
            </div>`)}
        `;case"channel-config":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-channel-config
                .hass=${this.hass}
                .entryId=${this._entryId}
                .interfaceId=${this._selectedInterfaceId}
                .channelAddress=${this._selectedChannel}
                .channelType=${this._selectedChannelType}
                .paramsetKey=${this._selectedParamsetKey}
                .deviceName=${this._selectedDeviceName}
                .editable=${this._hasPermission("device_config")}
                @back=${()=>this._navigateTo("device-detail",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
              ></hm-channel-config>
            </div>`)}
        `;case"change-history":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-change-history
                .hass=${this.hass}
                .entryId=${this._entryId}
                .filterDevice=${this._selectedDevice}
                .editable=${this._hasPermission("system_admin")}
                @back=${()=>this._navigateTo(this._selectedDevice?"device-detail":"device-list",this._selectedDevice?{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}:void 0)}
              ></hm-change-history>
            </div>`)}
        `;case"device-links":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-device-links
                .hass=${this.hass}
                .entryId=${this._entryId}
                .interfaceId=${this._selectedInterfaceId}
                .deviceAddress=${this._selectedDevice}
                .deviceName=${this._selectedDeviceName}
                .editable=${this._hasPermission("device_links")}
                @configure-link=${e=>this._navigateTo("link-config",e.detail)}
                @add-link=${e=>this._navigateTo("add-link",e.detail)}
                @back=${()=>this._navigateTo("device-detail",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
              ></hm-device-links>
            </div>`)}
        `;case"link-config":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-link-config
                .hass=${this.hass}
                .entryId=${this._entryId}
                .interfaceId=${this._selectedInterfaceId}
                .senderAddress=${this._selectedSenderAddress}
                .receiverAddress=${this._selectedReceiverAddress}
                .editable=${this._hasPermission("device_links")}
                .senderDeviceName=${this._senderDeviceName}
                .senderDeviceModel=${this._senderDeviceModel}
                .senderChannelTypeLabel=${this._senderChannelTypeLabel}
                .receiverDeviceName=${this._receiverDeviceName}
                .receiverDeviceModel=${this._receiverDeviceModel}
                .receiverChannelTypeLabel=${this._receiverChannelTypeLabel}
                @back=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
              ></hm-link-config>
            </div>`)}
        `;case"add-link":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-add-link
                .hass=${this.hass}
                .entryId=${this._entryId}
                .interfaceId=${this._selectedInterfaceId}
                .deviceAddress=${this._selectedDevice}
                @link-created=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
                @back=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
              ></hm-add-link>
            </div>`)}
        `;case"device-schedule":return F`
          ${this._renderToolbar()} ${this._renderBreadcrumb()}
          ${ke(this._view,F`<div class="view-content">
              <hm-device-schedule
                .hass=${this.hass}
                .entryId=${this._entryId}
                .deviceAddress=${this._selectedDevice}
                .deviceName=${this._selectedDeviceName}
                .editable=${this._hasPermission("schedule_edit")}
                @back=${()=>this._navigateTo(this._selectedDevice?"device-detail":"device-list",this._selectedDevice?{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}:void 0)}
              ></hm-device-schedule>
            </div>`)}
        `}}static{this.styles=n`
    :host {
      display: block;
      padding: 16px;
      max-width: 1200px;
      margin: 0 auto;
      font-family: var(--paper-font-body1_-_font-family, "Roboto", sans-serif);
      color: var(--primary-text-color);
      background-color: var(--primary-background-color);
    }

    .toolbar {
      display: flex;
      align-items: center;
      height: 48px;
      margin: -16px -16px 16px -16px;
      padding: 0 4px;
      background-color: var(--app-header-background-color, var(--primary-color));
      color: var(--app-header-text-color, var(--text-primary-color, #fff));
      font-size: 20px;
      --ha-icon-button-color: var(--app-header-text-color, var(--text-primary-color, #fff));
    }

    .main-title {
      margin-left: 8px;
      font-weight: 400;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .entry-selector {
      margin-bottom: 16px;
    }

    .entry-selector ha-select {
      width: 100%;
    }

    .tab-bar {
      display: flex;
      gap: 4px;
      margin-bottom: 16px;
      border-bottom: 2px solid var(--divider-color);
      padding-bottom: 0;
    }

    .tab {
      padding: 8px 16px;
      border: none;
      background: none;
      font-size: 14px;
      font-weight: 500;
      color: var(--secondary-text-color);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      margin-bottom: -2px;
      transition:
        color 0.2s,
        border-color 0.2s;
      font-family: inherit;
    }

    .tab:hover {
      color: var(--primary-text-color);
    }

    .tab.active {
      color: var(--primary-color);
      border-bottom-color: var(--primary-color);
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(4px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .view-content {
      animation: fadeIn 0.2s ease-out;
    }

    @media (max-width: 600px) {
      :host {
        padding: 8px;
      }

      .toolbar {
        margin: -8px -8px 8px -8px;
      }

      .tab-bar {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
      }

      .tab-bar::-webkit-scrollbar {
        display: none;
      }

      .tab {
        padding: 8px 12px;
        font-size: 13px;
        white-space: nowrap;
      }
    }
  `}};var _i;e([he({attribute:!1})],pi.prototype,"hass",void 0),e([he({attribute:!1})],pi.prototype,"panel",void 0),e([he({type:Boolean,reflect:!0})],pi.prototype,"narrow",void 0),e([pe()],pi.prototype,"_tab",void 0),e([pe()],pi.prototype,"_view",void 0),e([pe()],pi.prototype,"_entryId",void 0),e([pe()],pi.prototype,"_entries",void 0),e([pe()],pi.prototype,"_selectedDevice",void 0),e([pe()],pi.prototype,"_selectedInterfaceId",void 0),e([pe()],pi.prototype,"_selectedChannel",void 0),e([pe()],pi.prototype,"_selectedChannelType",void 0),e([pe()],pi.prototype,"_selectedParamsetKey",void 0),e([pe()],pi.prototype,"_selectedDeviceName",void 0),e([pe()],pi.prototype,"_selectedSenderAddress",void 0),e([pe()],pi.prototype,"_selectedReceiverAddress",void 0),e([pe()],pi.prototype,"_permissions",void 0),e([pe()],pi.prototype,"_senderDeviceName",void 0),e([pe()],pi.prototype,"_senderDeviceModel",void 0),e([pe()],pi.prototype,"_senderChannelTypeLabel",void 0),e([pe()],pi.prototype,"_receiverDeviceName",void 0),e([pe()],pi.prototype,"_receiverDeviceModel",void 0),e([pe()],pi.prototype,"_receiverChannelTypeLabel",void 0),pi=hi=e([we("homematic-config")],pi);let ui=class extends oe{constructor(){super(...arguments),this.entryId="",this._subTab="general",this._sysInfo=null,this._installMode=null,this._signalDevices=null,this._firmware=null,this._inboxDevices=[],this._serviceMessages=[],this._alarmMessages=[],this._loading=!0,this._error="",this._backupRunning=!1,this._refreshingFirmware=!1,this._signalSortColumn="name",this._signalSortAsc=!0,this._signalFilter="",this._signalInterfaceFilter="",this._signalReachableFilter="",this._signalBatteryFilter="",this._firmwareSortColumn="name",this._firmwareSortAsc=!0,this._firmwareFilter="",this._firmwareStateFilter=""}static{_i=this}static{this._POLL_INTERVAL=3e4}disconnectedCallback(){super.disconnectedCallback(),this._stopInstallModePolling(),this._stopPolling()}updated(e){e.has("entryId")&&this.entryId&&(this._stopPolling(),this._fetchAll())}_scheduleNextPoll(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchAll(),_i._POLL_INTERVAL)}_stopPolling(){void 0!==this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchAll(){if(this.entryId){null===this._sysInfo&&(this._loading=!0),this._error="";try{const[e,t,i,s,a,r,n]=await Promise.all([Oe(this.hass,this.entryId),je(this.hass,this.entryId),Ke(this.hass,this.entryId),Ye(this.hass,this.entryId),Ge(this.hass,this.entryId).catch(()=>[]),Ze(this.hass,this.entryId).catch(()=>[]),qe(this.hass,this.entryId).catch(()=>[])]);this._sysInfo=e,this._installMode=t,this._signalDevices=i,this._firmware=s,this._inboxDevices=a,this._serviceMessages=r,this._alarmMessages=n,(t.hmip.active||t.bidcos.active)&&this._startInstallModePolling()}catch(e){this._error=String(e)}finally{this._loading=!1,this._scheduleNextPoll()}}}_l(e,t){return tt(this.hass,e,t)}async _handleCreateBackup(){if(await st(0,{title:this._l("ccu.create_backup_title"),text:this._l("ccu.create_backup_text"),confirmText:this._l("ccu.create_backup"),dismissText:this._l("common.cancel")})){this._backupRunning=!0;try{const e=await async function(e,t){return e.callWS({type:"homematicip_local/ccu/create_backup",entry_id:t})}(this.hass,this.entryId);if(e.success){const t=(e.size/1024/1024).toFixed(1);rt(this,{message:this._l("ccu.backup_success",{filename:e.filename,size:t})})}}catch{rt(this,{message:this._l("ccu.backup_failed")})}finally{this._backupRunning=!1}}}async _handleTriggerInstallMode(e){const t="hmip"===e?"HmIP-RF":"BidCos-RF";if(await st(0,{title:this._l("ccu.install_mode_title"),text:this._l("ccu.install_mode_text",{interface:t}),confirmText:this._l("ccu.activate"),dismissText:this._l("common.cancel")}))try{await async function(e,t,i){return e.callWS({type:"homematicip_local/ccu/trigger_install_mode",entry_id:t,interface:i})}(this.hass,this.entryId,e),rt(this,{message:this._l("ccu.install_mode_activated",{interface:t})}),this._installMode=await je(this.hass,this.entryId),this._startInstallModePolling()}catch{rt(this,{message:this._l("ccu.action_failed")})}}_startInstallModePolling(){this._stopInstallModePolling(),this._installModeTimer=setInterval(async()=>{try{this._installMode=await je(this.hass,this.entryId),this._installMode.hmip.active||this._installMode.bidcos.active||this._stopInstallModePolling()}catch{this._stopInstallModePolling()}},1e3)}_stopInstallModePolling(){void 0!==this._installModeTimer&&(clearInterval(this._installModeTimer),this._installModeTimer=void 0)}async _handleRefreshFirmware(){this._refreshingFirmware=!0;try{await async function(e,t){return e.callWS({type:"homematicip_local/ccu/refresh_firmware_data",entry_id:t})}(this.hass,this.entryId),rt(this,{message:this._l("ccu.firmware_refreshed")}),this._firmware=await Ye(this.hass,this.entryId)}catch{rt(this,{message:this._l("ccu.action_failed")})}finally{this._refreshingFirmware=!1}}async _handleUpdateFirmware(e){if(await st(0,{title:this._l("ccu.update_firmware"),text:this._l("ccu.update_firmware_confirm",{device:e.name}),confirmText:this._l("ccu.update_firmware"),dismissText:this._l("common.cancel")}))try{await async function(e,t,i){return e.callWS({type:"homematicip_local/ccu/update_firmware",entry_id:t,device_address:i})}(this.hass,this.entryId,e.address),rt(this,{message:this._l("ccu.update_firmware_success",{device:e.name})})}catch{rt(this,{message:this._l("ccu.update_firmware_failed")})}}_switchSubTab(e){this._subTab=e}_renderSubTabs(){const e=[{id:"general",label:this._l("ccu.tab_general")},{id:"messages",label:this._l("ccu.tab_messages"),badge:this._serviceMessages.length+this._alarmMessages.length},{id:"pairing",label:this._l("ccu.tab_pairing"),badge:this._inboxDevices.length},{id:"signal",label:this._l("ccu.tab_signal")},{id:"firmware",label:this._l("ccu.tab_firmware")}];return F`
      <div class="sub-tab-bar">
        ${e.map(e=>F`
            <button
              class="sub-tab ${this._subTab===e.id?"active":""}"
              @click=${()=>this._switchSubTab(e.id)}
            >
              ${e.label} ${e.badge?F`<span class="tab-badge">${e.badge}</span>`:j}
            </button>
          `)}
      </div>
    `}_renderSubTabContent(){switch(this._subTab){case"general":return F`${this._renderSystemInfoCard()} ${this._renderActionsCard()}`;case"pairing":return F`${this._renderInstallModeCard()} ${this._renderInboxCard()}`;case"messages":return F`${this._renderServiceMessagesCard()} ${this._renderAlarmMessagesCard()}`;case"signal":return F`${this._renderSignalQualityCard()}`;case"firmware":return F`${this._renderFirmwareCard()}`}}render(){return this.entryId?this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:this._error?F`<div class="error">${this._error}</div>`:F` ${this._renderSubTabs()} ${this._renderSubTabContent()} `:F`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}_renderSystemInfoCard(){if(!this._sysInfo)return j;const e=this._sysInfo;return F`
      <ha-card>
        <div class="card-header">${this._l("ccu.system_information")}</div>
        <div class="card-content">
          <div class="kv-grid">
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.name")}</span>
              <span class="kv-value">${e.name}</span>
            </div>
            ${e.model?F`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.model")}</span>
                    <span class="kv-value">${e.model}</span>
                  </div>
                `:j}
            ${e.version?F`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.version")}</span>
                    <span class="kv-value">${e.version}</span>
                  </div>
                `:j}
            ${e.serial?F`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.serial")}</span>
                    <span class="kv-value">${e.serial}</span>
                  </div>
                `:j}
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.hostname")}</span>
              <span class="kv-value">${e.hostname}</span>
            </div>
            ${e.ccu_type?F`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.ccu_type")}</span>
                    <span class="kv-value">${e.ccu_type}</span>
                  </div>
                `:j}
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.interfaces")}</span>
              <span class="kv-value">${e.available_interfaces.join(", ")}</span>
            </div>
            ${null!==e.auth_enabled?F`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.auth_enabled")}</span>
                    <span class="kv-value"
                      >${this._l(e.auth_enabled?"common.yes":"common.no")}</span
                    >
                  </div>
                `:j}
          </div>
          <div class="status-badges"></div>
        </div>
      </ha-card>
    `}_renderInstallModeCard(){if(!this._installMode)return j;const{hmip:e,bidcos:t}=this._installMode;return e.available||t.available?F`
      <ha-card>
        <div class="card-header">${this._l("ccu.install_mode")}</div>
        <div class="card-content">
          <div class="install-mode-grid">
            ${e.available?this._renderInstallModeItem("HmIP-RF","hmip",e):j}
            ${t.available?this._renderInstallModeItem("BidCos-RF","bidcos",t):j}
          </div>
        </div>
      </ha-card>
    `:j}_renderInstallModeItem(e,t,i){return F`
      <div class="install-mode-item">
        <div class="install-mode-header">
          <span class="install-mode-label">${e}</span>
          <span class="install-mode-status ${i.active?"active":""}">
            ${this._l(i.active?"ccu.active":"ccu.inactive")}
          </span>
        </div>
        ${i.active&&null!==i.remaining_seconds?F`<span class="install-mode-remaining"
              >${this._l("ccu.remaining_seconds",{seconds:i.remaining_seconds})}</span
            >`:j}
        ${i.active?j:F`
              <ha-button @click=${()=>this._handleTriggerInstallMode(t)}>
                ${this._l("ccu.activate")}
              </ha-button>
            `}
      </div>
    `}async _handleAcceptInboxDevice(e){const t=await(i={title:this._l("ccu.accept_device_title"),text:this._l("ccu.accept_device_text",{device:e.name||e.address}),inputLabel:this._l("ccu.device_name"),defaultValue:e.name||"",confirmText:this._l("ccu.accept"),dismissText:this._l("common.cancel")},new Promise(e=>{const t=document.activeElement,s=document.createElement("dialog");s.style.cssText=["border: none","border-radius: var(--ha-card-border-radius, 12px)","padding: 24px","max-width: 450px","width: calc(100% - 48px)","max-height: 90vh","overflow-y: auto","box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3)","font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif)","background: var(--card-background-color, var(--ha-card-background, #fff))","color: var(--primary-text-color, #212121)"].join("; ");const a=i.title?`<h2 style="margin: 0 0 16px; font-size: 18px; font-weight: 500;">${at(i.title)}</h2>`:"",r=i.text?`<p style="margin: 0 0 16px; white-space: pre-line; line-height: 1.5; color: var(--secondary-text-color, #727272);">${at(i.text)}</p>`:"",n=i.inputLabel?`<label style="display: block; margin-bottom: 4px; font-size: 12px; color: var(--secondary-text-color, #727272);">${at(i.inputLabel)}</label>`:"";s.innerHTML=`\n      ${a}\n      ${r}\n      ${n}\n      <input type="text" class="prompt-input" value="${at(i.defaultValue||"")}" style="\n        width: 100%;\n        padding: 8px 12px;\n        border: 1px solid var(--divider-color, #e0e0e0);\n        border-radius: 4px;\n        background: var(--card-background-color, #fff);\n        color: var(--primary-text-color, #212121);\n        font-size: 14px;\n        font-family: inherit;\n        box-sizing: border-box;\n        margin-bottom: 24px;\n      " />\n      <div style="display: flex; justify-content: flex-end; gap: 8px;">\n        <button class="dismiss" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: transparent;\n          color: var(--primary-text-color, #212121);\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${at(i.dismissText||"Cancel")}</button>\n        <button class="confirm" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: var(--primary-color, #03a9f4);\n          color: #fff;\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${at(i.confirmText||"OK")}</button>\n      </div>\n    `;const o=i=>{s.close(),s.remove(),t?.focus(),e(i)},l=s.querySelector(".prompt-input");s.querySelector(".confirm").addEventListener("click",()=>o(l.value)),s.querySelector(".dismiss").addEventListener("click",()=>o(null)),l.addEventListener("keydown",e=>{"Enter"===e.key&&o(l.value)}),s.addEventListener("cancel",e=>{e.preventDefault(),o(null)}),document.body.appendChild(s),s.showModal(),l.focus(),l.select()}));var i;if(null!==t)try{await async function(e,t,i,s,a){return e.callWS({type:"homematicip_local/ccu/accept_inbox_device",entry_id:t,device_address:i,...s&&a?{device_name:s,device_id:a}:{}})}(this.hass,this.entryId,e.address,t||void 0,t?e.device_id:void 0),rt(this,{message:this._l("ccu.accept_device_success",{device:t||e.address})}),this._inboxDevices=await Ge(this.hass,this.entryId).catch(()=>[])}catch{rt(this,{message:this._l("ccu.action_failed")})}}async _handleAcknowledgeServiceMessage(e){try{await async function(e,t,i){return e.callWS({type:"homematicip_local/ccu/acknowledge_service_message",entry_id:t,msg_id:i})}(this.hass,this.entryId,e.msg_id),rt(this,{message:this._l("ccu.message_acknowledged")}),this._serviceMessages=await Ze(this.hass,this.entryId).catch(()=>[])}catch{rt(this,{message:this._l("ccu.action_failed")})}}async _handleAcknowledgeAlarmMessage(e){try{await async function(e,t,i){return e.callWS({type:"homematicip_local/ccu/acknowledge_alarm_message",entry_id:t,alarm_id:i})}(this.hass,this.entryId,e.alarm_id),rt(this,{message:this._l("ccu.message_acknowledged")}),this._alarmMessages=await qe(this.hass,this.entryId).catch(()=>[])}catch{rt(this,{message:this._l("ccu.action_failed")})}}_renderInboxCard(){return F`
      <ha-card>
        <div class="card-header">
          <span>${this._l("ccu.inbox")}</span>
          ${this._inboxDevices.length>0?F`<span class="badge">${this._inboxDevices.length}</span>`:j}
        </div>
        <div class="card-content">
          ${0===this._inboxDevices.length?F`<div class="empty-hint">${this._l("ccu.no_inbox_devices")}</div>`:F`
                <div class="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>${this._l("ccu.device")}</th>
                        <th>${this._l("ccu.address")}</th>
                        <th>${this._l("ccu.device_type")}</th>
                        <th>${this._l("ccu.interface")}</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      ${this._inboxDevices.map(e=>F`
                          <tr>
                            <td class="device-name" data-label=${this._l("ccu.device")}>
                              ${e.name||"—"}
                            </td>
                            <td data-label=${this._l("ccu.address")}>${e.address}</td>
                            <td data-label=${this._l("ccu.device_type")}>${e.device_type}</td>
                            <td data-label=${this._l("ccu.interface")}>${e.interface}</td>
                            <td>
                              <ha-button @click=${()=>this._handleAcceptInboxDevice(e)}>
                                ${this._l("ccu.accept")}
                              </ha-button>
                            </td>
                          </tr>
                        `)}
                    </tbody>
                  </table>
                </div>
              `}
        </div>
      </ha-card>
    `}_renderServiceMessagesCard(){return F`
      <ha-card>
        <div class="card-header">
          <span>${this._l("ccu.service_messages")}</span>
          ${this._serviceMessages.length>0?F`<span class="badge warning">${this._serviceMessages.length}</span>`:j}
        </div>
        <div class="card-content">
          ${0===this._serviceMessages.length?F`<div class="empty-hint">${this._l("ccu.no_service_messages")}</div>`:F`<div class="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>${this._l("ccu.device")}</th>
                      <th>${this._l("ccu.address")}</th>
                      <th>${this._l("ccu.msg_type")}</th>
                      <th>${this._l("ccu.message")}</th>
                      <th>${this._l("ccu.timestamp")}</th>
                      <th>${this._l("ccu.counter_label")}</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    ${this._serviceMessages.map(e=>F`
                        <tr>
                          <td class="device-name" data-label=${this._l("ccu.device")}>
                            ${e.device_name||"—"}
                          </td>
                          <td data-label=${this._l("ccu.address")}>${e.address||"—"}</td>
                          <td data-label=${this._l("ccu.msg_type")}>
                            <span class="msg-type msg-type-${e.msg_type}">
                              ${e.msg_type_name}
                            </span>
                          </td>
                          <td data-label=${this._l("ccu.message")}>${e.display_name}</td>
                          <td class="timestamp-cell" data-label=${this._l("ccu.timestamp")}>
                            ${e.timestamp||"—"}
                          </td>
                          <td data-label=${this._l("ccu.counter_label")}>
                            ${e.counter>1?e.counter:""}
                          </td>
                          <td>
                            ${e.quittable?F`
                                  <ha-button
                                    @click=${()=>this._handleAcknowledgeServiceMessage(e)}
                                  >
                                    ${this._l("ccu.acknowledge")}
                                  </ha-button>
                                `:j}
                          </td>
                        </tr>
                      `)}
                  </tbody>
                </table>
              </div>`}
        </div>
      </ha-card>
    `}_renderAlarmMessagesCard(){return F`
      <ha-card>
        <div class="card-header">
          <span>${this._l("ccu.alarm_messages")}</span>
          ${this._alarmMessages.length>0?F`<span class="badge error">${this._alarmMessages.length}</span>`:j}
        </div>
        <div class="card-content">
          ${0===this._alarmMessages.length?F`<div class="empty-hint">${this._l("ccu.no_alarm_messages")}</div>`:F`<div class="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>${this._l("ccu.device")}</th>
                      <th>${this._l("ccu.message")}</th>
                      <th>${this._l("ccu.description")}</th>
                      <th>${this._l("ccu.last_trigger")}</th>
                      <th>${this._l("ccu.timestamp")}</th>
                      <th>${this._l("ccu.counter_label")}</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    ${this._alarmMessages.map(e=>F`
                        <tr>
                          <td class="device-name" data-label=${this._l("ccu.device")}>
                            ${e.device_name||"—"}
                          </td>
                          <td data-label=${this._l("ccu.message")}>${e.display_name}</td>
                          <td data-label=${this._l("ccu.description")}>
                            ${e.description||"—"}
                          </td>
                          <td data-label=${this._l("ccu.last_trigger")}>
                            ${e.last_trigger||"—"}
                          </td>
                          <td class="timestamp-cell" data-label=${this._l("ccu.timestamp")}>
                            ${e.timestamp||"—"}
                          </td>
                          <td data-label=${this._l("ccu.counter_label")}>
                            ${e.counter>1?e.counter:""}
                          </td>
                          <td>
                            <ha-button @click=${()=>this._handleAcknowledgeAlarmMessage(e)}>
                              ${this._l("ccu.acknowledge")}
                            </ha-button>
                          </td>
                        </tr>
                      `)}
                  </tbody>
                </table>
              </div>`}
        </div>
      </ha-card>
    `}_filterSignalDevices(e){return e.filter(e=>{if(this._signalFilter){const t=this._signalFilter.toLowerCase();if(!e.name.toLowerCase().includes(t)&&!e.model.toLowerCase().includes(t))return!1}if(this._signalInterfaceFilter&&e.interface_id!==this._signalInterfaceFilter)return!1;if(this._signalReachableFilter&&String(e.is_reachable)!==this._signalReachableFilter)return!1;if(this._signalBatteryFilter){if("low"===this._signalBatteryFilter&&!0!==e.low_battery)return!1;if("ok"===this._signalBatteryFilter&&!1!==e.low_battery)return!1}return!0})}_renderSignalQualityCard(){if(!this._signalDevices||0===this._signalDevices.length)return j;const e=this._signalDevices.length>10,t=e?this._filterSignalDevices(this._signalDevices):this._signalDevices,i=[...t].sort((e,t)=>{const i=this._signalSortColumn,s=this._compareValues(e[i],t[i]);return this._signalSortAsc?s:-s}),s=e&&t.length!==this._signalDevices.length,a=[...new Set(this._signalDevices.map(e=>e.interface_id))].sort();return F`
      <ha-card>
        <div class="card-header">${this._l("ccu.signal_quality")}</div>
        <div class="card-content table-wrapper">
          ${e?F`
                <div class="filter-bar">
                  <ha-input
                    .value=${this._signalFilter}
                    .placeholder=${this._l("ccu.filter_devices")}
                    aria-label=${this._l("ccu.filter_devices")}
                    @input=${e=>{this._signalFilter=e.target.value}}
                    class="filter-search"
                  ></ha-input>
                  <div class="filter-selects">
                    <ha-select
                      .label=${this._l("ccu.interface")}
                      .value=${this._signalInterfaceFilter}
                      .options=${[{value:"",label:this._l("ccu.filter_all")},...a.map(e=>({value:e,label:e}))]}
                      @selected=${e=>{e.stopPropagation(),this._signalInterfaceFilter=e.detail.value??""}}
                      @closed=${e=>e.stopPropagation()}
                    ></ha-select>
                    <ha-select
                      .label=${this._l("ccu.reachable")}
                      .value=${this._signalReachableFilter}
                      .options=${[{value:"",label:this._l("ccu.filter_all")},{value:"true",label:this._l("common.yes")},{value:"false",label:this._l("common.no")}]}
                      @selected=${e=>{e.stopPropagation(),this._signalReachableFilter=e.detail.value??""}}
                      @closed=${e=>e.stopPropagation()}
                    ></ha-select>
                    <ha-select
                      .label=${this._l("ccu.battery")}
                      .value=${this._signalBatteryFilter}
                      .options=${[{value:"",label:this._l("ccu.filter_all")},{value:"ok",label:this._l("ccu.ok")},{value:"low",label:this._l("ccu.low")}]}
                      @selected=${e=>{e.stopPropagation(),this._signalBatteryFilter=e.detail.value??""}}
                      @closed=${e=>e.stopPropagation()}
                    ></ha-select>
                  </div>
                </div>
                ${s?F`<div class="filter-count">
                      ${this._l("ccu.filter_result",{count:t.length,total:this._signalDevices.length})}
                    </div>`:j}
              `:j}
          <table>
            <thead>
              <tr>
                <th @click=${()=>this._toggleSignalSort("name")}>
                  ${this._l("ccu.device")} ${this._sortIcon("signal","name")}
                </th>
                <th @click=${()=>this._toggleSignalSort("model")}>
                  ${this._l("ccu.model")} ${this._sortIcon("signal","model")}
                </th>
                <th @click=${()=>this._toggleSignalSort("interface_id")}>
                  ${this._l("ccu.interface")} ${this._sortIcon("signal","interface_id")}
                </th>
                <th @click=${()=>this._toggleSignalSort("is_reachable")}>
                  ${this._l("ccu.reachable")} ${this._sortIcon("signal","is_reachable")}
                </th>
                <th @click=${()=>this._toggleSignalSort("rssi_device")}>
                  RSSI ${this._sortIcon("signal","rssi_device")}
                </th>
                <th @click=${()=>this._toggleSignalSort("low_battery")}>
                  ${this._l("ccu.battery")} ${this._sortIcon("signal","low_battery")}
                </th>
              </tr>
            </thead>
            <tbody>
              ${i.map(e=>F`
                  <tr class="${e.is_reachable?"":"unreachable-row"}">
                    <td class="device-name" data-label=${this._l("ccu.device")}>${e.name}</td>
                    <td data-label=${this._l("ccu.model")}>${e.model}</td>
                    <td data-label=${this._l("ccu.interface")}>${e.interface_id}</td>
                    <td data-label=${this._l("ccu.reachable")}>
                      <span class="status-dot ${e.is_reachable?"online":"offline"}"></span>
                    </td>
                    <td data-label="RSSI">${e.rssi_device??"—"}</td>
                    <td data-label=${this._l("ccu.battery")}>
                      ${null===e.low_battery?"—":e.low_battery?F`<span class="warn-text">${this._l("ccu.low")}</span>`:this._l("ccu.ok")}
                    </td>
                  </tr>
                `)}
            </tbody>
          </table>
        </div>
      </ha-card>
    `}_filterFirmwareDevices(e){return e.filter(e=>{if(this._firmwareFilter){const t=this._firmwareFilter.toLowerCase();if(!e.name.toLowerCase().includes(t)&&!e.model.toLowerCase().includes(t))return!1}return!this._firmwareStateFilter||e.firmware_update_state===this._firmwareStateFilter})}_renderFirmwareCard(){if(!this._firmware)return j;const e=this._firmware.devices,t=e.length>10,i=t?this._filterFirmwareDevices(e):e,s=[...i].sort((e,t)=>{const i=this._firmwareSortColumn,s=this._compareValues(e[i],t[i]);return this._firmwareSortAsc?s:-s}),a=t&&i.length!==e.length,r=[...new Set(e.map(e=>e.firmware_update_state))].sort();return F`
      <ha-card>
        <div class="card-header">
          <span>${this._l("ccu.firmware_overview")}</span>
          ${this._firmware.summary.firmware_updatable>0?F`<span class="badge"
                >${this._firmware.summary.firmware_updatable} ${this._l("ccu.updatable")}</span
              >`:j}
        </div>
        <div class="card-content table-wrapper">
          <div class="action-bar">
            <ha-button @click=${this._handleRefreshFirmware} .disabled=${this._refreshingFirmware}>
              ${this._l(this._refreshingFirmware?"common.loading":"ccu.refresh_firmware")}
            </ha-button>
          </div>
          ${t?F`
                <div class="filter-bar">
                  <ha-input
                    .value=${this._firmwareFilter}
                    .placeholder=${this._l("ccu.filter_devices")}
                    aria-label=${this._l("ccu.filter_devices")}
                    @input=${e=>{this._firmwareFilter=e.target.value}}
                    class="filter-search"
                  ></ha-input>
                  <div class="filter-selects">
                    <ha-select
                      .label=${this._l("ccu.state")}
                      .value=${this._firmwareStateFilter}
                      .options=${[{value:"",label:this._l("ccu.filter_all")},...r.map(e=>({value:e,label:e}))]}
                      @selected=${e=>{e.stopPropagation(),this._firmwareStateFilter=e.detail.value??""}}
                      @closed=${e=>e.stopPropagation()}
                    ></ha-select>
                  </div>
                </div>
                ${a?F`<div class="filter-count">
                      ${this._l("ccu.filter_result",{count:i.length,total:e.length})}
                    </div>`:j}
              `:j}
          <table>
            <thead>
              <tr>
                <th @click=${()=>this._toggleFirmwareSort("name")}>
                  ${this._l("ccu.device")} ${this._sortIcon("firmware","name")}
                </th>
                <th @click=${()=>this._toggleFirmwareSort("model")}>
                  ${this._l("ccu.model")} ${this._sortIcon("firmware","model")}
                </th>
                <th @click=${()=>this._toggleFirmwareSort("firmware")}>
                  ${this._l("ccu.current_fw")} ${this._sortIcon("firmware","firmware")}
                </th>
                <th @click=${()=>this._toggleFirmwareSort("available_firmware")}>
                  ${this._l("ccu.available_fw")} ${this._sortIcon("firmware","available_firmware")}
                </th>
                <th @click=${()=>this._toggleFirmwareSort("firmware_update_state")}>
                  ${this._l("ccu.state")} ${this._sortIcon("firmware","firmware_update_state")}
                </th>
              </tr>
            </thead>
            <tbody>
              ${s.map(e=>F`
                  <tr class="${e.firmware_updatable?"updatable-row":""}">
                    <td class="device-name" data-label=${this._l("ccu.device")}>${e.name}</td>
                    <td data-label=${this._l("ccu.model")}>${e.model}</td>
                    <td data-label=${this._l("ccu.current_fw")}>${e.firmware}</td>
                    <td data-label=${this._l("ccu.available_fw")}>
                      ${e.available_firmware??"—"}
                    </td>
                    <td data-label=${this._l("ccu.state")}>
                      <span class="fw-state ${e.firmware_updatable?"updatable":""}">
                        ${e.firmware_update_state}
                      </span>
                    </td>
                    <td>
                      ${e.firmware_updatable?F`
                            <ha-button @click=${()=>this._handleUpdateFirmware(e)}>
                              ${this._l("ccu.update_firmware")}
                            </ha-button>
                          `:j}
                    </td>
                  </tr>
                `)}
            </tbody>
          </table>
        </div>
      </ha-card>
    `}_renderActionsCard(){return F`
      <ha-card>
        <div class="card-header">${this._l("ccu.actions")}</div>
        <div class="card-content">
          <div class="action-buttons">
            <ha-button @click=${this._fetchAll}>${this._l("ccu.refresh")}</ha-button>
            <ha-button @click=${this._handleCreateBackup} .disabled=${this._backupRunning}>
              ${this._l(this._backupRunning?"ccu.backup_running":"ccu.create_backup")}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `}_toggleSignalSort(e){this._signalSortColumn===e?this._signalSortAsc=!this._signalSortAsc:(this._signalSortColumn=e,this._signalSortAsc=!0)}_toggleFirmwareSort(e){this._firmwareSortColumn===e?this._firmwareSortAsc=!this._firmwareSortAsc:(this._firmwareSortColumn=e,this._firmwareSortAsc=!0)}_sortIcon(e,t){return("signal"===e?this._signalSortColumn:this._firmwareSortColumn)!==t?"":("signal"===e?this._signalSortAsc:this._firmwareSortAsc)?" ▲":" ▼"}_compareValues(e,t){return null==e?null==t?0:-1:null==t?1:"boolean"==typeof e&&"boolean"==typeof t?Number(e)-Number(t):"number"==typeof e&&"number"==typeof t?e-t:String(e).localeCompare(String(t))}static{this.styles=[Se,n`
      :host {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .sub-tab-bar {
        display: flex;
        gap: 4px;
        border-bottom: 2px solid var(--divider-color);
        padding-bottom: 0;
        margin-bottom: 4px;
      }

      .sub-tab {
        padding: 8px 16px;
        border: none;
        background: none;
        font-size: 14px;
        font-weight: 500;
        color: var(--secondary-text-color);
        cursor: pointer;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        transition:
          color 0.2s,
          border-color 0.2s;
        font-family: inherit;
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .sub-tab:hover {
        color: var(--primary-text-color);
      }

      .sub-tab.active {
        color: var(--primary-color);
        border-bottom-color: var(--primary-color);
      }

      .tab-badge {
        font-size: 11px;
        min-width: 18px;
        height: 18px;
        line-height: 18px;
        text-align: center;
        padding: 0 5px;
        border-radius: 9px;
        background: var(--warning-color, #ff9800);
        color: #fff;
        font-weight: 600;
      }

      .empty-hint {
        color: var(--secondary-text-color);
        font-size: 14px;
        padding: 8px 0;
      }

      ha-card {
        border-radius: var(--ha-card-border-radius, 12px);
        background: var(--ha-card-background, var(--card-background-color, #fff));
        box-shadow: var(--ha-card-box-shadow, 0 2px 6px rgba(0, 0, 0, 0.1));
        overflow: hidden;
      }

      .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .badge {
        font-size: 11px;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: 12px;
        white-space: nowrap;
        background: rgba(var(--rgb-primary-color, 3, 169, 244), 0.15);
        color: var(--primary-color);
      }

      .badge.warning {
        background: rgba(var(--rgb-amber, 255, 152, 0), 0.15);
        color: var(--warning-color, #ff9800);
      }

      .badge.error {
        background: rgba(var(--rgb-red, 244, 67, 54), 0.15);
        color: var(--error-color, #db4437);
      }

      .kv-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 12px;
      }

      .kv-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .kv-label {
        font-size: 12px;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .kv-value {
        font-size: 16px;
        font-weight: 500;
      }

      .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 16px;
      }

      .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 12px;
        border-radius: 8px;
        background: var(--secondary-background-color);
      }

      .stat-item.warning {
        background: rgba(var(--rgb-amber, 255, 152, 0), 0.1);
      }

      .stat-item.error {
        background: rgba(var(--rgb-red, 244, 67, 54), 0.1);
      }

      .stat-value {
        font-size: 28px;
        font-weight: 500;
      }

      .stat-label {
        font-size: 12px;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        margin-top: 4px;
      }

      .status-badges {
        display: flex;
        gap: 8px;
        margin-top: 12px;
        flex-wrap: wrap;
      }

      .status-badge {
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 500;
      }

      .status-badge.has-backup {
        background: rgba(var(--rgb-green, 76, 175, 80), 0.15);
        color: var(--success-color, #4caf50);
      }

      .install-mode-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 16px;
      }

      .install-mode-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 12px;
        border-radius: 8px;
        background: var(--secondary-background-color);
      }

      .install-mode-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .install-mode-label {
        font-weight: 500;
      }

      .install-mode-status {
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 8px;
        background: var(--secondary-background-color);
      }

      .install-mode-status.active {
        background: rgba(var(--rgb-green, 76, 175, 80), 0.15);
        color: var(--success-color, #4caf50);
      }

      .install-mode-remaining {
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .filter-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: end;
        margin-bottom: 12px;
      }

      .filter-search {
        flex: 1 1 200px;
        min-width: min(200px, 100%);
      }

      .filter-selects {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }

      .filter-selects ha-select {
        min-width: 140px;
      }

      .filter-count {
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-bottom: 8px;
      }

      .table-wrapper {
        overflow-x: auto;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
      }

      thead th {
        text-align: left;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 500;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid var(--divider-color);
        cursor: pointer;
        user-select: none;
        white-space: nowrap;
      }

      tbody td {
        padding: 8px 12px;
        border-bottom: 1px solid var(--divider-color);
      }

      tbody tr:last-child td {
        border-bottom: none;
      }

      tbody tr:hover {
        background: var(--secondary-background-color);
      }

      .device-name {
        font-weight: 500;
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .unreachable-row {
        opacity: 0.6;
      }

      .updatable-row {
        background: rgba(var(--rgb-blue, 33, 150, 243), 0.05);
      }

      .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }

      .status-dot.online {
        background: var(--success-color, #4caf50);
      }

      .status-dot.offline {
        background: var(--error-color, #db4437);
      }

      .warn-text {
        color: var(--warning-color, #ff9800);
      }

      .fw-state.updatable {
        color: var(--info-color, #2196f3);
        font-weight: 500;
      }

      .msg-type {
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 8px;
        white-space: nowrap;
      }

      .msg-type-0 {
        background: rgba(var(--rgb-blue, 33, 150, 243), 0.15);
        color: var(--info-color, #2196f3);
      }

      .msg-type-1 {
        background: rgba(var(--rgb-amber, 255, 152, 0), 0.15);
        color: var(--warning-color, #ff9800);
      }

      .msg-type-2 {
        background: rgba(var(--rgb-red, 244, 67, 54), 0.15);
        color: var(--error-color, #db4437);
      }

      .timestamp-cell {
        white-space: nowrap;
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .action-bar {
        margin-bottom: 12px;
      }

      .action-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      @media (max-width: 600px) {
        .sub-tab-bar {
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
          scrollbar-width: none;
        }

        .sub-tab-bar::-webkit-scrollbar {
          display: none;
        }

        .sub-tab {
          padding: 8px 10px;
          font-size: 13px;
          white-space: nowrap;
        }

        .kv-grid {
          grid-template-columns: 1fr 1fr;
        }

        .install-mode-grid {
          grid-template-columns: 1fr;
        }

        .filter-bar {
          flex-direction: column;
          gap: 8px;
        }

        .filter-search {
          min-width: 0;
          flex: 1 1 auto;
          width: 100%;
        }

        .filter-selects {
          width: 100%;
          gap: 8px;
        }

        .filter-selects ha-select {
          min-width: 0;
          flex: 1;
        }

        /* Tables as card list on mobile */
        table,
        thead,
        tbody,
        th,
        td,
        tr {
          display: block;
        }

        thead {
          display: none;
        }

        tbody tr {
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          padding: 12px;
          margin-bottom: 8px;
          background: var(--card-background-color, #fff);
        }

        tbody tr:hover {
          background: var(--secondary-background-color);
        }

        tbody td {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 4px 0;
          border-bottom: none;
          font-size: 13px;
        }

        tbody td::before {
          content: attr(data-label);
          font-weight: 500;
          font-size: 12px;
          color: var(--secondary-text-color);
          text-transform: uppercase;
          margin-right: 8px;
          flex-shrink: 0;
        }

        tbody td:empty {
          display: none;
        }

        .device-name {
          max-width: none;
          font-size: 14px;
        }

        .action-buttons {
          flex-direction: column;
        }

        .action-buttons ha-button {
          width: 100%;
        }
      }
    `]}};e([he({attribute:!1})],ui.prototype,"hass",void 0),e([he()],ui.prototype,"entryId",void 0),e([pe()],ui.prototype,"_subTab",void 0),e([pe()],ui.prototype,"_sysInfo",void 0),e([pe()],ui.prototype,"_installMode",void 0),e([pe()],ui.prototype,"_signalDevices",void 0),e([pe()],ui.prototype,"_firmware",void 0),e([pe()],ui.prototype,"_inboxDevices",void 0),e([pe()],ui.prototype,"_serviceMessages",void 0),e([pe()],ui.prototype,"_alarmMessages",void 0),e([pe()],ui.prototype,"_loading",void 0),e([pe()],ui.prototype,"_error",void 0),e([pe()],ui.prototype,"_backupRunning",void 0),e([pe()],ui.prototype,"_refreshingFirmware",void 0),e([pe()],ui.prototype,"_signalSortColumn",void 0),e([pe()],ui.prototype,"_signalSortAsc",void 0),e([pe()],ui.prototype,"_signalFilter",void 0),e([pe()],ui.prototype,"_signalInterfaceFilter",void 0),e([pe()],ui.prototype,"_signalReachableFilter",void 0),e([pe()],ui.prototype,"_signalBatteryFilter",void 0),e([pe()],ui.prototype,"_firmwareSortColumn",void 0),e([pe()],ui.prototype,"_firmwareSortAsc",void 0),e([pe()],ui.prototype,"_firmwareFilter",void 0),e([pe()],ui.prototype,"_firmwareStateFilter",void 0),ui=_i=e([we("hm-ccu-dashboard")],ui);var vi,mi=Object.freeze({__proto__:null,get HmCcuDashboard(){return ui}});let gi=class extends oe{constructor(){super(...arguments),this.entryId="",this._health=null,this._throttle=null,this._incidents=null,this._deviceStats=null,this._loading=!0,this._error=""}static{vi=this}static{this._POLL_INTERVAL_FAST=5e3}static{this._POLL_INTERVAL_SLOW=3e4}static{this._STABLE_STATES=["RUNNING","running"]}updated(e){e.has("entryId")&&this.entryId&&(this._stopPolling(),this._fetchAll())}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}_isStableState(){return null!==this._health&&vi._STABLE_STATES.includes(this._health.central_state)}_scheduleNextPoll(){this._stopPolling();const e=this._isStableState()?vi._POLL_INTERVAL_SLOW:vi._POLL_INTERVAL_FAST;this._pollTimer=setTimeout(()=>this._fetchAll(),e)}_stopPolling(){void 0!==this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchAll(){if(this.entryId){null===this._health&&(this._loading=!0),this._error="";try{const[e,t,i,s]=await Promise.all([Ue(this.hass,this.entryId),He(this.hass,this.entryId),We(this.hass,this.entryId),Fe(this.hass,this.entryId)]);this._health=e,this._throttle=t,this._incidents=i,this._deviceStats=s,this._entryEntityIds||await this._loadEntryEntityIds()}catch(e){this._error=String(e)}finally{this._loading=!1,this._scheduleNextPoll()}}}_l(e,t){return tt(this.hass,e,t)}async _handleClearIncidents(){if(await st(0,{title:this._l("integration.clear_incidents_title"),text:this._l("integration.clear_incidents_text"),confirmText:this._l("integration.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t){return e.callWS({type:"homematicip_local/integration/clear_incidents",entry_id:t})}(this.hass,this.entryId),rt(this,{message:this._l("integration.incidents_cleared")}),this._incidents=await We(this.hass,this.entryId)}catch{rt(this,{message:this._l("integration.action_failed")})}}async _handleClearCache(){if(await st(0,{title:this._l("integration.clear_cache_title"),text:this._l("integration.clear_cache_text"),confirmText:this._l("integration.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t){return e.callWS({type:"homematicip_local/integration/clear_cache",entry_id:t})}(this.hass,this.entryId),rt(this,{message:this._l("integration.cache_cleared")})}catch{rt(this,{message:this._l("integration.action_failed")})}}render(){return this.entryId?this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:this._error?F`<div class="error">${this._error}</div>`:F`
      ${this._renderHealthCard()} ${this._renderDeviceStatsCard()} ${this._renderRadioLevelsCard()}
      ${this._renderThrottleCard()} ${this._renderIncidentsCard()} ${this._renderActionsCard()}
    `:F`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}async _loadEntryEntityIds(){this._entryEntityIds=await async function(e,t){try{const i=await e.callWS({type:"config/entity_registry/list"});return new Set(i.filter(e=>e.config_entry_id===t).map(e=>e.entity_id))}catch{return}}(this.hass,this.entryId)}_renderRadioLevelsCard(){const e=function(e,t){if(!e)return[];const i=new Map;for(const[s,a]of Object.entries(e)){if(!s.startsWith("sensor."))continue;const e=s.endsWith("_duty_cycle_level"),r=s.endsWith("_carrier_sense_level");if(!e&&!r)continue;if(t&&!t.has(s))continue;const n=a.attributes,o=n?.friendly_name||s,l=s.replace(/_(?:duty_cycle|carrier_sense)_level$/,""),d=o.replace(/\s*Duty Cycle Level$/i,"").replace(/\s*Carrier Sense Level$/i,"").replace(/\s*DutyCycle Level$/i,"").replace(/\s*CarrierSense Level$/i,"");i.has(l)||i.set(l,{name:d,dutyCycle:null,carrierSense:null});const c=i.get(l),h=parseFloat(a.state);isNaN(h)||(e&&(c.dutyCycle=h),r&&(c.carrierSense=h))}return[...i.values()].sort((e,t)=>e.name.localeCompare(t.name))}(this.hass.states,this._entryEntityIds);return 0===e.length?j:F`
      <ha-card>
        <div class="card-header">${this._l("integration.radio_levels")}</div>
        <div class="card-content">
          <div class="radio-list">
            ${e.map(e=>{return F`
                <div class="radio-row">
                  <ha-icon .icon=${"mdi:radio-tower"} class="radio-icon"></ha-icon>
                  <span class="radio-name">${e.name}</span>
                  <span class="radio-values">
                    ${null!==e.dutyCycle?F`<span class="level-${t=e.dutyCycle,null===t?"":t>=80?"error":t>=60?"warning":""}"
                          >DC: ${e.dutyCycle}%</span
                        >`:j}
                    ${null!==e.dutyCycle&&null!==e.carrierSense?F` · `:j}
                    ${null!==e.carrierSense?F`<span class="level-${function(e){return null===e?"":e>=10?"error":""}(e.carrierSense)}"
                          >CS: ${e.carrierSense}%</span
                        >`:j}
                  </span>
                </div>
              `;var t})}
          </div>
        </div>
      </ha-card>
    `}_renderHealthCard(){return this._health?F`
      <ha-card>
        <div class="card-header">${this._l("integration.system_health")}</div>
        <div class="card-content">
          <div class="kv-grid">
            <div class="kv-item">
              <span class="kv-label">${this._l("integration.central_state")}</span>
              <span class="kv-value">${this._health.central_state}</span>
            </div>
            <div class="kv-item">
              <span class="kv-label">${this._l("integration.health_score")}</span>
              <span class="kv-value health-score"
                >${this._formatScore(this._health.overall_health_score)}</span
              >
            </div>
          </div>
        </div>
      </ha-card>
    `:j}_renderDeviceStatsCard(){if(!this._deviceStats)return j;const e=this._deviceStats;return F`
      <ha-card>
        <div class="card-header">${this._l("integration.device_statistics")}</div>
        <div class="card-content">
          <div class="stat-grid">
            <div class="stat-item">
              <span class="stat-value">${e.total_devices}</span>
              <span class="stat-label">${this._l("integration.total_devices")}</span>
            </div>
            <div class="stat-item ${e.unreachable_devices>0?"warning":""}">
              <span class="stat-value">${e.unreachable_devices}</span>
              <span class="stat-label">${this._l("integration.unreachable")}</span>
            </div>
            <div class="stat-item ${e.firmware_updatable_devices>0?"info":""}">
              <span class="stat-value">${e.firmware_updatable_devices}</span>
              <span class="stat-label">${this._l("integration.firmware_updatable")}</span>
            </div>
          </div>
          ${Object.keys(e.by_interface).length>1?F`
                <div class="interface-breakdown">
                  ${Object.entries(e.by_interface).map(([e,t])=>F`
                      <div class="interface-row">
                        <span class="interface-name">${e}</span>
                        <span class="interface-stats">
                          ${t.total} ${this._l("integration.total_short")}
                          ${t.unreachable>0?F`,
                                <span class="warn-text"
                                  >${t.unreachable}
                                  ${this._l("integration.unreachable_short")}</span
                                >`:j}
                        </span>
                      </div>
                    `)}
                </div>
              `:j}
        </div>
      </ha-card>
    `}_renderThrottleCard(){return this._throttle&&0!==Object.keys(this._throttle).length?F`
      <ha-card>
        <div class="card-header">${this._l("integration.command_throttle")}</div>
        <div class="card-content">
          ${Object.entries(this._throttle).map(([e,t])=>F`
              <div class="throttle-section">
                <div class="throttle-interface">${e}</div>
                <div class="kv-grid">
                  <div class="kv-item">
                    <span class="kv-label">${this._l("integration.enabled")}</span>
                    <span class="kv-value"
                      >${this._l(t.is_enabled?"common.yes":"common.no")}</span
                    >
                  </div>
                  <div class="kv-item">
                    <span class="kv-label">${this._l("integration.interval")}</span>
                    <span class="kv-value">${t.interval}s</span>
                  </div>
                  <div class="kv-item">
                    <span class="kv-label">${this._l("integration.queue_size")}</span>
                    <span class="kv-value">${t.queue_size}</span>
                  </div>
                  <div class="kv-item">
                    <span class="kv-label">${this._l("integration.throttled")}</span>
                    <span class="kv-value">${t.throttled_count}</span>
                  </div>
                  <div class="kv-item">
                    <span class="kv-label">${this._l("integration.burst_count")}</span>
                    <span class="kv-value">${t.burst_count}</span>
                  </div>
                </div>
              </div>
            `)}
        </div>
      </ha-card>
    `:j}_renderIncidentsCard(){if(!this._incidents)return j;const{incidents:e,summary:t}=this._incidents;return F`
      <ha-card>
        <div class="card-header">
          <span>${this._l("integration.incidents")}</span>
          <span class="badge">${t.total_incidents}</span>
        </div>
        <div class="card-content">
          ${0===e.length?F`<div class="empty-state">${this._l("integration.no_incidents")}</div>`:F`
                <div class="incident-list">
                  ${e.map(e=>F`
                      <div class="incident-row severity-${e.severity??"info"}">
                        <span class="incident-type">${e.type}</span>
                        <span class="incident-message">${e.message}</span>
                        <span class="incident-time"
                          >${this._formatTimestamp(String(e.timestamp??""))}</span
                        >
                      </div>
                    `)}
                </div>
              `}
          ${e.length>0?F`
                <div class="action-bar">
                  <ha-button class="destructive" @click=${this._handleClearIncidents}>
                    ${this._l("integration.clear_incidents")}
                  </ha-button>
                </div>
              `:j}
        </div>
      </ha-card>
    `}_renderActionsCard(){return F`
      <ha-card>
        <div class="card-header">${this._l("integration.actions")}</div>
        <div class="card-content">
          <div class="action-buttons">
            <ha-button @click=${this._fetchAll}>${this._l("integration.refresh")}</ha-button>
            <ha-button class="destructive" @click=${this._handleClearCache}>
              ${this._l("integration.clear_cache")}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `}_formatScore(e){return`${Math.round(e<=1?100*e:e)}%`}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleString(this.hass.config.language||"en")}catch{return e}}static{this.styles=[Se,n`
      :host {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      ha-card {
        border-radius: var(--ha-card-border-radius, 12px);
        background: var(--ha-card-background, var(--card-background-color, #fff));
        box-shadow: var(--ha-card-box-shadow, 0 2px 6px rgba(0, 0, 0, 0.1));
        overflow: hidden;
      }

      .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .badge {
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 12px;
        background: var(--primary-color);
        color: #fff;
      }

      .kv-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 12px;
      }

      .kv-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .kv-label {
        font-size: 12px;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .kv-value {
        font-size: 16px;
        font-weight: 500;
      }

      .health-score {
        color: var(--success-color, #4caf50);
      }

      .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 16px;
        margin-bottom: 16px;
      }

      .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 12px;
        border-radius: 8px;
        background: var(--secondary-background-color);
      }

      .stat-item.warning {
        background: rgba(var(--rgb-amber, 255, 152, 0), 0.1);
      }

      .stat-item.info {
        background: rgba(var(--rgb-blue, 33, 150, 243), 0.1);
      }

      .stat-value {
        font-size: 28px;
        font-weight: 500;
      }

      .stat-label {
        font-size: 12px;
        color: var(--secondary-text-color);
        text-transform: uppercase;
        margin-top: 4px;
      }

      .interface-breakdown {
        border-top: 1px solid var(--divider-color);
        padding-top: 12px;
      }

      .interface-row {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;
        font-size: 13px;
      }

      .interface-name {
        font-weight: 500;
      }

      .warn-text {
        color: var(--warning-color, #ff9800);
      }

      .throttle-section {
        margin-bottom: 16px;
      }

      .throttle-section:last-child {
        margin-bottom: 0;
      }

      .throttle-interface {
        font-weight: 500;
        font-size: 14px;
        margin-bottom: 8px;
        padding-bottom: 4px;
        border-bottom: 1px solid var(--divider-color);
      }

      .incident-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 400px;
        overflow-y: auto;
      }

      .incident-row {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 12px;
        align-items: center;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 13px;
        background: var(--secondary-background-color);
      }

      .incident-row.severity-error {
        border-left: 3px solid var(--error-color, #db4437);
      }

      .incident-row.severity-warning {
        border-left: 3px solid var(--warning-color, #ff9800);
      }

      .incident-row.severity-info {
        border-left: 3px solid var(--info-color, #2196f3);
      }

      .incident-type {
        font-weight: 500;
        white-space: nowrap;
      }

      .incident-message {
        color: var(--secondary-text-color);
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .incident-time {
        font-size: 11px;
        color: var(--secondary-text-color);
        white-space: nowrap;
      }

      .radio-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .radio-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        border-radius: 6px;
        background: var(--secondary-background-color);
        font-size: 14px;
      }

      .radio-icon {
        color: var(--secondary-text-color);
        --ha-icon-display-size: 20px;
        flex-shrink: 0;
      }

      .radio-name {
        flex: 1;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .radio-values {
        flex-shrink: 0;
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .level-warning {
        color: var(--warning-color, #ff9800);
        font-weight: 500;
      }

      .level-error {
        color: var(--error-color, #db4437);
        font-weight: 500;
      }

      .action-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      .destructive {
        --ha-button-color: var(--error-color, #db4437);
      }

      @media (max-width: 600px) {
        .stat-grid {
          grid-template-columns: repeat(3, 1fr);
        }

        .incident-row {
          grid-template-columns: 1fr;
          gap: 4px;
        }

        .kv-grid {
          grid-template-columns: 1fr 1fr;
        }
      }
    `]}};e([he({attribute:!1})],gi.prototype,"hass",void 0),e([he()],gi.prototype,"entryId",void 0),e([pe()],gi.prototype,"_health",void 0),e([pe()],gi.prototype,"_throttle",void 0),e([pe()],gi.prototype,"_incidents",void 0),e([pe()],gi.prototype,"_deviceStats",void 0),e([pe()],gi.prototype,"_loading",void 0),e([pe()],gi.prototype,"_error",void 0),e([pe()],gi.prototype,"_entryEntityIds",void 0),gi=vi=e([we("hm-integration-dashboard")],gi);var fi=Object.freeze({__proto__:null,get HmIntegrationDashboard(){return gi}});let bi=class extends oe{constructor(){super(...arguments),this.entryId="",this.filterDevice="",this.editable=!0,this._entries=[],this._total=0,this._loading=!0,this._error="",this._expandedEntries=new Set,this._schemaCache=new Map,this._schemaLoading=new Set}updated(e){(e.has("entryId")||e.has("filterDevice"))&&this.entryId&&this._fetchHistory()}async _fetchHistory(){this._loading=!0,this._error="";try{const e=await async function(e,t,i="",s=50){return e.callWS({type:"homematicip_local/config/get_change_history",entry_id:t,channel_address:i,limit:s})}(this.hass,this.entryId,this.filterDevice);this._entries=e.entries,this._total=e.total}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return tt(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_getSchemaCacheKey(e){return`${e.interface_id}|${e.channel_address}|${e.paramset_key}`}async _ensureSchema(e){const t=this._getSchemaCacheKey(e);if(!this._schemaCache.has(t)&&!this._schemaLoading.has(t)){this._schemaLoading.add(t);try{const i=await Ie(this.hass,e.entry_id,e.interface_id,e.channel_address,"",e.paramset_key);this._schemaCache.set(t,i)}catch{this._schemaCache.set(t,null)}finally{this._schemaLoading.delete(t),this.requestUpdate()}}}_findParam(e,t){const i=this._schemaCache.get(this._getSchemaCacheKey(e));if(i)for(const e of i.sections){const i=e.parameters.find(e=>e.id===t);if(i)return i}}_formatValue(e,t,i){const s=this._findParam(e,t);return s?dt(this.hass,s,i):String(i??"")}_getParamLabel(e,t){const i=this._findParam(e,t);return i?.label??t}_toggleEntry(e,t){const i=new Set(this._expandedEntries);i.has(e)?i.delete(e):(i.add(e),t&&this._ensureSchema(t)),this._expandedEntries=i}async _handleClear(){if(await st(0,{title:this._l("change_history.clear_confirm_title"),text:this._l("change_history.clear_confirm_text"),confirmText:this._l("change_history.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{const e=await async function(e,t){return e.callWS({type:"homematicip_local/config/clear_change_history",entry_id:t})}(this.hass,this.entryId);e.success&&(rt(this,{message:this._l("change_history.clear_success",{count:e.cleared})}),this._entries=[],this._total=0)}catch{rt(this,{message:this._l("change_history.clear_failed")})}}_formatTimestamp(e){try{return new Date(e).toLocaleString(this.hass.config.language||"en")}catch{return e}}_getSourceLabel(e){switch(e){case"manual":return this._l("change_history.source_manual");case"import":return this._l("change_history.source_import");case"copy":return this._l("change_history.source_copy");default:return e}}_getSourceBadgeHint(e){switch(e){case"manual":return this._l("change_history.source_manual_hint");case"import":return this._l("change_history.source_import_hint");case"copy":return this._l("change_history.source_copy_hint");default:return""}}render(){return F`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="history-header-bar">
        <h2>${this._l("change_history.title")}</h2>
      </div>

      ${this._loading?F`<div class="loading">${this._l("common.loading")}</div>`:this._error?F`<div class="error">
              ${this._error}
              <br />
              <ha-button outlined @click=${this._fetchHistory}>
                ${this._l("common.retry")}
              </ha-button>
            </div>`:0===this._entries.length?F`<div class="empty-state">
                <ha-icon class="empty-icon" .icon=${"mdi:history"}></ha-icon>
                <div class="empty-message">${this._l("change_history.empty")}</div>
              </div>`:this._renderEntries()}
      ${!this._loading&&this._entries.length>0&&this.editable?F`
            <div class="action-bar">
              <ha-button class="destructive" @click=${this._handleClear}>
                ${this._l("change_history.clear")}
              </ha-button>
            </div>
          `:j}
    `}_renderEntries(){return F`
      <div class="history-list">
        ${this._entries.map((e,t)=>{const i=`${e.timestamp}-${t}`,s=this._expandedEntries.has(i),a=Object.keys(e.changes).length;return F`
            <div class="history-entry">
              <div
                class="history-entry-header"
                role="button"
                tabindex="0"
                aria-expanded=${s}
                @click=${()=>this._toggleEntry(i,e)}
                @keydown=${t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._toggleEntry(i,e))}}
              >
                <div class="history-entry-info">
                  <div class="history-entry-time">${this._formatTimestamp(e.timestamp)}</div>
                  <div class="history-entry-device">
                    ${e.device_name} (${e.device_model}) — ${e.channel_address}
                  </div>
                  <div class="history-entry-meta">
                    ${this._l("change_history.parameters_changed",{count:a})}
                  </div>
                </div>
                <div class="history-entry-badges">
                  <span class="source-badge" title="${this._getSourceBadgeHint(e.source)}"
                    >${this._getSourceLabel(e.source)}</span
                  >
                  <ha-icon
                    class="expand-icon"
                    .icon=${s?"mdi:chevron-down":"mdi:chevron-right"}
                  ></ha-icon>
                </div>
              </div>
              ${s?F`
                    <div class="history-details">
                      ${Object.entries(e.changes).map(([t,i])=>F`
                          <div class="change-row">
                            <span class="change-param">${this._getParamLabel(e,t)}</span>
                            <span class="change-values">
                              <span class="change-old"
                                >${this._formatValue(e,t,i.old)}</span
                              >
                              <ha-icon class="change-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
                              <span class="change-new"
                                >${this._formatValue(e,t,i.new)}</span
                              >
                            </span>
                          </div>
                        `)}
                    </div>
                  `:j}
            </div>
          `})}
      </div>
    `}static{this.styles=[Se,n`
      .history-header-bar {
        margin-bottom: 16px;
      }

      .history-header-bar h2 {
        margin: 8px 0;
        font-size: 20px;
        font-weight: 400;
      }

      .history-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .history-entry {
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        overflow: hidden;
      }

      .history-entry-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: var(--secondary-background-color, #fafafa);
        cursor: pointer;
      }

      .history-entry-header:hover,
      .history-entry-header:focus-visible {
        background: var(--primary-background-color);
      }

      .history-entry-header:focus-visible {
        outline: 2px solid var(--primary-color, #03a9f4);
        outline-offset: -2px;
      }

      .history-entry-info {
        flex: 1;
        min-width: 0;
      }

      .history-entry-time {
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .history-entry-device {
        font-size: 14px;
        font-weight: 500;
        margin-top: 2px;
      }

      .history-entry-meta {
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 2px;
      }

      .history-entry-badges {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-left: 12px;
        flex-shrink: 0;
      }

      .source-badge {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 12px;
        background: var(--primary-color, #03a9f4);
        color: #fff;
        text-transform: uppercase;
      }

      .expand-icon {
        --ha-icon-display-size: 18px;
        color: var(--secondary-text-color);
      }

      .history-details {
        padding: 8px 16px 12px;
        border-top: 1px solid var(--divider-color, #e0e0e0);
        animation: slideDown 0.15s ease-out;
      }

      @keyframes slideDown {
        from {
          opacity: 0;
          max-height: 0;
        }
        to {
          opacity: 1;
          max-height: 500px;
        }
      }

      .change-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        font-size: 13px;
      }

      .change-param {
        font-weight: 500;
        margin-right: 12px;
      }

      .change-values {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .change-old {
        color: var(--error-color, #db4437);
        text-decoration: line-through;
        opacity: 0.8;
        font-size: 12px;
      }

      .change-new {
        color: var(--success-color, #4caf50);
        font-weight: 600;
      }

      .empty-icon {
        --ha-icon-display-size: 48px;
        color: var(--secondary-text-color);
        opacity: 0.5;
        margin-bottom: 12px;
      }

      .empty-message {
        font-size: 16px;
      }

      .destructive {
        --ha-button-color: var(--error-color, #db4437);
      }

      .change-arrow {
        --ha-icon-display-size: 18px;
        color: var(--secondary-text-color);
      }

      @media (max-width: 600px) {
        .history-entry-header {
          flex-direction: column;
          align-items: flex-start;
          gap: 8px;
        }

        .history-entry-badges {
          margin-left: 0;
        }

        .change-row {
          flex-direction: column;
          align-items: flex-start;
          gap: 2px;
        }
      }
    `]}};e([he({attribute:!1})],bi.prototype,"hass",void 0),e([he()],bi.prototype,"entryId",void 0),e([he()],bi.prototype,"filterDevice",void 0),e([he({type:Boolean})],bi.prototype,"editable",void 0),e([pe()],bi.prototype,"_entries",void 0),e([pe()],bi.prototype,"_total",void 0),e([pe()],bi.prototype,"_loading",void 0),e([pe()],bi.prototype,"_error",void 0),e([pe()],bi.prototype,"_expandedEntries",void 0),bi=e([we("hm-change-history")],bi);var yi=Object.freeze({__proto__:null,get HmChangeHistory(){return bi}});export{pi as HomematicConfigPanel};
