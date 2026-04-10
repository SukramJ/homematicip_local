function t(t,e,s,i){var r,n=arguments.length,a=n<3?e:null===i?i=Object.getOwnPropertyDescriptor(e,s):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,s,i);else for(var o=t.length-1;o>=0;o--)(r=t[o])&&(a=(n<3?r(a):n>3?r(e,s,a):r(e,s))||a);return n>3&&a&&Object.defineProperty(e,s,a),a}"function"==typeof SuppressedError&&SuppressedError;const e=globalThis,s=e.ShadowRoot&&(void 0===e.ShadyCSS||e.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),r=new WeakMap;let n=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(s&&void 0===t){const s=void 0!==e&&1===e.length;s&&(t=r.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),s&&r.set(e,t))}return t}toString(){return this.cssText}};const a=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,s,i)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+t[i+1],t[0]);return new n(s,t,i)},o=s?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return(t=>new n("string"==typeof t?t:t+"",void 0,i))(e)})(t):t,{is:c,defineProperty:l,getOwnPropertyDescriptor:h,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:_}=Object,m=globalThis,u=m.trustedTypes,g=u?u.emptyScript:"",v=m.reactiveElementPolyfillSupport,f=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?g:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let s=t;switch(e){case Boolean:s=null!==t;break;case Number:s=null===t?null:Number(t);break;case Object:case Array:try{s=JSON.parse(t)}catch(t){s=null}}return s}},$=(t,e)=>!c(t,e),b={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:$};Symbol.metadata??=Symbol("metadata"),m.litPropertyMetadata??=new WeakMap;let w=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=b){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const s=Symbol(),i=this.getPropertyDescriptor(t,s,e);void 0!==i&&l(this.prototype,t,i)}}static getPropertyDescriptor(t,e,s){const{get:i,set:r}=h(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:i,set(e){const n=i?.call(this);r?.call(this,e),this.requestUpdate(t,n,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??b}static _$Ei(){if(this.hasOwnProperty(f("elementProperties")))return;const t=_(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(f("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(f("properties"))){const t=this.properties,e=[...d(t),...p(t)];for(const s of e)this.createProperty(s,t[s])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,s]of e)this.elementProperties.set(t,s)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const s=this._$Eu(t,e);void 0!==s&&this._$Eh.set(s,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const s=new Set(t.flat(1/0).reverse());for(const t of s)e.unshift(o(t))}else void 0!==t&&e.push(o(t));return e}static _$Eu(t,e){const s=e.attribute;return!1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const s of e.keys())this.hasOwnProperty(s)&&(t.set(s,this[s]),delete this[s]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,i)=>{if(s)t.adoptedStyleSheets=i.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const s of i){const i=document.createElement("style"),r=e.litNonce;void 0!==r&&i.setAttribute("nonce",r),i.textContent=s.cssText,t.appendChild(i)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,s){this._$AK(t,s)}_$ET(t,e){const s=this.constructor.elementProperties.get(t),i=this.constructor._$Eu(t,s);if(void 0!==i&&!0===s.reflect){const r=(void 0!==s.converter?.toAttribute?s.converter:y).toAttribute(e,s.type);this._$Em=t,null==r?this.removeAttribute(i):this.setAttribute(i,r),this._$Em=null}}_$AK(t,e){const s=this.constructor,i=s._$Eh.get(t);if(void 0!==i&&this._$Em!==i){const t=s.getPropertyOptions(i),r="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=i;const n=r.fromAttribute(e,t.type);this[i]=n??this._$Ej?.get(i)??n,this._$Em=null}}requestUpdate(t,e,s,i=!1,r){if(void 0!==t){const n=this.constructor;if(!1===i&&(r=this[t]),s??=n.getPropertyOptions(t),!((s.hasChanged??$)(r,e)||s.useDefault&&s.reflect&&r===this._$Ej?.get(t)&&!this.hasAttribute(n._$Eu(t,s))))return;this.C(t,e,s)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:s,reflect:i,wrapped:r},n){s&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,n??e??this[t]),!0!==r||void 0!==n)||(this._$AL.has(t)||(this.hasUpdated||s||(e=void 0),this._$AL.set(t,e)),!0===i&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,s]of t){const{wrapped:t}=s,i=this[e];!0!==t||this._$AL.has(e)||void 0===i||this.C(e,void 0,s,i)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};w.elementStyles=[],w.shadowRootOptions={mode:"open"},w[f("elementProperties")]=new Map,w[f("finalized")]=new Map,v?.({ReactiveElement:w}),(m.reactiveElementVersions??=[]).push("2.1.2");const S=globalThis,x=t=>t,A=S.trustedTypes,C=A?A.createPolicy("lit-html",{createHTML:t=>t}):void 0,E="$lit$",k=`lit$${Math.random().toFixed(9).slice(2)}$`,P="?"+k,O=`<${P}>`,M=document,T=()=>M.createComment(""),D=t=>null===t||"object"!=typeof t&&"function"!=typeof t,U=Array.isArray,H="[ \t\n\f\r]",L=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,N=/-->/g,R=/>/g,I=RegExp(`>|${H}(?:([^\\s"'>=/]+)(${H}*=${H}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),z=/'/g,j=/"/g,W=/^(?:script|style|textarea|title)$/i,B=(t,...e)=>({_$litType$:1,strings:t,values:e}),K=Symbol.for("lit-noChange"),q=Symbol.for("lit-nothing"),V=new WeakMap,F=M.createTreeWalker(M,129);function G(t,e){if(!U(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==C?C.createHTML(e):e}const Z=(t,e)=>{const s=t.length-1,i=[];let r,n=2===e?"<svg>":3===e?"<math>":"",a=L;for(let e=0;e<s;e++){const s=t[e];let o,c,l=-1,h=0;for(;h<s.length&&(a.lastIndex=h,c=a.exec(s),null!==c);)h=a.lastIndex,a===L?"!--"===c[1]?a=N:void 0!==c[1]?a=R:void 0!==c[2]?(W.test(c[2])&&(r=RegExp("</"+c[2],"g")),a=I):void 0!==c[3]&&(a=I):a===I?">"===c[0]?(a=r??L,l=-1):void 0===c[1]?l=-2:(l=a.lastIndex-c[2].length,o=c[1],a=void 0===c[3]?I:'"'===c[3]?j:z):a===j||a===z?a=I:a===N||a===R?a=L:(a=I,r=void 0);const d=a===I&&t[e+1].startsWith("/>")?" ":"";n+=a===L?s+O:l>=0?(i.push(o),s.slice(0,l)+E+s.slice(l)+k+d):s+k+(-2===l?e:d)}return[G(t,n+(t[s]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),i]};class J{constructor({strings:t,_$litType$:e},s){let i;this.parts=[];let r=0,n=0;const a=t.length-1,o=this.parts,[c,l]=Z(t,e);if(this.el=J.createElement(c,s),F.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(i=F.nextNode())&&o.length<a;){if(1===i.nodeType){if(i.hasAttributes())for(const t of i.getAttributeNames())if(t.endsWith(E)){const e=l[n++],s=i.getAttribute(t).split(k),a=/([.?@])?(.*)/.exec(e);o.push({type:1,index:r,name:a[2],strings:s,ctor:"."===a[1]?et:"?"===a[1]?st:"@"===a[1]?it:tt}),i.removeAttribute(t)}else t.startsWith(k)&&(o.push({type:6,index:r}),i.removeAttribute(t));if(W.test(i.tagName)){const t=i.textContent.split(k),e=t.length-1;if(e>0){i.textContent=A?A.emptyScript:"";for(let s=0;s<e;s++)i.append(t[s],T()),F.nextNode(),o.push({type:2,index:++r});i.append(t[e],T())}}}else if(8===i.nodeType)if(i.data===P)o.push({type:2,index:r});else{let t=-1;for(;-1!==(t=i.data.indexOf(k,t+1));)o.push({type:7,index:r}),t+=k.length-1}r++}}static createElement(t,e){const s=M.createElement("template");return s.innerHTML=t,s}}function Q(t,e,s=t,i){if(e===K)return e;let r=void 0!==i?s._$Co?.[i]:s._$Cl;const n=D(e)?void 0:e._$litDirective$;return r?.constructor!==n&&(r?._$AO?.(!1),void 0===n?r=void 0:(r=new n(t),r._$AT(t,s,i)),void 0!==i?(s._$Co??=[])[i]=r:s._$Cl=r),void 0!==r&&(e=Q(t,r._$AS(t,e.values),r,i)),e}class X{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:s}=this._$AD,i=(t?.creationScope??M).importNode(e,!0);F.currentNode=i;let r=F.nextNode(),n=0,a=0,o=s[0];for(;void 0!==o;){if(n===o.index){let e;2===o.type?e=new Y(r,r.nextSibling,this,t):1===o.type?e=new o.ctor(r,o.name,o.strings,this,t):6===o.type&&(e=new rt(r,this,t)),this._$AV.push(e),o=s[++a]}n!==o?.index&&(r=F.nextNode(),n++)}return F.currentNode=M,i}p(t){let e=0;for(const s of this._$AV)void 0!==s&&(void 0!==s.strings?(s._$AI(t,s,e),e+=s.strings.length-2):s._$AI(t[e])),e++}}class Y{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,s,i){this.type=2,this._$AH=q,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=s,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=Q(this,t,e),D(t)?t===q||null==t||""===t?(this._$AH!==q&&this._$AR(),this._$AH=q):t!==this._$AH&&t!==K&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>U(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==q&&D(this._$AH)?this._$AA.nextSibling.data=t:this.T(M.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:s}=t,i="number"==typeof s?this._$AC(t):(void 0===s.el&&(s.el=J.createElement(G(s.h,s.h[0]),this.options)),s);if(this._$AH?._$AD===i)this._$AH.p(e);else{const t=new X(i,this),s=t.u(this.options);t.p(e),this.T(s),this._$AH=t}}_$AC(t){let e=V.get(t.strings);return void 0===e&&V.set(t.strings,e=new J(t)),e}k(t){U(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let s,i=0;for(const r of t)i===e.length?e.push(s=new Y(this.O(T()),this.O(T()),this,this.options)):s=e[i],s._$AI(r),i++;i<e.length&&(this._$AR(s&&s._$AB.nextSibling,i),e.length=i)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=x(t).nextSibling;x(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class tt{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,s,i,r){this.type=1,this._$AH=q,this._$AN=void 0,this.element=t,this.name=e,this._$AM=i,this.options=r,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=q}_$AI(t,e=this,s,i){const r=this.strings;let n=!1;if(void 0===r)t=Q(this,t,e,0),n=!D(t)||t!==this._$AH&&t!==K,n&&(this._$AH=t);else{const i=t;let a,o;for(t=r[0],a=0;a<r.length-1;a++)o=Q(this,i[s+a],e,a),o===K&&(o=this._$AH[a]),n||=!D(o)||o!==this._$AH[a],o===q?t=q:t!==q&&(t+=(o??"")+r[a+1]),this._$AH[a]=o}n&&!i&&this.j(t)}j(t){t===q?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class et extends tt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===q?void 0:t}}class st extends tt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==q)}}class it extends tt{constructor(t,e,s,i,r){super(t,e,s,i,r),this.type=5}_$AI(t,e=this){if((t=Q(this,t,e,0)??q)===K)return;const s=this._$AH,i=t===q&&s!==q||t.capture!==s.capture||t.once!==s.once||t.passive!==s.passive,r=t!==q&&(s===q||i);i&&this.element.removeEventListener(this.name,this,s),r&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class rt{constructor(t,e,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=s}get _$AU(){return this._$AM._$AU}_$AI(t){Q(this,t)}}const nt=S.litHtmlPolyfillSupport;nt?.(J,Y),(S.litHtmlVersions??=[]).push("3.3.2");const at=globalThis;class ot extends w{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,s)=>{const i=s?.renderBefore??e;let r=i._$litPart$;if(void 0===r){const t=s?.renderBefore??null;i._$litPart$=r=new Y(e.insertBefore(T(),t),t,void 0,s??{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return K}}ot._$litElement$=!0,ot.finalized=!0,at.litElementHydrateSupport?.({LitElement:ot});const ct=at.litElementPolyfillSupport;ct?.({LitElement:ot}),(at.litElementVersions??=[]).push("4.2.2");const lt={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:$},ht=(t=lt,e,s)=>{const{kind:i,metadata:r}=s;let n=globalThis.litPropertyMetadata.get(r);if(void 0===n&&globalThis.litPropertyMetadata.set(r,n=new Map),"setter"===i&&((t=Object.create(t)).wrapped=!0),n.set(s.name,t),"accessor"===i){const{name:i}=s;return{set(s){const r=e.get.call(this);e.set.call(this,s),this.requestUpdate(i,r,t,!0,s)},init(e){return void 0!==e&&this.C(i,void 0,t,e),e}}}if("setter"===i){const{name:i}=s;return function(s){const r=this[i];e.call(this,s),this.requestUpdate(i,r,t,!0,s)}}throw Error("Unsupported decorator location: "+i)};function dt(t){return(e,s)=>"object"==typeof s?ht(t,e,s):((t,e,s)=>{const i=e.hasOwnProperty(s);return e.constructor.createProperty(s,t),i?Object.getOwnPropertyDescriptor(e,s):void 0})(t,e,s)}function pt(t){return dt({...t,state:!0,attribute:!1})}async function _t(t,e){return t.callWS({type:"homematicip_local/integration/get_system_health",entry_id:e})}async function mt(t,e,s=50,i){return t.callWS({type:"homematicip_local/integration/get_incidents",entry_id:e,limit:s,...i})}async function ut(t,e){return t.callWS({type:"homematicip_local/integration/get_device_statistics",entry_id:e})}const gt=a`
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
`,vt={en:{systemHealth:"System Health",centralState:"Status",healthScore:"Health",devices:"Devices",unreachable:"Unreachable",firmwareUpdates:"FW Updates",incidents:"Incidents",noIncidents:"No incidents",throttleActive:"Throttle active",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Device Status",problems:"Problems",allDevicesOk:"All devices OK",notReachable:"Not reachable",lowBattery:"Low battery",configPending:"Config pending",devicesOk:"{count} devices OK",noDevices:"No devices found",messages:"Messages",alarms:"Alarms",serviceMessages:"Service",acknowledge:"Acknowledge",noMessages:"No service messages",noAlarms:"No alarms",loading:"Loading...",error:"Error loading data",refresh:"Refresh"},de:{systemHealth:"Systemstatus",centralState:"Status",healthScore:"Zustand",devices:"Geräte",unreachable:"Nicht erreichbar",firmwareUpdates:"FW-Updates",incidents:"Vorfälle",noIncidents:"Keine Vorfälle",throttleActive:"Drosselung aktiv",dutyCycle:"Duty Cycle",carrierSense:"Carrier Sense",deviceStatus:"Gerätestatus",problems:"Probleme",allDevicesOk:"Alle Geräte OK",notReachable:"Nicht erreichbar",lowBattery:"Batterie niedrig",configPending:"Konfiguration ausstehend",devicesOk:"{count} Geräte OK",noDevices:"Keine Geräte gefunden",messages:"Meldungen",alarms:"Alarme",serviceMessages:"Service",acknowledge:"Quittieren",noMessages:"Keine Servicemeldungen",noAlarms:"Keine Alarme",loading:"Laden...",error:"Fehler beim Laden",refresh:"Aktualisieren"}};function ft(t){return vt[t]||vt.en}class yt extends ot{constructor(){super(...arguments),this._loading=!0,this._error=""}static{this.styles=gt}setConfig(t){this._config={show_incidents:!1,max_incidents:5,show_throttle:!1,poll_interval:30,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=ft(this.hass.config.language))}_startPolling(t){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),t)}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(!this.hass||!this._config||!this._config.entry_id)return void(this._loading=!1);try{const t=this._config.show_incidents?this._config.max_incidents:0,[e,s,i]=await Promise.all([_t(this.hass,this._config.entry_id),ut(this.hass,this._config.entry_id),t>0?mt(this.hass,this._config.entry_id,t):Promise.resolve(void 0)]);this._health=e,this._deviceStats=s,i&&(this._incidents=i),this._entryEntityIds||await this._loadEntryEntityIds(),this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}const t="running"===this._health?.central_state?.toLowerCase();this._startPolling(t?Math.max(1e3*(this._config.poll_interval??30),3e4):5e3)}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.systemHealth;return this._loading?B`
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
    `}_renderStatusBadge(){if(!this._health)return q;const t=this._health.central_state,e="running"===t?.toLowerCase(),s=Math.round(100*this._health.overall_health_score);return B` <span class="badge ${e?"ok":"error"}">${s}%</span> `}_renderStats(){if(!this._deviceStats)return q;const t=this._deviceStats;return B`
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
    `}async _loadEntryEntityIds(){this.hass&&this._config&&(this._entryEntityIds=await async function(t,e){try{const s=await t.callWS({type:"config/entity_registry/list"});return new Set(s.filter(t=>t.config_entry_id===e).map(t=>t.entity_id))}catch{return}}(this.hass,this._config.entry_id))}_renderRadioLevels(){const t=function(t,e){if(!t)return[];const s=new Map;for(const[i,r]of Object.entries(t)){if(!i.startsWith("sensor."))continue;const t=i.endsWith("_duty_cycle_level"),n=i.endsWith("_carrier_sense_level");if(!t&&!n)continue;if(e&&!e.has(i))continue;const a=r.attributes,o=a?.friendly_name||i,c=i.replace(/_(?:duty_cycle|carrier_sense)_level$/,""),l=o.replace(/\s*Duty Cycle Level$/i,"").replace(/\s*Carrier Sense Level$/i,"").replace(/\s*DutyCycle Level$/i,"").replace(/\s*CarrierSense Level$/i,"");s.has(c)||s.set(c,{name:l,dutyCycle:null,carrierSense:null});const h=s.get(c),d=parseFloat(r.state);isNaN(d)||(t&&(h.dutyCycle=d),n&&(h.carrierSense=d))}return[...s.values()].sort((t,e)=>t.name.localeCompare(e.name))}(this.hass?.states,this._entryEntityIds);return 0===t.length?q:B`
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
    `}_incidentSeverity(t){const e=String(t.severity||"info").toLowerCase();return"error"===e||"critical"===e?"error":"warning"===e?"warning":""}_incidentIcon(t){const e=String(t.severity||"info").toLowerCase();return"error"===e||"critical"===e?"mdi:alert-circle":"warning"===e?"mdi:alert":"mdi:information"}_formatTimestamp(t){if(!t)return"";try{return new Date(t).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return t}}static getConfigElement(){return document.createElement("homematicip-system-health-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}t([dt({attribute:!1})],yt.prototype,"hass",void 0),t([pt()],yt.prototype,"_config",void 0),t([pt()],yt.prototype,"_health",void 0),t([pt()],yt.prototype,"_deviceStats",void 0),t([pt()],yt.prototype,"_incidents",void 0),t([pt()],yt.prototype,"_entryEntityIds",void 0),t([pt()],yt.prototype,"_loading",void 0),t([pt()],yt.prototype,"_error",void 0);const $t="homematicip-system-health-card";async function bt(t){try{return(await t.callWS({type:"config_entries/get",domain:"homematicip_local"})).map(t=>({value:t.entry_id,label:t.title}))}catch{return[]}}customElements.get($t)||customElements.define($t,yt);class wt extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",show_incidents:"Show incidents",max_incidents:"Max incidents",poll_interval:"Poll interval"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_incidents",selector:{boolean:{}},default:!1},{name:"max_incidents",selector:{number:{min:1,max:50,mode:"box"}},default:5},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){var e;t.stopPropagation(),e={config:{...this._config,...t.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:e}))}static{this.styles=a`
    ha-form {
      display: block;
    }
  `}}t([dt({attribute:!1})],wt.prototype,"hass",void 0),t([pt()],wt.prototype,"_config",void 0),t([pt()],wt.prototype,"_entryOptions",void 0);const St="homematicip-system-health-editor";customElements.get(St)||customElements.define(St,wt);class xt extends ot{constructor(){super(...arguments),this._devices=[],this._totalDevices=0,this._problemCount=0,this._loading=!0,this._error=""}static{this.styles=gt}setConfig(t){this._config={filter:"problems",show_model:!0,max_devices:10,poll_interval:60,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=ft(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??60))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{let t=await async function(t,e){return(await t.callWS({type:"homematicip_local/config/list_devices",entry_id:e})).devices}(this.hass,this._config.entry_id);this._config.interface_filter&&(t=t.filter(t=>t.interface_id===this._config.interface_filter)),this._totalDevices=t.length,this._devices=this._filterDevices(t),this._problemCount=this._devices.filter(t=>"ok"!==t.severity).length,this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}this._startPolling()}else this._loading=!1}_filterDevices(t){const e=this._config?.filter??"problems",s=[];for(const i of t){const t=i.maintenance,r=[];let n="ok";!t.unreach||"all"!==e&&"problems"!==e&&"unreachable"!==e||(r.push(this._t?.notReachable??"Not reachable"),n="error"),!t.low_bat||"all"!==e&&"problems"!==e&&"low_battery"!==e||(r.push(this._t?.lowBattery??"Low battery"),"ok"===n&&(n="warning")),!t.config_pending||"all"!==e&&"problems"!==e&&"config_pending"!==e||(r.push(this._t?.configPending??"Config pending"),"ok"===n&&(n="warning")),("all"===e||r.length>0)&&s.push({device:i,issues:r,severity:n})}const i={error:0,warning:1,ok:2};s.sort((t,e)=>{const s=i[t.severity]-i[e.severity];return 0!==s?s:t.device.name.localeCompare(e.device.name)});const r=this._config?.max_devices??10;return r>0?s.slice(0,r):s}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.deviceStatus;return this._loading?B`
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
    `}_renderAllOk(){return B`<div class="empty-state">${this._t.allDevicesOk}</div>`}static getConfigElement(){return document.createElement("homematicip-device-status-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}t([dt({attribute:!1})],xt.prototype,"hass",void 0),t([pt()],xt.prototype,"_config",void 0),t([pt()],xt.prototype,"_devices",void 0),t([pt()],xt.prototype,"_totalDevices",void 0),t([pt()],xt.prototype,"_problemCount",void 0),t([pt()],xt.prototype,"_loading",void 0),t([pt()],xt.prototype,"_error",void 0);const At="homematicip-device-status-card";customElements.get(At)||customElements.define(At,xt);class Ct extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",filter:"Filter",show_model:"Show device model",max_devices:"Max devices (0 = all)",poll_interval:"Poll interval",interface_filter:"Interface filter (optional)"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"filter",selector:{select:{options:[{value:"problems",label:"Problems only"},{value:"all",label:"All devices"},{value:"unreachable",label:"Unreachable"},{value:"low_battery",label:"Low battery"},{value:"config_pending",label:"Config pending"}],mode:"dropdown"}},default:"problems"},{name:"show_model",selector:{boolean:{}},default:!0},{name:"max_devices",selector:{number:{min:0,max:100,mode:"box"}},default:10},{name:"poll_interval",selector:{number:{min:10,max:600,mode:"box",unit_of_measurement:"s"}},default:60},{name:"interface_filter",selector:{text:{}}}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${{...this._config,filter:this._config.filter||"problems"}}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){t.stopPropagation();const e={...this._config,...t.detail.value};e.interface_filter||delete e.interface_filter,this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:{config:e}}))}static{this.styles=a`
    ha-form {
      display: block;
    }
  `}}t([dt({attribute:!1})],Ct.prototype,"hass",void 0),t([pt()],Ct.prototype,"_config",void 0),t([pt()],Ct.prototype,"_entryOptions",void 0);const Et="homematicip-device-status-editor";customElements.get(Et)||customElements.define(Et,Ct);class kt extends ot{constructor(){super(...arguments),this._serviceMessages=[],this._alarmMessages=[],this._loading=!0,this._error=""}static{this.styles=gt}setConfig(t){this._config={show_service:!0,show_alarms:!0,max_messages:10,show_timestamp:!0,compact:!1,poll_interval:30,...t}}connectedCallback(){super.connectedCallback(),this._fetchData()}disconnectedCallback(){super.disconnectedCallback(),this._stopPolling()}updated(t){t.has("hass")&&this.hass&&(this._t=ft(this.hass.config.language))}_startPolling(){this._stopPolling(),this._pollTimer=setTimeout(()=>this._fetchData(),1e3*(this._config?.poll_interval??30))}_stopPolling(){this._pollTimer&&(clearTimeout(this._pollTimer),this._pollTimer=void 0)}async _fetchData(){if(this.hass&&this._config&&this._config.entry_id){try{const t=[];this._config.show_service&&t.push(async function(t,e){return(await t.callWS({type:"homematicip_local/ccu/get_service_messages",entry_id:e})).messages}(this.hass,this._config.entry_id).then(t=>this._serviceMessages=t)),this._config.show_alarms&&t.push(async function(t,e){return(await t.callWS({type:"homematicip_local/ccu/get_alarm_messages",entry_id:e})).alarms}(this.hass,this._config.entry_id).then(t=>this._alarmMessages=t)),await Promise.all(t),this._error=""}catch(t){this._error=String(t)}finally{this._loading=!1}this._startPolling()}else this._loading=!1}async _acknowledgeService(t){if(this.hass&&this._config)try{await async function(t,e,s){return t.callWS({type:"homematicip_local/ccu/acknowledge_service_message",entry_id:e,msg_id:s})}(this.hass,this._config.entry_id,t),this._serviceMessages=this._serviceMessages.filter(e=>e.msg_id!==t)}catch{}}async _acknowledgeAlarm(t){if(this.hass&&this._config)try{await async function(t,e,s){return t.callWS({type:"homematicip_local/ccu/acknowledge_alarm_message",entry_id:e,alarm_id:s})}(this.hass,this._config.entry_id,t),this._alarmMessages=this._alarmMessages.filter(e=>e.alarm_id!==t)}catch{}}render(){if(!this._config||!this._t)return q;const t=this._config.title??this._t.messages;if(this._loading)return B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="loading"><ha-circular-progress indeterminate></ha-circular-progress></div>
        </ha-card>
      `;if(this._error&&0===this._serviceMessages.length&&0===this._alarmMessages.length)return B`
        <ha-card>
          <div class="card-header">${t}</div>
          <div class="error-msg">${this._t.error}</div>
        </ha-card>
      `;const e=this._alarmMessages.length,s=this._serviceMessages.length;return B`
      <ha-card>
        <div class="card-header">
          ${t}
          <div class="badges">
            ${e>0?B`<span class="badge error">${e}</span>`:q}
            ${s>0?B`<span class="badge warning">${s}</span>`:q}
            ${0===e&&0===s?B`<span class="badge ok">OK</span>`:q}
          </div>
        </div>
        <div class="card-content">
          ${this._renderAlarms()} ${this._renderServiceMessages()}
          ${0===e&&0===s?B`<div class="empty-state">${this._t.noMessages}</div>`:q}
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
    `}_formatTimestamp(t){if(!t)return"";try{return new Date(t).toLocaleTimeString(this.hass?.config.language||"en",{hour:"2-digit",minute:"2-digit"})}catch{return t}}static getConfigElement(){return document.createElement("homematicip-messages-editor")}static getStubConfig(){return{entry_id:""}}getCardSize(){return 3}}t([dt({attribute:!1})],kt.prototype,"hass",void 0),t([pt()],kt.prototype,"_config",void 0),t([pt()],kt.prototype,"_serviceMessages",void 0),t([pt()],kt.prototype,"_alarmMessages",void 0),t([pt()],kt.prototype,"_loading",void 0),t([pt()],kt.prototype,"_error",void 0);const Pt="homematicip-messages-card";customElements.get(Pt)||customElements.define(Pt,kt);class Ot extends ot{constructor(){super(...arguments),this._entryOptions=[],this._computeLabel=t=>({entry_id:"Integration",title:"Title (optional)",show_alarms:"Show alarms",show_service:"Show service messages",max_messages:"Max messages",show_timestamp:"Show timestamps",poll_interval:"Poll interval"}[t.name]||t.name)}setConfig(t){this._config=t}connectedCallback(){super.connectedCallback(),this._loadEntries()}updated(t){t.has("hass")&&this.hass&&0===this._entryOptions.length&&this._loadEntries()}async _loadEntries(){this.hass&&(this._entryOptions=await bt(this.hass))}_buildSchema(){return[{name:"entry_id",required:!0,selector:{select:{options:this._entryOptions,mode:"dropdown"}}},{name:"title",selector:{text:{}}},{name:"show_alarms",selector:{boolean:{}},default:!0},{name:"show_service",selector:{boolean:{}},default:!0},{name:"max_messages",selector:{number:{min:1,max:50,mode:"box"}},default:10},{name:"show_timestamp",selector:{boolean:{}},default:!0},{name:"poll_interval",selector:{number:{min:5,max:300,mode:"box",unit_of_measurement:"s"}},default:30}]}render(){return this.hass&&this._config?B`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${this._buildSchema()}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:q}_valueChanged(t){var e;t.stopPropagation(),e={config:{...this._config,...t.detail.value}},this.dispatchEvent(new CustomEvent("config-changed",{bubbles:!0,composed:!0,detail:e}))}static{this.styles=a`
    ha-form {
      display: block;
    }
  `}}t([dt({attribute:!1})],Ot.prototype,"hass",void 0),t([pt()],Ot.prototype,"_config",void 0),t([pt()],Ot.prototype,"_entryOptions",void 0);const Mt="homematicip-messages-editor";customElements.get(Mt)||customElements.define(Mt,Ot),window.customCards=window.customCards||[];const Tt=(t,e,s)=>{window.customCards.some(e=>e.type===t)||window.customCards.push({type:t,name:e,description:s})};Tt("homematicip-system-health-card","HomematicIP System Health","System health, device statistics, and incidents for HomematicIP Local"),Tt("homematicip-device-status-card","HomematicIP Device Status","Device status overview with problem highlighting for HomematicIP Local"),Tt("homematicip-messages-card","HomematicIP Messages","Service messages and alarms with acknowledgment for HomematicIP Local");
