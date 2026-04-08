function e(e,t,s,i){var r,a=arguments.length,n=a<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,s):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,s,i);else for(var o=e.length-1;o>=0;o--)(r=e[o])&&(n=(a<3?r(n):a>3?r(t,s,n):r(t,s))||n);return a>3&&n&&Object.defineProperty(t,s,n),n}"function"==typeof SuppressedError&&SuppressedError;const t=globalThis,s=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),r=new WeakMap;let a=class{constructor(e,t,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;const t=this.t;if(s&&void 0===e){const s=void 0!==t&&1===t.length;s&&(e=r.get(t)),void 0===e&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),s&&r.set(t,e))}return e}toString(){return this.cssText}};const n=(e,...t)=>{const s=1===e.length?e[0]:t.reduce((t,s,i)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+e[i+1],e[0]);return new a(s,e,i)},o=s?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const s of e.cssRules)t+=s.cssText;return(e=>new a("string"==typeof e?e:e+"",void 0,i))(t)})(e):e,{is:c,defineProperty:l,getOwnPropertyDescriptor:h,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:_}=Object,m=globalThis,u=m.trustedTypes,g=u?u.emptyScript:"",v=m.reactiveElementPolyfillSupport,f=(e,t)=>e,y={toAttribute(e,t){switch(t){case Boolean:e=e?g:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let s=e;switch(t){case Boolean:s=null!==e;break;case Number:s=null===e?null:Number(e);break;case Object:case Array:try{s=JSON.parse(e)}catch(e){s=null}}return s}},$=(e,t)=>!c(e,t),b={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:$};Symbol.metadata??=Symbol("metadata"),m.litPropertyMetadata??=new WeakMap;let w=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=b){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){const s=Symbol(),i=this.getPropertyDescriptor(e,s,t);void 0!==i&&l(this.prototype,e,i)}}static getPropertyDescriptor(e,t,s){const{get:i,set:r}=h(this.prototype,e)??{get(){return this[t]},set(e){this[t]=e}};return{get:i,set(t){const a=i?.call(this);r?.call(this,t),this.requestUpdate(e,a,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??b}static _$Ei(){if(this.hasOwnProperty(f("elementProperties")))return;const e=_(this);e.finalize(),void 0!==e.l&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(f("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(f("properties"))){const e=this.properties,t=[...d(e),...p(e)];for(const s of t)this.createProperty(s,e[s])}const e=this[Symbol.metadata];if(null!==e){const t=litPropertyMetadata.get(e);if(void 0!==t)for(const[e,s]of t)this.elementProperties.set(e,s)}this._$Eh=new Map;for(const[e,t]of this.elementProperties){const s=this._$Eu(e,t);void 0!==s&&this._$Eh.set(s,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const s=new Set(e.flat(1/0).reverse());for(const e of s)t.unshift(o(e))}else void 0!==e&&t.push(o(e));return t}static _$Eu(e,t){const s=t.attribute;return!1===s?void 0:"string"==typeof s?s:"string"==typeof e?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),void 0!==this.renderRoot&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){const e=new Map,t=this.constructor.elementProperties;for(const s of t.keys())this.hasOwnProperty(s)&&(e.set(s,this[s]),delete this[s]);e.size>0&&(this._$Ep=e)}createRenderRoot(){const e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((e,i)=>{if(s)e.adoptedStyleSheets=i.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const s of i){const i=document.createElement("style"),r=t.litNonce;void 0!==r&&i.setAttribute("nonce",r),i.textContent=s.cssText,e.appendChild(i)}})(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,s){this._$AK(e,s)}_$ET(e,t){const s=this.constructor.elementProperties.get(e),i=this.constructor._$Eu(e,s);if(void 0!==i&&!0===s.reflect){const r=(void 0!==s.converter?.toAttribute?s.converter:y).toAttribute(t,s.type);this._$Em=e,null==r?this.removeAttribute(i):this.setAttribute(i,r),this._$Em=null}}_$AK(e,t){const s=this.constructor,i=s._$Eh.get(e);if(void 0!==i&&this._$Em!==i){const e=s.getPropertyOptions(i),r="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==e.converter?.fromAttribute?e.converter:y;this._$Em=i;const a=r.fromAttribute(t,e.type);this[i]=a??this._$Ej?.get(i)??a,this._$Em=null}}requestUpdate(e,t,s,i=!1,r){if(void 0!==e){const a=this.constructor;if(!1===i&&(r=this[e]),s??=a.getPropertyOptions(e),!((s.hasChanged??$)(r,t)||s.useDefault&&s.reflect&&r===this._$Ej?.get(e)&&!this.hasAttribute(a._$Eu(e,s))))return;this.C(e,t,s)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(e,t,{useDefault:s,reflect:i,wrapped:r},a){s&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,a??t??this[e]),!0!==r||void 0!==a)||(this._$AL.has(e)||(this.hasUpdated||s||(t=void 0),this._$AL.set(e,t)),!0===i&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[e,t]of this._$Ep)this[e]=t;this._$Ep=void 0}const e=this.constructor.elementProperties;if(e.size>0)for(const[t,s]of e){const{wrapped:e}=s,i=this[t];!0!==e||this._$AL.has(t)||void 0===i||this.C(t,void 0,s,i)}}let e=!1;const t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(e=>e.hostUpdate?.()),this.update(t)):this._$EM()}catch(t){throw e=!1,this._$EM(),t}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(e){}firstUpdated(e){}};w.elementStyles=[],w.shadowRootOptions={mode:"open"},w[f("elementProperties")]=new Map,w[f("finalized")]=new Map,v?.({ReactiveElement:w}),(m.reactiveElementVersions??=[]).push("2.1.2");const S=globalThis,x=e=>e,A=S.trustedTypes,C=A?A.createPolicy("lit-html",{createHTML:e=>e}):void 0,E="$lit$",k=`lit$${Math.random().toFixed(9).slice(2)}$`,P="?"+k,O=`<${P}>`,M=document,T=()=>M.createComment(""),D=e=>null===e||"object"!=typeof e&&"function"!=typeof e,U=Array.isArray,H="[ \t\n\f\r]",L=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,R=/-->/g,N=/>/g,I=RegExp(`>|${H}(?:([^\\s"'>=/]+)(${H}*=${H}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),z=/'/g,j=/"/g,W=/^(?:script|style|textarea|title)$/i,B=(e,...t)=>({_$litType$:1,strings:e,values:t}),q=Symbol.for("lit-noChange"),K=Symbol.for("lit-nothing"),V=new WeakMap,F=M.createTreeWalker(M,129);function G(e,t){if(!U(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==C?C.createHTML(t):t}const Z=(e,t)=>{const s=e.length-1,i=[];let r,a=2===t?"<svg>":3===t?"<math>":"",n=L;for(let t=0;t<s;t++){const s=e[t];let o,c,l=-1,h=0;for(;h<s.length&&(n.lastIndex=h,c=n.exec(s),null!==c);)h=n.lastIndex,n===L?"!--"===c[1]?n=R:void 0!==c[1]?n=N:void 0!==c[2]?(W.test(c[2])&&(r=RegExp("</"+c[2],"g")),n=I):void 0!==c[3]&&(n=I):n===I?">"===c[0]?(n=r??L,l=-1):void 0===c[1]?l=-2:(l=n.lastIndex-c[2].length,o=c[1],n=void 0===c[3]?I:'"'===c[3]?j:z):n===j||n===z?n=I:n===R||n===N?n=L:(n=I,r=void 0);const d=n===I&&e[t+1].startsWith("/>")?" ":"";a+=n===L?s+O:l>=0?(i.push(o),s.slice(0,l)+E+s.slice(l)+k+d):s+k+(-2===l?t:d)}return[G(e,a+(e[s]||"<?>")+(2===t?"</svg>":3===t?"</math>":"")),i]};class J{constructor({strings:e,_$litType$:t},s){let i;this.parts=[];let r=0,a=0;const n=e.length-1,o=this.parts,[c,l]=Z(e,t);if(this.el=J.createElement(c,s),F.currentNode=this.el.content,2===t||3===t){const e=this.el.content.firstChild;e.replaceWith(...e.childNodes)}for(;null!==(i=F.nextNode())&&o.length<n;){if(1===i.nodeType){if(i.hasAttributes())for(const e of i.getAttributeNames())if(e.endsWith(E)){const t=l[a++],s=i.getAttribute(e).split(k),n=/([.?@])?(.*)/.exec(t);o.push({type:1,index:r,name:n[2],strings:s,ctor:"."===n[1]?te:"?"===n[1]?se:"@"===n[1]?ie:ee}),i.removeAttribute(e)}else e.startsWith(k)&&(o.push({type:6,index:r}),i.removeAttribute(e));if(W.test(i.tagName)){const e=i.textContent.split(k),t=e.length-1;if(t>0){i.textContent=A?A.emptyScript:"";for(let s=0;s<t;s++)i.append(e[s],T()),F.nextNode(),o.push({type:2,index:++r});i.append(e[t],T())}}}else if(8===i.nodeType)if(i.data===P)o.push({type:2,index:r});else{let e=-1;for(;-1!==(e=i.data.indexOf(k,e+1));)o.push({type:7,index:r}),e+=k.length-1}r++}}static createElement(e,t){const s=M.createElement("template");return s.innerHTML=e,s}}function Q(e,t,s=e,i){if(t===q)return t;let r=void 0!==i?s._$Co?.[i]:s._$Cl;const a=D(t)?void 0:t._$litDirective$;return r?.constructor!==a&&(r?._$AO?.(!1),void 0===a?r=void 0:(r=new a(e),r._$AT(e,s,i)),void 0!==i?(s._$Co??=[])[i]=r:s._$Cl=r),void 0!==r&&(t=Q(e,r._$AS(e,t.values),r,i)),t}class X{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){const{el:{content:t},parts:s}=this._$AD,i=(e?.creationScope??M).importNode(t,!0);F.currentNode=i;let r=F.nextNode(),a=0,n=0,o=s[0];for(;void 0!==o;){if(a===o.index){let t;2===o.type?t=new Y(r,r.nextSibling,this,e):1===o.type?t=new o.ctor(r,o.name,o.strings,this,e):6===o.type&&(t=new re(r,this,e)),this._$AV.push(t),o=s[++n]}a!==o?.index&&(r=F.nextNode(),a++)}return F.currentNode=M,i}p(e){let t=0;for(const s of this._$AV)void 0!==s&&(void 0!==s.strings?(s._$AI(e,s,t),t+=s.strings.length-2):s._$AI(e[t])),t++}}class Y{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,s,i){this.type=2,this._$AH=K,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=s,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e?.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=Q(this,e,t),D(e)?e===K||null==e||""===e?(this._$AH!==K&&this._$AR(),this._$AH=K):e!==this._$AH&&e!==q&&this._(e):void 0!==e._$litType$?this.$(e):void 0!==e.nodeType?this.T(e):(e=>U(e)||"function"==typeof e?.[Symbol.iterator])(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==K&&D(this._$AH)?this._$AA.nextSibling.data=e:this.T(M.createTextNode(e)),this._$AH=e}$(e){const{values:t,_$litType$:s}=e,i="number"==typeof s?this._$AC(e):(void 0===s.el&&(s.el=J.createElement(G(s.h,s.h[0]),this.options)),s);if(this._$AH?._$AD===i)this._$AH.p(t);else{const e=new X(i,this),s=e.u(this.options);e.p(t),this.T(s),this._$AH=e}}_$AC(e){let t=V.get(e.strings);return void 0===t&&V.set(e.strings,t=new J(e)),t}k(e){U(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let s,i=0;for(const r of e)i===t.length?t.push(s=new Y(this.O(T()),this.O(T()),this,this.options)):s=t[i],s._$AI(r),i++;i<t.length&&(this._$AR(s&&s._$AB.nextSibling,i),t.length=i)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){const t=x(e).nextSibling;x(e).remove(),e=t}}setConnected(e){void 0===this._$AM&&(this._$Cv=e,this._$AP?.(e))}}class ee{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,s,i,r){this.type=1,this._$AH=K,this._$AN=void 0,this.element=e,this.name=t,this._$AM=i,this.options=r,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=K}_$AI(e,t=this,s,i){const r=this.strings;let a=!1;if(void 0===r)e=Q(this,e,t,0),a=!D(e)||e!==this._$AH&&e!==q,a&&(this._$AH=e);else{const i=e;let n,o;for(e=r[0],n=0;n<r.length-1;n++)o=Q(this,i[s+n],t,n),o===q&&(o=this._$AH[n]),a||=!D(o)||o!==this._$AH[n],o===K?e=K:e!==K&&(e+=(o??"")+r[n+1]),this._$AH[n]=o}a&&!i&&this.j(e)}j(e){e===K?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}}class te extends ee{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===K?void 0:e}}class se extends ee{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==K)}}class ie extends ee{constructor(e,t,s,i,r){super(e,t,s,i,r),this.type=5}_$AI(e,t=this){if((e=Q(this,e,t,0)??K)===q)return;const s=this._$AH,i=e===K&&s!==K||e.capture!==s.capture||e.once!==s.once||e.passive!==s.passive,r=e!==K&&(s===K||i);i&&this.element.removeEventListener(this.name,this,s),r&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}}class re{constructor(e,t,s){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=s}get _$AU(){return this._$AM._$AU}_$AI(e){Q(this,e)}}const ae=S.litHtmlPolyfillSupport;ae?.(J,Y),(S.litHtmlVersions??=[]).push("3.3.2");const ne=globalThis;class oe extends w{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,s)=>{const i=s?.renderBefore??t;let r=i._$litPart$;if(void 0===r){const e=s?.renderBefore??null;i._$litPart$=r=new Y(t.insertBefore(T(),e),e,void 0,s??{})}return r._$AI(e),r})(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return q}}oe._$litElement$=!0,oe.finalized=!0,ne.litElementHydrateSupport?.({LitElement:oe});const ce=ne.litElementPolyfillSupport;ce?.({LitElement:oe}),(ne.litElementVersions??=[]).push("4.2.2");const le=e=>(t,s)=>{void 0!==s?s.addInitializer(()=>{customElements.define(e,t)}):customElements.define(e,t)},he={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:$},de=(e=he,t,s)=>{const{kind:i,metadata:r}=s;let a=globalThis.litPropertyMetadata.get(r);if(void 0===a&&globalThis.litPropertyMetadata.set(r,a=new Map),"setter"===i&&((e=Object.create(e)).wrapped=!0),a.set(s.name,e),"accessor"===i){const{name:i}=s;return{set(s){const r=t.get.call(this);t.set.call(this,s),this.requestUpdate(i,r,e,!0,s)},init(t){return void 0!==t&&this.C(i,void 0,e,t),t}}}if("setter"===i){const{name:i}=s;return function(s){const r=this[i];t.call(this,s),this.requestUpdate(i,r,e,!0,s)}}throw Error("Unsupported decorator location: "+i)};function pe(e){return(t,s)=>"object"==typeof s?de(e,t,s):((e,t,s)=>{const i=t.hasOwnProperty(s);return t.constructor.createProperty(s,e),i?Object.getOwnPropertyDescriptor(t,s):void 0})(e,t,s)}function _e(e){return pe({...e,state:!0,attribute:!1})}async function me(e,t){return e.callWS({type:"homematicip_local/integration/get_system_health",entry_id:t})}async function ue(e,t,s=50,i){return e.callWS({type:"homematicip_local/integration/get_incidents",entry_id:t,limit:s,...i})}async function ge(e,t){return e.callWS({type:"homematicip_local/integration/get_device_statistics",entry_id:t})}const ve=n`
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
`,fe={en:{systemHealth:"System Health",centralState:"Status",healthScore:"Health",devices:"Devices",unreachable:"Unreachable",firmwareUpdates:"FW Updates",incidents:"Incidents",noIncidents:"No incidents",throttleActive:"Throttle active",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Device Status",problems:"Problems",allDevicesOk:"All devices OK",notReachable:"Not reachable",lowBattery:"Low battery",configPending:"Config pending",devicesOk:"{count} devices OK",noDevices:"No devices found",messages:"Messages",alarms:"Alarms",serviceMessages:"Service",acknowledge:"Acknowledge",noMessages:"No service messages",noAlarms:"No alarms",loading:"Loading...",error:"Error loading data",refresh:"Refresh"},de:{systemHealth:"Systemstatus",centralState:"Status",healthScore:"Zustand",devices:"Geräte",unreachable:"Nicht erreichbar",firmwareUpdates:"FW-Updates",incidents:"Vorfälle",noIncidents:"Keine Vorfälle",throttleActive:"Drosselung aktiv",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Gerätestatus",problems:"Probleme",allDevicesOk:"Alle Geräte OK",notReachable:"Nicht erreichbar",lowBattery:"Batterie niedrig",configPending:"Konfiguration ausstehend",devicesOk:"{count} Geräte OK",noDevices:"Keine Geräte gefunden",messages:"Meldungen",alarms:"Alarme",serviceMessages:"Service",acknowledge:"Quittieren",noMessages:"Keine Servicemeldungen",noAlarms:"Keine Alarme",loading:"Laden...",error:"Fehler beim Laden",refresh:"Aktualisieren"}};function ye(e){return fe[e]||fe.en}let $e=class extends oe{constructor(){super(...arguments),this._loading=!0,this._error=""}static{this.styles=ve}setConfig(e){if(!e.entry_id)throw new Error("entry_id is required");this._config={show_incidents:!1,max_incidents:5,show_throttle:!1,poll_interval:30,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=ye(this.hass.config.language))}_startPolling(e){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),e)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(!this.hass||!this._config)return;try{const e=this._config.show_incidents?this._config.max_incidents:0,[t,s,i]=await Promise.all([me(this.hass,this._config.entry_id),ge(this.hass,this._config.entry_id),e>0?ue(this.hass,this._config.entry_id,e):Promise.resolve(void 0)]);this._health=t,this._deviceStats=s,i&&(this._incidents=i),this._entryEntityIds||await this._loadEntryEntityIds(),this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}const e="running"===this._health?.central_state?.toLowerCase();this._startPolling(e?Math.max(1e3*(this._config.poll_interval??30),3e4):5e3)}render(){if(!this._config||!this._t)return K;const e=this._config.title??this._t.systemHealth;return this._loading?B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&!this._health?B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:B`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">${this._renderStatusBadge()}</div>
        </div>
        <div class="card-content">
          ${this._renderStats()} ${this._renderRadioLevels()} ${this._renderIncidents()}
        </div>
      </ha-card>
    `}_renderStatusBadge(){if(!this._health)return K;const e=this._health.central_state,t="running"===e?.toLowerCase(),s=Math.round(100*this._health.overall_health_score);return B`
      <span class="badge ${t?"ok":"error"}">${s}%</span>
    `}_renderStats(){if(!this._deviceStats)return K;const e=this._deviceStats;return B`
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
    `}async _loadEntryEntityIds(){if(this.hass&&this._config)try{const e=await this.hass.callWS({type:"config/entity_registry/list"}),t=this._config.entry_id;this._entryEntityIds=new Set(e.filter(e=>e.config_entry_id===t).map(e=>e.entity_id))}catch{this._entryEntityIds=void 0}}_getRadioLevels(){const e=this.hass?.states;if(!e)return[];const t=new Map;for(const[s,i]of Object.entries(e)){if(!s.startsWith("sensor."))continue;const e=s.endsWith("_duty_cycle_level"),r=s.endsWith("_carrier_sense_level");if(!e&&!r)continue;if(this._entryEntityIds&&!this._entryEntityIds.has(s))continue;const a=i.attributes,n=a?.friendly_name||s,o=s.replace(/_(?:duty_cycle|carrier_sense)_level$/,""),c=n.replace(/\s*Duty Cycle Level$/i,"").replace(/\s*Carrier Sense Level$/i,"").replace(/\s*DutyCycle Level$/i,"").replace(/\s*CarrierSense Level$/i,"");t.has(o)||t.set(o,{name:c,dutyCycle:null,carrierSense:null});const l=t.get(o),h=parseFloat(i.state);isNaN(h)||(e&&(l.dutyCycle=h),r&&(l.carrierSense=h))}return[...t.values()].sort((e,t)=>e.name.localeCompare(t.name))}_dcClass(e){return null===e?"":e>=80?"error":e>=60?"warning":""}_csClass(e){return null===e?"":e>=10?"error":""}_renderRadioLevels(){const e=this._getRadioLevels();return 0===e.length?K:B`
      <div class="section-title">${this._t.dutyCycle} / ${this._t.carrierSense}</div>
      <div class="item-list">
        ${e.map(e=>B`
            <div class="item-row">
              <ha-icon class="item-icon" .icon=${"mdi:radio-tower"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.name}</div>
                <div class="item-secondary">
                  ${null!==e.dutyCycle?B`<span class="${this._dcClass(e.dutyCycle)}"
                        >DC: ${e.dutyCycle}%</span
                      >`:K}
                  ${null!==e.dutyCycle&&null!==e.carrierSense?" · ":K}
                  ${null!==e.carrierSense?B`<span class="${this._csClass(e.carrierSense)}"
                        >CS: ${e.carrierSense}%</span
                      >`:K}
                </div>
              </div>
            </div>
          `)}
      </div>
    `}_renderIncidents(){if(!this._config?.show_incidents||!this._incidents)return K;const e=this._incidents.summary.total_incidents;return 0===e?B`<div class="empty-state">${this._t.noIncidents}</div>`:B`
      <div class="section-title">
        ${this._t.incidents}
        <span class="badge warning">${e}</span>
      </div>
      <div class="item-list">
        ${this._incidents.incidents.map(e=>B`
            <div class="item-row ${this._incidentSeverity(e)}">
              <ha-icon
                class="item-icon"
                .icon=${this._incidentIcon(e)}
              ></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.message||e.type}</div>
                <div class="item-secondary">${this._formatTimestamp(e.timestamp)}</div>
              </div>
            </div>
          `)}
      </div>
    `}_incidentSeverity(e){const t=String(e.severity||"info").toLowerCase();return"error"===t||"critical"===t?"error":"warning"===t?"warning":""}_incidentIcon(e){const t=String(e.severity||"info").toLowerCase();return"error"===t||"critical"===t?"mdi:alert-circle":"warning"===t?"mdi:alert":"mdi:information"}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return e}}static getConfigElement(){return document.createElement("homematicip-system-health-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};async function be(e){try{return(await e.callWS({type:"config_entries/get",domain:"homematicip_local"})).map(e=>({value:e.entry_id,label:e.title}))}catch{return[]}}e([pe({attribute:!1})],$e.prototype,"hass",void 0),e([_e()],$e.prototype,"_config",void 0),e([_e()],$e.prototype,"_health",void 0),e([_e()],$e.prototype,"_deviceStats",void 0),e([_e()],$e.prototype,"_incidents",void 0),e([_e()],$e.prototype,"_entryEntityIds",void 0),e([_e()],$e.prototype,"_loading",void 0),e([_e()],$e.prototype,"_error",void 0),$e=e([le("homematicip-system-health-card")],$e);let we=class extends oe{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",show_incidents:"Show incidents",max_incidents:"Max incidents",poll_interval:"Poll interval"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await be(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_incidents",selector:{boolean:{}},default:!1},{name:"max_incidents",selector:{number:{min:1,max:50,mode:"box"}},default:5},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:K}_valueChanged(e){var t;e.stopPropagation(),t={config:{...this._config,...e.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:t}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};e([pe({attribute:!1})],we.prototype,"hass",void 0),e([_e()],we.prototype,"_config",void 0),e([_e()],we.prototype,"_entryOptions",void 0),we=e([le("homematicip-system-health-editor")],we);let Se=class extends oe{constructor(){super(...arguments),this._devices=[],this._totalDevices=0,this._problemCount=0,this._loading=!0,this._error=""}static{this.styles=ve}setConfig(e){if(!e.entry_id)throw new Error("entry_id is required");this._config={filter:"problems",show_model:!0,max_devices:10,poll_interval:60,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=ye(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??60))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config){try{let e=await async function(e,t){return(await e.callWS({type:"homematicip_local/config/list_devices",entry_id:t})).devices}(this.hass,this._config.entry_id);this._config.interface_filter&&(e=e.filter(e=>e.interface_id===this._config.interface_filter)),this._totalDevices=e.length,this._devices=this._filterDevices(e),this._problemCount=this._devices.filter(e=>"ok"!==e.severity).length,this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}this._startPolling()}}_filterDevices(e){const t=this._config?.filter??"problems",s=[];for(const i of e){const e=i.maintenance,r=[];let a="ok";!e.unreach||"all"!==t&&"problems"!==t&&"unreachable"!==t||(r.push(this._t?.notReachable??"Not reachable"),a="error"),!e.low_bat||"all"!==t&&"problems"!==t&&"low_battery"!==t||(r.push(this._t?.lowBattery??"Low battery"),"ok"===a&&(a="warning")),!e.config_pending||"all"!==t&&"problems"!==t&&"config_pending"!==t||(r.push(this._t?.configPending??"Config pending"),"ok"===a&&(a="warning")),("all"===t||r.length>0)&&s.push({device:i,issues:r,severity:a})}const i={error:0,warning:1,ok:2};s.sort((e,t)=>{const s=i[e.severity]-i[t.severity];return 0!==s?s:e.device.name.localeCompare(t.device.name)});const r=this._config?.max_devices??10;return r>0?s.slice(0,r):s}render(){if(!this._config||!this._t)return K;const e=this._config.title??this._t.deviceStatus;return this._loading?B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `:this._error&&0===this._totalDevices?B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `:B`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">
            ${this._problemCount>0?B`<span class="badge error">${this._problemCount} ${this._t.problems}</span>`:B`<span class="badge ok">OK</span>`}
          </div>
        </div>
        <div class="card-content">
          ${this._devices.length>0?this._renderDevices():this._renderAllOk()}
        </div>
      </ha-card>
    `}_deviceIcon(e){return"error"===e?"mdi:close-circle":"warning"===e?"mdi:alert":"mdi:check-circle"}_renderDevices(){const e=this._totalDevices-this._devices.length;return B`
      <div class="item-list">
        ${this._devices.map(e=>B`
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
      ${e>0?B`<div class="summary-line">+ ${e} ${this._t.devices}</div>`:K}
    `}_renderAllOk(){return B`<div class="empty-state">${this._t.allDevicesOk}</div>`}static getConfigElement(){return document.createElement("homematicip-device-status-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};e([pe({attribute:!1})],Se.prototype,"hass",void 0),e([_e()],Se.prototype,"_config",void 0),e([_e()],Se.prototype,"_devices",void 0),e([_e()],Se.prototype,"_totalDevices",void 0),e([_e()],Se.prototype,"_problemCount",void 0),e([_e()],Se.prototype,"_loading",void 0),e([_e()],Se.prototype,"_error",void 0),Se=e([le("homematicip-device-status-card")],Se);let xe=class extends oe{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",filter:"Filter",show_model:"Show device model",max_devices:"Max devices (0 = all)",poll_interval:"Poll interval",interface_filter:"Interface filter (optional)"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await be(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"filter",selector:{select:{options:[{value:"problems",label:"Problems only"},{value:"all",label:"All devices"},{value:"unreachable",label:"Unreachable"},{value:"low_battery",label:"Low battery"},{value:"config_pending",label:"Config pending"}],mode:"dropdown"}},default:"problems"},{name:"show_model",selector:{boolean:{}},default:!0},{name:"max_devices",selector:{number:{min:0,max:100,mode:"box"}},default:10},{name:"poll_interval",selector:{number:{min:10,max:600,mode:"box",unit_of_measurement:"s"}},default:60},{name:"interface_filter",selector:{text:{}}}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${{...this._config,filter:this._config.filter||"problems"}}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:K}_valueChanged(e){e.stopPropagation();const t={...this._config,...e.detail.value};t.interface_filter||delete t.interface_filter,this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:{config:t}}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};e([pe({attribute:!1})],xe.prototype,"hass",void 0),e([_e()],xe.prototype,"_config",void 0),e([_e()],xe.prototype,"_entryOptions",void 0),xe=e([le("homematicip-device-status-editor")],xe);let Ae=class extends oe{constructor(){super(...arguments),this._serviceMessages=[],this._alarmMessages=[],this._loading=!0,this._error=""}static{this.styles=ve}setConfig(e){if(!e.entry_id)throw new Error("entry_id is required");this._config={show_service:!0,show_alarms:!0,max_messages:10,show_timestamp:!0,compact:!1,poll_interval:30,...e}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(e){e.has("hass")&&this.hass&&(this._t=ye(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??30))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config){try{const e=[];this._config.show_service&&e.push(async function(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_service_messages",entry_id:t})).messages}(this.hass,this._config.entry_id).then(e=>this._serviceMessages=e)),this._config.show_alarms&&e.push(async function(e,t){return(await e.callWS({type:"homematicip_local/ccu/get_alarm_messages",entry_id:t})).alarms}(this.hass,this._config.entry_id).then(e=>this._alarmMessages=e)),await Promise.all(e),this._error=""}catch(e){this._error=String(e)}finally{this._loading=!1}this._startPolling()}}async _acknowledgeService(e){if(this.hass&&this._config)try{await async function(e,t,s){return e.callWS({type:"homematicip_local/ccu/acknowledge_service_message",entry_id:t,msg_id:s})}(this.hass,this._config.entry_id,e),this._serviceMessages=this._serviceMessages.filter(t=>t.msg_id!==e)}catch{}}async _acknowledgeAlarm(e){if(this.hass&&this._config)try{await async function(e,t,s){return e.callWS({type:"homematicip_local/ccu/acknowledge_alarm_message",entry_id:t,alarm_id:s})}(this.hass,this._config.entry_id,e),this._alarmMessages=this._alarmMessages.filter(t=>t.alarm_id!==e)}catch{}}render(){if(!this._config||!this._t)return K;const e=this._config.title??this._t.messages;if(this._loading)return B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `;if(this._error&&0===this._serviceMessages.length&&0===this._alarmMessages.length)return B`
        <ha-card>
          <div class="card-header">${e}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `;const t=this._alarmMessages.length,s=this._serviceMessages.length;return B`
      <ha-card>
        <div class="card-header">
          ${e}
          <div class="badges">
            ${t>0?B`<span class="badge error">${t}</span>`:K}
            ${s>0?B`<span class="badge warning">${s}</span>`:K}
            ${0===t&&0===s?B`<span class="badge ok">OK</span>`:K}
          </div>
        </div>
        <div class="card-content">
          ${this._renderAlarms()} ${this._renderServiceMessages()}
          ${0===t&&0===s?B`<div class="empty-state">${this._t.noMessages}</div>`:K}
        </div>
      </ha-card>
    `}_renderAlarms(){if(!this._config?.show_alarms||0===this._alarmMessages.length)return K;const e=this._alarmMessages.slice(0,this._config.max_messages??10);return B`
      <div class="section-title">${this._t.alarms}</div>
      <div class="item-list">
        ${e.map(e=>B`
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
    `}_renderServiceMessages(){if(!this._config?.show_service||0===this._serviceMessages.length)return K;const e=this._serviceMessages.slice(0,this._config.max_messages??10);return B`
      <div class="section-title">${this._t.serviceMessages}</div>
      <div class="item-list">
        ${e.map(e=>B`
            <div class="item-row warning">
              <ha-icon class="item-icon" .icon=${"mdi:alert"}></ha-icon>
              <div class="item-content">
                <div class="item-primary">${e.device_name||e.name}</div>
                <div class="item-secondary">
                  ${e.message_code}${e.counter>1?` · ${e.counter}x`:""}${this._config?.show_timestamp?` · ${this._formatTimestamp(e.timestamp)}`:""}
                </div>
              </div>
              ${e.quittable?B`
                    <div class="item-action">
                      <ha-icon-button
                        .label=${this._t.acknowledge}
                        @click=${()=>this._acknowledgeService(e.msg_id)}
                      >
                        <ha-icon .icon=${"mdi:check"}></ha-icon>
                      </ha-icon-button>
                    </div>
                  `:K}
            </div>
          `)}
      </div>
    `}_formatTimestamp(e){if(!e)return"";try{return new Date(e).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return e}}static getConfigElement(){return document.createElement("homematicip-messages-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}};e([pe({attribute:!1})],Ae.prototype,"hass",void 0),e([_e()],Ae.prototype,"_config",void 0),e([_e()],Ae.prototype,"_serviceMessages",void 0),e([_e()],Ae.prototype,"_alarmMessages",void 0),e([_e()],Ae.prototype,"_loading",void 0),e([_e()],Ae.prototype,"_error",void 0),Ae=e([le("homematicip-messages-card")],Ae);let Ce=class extends oe{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=e=>({entry_id:"Integration",title:"Title (optional)",show_alarms:"Show alarms",show_service:"Show service messages",max_messages:"Max messages",show_timestamp:"Show timestamps",poll_interval:"Poll interval"}[e.name]||e.name)}setConfig(e){this._config=e}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(e){e.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await be(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_alarms",selector:{boolean:{}},default:!0},{name:"show_service",selector:{boolean:{}},default:!0},{name:"max_messages",selector:{number:{min:1,max:50,mode:"box"}},default:10},{name:"show_timestamp",selector:{boolean:{}},default:!0},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:K}_valueChanged(e){var t;e.stopPropagation(),t={config:{...this._config,...e.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:t}))}static{this.styles=n`
    ha-form {
      display: block;
    }
  `}};e([pe({attribute:!1})],Ce.prototype,"hass",void 0),e([_e()],Ce.prototype,"_config",void 0),e([_e()],Ce.prototype,"_entryOptions",void 0),Ce=e([le("homematicip-messages-editor")],Ce),window.customCards=window.customCards||[],window.customCards.push({type:"homematicip-system-health-card",name:"HomematicIP System Health",description:"System health, device statistics, and incidents for HomematicIP Local"}),window.customCards.push({type:"homematicip-device-status-card",name:"HomematicIP Device Status",description:"Device status overview with problem highlighting for HomematicIP Local"}),window.customCards.push({type:"homematicip-messages-card",name:"HomematicIP Messages",description:"Service messages and alarms with acknowledgment for HomematicIP Local"});
