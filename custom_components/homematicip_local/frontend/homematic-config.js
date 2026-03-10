function e(e,t,i,s){var a,n=arguments.length,r=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(r=(n<3?a(r):n>3?a(t,i,r):a(t,i))||r);return n>3&&r&&Object.defineProperty(t,i,r),r}"function"==typeof SuppressedError&&SuppressedError;const t=globalThis,i=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),a=new WeakMap;let n=class{constructor(e,t,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(i&&void 0===e){const i=void 0!==t&&1===t.length;i&&(e=a.get(t)),void 0===e&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),i&&a.set(t,e))}return e}toString(){return this.cssText}};const r=(e,...t)=>{const i=1===e.length?e[0]:t.reduce((t,i,s)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[s+1],e[0]);return new n(i,e,s)},o=i?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>new n("string"==typeof e?e:e+"",void 0,s))(t)})(e):e,{is:d,defineProperty:l,getOwnPropertyDescriptor:c,getOwnPropertyNames:h,getOwnPropertySymbols:p,getPrototypeOf:_}=Object,u=globalThis,v=u.trustedTypes,m=v?v.emptyScript:"",g=u.reactiveElementPolyfillSupport,f=(e,t)=>e,y={toAttribute(e,t){switch(t){case Boolean:e=e?m:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},b=(e,t)=>!d(e,t),x={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:b};Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;let $=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=x){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(e,i,t);void 0!==s&&l(this.prototype,e,s)}}static getPropertyDescriptor(e,t,i){const{get:s,set:a}=c(this.prototype,e)??{get(){return this[t]},set(e){this[t]=e}};return{get:s,set(t){const n=s?.call(this);a?.call(this,t),this.requestUpdate(e,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??x}static _$Ei(){if(this.hasOwnProperty(f("elementProperties")))return;const e=_(this);e.finalize(),void 0!==e.l&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(f("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(f("properties"))){const e=this.properties,t=[...h(e),...p(e)];for(const i of t)this.createProperty(i,e[i])}const e=this[Symbol.metadata];if(null!==e){const t=litPropertyMetadata.get(e);if(void 0!==t)for(const[e,i]of t)this.elementProperties.set(e,i)}this._$Eh=new Map;for(const[e,t]of this.elementProperties){const i=this._$Eu(e,t);void 0!==i&&this._$Eh.set(i,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(o(e))}else void 0!==e&&t.push(o(e));return t}static _$Eu(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),void 0!==this.renderRoot&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){const e=new Map,t=this.constructor.elementProperties;for(const i of t.keys())this.hasOwnProperty(i)&&(e.set(i,this[i]),delete this[i]);e.size>0&&(this._$Ep=e)}createRenderRoot(){const e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((e,s)=>{if(i)e.adoptedStyleSheets=s.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const i of s){const s=document.createElement("style"),a=t.litNonce;void 0!==a&&s.setAttribute("nonce",a),s.textContent=i.cssText,e.appendChild(s)}})(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,i){this._$AK(e,i)}_$ET(e,t){const i=this.constructor.elementProperties.get(e),s=this.constructor._$Eu(e,i);if(void 0!==s&&!0===i.reflect){const a=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(t,i.type);this._$Em=e,null==a?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(e,t){const i=this.constructor,s=i._$Eh.get(e);if(void 0!==s&&this._$Em!==s){const e=i.getPropertyOptions(s),a="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==e.converter?.fromAttribute?e.converter:y;this._$Em=s;const n=a.fromAttribute(t,e.type);this[s]=n??this._$Ej?.get(s)??n,this._$Em=null}}requestUpdate(e,t,i,s=!1,a){if(void 0!==e){const n=this.constructor;if(!1===s&&(a=this[e]),i??=n.getPropertyOptions(e),!((i.hasChanged??b)(a,t)||i.useDefault&&i.reflect&&a===this._$Ej?.get(e)&&!this.hasAttribute(n._$Eu(e,i))))return;this.C(e,t,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(e,t,{useDefault:i,reflect:s,wrapped:a},n){i&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,n??t??this[e]),!0!==a||void 0!==n)||(this._$AL.has(e)||(this.hasUpdated||i||(t=void 0),this._$AL.set(e,t)),!0===s&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[e,t]of this._$Ep)this[e]=t;this._$Ep=void 0}const e=this.constructor.elementProperties;if(e.size>0)for(const[t,i]of e){const{wrapped:e}=i,s=this[t];!0!==e||this._$AL.has(t)||void 0===s||this.C(t,void 0,i,s)}}let e=!1;const t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(e=>e.hostUpdate?.()),this.update(t)):this._$EM()}catch(t){throw e=!1,this._$EM(),t}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(e){}firstUpdated(e){}};$.elementStyles=[],$.shadowRootOptions={mode:"open"},$[f("elementProperties")]=new Map,$[f("finalized")]=new Map,g?.({ReactiveElement:$}),(u.reactiveElementVersions??=[]).push("2.1.2");const k=globalThis,w=e=>e,S=k.trustedTypes,C=S?S.createPolicy("lit-html",{createHTML:e=>e}):void 0,E="$lit$",A=`lit$${Math.random().toFixed(9).slice(2)}$`,I="?"+A,D=`<${I}>`,T=document,M=()=>T.createComment(""),P=e=>null===e||"object"!=typeof e&&"function"!=typeof e,L=Array.isArray,z="[ \t\n\f\r]",N=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,R=/-->/g,B=/>/g,U=RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),V=/'/g,O=/"/g,H=/^(?:script|style|textarea|title)$/i,W=(e,...t)=>({_$litType$:1,strings:e,values:t}),F=Symbol.for("lit-noChange"),j=Symbol.for("lit-nothing"),K=new WeakMap,Y=T.createTreeWalker(T,129);function Z(e,t){if(!L(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==C?C.createHTML(t):t}class G{constructor({strings:e,_$litType$:t},i){let s;this.parts=[];let a=0,n=0;const r=e.length-1,o=this.parts,[d,l]=((e,t)=>{const i=e.length-1,s=[];let a,n=2===t?"<svg>":3===t?"<math>":"",r=N;for(let t=0;t<i;t++){const i=e[t];let o,d,l=-1,c=0;for(;c<i.length&&(r.lastIndex=c,d=r.exec(i),null!==d);)c=r.lastIndex,r===N?"!--"===d[1]?r=R:void 0!==d[1]?r=B:void 0!==d[2]?(H.test(d[2])&&(a=RegExp("</"+d[2],"g")),r=U):void 0!==d[3]&&(r=U):r===U?">"===d[0]?(r=a??N,l=-1):void 0===d[1]?l=-2:(l=r.lastIndex-d[2].length,o=d[1],r=void 0===d[3]?U:'"'===d[3]?O:V):r===O||r===V?r=U:r===R||r===B?r=N:(r=U,a=void 0);const h=r===U&&e[t+1].startsWith("/>")?" ":"";n+=r===N?i+D:l>=0?(s.push(o),i.slice(0,l)+E+i.slice(l)+A+h):i+A+(-2===l?t:h)}return[Z(e,n+(e[i]||"<?>")+(2===t?"</svg>":3===t?"</math>":"")),s]})(e,t);if(this.el=G.createElement(d,i),Y.currentNode=this.el.content,2===t||3===t){const e=this.el.content.firstChild;e.replaceWith(...e.childNodes)}for(;null!==(s=Y.nextNode())&&o.length<r;){if(1===s.nodeType){if(s.hasAttributes())for(const e of s.getAttributeNames())if(e.endsWith(E)){const t=l[n++],i=s.getAttribute(e).split(A),r=/([.?@])?(.*)/.exec(t);o.push({type:1,index:a,name:r[2],strings:i,ctor:"."===r[1]?ee:"?"===r[1]?te:"@"===r[1]?ie:X}),s.removeAttribute(e)}else e.startsWith(A)&&(o.push({type:6,index:a}),s.removeAttribute(e));if(H.test(s.tagName)){const e=s.textContent.split(A),t=e.length-1;if(t>0){s.textContent=S?S.emptyScript:"";for(let i=0;i<t;i++)s.append(e[i],M()),Y.nextNode(),o.push({type:2,index:++a});s.append(e[t],M())}}}else if(8===s.nodeType)if(s.data===I)o.push({type:2,index:a});else{let e=-1;for(;-1!==(e=s.data.indexOf(A,e+1));)o.push({type:7,index:a}),e+=A.length-1}a++}}static createElement(e,t){const i=T.createElement("template");return i.innerHTML=e,i}}function q(e,t,i=e,s){if(t===F)return t;let a=void 0!==s?i._$Co?.[s]:i._$Cl;const n=P(t)?void 0:t._$litDirective$;return a?.constructor!==n&&(a?._$AO?.(!1),void 0===n?a=void 0:(a=new n(e),a._$AT(e,i,s)),void 0!==s?(i._$Co??=[])[s]=a:i._$Cl=a),void 0!==a&&(t=q(e,a._$AS(e,t.values),a,s)),t}class Q{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){const{el:{content:t},parts:i}=this._$AD,s=(e?.creationScope??T).importNode(t,!0);Y.currentNode=s;let a=Y.nextNode(),n=0,r=0,o=i[0];for(;void 0!==o;){if(n===o.index){let t;2===o.type?t=new J(a,a.nextSibling,this,e):1===o.type?t=new o.ctor(a,o.name,o.strings,this,e):6===o.type&&(t=new se(a,this,e)),this._$AV.push(t),o=i[++r]}n!==o?.index&&(a=Y.nextNode(),n++)}return Y.currentNode=T,s}p(e){let t=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(e,i,t),t+=i.strings.length-2):i._$AI(e[t])),t++}}class J{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,i,s){this.type=2,this._$AH=j,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e?.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=q(this,e,t),P(e)?e===j||null==e||""===e?(this._$AH!==j&&this._$AR(),this._$AH=j):e!==this._$AH&&e!==F&&this._(e):void 0!==e._$litType$?this.$(e):void 0!==e.nodeType?this.T(e):(e=>L(e)||"function"==typeof e?.[Symbol.iterator])(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==j&&P(this._$AH)?this._$AA.nextSibling.data=e:this.T(T.createTextNode(e)),this._$AH=e}$(e){const{values:t,_$litType$:i}=e,s="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=G.createElement(Z(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(t);else{const e=new Q(s,this),i=e.u(this.options);e.p(t),this.T(i),this._$AH=e}}_$AC(e){let t=K.get(e.strings);return void 0===t&&K.set(e.strings,t=new G(e)),t}k(e){L(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let i,s=0;for(const a of e)s===t.length?t.push(i=new J(this.O(M()),this.O(M()),this,this.options)):i=t[s],i._$AI(a),s++;s<t.length&&(this._$AR(i&&i._$AB.nextSibling,s),t.length=s)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){const t=w(e).nextSibling;w(e).remove(),e=t}}setConnected(e){void 0===this._$AM&&(this._$Cv=e,this._$AP?.(e))}}class X{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,i,s,a){this.type=1,this._$AH=j,this._$AN=void 0,this.element=e,this.name=t,this._$AM=s,this.options=a,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=j}_$AI(e,t=this,i,s){const a=this.strings;let n=!1;if(void 0===a)e=q(this,e,t,0),n=!P(e)||e!==this._$AH&&e!==F,n&&(this._$AH=e);else{const s=e;let r,o;for(e=a[0],r=0;r<a.length-1;r++)o=q(this,s[i+r],t,r),o===F&&(o=this._$AH[r]),n||=!P(o)||o!==this._$AH[r],o===j?e=j:e!==j&&(e+=(o??"")+a[r+1]),this._$AH[r]=o}n&&!s&&this.j(e)}j(e){e===j?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}}class ee extends X{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===j?void 0:e}}class te extends X{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==j)}}class ie extends X{constructor(e,t,i,s,a){super(e,t,i,s,a),this.type=5}_$AI(e,t=this){if((e=q(this,e,t,0)??j)===F)return;const i=this._$AH,s=e===j&&i!==j||e.capture!==i.capture||e.once!==i.once||e.passive!==i.passive,a=e!==j&&(i===j||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}}class se{constructor(e,t,i){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(e){q(this,e)}}const ae={I:J},ne=k.litHtmlPolyfillSupport;ne?.(G,J),(k.litHtmlVersions??=[]).push("3.3.2");const re=globalThis;let oe=class extends ${constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,i)=>{const s=i?.renderBefore??t;let a=s._$litPart$;if(void 0===a){const e=i?.renderBefore??null;s._$litPart$=a=new J(t.insertBefore(M(),e),e,void 0,i??{})}return a._$AI(e),a})(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return F}};oe._$litElement$=!0,oe.finalized=!0,re.litElementHydrateSupport?.({LitElement:oe});const de=re.litElementPolyfillSupport;de?.({LitElement:oe}),(re.litElementVersions??=[]).push("4.2.2");const le={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:b},ce=(e=le,t,i)=>{const{kind:s,metadata:a}=i;let n=globalThis.litPropertyMetadata.get(a);if(void 0===n&&globalThis.litPropertyMetadata.set(a,n=new Map),"setter"===s&&((e=Object.create(e)).wrapped=!0),n.set(i.name,e),"accessor"===s){const{name:s}=i;return{set(i){const a=t.get.call(this);t.set.call(this,i),this.requestUpdate(s,a,e,!0,i)},init(t){return void 0!==t&&this.C(s,void 0,e,t),t}}}if("setter"===s){const{name:s}=i;return function(i){const a=this[s];t.call(this,i),this.requestUpdate(s,a,e,!0,i)}}throw Error("Unsupported decorator location: "+s)};function he(e){return(t,i)=>"object"==typeof i?ce(e,t,i):((e,t,i)=>{const s=t.hasOwnProperty(i);return t.constructor.createProperty(i,e),s?Object.getOwnPropertyDescriptor(t,i):void 0})(e,t,i)}function pe(e){return he({...e,state:!0,attribute:!1})}function _e(e){return t=>(customElements.get(e)||customElements.define(e,t),t)}const ue=r`
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
    --mdc-icon-button-size: 48px;
    --mdc-icon-size: 24px;
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
    max-width: 200px;
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

  /* ---- Responsive: mobile (< 600px) ---- */
  @media (max-width: 600px) {
    .parameter-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 6px;
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
  }
`,ve=new Set(["BidCos-RF","BidCos-Wired","HmIP-RF"]);function me(e,t){return`/api/homematicip_local/${e}/device_icon/${t}`}async function ge(e,t){return(await e.callWS({type:"homematicip_local/config/list_devices",entry_id:t})).devices}async function fe(e,t,i,s,a="",n="MASTER"){return e.callWS({type:"homematicip_local/config/get_form_schema",entry_id:t,interface_id:i,channel_address:s,channel_type:a,paramset_key:n})}async function ye(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/session_open",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}async function be(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_discard",entry_id:t,channel_address:i,paramset_key:s})}async function xe(e,t,i,s,a){return e.callWS({type:"homematicip_local/config/get_link_form_schema",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a})}async function $e(e,t,i,s,a,n){return e.callWS({type:"homematicip_local/config/put_link_paramset",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a,values:n})}async function ke(e,t){return(await e.callWS({type:"homematicip_local/config/list_schedule_devices",entry_id:t})).devices}async function we(e,t,i,s){return e.callWS({type:"homematicip_local/config/get_climate_schedule",entry_id:t,device_address:i,...s&&{profile:s}})}async function Se(e,t,i,s,a,n,r){return e.callWS({type:"homematicip_local/config/set_climate_schedule_weekday",entry_id:t,device_address:i,profile:s,weekday:a,base_temperature:n,simple_weekday_list:r})}async function Ce(e,t,i,s){return e.callWS({type:"homematicip_local/config/set_device_schedule",entry_id:t,device_address:i,schedule_data:s})}async function Ee(e,t,i,s,a){try{return await e.callWS({type:"homematicip_local/config/get_link_profiles",entry_id:t,interface_id:i,sender_channel_address:s,receiver_channel_address:a})}catch{return null}}const Ae={en:{common:{back:"Back",loading:"Loading...",save:"Save",cancel:"Cancel",yes:"Yes",no:"No"},device_list:{title:"Homematic Device Configuration",select_ccu:"CCU",select_placeholder:"Select a CCU...",search_placeholder:"Search devices...",no_entry_selected:"Please select a CCU to view devices.",no_devices:"No configurable devices found.",channels:"channels",unreachable:"Unreachable",reachable:"Reachable",low_battery:"Low battery",config_pending:"Configuration pending"},device_detail:{address:"Address",firmware:"Firmware",channel:"Channel",configure_master:"Configure MASTER",no_master_config:"No MASTER configuration available.",not_found:"Device not found.",yes:"Yes",no:"No",reachable:"Reachable",unreachable:"Unreachable",export:"Export",import:"Import",export_success:"Configuration exported successfully.",export_failed:"Failed to export configuration.",import_confirm_title:"Import Configuration",import_confirm_text:"Import and apply configuration to channel {channel}?",import_success:"Configuration imported successfully.",import_failed:"Failed to import configuration.",import_validation_failed:"Import validation failed.",show_history:"Change History",show_links:"Direct Links",show_schedules:"Schedules",rssi_device:"RSSI Device",rssi_peer:"RSSI Peer",dutycycle:"Duty Cycle",low_bat:"Low Battery",unreach:"Reachability",config_pending_label:"Config Pending"},form_parameter:{toggle_on:"On",toggle_off:"Off",custom_value:"Custom value"},time_selector:{base:"Base",factor:"Factor"},channel_config:{save:"Save",saving:"Saving...",discard:"Discard Changes",reset_defaults:"Reset to Defaults",confirm_save_title:"Save Changes",confirm_save_text:"Apply {count} change(s) to the device?",unsaved_title:"Unsaved Changes",unsaved_warning:"You have unsaved changes. Discard them and go back?",save_success:"Changes saved successfully.",save_failed:"Failed to save changes.",validation_failed:"Validation failed. Please check the highlighted fields.",undo:"Undo",redo:"Redo"},change_history:{title:"Change History",empty:"No configuration changes recorded.",clear:"Clear History",clear_confirm_title:"Clear History",clear_confirm_text:"Delete all history entries? This cannot be undone.",clear_success:"History cleared ({count} entries removed).",source_manual:"Manual",source_import:"Import",source_copy:"Copy",parameters_changed:"{count} parameter(s) changed"},device_links:{title:"Direct Links",subtitle:"Direct links for {device}",empty:"No direct links configured.",add_link:"New Link",outgoing:"Outgoing",incoming:"Incoming",configure:"Configure",delete:"Delete",delete_confirm_title:"Delete Link",delete_confirm_text:"Remove the direct link from {sender} to {receiver}? The devices will no longer communicate directly.",delete_success:"Link deleted successfully.",delete_failed:"Failed to delete link.",channel_group:"Channel {channel}"},link_config:{title:"Link Configuration",sender:"Sender",receiver:"Receiver",save_success:"Link configuration saved.",save_failed:"Failed to save link configuration.",discard:"Discard Changes",confirm_save_title:"Save Link Changes",confirm_save_text:"Apply {count} change(s) to this link?",unsaved_title:"Unsaved Changes",unsaved_warning:"You have unsaved changes. Discard them and go back?",receiver_params:"Receiver Parameters",sender_params:"Sender Parameters",no_params:"No configurable parameters for this link.",profile:"Profile",short_keypress:"Short keypress",long_keypress:"Long keypress",last_value:"Last value",custom_time:"Custom"},device_schedule:{title:"Schedules",subtitle:"Schedules for {device}",select_device:"Select a device...",no_devices:"No devices with schedule support found.",schedule_type_climate:"Climate",schedule_type_default:"Device",profile:"Profile",active_profile:"Active profile",weekdays:"Mon,Tue,Wed,Thu,Fri,Sat,Sun",weekday_monday:"Monday",weekday_tuesday:"Tuesday",weekday_wednesday:"Wednesday",weekday_thursday:"Thursday",weekday_friday:"Friday",weekday_saturday:"Saturday",weekday_sunday:"Sunday",base_temperature:"Base temperature",temperature:"Temperature",time:"Time",from:"From",to:"To",add_period:"Add period",delete_period:"Delete",save:"Save",saving:"Saving...",save_success:"Schedule saved successfully.",save_failed:"Failed to save schedule.",load_failed:"Failed to load schedule.",reload:"Reload from device",reload_success:"Device configuration reloaded.",reload_failed:"Failed to reload device configuration.",export:"Export",import:"Import",import_confirm_title:"Import Schedule",import_confirm_text:"Import and apply this schedule?",import_success:"Schedule imported.",import_failed:"Failed to import schedule.",no_schedule_data:"No schedule data available.",click_to_edit:"Click on a time slot to edit the schedule",copy_schedule:"Copy schedule",paste_schedule:"Paste schedule",edit:"Edit {weekday}",add_time_block:"+ Add Time Block",edit_slot:"Edit",save_slot:"Save",cancel_slot_edit:"Cancel",undo_shortcut:"Undo (Ctrl+Z)",redo_shortcut:"Redo (Ctrl+Y)",warnings_title:"Validation Warnings",base_temperature_description:"Temperature for unscheduled periods",temperature_periods:"Temperature Periods",invalid_schedule:"Invalid schedule: {error}",validation_block_end_before_start:"Block {block}: End time is before start time",validation_block_zero_duration:"Block {block}: Block has zero duration",validation_invalid_start_time:"Block {block}: Invalid start time",validation_invalid_end_time:"Block {block}: Invalid end time",validation_temp_out_of_range:"Block {block}: Temperature out of range ({min}-{max}°C)",validation_invalid_slot_count:"Invalid number of slots: {count} (expected 13)",validation_invalid_slot_key:"Invalid slot key: {key} (must be integer 1-13)",validation_missing_slot:"Missing slot {slot}",validation_slot_missing_values:"Slot {slot} missing ENDTIME or TEMPERATURE",validation_slot_time_backwards:"Slot {slot} time goes backwards: {time}",validation_slot_time_exceeds_day:"Slot {slot} time exceeds 24:00: {time}",validation_last_slot_must_end:"Last slot must end at 24:00",validation_schedule_must_be_object:"Schedule data must be an object",validation_missing_weekday:"Missing weekday: {weekday}",validation_invalid_weekday_data:"Invalid data for {weekday}",validation_weekday_error:"{weekday}: {details}",entries:"{count} entries",max_entries:"Max entries: {max}",level:"Level",duration:"Duration",condition:"Condition",target_channel:"Target channel",add_event:"Add Event",edit_event:"Edit Event",confirm_delete:"Are you sure you want to delete this event?",weekdays_label:"Weekdays",level_on:"On",level_off:"Off",slat:"Slat Position",ramp_time:"Ramp Time",astro_sunrise:"Sunrise",astro_sunset:"Sunset",astro_offset:"Astro Offset (min)",condition_fixed_time:"Fixed Time",condition_astro:"Astro",condition_fixed_if_before_astro:"Fixed if before Astro",condition_astro_if_before_fixed:"Astro if before Fixed",condition_fixed_if_after_astro:"Fixed if after Astro",condition_astro_if_after_fixed:"Astro if after Fixed",condition_earliest:"Earliest",condition_latest:"Latest"},add_link:{title:"New Direct Link",step_channel:"Step 1/3 — Select Channel",step_peer:"Step 2/3 — Select Partner",step_confirm:"Step 3/3 — Confirm",select_channel:"Select a channel from this device:",select_role:"Role of selected channel:",role_sender:"Sender (sends commands)",role_receiver:"Receiver (receives commands)",search_devices:"Search devices...",no_compatible:"No compatible channels found.",link_name:"Link name (optional)",create:"Create Link",create_success:"Link created successfully.",create_failed:"Failed to create link.",next:"Next",back:"Back"},tabs:{devices:"Devices",integration:"Integration",ccu:"OpenCCU"},integration:{system_health:"System Health",central_state:"Central State",health_score:"Health Score",device_statistics:"Device Statistics",total_devices:"Total Devices",unreachable:"Unreachable",firmware_updatable:"Firmware Updatable",total_short:"total",unreachable_short:"unreachable",command_throttle:"Command Throttle",enabled:"Enabled",interval:"Interval",queue_size:"Queue Size",throttled:"Throttled",burst_count:"Burst Count",incidents:"Incidents",no_incidents:"No incidents recorded.",clear_incidents:"Clear Incidents",clear_incidents_title:"Clear Incidents",clear_incidents_text:"Delete all recorded incidents? This cannot be undone.",incidents_cleared:"Incidents cleared.",clear:"Clear",clear_cache:"Clear Cache",clear_cache_title:"Clear Cache",clear_cache_text:"Clear all cached data? The integration will re-fetch data from the CCU.",cache_cleared:"Cache cleared.",actions:"Actions",refresh:"Refresh",action_failed:"Action failed."},ccu:{system_information:"System Information",name:"Name",model:"Model",version:"Version",serial:"Serial",hostname:"Hostname",ccu_type:"CCU Type",interfaces:"Interfaces",auth_enabled:"Authentication",update_available:"Update available",backup_exists:"Backup available",hub_messages:"Hub Messages",service_messages:"Service Messages",alarm_messages:"Alarm Messages",install_mode:"Install Mode",active:"Active",inactive:"Inactive",remaining_seconds:"{seconds}s remaining",activate:"Activate",install_mode_title:"Activate Install Mode",install_mode_text:"Activate install mode for {interface}? The CCU will accept new devices for 60 seconds.",install_mode_activated:"Install mode activated for {interface}.",signal_quality:"Signal Quality",device:"Device",interface:"Interface",reachable:"Reachable",signal:"Signal",battery:"Battery",low:"Low",ok:"OK",firmware_overview:"Firmware Overview",updatable:"updatable",current_fw:"Current",available_fw:"Available",state:"State",refresh_firmware:"Refresh Firmware Data",firmware_refreshed:"Firmware data refreshed.",actions:"Actions",refresh:"Refresh",create_backup:"Create Backup",create_backup_title:"Create CCU Backup",create_backup_text:"Create a backup of the CCU configuration? This may take a moment.",backup_running:"Creating backup...",backup_success:"Backup created: {filename} ({size} MB)",backup_failed:"Failed to create backup.",action_failed:"Action failed."}},de:{common:{back:"Zurück",loading:"Laden...",save:"Speichern",cancel:"Abbrechen",yes:"Ja",no:"Nein"},device_list:{title:"Homematic Gerätekonfiguration",select_ccu:"CCU",select_placeholder:"CCU auswählen...",search_placeholder:"Geräte suchen...",no_entry_selected:"Bitte eine CCU auswählen, um Geräte anzuzeigen.",no_devices:"Keine konfigurierbaren Geräte gefunden.",channels:"Kanäle",unreachable:"Nicht erreichbar",reachable:"Erreichbar",low_battery:"Batterie schwach",config_pending:"Konfiguration ausstehend"},device_detail:{address:"Adresse",firmware:"Firmware",channel:"Kanal",configure_master:"MASTER konfigurieren",no_master_config:"Keine MASTER-Konfiguration verfügbar.",not_found:"Gerät nicht gefunden.",yes:"Ja",no:"Nein",reachable:"Erreichbar",unreachable:"Nicht erreichbar",export:"Exportieren",import:"Importieren",export_success:"Konfiguration erfolgreich exportiert.",export_failed:"Export der Konfiguration fehlgeschlagen.",import_confirm_title:"Konfiguration importieren",import_confirm_text:"Konfiguration importieren und auf Kanal {channel} anwenden?",import_success:"Konfiguration erfolgreich importiert.",import_failed:"Import der Konfiguration fehlgeschlagen.",import_validation_failed:"Import-Validierung fehlgeschlagen.",show_history:"Änderungsverlauf",show_links:"Direktverknüpfungen",show_schedules:"Zeitpläne",rssi_device:"RSSI Gerät",rssi_peer:"RSSI Peer",dutycycle:"Duty Cycle",low_bat:"Batterie schwach",unreach:"Erreichbarkeit",config_pending_label:"Konfig. ausstehend"},form_parameter:{toggle_on:"Ein",toggle_off:"Aus",custom_value:"Wert eingeben"},time_selector:{base:"Basis",factor:"Faktor"},channel_config:{save:"Speichern",saving:"Speichern...",discard:"Änderungen verwerfen",reset_defaults:"Standardwerte laden",confirm_save_title:"Änderungen speichern",confirm_save_text:"{count} Änderung(en) auf das Gerät anwenden?",unsaved_title:"Ungespeicherte Änderungen",unsaved_warning:"Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",save_success:"Änderungen erfolgreich gespeichert.",save_failed:"Fehler beim Speichern der Änderungen.",validation_failed:"Validierung fehlgeschlagen. Bitte die markierten Felder prüfen.",undo:"Rückgängig",redo:"Wiederherstellen"},change_history:{title:"Änderungsverlauf",empty:"Keine Konfigurationsänderungen aufgezeichnet.",clear:"Verlauf löschen",clear_confirm_title:"Verlauf löschen",clear_confirm_text:"Alle Verlaufseinträge löschen? Dies kann nicht rückgängig gemacht werden.",clear_success:"Verlauf gelöscht ({count} Einträge entfernt).",source_manual:"Manuell",source_import:"Import",source_copy:"Kopie",parameters_changed:"{count} Parameter geändert"},device_links:{title:"Direktverknüpfungen",subtitle:"Direktverknüpfungen für {device}",empty:"Keine Direktverknüpfungen konfiguriert.",add_link:"Neue Verknüpfung",outgoing:"Ausgehend",incoming:"Eingehend",configure:"Konfigurieren",delete:"Löschen",delete_confirm_title:"Verknüpfung löschen",delete_confirm_text:"Direktverknüpfung von {sender} nach {receiver} entfernen? Die Geräte kommunizieren dann nicht mehr direkt.",delete_success:"Verknüpfung erfolgreich gelöscht.",delete_failed:"Fehler beim Löschen der Verknüpfung.",channel_group:"Kanal {channel}"},link_config:{title:"Link-Konfiguration",sender:"Sender",receiver:"Empfänger",save_success:"Link-Konfiguration gespeichert.",save_failed:"Fehler beim Speichern der Link-Konfiguration.",discard:"Änderungen verwerfen",confirm_save_title:"Link-Änderungen speichern",confirm_save_text:"{count} Änderung(en) auf diese Verknüpfung anwenden?",unsaved_title:"Ungespeicherte Änderungen",unsaved_warning:"Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",receiver_params:"Empfänger-Parameter",sender_params:"Sender-Parameter",no_params:"Keine konfigurierbaren Parameter für diese Verknüpfung.",profile:"Profil",short_keypress:"Kurzer Tastendruck",long_keypress:"Langer Tastendruck",last_value:"Letzter Wert",custom_time:"Benutzerdefiniert"},device_schedule:{title:"Zeitpläne",subtitle:"Zeitpläne für {device}",select_device:"Gerät auswählen...",no_devices:"Keine Geräte mit Zeitplan-Unterstützung gefunden.",schedule_type_climate:"Heizung",schedule_type_default:"Gerät",profile:"Profil",active_profile:"Aktives Profil",weekdays:"Mo,Di,Mi,Do,Fr,Sa,So",weekday_monday:"Montag",weekday_tuesday:"Dienstag",weekday_wednesday:"Mittwoch",weekday_thursday:"Donnerstag",weekday_friday:"Freitag",weekday_saturday:"Samstag",weekday_sunday:"Sonntag",base_temperature:"Basistemperatur",temperature:"Temperatur",time:"Uhrzeit",from:"Von",to:"Bis",add_period:"Zeitraum hinzufügen",delete_period:"Löschen",save:"Speichern",saving:"Speichern...",save_success:"Zeitplan erfolgreich gespeichert.",save_failed:"Fehler beim Speichern des Zeitplans.",load_failed:"Fehler beim Laden des Zeitplans.",reload:"Vom Gerät laden",reload_success:"Gerätekonfiguration neu geladen.",reload_failed:"Fehler beim Laden der Gerätekonfiguration.",export:"Exportieren",import:"Importieren",import_confirm_title:"Zeitplan importieren",import_confirm_text:"Diesen Zeitplan importieren und anwenden?",import_success:"Zeitplan importiert.",import_failed:"Fehler beim Importieren des Zeitplans.",no_schedule_data:"Keine Zeitplan-Daten verfügbar.",click_to_edit:"Klicken Sie auf einen Zeitabschnitt, um den Zeitplan zu bearbeiten",copy_schedule:"Zeitplan kopieren",paste_schedule:"Zeitplan einfügen",edit:"{weekday} bearbeiten",add_time_block:"+ Zeitblock hinzufügen",edit_slot:"Bearbeiten",save_slot:"Speichern",cancel_slot_edit:"Abbrechen",undo_shortcut:"Rückgängig (Strg+Z)",redo_shortcut:"Wiederholen (Strg+Y)",warnings_title:"Validierungswarnungen",base_temperature_description:"Temperatur für nicht geplante Zeiträume",temperature_periods:"Temperaturperioden",invalid_schedule:"Ungültiger Zeitplan: {error}",validation_block_end_before_start:"Block {block}: Die Endzeit liegt vor der Startzeit",validation_block_zero_duration:"Block {block}: Der Block hat keine Dauer",validation_invalid_start_time:"Block {block}: Ungültige Startzeit",validation_invalid_end_time:"Block {block}: Ungültige Endzeit",validation_temp_out_of_range:"Block {block}: Temperatur außerhalb des Bereichs ({min}-{max}°C)",validation_invalid_slot_count:"Ungültige Anzahl an Slots: {count} (erwartet 13)",validation_invalid_slot_key:"Ungültiger Slot-Schlüssel: {key} (muss eine Ganzzahl 1-13 sein)",validation_missing_slot:"Slot {slot} fehlt",validation_slot_missing_values:"Slot {slot} fehlt ENDTIME oder TEMPERATURE",validation_slot_time_backwards:"Slot {slot}: Zeit läuft rückwärts: {time}",validation_slot_time_exceeds_day:"Slot {slot}: Zeit überschreitet 24:00: {time}",validation_last_slot_must_end:"Der letzte Slot muss um 24:00 enden",validation_schedule_must_be_object:"Zeitplandaten müssen ein Objekt sein",validation_missing_weekday:"Fehlender Wochentag: {weekday}",validation_invalid_weekday_data:"Ungültige Daten für {weekday}",validation_weekday_error:"{weekday}: {details}",entries:"{count} Einträge",max_entries:"Max. Einträge: {max}",level:"Wert",duration:"Dauer",condition:"Bedingung",target_channel:"Zielkanal",add_event:"Ereignis hinzufügen",edit_event:"Ereignis bearbeiten",confirm_delete:"Möchten Sie dieses Ereignis wirklich löschen?",weekdays_label:"Wochentage",level_on:"Ein",level_off:"Aus",slat:"Lamellenposition",ramp_time:"Rampenzeit",astro_sunrise:"Sonnenaufgang",astro_sunset:"Sonnenuntergang",astro_offset:"Astro-Offset (Min.)",condition_fixed_time:"Feste Zeit",condition_astro:"Astro",condition_fixed_if_before_astro:"Fest wenn vor Astro",condition_astro_if_before_fixed:"Astro wenn vor Fest",condition_fixed_if_after_astro:"Fest wenn nach Astro",condition_astro_if_after_fixed:"Astro wenn nach Fest",condition_earliest:"Frühester",condition_latest:"Spätester"},add_link:{title:"Neue Direktverknüpfung",step_channel:"Schritt 1/3 — Kanal wählen",step_peer:"Schritt 2/3 — Partner wählen",step_confirm:"Schritt 3/3 — Bestätigen",select_channel:"Kanal dieses Geräts auswählen:",select_role:"Rolle des gewählten Kanals:",role_sender:"Sender (sendet Kommandos)",role_receiver:"Empfänger (empfängt Kommandos)",search_devices:"Geräte suchen...",no_compatible:"Keine kompatiblen Kanäle gefunden.",link_name:"Verknüpfungsname (optional)",create:"Verknüpfung erstellen",create_success:"Verknüpfung erfolgreich erstellt.",create_failed:"Fehler beim Erstellen der Verknüpfung.",next:"Weiter",back:"Zurück"},tabs:{devices:"Geräte",integration:"Integration",ccu:"OpenCCU"},integration:{system_health:"Systemzustand",central_state:"Zentralenstatus",health_score:"Gesundheitswert",device_statistics:"Gerätestatistik",total_devices:"Geräte gesamt",unreachable:"Nicht erreichbar",firmware_updatable:"Firmware aktualisierbar",total_short:"gesamt",unreachable_short:"nicht erreichbar",command_throttle:"Befehlsdrosselung",enabled:"Aktiviert",interval:"Intervall",queue_size:"Warteschlange",throttled:"Gedrosselt",burst_count:"Burst-Anzahl",incidents:"Vorfälle",no_incidents:"Keine Vorfälle aufgezeichnet.",clear_incidents:"Vorfälle löschen",clear_incidents_title:"Vorfälle löschen",clear_incidents_text:"Alle aufgezeichneten Vorfälle löschen? Dies kann nicht rückgängig gemacht werden.",incidents_cleared:"Vorfälle gelöscht.",clear:"Löschen",clear_cache:"Cache leeren",clear_cache_title:"Cache leeren",clear_cache_text:"Alle zwischengespeicherten Daten löschen? Die Integration holt die Daten erneut von der CCU.",cache_cleared:"Cache geleert.",actions:"Aktionen",refresh:"Aktualisieren",action_failed:"Aktion fehlgeschlagen."},ccu:{system_information:"Systeminformationen",name:"Name",model:"Modell",version:"Version",serial:"Seriennummer",hostname:"Hostname",ccu_type:"CCU-Typ",interfaces:"Schnittstellen",auth_enabled:"Authentifizierung",update_available:"Update verfügbar",backup_exists:"Backup vorhanden",hub_messages:"Hub-Meldungen",service_messages:"Servicemeldungen",alarm_messages:"Alarmmeldungen",install_mode:"Anlernmodus",active:"Aktiv",inactive:"Inaktiv",remaining_seconds:"Noch {seconds}s",activate:"Aktivieren",install_mode_title:"Anlernmodus aktivieren",install_mode_text:"Anlernmodus für {interface} aktivieren? Die CCU akzeptiert 60 Sekunden lang neue Geräte.",install_mode_activated:"Anlernmodus für {interface} aktiviert.",signal_quality:"Signalqualität",device:"Gerät",interface:"Schnittstelle",reachable:"Erreichbar",signal:"Signal",battery:"Batterie",low:"Schwach",ok:"OK",firmware_overview:"Firmware-Übersicht",updatable:"aktualisierbar",current_fw:"Aktuell",available_fw:"Verfügbar",state:"Status",refresh_firmware:"Firmware-Daten aktualisieren",firmware_refreshed:"Firmware-Daten aktualisiert.",actions:"Aktionen",refresh:"Aktualisieren",create_backup:"Backup erstellen",create_backup_title:"CCU-Backup erstellen",create_backup_text:"Ein Backup der CCU-Konfiguration erstellen? Dies kann einen Moment dauern.",backup_running:"Backup wird erstellt...",backup_success:"Backup erstellt: {filename} ({size} MB)",backup_failed:"Fehler beim Erstellen des Backups.",action_failed:"Aktion fehlgeschlagen."}}};function Ie(e,t=""){const i={};for(const[s,a]of Object.entries(e)){const e=t?`${t}.${s}`:s;"string"==typeof a?i[e]=a:"object"==typeof a&&null!==a&&Object.assign(i,Ie(a,e))}return i}const De=new Map;function Te(e){if(De.has(e))return De.get(e);const t=Ie(Ae[e]??Ae.en);return De.set(e,t),t}function Me(e,t,i){const s=Te(e.config.language??"en");let a=s[t]??s[t.replace(/^panel\./,"")]??t;if(i)for(const[e,t]of Object.entries(i))a=a.replace(`{${e}}`,String(t));return a}let Pe=class extends oe{constructor(){super(...arguments),this.entryId="",this.entries=[],this._devices=[],this._loading=!1,this._searchQuery="",this._error=""}updated(e){e.has("entryId")&&this.entryId&&this._fetchDevices()}async _fetchDevices(){if(this.entryId){this._loading=!0,this._error="";try{this._devices=await ge(this.hass,this.entryId)}catch(e){this._error=String(e),this._devices=[]}finally{this._loading=!1}}}_l(e,t){return Me(this.hass,e,t)}get _filteredDevices(){if(!this._searchQuery)return this._devices;const e=this._searchQuery.toLowerCase();return this._devices.filter(t=>t.name.toLowerCase().includes(e)||t.address.toLowerCase().includes(e)||t.model.toLowerCase().includes(e))}get _groupedDevices(){const e=[...this._filteredDevices].sort((e,t)=>e.name.localeCompare(t.name)),t=new Map;for(const i of e){const e=i.interface_id.split("-").slice(1).join("-")||i.interface_id;t.has(e)||t.set(e,[]),t.get(e).push(i)}return t}_handleEntryChanged(e){e.stopPropagation();const t=e.detail.value;t&&t!==this.entryId&&this.dispatchEvent(new CustomEvent("entry-changed",{detail:{entryId:t},bubbles:!0,composed:!0}))}_handleDeviceClick(e){this.dispatchEvent(new CustomEvent("device-selected",{detail:{device:e.address,interfaceId:e.interface_id},bubbles:!0,composed:!0}))}_handleIconError(e){e.target.style.display="none"}_renderMaintenanceIcons(e){return e&&0!==Object.keys(e).length?W`
      <div class="device-status">
        ${!0===e.unreach?W`<ha-icon
              class="status-badge unreachable"
              .icon=${"mdi:close-circle"}
              title="${this._l("device_list.unreachable")}"
            ></ha-icon>`:!1===e.unreach?W`<ha-icon
                class="status-badge reachable"
                .icon=${"mdi:check-circle"}
                title="${this._l("device_list.reachable")}"
              ></ha-icon>`:j}
        ${!0===e.low_bat?W`<ha-icon
              class="status-badge low-bat"
              .icon=${"mdi:battery-alert"}
              title="${this._l("device_list.low_battery")}"
            ></ha-icon>`:j}
        ${!0===e.config_pending?W`<ha-icon
              class="status-badge config-pending"
              .icon=${"mdi:clock-alert-outline"}
              title="${this._l("device_list.config_pending")}"
            ></ha-icon>`:j}
      </div>
    `:j}render(){return W`
      <div class="panel-header">
        <h1>${this._l("device_list.title")}</h1>
      </div>

      ${this.entries.length>1?W`
            <div class="entry-selector">
              <ha-select
                .label=${this._l("device_list.select_ccu")}
                .value=${this.entryId}
                .options=${this.entries.map(e=>({value:e.entry_id,label:e.title}))}
                @selected=${this._handleEntryChanged}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            </div>
          `:j}
      ${this.entryId?W`
            <div class="search-bar">
              <input
                type="text"
                .value=${this._searchQuery}
                @input=${e=>{this._searchQuery=e.target.value}}
                placeholder=${this._l("device_list.search_placeholder")}
              />
            </div>
          `:j}
      ${this._loading?W`<div class="loading"><span>${this._l("common.loading")}</span></div>`:this._error?W`<div class="error">${this._error}</div>`:this.entryId?0===this._filteredDevices.length?W`<div class="empty-state">${this._l("device_list.no_devices")}</div>`:this._renderDeviceGroups():W`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}
    `}_renderDeviceGroups(){return W`
      ${Array.from(this._groupedDevices.entries()).map(([e,t])=>W`
          <div class="interface-group">
            <div class="interface-header">${e}</div>
            ${t.map(e=>W`
                <div class="device-card" @click=${()=>this._handleDeviceClick(e)}>
                  ${e.device_icon?W`<img
                        class="device-icon"
                        src=${me(this.entryId,e.device_icon)}
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
    `}static{this.styles=[ue,r`
      .panel-header h1 {
        margin: 0 0 16px;
        font-size: 24px;
        font-weight: 400;
      }

      .entry-selector {
        margin-bottom: 16px;
      }

      .entry-selector ha-select {
        width: 100%;
      }

      .search-bar {
        margin-bottom: 16px;
      }

      .search-bar input {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid var(--divider-color);
        border-radius: 4px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
        font-size: 14px;
        box-sizing: border-box;
      }

      .interface-group {
        margin-bottom: 16px;
      }

      .interface-header {
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

      .device-card:hover {
        background-color: var(--secondary-background-color, #f5f5f5);
      }

      .device-icon {
        height: 32px;
        width: 32px;
        object-fit: contain;
        flex-shrink: 0;
        margin-right: 4px;
      }

      .device-main {
        flex: 1;
      }

      .device-name {
        font-size: 14px;
        font-weight: 500;
      }

      .device-model {
        font-size: 13px;
        color: var(--secondary-text-color);
        margin-top: 2px;
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
        --mdc-icon-size: 18px;
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
        --mdc-icon-size: 18px;
        color: var(--secondary-text-color);
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
    `]}};function Le(e,t){return new Promise(e=>{const i=document.createElement("dialog");i.style.cssText=["border: none","border-radius: var(--ha-card-border-radius, 12px)","padding: 24px","max-width: 450px","width: calc(100% - 48px)","box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3)","font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif)","background: var(--card-background-color, var(--ha-card-background, #fff))","color: var(--primary-text-color, #212121)"].join("; ");const s=t.title?`<h2 style="margin: 0 0 16px; font-size: 18px; font-weight: 500;">${ze(t.title)}</h2>`:"",a=t.text?`<p style="margin: 0 0 24px; white-space: pre-line; line-height: 1.5; color: var(--secondary-text-color, #727272);">${ze(t.text)}</p>`:"",n=t.destructive?"var(--error-color, #db4437)":"var(--primary-color, #03a9f4)";i.innerHTML=`\n      ${s}\n      ${a}\n      <div style="display: flex; justify-content: flex-end; gap: 8px;">\n        <button class="dismiss" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: transparent;\n          color: var(--primary-text-color, #212121);\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${ze(t.dismissText||"Cancel")}</button>\n        <button class="confirm" style="\n          padding: 8px 16px;\n          border: none;\n          border-radius: 4px;\n          background: ${n};\n          color: #fff;\n          font-size: 14px;\n          font-family: inherit;\n          cursor: pointer;\n        ">${ze(t.confirmText||"OK")}</button>\n      </div>\n    `;const r=t=>{i.close(),i.remove(),e(t)};i.querySelector(".confirm").addEventListener("click",()=>r(!0)),i.querySelector(".dismiss").addEventListener("click",()=>r(!1)),i.addEventListener("cancel",e=>{e.preventDefault(),r(!1)}),document.body.appendChild(i),i.showModal()})}function ze(e){const t=document.createElement("div");return t.textContent=e,t.innerHTML}function Ne(e,t){const i=new CustomEvent("hass-notification",{bubbles:!0,composed:!0,detail:t});e.dispatchEvent(i)}e([he({attribute:!1})],Pe.prototype,"hass",void 0),e([he()],Pe.prototype,"entryId",void 0),e([he({attribute:!1})],Pe.prototype,"entries",void 0),e([pe()],Pe.prototype,"_devices",void 0),e([pe()],Pe.prototype,"_loading",void 0),e([pe()],Pe.prototype,"_searchQuery",void 0),e([pe()],Pe.prototype,"_error",void 0),Pe=e([_e("hm-device-list")],Pe);let Re=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this._device=null,this._hasSchedule=!1,this._loading=!0,this._error=""}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this.deviceAddress&&this._fetchDevice()}async _fetchDevice(){this._loading=!0,this._error="";try{const[e,t]=await Promise.all([ge(this.hass,this.entryId),ke(this.hass,this.entryId).catch(()=>[])]);this._device=e.find(e=>e.address===this.deviceAddress)??null,this._hasSchedule=t.some(e=>e.address===this.deviceAddress)}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_handleChannelClick(e){this.dispatchEvent(new CustomEvent("channel-selected",{detail:{channel:e.address,interfaceId:this.interfaceId,channelType:e.channel_type,paramsetKey:"MASTER",deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowHistory(){this.dispatchEvent(new CustomEvent("show-history",{detail:{device:this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowLinks(){this.dispatchEvent(new CustomEvent("show-links",{detail:{device:this.deviceAddress,interfaceId:this.interfaceId,deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}_handleShowSchedules(){this.dispatchEvent(new CustomEvent("show-schedules",{detail:{device:this.deviceAddress,interfaceId:this.interfaceId,deviceName:this._device?.name||this.deviceAddress},bubbles:!0,composed:!0}))}async _handleExport(e){try{const t=await async function(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/export_paramset",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}(this.hass,this.entryId,this.interfaceId,e.address,"MASTER"),i=new Blob([t.json_data],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s,a.download=`${e.address.replace(/:/g,"_")}_MASTER.json`,a.click(),URL.revokeObjectURL(s),Ne(this,{message:this._l("device_detail.export_success")})}catch{Ne(this,{message:this._l("device_detail.export_failed")})}}async _handleImport(e){const t=document.createElement("input");t.type="file",t.accept=".json",t.onchange=async()=>{const i=t.files?.[0];if(i)try{const t=await i.text();if(!await Le(0,{title:this._l("device_detail.import_confirm_title"),text:this._l("device_detail.import_confirm_text",{channel:e.address}),confirmText:this._l("device_detail.import"),dismissText:this._l("common.cancel")}))return;const s=await async function(e,t,i,s,a,n="MASTER"){return e.callWS({type:"homematicip_local/config/import_paramset",entry_id:t,interface_id:i,channel_address:s,json_data:a,paramset_key:n})}(this.hass,this.entryId,this.interfaceId,e.address,t,"MASTER");Ne(this,s.success?{message:this._l("device_detail.import_success")}:{message:this._l("device_detail.import_validation_failed")})}catch{Ne(this,{message:this._l("device_detail.import_failed")})}},t.click()}_handleIconError(e){e.target.style.display="none"}render(){if(this._loading)return W`<div class="loading">${this._l("common.loading")}</div>`;if(this._error)return W`<div class="error">${this._error}</div>`;if(!this._device)return W`<div class="empty-state">${this._l("device_detail.not_found")}</div>`;const e=this._device,t=e.channels.find(e=>e.address.endsWith(":0")),i=e.channels.filter(e=>!e.address.endsWith(":0"));return W`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="device-header">
        ${e.device_icon?W`<img
              class="device-icon"
              src=${me(this.entryId,e.device_icon)}
              alt=""
              @error=${this._handleIconError}
            />`:j}
        <div class="device-header-text">
          <h2>${e.model} — ${e.name}</h2>
          <div class="device-info">
            ${this._l("device_detail.address")}: ${e.address} |
            ${this._l("device_detail.firmware")}: ${e.firmware}
          </div>
        </div>
        <div class="header-actions">
          ${ve.has(e.interface)?W`
                <ha-button outlined @click=${this._handleShowLinks}>
                  ${this._l("device_detail.show_links")}
                </ha-button>
              `:j}
          ${this._hasSchedule?W`
                <ha-button outlined @click=${this._handleShowSchedules}>
                  ${this._l("device_detail.show_schedules")}
                </ha-button>
              `:j}
          <ha-button outlined @click=${this._handleShowHistory}>
            ${this._l("device_detail.show_history")}
          </ha-button>
        </div>
      </div>

      ${t?this._renderMaintenanceChannel(t,e.maintenance):j}
      ${i.map(e=>this._renderChannel(e))}
    `}_renderMaintenanceChannel(e,t){const i=t&&Object.keys(t).length>0,s=e.paramset_keys.includes("MASTER");return W`
      <div class="channel-card maintenance">
        <div class="channel-header">
          ${this._l("device_detail.channel")} 0: ${e.channel_type_label}
        </div>
        ${i?this._renderStatusSummary(t):j}
        ${s?W`
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
    `}_renderStatusSummary(e){const t=[];return void 0!==e.rssi_device&&t.push({label:this._l("device_detail.rssi_device"),value:`${e.rssi_device} dBm`,icon:"mdi:signal"}),void 0!==e.rssi_peer&&t.push({label:this._l("device_detail.rssi_peer"),value:`${e.rssi_peer} dBm`,icon:"mdi:signal"}),void 0!==e.dutycycle&&t.push({label:this._l("device_detail.dutycycle"),value:String(e.dutycycle),icon:"mdi:timer-outline"}),void 0!==e.low_bat&&t.push({label:this._l("device_detail.low_bat"),value:this._l(e.low_bat?"device_detail.yes":"device_detail.no"),icon:"mdi:battery-alert"}),void 0!==e.unreach&&t.push({label:this._l("device_detail.unreach"),value:this._l(e.unreach?"device_detail.unreachable":"device_detail.reachable"),icon:e.unreach?"mdi:close-circle":"mdi:check-circle"}),void 0!==e.config_pending&&t.push({label:this._l("device_detail.config_pending_label"),value:this._l(e.config_pending?"device_detail.yes":"device_detail.no"),icon:"mdi:information-outline"}),0===t.length?j:W`
      <div class="status-grid">
        ${t.map(e=>W`
            <div class="status-item">
              <ha-icon class="status-icon" .icon=${e.icon}></ha-icon>
              <span>${e.label}: ${e.value}</span>
            </div>
          `)}
      </div>
    `}_renderChannel(e){const t=e.address.split(":").pop()??"",i=e.paramset_keys.includes("MASTER");return W`
      <div class="channel-card">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${e.channel_type_label}
        </div>
        ${i?W`
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
            `:W`
              <div class="channel-no-config">${this._l("device_detail.no_master_config")}</div>
            `}
      </div>
    `}static{this.styles=[ue,r`
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
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
      }
    `]}};function Be(e,t){return e.option_labels?.[t]??t}function Ue(e,t,i){return t.options&&"number"==typeof i&&i>=0&&i<t.options.length?Be(t,t.options[i]):"toggle"===t.widget?Me(e,i?"form_parameter.toggle_on":"form_parameter.toggle_off"):String(i??"")}e([he({attribute:!1})],Re.prototype,"hass",void 0),e([he()],Re.prototype,"entryId",void 0),e([he()],Re.prototype,"interfaceId",void 0),e([he()],Re.prototype,"deviceAddress",void 0),e([pe()],Re.prototype,"_device",void 0),e([pe()],Re.prototype,"_hasSchedule",void 0),e([pe()],Re.prototype,"_loading",void 0),e([pe()],Re.prototype,"_error",void 0),Re=e([_e("hm-device-detail")],Re);let Ve=class extends oe{constructor(){super(...arguments),this.value=null,this.modified=!1,this.validationError=""}_getDisplayValue(e){return Ue(this.hass,this.parameter,e)}_emitChange(e){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:this.parameter.id,value:e,currentValue:this.parameter.current_value},bubbles:!0,composed:!0}))}render(){const e=this.parameter,t=!e.writable;return W`
      <div class="parameter-row ${t?"read-only":""}">
        <div class="parameter-label">
          ${e.label}
          ${e.unit?W`<span class="parameter-unit">(${e.unit})</span>`:j}
          ${this.modified?W`<span class="modified-dot"></span>`:j}
        </div>
        <div class="parameter-control">${this._renderWidget(e,t)}</div>
      </div>
      ${e.description?W`<ha-markdown
            .content=${e.description}
            class="parameter-description"
          ></ha-markdown>`:j}
      ${this.validationError?W`<div class="validation-error">${this.validationError}</div>`:j}
    `}_renderWidget(e,t){switch(e.widget){case"toggle":return W`
          <ha-switch
            .checked=${Boolean(this.value)}
            .disabled=${t}
            @change=${e=>{this._emitChange(e.target.checked)}}
          ></ha-switch>
        `;case"slider_with_input":return W`
          <div class="slider-group">
            <ha-slider
              .min=${e.min??0}
              .max=${e.max??100}
              .step=${e.step??1}
              .value=${Number(this.value??e.min??0)}
              .disabled=${t}
              @value-changed=${t=>{t.stopPropagation();const i=Number(t.detail.value),s="integer"===e.type?Math.round(i):i;s!==this.value&&this._emitChange(s)}}
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
        `;case"number_input":return W`
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
        `;case"dropdown":return W`
          <ha-select
            .value=${String(this.value??0)}
            .disabled=${t}
            .options=${(e.options??[]).map((t,i)=>({value:String(i),label:Be(e,t)}))}
            @selected=${e=>{e.stopPropagation();const t=parseInt(e.detail.value,10);Number.isNaN(t)||t===this.value||this._emitChange(t)}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        `;case"radio_group":return W`
          <div class="radio-group">
            ${(e.options??[]).map((i,s)=>W`
                <label class="radio-item">
                  <ha-radio
                    name=${e.id}
                    .checked=${this.value===s}
                    .disabled=${t}
                    @change=${()=>this._emitChange(s)}
                  ></ha-radio>
                  ${Be(e,i)}
                </label>
              `)}
          </div>
        `;case"text_input":return W`
          <input
            type="text"
            .value=${String(this.value??"")}
            ?disabled=${t}
            @change=${e=>{this._emitChange(e.target.value)}}
          />
        `;case"button":return W`
          <ha-button outlined .disabled=${t} @click=${()=>this._emitChange(!0)}>
            ${e.label}
          </ha-button>
        `;default:return W`<span class="read-only-value">${this._getDisplayValue(this.value)}</span>`}}static{this.styles=[ue,r`
      .read-only {
        opacity: 0.7;
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

      .parameter-description {
        display: block;
        font-size: 12px;
        color: var(--secondary-text-color);
        margin: -4px 0 4px;
        line-height: 1.4;
      }

      @media (max-width: 600px) {
        .slider-group {
          width: 100%;
        }

        .number-input {
          width: 100%;
          box-sizing: border-box;
        }

        ha-select {
          width: 100%;
          box-sizing: border-box;
        }

        input[type="text"] {
          width: 100%;
          box-sizing: border-box;
        }
      }
    `]}};e([he({attribute:!1})],Ve.prototype,"hass",void 0),e([he({attribute:!1})],Ve.prototype,"parameter",void 0),e([he()],Ve.prototype,"value",void 0),e([he({type:Boolean})],Ve.prototype,"modified",void 0),e([he()],Ve.prototype,"validationError",void 0),Ve=e([_e("hm-form-parameter")],Ve);const Oe=[{unit:0,value:0,label_en:"Not active",label_de:"Nicht aktiv"},{unit:0,value:1,label_en:"100ms",label_de:"100ms"},{unit:0,value:3,label_en:"300ms",label_de:"300ms"},{unit:0,value:5,label_en:"500ms",label_de:"500ms"},{unit:0,value:15,label_en:"1500ms",label_de:"1500ms"},{unit:1,value:1,label_en:"1 second",label_de:"1 Sekunde"},{unit:1,value:2,label_en:"2 seconds",label_de:"2 Sekunden"},{unit:1,value:3,label_en:"3 seconds",label_de:"3 Sekunden"},{unit:1,value:30,label_en:"30 seconds",label_de:"30 Sekunden"},{unit:2,value:1,label_en:"1 minute",label_de:"1 Minute"},{unit:2,value:2,label_en:"2 minutes",label_de:"2 Minuten"},{unit:2,value:4,label_en:"4 minutes",label_de:"4 Minuten"},{unit:2,value:15,label_en:"15 minutes",label_de:"15 Minuten"}];let He=class extends oe{constructor(){super(...arguments),this.pendingChanges=new Map,this.validationErrors={},this._customModePairs=new Set}_getEffectiveValue(e){return this.pendingChanges.has(e.id)?this.pendingChanges.get(e.id):e.current_value}_isModified(e){return this.pendingChanges.has(e.id)}_detectPairs(e){const t=new Map,i=new Set;for(const s of e.parameters)if(s.id.endsWith("_UNIT")&&s.options?.length){const a=s.id.slice(0,-5),n=e.parameters.find(e=>e.id===`${a}_VALUE`);n&&(t.set(a,{unitParam:s,valueParam:n}),i.add(s.id),i.add(n.id))}return{pairs:t,pairedIds:i}}_derivePairLabel(e,t){if("de"===t){if(e.startsWith("Wert "))return e.slice(5)}else if(e.endsWith(" Value"))return e.slice(0,-6);return e}render(){return this.schema&&this.schema.sections?W`
      ${this.schema.sections.map(e=>{const{pairs:t,pairedIds:i}=this._detectPairs(e),s=new Set;return W`
          <div class="form-section">
            <div class="section-header">${e.title}</div>
            ${e.parameters.map(e=>{if(s.has(e.id))return j;if(i.has(e.id)){const i=e.id.endsWith("_UNIT")?e.id.slice(0,-5):e.id.slice(0,-6),a=t.get(i);if(a)return s.add(a.unitParam.id),s.add(a.valueParam.id),this._renderTimePair(i,a)}return W`
                <hm-form-parameter
                  .hass=${this.hass}
                  .parameter=${e}
                  .value=${this._getEffectiveValue(e)}
                  .modified=${this._isModified(e)}
                  .validationError=${this.validationErrors[e.id]??""}
                  @value-changed=${this._handleValueChanged}
                ></hm-form-parameter>
              `})}
          </div>
        `})}
    `:j}_renderTimePair(e,t){const{unitParam:i,valueParam:s}=t,a=this.hass.config.language??"en",n=Number(this._getEffectiveValue(i)??0),r=Number(this._getEffectiveValue(s)??0),o=this._isModified(i)||this._isModified(s),d=!i.writable||!s.writable,l=this._derivePairLabel(s.label,a),c=Oe.findIndex(e=>e.unit===n&&e.value===r),h=this._customModePairs.has(e)||c<0,p=h?"custom":String(c);return W`
      <div class="parameter-row ${d?"read-only":""}">
        <div class="parameter-label">
          ${l} ${o?W`<span class="modified-dot"></span>`:j}
        </div>
        <div class="parameter-control">
          <ha-select
            .value=${p}
            .disabled=${d}
            .options=${[...Oe.map((e,t)=>({value:String(t),label:"de"===a?e.label_de:e.label_en})),{value:"custom",label:Me(this.hass,"form_parameter.custom_value")}]}
            @selected=${t=>this._handlePresetSelected(t,e,i,s)}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
      ${this._renderPairValidationErrors(i,s)}
      ${h?this._renderCustomFields(i,s):j}
    `}_renderPairValidationErrors(e,t){const i=this.validationErrors[e.id],s=this.validationErrors[t.id];return i||s?W`
      ${i?W`<div class="validation-error">${i}</div>`:j}
      ${s?W`<div class="validation-error">${s}</div>`:j}
    `:j}_renderCustomFields(e,t){return W`
      <div class="custom-fields">
        <hm-form-parameter
          .hass=${this.hass}
          .parameter=${e}
          .value=${this._getEffectiveValue(e)}
          .modified=${this._isModified(e)}
          .validationError=${""}
          @value-changed=${this._handleValueChanged}
        ></hm-form-parameter>
        <hm-form-parameter
          .hass=${this.hass}
          .parameter=${t}
          .value=${this._getEffectiveValue(t)}
          .modified=${this._isModified(t)}
          .validationError=${""}
          @value-changed=${this._handleValueChanged}
        ></hm-form-parameter>
      </div>
    `}_handlePresetSelected(e,t,i,s){e.stopPropagation();const a=e.detail.value;if(!a||"custom"===a)return this._customModePairs.add(t),void this.requestUpdate();this._customModePairs.delete(t);const n=Oe[parseInt(a,10)];if(n){const e=Number(this._getEffectiveValue(i)??0),t=Number(this._getEffectiveValue(s)??0);if(n.unit===e&&n.value===t)return;this._dispatchValueChanged(i.id,n.unit,i.current_value),this._dispatchValueChanged(s.id,n.value,s.current_value)}}_dispatchValueChanged(e,t,i){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:e,value:t,currentValue:i},bubbles:!0,composed:!0}))}_handleValueChanged(e){this.dispatchEvent(new CustomEvent("value-changed",{detail:e.detail,bubbles:!0,composed:!0}))}static{this.styles=[ue,r`
      .form-section {
        margin-bottom: 16px;
      }

      .custom-fields {
        padding-left: 16px;
        border-left: 2px solid var(--divider-color, #e0e0e0);
        margin: 0 0 8px;
      }
    `]}};e([he({attribute:!1})],He.prototype,"hass",void 0),e([he({attribute:!1})],He.prototype,"schema",void 0),e([he({attribute:!1})],He.prototype,"pendingChanges",void 0),e([he({attribute:!1})],He.prototype,"validationErrors",void 0),He=e([_e("hm-config-form")],He);let We=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.channelAddress="",this.channelType="",this.paramsetKey="MASTER",this.deviceName="",this._schema=null,this._pendingChanges=new Map,this._loading=!0,this._saving=!1,this._error="",this._validationErrors={},this._sessionActive=!1,this._canUndo=!1,this._canRedo=!1}updated(e){(e.has("channelAddress")||e.has("entryId"))&&this.entryId&&this.channelAddress&&this._fetchSchema()}async _fetchSchema(){this._loading=!0,this._error="",this._pendingChanges=new Map,this._validationErrors={},this._canUndo=!1,this._canRedo=!1;try{this._schema=await fe(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.channelType,this.paramsetKey),await ye(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey),this._sessionActive=!0}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}get _isDirty(){return this._pendingChanges.size>0}async _handleValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;if(i===s?this._pendingChanges.delete(t):this._pendingChanges.set(t,i),this._pendingChanges=new Map(this._pendingChanges),this._sessionActive)try{const e=await async function(e,t,i,s,a,n="MASTER"){return e.callWS({type:"homematicip_local/config/session_set",entry_id:t,channel_address:i,parameter:s,value:a,paramset_key:n})}(this.hass,this.entryId,this.channelAddress,t,i,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,this._validationErrors=e.validation_errors}catch{}}async _handleUndo(){if(this._sessionActive)try{const e=await async function(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_undo",entry_id:t,channel_address:i,paramset_key:s})}(this.hass,this.entryId,this.channelAddress,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,e.performed&&await this._refreshSchemaValues()}catch(e){this._error=String(e)}}async _handleRedo(){if(this._sessionActive)try{const e=await async function(e,t,i,s="MASTER"){return e.callWS({type:"homematicip_local/config/session_redo",entry_id:t,channel_address:i,paramset_key:s})}(this.hass,this.entryId,this.channelAddress,this.paramsetKey);this._canUndo=e.can_undo,this._canRedo=e.can_redo,e.performed&&await this._refreshSchemaValues()}catch(e){this._error=String(e)}}async _refreshSchemaValues(){try{this._schema=await fe(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.channelType,this.paramsetKey),this._pendingChanges=new Map}catch(e){this._error=String(e)}}_handleDiscard(){this._pendingChanges=new Map,this._validationErrors={},this._sessionActive&&be(this.hass,this.entryId,this.channelAddress,this.paramsetKey).then(()=>(this._canUndo=!1,this._canRedo=!1,ye(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey))).catch(()=>{})}_handleResetDefaults(){if(this._schema){this._pendingChanges=new Map;for(const e of this._schema.sections)for(const t of e.parameters)t.writable&&void 0!==t.default&&t.default!==t.current_value&&this._pendingChanges.set(t.id,t.default);this._pendingChanges=new Map(this._pendingChanges)}}async _handleSave(){if(!this._isDirty||this._saving)return;const e=this._pendingChanges.size,t=[...this._pendingChanges.entries()].map(([e,t])=>{const i=this._findParameter(e);return`${i?.label??e}: ${i?Ue(this.hass,i,i.current_value):"?"} → ${i?Ue(this.hass,i,t):String(t)}`}).join("\n");if(await Le(0,{title:this._l("channel_config.confirm_save_title"),text:`${this._l("channel_config.confirm_save_text",{count:e})}\n\n${t}`,confirmText:this._l("common.save"),dismissText:this._l("common.cancel")})){this._saving=!0,this._validationErrors={};try{if(this._sessionActive){const e=await async function(e,t,i,s,a="MASTER"){return e.callWS({type:"homematicip_local/config/session_save",entry_id:t,interface_id:i,channel_address:s,paramset_key:a})}(this.hass,this.entryId,this.interfaceId,this.channelAddress,this.paramsetKey);e.success?(this._pendingChanges=new Map,this._sessionActive=!1,Ne(this,{message:this._l("channel_config.save_success")}),await this._fetchSchema()):Object.keys(e.validation_errors).length>0?(this._validationErrors=e.validation_errors,Ne(this,{message:this._l("channel_config.validation_failed")})):Ne(this,{message:this._l("channel_config.save_failed")})}else{const e=Object.fromEntries(this._pendingChanges),t=await async function(e,t,i,s,a,n="MASTER",r=!0){return e.callWS({type:"homematicip_local/config/put_paramset",entry_id:t,interface_id:i,channel_address:s,paramset_key:n,values:a,validate:r})}(this.hass,this.entryId,this.interfaceId,this.channelAddress,e,this.paramsetKey);t.success?(this._pendingChanges=new Map,Ne(this,{message:this._l("channel_config.save_success")}),await this._fetchSchema()):Object.keys(t.validation_errors).length>0?(this._validationErrors=t.validation_errors,Ne(this,{message:this._l("channel_config.validation_failed")})):Ne(this,{message:this._l("channel_config.save_failed")})}}catch(e){this._error=String(e),Ne(this,{message:this._l("channel_config.save_failed")})}finally{this._saving=!1}}}_findParameter(e){if(this._schema)for(const t of this._schema.sections){const i=t.parameters.find(t=>t.id===e);if(i)return i}}async _handleBack(){if(!this._isDirty||await Le(0,{title:this._l("channel_config.unsaved_title"),text:this._l("channel_config.unsaved_warning"),confirmText:this._l("channel_config.discard"),dismissText:this._l("common.cancel"),destructive:!0})){if(this._sessionActive){try{await be(this.hass,this.entryId,this.channelAddress,this.paramsetKey)}catch{}this._sessionActive=!1}this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}}_handleIconError(e){e.target.style.display="none"}render(){return this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:this._error&&!this._schema?W`<div class="error">${this._error}</div>`:W`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="config-header">
        ${this._schema?.device_icon?W`<img
              class="device-icon"
              src=${me(this.entryId,this._schema.device_icon)}
              alt=""
              @error=${this._handleIconError}
            />`:j}
        <div class="config-header-text">
          ${this.deviceName?W`<h2>${this.deviceName}</h2>`:j}
          <div class="device-info">
            ${this.channelAddress} —
            ${this._schema?.channel_type_label||this._schema?.channel_type||""} —
            ${this.paramsetKey}
          </div>
        </div>
      </div>

      ${this._error?W`<div class="error">${this._error}</div>`:j}
      ${this._schema?W`
            <hm-config-form
              .hass=${this.hass}
              .schema=${this._schema}
              .pendingChanges=${this._pendingChanges}
              .validationErrors=${this._validationErrors}
              @value-changed=${this._handleValueChanged}
            ></hm-config-form>
          `:j}

      <div class="action-bar-split">
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
          <ha-button raised @click=${this._handleSave} .disabled=${!this._isDirty||this._saving}>
            ${this._l(this._saving?"channel_config.saving":"channel_config.save")}
          </ha-button>
        </div>
      </div>
    `}static{this.styles=[ue,r`
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

      .config-header-text h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
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
    `]}};e([he({attribute:!1})],We.prototype,"hass",void 0),e([he()],We.prototype,"entryId",void 0),e([he()],We.prototype,"interfaceId",void 0),e([he()],We.prototype,"channelAddress",void 0),e([he()],We.prototype,"channelType",void 0),e([he()],We.prototype,"paramsetKey",void 0),e([he()],We.prototype,"deviceName",void 0),e([pe()],We.prototype,"_schema",void 0),e([pe()],We.prototype,"_pendingChanges",void 0),e([pe()],We.prototype,"_loading",void 0),e([pe()],We.prototype,"_saving",void 0),e([pe()],We.prototype,"_error",void 0),e([pe()],We.prototype,"_validationErrors",void 0),e([pe()],We.prototype,"_sessionActive",void 0),e([pe()],We.prototype,"_canUndo",void 0),e([pe()],We.prototype,"_canRedo",void 0),We=e([_e("hm-channel-config")],We);let Fe=class extends oe{constructor(){super(...arguments),this.entryId="",this.filterDevice="",this._entries=[],this._total=0,this._loading=!0,this._error="",this._expandedEntries=new Set}updated(e){(e.has("entryId")||e.has("filterDevice"))&&this.entryId&&this._fetchHistory()}async _fetchHistory(){this._loading=!0,this._error="";try{const e=await async function(e,t,i="",s=50){return e.callWS({type:"homematicip_local/config/get_change_history",entry_id:t,channel_address:i,limit:s})}(this.hass,this.entryId,this.filterDevice);this._entries=e.entries,this._total=e.total}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_toggleEntry(e){const t=new Set(this._expandedEntries);t.has(e)?t.delete(e):t.add(e),this._expandedEntries=t}async _handleClear(){if(await Le(0,{title:this._l("change_history.clear_confirm_title"),text:this._l("change_history.clear_confirm_text"),confirmText:this._l("change_history.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{const e=await async function(e,t){return e.callWS({type:"homematicip_local/config/clear_change_history",entry_id:t})}(this.hass,this.entryId);e.success&&(Ne(this,{message:this._l("change_history.clear_success",{count:e.cleared})}),this._entries=[],this._total=0)}catch{Ne(this,{message:this._l("channel_config.save_failed")})}}_formatTimestamp(e){try{return new Date(e).toLocaleString(this.hass.config.language||"en")}catch{return e}}_getSourceLabel(e){switch(e){case"manual":return this._l("change_history.source_manual");case"import":return this._l("change_history.source_import");case"copy":return this._l("change_history.source_copy");default:return e}}render(){return W`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("common.back")}
      ></ha-icon-button>

      <div class="history-header-bar">
        <h2>${this._l("change_history.title")}</h2>
      </div>

      ${this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:this._error?W`<div class="error">${this._error}</div>`:0===this._entries.length?W`<div class="empty-state">${this._l("change_history.empty")}</div>`:this._renderEntries()}
      ${!this._loading&&this._entries.length>0?W`
            <div class="action-bar">
              <ha-button class="destructive" @click=${this._handleClear}>
                ${this._l("change_history.clear")}
              </ha-button>
            </div>
          `:j}
    `}_renderEntries(){return W`
      <div class="history-list">
        ${this._entries.map((e,t)=>{const i=`${e.timestamp}-${t}`,s=this._expandedEntries.has(i),a=Object.keys(e.changes).length;return W`
            <div class="history-entry">
              <div class="history-entry-header" @click=${()=>this._toggleEntry(i)}>
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
                  <span class="source-badge">${this._getSourceLabel(e.source)}</span>
                  <ha-icon
                    class="expand-icon"
                    .icon=${s?"mdi:chevron-down":"mdi:chevron-right"}
                  ></ha-icon>
                </div>
              </div>
              ${s?W`
                    <div class="history-details">
                      ${Object.entries(e.changes).map(([e,t])=>W`
                          <div class="change-row">
                            <span class="change-param">${e}</span>
                            <span class="change-values">
                              <span class="change-old">${String(t.old)}</span>
                              <ha-icon class="change-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
                              <span class="change-new">${String(t.new)}</span>
                            </span>
                          </div>
                        `)}
                    </div>
                  `:j}
            </div>
          `})}
      </div>
    `}static{this.styles=[ue,r`
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

      .history-entry-header:hover {
        background: var(--primary-background-color);
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
        --mdc-icon-size: 18px;
        color: var(--secondary-text-color);
      }

      .history-details {
        padding: 8px 16px 12px;
        border-top: 1px solid var(--divider-color, #e0e0e0);
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
      }

      .change-new {
        color: var(--primary-color, #03a9f4);
        font-weight: 500;
      }

      .destructive {
        --mdc-theme-primary: var(--error-color, #db4437);
      }

      .change-arrow {
        --mdc-icon-size: 14px;
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
    `]}};e([he({attribute:!1})],Fe.prototype,"hass",void 0),e([he()],Fe.prototype,"entryId",void 0),e([he()],Fe.prototype,"filterDevice",void 0),e([pe()],Fe.prototype,"_entries",void 0),e([pe()],Fe.prototype,"_total",void 0),e([pe()],Fe.prototype,"_loading",void 0),e([pe()],Fe.prototype,"_error",void 0),e([pe()],Fe.prototype,"_expandedEntries",void 0),Fe=e([_e("hm-change-history")],Fe);let je=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this.deviceName="",this._links=[],this._loading=!0,this._error=""}updated(e){(e.has("entryId")||e.has("deviceAddress")||e.has("interfaceId"))&&this.entryId&&this.deviceAddress&&this.interfaceId&&this._fetchLinks()}async _fetchLinks(){this._loading=!0,this._error="";try{this._links=await async function(e,t,i,s){return(await e.callWS({type:"homematicip_local/config/list_device_links",entry_id:t,interface_id:i,device_address:s})).links}(this.hass,this.entryId,this.interfaceId,this.deviceAddress)}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_handleAddLink(){this.dispatchEvent(new CustomEvent("add-link",{detail:{deviceAddress:this.deviceAddress,interfaceId:this.interfaceId},bubbles:!0,composed:!0}))}_handleConfigure(e){this.dispatchEvent(new CustomEvent("configure-link",{detail:{senderAddress:e.sender_address,receiverAddress:e.receiver_address,interfaceId:this.interfaceId,senderDeviceName:e.sender_device_name,senderDeviceModel:e.sender_device_model,senderChannelTypeLabel:e.sender_channel_type_label,receiverDeviceName:e.receiver_device_name,receiverDeviceModel:e.receiver_device_model,receiverChannelTypeLabel:e.receiver_channel_type_label},bubbles:!0,composed:!0}))}async _handleDelete(e){if(await Le(0,{title:this._l("device_links.delete_confirm_title"),text:this._l("device_links.delete_confirm_text",{sender:e.sender_address,receiver:e.receiver_address}),confirmText:this._l("device_links.delete"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t,i,s){return e.callWS({type:"homematicip_local/config/remove_link",entry_id:t,sender_channel_address:i,receiver_channel_address:s})}(this.hass,this.entryId,e.sender_address,e.receiver_address),Ne(this,{message:this._l("device_links.delete_success")}),await this._fetchLinks()}catch{Ne(this,{message:this._l("device_links.delete_failed")})}}_groupByChannel(){const e=new Map;for(const t of this._links){const i=(t.sender_address.startsWith(this.deviceAddress)?t.sender_address:t.receiver_address).split(":").pop()??"";e.has(i)||e.set(i,[]),e.get(i).push(t)}return e}render(){return W`
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

      <ha-button class="add-link-btn" @click=${this._handleAddLink}>
        <ha-icon slot="icon" .icon=${"mdi:plus"}></ha-icon>
        ${this._l("device_links.add_link")}
      </ha-button>

      ${this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:this._error?W`<div class="error">${this._error}</div>`:0===this._links.length?W`<div class="empty-state">${this._l("device_links.empty")}</div>`:this._renderGroupedLinks()}
    `}_renderGroupedLinks(){const e=this._groupByChannel(),t=[...e.keys()].sort((e,t)=>parseInt(e)-parseInt(t));return W`
      ${t.map(t=>{const i=e.get(t);return W`
          <div class="link-channel-group">
            <div class="link-channel-header">
              ${this._l("device_links.channel_group",{channel:t})}
            </div>
            ${i.map(e=>this._renderLinkCard(e))}
          </div>
        `})}
    `}_renderLinkCard(e){const t="outgoing"===e.direction;return W`
      <div class="link-card ${t?"outgoing":"incoming"}">
        <div class="link-direction">
          <span class="direction-badge ${e.direction}">
            ${this._l(t?"device_links.outgoing":"device_links.incoming")}
          </span>
        </div>
        <div class="link-info">
          <div class="link-endpoints">
            <div class="link-endpoint-info">
              <span class="link-device-name">${e.sender_device_name}</span>
              <span class="link-device-detail">
                ${e.sender_device_model}${e.sender_channel_type_label?W` · ${e.sender_channel_type_label}`:j}
              </span>
              <span class="link-endpoint-address">${e.sender_address}</span>
            </div>
            <ha-icon class="link-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
            <div class="link-endpoint-info">
              <span class="link-device-name">${e.receiver_device_name}</span>
              <span class="link-device-detail">
                ${e.receiver_device_model}${e.receiver_channel_type_label?W` · ${e.receiver_channel_type_label}`:j}
              </span>
              <span class="link-endpoint-address">${e.receiver_address}</span>
            </div>
          </div>
          ${e.name?W`<div class="link-name">"${e.name}"</div>`:j}
        </div>
        <div class="link-actions">
          <ha-button outlined @click=${()=>this._handleConfigure(e)}>
            ${this._l("device_links.configure")}
          </ha-button>
          <ha-button outlined class="destructive" @click=${()=>this._handleDelete(e)}>
            ${this._l("device_links.delete")}
          </ha-button>
        </div>
      </div>
    `}static{this.styles=[ue,r`
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

      .link-card {
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
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
      }

      .link-arrow {
        --mdc-icon-size: 20px;
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
        --mdc-theme-primary: var(--error-color, #db4437);
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
    `]}};e([he({attribute:!1})],je.prototype,"hass",void 0),e([he()],je.prototype,"entryId",void 0),e([he()],je.prototype,"interfaceId",void 0),e([he()],je.prototype,"deviceAddress",void 0),e([he()],je.prototype,"deviceName",void 0),e([pe()],je.prototype,"_links",void 0),e([pe()],je.prototype,"_loading",void 0),e([pe()],je.prototype,"_error",void 0),je=e([_e("hm-device-links")],je);let Ke=class extends oe{constructor(){super(...arguments),this.baseValue=0,this.factorValue=0,this.presets=[],this.modified=!1,this._isCustom=!1}_l(e){return Me(this.hass,e)}get _matchesPreset(){return this.presets.some(e=>e.base===this.baseValue&&e.factor===this.factorValue)}_emitChange(e,t,i){this.dispatchEvent(new CustomEvent("value-changed",{detail:{parameterId:e,value:t,currentValue:i},bubbles:!0,composed:!0}))}_handlePresetChange(e){e.stopPropagation();const t=e.detail.value;if(!t||"custom"===t)return void(this._isCustom=!0);this._isCustom=!1;const[i,s]=t.split("-"),a=Number(i),n=Number(s);a===this.baseValue&&n===this.factorValue||(this._emitChange(this.baseParam.id,a,this.baseParam.current_value),this._emitChange(this.factorParam.id,n,this.factorParam.current_value))}_handleBaseChange(e){const t=Number(e.target.value);this._emitChange(this.baseParam.id,t,this.baseParam.current_value)}_handleFactorChange(e){const t=Number(e.target.value);this._emitChange(this.factorParam.id,t,this.factorParam.current_value)}render(){const e=this.baseParam.label.replace(/ Base$/,"").replace(/ Basis$/,""),t=this._matchesPreset,i=this._isCustom&&!t;return W`
      <div class="time-selector">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e} ${this.modified?W`<span class="modified-dot"></span>`:j}
          </div>
          <div class="parameter-control">
            <ha-select
              .value=${t?`${this.baseValue}-${this.factorValue}`:"custom"}
              .options=${[...this.presets.map(e=>({value:`${e.base}-${e.factor}`,label:e.label})),{value:"custom",label:this._l("link_config.custom_time")}]}
              @selected=${this._handlePresetChange}
              @closed=${e=>e.stopPropagation()}
            ></ha-select>
          </div>
        </div>
        ${i||!t?W`
              <div class="custom-time-inputs">
                <label>
                  ${this._l("time_selector.base")}:
                  <input
                    type="number"
                    min="0"
                    max="7"
                    .value=${String(this.baseValue)}
                    @change=${this._handleBaseChange}
                  />
                </label>
                <label>
                  ${this._l("time_selector.factor")}:
                  <input
                    type="number"
                    min="0"
                    max="31"
                    .value=${String(this.factorValue)}
                    @change=${this._handleFactorChange}
                  />
                </label>
              </div>
            `:j}
      </div>
    `}static{this.styles=[ue,r`
      .time-selector {
        margin-bottom: 4px;
      }

      ha-select {
        min-width: 120px;
      }

      .custom-time-inputs {
        display: flex;
        gap: 12px;
        padding: 8px 0 4px;
        margin-left: 16px;
      }

      .custom-time-inputs label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        color: var(--secondary-text-color);
      }

      .custom-time-inputs input[type="number"] {
        width: 60px;
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      @media (max-width: 600px) {
        ha-select {
          width: 100%;
          box-sizing: border-box;
        }
      }
    `]}};e([he({attribute:!1})],Ke.prototype,"hass",void 0),e([he({attribute:!1})],Ke.prototype,"baseParam",void 0),e([he({attribute:!1})],Ke.prototype,"factorParam",void 0),e([he({type:Number})],Ke.prototype,"baseValue",void 0),e([he({type:Number})],Ke.prototype,"factorValue",void 0),e([he({attribute:!1})],Ke.prototype,"presets",void 0),e([he({type:Boolean})],Ke.prototype,"modified",void 0),e([pe()],Ke.prototype,"_isCustom",void 0),Ke=e([_e("hm-time-selector")],Ke);let Ye=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.senderAddress="",this.receiverAddress="",this.senderDeviceName="",this.senderDeviceModel="",this.senderChannelTypeLabel="",this.receiverDeviceName="",this.receiverDeviceModel="",this.receiverChannelTypeLabel="",this._receiverSchema=null,this._senderSchema=null,this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._loading=!0,this._saving=!1,this._error="",this._validationErrors={},this._senderValidationErrors={},this._profiles=null,this._activeProfileId=0,this._selectedProfileId=0,this._activeKeypressTab="short"}updated(e){(e.has("senderAddress")||e.has("receiverAddress")||e.has("entryId"))&&this.entryId&&this.senderAddress&&this.receiverAddress&&this._fetchSchemas()}async _fetchSchemas(){this._loading=!0,this._error="",this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._validationErrors={},this._senderValidationErrors={};try{const[e,t,i]=await Promise.all([xe(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress),xe(this.hass,this.entryId,this.interfaceId,this.receiverAddress,this.senderAddress).catch(()=>null),Ee(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress)]);this._receiverSchema=e,this._senderSchema=t,this._profiles=i?.profiles??null,this._activeProfileId=i?.active_profile_id??0,this._selectedProfileId=this._activeProfileId}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}get _isDirty(){return this._receiverPendingChanges.size>0||this._senderPendingChanges.size>0}get _filteredReceiverSchema(){if(!this._receiverSchema||!this._profiles||0===this._selectedProfileId)return this._receiverSchema;const e=this._profiles.find(e=>e.id===this._selectedProfileId);if(!e)return this._receiverSchema;const t=new Set(e.editable_params),i=this._receiverSchema.sections.map(e=>({...e,parameters:e.parameters.filter(e=>t.has(e.id))})).filter(e=>e.parameters.length>0);return{...this._receiverSchema,sections:i}}get _groupedReceiverParams(){const e=this._filteredReceiverSchema;if(!e)return null;const t=e.sections.flatMap(e=>e.parameters);return t.some(e=>e.keypress_group)?{short:t.filter(e=>"short"===e.keypress_group),long:t.filter(e=>"long"===e.keypress_group),common:t.filter(e=>"common"===e.keypress_group||!e.keypress_group)}:null}_getEffectiveValue(e){return this._receiverPendingChanges.has(e.id)?this._receiverPendingChanges.get(e.id):e.current_value}_isModified(e){return this._receiverPendingChanges.has(e.id)}_emitReceiverChange(e,t){const i=this._findParameter(e),s=i?.current_value;t===s?this._receiverPendingChanges.delete(e):this._receiverPendingChanges.set(e,t),this._receiverPendingChanges=new Map(this._receiverPendingChanges)}_handleProfileChange(e){e.stopPropagation();const t=parseInt(e.detail.value,10);if(Number.isNaN(t)||t===this._selectedProfileId)return;if(this._selectedProfileId=t,0===t||!this._profiles)return;const i=this._profiles.find(e=>e.id===t);if(!i)return;const s=new Map;for(const[e,t]of Object.entries(i.fixed_params)){const i=this._findParameter(e);i&&i.current_value!==t&&s.set(e,t)}for(const[e,t]of Object.entries(i.default_values)){const i=this._findParameter(e);i&&i.current_value!==t&&s.set(e,t)}this._receiverPendingChanges=s}_handleReceiverValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;i===s?this._receiverPendingChanges.delete(t):this._receiverPendingChanges.set(t,i),this._receiverPendingChanges=new Map(this._receiverPendingChanges)}_handleSenderValueChanged(e){const{parameterId:t,value:i,currentValue:s}=e.detail;i===s?this._senderPendingChanges.delete(t):this._senderPendingChanges.set(t,i),this._senderPendingChanges=new Map(this._senderPendingChanges)}_handleDiscard(){this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,this._validationErrors={},this._senderValidationErrors={},this._selectedProfileId=this._activeProfileId}async _handleSave(){if(!this._isDirty||this._saving)return;const e=[...this._receiverPendingChanges.entries(),...this._senderPendingChanges.entries()],t=e.length,i=e.map(([e,t])=>{const i=this._findParameter(e);return`${i?.label??e}: ${i?.current_value??"?"} → ${t}`}).join("\n");if(await Le(0,{title:this._l("link_config.confirm_save_title"),text:`${this._l("link_config.confirm_save_text",{count:t})}\n\n${i}`,confirmText:this._l("common.save"),dismissText:this._l("common.cancel")})){this._saving=!0,this._validationErrors={},this._senderValidationErrors={};try{const e=[];this._receiverPendingChanges.size>0&&e.push($e(this.hass,this.entryId,this.interfaceId,this.senderAddress,this.receiverAddress,Object.fromEntries(this._receiverPendingChanges))),this._senderPendingChanges.size>0&&e.push($e(this.hass,this.entryId,this.interfaceId,this.receiverAddress,this.senderAddress,Object.fromEntries(this._senderPendingChanges))),await Promise.all(e),this._receiverPendingChanges=new Map,this._senderPendingChanges=new Map,Ne(this,{message:this._l("link_config.save_success")}),await this._fetchSchemas()}catch(e){this._error=String(e),Ne(this,{message:this._l("link_config.save_failed")})}finally{this._saving=!1}}}_findParameter(e){for(const t of[this._receiverSchema,this._senderSchema])if(t)for(const i of t.sections){const t=i.parameters.find(t=>t.id===e);if(t)return t}}async _handleBack(){this._isDirty&&!await Le(0,{title:this._l("link_config.unsaved_title"),text:this._l("link_config.unsaved_warning"),confirmText:this._l("link_config.discard"),dismissText:this._l("common.cancel"),destructive:!0})||this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}_hasReceiverParams(){return(this._filteredReceiverSchema?.sections.length??0)>0}_hasSenderParams(){return(this._senderSchema?.sections.length??0)>0}_renderProfileSelector(){if(!this._profiles)return j;const e=this._profiles.find(e=>e.id===this._selectedProfileId),t=e?.description||"";return W`
      <div class="profile-selector">
        <ha-select
          .label=${this._l("link_config.profile")}
          .value=${String(this._selectedProfileId)}
          .options=${this._profiles.map(e=>({value:String(e.id),label:e.name}))}
          @selected=${this._handleProfileChange}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
        ${t?W`<p class="profile-description">${t}</p>`:j}
      </div>
    `}_renderParamList(e){const t=new Map,i=[];for(const s of e)if(s.time_pair_id&&s.id.toUpperCase().endsWith("_TIME_BASE")){const e=t.get(s.time_pair_id)??{};e.base=s,t.set(s.time_pair_id,e)}else if(s.time_pair_id&&s.id.toUpperCase().endsWith("_TIME_FACTOR")){const e=t.get(s.time_pair_id)??{};e.factor=s,t.set(s.time_pair_id,e)}else s.hidden_by_default&&0!==this._selectedProfileId||i.push(s);return W`
      ${[...t.entries()].map(([,e])=>e.base&&e.factor?W`
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
      ${i.map(e=>e.display_as_percent&&e.has_last_value?this._renderLevelParam(e):W`
              <hm-form-parameter
                .hass=${this.hass}
                .parameter=${e}
                .value=${this._getEffectiveValue(e)}
                .modified=${this._isModified(e)}
                @value-changed=${this._handleReceiverValueChanged}
              ></hm-form-parameter>
            `)}
    `}_renderLevelParam(e){const t=this._getEffectiveValue(e),i=t>1,s=i?100:Math.round(100*t);return W`
      <div class="level-param">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e.label}
            ${this._isModified(e)?W`<span class="modified-dot"></span>`:j}
          </div>
          <div class="parameter-control level-controls">
            <label class="last-value-toggle">
              <ha-checkbox
                .checked=${i}
                @change=${t=>{this._emitReceiverChange(e.id,t.target.checked?1.005:1)}}
              ></ha-checkbox>
              ${this._l("link_config.last_value")}
            </label>
            ${i?j:W`
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
    `}_renderReceiverParams(){const e=this._groupedReceiverParams;if(e){const t=e.short.length>0,i=e.long.length>0,s=t&&i;return W`
        <div class="param-section">
          <h3>${this._l("link_config.receiver_params")}</h3>
          ${s?W`
                <div class="keypress-tabs">
                  <div
                    class="tab ${"short"===this._activeKeypressTab?"active":""}"
                    @click=${()=>{this._activeKeypressTab="short"}}
                  >
                    ${this._l("link_config.short_keypress")}
                  </div>
                  <div
                    class="tab ${"long"===this._activeKeypressTab?"active":""}"
                    @click=${()=>{this._activeKeypressTab="long"}}
                  >
                    ${this._l("link_config.long_keypress")}
                  </div>
                </div>
                <div class="keypress-params">
                  ${this._renderParamList("short"===this._activeKeypressTab?e.short:e.long)}
                </div>
              `:t?this._renderParamList(e.short):i?this._renderParamList(e.long):j}
          ${e.common.length>0?W` <div class="common-params">${this._renderParamList(e.common)}</div> `:j}
        </div>
      `}return W`
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
    `}render(){return this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:!this._error||this._receiverSchema||this._senderSchema?W`
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
            ${this.senderDeviceName?W`<span class="link-device-name">${this.senderDeviceName}</span>`:j}
            ${this.senderDeviceModel||this.senderChannelTypeLabel?W`<span class="link-device-detail">
                  ${this.senderDeviceModel}${this.senderChannelTypeLabel?W` &middot; ${this.senderChannelTypeLabel}`:j}
                </span>`:j}
            <span class="link-address">${this.senderAddress}</span>
          </div>
          <ha-icon class="link-direction-arrow" .icon=${"mdi:arrow-right"}></ha-icon>
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.receiver")}</span>
            ${this.receiverDeviceName?W`<span class="link-device-name">${this.receiverDeviceName}</span>`:j}
            ${this.receiverDeviceModel||this.receiverChannelTypeLabel?W`<span class="link-device-detail">
                  ${this.receiverDeviceModel}${this.receiverChannelTypeLabel?W` &middot; ${this.receiverChannelTypeLabel}`:j}
                </span>`:j}
            <span class="link-address">${this.receiverAddress}</span>
          </div>
        </div>
      </div>

      ${this._error?W`<div class="error">${this._error}</div>`:j}
      ${this._renderProfileSelector()}
      ${this._hasReceiverParams()?this._renderReceiverParams():j}
      ${this._hasSenderParams()?W`
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
      ${this._hasReceiverParams()||this._hasSenderParams()?j:W`<div class="empty-state">${this._l("link_config.no_params")}</div>`}

      <div class="action-bar">
        <ha-button
          outlined
          @click=${this._handleDiscard}
          .disabled=${!this._isDirty||this._saving}
        >
          ${this._l("link_config.discard")}
        </ha-button>
        <ha-button raised @click=${this._handleSave} .disabled=${!this._isDirty||this._saving}>
          ${this._l(this._saving?"channel_config.saving":"common.save")}
        </ha-button>
      </div>
    `:W`<div class="error">${this._error}</div>`}static{this.styles=[ue,r`
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
      }

      .link-direction-arrow {
        --mdc-icon-size: 24px;
        color: var(--primary-color, #03a9f4);
        flex-shrink: 0;
      }

      .profile-selector {
        margin: 16px 0;
        padding: 12px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 8px;
      }

      .profile-selector ha-select {
        width: 100%;
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

      .tab:hover {
        color: var(--primary-text-color);
      }

      .tab.active {
        color: var(--primary-color, #03a9f4);
        border-bottom-color: var(--primary-color, #03a9f4);
      }

      .keypress-params {
        padding: 4px 0;
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
    `]}};e([he({attribute:!1})],Ye.prototype,"hass",void 0),e([he()],Ye.prototype,"entryId",void 0),e([he()],Ye.prototype,"interfaceId",void 0),e([he()],Ye.prototype,"senderAddress",void 0),e([he()],Ye.prototype,"receiverAddress",void 0),e([he()],Ye.prototype,"senderDeviceName",void 0),e([he()],Ye.prototype,"senderDeviceModel",void 0),e([he()],Ye.prototype,"senderChannelTypeLabel",void 0),e([he()],Ye.prototype,"receiverDeviceName",void 0),e([he()],Ye.prototype,"receiverDeviceModel",void 0),e([he()],Ye.prototype,"receiverChannelTypeLabel",void 0),e([pe()],Ye.prototype,"_receiverSchema",void 0),e([pe()],Ye.prototype,"_senderSchema",void 0),e([pe()],Ye.prototype,"_receiverPendingChanges",void 0),e([pe()],Ye.prototype,"_senderPendingChanges",void 0),e([pe()],Ye.prototype,"_loading",void 0),e([pe()],Ye.prototype,"_saving",void 0),e([pe()],Ye.prototype,"_error",void 0),e([pe()],Ye.prototype,"_validationErrors",void 0),e([pe()],Ye.prototype,"_senderValidationErrors",void 0),e([pe()],Ye.prototype,"_profiles",void 0),e([pe()],Ye.prototype,"_activeProfileId",void 0),e([pe()],Ye.prototype,"_selectedProfileId",void 0),e([pe()],Ye.prototype,"_activeKeypressTab",void 0),Ye=e([_e("hm-link-config")],Ye);let Ze=class extends oe{constructor(){super(...arguments),this.entryId="",this.interfaceId="",this.deviceAddress="",this._step="select-channel",this._device=null,this._selectedChannel="",this._selectedRole="sender",this._selectedPeer="",this._linkName="",this._linkableChannels=[],this._filteredChannels=[],this._searchQuery="",this._loading=!1,this._error=""}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this.deviceAddress&&this._fetchDevice()}async _fetchDevice(){this._loading=!0;try{const e=await ge(this.hass,this.entryId);this._device=e.find(e=>e.address===this.deviceAddress)??null}catch(e){this._error=String(e)}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}_handleBack(){if("select-peer"===this._step)return this._step="select-channel",this._selectedPeer="",this._linkableChannels=[],this._filteredChannels=[],void(this._searchQuery="");"confirm"!==this._step?this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0})):this._step="select-peer"}_getLinkableChannels(){return this._device?this._device.channels.filter(e=>!e.address.endsWith(":0")&&e.paramset_keys.includes("LINK")):[]}_handleSelectChannel(e){this._selectedChannel=e}async _handleNextToSelectPeer(){this._selectedChannel&&(this._step="select-peer",await this._fetchLinkableChannels())}async _fetchLinkableChannels(){this._loading=!0,this._error="",this._linkableChannels=[],this._filteredChannels=[],this._searchQuery="";try{this._linkableChannels=await async function(e,t,i,s,a){return(await e.callWS({type:"homematicip_local/config/get_linkable_channels",entry_id:t,interface_id:i,channel_address:s,role:a})).channels}(this.hass,this.entryId,this.interfaceId,this._selectedChannel,this._selectedRole),this._filteredChannels=this._linkableChannels}catch(e){this._error=String(e)}finally{this._loading=!1}}async _handleRoleChange(e){this._selectedRole=e,this._selectedPeer="",await this._fetchLinkableChannels()}_handleSearchInput(e){const t=e.target.value.toLowerCase();this._searchQuery=t,this._filteredChannels=t?this._linkableChannels.filter(e=>e.address.toLowerCase().includes(t)||e.device_name.toLowerCase().includes(t)||e.device_model.toLowerCase().includes(t)||e.channel_type.toLowerCase().includes(t)):this._linkableChannels}_handleSelectPeer(e){this._selectedPeer=e}_handleNextToConfirm(){this._selectedPeer&&(this._linkName="",this._step="confirm")}async _handleCreate(){this._loading=!0;try{const e="sender"===this._selectedRole?this._selectedChannel:this._selectedPeer,t="sender"===this._selectedRole?this._selectedPeer:this._selectedChannel;await async function(e,t,i,s,a){return e.callWS({type:"homematicip_local/config/add_link",entry_id:t,sender_channel_address:i,receiver_channel_address:s,...a&&{name:a}})}(this.hass,this.entryId,e,t,this._linkName||void 0),Ne(this,{message:this._l("add_link.create_success")}),this.dispatchEvent(new CustomEvent("link-created",{bubbles:!0,composed:!0}))}catch{Ne(this,{message:this._l("add_link.create_failed")})}finally{this._loading=!1}}render(){return this._loading&&!this._device?W`<div class="loading">${this._l("common.loading")}</div>`:W`
      <ha-icon-button
        class="back-button"
        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
        @click=${this._handleBack}
        .label=${this._l("select-channel"===this._step?"common.back":"add_link.back")}
      ></ha-icon-button>

      <div class="wizard-header">
        <h2>${this._l("add_link.title")}</h2>
      </div>

      ${this._error?W`<div class="error">${this._error}</div>`:j}
      ${"select-channel"===this._step?this._renderStepChannel():"select-peer"===this._step?this._renderStepPeer():this._renderStepConfirm()}
    `}_renderStepChannel(){const e=this._getLinkableChannels();return W`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_channel")}</div>
        <div class="step-description">${this._l("add_link.select_channel")}</div>

        <div class="radio-list">
          ${0===e.length?W`<div class="empty-state">${this._l("add_link.no_compatible")}</div>`:e.map(e=>{const t=e.address.split(":").pop()??"",i=this._selectedChannel===e.address;return W`
                  <div
                    class="radio-option ${i?"selected":""}"
                    @click=${()=>this._handleSelectChannel(e.address)}
                  >
                    <ha-radio name="channel" .checked=${i}></ha-radio>
                    <div class="radio-content">
                      <div class="radio-title">
                        ${this._l("device_detail.channel")} ${t}: ${e.channel_type_label}
                      </div>
                      <div class="radio-subtitle">${e.address}</div>
                    </div>
                  </div>
                `})}
        </div>

        ${e.length>0?W`
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
    `}_renderStepPeer(){return W`
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

        ${this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:W`
              <div class="search-box">
                <input
                  type="text"
                  .value=${this._searchQuery}
                  @input=${this._handleSearchInput}
                  placeholder="${this._l("add_link.search_devices")}"
                />
              </div>

              <div class="radio-list">
                ${0===this._filteredChannels.length?W`<div class="empty-state">${this._l("add_link.no_compatible")}</div>`:this._filteredChannels.map(e=>{const t=this._selectedPeer===e.address;return W`
                        <div
                          class="radio-option ${t?"selected":""}"
                          @click=${()=>this._handleSelectPeer(e.address)}
                        >
                          <ha-radio name="peer" .checked=${t}></ha-radio>
                          <div class="radio-content">
                            <div class="radio-title">${e.device_name} (${e.device_model})</div>
                            <div class="radio-subtitle">
                              ${e.address} — ${e.channel_type_label}
                            </div>
                          </div>
                        </div>
                      `})}
              </div>

              ${this._filteredChannels.length>0?W`
                    <div class="wizard-actions">
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
    `}_renderStepConfirm(){const e="sender"===this._selectedRole?this._selectedChannel:this._selectedPeer,t="sender"===this._selectedRole?this._selectedPeer:this._selectedChannel,i=this._resolveName(e),s=this._resolveName(t);return W`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_confirm")}</div>

        <div class="link-summary">
          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l("link_config.sender")}</div>
            <div class="link-endpoint-address">${e}</div>
            <div class="link-endpoint-name">${i}</div>
          </div>

          <ha-icon class="link-direction-arrow" .icon=${"mdi:arrow-right"}></ha-icon>

          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l("link_config.receiver")}</div>
            <div class="link-endpoint-address">${t}</div>
            <div class="link-endpoint-name">${s}</div>
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
          <ha-button raised .disabled=${this._loading} @click=${this._handleCreate}>
            ${this._l(this._loading?"common.loading":"add_link.create")}
          </ha-button>
        </div>
      </div>
    `}_resolveName(e){if(!this._device)return e;if(e.startsWith(this.deviceAddress))return this._device.name||this.deviceAddress;const t=this._linkableChannels.find(t=>t.address===e);return t?`${t.device_name} (${t.device_model})`:e}static{this.styles=[ue,r`
      .wizard-header {
        margin-bottom: 16px;
      }

      .wizard-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
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

      .radio-option:hover {
        border-color: var(--primary-color, #03a9f4);
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
        --mdc-icon-size: 28px;
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
    `]}};function Ge(e){return t=>(customElements.get(e)||customElements.define(e,t),t)}e([he({attribute:!1})],Ze.prototype,"hass",void 0),e([he()],Ze.prototype,"entryId",void 0),e([he()],Ze.prototype,"interfaceId",void 0),e([he()],Ze.prototype,"deviceAddress",void 0),e([pe()],Ze.prototype,"_step",void 0),e([pe()],Ze.prototype,"_device",void 0),e([pe()],Ze.prototype,"_selectedChannel",void 0),e([pe()],Ze.prototype,"_selectedRole",void 0),e([pe()],Ze.prototype,"_selectedPeer",void 0),e([pe()],Ze.prototype,"_linkName",void 0),e([pe()],Ze.prototype,"_linkableChannels",void 0),e([pe()],Ze.prototype,"_filteredChannels",void 0),e([pe()],Ze.prototype,"_searchQuery",void 0),e([pe()],Ze.prototype,"_loading",void 0),e([pe()],Ze.prototype,"_error",void 0),Ze=e([_e("hm-add-link")],Ze);let qe=class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,i){this._$Ct=e,this._$AM=t,this._$Ci=i}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}};const{I:Qe}=ae,Je=e=>e,Xe=()=>document.createComment(""),et=(e,t,i)=>{const s=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===i){const t=s.insertBefore(Xe(),a),n=s.insertBefore(Xe(),a);i=new Qe(t,n,e,e.options)}else{const t=i._$AB.nextSibling,n=i._$AM,r=n!==e;if(r){let t;i._$AQ?.(e),i._$AM=e,void 0!==i._$AP&&(t=e._$AU)!==n._$AU&&i._$AP(t)}if(t!==a||r){let e=i._$AA;for(;e!==t;){const t=Je(e).nextSibling;Je(s).insertBefore(e,a),e=t}}}return i},tt=(e,t,i=e)=>(e._$AI(t,i),e),it={},st=(e,t=it)=>e._$AH=t,at=e=>{e._$AR(),e._$AA.remove()},nt=(e,t,i)=>{const s=new Map;for(let a=t;a<=i;a++)s.set(e[a],a);return s},rt=(e=>(...t)=>({_$litDirective$:e,values:t}))(class extends qe{constructor(e){if(super(e),2!==e.type)throw Error("repeat() can only be used in text expressions")}dt(e,t,i){let s;void 0===i?i=t:void 0!==t&&(s=t);const a=[],n=[];let r=0;for(const t of e)a[r]=s?s(t,r):r,n[r]=i(t,r),r++;return{values:n,keys:a}}render(e,t,i){return this.dt(e,t,i).values}update(e,[t,i,s]){const a=(e=>e._$AH)(e),{values:n,keys:r}=this.dt(t,i,s);if(!Array.isArray(a))return this.ut=r,n;const o=this.ut??=[],d=[];let l,c,h=0,p=a.length-1,_=0,u=n.length-1;for(;h<=p&&_<=u;)if(null===a[h])h++;else if(null===a[p])p--;else if(o[h]===r[_])d[_]=tt(a[h],n[_]),h++,_++;else if(o[p]===r[u])d[u]=tt(a[p],n[u]),p--,u--;else if(o[h]===r[u])d[u]=tt(a[h],n[u]),et(e,d[u+1],a[h]),h++,u--;else if(o[p]===r[_])d[_]=tt(a[p],n[_]),et(e,a[h],a[p]),p--,_++;else if(void 0===l&&(l=nt(r,_,u),c=nt(o,h,p)),l.has(o[h]))if(l.has(o[p])){const t=c.get(r[_]),i=void 0!==t?a[t]:null;if(null===i){const t=et(e,a[h]);tt(t,n[_]),d[_]=t}else d[_]=tt(i,n[_]),et(e,a[h],i),a[t]=null;_++}else at(a[p]),p--;else at(a[h]),h++;for(;_<=u;){const t=et(e,d[u+1]);tt(t,n[_]),d[_++]=t}for(;h<=p;){const e=a[h++];null!==e&&at(e)}return this.ut=r,st(e,d),F}}),ot=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"],dt=["fixed_time","astro","fixed_if_before_astro","astro_if_before_fixed","fixed_if_after_astro","astro_if_after_fixed","earliest","latest"],lt={switch:{levelType:"binary",hasLevel2:!1,hasDuration:!0,hasRampTime:!1},light:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!0},cover:{levelType:"percentage",hasLevel2:!0,hasDuration:!1,hasRampTime:!1},valve:{levelType:"percentage",hasLevel2:!1,hasDuration:!0,hasRampTime:!1}},ct=["ms","s","min","h"];function ht(e){const[t,i]=e.split(":").map(Number);return 60*t+i}function pt(e){const t=e%60;return`${Math.floor(e/60).toString().padStart(2,"0")}:${t.toString().padStart(2,"0")}`}function _t(e,t="24"){if("24"===t)return e;const[i,s]=e.split(":");let a=parseInt(i,10);if(24===a)return"12:00 AM";const n=a>=12?"PM":"AM";return 0===a?a=12:a>12&&(a-=12),`${a}:${s||"00"} ${n}`}function ut(e){return e<10?"#2b9af9":e<14?"#40c4ff":e<17?"#26c6da":e<19?"#66bb6a":e<21?"#9ccc65":e<23?"#ffb74d":e<25?"#ff8100":"#f4511e"}function vt(e){const{base_temperature:t,periods:i}=e,s=[],a=[...i].sort((e,t)=>ht(e.starttime)-ht(t.starttime));for(let e=0;e<a.length;e++){const t=a[e];s.push({startTime:t.starttime,startMinutes:ht(t.starttime),endTime:t.endtime,endMinutes:ht(t.endtime),temperature:t.temperature,slot:e+1})}return{blocks:s,baseTemperature:t}}function mt(e,t){const i=[],s=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of s)i.push({starttime:e.startTime,endtime:e.endTime,temperature:e.temperature});return{base_temperature:t,periods:i}}function gt(e){if(0===e.length)return[];const t=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),i=[];let s={...t[0]};for(let e=1;e<t.length;e++){const a=t[e];s.endMinutes===a.startMinutes&&s.temperature===a.temperature?s={...s,endTime:a.endTime,endMinutes:a.endMinutes}:(i.push(s),s={...a})}return i.push(s),i.map((e,t)=>({...e,slot:t+1}))}function ft(e,t){if(0===e.length)return[{startTime:"00:00",startMinutes:0,endTime:"24:00",endMinutes:1440,temperature:t,slot:1}];const i=[...e].sort((e,t)=>e.startMinutes-t.startMinutes),s=[];let a=0;for(const e of i)e.startMinutes>a&&s.push({startTime:pt(a),startMinutes:a,endTime:e.startTime,endMinutes:e.startMinutes,temperature:t,slot:s.length+1}),s.push({...e,slot:s.length+1}),a=e.endMinutes;return a<1440&&s.push({startTime:pt(a),startMinutes:a,endTime:"24:00",endMinutes:1440,temperature:t,slot:s.length+1}),gt(s)}function yt(e){return[...e].sort((e,t)=>e.startMinutes-t.startMinutes).map((e,t)=>({...e,slot:t+1}))}function bt(e){return Boolean(Array.isArray(e.weekdays)&&e.weekdays.length>0&&Array.isArray(e.target_channels)&&e.target_channels.length>0)}function xt(e){return"fixed_time"!==e}const $t=/^(\d+(?:\.\d+)?)\s*(ms|s|min|h)$/;function kt(e){const t=e.trim().match($t);return t?{value:parseFloat(t[1]),unit:t[2]}:null}function wt(e,t){return`${e}${t}`}function St(e){return $t.test(e.trim())}function Ct(e){const t={weekdays:e.weekdays,time:e.time,target_channels:e.target_channels,level:e.level};return"fixed_time"!==e.condition&&(t.condition=e.condition),null!==e.astro_type&&(t.astro_type=e.astro_type),0!==e.astro_offset_minutes&&(t.astro_offset_minutes=e.astro_offset_minutes),null!==e.level_2&&(t.level_2=e.level_2),null!==e.duration&&(t.duration=e.duration),null!==e.ramp_time&&(t.ramp_time=e.ramp_time),t}function Et(e){const t={};for(const[i,s]of Object.entries(e))t[i]=Ct(s);return t}function At(e,t=5,i=30.5){const{base_temperature:s,periods:a}=e;if(s<t||s>i)return{key:"temperatureOutOfRange",params:{block:"base",min:`${t}`,max:`${i}`}};let n=0;for(let e=0;e<a.length;e++){const s=a[e];if(!s.starttime||!s.endtime||void 0===s.temperature)return{key:"slotMissingValues",params:{slot:`${e+1}`}};const r=ht(s.starttime),o=ht(s.endtime);if(o<=r)return{key:"blockEndBeforeStart",params:{block:`${e+1}`}};if(r<n)return{key:"slotTimeBackwards",params:{slot:`${e+1}`,time:s.starttime}};if(s.temperature<t||s.temperature>i)return{key:"temperatureOutOfRange",params:{block:`${e+1}`,min:`${t}`,max:`${i}`}};n=o}return null}const It=r`
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
    --mdc-icon-button-size: 28px;
    --mdc-icon-size: 16px;
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
      --mdc-icon-button-size: 24px;
      --mdc-icon-size: 14px;
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
      --mdc-icon-button-size: 20px;
      --mdc-icon-size: 12px;
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
`;var Dt=function(e,t,i,s){var a,n=arguments.length,r=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(r=(n<3?a(r):n>3?a(t,i,r):a(t,i))||r);return n>3&&r&&Object.defineProperty(t,i,r),r};let Tt=class extends oe{constructor(){super(...arguments),this.editable=!1,this.showTemperature=!0,this.showGradient=!1,this.temperatureUnit="°C",this.hourFormat="24",this.editorOpen=!1,this._currentTimePercent=0,this._currentTimeMinutes=0}connectedCallback(){super.connectedCallback(),this._updateCurrentTime(),this._timeUpdateInterval=window.setInterval(()=>{this._updateCurrentTime()},6e4)}disconnectedCallback(){super.disconnectedCallback(),void 0!==this._timeUpdateInterval&&(clearInterval(this._timeUpdateInterval),this._timeUpdateInterval=void 0)}willUpdate(e){super.willUpdate(e)}_updateCurrentTime(){const e=new Date,t=60*e.getHours()+e.getMinutes();this._currentTimePercent=t/1440*100,this._currentTimeMinutes=t;const i=e.getDay();this._currentWeekday=["SUNDAY","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY"][i]}_isBlockActive(e,t){return!(!this._currentWeekday||this._currentWeekday!==e)&&this._currentTimeMinutes>=t.startMinutes&&this._currentTimeMinutes<t.endMinutes}_getTimeLabels(){const e=[];for(let t=0;t<=24;t+=3){const i=`${t.toString().padStart(2,"0")}:00`;e.push({hour:t,label:_t(i,this.hourFormat),position:t/24*100})}return e}_formatTimeDisplay(e){return _t(e,this.hourFormat)}_getBaseTemperature(e){if(this.scheduleData){const t=this.scheduleData[e];if(t){const{baseTemperature:e}=vt(t);return e}}return 20}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=vt(t);return i}return[]}_getWeekdayLabel(e){return this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_handleWeekdayClick(e){this.editable&&this.dispatchEvent(new CustomEvent("weekday-click",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handleCopy(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("copy-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}_handlePaste(e,t){t.stopPropagation(),this.dispatchEvent(new CustomEvent("paste-schedule",{detail:{weekday:e},bubbles:!0,composed:!0}))}render(){return this.scheduleData?W`
      <div class="schedule-container">
        <!-- Empty cell for time-axis header alignment -->
        <div class="time-axis-header"></div>

        <!-- Weekday headers -->
        ${rt(ot,e=>`header-${e}`,e=>{const t=this.copiedWeekday===e;return W`
              <div class="weekday-header">
                <div class="weekday-label">${this._getWeekdayLabel(e)}</div>
                ${this.editable?W`
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
          ${rt(this._getTimeLabels(),e=>e.hour,e=>W`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `)}
        </div>

        <!-- Time blocks content wrapper (for correct indicator positioning) -->
        <div class="schedule-content">
          ${rt(ot,e=>`${e}-${this.currentProfile}-${this.scheduleDataHash}`,e=>{const t=this._getParsedBlocks(e),i=this._getBaseTemperature(e),s=ft(t,i);return W`
                <div
                  class="time-blocks ${this.editable?"editable":""}"
                  @click=${()=>this._handleWeekdayClick(e)}
                >
                  ${rt(s,e=>`${e.slot}-${e.startMinutes}-${this.currentProfile}`,(a,n)=>{const r=this._isBlockActive(e,a),o=a.temperature===i&&!t.some(e=>e.startMinutes===a.startMinutes&&e.endMinutes===a.endMinutes);let d;if(o)d="background-color: var(--secondary-background-color, #e0e0e0);";else if(this.showGradient){d=`background: ${function(e,t,i){const s=ut(e);return null===t&&null===i?s:null!==t&&null===i?`linear-gradient(to bottom, ${ut(t)}, ${s})`:null===t&&null!==i?`linear-gradient(to bottom, ${s}, ${ut(i)})`:`linear-gradient(to bottom, ${ut(t)}, ${s} 50%, ${ut(i)})`}(a.temperature,n>0?s[n-1].temperature:null,n<s.length-1?s[n+1].temperature:null)};`}else d=`background-color: ${ut(a.temperature)};`;return W`
                        <div
                          class="time-block ${r?"active":""} ${o?"base-temp-block":""}"
                          style="
                              height: ${(a.endMinutes-a.startMinutes)/1440*100}%;
                              ${d}
                            "
                        >
                          ${this.showTemperature?W`<span class="temperature"
                                >${a.temperature.toFixed(1)}°</span
                              >`:""}
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
              `})}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${this.editorOpen?"":W`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`}
        </div>
      </div>

      ${this.editable?W`<div class="hint">${this.translations?.clickToEdit??""}</div>`:""}
    `:W``}static{this.styles=It}};Dt([he({attribute:!1})],Tt.prototype,"scheduleData",void 0),Dt([he({type:Boolean})],Tt.prototype,"editable",void 0),Dt([he({type:Boolean})],Tt.prototype,"showTemperature",void 0),Dt([he({type:Boolean})],Tt.prototype,"showGradient",void 0),Dt([he({type:String})],Tt.prototype,"temperatureUnit",void 0),Dt([he({type:String})],Tt.prototype,"hourFormat",void 0),Dt([he({attribute:!1})],Tt.prototype,"translations",void 0),Dt([he({type:String})],Tt.prototype,"copiedWeekday",void 0),Dt([he({type:Boolean})],Tt.prototype,"editorOpen",void 0),Dt([he({type:String})],Tt.prototype,"currentProfile",void 0),Dt([he({type:String})],Tt.prototype,"scheduleDataHash",void 0),Dt([pe()],Tt.prototype,"_currentTimePercent",void 0),Dt([pe()],Tt.prototype,"_currentTimeMinutes",void 0),Dt([pe()],Tt.prototype,"_currentWeekday",void 0),Tt=Dt([Ge("hmip-schedule-grid")],Tt);const Mt=r`
  :host {
    display: block;
  }

  /* Dialog styles */
  ha-dialog {
    --mdc-dialog-max-width: 90vw;
    --mdc-dialog-max-height: 90vh;
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
    display: none;
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
    --mdc-icon-button-size: 36px;
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
    --mdc-typography-button-font-size: 12px;
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
    --mdc-icon-button-size: 32px;
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
    --mdc-theme-primary: var(--primary-color);
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
      --mdc-dialog-max-width: 100vw;
      --mdc-dialog-max-height: 100vh;
    }

    .dialog-content {
      max-height: calc(100vh - 150px);
    }

    .editor-header h3 {
      font-size: 18px;
    }

    .editor-actions ha-icon-button {
      --mdc-icon-button-size: 44px;
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
`;var Pt=function(e,t,i,s){var a,n=arguments.length,r=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(r=(n<3?a(r):n>3?a(t,i,r):a(t,i))||r);return n>3&&r&&Object.defineProperty(t,i,r),r};let Lt=class extends oe{constructor(){super(),this.open=!1,this.minTemp=5,this.maxTemp=30.5,this.tempStep=.5,this.temperatureUnit="°C",this.hourFormat="24",this._validationWarnings=[],this._historyStack=[],this._historyIndex=-1,this._keyDownHandler=this._handleKeyDown.bind(this)}connectedCallback(){super.connectedCallback(),window.addEventListener("keydown",this._keyDownHandler)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("keydown",this._keyDownHandler)}willUpdate(e){if(super.willUpdate(e),(e.has("open")||e.has("weekday"))&&this.open&&this.weekday){const t=e.get("open"),i=e.get("weekday");(!t&&this.open||this.open&&i!==this.weekday)&&this._initializeEditor(this.weekday)}}_initializeEditor(e){this._editingWeekday=e,this._editingBlocks=this._getParsedBlocks(e),this._editingSlotIndex=void 0,this._editingSlotData=void 0;const t=this.scheduleData?.[e];if(t){const{baseTemperature:e}=vt(t);this._editingBaseTemperature=e}else this._editingBaseTemperature=20;this._historyStack=[JSON.parse(JSON.stringify(this._editingBlocks))],this._historyIndex=0,this._updateValidationWarnings()}_getParsedBlocks(e){if(this.scheduleData){const t=this.scheduleData[e];if(!t)return[];const{blocks:i}=vt(t);return i}return[]}_getWeekdayLabel(e,t){return"long"===t?this.translations?.weekdayLongLabels[e]??e:this.translations?.weekdayShortLabels[e]??e.slice(0,2)}_formatTimeDisplay(e){return _t(e,this.hourFormat)}_formatValidationParams(e){if(!e)return{};const t={};for(const[i,s]of Object.entries(e))"weekday"===i&&ot.includes(s)?t.weekday=this._getWeekdayLabel(s,"long"):t[i]=s;return t}_translateValidationMessage(e){const t=this.translations?.validationMessages[e.key]||e.key,i=this._formatValidationParams(e.params);e.nested&&(i.details=this._translateValidationMessage(e.nested));let s=t;for(const[e,t]of Object.entries(i))s=s.replace(`{${e}}`,t);return s}_saveHistoryState(){if(!this._editingBlocks)return;const e=JSON.parse(JSON.stringify(this._editingBlocks));this._historyStack=this._historyStack.slice(0,this._historyIndex+1),this._historyStack.push(e),this._historyIndex++,this._historyStack.length>50&&(this._historyStack.shift(),this._historyIndex--)}_undo(){this._historyIndex<=0||(this._historyIndex--,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_redo(){this._historyIndex>=this._historyStack.length-1||(this._historyIndex++,this._editingBlocks=JSON.parse(JSON.stringify(this._historyStack[this._historyIndex])),this._updateValidationWarnings())}_canUndo(){return this._historyIndex>0}_canRedo(){return this._historyIndex<this._historyStack.length-1}_handleKeyDown(e){if(!this.open||!this._editingWeekday||!this._editingBlocks)return;const t=e.ctrlKey||e.metaKey;t&&"z"===e.key&&!e.shiftKey?(e.preventDefault(),this._undo()):t&&("y"===e.key||"z"===e.key&&e.shiftKey)&&(e.preventDefault(),this._redo())}_updateValidationWarnings(){this._validationWarnings=this._editingBlocks?function(e,t=5,i=30.5){const s=[];if(0===e.length)return s;for(let t=0;t<e.length-1;t++){const i=e[t];i.endMinutes<i.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${t+1}`}}),i.endMinutes===i.startMinutes&&s.push({key:"blockZeroDuration",params:{block:`${t+1}`}})}const a=e[e.length-1];return a.endMinutes<a.startMinutes&&s.push({key:"blockEndBeforeStart",params:{block:`${e.length}`}}),e.forEach((e,a)=>{(e.startMinutes<0||e.startMinutes>1440)&&s.push({key:"invalidStartTime",params:{block:`${a+1}`}}),(e.endMinutes<0||e.endMinutes>1440)&&s.push({key:"invalidEndTime",params:{block:`${a+1}`}}),(e.temperature<t||e.temperature>i)&&s.push({key:"temperatureOutOfRange",params:{block:`${a+1}`,min:`${t}`,max:`${i}`}})}),s}(this._editingBlocks,this.minTemp,this.maxTemp):[]}_startSlotEdit(e){if(!this._editingBlocks||e<0||e>=this._editingBlocks.length)return;const t=this._editingBlocks[e];this._editingSlotIndex=e,this._editingSlotData={startTime:t.startTime,endTime:t.endTime,temperature:t.temperature}}_startSlotEditFromDisplay(e,t){if(!this._editingBlocks)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);-1!==s&&this._startSlotEdit(s)}_cancelSlotEdit(){this._editingSlotIndex=void 0,this._editingSlotData=void 0}_saveSlotEdit(){if(void 0===this._editingSlotIndex||!this._editingSlotData||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=this._editingSlotIndex,{startTime:t,endTime:i,temperature:s}=this._editingSlotData,a={startTime:t,startMinutes:ht(t),endTime:i,endMinutes:ht(i),temperature:s,slot:e+1},n=this._editingBlocks.filter((t,i)=>i!==e),r=function(e,t){const i=[],s=t.startMinutes,a=t.endMinutes,n=[...e].sort((e,t)=>e.startMinutes-t.startMinutes);for(const e of n){const t=e.startMinutes,n=e.endMinutes;n<=s||t>=a?i.push(e):(t<s&&i.push({...e,endTime:pt(s),endMinutes:s,slot:i.length+1}),n>a&&i.push({...e,startTime:pt(a),startMinutes:a,slot:i.length+1}))}i.push({...t,slot:i.length+1});const r=i.sort((e,t)=>e.startMinutes-t.startMinutes);return gt(r)}(n,a),o=gt(yt(r));this._saveHistoryState(),this._editingBlocks=o,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._updateValidationWarnings()}_addNewSlot(){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;if(this._editingBlocks.length>=12)return;let e=0,t=60;if(this._editingBlocks.length>0){const i=yt(this._editingBlocks),s=i[i.length-1];if(s.endMinutes<1440)e=s.endMinutes,t=Math.min(e+60,1440);else{let s=!1;for(let a=0;a<i.length;a++){const n=0===a?0:i[a-1].endMinutes;if(i[a].startMinutes>n){e=n,t=i[a].startMinutes,s=!0;break}}if(!s)return}}const i=Math.min(this._editingBaseTemperature+2,this.maxTemp),s={startTime:pt(e),startMinutes:e,endTime:pt(t),endMinutes:t,temperature:i,slot:this._editingBlocks.length+1};this._saveHistoryState();const a=yt([...this._editingBlocks,s]);this._editingBlocks=a;const n=a.findIndex(i=>i.startMinutes===e&&i.endMinutes===t);n>=0&&this._startSlotEdit(n),this._updateValidationWarnings()}_removeTimeBlockByIndex(e,t){if(!this._editingBlocks||void 0===this._editingBaseTemperature)return;const i=t[e],s=this._editingBlocks.findIndex(e=>e.startMinutes===i.startMinutes&&e.endMinutes===i.endMinutes&&e.temperature===i.temperature);if(-1===s)return;this._saveHistoryState();const a=this._editingBlocks.filter((e,t)=>t!==s);this._editingBlocks=gt(yt(a)),this._updateValidationWarnings()}_switchToWeekday(e){e!==this._editingWeekday&&this._initializeEditor(e)}_closeEditor(){this._editingWeekday=void 0,this._editingBlocks=void 0,this._editingBaseTemperature=void 0,this._editingSlotIndex=void 0,this._editingSlotData=void 0,this._historyStack=[],this._historyIndex=-1,this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_saveSchedule(){if(!this._editingWeekday||!this._editingBlocks||void 0===this._editingBaseTemperature)return;const e=At(mt(this._editingBlocks,this._editingBaseTemperature),this.minTemp,this.maxTemp);if(e){const t=this._translateValidationMessage(e);return void this.dispatchEvent(new CustomEvent("validation-failed",{detail:{error:t},bubbles:!0,composed:!0}))}this.dispatchEvent(new CustomEvent("save-schedule",{detail:{weekday:this._editingWeekday,blocks:this._editingBlocks,baseTemperature:this._editingBaseTemperature},bubbles:!0,composed:!0}))}_saveAndClose(){this._saveSchedule()}render(){return this.open&&this._editingWeekday?W`
      <ha-dialog
        open
        @closed=${this._closeEditor}
        .heading=${this._formatEdit(this._editingWeekday)}
        scrimClickAction="close"
        escapeKeyAction="close"
      >
        <div class="dialog-content">
          <!-- Weekday selector tabs -->
          <div class="weekday-tabs">
            ${ot.map(e=>W`
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

        <ha-button slot="primaryAction" @click=${this._saveAndClose} dialogAction="close">
          ${this.translations?.save??"Save"}
        </ha-button>
        <ha-button slot="secondaryAction" @click=${this._closeEditor} dialogAction="close">
          ${this.translations?.cancel??"Cancel"}
        </ha-button>
      </ha-dialog>
    `:W``}_formatEdit(e){return(this.translations?.edit??"Edit {weekday}").replace("{weekday}",this._getWeekdayLabel(e,"long"))}_renderEditor(){if(!this._editingWeekday||!this._editingBlocks)return W``;const e=void 0!==this._editingBaseTemperature?ft(this._editingBlocks,this._editingBaseTemperature):this._editingBlocks;return W`
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

        ${this._validationWarnings.length>0?W`
              <ha-alert alert-type="warning" .title=${this.translations?.warningsTitle??""}>
                <ul class="warnings-list">
                  ${this._validationWarnings.map(e=>W`<li class="warning-item">
                        ${this._translateValidationMessage(e)}
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
              @change=${e=>{this._saveHistoryState(),this._editingBaseTemperature=parseFloat(e.target.value),this.requestUpdate()}}
            />
            <span class="temp-unit">${this.temperatureUnit}</span>
            <div
              class="color-indicator"
              style="background-color: ${ut(this._editingBaseTemperature||20)}"
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
          ${e.map((t,i)=>{const s=this._editingBlocks.findIndex(e=>e.startMinutes===t.startMinutes&&e.endMinutes===t.endMinutes),a=!(-1!==s);return void 0!==this._editingSlotIndex&&this._editingSlotIndex===s&&void 0!==this._editingSlotData&&this._editingSlotData?W`
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
                    style="background-color: ${ut(this._editingSlotData.temperature)}"
                  ></div>
                </div>
              `:W`
              <div class="time-block-editor ${a?"base-temp-slot":""}">
                <span class="time-display">${this._formatTimeDisplay(t.startTime)}</span>
                <span class="time-display">${this._formatTimeDisplay(t.endTime)}</span>
                <div class="temp-display-group">
                  <span class="temp-display">${t.temperature.toFixed(1)}</span>
                  <span class="temp-unit">${this.temperatureUnit}</span>
                </div>
                <div class="slot-actions">
                  ${a?W``:W`
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
                        ></ha-icon-button>
                      `}
                </div>
                <div
                  class="color-indicator"
                  style="background-color: ${ut(t.temperature)}"
                ></div>
              </div>
            `})}
          ${this._editingBlocks.length<12&&void 0===this._editingSlotIndex?W`
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
    `}static{this.styles=Mt}};Pt([he({type:Boolean})],Lt.prototype,"open",void 0),Pt([he({type:String})],Lt.prototype,"weekday",void 0),Pt([he({attribute:!1})],Lt.prototype,"scheduleData",void 0),Pt([he({type:Number})],Lt.prototype,"minTemp",void 0),Pt([he({type:Number})],Lt.prototype,"maxTemp",void 0),Pt([he({type:Number})],Lt.prototype,"tempStep",void 0),Pt([he({type:String})],Lt.prototype,"temperatureUnit",void 0),Pt([he({type:String})],Lt.prototype,"hourFormat",void 0),Pt([he({attribute:!1})],Lt.prototype,"translations",void 0),Pt([pe()],Lt.prototype,"_editingWeekday",void 0),Pt([pe()],Lt.prototype,"_editingBlocks",void 0),Pt([pe()],Lt.prototype,"_editingBaseTemperature",void 0),Pt([pe()],Lt.prototype,"_validationWarnings",void 0),Pt([pe()],Lt.prototype,"_editingSlotIndex",void 0),Pt([pe()],Lt.prototype,"_editingSlotData",void 0),Lt=Pt([Ge("hmip-schedule-editor")],Lt);const zt=r`
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
    --mdc-theme-primary: var(--primary-color);
  }

  .no-data {
    text-align: center;
    padding: 32px;
    color: var(--secondary-text-color);
  }

  .events-table {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--divider-color);
    border-radius: 8px;
    overflow: hidden;
  }

  .events-header {
    display: grid;
    grid-template-columns: 70px 1fr minmax(60px, auto) minmax(60px, auto) 70px;
    gap: 8px;
    padding: 8px 16px;
    background-color: var(--secondary-background-color);
    font-weight: 500;
    font-size: 13px;
    color: var(--secondary-text-color);
    text-transform: uppercase;
  }

  .events-header.no-actions {
    grid-template-columns: 70px 1fr minmax(60px, auto) minmax(60px, auto);
  }

  .event-row {
    display: grid;
    grid-template-columns: 70px 1fr minmax(60px, auto) minmax(60px, auto) 70px;
    gap: 8px;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid var(--divider-color);
    transition: background-color 0.2s;
  }

  .event-row.no-actions {
    grid-template-columns: 70px 1fr minmax(60px, auto) minmax(60px, auto);
  }

  .event-row:last-child {
    border-bottom: none;
  }

  .event-row.inactive {
    opacity: 0.5;
  }

  .event-row:hover {
    background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.05);
  }

  .col-time {
    font-weight: 500;
    font-family: monospace;
    color: var(--primary-text-color);
  }

  .col-weekdays {
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

  .col-actions {
    display: flex;
    gap: 0;
    justify-content: flex-end;
  }

  ha-icon-button {
    --mdc-icon-button-size: 36px;
    color: var(--secondary-text-color);
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    .events-header {
      grid-template-columns: 55px 1fr minmax(50px, auto) minmax(50px, auto) 60px;
      gap: 6px;
      padding: 8px 12px;
      font-size: 11px;
    }

    .event-row {
      grid-template-columns: 55px 1fr minmax(50px, auto) minmax(50px, auto) 60px;
      gap: 6px;
      padding: 10px 12px;
    }

    .weekday-badge {
      min-width: 22px;
      padding: 2px 3px;
      font-size: 10px;
    }
  }

  @media (max-width: 480px) {
    .events-header {
      grid-template-columns: 50px 1fr 50px;
      gap: 6px;
      padding: 6px 8px;
      font-size: 10px;
    }

    .events-header .col-duration,
    .events-header .col-state {
      display: none;
    }

    .event-row {
      grid-template-columns: 50px 1fr 50px;
      gap: 6px;
      padding: 8px;
    }

    .event-row .col-duration,
    .event-row .col-state {
      display: none;
    }

    .col-time {
      font-size: 12px;
    }

    .weekday-badge {
      min-width: 20px;
      padding: 1px 2px;
      font-size: 9px;
    }
  }

  /* Touch device optimizations */
  @media (hover: none) and (pointer: coarse) {
    .event-row:hover {
      background-color: transparent;
    }

    .event-row:active {
      background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
    }
  }
`;var Nt=function(e,t,i,s){var a,n=arguments.length,r=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(r=(n<3?a(r):n>3?a(t,i,r):a(t,i))||r);return n>3&&r&&Object.defineProperty(t,i,r),r};let Rt=class extends oe{constructor(){super(...arguments),this.editable=!0}static{this.styles=zt}_handleAdd(){this.dispatchEvent(new CustomEvent("add-event",{bubbles:!0,composed:!0}))}_handleEdit(e){this.dispatchEvent(new CustomEvent("edit-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}_handleDelete(e){this.dispatchEvent(new CustomEvent("delete-event",{bubbles:!0,composed:!0,detail:{entry:e}}))}render(){if(!this.scheduleData)return W`<div class="no-data">${this.translations.loading}</div>`;const e=function(e){const t=[];for(const[i,s]of Object.entries(e))t.push({...s,groupNo:i,isActive:bt(s)});return t.sort((e,t)=>e.time.localeCompare(t.time)),t}(this.scheduleData);return 0===e.length?W`
        <div class="no-data">
          <p>${this.translations.noScheduleEvents}</p>
          ${this.editable?W`<ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>`:""}
        </div>
      `:W`
      <div class="schedule-list">
        ${this.editable?W`<div class="toolbar">
              <ha-button @click=${this._handleAdd}> ${this.translations.addEvent} </ha-button>
            </div>`:""}
        <div class="events-table">
          <div class="events-header ${this.editable?"":"no-actions"}">
            <div class="col-time">${this.translations.time}</div>
            <div class="col-weekdays">${this.translations.weekdays}</div>
            <div class="col-state">${this.translations.state}</div>
            <div class="col-duration">${this.translations.duration}</div>
            ${this.editable?W`<div class="col-actions"></div>`:""}
          </div>
          ${rt(e,e=>e.groupNo,e=>this._renderEvent(e))}
        </div>
      </div>
    `}_renderEvent(e){const t=function(e,t){const i=t?lt[t]:void 0;return"binary"===i?.levelType?0===e?"Off":"On":`${Math.round(100*e)}%`}(e.level,this.domain),i=function(e){if(!e)return"-";const t=kt(e);return t?`${t.value}${{ms:"ms",s:"s",min:"min",h:"h"}[t.unit]}`:e}(e.duration);return W`
      <div
        class="event-row ${e.isActive?"active":"inactive"} ${this.editable?"":"no-actions"}"
      >
        <div class="col-time">${e.time}</div>
        <div class="col-weekdays">
          <div class="weekday-badges">
            ${ot.map(t=>{const i=e.weekdays.includes(t);return W`<span class="weekday-badge ${i?"active":"inactive"}"
                >${this.translations.weekdayShortLabels[t]}</span
              >`})}
          </div>
        </div>
        <div class="col-state">
          ${t}
          ${null!==e.level_2?W`<span class="level-2"
                >, ${this.translations.slat}: ${Math.round(100*e.level_2)}%</span
              >`:""}
        </div>
        <div class="col-duration">${i}</div>
        ${this.editable?W`<div class="col-actions">
              <ha-icon-button
                .path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}
                @click=${()=>this._handleEdit(e)}
              ></ha-icon-button>
              <ha-icon-button
                .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                @click=${()=>this._handleDelete(e)}
              ></ha-icon-button>
            </div>`:""}
      </div>
    `}};Nt([he({attribute:!1})],Rt.prototype,"scheduleData",void 0),Nt([he({attribute:!1})],Rt.prototype,"domain",void 0),Nt([he({type:Boolean})],Rt.prototype,"editable",void 0),Nt([he({attribute:!1})],Rt.prototype,"translations",void 0),Rt=Nt([Ge("hmip-device-schedule-list")],Rt);const Bt=r`
  :host {
    display: block;
  }

  /* Dialog styles */
  ha-dialog {
    --mdc-dialog-max-width: 500px;
  }

  .editor-content {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
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

  /* Mobile Optimization */
  @media (max-width: 768px) {
    ha-dialog {
      --mdc-dialog-max-width: 100vw;
    }
  }
`;var Ut=function(e,t,i,s){var a,n=arguments.length,r=n<3?t:null===s?s=Object.getOwnPropertyDescriptor(t,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(e,t,i,s);else for(var o=e.length-1;o>=0;o--)(a=e[o])&&(r=(n<3?a(r):n>3?a(t,i,r):a(t,i))||r);return n>3&&r&&Object.defineProperty(t,i,r),r};let Vt=class extends oe{constructor(){super(...arguments),this.open=!1,this.isNewEvent=!1,this._validationErrors=[]}static{this.styles=Bt}willUpdate(e){(e.has("open")||e.has("entry"))&&(this.open&&this.entry?(this._editingEntry={...this.entry},this._validationErrors=[]):this.open||(this._editingEntry=void 0,this._validationErrors=[]))}_updateEditingEntry(e){this._editingEntry&&(this._editingEntry={...this._editingEntry,...e},this._validationErrors=[],this.requestUpdate())}_handleClose(){this.dispatchEvent(new CustomEvent("editor-closed",{bubbles:!0,composed:!0}))}_handleSave(){if(!this._editingEntry||void 0===this.groupNo)return;const e=function(e,t){const i=[];(function(e){try{return function(e){const t=e.split(":");if(2!==t.length)throw new Error(`Invalid time format: ${e}`);const i=parseInt(t[0],10),s=parseInt(t[1],10);if(isNaN(i)||isNaN(s)||i<0||i>23||s<0||s>59)throw new Error(`Invalid time values: ${e}`)}(e),!0}catch{return!1}})(e.time)||i.push({field:"time",message:"Time must be in HH:MM format (00:00-23:59)"}),e.weekdays&&0!==e.weekdays.length||i.push({field:"weekdays",message:"At least one weekday must be selected"});const s=t?lt[t]:void 0;return"binary"===s?.levelType?0!==e.level&&1!==e.level&&i.push({field:"level",message:"Level must be 0 or 1 for switch"}):(e.level<0||e.level>1)&&i.push({field:"level",message:"Level must be between 0.0 and 1.0"}),"cover"===t&&null!==e.level_2&&(e.level_2<0||e.level_2>1)&&i.push({field:"level_2",message:"Slat position must be between 0.0 and 1.0"}),xt(e.condition)&&(e.astro_offset_minutes<-720||e.astro_offset_minutes>720)&&i.push({field:"astro_offset_minutes",message:"Astro offset must be between -720 and 720 minutes"}),null===e.duration||St(e.duration)||i.push({field:"duration",message:"Invalid duration format"}),null===e.ramp_time||St(e.ramp_time)||i.push({field:"ramp_time",message:"Invalid ramp time format"}),i}(this._editingEntry,this.domain);e.length>0?this._validationErrors=e.map(e=>`${e.field}: ${e.message}`):this.dispatchEvent(new CustomEvent("save-event",{bubbles:!0,composed:!0,detail:{entry:{...this._editingEntry},groupNo:this.groupNo}}))}render(){return this.open&&this._editingEntry?W`
      <ha-dialog
        open
        @closed=${this._handleClose}
        .heading=${this.isNewEvent?this.translations.addEvent:this.translations.editEvent}
        scrimClickAction="close"
        escapeKeyAction="close"
      >
        <div class="editor-content">
          ${this._renderTimeFields()} ${this._renderConditionFields()}
          ${this._renderWeekdayFields()} ${this._renderLevelFields()}
          ${this._renderDurationFields()} ${this._renderRampTimeFields()}
          ${this._renderChannelFields()} ${this._renderValidationErrors()}
        </div>
        <ha-button slot="primaryAction" @click=${this._handleSave}>
          ${this.translations.save}
        </ha-button>
        <ha-button slot="secondaryAction" @click=${this._handleClose} dialogAction="close">
          ${this.translations.cancel}
        </ha-button>
      </ha-dialog>
    `:W``}_renderValidationErrors(){return 0===this._validationErrors.length?W``:W`
      <ha-alert alert-type="error">
        <ul class="validation-list">
          ${this._validationErrors.map(e=>W`<li>${e}</li>`)}
        </ul>
      </ha-alert>
    `}_renderTimeFields(){return this._editingEntry?W`
      <div class="form-group">
        <label>${this.translations.time}</label>
        <input
          type="time"
          .value=${this._editingEntry.time}
          @change=${e=>{this._updateEditingEntry({time:e.target.value})}}
        />
      </div>
    `:W``}_renderConditionFields(){if(!this._editingEntry)return W``;const e=xt(this._editingEntry.condition);return W`
      <div class="form-group">
        <label>${this.translations.condition}</label>
        <ha-select
          .value=${this._editingEntry.condition}
          .options=${dt.map(e=>({value:e,label:this.translations.conditionLabels[e]||e}))}
          @selected=${e=>{e.stopPropagation();const t=e.detail.value,i={condition:t};"fixed_time"===t?(i.astro_type=null,i.astro_offset_minutes=0):null===this._editingEntry.astro_type&&(i.astro_type="sunrise"),this._updateEditingEntry(i)}}
          @closed=${e=>e.stopPropagation()}
        ></ha-select>
      </div>
      ${e?W`
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
                min="-720"
                max="720"
                .value=${String(this._editingEntry.astro_offset_minutes)}
                @input=${e=>{const t=parseInt(e.target.value,10);isNaN(t)||this._updateEditingEntry({astro_offset_minutes:t})}}
              />
            </div>
          `:""}
    `}_renderWeekdayFields(){return this._editingEntry?W`
      <div class="form-group">
        <label>${this.translations.weekdaysLabel}</label>
        <div class="weekday-checkboxes">
          ${ot.map(e=>{const t=this._editingEntry.weekdays.includes(e);return W`
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
    `:W``}_renderLevelFields(){if(!this._editingEntry)return W``;const e=this.domain?lt[this.domain]:void 0;return W`
      <div class="form-group">
        <label>${this.translations.stateLabel}</label>
        ${"binary"===e?.levelType?W`
              <ha-select
                .value=${String(this._editingEntry.level)}
                .options=${[{value:"0",label:this.translations.levelOff},{value:"1",label:this.translations.levelOn}]}
                @selected=${e=>{e.stopPropagation();const t=parseInt(e.detail.value,10);this._updateEditingEntry({level:t})}}
                @closed=${e=>e.stopPropagation()}
              ></ha-select>
            `:W`
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*this._editingEntry.level)}
                  @value-changed=${e=>{e.stopPropagation(),this._updateEditingEntry({level:parseInt(e.detail.value,10)/100})}}
                ></ha-slider>
                <span class="slider-value">${Math.round(100*this._editingEntry.level)}%</span>
              </div>
            `}
      </div>
      ${e?.hasLevel2?W`
            <div class="form-group">
              <label>${this.translations.slat}</label>
              <div class="slider-group">
                <ha-slider
                  min="0"
                  max="100"
                  .value=${Math.round(100*(this._editingEntry.level_2||0))}
                  @value-changed=${e=>{e.stopPropagation(),this._updateEditingEntry({level_2:parseInt(e.detail.value,10)/100})}}
                ></ha-slider>
                <span class="slider-value"
                  >${Math.round(100*(this._editingEntry.level_2||0))}%</span
                >
              </div>
            </div>
          `:""}
    `}_renderDurationFields(){if(!this._editingEntry)return W``;const e=this.domain?lt[this.domain]:void 0;if(e&&!e.hasDuration)return W``;const t=this._editingEntry.duration?kt(this._editingEntry.duration):null,i=t?.value??0,s=t?.unit??"s";return W`
      <div class="form-group">
        <label>${this.translations.duration}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({duration:wt(t,s)}):this._updateEditingEntry({duration:null})}}
          />
          <ha-select
            .value=${s}
            .options=${ct.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation(),i>0&&this._updateEditingEntry({duration:wt(i,e.detail.value)})}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderRampTimeFields(){if(!this._editingEntry)return W``;const e=this.domain?lt[this.domain]:void 0;if(e&&!e.hasRampTime)return W``;const t=this._editingEntry.ramp_time?kt(this._editingEntry.ramp_time):null,i=t?.value??0,s=t?.unit??"s";return W`
      <div class="form-group">
        <label>${this.translations.rampTime}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${e=>{const t=parseFloat(e.target.value);!isNaN(t)&&t>0?this._updateEditingEntry({ramp_time:wt(t,s)}):this._updateEditingEntry({ramp_time:null})}}
          />
          <ha-select
            .value=${s}
            .options=${ct.map(e=>({value:e,label:e}))}
            @selected=${e=>{e.stopPropagation(),i>0&&this._updateEditingEntry({ramp_time:wt(i,e.detail.value)})}}
            @closed=${e=>e.stopPropagation()}
          ></ha-select>
        </div>
      </div>
    `}_renderChannelFields(){return this._editingEntry&&this.availableTargetChannels&&Object.keys(this.availableTargetChannels).length>0?W`
        <div class="form-group">
          <label>${this.translations.channels}</label>
          <div class="channel-checkboxes">
            ${Object.entries(this.availableTargetChannels).map(([e,t])=>{const i=this._editingEntry.target_channels.includes(e);return W`
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
      `:W``}};Ut([he({type:Boolean})],Vt.prototype,"open",void 0),Ut([he({attribute:!1})],Vt.prototype,"entry",void 0),Ut([he()],Vt.prototype,"groupNo",void 0),Ut([he({type:Boolean})],Vt.prototype,"isNewEvent",void 0),Ut([he({attribute:!1})],Vt.prototype,"domain",void 0),Ut([he({attribute:!1})],Vt.prototype,"availableTargetChannels",void 0),Ut([he({attribute:!1})],Vt.prototype,"translations",void 0),Ut([pe()],Vt.prototype,"_editingEntry",void 0),Ut([pe()],Vt.prototype,"_validationErrors",void 0),Vt=Ut([Ge("hmip-device-schedule-editor")],Vt);let Ot=class extends oe{constructor(){super(...arguments),this.entryId="",this.deviceAddress="",this.deviceName="",this._devices=[],this._selectedDevice=null,this._climateData=null,this._deviceData=null,this._selectedProfile="",this._loading=!0,this._saving=!1,this._error="",this._deviceShowEditor=!1,this._deviceIsNewEvent=!1}updated(e){(e.has("entryId")||e.has("deviceAddress"))&&this.entryId&&this._fetchDevices()}async _fetchDevices(){this._loading=!0,this._error="";try{let e;this._devices=await ke(this.hass,this.entryId),this.deviceAddress&&(e=this._devices.find(e=>e.address===this.deviceAddress)),!e&&this._devices.length>0&&(e=this._devices[0]),e&&(this._selectedDevice=e,await this._loadSchedule(e))}catch(e){this._error=String(e)}finally{this._loading=!1}}async _loadSchedule(e){this._loading=!0,this._error="",this._climateData=null,this._deviceData=null;try{if("climate"===e.schedule_type){let t=this._selectedProfile||void 0;if(!t){const i=await we(this.hass,this.entryId,e.address);t=i.active_profile,this._selectedProfile=t;const s=Object.keys(i.schedule_data).some(e=>"MONDAY"===e||"TUESDAY"===e||"WEDNESDAY"===e||"THURSDAY"===e||"FRIDAY"===e||"SATURDAY"===e||"SUNDAY"===e);s&&(this._climateData=i)}if(!this._climateData){const i=await we(this.hass,this.entryId,e.address,t);this._climateData=i,!this._selectedProfile&&i.active_profile&&(this._selectedProfile=i.active_profile)}}else this._deviceData=await async function(e,t,i){return e.callWS({type:"homematicip_local/config/get_device_schedule",entry_id:t,device_address:i})}(this.hass,this.entryId,e.address)}catch{this._error=this._l("device_schedule.load_failed")}finally{this._loading=!1}}_l(e,t){return Me(this.hass,e,t)}_handleBack(){this.dispatchEvent(new CustomEvent("back",{bubbles:!0,composed:!0}))}async _handleDeviceSelect(e){e.stopPropagation();const t=e.detail.value;if(!t||t===this._selectedDevice?.address)return;const i=this._devices.find(e=>e.address===t);i&&(this._selectedDevice=i,this._selectedProfile="",this._editingWeekday=void 0,this._copiedSchedule=void 0,this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1,await this._loadSchedule(i))}async _handleProfileChange(e){e.stopPropagation();const t=e.detail.value;if(t&&t!==this._selectedProfile&&(this._selectedProfile=t,this._selectedDevice)){try{await async function(e,t,i,s){return e.callWS({type:"homematicip_local/config/set_climate_active_profile",entry_id:t,device_address:i,profile:s})}(this.hass,this.entryId,this._selectedDevice.address,t)}catch{return void Ne(this,{message:this._l("device_schedule.save_failed")})}await this._loadSchedule(this._selectedDevice)}}_onWeekdayClick(e){this._editingWeekday=e.detail.weekday}_onCopySchedule(e){const t=e.detail.weekday;if(!this._climateData)return;const i=this._climateData.schedule_data[t];if(!i)return;const{blocks:s,baseTemperature:a}=vt(i);this._copiedSchedule={weekday:t,blocks:JSON.parse(JSON.stringify(s)),baseTemperature:a}}async _onPasteSchedule(e){const t=e.detail.weekday;if(!this._selectedDevice||!this._copiedSchedule||!this._climateData)return;const i=this._copiedSchedule.baseTemperature??function(e){if(0===e.length)return 20;const t=new Map;for(const i of e){const e=i.endMinutes-i.startMinutes,s=t.get(i.temperature)||0;t.set(i.temperature,s+e)}let i=0,s=20;for(const[e,a]of t.entries())a>i&&(i=a,s=e);return s}(this._copiedSchedule.blocks),s=mt(this._copiedSchedule.blocks,i);if(At(s,this._climateData.min_temp??5,this._climateData.max_temp??30.5))Ne(this,{message:this._l("device_schedule.invalid_schedule")});else{this._saving=!0;try{const{base_temperature:e,periods:i}=s;await Se(this.hass,this.entryId,this._selectedDevice.address,this._selectedProfile,t,e,i.map(e=>({...e}))),Ne(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{Ne(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}}async _onSaveSchedule(e){if(!this._selectedDevice||!this._climateData)return;const{weekday:t,blocks:i,baseTemperature:s}=e.detail,a=mt(i,s);if(At(a,this._climateData.min_temp??5,this._climateData.max_temp??30.5))Ne(this,{message:this._l("device_schedule.invalid_schedule")});else{this._saving=!0;try{const{base_temperature:e,periods:i}=a;await Se(this.hass,this.entryId,this._selectedDevice.address,this._selectedProfile,t,e,i.map(e=>({...e}))),Ne(this,{message:this._l("device_schedule.save_success")}),this._editingWeekday=void 0,await this._loadSchedule(this._selectedDevice)}catch{Ne(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}}_onValidationFailed(e){Ne(this,{message:this._l("device_schedule.invalid_schedule",{error:e.detail.error})})}_onEditorClosed(){this._editingWeekday=void 0}async _handleReload(){if(this._selectedDevice)try{await async function(e,t,i){return e.callWS({type:"homematicip_local/config/reload_device_config",entry_id:t,device_address:i})}(this.hass,this.entryId,this._selectedDevice.address),Ne(this,{message:this._l("device_schedule.reload_success")}),await this._loadSchedule(this._selectedDevice)}catch{Ne(this,{message:this._l("device_schedule.reload_failed")})}}async _handleExport(){const e=this._climateData?.schedule_data??this._deviceData?.schedule_data;if(!e)return;const t=JSON.stringify(e,null,2),i=new Blob([t],{type:"application/json"}),s=URL.createObjectURL(i),a=document.createElement("a");a.href=s;const n=this._selectedDevice?.address.replace(/:/g,"_")??"schedule";a.download=`${n}_schedule.json`,a.click(),URL.revokeObjectURL(s)}async _handleImport(){const e=document.createElement("input");e.type="file",e.accept=".json",e.onchange=async()=>{const t=e.files?.[0];if(t&&this._selectedDevice)try{const e=await t.text(),i=JSON.parse(e);if(!await Le(0,{title:this._l("device_schedule.import_confirm_title"),text:this._l("device_schedule.import_confirm_text"),confirmText:this._l("device_schedule.import"),dismissText:this._l("common.cancel")}))return;"climate"===this._selectedDevice.schedule_type?(this._climateData={...this._climateData,schedule_data:i},Ne(this,{message:this._l("device_schedule.import_success")})):(await Ce(this.hass,this.entryId,this._selectedDevice.address,i),Ne(this,{message:this._l("device_schedule.import_success")}),await this._loadSchedule(this._selectedDevice))}catch{Ne(this,{message:this._l("device_schedule.import_failed")})}},e.click()}_buildGridTranslations(){return{weekdayShortLabels:{MONDAY:this._l("device_schedule.weekdays").split(",")[0],TUESDAY:this._l("device_schedule.weekdays").split(",")[1],WEDNESDAY:this._l("device_schedule.weekdays").split(",")[2],THURSDAY:this._l("device_schedule.weekdays").split(",")[3],FRIDAY:this._l("device_schedule.weekdays").split(",")[4],SATURDAY:this._l("device_schedule.weekdays").split(",")[5],SUNDAY:this._l("device_schedule.weekdays").split(",")[6]},clickToEdit:this._l("device_schedule.click_to_edit"),copySchedule:this._l("device_schedule.copy_schedule"),pasteSchedule:this._l("device_schedule.paste_schedule")}}_buildEditorTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},weekdayLongLabels:{MONDAY:this._l("device_schedule.weekday_monday"),TUESDAY:this._l("device_schedule.weekday_tuesday"),WEDNESDAY:this._l("device_schedule.weekday_wednesday"),THURSDAY:this._l("device_schedule.weekday_thursday"),FRIDAY:this._l("device_schedule.weekday_friday"),SATURDAY:this._l("device_schedule.weekday_saturday"),SUNDAY:this._l("device_schedule.weekday_sunday")},edit:this._l("device_schedule.edit"),cancel:this._l("common.cancel"),save:this._l("device_schedule.save"),addTimeBlock:this._l("device_schedule.add_time_block"),from:this._l("device_schedule.from"),to:this._l("device_schedule.to"),baseTemperature:this._l("device_schedule.base_temperature"),baseTemperatureDescription:this._l("device_schedule.base_temperature_description"),temperaturePeriods:this._l("device_schedule.temperature_periods"),editSlot:this._l("device_schedule.edit_slot"),saveSlot:this._l("device_schedule.save_slot"),cancelSlotEdit:this._l("device_schedule.cancel_slot_edit"),undoShortcut:this._l("device_schedule.undo_shortcut"),redoShortcut:this._l("device_schedule.redo_shortcut"),warningsTitle:this._l("device_schedule.warnings_title"),validationMessages:{blockEndBeforeStart:this._l("device_schedule.validation_block_end_before_start"),blockZeroDuration:this._l("device_schedule.validation_block_zero_duration"),invalidStartTime:this._l("device_schedule.validation_invalid_start_time"),invalidEndTime:this._l("device_schedule.validation_invalid_end_time"),temperatureOutOfRange:this._l("device_schedule.validation_temp_out_of_range"),invalidSlotCount:this._l("device_schedule.validation_invalid_slot_count"),invalidSlotKey:this._l("device_schedule.validation_invalid_slot_key"),missingSlot:this._l("device_schedule.validation_missing_slot"),slotMissingValues:this._l("device_schedule.validation_slot_missing_values"),slotTimeBackwards:this._l("device_schedule.validation_slot_time_backwards"),slotTimeExceedsDay:this._l("device_schedule.validation_slot_time_exceeds_day"),lastSlotMustEnd:this._l("device_schedule.validation_last_slot_must_end"),scheduleMustBeObject:this._l("device_schedule.validation_schedule_must_be_object"),missingWeekday:this._l("device_schedule.validation_missing_weekday"),invalidWeekdayData:this._l("device_schedule.validation_invalid_weekday_data"),weekdayValidationError:this._l("device_schedule.validation_weekday_error")}}}render(){return this._loading&&0===this._devices.length?W`<div class="loading">${this._l("common.loading")}</div>`:this._error&&0===this._devices.length?W`<div class="error">${this._error}</div>`:W`
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
      </div>

      ${0===this._devices.length?W`<div class="empty-state">${this._l("device_schedule.no_devices")}</div>`:j}
      ${this._selectedDevice&&this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:j}
      ${this._error&&this._selectedDevice?W`<div class="error">${this._error}</div>`:j}
      ${"climate"===this._selectedDevice?.schedule_type&&this._climateData?this._renderClimateSchedule():j}
      ${"default"===this._selectedDevice?.schedule_type&&this._deviceData?this._renderDeviceSchedule():j}
    `}_renderClimateSchedule(){const e=this._climateData,t=e.schedule_data;return W`
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
            <ha-button outlined @click=${this._handleImport}>
              ${this._l("device_schedule.import")}
            </ha-button>
            <ha-button outlined @click=${this._handleReload}>
              ${this._l("device_schedule.reload")}
            </ha-button>
          </div>
        </div>

        <div class="climate-grid-container">
          <hmip-schedule-grid
            .scheduleData=${t}
            .editable=${!0}
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

      ${this._saving?W`<div class="saving-overlay">${this._l("device_schedule.saving")}</div>`:j}
    `}_onDeviceAddEvent(){if(!this._deviceData)return;const e=this._deviceData.schedule_data?.entries??{},t=this._deviceData.max_entries;if(t&&Object.keys(e).length>=t)return void Ne(this,{message:this._l("device_schedule.max_entries",{max:t})});const i=function(e){const t={weekdays:[],time:"00:00",condition:"fixed_time",astro_type:null,astro_offset_minutes:0,target_channels:[],level:0,level_2:null,duration:null,ramp_time:null};return"cover"===e&&(t.level_2=0),t}(this._deviceData.schedule_domain??void 0),s=this._deviceData.available_target_channels;if(s){const e=Object.keys(s)[0];e&&(i.target_channels=[e])}const a=Object.keys(e).map(e=>parseInt(e,10)),n=a.length>0?Math.max(...a):0;this._deviceEditingGroupNo=String(n+1),this._deviceEditingEntry={...i},this._deviceIsNewEvent=!0,this._deviceShowEditor=!0}_onDeviceEditEvent(e){const t=e.detail.entry;this._deviceEditingGroupNo=t.groupNo,this._deviceEditingEntry={...t},this._deviceIsNewEvent=!1,this._deviceShowEditor=!0}async _onDeviceDeleteEvent(e){if(!confirm(this._l("device_schedule.confirm_delete")))return;if(!this._deviceData||!this._selectedDevice)return;const t={...this._deviceData.schedule_data?.entries??{}};delete t[e.detail.entry.groupNo],this._saving=!0;try{await Ce(this.hass,this.entryId,this._selectedDevice.address,{entries:Et(t)}),Ne(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{Ne(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}async _onDeviceSaveEvent(e){if(!this._deviceData||!this._selectedDevice)return;const{entry:t,groupNo:i}=e.detail,s={...this._deviceData.schedule_data?.entries??{},[i]:t};this._saving=!0,this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1;try{await Ce(this.hass,this.entryId,this._selectedDevice.address,{entries:Et(s)}),Ne(this,{message:this._l("device_schedule.save_success")}),await this._loadSchedule(this._selectedDevice)}catch{Ne(this,{message:this._l("device_schedule.save_failed")})}finally{this._saving=!1}}_onDeviceEditorClosed(){this._deviceShowEditor=!1,this._deviceEditingEntry=void 0,this._deviceEditingGroupNo=void 0,this._deviceIsNewEvent=!1}_buildDeviceListTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},time:this._l("device_schedule.time"),weekdays:this._l("device_schedule.weekdays_label"),duration:this._l("device_schedule.duration"),state:this._l("device_schedule.level"),addEvent:this._l("device_schedule.add_event"),slat:this._l("device_schedule.slat"),noScheduleEvents:this._l("device_schedule.no_schedule_data"),loading:this._l("common.loading")}}_buildDeviceEditorTranslations(){const e=this._l("device_schedule.weekdays").split(",");return{weekdayShortLabels:{MONDAY:e[0],TUESDAY:e[1],WEDNESDAY:e[2],THURSDAY:e[3],FRIDAY:e[4],SATURDAY:e[5],SUNDAY:e[6]},addEvent:this._l("device_schedule.add_event"),editEvent:this._l("device_schedule.edit_event"),cancel:this._l("common.cancel"),save:this._l("device_schedule.save"),time:this._l("device_schedule.time"),condition:this._l("device_schedule.condition"),weekdaysLabel:this._l("device_schedule.weekdays_label"),stateLabel:this._l("device_schedule.level"),duration:this._l("device_schedule.duration"),rampTime:this._l("device_schedule.ramp_time"),channels:this._l("device_schedule.target_channel"),levelOn:this._l("device_schedule.level_on"),levelOff:this._l("device_schedule.level_off"),slat:this._l("device_schedule.slat"),astroSunrise:this._l("device_schedule.astro_sunrise"),astroSunset:this._l("device_schedule.astro_sunset"),astroOffset:this._l("device_schedule.astro_offset"),confirmDelete:this._l("device_schedule.confirm_delete"),conditionLabels:{fixed_time:this._l("device_schedule.condition_fixed_time"),astro:this._l("device_schedule.condition_astro"),fixed_if_before_astro:this._l("device_schedule.condition_fixed_if_before_astro"),astro_if_before_fixed:this._l("device_schedule.condition_astro_if_before_fixed"),fixed_if_after_astro:this._l("device_schedule.condition_fixed_if_after_astro"),astro_if_after_fixed:this._l("device_schedule.condition_astro_if_after_fixed"),earliest:this._l("device_schedule.condition_earliest"),latest:this._l("device_schedule.condition_latest")}}}_renderDeviceSchedule(){const e=this._deviceData,t=e.schedule_data,i=t?.entries??{},s=Object.keys(i).length,a=e.schedule_domain??void 0,n=e.available_target_channels;return W`
      <div class="schedule-content">
        <div class="toolbar">
          <div class="schedule-info">
            ${this._l("device_schedule.entries",{count:s})} |
            ${this._l("device_schedule.max_entries",{max:e.max_entries})}
            ${e.schedule_domain?W` | ${e.schedule_domain}`:j}
          </div>
          <div class="toolbar-actions">
            <ha-button outlined @click=${this._handleExport}>
              ${this._l("device_schedule.export")}
            </ha-button>
            <ha-button outlined @click=${this._handleImport}>
              ${this._l("device_schedule.import")}
            </ha-button>
            <ha-button outlined @click=${this._handleReload}>
              ${this._l("device_schedule.reload")}
            </ha-button>
          </div>
        </div>

        <div class="device-schedule-container">
          <hmip-device-schedule-list
            .scheduleData=${i}
            .domain=${a}
            .editable=${!0}
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
          .availableTargetChannels=${n}
          .translations=${this._buildDeviceEditorTranslations()}
          @save-event=${this._onDeviceSaveEvent}
          @editor-closed=${this._onDeviceEditorClosed}
        ></hmip-device-schedule-editor>
      </div>

      ${this._saving?W`<div class="saving-overlay">${this._l("device_schedule.saving")}</div>`:j}
    `}static{this.styles=[ue,r`
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
    `]}};async function Ht(e,t){return e.callWS({type:"homematicip_local/integration/get_system_health",entry_id:t})}async function Wt(e,t){return(await e.callWS({type:"homematicip_local/integration/get_command_throttle_stats",entry_id:t})).throttle_stats}async function Ft(e,t,i=50,s){return e.callWS({type:"homematicip_local/integration/get_incidents",entry_id:t,limit:i,...s})}async function jt(e,t){return e.callWS({type:"homematicip_local/integration/get_device_statistics",entry_id:t})}async function Kt(e,t){return e.callWS({type:"homematicip_local/ccu/get_system_information",entry_id:t})}async function Yt(e,t){return e.callWS({type:"homematicip_local/ccu/get_hub_data",entry_id:t})}async function Zt(e,t){return e.callWS({type:"homematicip_local/ccu/get_install_mode_status",entry_id:t})}async function Gt(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_signal_quality",entry_id:t})).devices}async function qt(e,t){return e.callWS({type:"homematicip_local/ccu/get_firmware_overview",entry_id:t})}var Qt;e([he({attribute:!1})],Ot.prototype,"hass",void 0),e([he()],Ot.prototype,"entryId",void 0),e([he()],Ot.prototype,"deviceAddress",void 0),e([he()],Ot.prototype,"deviceName",void 0),e([pe()],Ot.prototype,"_devices",void 0),e([pe()],Ot.prototype,"_selectedDevice",void 0),e([pe()],Ot.prototype,"_climateData",void 0),e([pe()],Ot.prototype,"_deviceData",void 0),e([pe()],Ot.prototype,"_selectedProfile",void 0),e([pe()],Ot.prototype,"_editingWeekday",void 0),e([pe()],Ot.prototype,"_copiedSchedule",void 0),e([pe()],Ot.prototype,"_loading",void 0),e([pe()],Ot.prototype,"_saving",void 0),e([pe()],Ot.prototype,"_error",void 0),e([pe()],Ot.prototype,"_deviceEditingEntry",void 0),e([pe()],Ot.prototype,"_deviceEditingGroupNo",void 0),e([pe()],Ot.prototype,"_deviceShowEditor",void 0),e([pe()],Ot.prototype,"_deviceIsNewEvent",void 0),Ot=e([_e("hm-device-schedule")],Ot);let Jt=class extends oe{constructor(){super(...arguments),this.entryId="",this._health=null,this._throttle=null,this._incidents=null,this._deviceStats=null,this._loading=!0,this._error=""}static{Qt=this}static{this._POLL_INTERVAL_FAST=5e3}static{this._POLL_INTERVAL_SLOW=3e4}static{this._STABLE_STATES=["RUNNING","running"]}updated(e){e.has("entryId")&&this.entryId&&(this._stopPolling(),this._fetchAll())}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}_isStableState(){return null!==this._health&&Qt._STABLE_STATES.includes(this._health.central_state)}_scheduleNextPoll(){this._stopPolling();const e=this._isStableState()?Qt._POLL_INTERVAL_SLOW:Qt._POLL_INTERVAL_FAST;this._pollTimer=setTimeout(()=>this._fetchAll(),e)}_stopPolling(){void 0!==this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchAll(){if(this.entryId){null===this._health&&(this._loading=!0),this._error="";try{const[e,t,i,s]=await Promise.all([Ht(this.hass,this.entryId),Wt(this.hass,this.entryId),Ft(this.hass,this.entryId),jt(this.hass,this.entryId)]);this._health=e,this._throttle=t,this._incidents=i,this._deviceStats=s}catch(e){this._error=String(e)}finally{this._loading=!1,this._scheduleNextPoll()}}}_l(e,t){return Me(this.hass,e,t)}async _handleClearIncidents(){if(await Le(0,{title:this._l("integration.clear_incidents_title"),text:this._l("integration.clear_incidents_text"),confirmText:this._l("integration.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t){return e.callWS({type:"homematicip_local/integration/clear_incidents",entry_id:t})}(this.hass,this.entryId),Ne(this,{message:this._l("integration.incidents_cleared")}),this._incidents=await Ft(this.hass,this.entryId)}catch{Ne(this,{message:this._l("integration.action_failed")})}}async _handleClearCache(){if(await Le(0,{title:this._l("integration.clear_cache_title"),text:this._l("integration.clear_cache_text"),confirmText:this._l("integration.clear"),dismissText:this._l("common.cancel"),destructive:!0}))try{await async function(e,t){return e.callWS({type:"homematicip_local/integration/clear_cache",entry_id:t})}(this.hass,this.entryId),Ne(this,{message:this._l("integration.cache_cleared")})}catch{Ne(this,{message:this._l("integration.action_failed")})}}render(){return this.entryId?this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:this._error?W`<div class="error">${this._error}</div>`:W`
      ${this._renderHealthCard()} ${this._renderDeviceStatsCard()} ${this._renderThrottleCard()}
      ${this._renderIncidentsCard()} ${this._renderActionsCard()}
    `:W`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}_renderHealthCard(){return this._health?W`
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
    `:j}_renderDeviceStatsCard(){if(!this._deviceStats)return j;const e=this._deviceStats;return W`
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
          ${Object.keys(e.by_interface).length>1?W`
                <div class="interface-breakdown">
                  ${Object.entries(e.by_interface).map(([e,t])=>W`
                      <div class="interface-row">
                        <span class="interface-name">${e}</span>
                        <span class="interface-stats">
                          ${t.total} ${this._l("integration.total_short")}
                          ${t.unreachable>0?W`,
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
    `}_renderThrottleCard(){return this._throttle&&0!==Object.keys(this._throttle).length?W`
      <ha-card>
        <div class="card-header">${this._l("integration.command_throttle")}</div>
        <div class="card-content">
          ${Object.entries(this._throttle).map(([e,t])=>W`
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
    `:j}_renderIncidentsCard(){if(!this._incidents)return j;const{incidents:e,summary:t}=this._incidents;return W`
      <ha-card>
        <div class="card-header">
          <span>${this._l("integration.incidents")}</span>
          <span class="badge">${t.total_incidents}</span>
        </div>
        <div class="card-content">
          ${0===e.length?W`<div class="empty-state">${this._l("integration.no_incidents")}</div>`:W`
                <div class="incident-list">
                  ${e.map(e=>W`
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
          ${e.length>0?W`
                <div class="action-bar">
                  <ha-button class="destructive" @click=${this._handleClearIncidents}>
                    ${this._l("integration.clear_incidents")}
                  </ha-button>
                </div>
              `:j}
        </div>
      </ha-card>
    `}_renderActionsCard(){return W`
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
    `}_formatScore(e){return`${Math.round(e<=1?100*e:e)}%`}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleString(this.hass.config.language||"en")}catch{return e}}static{this.styles=[ue,r`
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

      .action-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      .destructive {
        --mdc-theme-primary: var(--error-color, #db4437);
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
    `]}};var Xt;e([he({attribute:!1})],Jt.prototype,"hass",void 0),e([he()],Jt.prototype,"entryId",void 0),e([pe()],Jt.prototype,"_health",void 0),e([pe()],Jt.prototype,"_throttle",void 0),e([pe()],Jt.prototype,"_incidents",void 0),e([pe()],Jt.prototype,"_deviceStats",void 0),e([pe()],Jt.prototype,"_loading",void 0),e([pe()],Jt.prototype,"_error",void 0),Jt=Qt=e([_e("hm-integration-dashboard")],Jt);let ei=class extends oe{constructor(){super(...arguments),this.entryId="",this._sysInfo=null,this._hubData=null,this._installMode=null,this._signalDevices=null,this._firmware=null,this._loading=!0,this._error="",this._backupRunning=!1,this._refreshingFirmware=!1,this._signalSortColumn="name",this._signalSortAsc=!0,this._firmwareSortColumn="name",this._firmwareSortAsc=!0}static{Xt=this}static{this._POLL_INTERVAL=3e4}disconnectedCallback(){super.disconnectedCallback(),this._stopInstallModePolling(),this._stopPolling()}updated(e){e.has("entryId")&&this.entryId&&(this._stopPolling(),this._fetchAll())}_scheduleNextPoll(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchAll(),Xt._POLL_INTERVAL)}_stopPolling(){void 0!==this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchAll(){if(this.entryId){null===this._sysInfo&&(this._loading=!0),this._error="";try{const[e,t,i,s,a]=await Promise.all([Kt(this.hass,this.entryId),Yt(this.hass,this.entryId),Zt(this.hass,this.entryId),Gt(this.hass,this.entryId),qt(this.hass,this.entryId)]);this._sysInfo=e,this._hubData=t,this._installMode=i,this._signalDevices=s,this._firmware=a,(i.hmip.active||i.bidcos.active)&&this._startInstallModePolling()}catch(e){this._error=String(e)}finally{this._loading=!1,this._scheduleNextPoll()}}}_l(e,t){return Me(this.hass,e,t)}async _handleCreateBackup(){if(await Le(0,{title:this._l("ccu.create_backup_title"),text:this._l("ccu.create_backup_text"),confirmText:this._l("ccu.create_backup"),dismissText:this._l("common.cancel")})){this._backupRunning=!0;try{const e=await async function(e,t){return e.callWS({type:"homematicip_local/ccu/create_backup",entry_id:t})}(this.hass,this.entryId);if(e.success){const t=(e.size/1024/1024).toFixed(1);Ne(this,{message:this._l("ccu.backup_success",{filename:e.filename,size:t})})}}catch{Ne(this,{message:this._l("ccu.backup_failed")})}finally{this._backupRunning=!1}}}async _handleTriggerInstallMode(e){const t="hmip"===e?"HmIP-RF":"BidCos-RF";if(await Le(0,{title:this._l("ccu.install_mode_title"),text:this._l("ccu.install_mode_text",{interface:t}),confirmText:this._l("ccu.activate"),dismissText:this._l("common.cancel")}))try{await async function(e,t,i){return e.callWS({type:"homematicip_local/ccu/trigger_install_mode",entry_id:t,interface:i})}(this.hass,this.entryId,e),Ne(this,{message:this._l("ccu.install_mode_activated",{interface:t})}),this._installMode=await Zt(this.hass,this.entryId),this._startInstallModePolling()}catch{Ne(this,{message:this._l("ccu.action_failed")})}}_startInstallModePolling(){this._stopInstallModePolling(),this._installModeTimer=setInterval(async()=>{try{this._installMode=await Zt(this.hass,this.entryId),this._installMode.hmip.active||this._installMode.bidcos.active||this._stopInstallModePolling()}catch{this._stopInstallModePolling()}},1e3)}_stopInstallModePolling(){void 0!==this._installModeTimer&&(clearInterval(this._installModeTimer),this._installModeTimer=void 0)}async _handleRefreshFirmware(){this._refreshingFirmware=!0;try{await async function(e,t){return e.callWS({type:"homematicip_local/ccu/refresh_firmware_data",entry_id:t})}(this.hass,this.entryId),Ne(this,{message:this._l("ccu.firmware_refreshed")}),this._firmware=await qt(this.hass,this.entryId)}catch{Ne(this,{message:this._l("ccu.action_failed")})}finally{this._refreshingFirmware=!1}}render(){return this.entryId?this._loading?W`<div class="loading">${this._l("common.loading")}</div>`:this._error?W`<div class="error">${this._error}</div>`:W`
      ${this._renderSystemInfoCard()} ${this._renderHubDataCard()} ${this._renderInstallModeCard()}
      ${this._renderSignalQualityCard()} ${this._renderFirmwareCard()} ${this._renderActionsCard()}
    `:W`<div class="empty-state">${this._l("device_list.no_entry_selected")}</div>`}_renderSystemInfoCard(){if(!this._sysInfo)return j;const e=this._sysInfo;return W`
      <ha-card>
        <div class="card-header">${this._l("ccu.system_information")}</div>
        <div class="card-content">
          <div class="kv-grid">
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.name")}</span>
              <span class="kv-value">${e.name}</span>
            </div>
            ${e.model?W`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.model")}</span>
                    <span class="kv-value">${e.model}</span>
                  </div>
                `:j}
            ${e.version?W`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.version")}</span>
                    <span class="kv-value">${e.version}</span>
                  </div>
                `:j}
            ${e.serial?W`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.serial")}</span>
                    <span class="kv-value">${e.serial}</span>
                  </div>
                `:j}
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.hostname")}</span>
              <span class="kv-value">${e.hostname}</span>
            </div>
            ${e.ccu_type?W`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.ccu_type")}</span>
                    <span class="kv-value">${e.ccu_type}</span>
                  </div>
                `:j}
            <div class="kv-item">
              <span class="kv-label">${this._l("ccu.interfaces")}</span>
              <span class="kv-value">${e.available_interfaces.join(", ")}</span>
            </div>
            ${null!==e.auth_enabled?W`
                  <div class="kv-item">
                    <span class="kv-label">${this._l("ccu.auth_enabled")}</span>
                    <span class="kv-value"
                      >${this._l(e.auth_enabled?"common.yes":"common.no")}</span
                    >
                  </div>
                `:j}
          </div>
          <div class="status-badges">
            ${e.has_system_update?W`<span class="status-badge update-available"
                  >${this._l("ccu.update_available")}</span
                >`:j}
            ${e.has_backup?W`<span class="status-badge has-backup">${this._l("ccu.backup_exists")}</span>`:j}
          </div>
        </div>
      </ha-card>
    `}_renderHubDataCard(){return this._hubData?W`
      <ha-card>
        <div class="card-header">${this._l("ccu.hub_messages")}</div>
        <div class="card-content">
          <div class="stat-grid">
            <div class="stat-item ${(this._hubData.service_messages??0)>0?"warning":""}">
              <span class="stat-value">${this._hubData.service_messages??"—"}</span>
              <span class="stat-label">${this._l("ccu.service_messages")}</span>
            </div>
            <div class="stat-item ${(this._hubData.alarm_messages??0)>0?"error":""}">
              <span class="stat-value">${this._hubData.alarm_messages??"—"}</span>
              <span class="stat-label">${this._l("ccu.alarm_messages")}</span>
            </div>
          </div>
        </div>
      </ha-card>
    `:j}_renderInstallModeCard(){if(!this._installMode)return j;const{hmip:e,bidcos:t}=this._installMode;return e.available||t.available?W`
      <ha-card>
        <div class="card-header">${this._l("ccu.install_mode")}</div>
        <div class="card-content">
          <div class="install-mode-grid">
            ${e.available?this._renderInstallModeItem("HmIP-RF","hmip",e):j}
            ${t.available?this._renderInstallModeItem("BidCos-RF","bidcos",t):j}
          </div>
        </div>
      </ha-card>
    `:j}_renderInstallModeItem(e,t,i){return W`
      <div class="install-mode-item">
        <div class="install-mode-header">
          <span class="install-mode-label">${e}</span>
          <span class="install-mode-status ${i.active?"active":""}">
            ${this._l(i.active?"ccu.active":"ccu.inactive")}
          </span>
        </div>
        ${i.active&&null!==i.remaining_seconds?W`<span class="install-mode-remaining"
              >${this._l("ccu.remaining_seconds",{seconds:i.remaining_seconds})}</span
            >`:j}
        ${i.active?j:W`
              <ha-button @click=${()=>this._handleTriggerInstallMode(t)}>
                ${this._l("ccu.activate")}
              </ha-button>
            `}
      </div>
    `}_renderSignalQualityCard(){if(!this._signalDevices||0===this._signalDevices.length)return j;const e=[...this._signalDevices].sort((e,t)=>{const i=this._signalSortColumn,s="name"===i?e.name.localeCompare(t.name):(e[i]??-999)-(t[i]??-999);return this._signalSortAsc?s:-s});return W`
      <ha-card>
        <div class="card-header">${this._l("ccu.signal_quality")}</div>
        <div class="card-content table-wrapper">
          <table>
            <thead>
              <tr>
                <th @click=${()=>this._toggleSignalSort("name")}>
                  ${this._l("ccu.device")} ${this._sortIcon("signal","name")}
                </th>
                <th>${this._l("ccu.model")}</th>
                <th>${this._l("ccu.interface")}</th>
                <th>${this._l("ccu.reachable")}</th>
                <th @click=${()=>this._toggleSignalSort("rssi_device")}>
                  RSSI ${this._sortIcon("signal","rssi_device")}
                </th>
                <th @click=${()=>this._toggleSignalSort("signal_strength")}>
                  ${this._l("ccu.signal")} ${this._sortIcon("signal","signal_strength")}
                </th>
                <th>${this._l("ccu.battery")}</th>
              </tr>
            </thead>
            <tbody>
              ${e.map(e=>W`
                  <tr class="${e.is_reachable?"":"unreachable-row"}">
                    <td class="device-name">${e.name}</td>
                    <td>${e.model}</td>
                    <td>${e.interface_id}</td>
                    <td>
                      <span class="status-dot ${e.is_reachable?"online":"offline"}"></span>
                    </td>
                    <td>${e.rssi_device??"—"}</td>
                    <td>${null!==e.signal_strength?`${e.signal_strength}%`:"—"}</td>
                    <td>
                      ${null===e.low_battery?"—":e.low_battery?W`<span class="warn-text">${this._l("ccu.low")}</span>`:this._l("ccu.ok")}
                    </td>
                  </tr>
                `)}
            </tbody>
          </table>
        </div>
      </ha-card>
    `}_renderFirmwareCard(){if(!this._firmware)return j;const e=[...this._firmware.devices].sort((e,t)=>{const i=this._firmwareSortColumn,s=String(e[i]??"").localeCompare(String(t[i]??""));return this._firmwareSortAsc?s:-s});return W`
      <ha-card>
        <div class="card-header">
          <span>${this._l("ccu.firmware_overview")}</span>
          ${this._firmware.summary.firmware_updatable>0?W`<span class="badge"
                >${this._firmware.summary.firmware_updatable} ${this._l("ccu.updatable")}</span
              >`:j}
        </div>
        <div class="card-content table-wrapper">
          <div class="action-bar">
            <ha-button @click=${this._handleRefreshFirmware} .disabled=${this._refreshingFirmware}>
              ${this._l(this._refreshingFirmware?"common.loading":"ccu.refresh_firmware")}
            </ha-button>
          </div>
          <table>
            <thead>
              <tr>
                <th @click=${()=>this._toggleFirmwareSort("name")}>
                  ${this._l("ccu.device")} ${this._sortIcon("firmware","name")}
                </th>
                <th>${this._l("ccu.model")}</th>
                <th @click=${()=>this._toggleFirmwareSort("firmware")}>
                  ${this._l("ccu.current_fw")} ${this._sortIcon("firmware","firmware")}
                </th>
                <th>${this._l("ccu.available_fw")}</th>
                <th @click=${()=>this._toggleFirmwareSort("firmware_update_state")}>
                  ${this._l("ccu.state")} ${this._sortIcon("firmware","firmware_update_state")}
                </th>
              </tr>
            </thead>
            <tbody>
              ${e.map(e=>W`
                  <tr class="${e.firmware_updatable?"updatable-row":""}">
                    <td class="device-name">${e.name}</td>
                    <td>${e.model}</td>
                    <td>${e.firmware}</td>
                    <td>${e.available_firmware??"—"}</td>
                    <td>
                      <span class="fw-state ${e.firmware_updatable?"updatable":""}">
                        ${e.firmware_update_state}
                      </span>
                    </td>
                  </tr>
                `)}
            </tbody>
          </table>
        </div>
      </ha-card>
    `}_renderActionsCard(){return W`
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
    `}_toggleSignalSort(e){this._signalSortColumn===e?this._signalSortAsc=!this._signalSortAsc:(this._signalSortColumn=e,this._signalSortAsc=!0)}_toggleFirmwareSort(e){this._firmwareSortColumn===e?this._firmwareSortAsc=!this._firmwareSortAsc:(this._firmwareSortColumn=e,this._firmwareSortAsc=!0)}_sortIcon(e,t){return("signal"===e?this._signalSortColumn:this._firmwareSortColumn)!==t?"":("signal"===e?this._signalSortAsc:this._firmwareSortAsc)?" ▲":" ▼"}static{this.styles=[ue,r`
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

      .status-badge.update-available {
        background: rgba(var(--rgb-blue, 33, 150, 243), 0.15);
        color: var(--info-color, #2196f3);
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

      .action-bar {
        margin-bottom: 12px;
      }

      .action-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      @media (max-width: 600px) {
        .kv-grid {
          grid-template-columns: 1fr 1fr;
        }

        .install-mode-grid {
          grid-template-columns: 1fr;
        }

        table {
          font-size: 12px;
        }

        thead th,
        tbody td {
          padding: 6px 8px;
        }

        .device-name {
          max-width: 120px;
        }
      }
    `]}};e([he({attribute:!1})],ei.prototype,"hass",void 0),e([he()],ei.prototype,"entryId",void 0),e([pe()],ei.prototype,"_sysInfo",void 0),e([pe()],ei.prototype,"_hubData",void 0),e([pe()],ei.prototype,"_installMode",void 0),e([pe()],ei.prototype,"_signalDevices",void 0),e([pe()],ei.prototype,"_firmware",void 0),e([pe()],ei.prototype,"_loading",void 0),e([pe()],ei.prototype,"_error",void 0),e([pe()],ei.prototype,"_backupRunning",void 0),e([pe()],ei.prototype,"_refreshingFirmware",void 0),e([pe()],ei.prototype,"_signalSortColumn",void 0),e([pe()],ei.prototype,"_signalSortAsc",void 0),e([pe()],ei.prototype,"_firmwareSortColumn",void 0),e([pe()],ei.prototype,"_firmwareSortAsc",void 0),ei=Xt=e([_e("hm-ccu-dashboard")],ei);let ti=class extends oe{constructor(){super(...arguments),this.narrow=!1,this._tab="devices",this._view="device-list",this._entryId="",this._entries=[],this._selectedDevice="",this._selectedInterfaceId="",this._selectedChannel="",this._selectedChannelType="",this._selectedParamsetKey="MASTER",this._selectedDeviceName="",this._selectedSenderAddress="",this._selectedReceiverAddress="",this._senderDeviceName="",this._senderDeviceModel="",this._senderChannelTypeLabel="",this._receiverDeviceName="",this._receiverDeviceModel="",this._receiverChannelTypeLabel="",this._onPopState=()=>{this._parseUrlHash()}}connectedCallback(){super.connectedCallback(),this._resolveEntryId().then(()=>this._parseUrlHash()),window.addEventListener("popstate",this._onPopState)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("popstate",this._onPopState)}_parseUrlHash(){const e=window.location.hash.slice(1);if(!e)return;const t=new URLSearchParams(e),i=t.get("tab"),s=t.get("view"),a=t.get("entry")||this._entryId,n=t.get("device")||"",r=t.get("interface")||"",o=t.get("channel")||"",d=t.get("channel_type")||"",l=t.get("paramset")||"MASTER",c=t.get("sender")||"",h=t.get("receiver")||"";a&&(this._entryId=a),i&&(this._tab=i),s?this._navigateTo(s,{device:n,interfaceId:r,channel:o,channelType:d,paramsetKey:l,senderAddress:c,receiverAddress:h}):i&&this._switchTab(i)}_updateUrlHash(){const e=new URLSearchParams;e.set("tab",this._tab),e.set("view",this._view),this._entryId&&e.set("entry",this._entryId),"device-list"!==this._view&&(this._selectedDevice&&e.set("device",this._selectedDevice),this._selectedInterfaceId&&e.set("interface",this._selectedInterfaceId)),"channel-config"===this._view&&(this._selectedChannel&&e.set("channel",this._selectedChannel),this._selectedChannelType&&e.set("channel_type",this._selectedChannelType),"MASTER"!==this._selectedParamsetKey&&e.set("paramset",this._selectedParamsetKey)),"link-config"===this._view&&(this._selectedSenderAddress&&e.set("sender",this._selectedSenderAddress),this._selectedReceiverAddress&&e.set("receiver",this._selectedReceiverAddress)),"add-link"===this._view&&this._selectedChannel&&e.set("channel",this._selectedChannel);const t=e.toString();window.history.replaceState(null,"",`#${t}`)}async _resolveEntryId(){const e=await this.hass.callWS({type:"config_entries/get",domain:"homematicip_local"});this._entries=e.filter(e=>"loaded"===e.state).map(e=>({entry_id:e.entry_id,title:e.title})),1===this._entries.length&&(this._entryId=this._entries[0].entry_id)}_navigateTo(e,t){this._view=e,void 0!==t?.device&&(this._selectedDevice=t.device),void 0!==t?.interfaceId&&(this._selectedInterfaceId=t.interfaceId),void 0!==t?.channel&&(this._selectedChannel=t.channel),void 0!==t?.channelType&&(this._selectedChannelType=t.channelType),void 0!==t?.paramsetKey&&(this._selectedParamsetKey=t.paramsetKey),void 0!==t?.deviceName&&(this._selectedDeviceName=t.deviceName),void 0!==t?.senderAddress&&(this._selectedSenderAddress=t.senderAddress),void 0!==t?.receiverAddress&&(this._selectedReceiverAddress=t.receiverAddress),void 0!==t?.senderDeviceName&&(this._senderDeviceName=t.senderDeviceName),void 0!==t?.senderDeviceModel&&(this._senderDeviceModel=t.senderDeviceModel),void 0!==t?.senderChannelTypeLabel&&(this._senderChannelTypeLabel=t.senderChannelTypeLabel),void 0!==t?.receiverDeviceName&&(this._receiverDeviceName=t.receiverDeviceName),void 0!==t?.receiverDeviceModel&&(this._receiverDeviceModel=t.receiverDeviceModel),void 0!==t?.receiverChannelTypeLabel&&(this._receiverChannelTypeLabel=t.receiverChannelTypeLabel),this._updateUrlHash()}_switchTab(e){switch(this._tab=e,e){case"devices":this._view="device-list";break;case"integration":this._view="integration-dashboard";break;case"ccu":this._view="ccu-dashboard"}this._updateUrlHash()}_l(e,t){return Me(this.hass,e,t)}_renderTabs(){const e=[{id:"devices",label:this._l("tabs.devices")},{id:"integration",label:this._l("tabs.integration")},{id:"ccu",label:this._l("tabs.ccu")}];return W`
      <div class="tab-bar">
        ${e.map(e=>W`
            <button
              class="tab ${this._tab===e.id?"active":""}"
              @click=${()=>this._switchTab(e.id)}
            >
              ${e.label}
            </button>
          `)}
      </div>
    `}render(){if("integration-dashboard"===this._view)return W`
        ${this._renderTabs()}
        <hm-integration-dashboard
          .hass=${this.hass}
          .entryId=${this._entryId}
        ></hm-integration-dashboard>
      `;if("ccu-dashboard"===this._view)return W`
        ${this._renderTabs()}
        <hm-ccu-dashboard .hass=${this.hass} .entryId=${this._entryId}></hm-ccu-dashboard>
      `;switch(this._view){case"device-list":return W`
          ${this._renderTabs()}
          <hm-device-list
            .hass=${this.hass}
            .entryId=${this._entryId}
            .entries=${this._entries}
            @entry-changed=${e=>{this._entryId=e.detail.entryId,this._updateUrlHash()}}
            @device-selected=${e=>this._navigateTo("device-detail",e.detail)}
          ></hm-device-list>
        `;case"device-detail":return W`
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
        `;case"channel-config":return W`
          <hm-channel-config
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .channelAddress=${this._selectedChannel}
            .channelType=${this._selectedChannelType}
            .paramsetKey=${this._selectedParamsetKey}
            .deviceName=${this._selectedDeviceName}
            @back=${()=>this._navigateTo("device-detail",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
          ></hm-channel-config>
        `;case"change-history":return W`
          <hm-change-history
            .hass=${this.hass}
            .entryId=${this._entryId}
            .filterDevice=${this._selectedDevice}
            @back=${()=>this._navigateTo(this._selectedDevice?"device-detail":"device-list",this._selectedDevice?{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}:void 0)}
          ></hm-change-history>
        `;case"device-links":return W`
          <hm-device-links
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            .deviceName=${this._selectedDeviceName}
            @configure-link=${e=>this._navigateTo("link-config",e.detail)}
            @add-link=${e=>this._navigateTo("add-link",e.detail)}
            @back=${()=>this._navigateTo("device-detail",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
          ></hm-device-links>
        `;case"link-config":return W`
          <hm-link-config
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .senderAddress=${this._selectedSenderAddress}
            .receiverAddress=${this._selectedReceiverAddress}
            .senderDeviceName=${this._senderDeviceName}
            .senderDeviceModel=${this._senderDeviceModel}
            .senderChannelTypeLabel=${this._senderChannelTypeLabel}
            .receiverDeviceName=${this._receiverDeviceName}
            .receiverDeviceModel=${this._receiverDeviceModel}
            .receiverChannelTypeLabel=${this._receiverChannelTypeLabel}
            @back=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
          ></hm-link-config>
        `;case"add-link":return W`
          <hm-add-link
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            @link-created=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
            @back=${()=>this._navigateTo("device-links",{device:this._selectedDevice,interfaceId:this._selectedInterfaceId})}
          ></hm-add-link>
        `;case"device-schedule":return W`
          <hm-device-schedule
            .hass=${this.hass}
            .entryId=${this._entryId}
            .deviceAddress=${this._selectedDevice}
            .deviceName=${this._selectedDeviceName}
            @back=${()=>this._navigateTo(this._selectedDevice?"device-detail":"device-list",this._selectedDevice?{device:this._selectedDevice,interfaceId:this._selectedInterfaceId}:void 0)}
          ></hm-device-schedule>
        `}}static{this.styles=r`
    :host {
      display: block;
      padding: 16px;
      max-width: 1200px;
      margin: 0 auto;
      font-family: var(--paper-font-body1_-_font-family, "Roboto", sans-serif);
      color: var(--primary-text-color);
      background-color: var(--primary-background-color);
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

    @media (max-width: 600px) {
      :host {
        padding: 8px;
      }

      .tab {
        padding: 8px 12px;
        font-size: 13px;
      }
    }
  `}};e([he({attribute:!1})],ti.prototype,"hass",void 0),e([he({attribute:!1})],ti.prototype,"panel",void 0),e([he({type:Boolean,reflect:!0})],ti.prototype,"narrow",void 0),e([pe()],ti.prototype,"_tab",void 0),e([pe()],ti.prototype,"_view",void 0),e([pe()],ti.prototype,"_entryId",void 0),e([pe()],ti.prototype,"_entries",void 0),e([pe()],ti.prototype,"_selectedDevice",void 0),e([pe()],ti.prototype,"_selectedInterfaceId",void 0),e([pe()],ti.prototype,"_selectedChannel",void 0),e([pe()],ti.prototype,"_selectedChannelType",void 0),e([pe()],ti.prototype,"_selectedParamsetKey",void 0),e([pe()],ti.prototype,"_selectedDeviceName",void 0),e([pe()],ti.prototype,"_selectedSenderAddress",void 0),e([pe()],ti.prototype,"_selectedReceiverAddress",void 0),e([pe()],ti.prototype,"_senderDeviceName",void 0),e([pe()],ti.prototype,"_senderDeviceModel",void 0),e([pe()],ti.prototype,"_senderChannelTypeLabel",void 0),e([pe()],ti.prototype,"_receiverDeviceName",void 0),e([pe()],ti.prototype,"_receiverDeviceModel",void 0),e([pe()],ti.prototype,"_receiverChannelTypeLabel",void 0),ti=e([_e("homematic-config")],ti);export{ti as HomematicConfigPanel};
