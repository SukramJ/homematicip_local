function t(t,e,i,s){var r,a=arguments.length,n=a<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,i,s);else for(var o=t.length-1;o>=0;o--)(r=t[o])&&(n=(a<3?r(n):a>3?r(e,i,n):r(e,i))||n);return a>3&&n&&Object.defineProperty(e,i,n),n}"function"==typeof SuppressedError&&SuppressedError;const e=globalThis,i=e.ShadowRoot&&(void 0===e.ShadyCSS||e.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),r=new WeakMap;let a=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(i&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=r.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&r.set(e,t))}return t}toString(){return this.cssText}};const n=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new a(i,t,s)},o=i?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new a("string"==typeof t?t:t+"",void 0,s))(e)})(t):t,{is:c,defineProperty:l,getOwnPropertyDescriptor:h,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:_}=Object,m=globalThis,u=m.trustedTypes,g=u?u.emptyScript:"",v=m.reactiveElementPolyfillSupport,f=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?g:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},$=(t,e)=>!c(t,e),b={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:$};Symbol.metadata??=Symbol("metadata"),m.litPropertyMetadata??=new WeakMap;let w=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=b){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&l(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:r}=h(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const a=s?.call(this);r?.call(this,e),this.requestUpdate(t,a,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??b}static _$Ei(){if(this.hasOwnProperty(f("elementProperties")))return;const t=_(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(f("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(f("properties"))){const t=this.properties,e=[...d(t),...p(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(o(t))}else void 0!==t&&e.push(o(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,s)=>{if(i)t.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const i of s){const s=document.createElement("style"),r=e.litNonce;void 0!==r&&s.setAttribute("nonce",r),s.textContent=i.cssText,t.appendChild(s)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const r=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(e,i.type);this._$Em=t,null==r?this.removeAttribute(s):this.setAttribute(s,r),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),r="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=s;const a=r.fromAttribute(e,t.type);this[s]=a??this._$Ej?.get(s)??a,this._$Em=null}}requestUpdate(t,e,i,s=!1,r){if(void 0!==t){const a=this.constructor;if(!1===s&&(r=this[t]),i??=a.getPropertyOptions(t),!((i.hasChanged??$)(r,e)||i.useDefault&&i.reflect&&r===this._$Ej?.get(t)&&!this.hasAttribute(a._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:r},a){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,a??e??this[t]),!0!==r||void 0!==a)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};w.elementStyles=[],w.shadowRootOptions={mode:"open"},w[f("elementProperties")]=new Map,w[f("finalized")]=new Map,v?.({ReactiveElement:w}),(m.reactiveElementVersions??=[]).push("2.1.2");const S=globalThis,x=t=>t,A=S.trustedTypes,C=A?A.createPolicy("lit-html",{createHTML:t=>t}):void 0,E="$lit$",k=`lit$${Math.random().toFixed(9).slice(2)}$`,P="?"+k,O=`<${P}>`,M=document,T=()=>M.createComment(""),D=t=>null===t||"object"!=typeof t&&"function"!=typeof t,U=Array.isArray,H="[ \t\n\f\r]",L=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,N=/-->/g,R=/>/g,I=RegExp(`>|${H}(?:([^\\s"'>=/]+)(${H}*=${H}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),z=/'/g,j=/"/g,W=/^(?:script|style|textarea|title)$/i,B=(t,...e)=>({_$litType$:1,strings:t,values:e}),K=Symbol.for("lit-noChange"),q=Symbol.for("lit-nothing"),V=new WeakMap,F=M.createTreeWalker(M,129);function G(t,e){if(!U(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==C?C.createHTML(e):e}const Z=(t,e)=>{const i=t.length-1,s=[];let r,a=2===e?"<svg>":3===e?"<math>":"",n=L;for(let e=0;e<i;e++){const i=t[e];let o,c,l=-1,h=0;for(;h<i.length&&(n.lastIndex=h,c=n.exec(i),null!==c);)h=n.lastIndex,n===L?"!--"===c[1]?n=N:void 0!==c[1]?n=R:void 0!==c[2]?(W.test(c[2])&&(r=RegExp("</"+c[2],"g")),n=I):void 0!==c[3]&&(n=I):n===I?">"===c[0]?(n=r??L,l=-1):void 0===c[1]?l=-2:(l=n.lastIndex-c[2].length,o=c[1],n=void 0===c[3]?I:'"'===c[3]?j:z):n===j||n===z?n=I:n===N||n===R?n=L:(n=I,r=void 0);const d=n===I&&t[e+1].startsWith("/>")?" ":"";a+=n===L?i+O:l>=0?(s.push(o),i.slice(0,l)+E+i.slice(l)+k+d):i+k+(-2===l?e:d)}return[G(t,a+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class J{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let r=0,a=0;const n=t.length-1,o=this.parts,[c,l]=Z(t,e);if(this.el=J.createElement(c,i),F.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=F.nextNode())&&o.length<n;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(E)){const e=l[a++],i=s.getAttribute(t).split(k),n=/([.?@])?(.*)/.exec(e);o.push({type:1,index:r,name:n[2],strings:i,ctor:"."===n[1]?et:"?"===n[1]?it:"@"===n[1]?st:tt}),s.removeAttribute(t)}else t.startsWith(k)&&(o.push({type:6,index:r}),s.removeAttribute(t));if(W.test(s.tagName)){const t=s.textContent.split(k),e=t.length-1;if(e>0){s.textContent=A?A.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],T()),F.nextNode(),o.push({type:2,index:++r});s.append(t[e],T())}}}else if(8===s.nodeType)if(s.data===P)o.push({type:2,index:r});else{let t=-1;for(;-1!==(t=s.data.indexOf(k,t+1));)o.push({type:7,index:r}),t+=k.length-1}r++}}static createElement(t,e){const i=M.createElement("template");return i.innerHTML=t,i}}function Q(t,e,i=t,s){if(e===K)return e;let r=void 0!==s?i._$Co?.[s]:i._$Cl;const a=D(e)?void 0:e._$litDirective$;return r?.constructor!==a&&(r?._$AO?.(!1),void 0===a?r=void 0:(r=new a(t),r._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=r:i._$Cl=r),void 0!==r&&(e=Q(t,r._$AS(t,e.values),r,s)),e}class X{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??M).importNode(e,!0);F.currentNode=s;let r=F.nextNode(),a=0,n=0,o=i[0];for(;void 0!==o;){if(a===o.index){let e;2===o.type?e=new Y(r,r.nextSibling,this,t):1===o.type?e=new o.ctor(r,o.name,o.strings,this,t):6===o.type&&(e=new rt(r,this,t)),this._$AV.push(e),o=i[++n]}a!==o?.index&&(r=F.nextNode(),a++)}return F.currentNode=M,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class Y{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=q,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=Q(this,t,e),D(t)?t===q||null==t||""===t?(this._$AH!==q&&this._$AR(),this._$AH=q):t!==this._$AH&&t!==K&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>U(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==q&&D(this._$AH)?this._$AA.nextSibling.data=t:this.T(M.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=J.createElement(G(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new X(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=V.get(t.strings);return void 0===e&&V.set(t.strings,e=new J(t)),e}k(t){U(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const r of t)s===e.length?e.push(i=new Y(this.O(T()),this.O(T()),this,this.options)):i=e[s],i._$AI(r),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=x(t).nextSibling;x(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class tt{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,r){this.type=1,this._$AH=q,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=r,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=q}_$AI(t,e=this,i,s){const r=this.strings;let a=!1;if(void 0===r)t=Q(this,t,e,0),a=!D(t)||t!==this._$AH&&t!==K,a&&(this._$AH=t);else{const s=t;let n,o;for(t=r[0],n=0;n<r.length-1;n++)o=Q(this,s[i+n],e,n),o===K&&(o=this._$AH[n]),a||=!D(o)||o!==this._$AH[n],o===q?t=q:t!==q&&(t+=(o??"")+r[n+1]),this._$AH[n]=o}a&&!s&&this.j(t)}j(t){t===q?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class et extends tt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===q?void 0:t}}class it extends tt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==q)}}class st extends tt{constructor(t,e,i,s,r){super(t,e,i,s,r),this.type=5}_$AI(t,e=this){if((t=Q(this,t,e,0)??q)===K)return;const i=this._$AH,s=t===q&&i!==q||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,r=t!==q&&(i===q||s);s&&this.element.removeEventListener(this.name,this,i),r&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class rt{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){Q(this,t)}}const at=S.litHtmlPolyfillSupport;at?.(J,Y),(S.litHtmlVersions??=[]).push("3.3.2");const nt=globalThis;class ot extends w{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let r=s._$litPart$;if(void 0===r){const t=i?.renderBefore??null;s._$litPart$=r=new Y(e.insertBefore(T(),t),t,void 0,i??{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return K}}ot._$litElement$=!0,ot.finalized=!0,nt.litElementHydrateSupport?.({LitElement:ot});const ct=nt.litElementPolyfillSupport;ct?.({LitElement:ot}),(nt.litElementVersions??=[]).push("4.2.2");const lt=t=>(e,i)=>{void 0!==i?i.addInitializer(()=>{customElements.define(t,e)}):customElements.define(t,e)},ht={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:$},dt=(t=ht,e,i)=>{const{kind:s,metadata:r}=i;let a=globalThis.litPropertyMetadata.get(r);if(void 0===a&&globalThis.litPropertyMetadata.set(r,a=new Map),"setter"===s&&((t=Object.create(t)).wrapped=!0),a.set(i.name,t),"accessor"===s){const{name:s}=i;return{set(i){const r=e.get.call(this);e.set.call(this,i),this.requestUpdate(s,r,t,!0,i)},init(e){return void 0!==e&&this.C(s,void 0,t,e),e}}}if("setter"===s){const{name:s}=i;return function(i){const r=this[s];e.call(this,i),this.requestUpdate(s,r,t,!0,i)}}throw Error("Unsupported decorator location: "+s)};function pt(t){return(e,i)=>"object"==typeof i?dt(t,e,i):((t,e,i)=>{const s=e.hasOwnProperty(i);return e.constructor.createProperty(i,t),s?Object.getOwnPropertyDescriptor(e,i):void 0})(t,e,i)}function _t(t){return pt({...t,state:!0,attribute:!1})}async function mt(t,e){return t.callWS({type:"homematicip_local/integration/get_system_health",entry_id:e})}async function ut(t,e,i=50,s){return t.callWS({type:"homematicip_local/integration/get_incidents",entry_id:e,limit:i,...s})}async function gt(t,e){return t.callWS({type:"homematicip_local/integration/get_device_statistics",entry_id:e})}const vt=n`
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
`,ft={en:{systemHealth:"System Health",centralState:"Status",healthScore:"Health",devices:"Devices",unreachable:"Unreachable",firmwareUpdates:"FW Updates",incidents:"Incidents",noIncidents:"No incidents",throttleActive:"Throttle active",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Device Status",problems:"Problems",allDevicesOk:"All devices OK",notReachable:"Not reachable",lowBattery:"Low battery",configPending:"Config pending",devicesOk:"{count} devices OK",noDevices:"No devices found",messages:"Messages",alarms:"Alarms",serviceMessages:"Service",acknowledge:"Acknowledge",noMessages:"No service messages",noAlarms:"No alarms",loading:"Loading...",error:"Error loading data",refresh:"Refresh"},de:{systemHealth:"Systemstatus",centralState:"Status",healthScore:"Zustand",devices:"Geräte",unreachable:"Nicht erreichbar",firmwareUpdates:"FW-Updates",incidents:"Vorfälle",noIncidents:"Keine Vorfälle",throttleActive:"Drosselung aktiv",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Gerätestatus",problems:"Probleme",allDevicesOk:"Alle Geräte OK",notReachable:"Nicht erreichbar",lowBattery:"Batterie niedrig",configPending:"Konfiguration ausstehend",devicesOk:"{count} Geräte OK",noDevices:"Keine Geräte gefunden",messages:"Meldungen",alarms:"Alarme",serviceMessages:"Service",acknowledge:"Quittieren",noMessages:"Keine Servicemeldungen",noAlarms:"Keine Alarme",loading:"Laden...",error:"Fehler beim Laden",refresh:"Aktualisieren"}};function yt(t){return ft[t]||ft.en}let $t=class extends ot{constructor(){super(...arguments),this._loading=!0,this._error=""}static{this.styles=vt}setConfig(t){this._config={show_incidents:!1,max_incidents:5,show_throttle:!1,poll_interval:30,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=yt(this.hass.config.language))}_startPolling(t){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),t)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(!this.hass||!this._config||!this._config.entry_id)return;try{const t=this._config.show_incidents?this._config.max_incidents:0,[e,i,s]=await Promise.all([mt(this.hass,this._config.entry_id),gt(this.hass,this._config.entry_id),t>0?ut(this.hass,this._config.entry_id,t):Promise.resolve(void 0)]);this._health=e,this._deviceStats=i,s&&(this._incidents=s),this._entryEntityIds||await this._loadEntryEntityIds(),this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}const t="running"===this._health?.central_state?.toLowerCase();this._startPolling(t?Math.max(1e3*(this._config.poll_interval??30),3e4):5e3)}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.systemHealth;return this._loading?B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&!this._health?B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:B`
      <ha-card>
        <div class="card-header">
          ${t}
          <div class="badges">${this._renderStatusBadge()}</div>
        </div>
        <div class="card-content">
          ${this._renderStats()} ${this._renderRadioLevels()} ${this._renderIncidents()}
        </div>
      </ha-card>
    `}_renderStatusBadge(){if(!this._health)return q;const t=this._health.central_state,e="running"===t?.toLowerCase(),i=Math.round(100*this._health.overall_health_score);return B` <span class="badge ${e?"ok":"error"}">${i}%</span> `}_renderStats(){if(!this._deviceStats)return q;const t=this._deviceStats;return B`
      <div class="stat-grid">
        <div class="stat-item">
          <div class="stat-value">${t.total_devices}</div>
          <div class="stat-label">${this._t.devices}</div>
        </div>
        <div class="stat-item ${t.unreachable_devices>0?"error":""}">
          <div class="stat-value">${t.unreachable_devices}</div>
          <div class="stat-label">${this._t.unreachable}</div>
        </div>
        <div class="stat-item ${t.firmware_updatable_devices>0?"warning":""}">
          <div class="stat-value">${t.firmware_updatable_devices}</div>
          <div class="stat-label">${this._t.firmwareUpdates}</div>
        </div>
      </div>
    `}async _loadEntryEntityIds(){this.hass&&this._config&&(this._entryEntityIds=await async function(t,e){try{const i=await t.callWS({type:"config/entity_registry/list"});return new Set(i.filter(t=>t.config_entry_id===e).map(t=>t.entity_id))}catch{return}}(this.hass,this._config.entry_id))}_renderRadioLevels(){const t=function(t,e){if(!t)return[];const i=new Map;for(const[s,r]of Object.entries(t)){if(!s.startsWith("sensor."))continue;const t=s.endsWith("_duty_cycle_level"),a=s.endsWith("_carrier_sense_level");if(!t&&!a)continue;if(e&&!e.has(s))continue;const n=r.attributes,o=n?.friendly_name||s,c=s.replace(/_(?:duty_cycle|carrier_sense)_level$/,""),l=o.replace(/\s*Duty Cycle Level$/i,"").replace(/\s*Carrier Sense Level$/i,"").replace(/\s*DutyCycle Level$/i,"").replace(/\s*CarrierSense Level$/i,"");i.has(c)||i.set(c,{name:l,dutyCycle:null,carrierSense:null});const h=i.get(c),d=parseFloat(r.state);isNaN(d)||(t&&(h.dutyCycle=d),a&&(h.carrierSense=d))}return[...i.values()].sort((t,e)=>t.name.localeCompare(e.name))}(this.hass?.states,this._entryEntityIds);return 0===t.length?q:B`
      <div class="section-title">${this._t.dutyCycle} / ${this._t.carrierSense}</div>
      <div class="item-list">
        ${t.map(t=>{return B`
            <div class="item-row">
              <ha-icon class="item-icon" .icon=${"mdi:radio-tower"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${t.name}</div>
                <div class="item-secondary">
                  ${null!==t.dutyCycle?B`<span class="${e=t.dutyCycle,null===e?"":e>=80?"error":e>=60?"warning":""}">DC: ${t.dutyCycle}%</span>`:q}
                  ${null!==t.dutyCycle&&null!==t.carrierSense?" · ":q}
                  ${null!==t.carrierSense?B`<span class="${function(t){return null===t?"":t>=10?"error":""}(t.carrierSense)}"
                        >CS: ${t.carrierSense}%</span
                      >`:q}
                </div>
              </div>
            </div>
          `;var e})}
      </div>
    `}_renderIncidents(){if(!this._config?.show_incidents||!this._incidents)return q;const t=this._incidents.summary.total_incidents;return 0===t?B`<div class="empty-state">${this._t.noIncidents}</div>`:B`
      <div class="section-title">
        ${this._t.incidents}
        <span class="badge warning">${t}</span>
      </div>
      <div class="item-list">
        ${this._incidents.incidents.map(t=>B`
            <div class="item-row ${this._incidentSeverity(t)}">
              <ha-icon class="item-icon" .icon=${this._incidentIcon(t)}></ha-icon>
              <div class="item-content">
                <div class="item-primary">
                  ${t.message||t.type}
                </div>
                <div class="item-secondary">
                  ${this._formatTimestamp(t.timestamp)}
                </div>
              </div>
            </div>
          `)}
      </div>
    `}_incidentSeverity(t){const e=String(t.severity||"info").toLowerCase();return"error"===e||"critical"===e?"error":"warning"===e?"warning":""}_incidentIcon(t){const e=String(t.severity||"info").toLowerCase();return"error"===e||"critical"===e?"mdi:alert-circle":"warning"===e?"mdi:alert":"mdi:information"}_formatTimestamp(t){if(!t)return"";try{return new Date(t).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return t}}static getConfigElement(){return document.createElement("homematicip-system-health-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};async function bt(t){try{return(await t.callWS({type:"config_entries/get",domain:"homematicip_local"})).map(t=>({value:t.entry_id,label:t.title}))}catch{return[]}}t([pt({attribute:!1})],$t.prototype,"hass",void 0),t([_t()],$t.prototype,"_config",void 0),t([_t()],$t.prototype,"_health",void 0),t([_t()],$t.prototype,"_deviceStats",void 0),t([_t()],$t.prototype,"_incidents",void 0),t([_t()],$t.prototype,"_entryEntityIds",void 0),t([_t()],$t.prototype,"_loading",void 0),t([_t()],$t.prototype,"_error",void 0),$t=t([lt("homematicip-system-health-card")],$t);let wt=class extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",show_incidents:"Show incidents",max_incidents:"Max incidents",poll_interval:"Poll interval"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_incidents",selector:{boolean:{}},default:!1},{name:"max_incidents",selector:{number:{min:1,max:50,mode:"box"}},default:5},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){var e;t.stopPropagation(),e={config:{...this._config,...t.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:e}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};t([pt({attribute:!1})],wt.prototype,"hass",void 0),t([_t()],wt.prototype,"_config",void 0),t([_t()],wt.prototype,"_entryOptions",void 0),wt=t([lt("homematicip-system-health-editor")],wt);let St=class extends ot{constructor(){super(...arguments),this._devices=[],this._totalDevices=0,this._problemCount=0,this._loading=!0,this._error=""}static{this.styles=vt}setConfig(t){this._config={filter:"problems",show_model:!0,max_devices:10,poll_interval:60,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=yt(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??60))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{let t=await async function(t,e){return(await t.callWS({type:"homematicip_local/config/list_devices",entry_id:e})).devices}(this.hass,this._config.entry_id);this._config.interface_filter&&(t=t.filter(t=>t.interface_id===this._config.interface_filter)),this._totalDevices=t.length,this._devices=this._filterDevices(t),this._problemCount=this._devices.filter(t=>"ok"!==t.severity).length,this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}this._startPolling()}}_filterDevices(t){const e=this._config?.filter??"problems",i=[];for(const s of t){const t=s.maintenance,r=[];let a="ok";!t.unreach||"all"!==e&&"problems"!==e&&"unreachable"!==e||(r.push(this._t?.notReachable??"Not reachable"),a="error"),!t.low_bat||"all"!==e&&"problems"!==e&&"low_battery"!==e||(r.push(this._t?.lowBattery??"Low battery"),"ok"===a&&(a="warning")),!t.config_pending||"all"!==e&&"problems"!==e&&"config_pending"!==e||(r.push(this._t?.configPending??"Config pending"),"ok"===a&&(a="warning")),("all"===e||r.length>0)&&i.push({device:s,issues:r,severity:a})}const s={error:0,warning:1,ok:2};i.sort((t,e)=>{const i=s[t.severity]-s[e.severity];return 0!==i?i:t.device.name.localeCompare(e.device.name)});const r=this._config?.max_devices??10;return r>0?i.slice(0,r):i}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.deviceStatus;return this._loading?B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&0===this._totalDevices?B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:B`
      <ha-card>
        <div class="card-header">
          ${t}
          <div class="badges">
            ${this._problemCount>0?B`<span class="badge error">${this._problemCount} ${this._t.problems}</span>`:B`<span class="badge ok">OK</span>`}
          </div>
        </div>
        <div class="card-content">
          ${this._devices.length>0?this._renderDevices():this._renderAllOk()}
        </div>
      </ha-card>
    `}_deviceIcon(t){return"error"===t?"mdi:close-circle":"warning"===t?"mdi:alert":"mdi:check-circle"}_renderDevices(){const t=this._totalDevices-this._devices.length;return B`
      <div class="item-list">
        ${this._devices.map(t=>B`
            <div class="item-row ${t.severity}">
              <ha-icon class="item-icon" .icon=${this._deviceIcon(t.severity)}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${t.device.name}</div>
                <div class="item-secondary">
                  ${this._config?.show_model?`${t.device.model}`:""}${t.issues.length>0?`${this._config?.show_model?" · ":""}${t.issues.join(", ")}`:""}
                </div>
              </div>
            </div>
          `)}
      </div>
      ${t>0?B`<div class="summary-line">+ ${t} ${this._t.devices}</div>`:q}
    `}_renderAllOk(){return B`<div class="empty-state">${this._t.allDevicesOk}</div>`}static getConfigElement(){return document.createElement("homematicip-device-status-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};t([pt({attribute:!1})],St.prototype,"hass",void 0),t([_t()],St.prototype,"_config",void 0),t([_t()],St.prototype,"_devices",void 0),t([_t()],St.prototype,"_totalDevices",void 0),t([_t()],St.prototype,"_problemCount",void 0),t([_t()],St.prototype,"_loading",void 0),t([_t()],St.prototype,"_error",void 0),St=t([lt("homematicip-device-status-card")],St);let xt=class extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",filter:"Filter",show_model:"Show device model",max_devices:"Max devices (0 = all)",poll_interval:"Poll interval",interface_filter:"Interface filter (optional)"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"filter",selector:{select:{options:[{value:"problems",label:"Problems only"},{value:"all",label:"All devices"},{value:"unreachable",label:"Unreachable"},{value:"low_battery",label:"Low battery"},{value:"config_pending",label:"Config pending"}],mode:"dropdown"}},default:"problems"},{name:"show_model",selector:{boolean:{}},default:!0},{name:"max_devices",selector:{number:{min:0,max:100,mode:"box"}},default:10},{name:"poll_interval",selector:{number:{min:10,max:600,mode:"box",unit_of_measurement:"s"}},default:60},{name:"interface_filter",selector:{text:{}}}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${{...this._config,filter:this._config.filter||"problems"}}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){t.stopPropagation();const e={...this._config,...t.detail.value};e.interface_filter||delete e.interface_filter,this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:{config:e}}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};t([pt({attribute:!1})],xt.prototype,"hass",void 0),t([_t()],xt.prototype,"_config",void 0),t([_t()],xt.prototype,"_entryOptions",void 0),xt=t([lt("homematicip-device-status-editor")],xt);let At=class extends ot{constructor(){super(...arguments),this._serviceMessages=[],this._alarmMessages=[],this._loading=!0,this._error=""}static{this.styles=vt}setConfig(t){this._config={show_service:!0,show_alarms:!0,max_messages:10,show_timestamp:!0,compact:!1,poll_interval:30,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=yt(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??30))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{const t=[];this._config.show_service&&t.push(async function(t,e){return(await t.callWS({type:"homematicip_local/ccu/get_service_messages",entry_id:e})).messages}(this.hass,this._config.entry_id).then(t=>this._serviceMessages=t)),this._config.show_alarms&&t.push(async function(t,e){return(await t.callWS({type:"homematicip_local/ccu/get_alarm_messages",entry_id:e})).alarms}(this.hass,this._config.entry_id).then(t=>this._alarmMessages=t)),await Promise.all(t),this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}this._startPolling()}}async _acknowledgeService(t){if(this.hass&&this._config)try{await async function(t,e,i){return t.callWS({type:"homematicip_local/ccu/acknowledge_service_message",entry_id:e,msg_id:i})}(this.hass,this._config.entry_id,t),this._serviceMessages=this._serviceMessages.filter(e=>e.msg_id!==t)}catch{}}async _acknowledgeAlarm(t){if(this.hass&&this._config)try{await async function(t,e,i){return t.callWS({type:"homematicip_local/ccu/acknowledge_alarm_message",entry_id:e,alarm_id:i})}(this.hass,this._config.entry_id,t),this._alarmMessages=this._alarmMessages.filter(e=>e.alarm_id!==t)}catch{}}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.messages;if(this._loading)return B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `;if(this._error&&0===this._serviceMessages.length&&0===this._alarmMessages.length)return B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `;const e=this._alarmMessages.length,i=this._serviceMessages.length;return B`
      <ha-card>
        <div class="card-header">
          ${t}
          <div class="badges">
            ${e>0?B`<span class="badge error">${e}</span>`:q}
            ${i>0?B`<span class="badge warning">${i}</span>`:q}
            ${0===e&&0===i?B`<span class="badge ok">OK</span>`:q}
          </div>
        </div>
        <div class="card-content">
          ${this._renderAlarms()} ${this._renderServiceMessages()}
          ${0===e&&0===i?B`<div class="empty-state">${this._t.noMessages}</div>`:q}
        </div>
      </ha-card>
    `}_renderAlarms(){if(!this._config?.show_alarms||0===this._alarmMessages.length)return q;const t=this._alarmMessages.slice(0,this._config.max_messages??10);return B`
      <div class="section-title">${this._t.alarms}</div>
      <div class="item-list">
        ${t.map(t=>B`
            <div class="item-row error">
              <ha-icon class="item-icon" .icon=${"mdi:bell-alert"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${t.device_name||t.name}</div>
                <div class="item-secondary">
                  ${t.display_name}${t.counter>1?` · ${t.counter}x`:""}${this._config?.show_timestamp?` · ${this._formatTimestamp(t.timestamp)}`:""}
                </div>
              </div>
              <div class="item-action">
                <ha-icon-button
                  .label=${this._t.acknowledge}
                  @click=${()=>this._acknowledgeAlarm(t.alarm_id)}
                >
                  <ha-icon .icon=${"mdi:check"}></ha-icon>
                </ha-icon-button>
              </div>
            </div>
          `)}
      </div>
    `}_renderServiceMessages(){if(!this._config?.show_service||0===this._serviceMessages.length)return q;const t=this._serviceMessages.slice(0,this._config.max_messages??10);return B`
      <div class="section-title">${this._t.serviceMessages}</div>
      <div class="item-list">
        ${t.map(t=>B`
            <div class="item-row warning">
              <ha-icon class="item-icon" .icon=${"mdi:alert"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${t.device_name||t.name}</div>
                <div class="item-secondary">
                  ${t.message_code}${t.counter>1?` · ${t.counter}x`:""}${this._config?.show_timestamp?` · ${this._formatTimestamp(t.timestamp)}`:""}
                </div>
              </div>
              ${t.quittable?B`
                    <div class="item-action">
                      <ha-icon-button
                        .label=${this._t.acknowledge}
                        @click=${()=>this._acknowledgeService(t.msg_id)}
                      >
                        <ha-icon .icon=${"mdi:check"}></ha-icon>
                      </ha-icon-button>
                    </div>
                  `:q}
            </div>
          `)}
      </div>
    `}_formatTimestamp(t){if(!t)return"";try{return new Date(t).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return t}}static getConfigElement(){return document.createElement("homematicip-messages-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};t([pt({attribute:!1})],At.prototype,"hass",void 0),t([_t()],At.prototype,"_config",void 0),t([_t()],At.prototype,"_serviceMessages",void 0),t([_t()],At.prototype,"_alarmMessages",void 0),t([_t()],At.prototype,"_loading",void 0),t([_t()],At.prototype,"_error",void 0),At=t([lt("homematicip-messages-card")],At);let Ct=class extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",show_alarms:"Show alarms",show_service:"Show service messages",max_messages:"Max messages",show_timestamp:"Show timestamps",poll_interval:"Poll interval"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_alarms",selector:{boolean:{}},default:!0},{name:"show_service",selector:{boolean:{}},default:!0},{name:"max_messages",selector:{number:{min:1,max:50,mode:"box"}},default:10},{name:"show_timestamp",selector:{boolean:{}},default:!0},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){var e;t.stopPropagation(),e={config:{...this._config,...t.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:e}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};t([pt({attribute:!1})],Ct.prototype,"hass",void 0),t([_t()],Ct.prototype,"_config",void 0),t([_t()],Ct.prototype,"_entryOptions",void 0),Ct=t([lt("homematicip-messages-editor")],Ct),window.customCards=window.customCards||[],window.customCards.push({type:"homematicip-system-health-card",name:"HomematicIP System Health",description:"System health, device statistics, and incidents for HomematicIP Local"}),window.customCards.push({type:"homematicip-device-status-card",name:"HomematicIP Device Status",description:"Device status overview with problem highlighting for HomematicIP Local"}),window.customCards.push({type:"homematicip-messages-card",name:"HomematicIP Messages",description:"Service messages and alarms with acknowledgment for HomematicIP Local"});
