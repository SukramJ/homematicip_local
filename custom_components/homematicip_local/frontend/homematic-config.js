function e(e, t, i, s) {
  var n,
    r = arguments.length,
    a =
      r < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    a = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (n = e[o]) && (a = (r < 3 ? n(a) : r > 3 ? n(t, i, a) : n(t, i)) || a);
  return r > 3 && a && Object.defineProperty(t, i, a), a;
}
"function" == typeof SuppressedError && SuppressedError;
const t = globalThis,
  i =
    t.ShadowRoot &&
    (void 0 === t.ShadyCSS || t.ShadyCSS.nativeShadow) &&
    "adoptedStyleSheets" in Document.prototype &&
    "replace" in CSSStyleSheet.prototype,
  s = Symbol(),
  n = new WeakMap();
let r = class {
  constructor(e, t, i) {
    if (((this._$cssResult$ = !0), i !== s))
      throw Error(
        "CSSResult is not constructable. Use `unsafeCSS` or `css` instead.",
      );
    (this.cssText = e), (this.t = t);
  }
  get styleSheet() {
    let e = this.o;
    const t = this.t;
    if (i && void 0 === e) {
      const i = void 0 !== t && 1 === t.length;
      i && (e = n.get(t)),
        void 0 === e &&
          ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText),
          i && n.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const a = (e, ...t) => {
    const i =
      1 === e.length
        ? e[0]
        : t.reduce(
            (t, i, s) =>
              t +
              ((e) => {
                if (!0 === e._$cssResult$) return e.cssText;
                if ("number" == typeof e) return e;
                throw Error(
                  "Value passed to 'css' function must be a 'css' function result: " +
                    e +
                    ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.",
                );
              })(i) +
              e[s + 1],
            e[0],
          );
    return new r(i, e, s);
  },
  o = i
    ? (e) => e
    : (e) =>
        e instanceof CSSStyleSheet
          ? ((e) => {
              let t = "";
              for (const i of e.cssRules) t += i.cssText;
              return ((e) =>
                new r("string" == typeof e ? e : e + "", void 0, s))(t);
            })(e)
          : e,
  {
    is: d,
    defineProperty: c,
    getOwnPropertyDescriptor: l,
    getOwnPropertyNames: h,
    getOwnPropertySymbols: p,
    getPrototypeOf: u,
  } = Object,
  _ = globalThis,
  v = _.trustedTypes,
  g = v ? v.emptyScript : "",
  f = _.reactiveElementPolyfillSupport,
  m = (e, t) => e,
  y = {
    toAttribute(e, t) {
      switch (t) {
        case Boolean:
          e = e ? g : null;
          break;
        case Object:
        case Array:
          e = null == e ? e : JSON.stringify(e);
      }
      return e;
    },
    fromAttribute(e, t) {
      let i = e;
      switch (t) {
        case Boolean:
          i = null !== e;
          break;
        case Number:
          i = null === e ? null : Number(e);
          break;
        case Object:
        case Array:
          try {
            i = JSON.parse(e);
          } catch (e) {
            i = null;
          }
      }
      return i;
    },
  },
  $ = (e, t) => !d(e, t),
  b = {
    attribute: !0,
    type: String,
    converter: y,
    reflect: !1,
    useDefault: !1,
    hasChanged: $,
  };
(Symbol.metadata ??= Symbol("metadata")),
  (_.litPropertyMetadata ??= new WeakMap());
let x = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ??= []).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = b) {
    if (
      (t.state && (t.attribute = !1),
      this._$Ei(),
      this.prototype.hasOwnProperty(e) && ((t = Object.create(t)).wrapped = !0),
      this.elementProperties.set(e, t),
      !t.noAccessor)
    ) {
      const i = Symbol(),
        s = this.getPropertyDescriptor(e, i, t);
      void 0 !== s && c(this.prototype, e, s);
    }
  }
  static getPropertyDescriptor(e, t, i) {
    const { get: s, set: n } = l(this.prototype, e) ?? {
      get() {
        return this[t];
      },
      set(e) {
        this[t] = e;
      },
    };
    return {
      get: s,
      set(t) {
        const r = s?.call(this);
        n?.call(this, t), this.requestUpdate(e, r, i);
      },
      configurable: !0,
      enumerable: !0,
    };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? b;
  }
  static _$Ei() {
    if (this.hasOwnProperty(m("elementProperties"))) return;
    const e = u(this);
    e.finalize(),
      void 0 !== e.l && (this.l = [...e.l]),
      (this.elementProperties = new Map(e.elementProperties));
  }
  static finalize() {
    if (this.hasOwnProperty(m("finalized"))) return;
    if (
      ((this.finalized = !0), this._$Ei(), this.hasOwnProperty(m("properties")))
    ) {
      const e = this.properties,
        t = [...h(e), ...p(e)];
      for (const i of t) this.createProperty(i, e[i]);
    }
    const e = this[Symbol.metadata];
    if (null !== e) {
      const t = litPropertyMetadata.get(e);
      if (void 0 !== t)
        for (const [e, i] of t) this.elementProperties.set(e, i);
    }
    this._$Eh = new Map();
    for (const [e, t] of this.elementProperties) {
      const i = this._$Eu(e, t);
      void 0 !== i && this._$Eh.set(i, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(e) {
    const t = [];
    if (Array.isArray(e)) {
      const i = new Set(e.flat(1 / 0).reverse());
      for (const e of i) t.unshift(o(e));
    } else void 0 !== e && t.push(o(e));
    return t;
  }
  static _$Eu(e, t) {
    const i = t.attribute;
    return !1 === i
      ? void 0
      : "string" == typeof i
        ? i
        : "string" == typeof e
          ? e.toLowerCase()
          : void 0;
  }
  constructor() {
    super(),
      (this._$Ep = void 0),
      (this.isUpdatePending = !1),
      (this.hasUpdated = !1),
      (this._$Em = null),
      this._$Ev();
  }
  _$Ev() {
    (this._$ES = new Promise((e) => (this.enableUpdating = e))),
      (this._$AL = new Map()),
      this._$E_(),
      this.requestUpdate(),
      this.constructor.l?.forEach((e) => e(this));
  }
  addController(e) {
    (this._$EO ??= new Set()).add(e),
      void 0 !== this.renderRoot && this.isConnected && e.hostConnected?.();
  }
  removeController(e) {
    this._$EO?.delete(e);
  }
  _$E_() {
    const e = new Map(),
      t = this.constructor.elementProperties;
    for (const i of t.keys())
      this.hasOwnProperty(i) && (e.set(i, this[i]), delete this[i]);
    e.size > 0 && (this._$Ep = e);
  }
  createRenderRoot() {
    const e =
      this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return (
      ((e, s) => {
        if (i)
          e.adoptedStyleSheets = s.map((e) =>
            e instanceof CSSStyleSheet ? e : e.styleSheet,
          );
        else
          for (const i of s) {
            const s = document.createElement("style"),
              n = t.litNonce;
            void 0 !== n && s.setAttribute("nonce", n),
              (s.textContent = i.cssText),
              e.appendChild(s);
          }
      })(e, this.constructor.elementStyles),
      e
    );
  }
  connectedCallback() {
    (this.renderRoot ??= this.createRenderRoot()),
      this.enableUpdating(!0),
      this._$EO?.forEach((e) => e.hostConnected?.());
  }
  enableUpdating(e) {}
  disconnectedCallback() {
    this._$EO?.forEach((e) => e.hostDisconnected?.());
  }
  attributeChangedCallback(e, t, i) {
    this._$AK(e, i);
  }
  _$ET(e, t) {
    const i = this.constructor.elementProperties.get(e),
      s = this.constructor._$Eu(e, i);
    if (void 0 !== s && !0 === i.reflect) {
      const n = (
        void 0 !== i.converter?.toAttribute ? i.converter : y
      ).toAttribute(t, i.type);
      (this._$Em = e),
        null == n ? this.removeAttribute(s) : this.setAttribute(s, n),
        (this._$Em = null);
    }
  }
  _$AK(e, t) {
    const i = this.constructor,
      s = i._$Eh.get(e);
    if (void 0 !== s && this._$Em !== s) {
      const e = i.getPropertyOptions(s),
        n =
          "function" == typeof e.converter
            ? { fromAttribute: e.converter }
            : void 0 !== e.converter?.fromAttribute
              ? e.converter
              : y;
      this._$Em = s;
      const r = n.fromAttribute(t, e.type);
      (this[s] = r ?? this._$Ej?.get(s) ?? r), (this._$Em = null);
    }
  }
  requestUpdate(e, t, i, s = !1, n) {
    if (void 0 !== e) {
      const r = this.constructor;
      if (
        (!1 === s && (n = this[e]),
        (i ??= r.getPropertyOptions(e)),
        !(
          (i.hasChanged ?? $)(n, t) ||
          (i.useDefault &&
            i.reflect &&
            n === this._$Ej?.get(e) &&
            !this.hasAttribute(r._$Eu(e, i)))
        ))
      )
        return;
      this.C(e, t, i);
    }
    !1 === this.isUpdatePending && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: i, reflect: s, wrapped: n }, r) {
    (i &&
      !(this._$Ej ??= new Map()).has(e) &&
      (this._$Ej.set(e, r ?? t ?? this[e]), !0 !== n || void 0 !== r)) ||
      (this._$AL.has(e) ||
        (this.hasUpdated || i || (t = void 0), this._$AL.set(e, t)),
      !0 === s && this._$Em !== e && (this._$Eq ??= new Set()).add(e));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (e) {
      Promise.reject(e);
    }
    const e = this.scheduleUpdate();
    return null != e && (await e), !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (((this.renderRoot ??= this.createRenderRoot()), this._$Ep)) {
        for (const [e, t] of this._$Ep) this[e] = t;
        this._$Ep = void 0;
      }
      const e = this.constructor.elementProperties;
      if (e.size > 0)
        for (const [t, i] of e) {
          const { wrapped: e } = i,
            s = this[t];
          !0 !== e ||
            this._$AL.has(t) ||
            void 0 === s ||
            this.C(t, void 0, i, s);
        }
    }
    let e = !1;
    const t = this._$AL;
    try {
      (e = this.shouldUpdate(t)),
        e
          ? (this.willUpdate(t),
            this._$EO?.forEach((e) => e.hostUpdate?.()),
            this.update(t))
          : this._$EM();
    } catch (t) {
      throw ((e = !1), this._$EM(), t);
    }
    e && this._$AE(t);
  }
  willUpdate(e) {}
  _$AE(e) {
    this._$EO?.forEach((e) => e.hostUpdated?.()),
      this.hasUpdated || ((this.hasUpdated = !0), this.firstUpdated(e)),
      this.updated(e);
  }
  _$EM() {
    (this._$AL = new Map()), (this.isUpdatePending = !1);
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(e) {
    return !0;
  }
  update(e) {
    (this._$Eq &&= this._$Eq.forEach((e) => this._$ET(e, this[e]))),
      this._$EM();
  }
  updated(e) {}
  firstUpdated(e) {}
};
(x.elementStyles = []),
  (x.shadowRootOptions = { mode: "open" }),
  (x[m("elementProperties")] = new Map()),
  (x[m("finalized")] = new Map()),
  f?.({ ReactiveElement: x }),
  (_.reactiveElementVersions ??= []).push("2.1.2");
const A = globalThis,
  w = (e) => e,
  E = A.trustedTypes,
  C = E ? E.createPolicy("lit-html", { createHTML: (e) => e }) : void 0,
  S = "$lit$",
  k = `lit$${Math.random().toFixed(9).slice(2)}$`,
  I = "?" + k,
  T = `<${I}>`,
  P = document,
  M = () => P.createComment(""),
  U = (e) => null === e || ("object" != typeof e && "function" != typeof e),
  R = Array.isArray,
  O = "[ \t\n\f\r]",
  D = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,
  z = /-->/g,
  N = />/g,
  H = RegExp(
    `>|${O}(?:([^\\s"'>=/]+)(${O}*=${O}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,
    "g",
  ),
  j = /'/g,
  B = /"/g,
  L = /^(?:script|style|textarea|title)$/i,
  V = (
    (e) =>
    (t, ...i) => ({ _$litType$: e, strings: t, values: i })
  )(1),
  K = Symbol.for("lit-noChange"),
  W = Symbol.for("lit-nothing"),
  G = new WeakMap(),
  q = P.createTreeWalker(P, 129);
function F(e, t) {
  if (!R(e) || !e.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return void 0 !== C ? C.createHTML(t) : t;
}
const Y = (e, t) => {
  const i = e.length - 1,
    s = [];
  let n,
    r = 2 === t ? "<svg>" : 3 === t ? "<math>" : "",
    a = D;
  for (let t = 0; t < i; t++) {
    const i = e[t];
    let o,
      d,
      c = -1,
      l = 0;
    for (; l < i.length && ((a.lastIndex = l), (d = a.exec(i)), null !== d); )
      (l = a.lastIndex),
        a === D
          ? "!--" === d[1]
            ? (a = z)
            : void 0 !== d[1]
              ? (a = N)
              : void 0 !== d[2]
                ? (L.test(d[2]) && (n = RegExp("</" + d[2], "g")), (a = H))
                : void 0 !== d[3] && (a = H)
          : a === H
            ? ">" === d[0]
              ? ((a = n ?? D), (c = -1))
              : void 0 === d[1]
                ? (c = -2)
                : ((c = a.lastIndex - d[2].length),
                  (o = d[1]),
                  (a = void 0 === d[3] ? H : '"' === d[3] ? B : j))
            : a === B || a === j
              ? (a = H)
              : a === z || a === N
                ? (a = D)
                : ((a = H), (n = void 0));
    const h = a === H && e[t + 1].startsWith("/>") ? " " : "";
    r +=
      a === D
        ? i + T
        : c >= 0
          ? (s.push(o), i.slice(0, c) + S + i.slice(c) + k + h)
          : i + k + (-2 === c ? t : h);
  }
  return [
    F(e, r + (e[i] || "<?>") + (2 === t ? "</svg>" : 3 === t ? "</math>" : "")),
    s,
  ];
};
class Q {
  constructor({ strings: e, _$litType$: t }, i) {
    let s;
    this.parts = [];
    let n = 0,
      r = 0;
    const a = e.length - 1,
      o = this.parts,
      [d, c] = Y(e, t);
    if (
      ((this.el = Q.createElement(d, i)),
      (q.currentNode = this.el.content),
      2 === t || 3 === t)
    ) {
      const e = this.el.content.firstChild;
      e.replaceWith(...e.childNodes);
    }
    for (; null !== (s = q.nextNode()) && o.length < a; ) {
      if (1 === s.nodeType) {
        if (s.hasAttributes())
          for (const e of s.getAttributeNames())
            if (e.endsWith(S)) {
              const t = c[r++],
                i = s.getAttribute(e).split(k),
                a = /([.?@])?(.*)/.exec(t);
              o.push({
                type: 1,
                index: n,
                name: a[2],
                strings: i,
                ctor:
                  "." === a[1]
                    ? te
                    : "?" === a[1]
                      ? ie
                      : "@" === a[1]
                        ? se
                        : ee,
              }),
                s.removeAttribute(e);
            } else
              e.startsWith(k) &&
                (o.push({ type: 6, index: n }), s.removeAttribute(e));
        if (L.test(s.tagName)) {
          const e = s.textContent.split(k),
            t = e.length - 1;
          if (t > 0) {
            s.textContent = E ? E.emptyScript : "";
            for (let i = 0; i < t; i++)
              s.append(e[i], M()),
                q.nextNode(),
                o.push({ type: 2, index: ++n });
            s.append(e[t], M());
          }
        }
      } else if (8 === s.nodeType)
        if (s.data === I) o.push({ type: 2, index: n });
        else {
          let e = -1;
          for (; -1 !== (e = s.data.indexOf(k, e + 1)); )
            o.push({ type: 7, index: n }), (e += k.length - 1);
        }
      n++;
    }
  }
  static createElement(e, t) {
    const i = P.createElement("template");
    return (i.innerHTML = e), i;
  }
}
function J(e, t, i = e, s) {
  if (t === K) return t;
  let n = void 0 !== s ? i._$Co?.[s] : i._$Cl;
  const r = U(t) ? void 0 : t._$litDirective$;
  return (
    n?.constructor !== r &&
      (n?._$AO?.(!1),
      void 0 === r ? (n = void 0) : ((n = new r(e)), n._$AT(e, i, s)),
      void 0 !== s ? ((i._$Co ??= [])[s] = n) : (i._$Cl = n)),
    void 0 !== n && (t = J(e, n._$AS(e, t.values), n, s)),
    t
  );
}
class Z {
  constructor(e, t) {
    (this._$AV = []), (this._$AN = void 0), (this._$AD = e), (this._$AM = t);
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(e) {
    const {
        el: { content: t },
        parts: i,
      } = this._$AD,
      s = (e?.creationScope ?? P).importNode(t, !0);
    q.currentNode = s;
    let n = q.nextNode(),
      r = 0,
      a = 0,
      o = i[0];
    for (; void 0 !== o; ) {
      if (r === o.index) {
        let t;
        2 === o.type
          ? (t = new X(n, n.nextSibling, this, e))
          : 1 === o.type
            ? (t = new o.ctor(n, o.name, o.strings, this, e))
            : 6 === o.type && (t = new ne(n, this, e)),
          this._$AV.push(t),
          (o = i[++a]);
      }
      r !== o?.index && ((n = q.nextNode()), r++);
    }
    return (q.currentNode = P), s;
  }
  p(e) {
    let t = 0;
    for (const i of this._$AV)
      void 0 !== i &&
        (void 0 !== i.strings
          ? (i._$AI(e, i, t), (t += i.strings.length - 2))
          : i._$AI(e[t])),
        t++;
  }
}
class X {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(e, t, i, s) {
    (this.type = 2),
      (this._$AH = W),
      (this._$AN = void 0),
      (this._$AA = e),
      (this._$AB = t),
      (this._$AM = i),
      (this.options = s),
      (this._$Cv = s?.isConnected ?? !0);
  }
  get parentNode() {
    let e = this._$AA.parentNode;
    const t = this._$AM;
    return void 0 !== t && 11 === e?.nodeType && (e = t.parentNode), e;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(e, t = this) {
    (e = J(this, e, t)),
      U(e)
        ? e === W || null == e || "" === e
          ? (this._$AH !== W && this._$AR(), (this._$AH = W))
          : e !== this._$AH && e !== K && this._(e)
        : void 0 !== e._$litType$
          ? this.$(e)
          : void 0 !== e.nodeType
            ? this.T(e)
            : ((e) => R(e) || "function" == typeof e?.[Symbol.iterator])(e)
              ? this.k(e)
              : this._(e);
  }
  O(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), (this._$AH = this.O(e)));
  }
  _(e) {
    this._$AH !== W && U(this._$AH)
      ? (this._$AA.nextSibling.data = e)
      : this.T(P.createTextNode(e)),
      (this._$AH = e);
  }
  $(e) {
    const { values: t, _$litType$: i } = e,
      s =
        "number" == typeof i
          ? this._$AC(e)
          : (void 0 === i.el &&
              (i.el = Q.createElement(F(i.h, i.h[0]), this.options)),
            i);
    if (this._$AH?._$AD === s) this._$AH.p(t);
    else {
      const e = new Z(s, this),
        i = e.u(this.options);
      e.p(t), this.T(i), (this._$AH = e);
    }
  }
  _$AC(e) {
    let t = G.get(e.strings);
    return void 0 === t && G.set(e.strings, (t = new Q(e))), t;
  }
  k(e) {
    R(this._$AH) || ((this._$AH = []), this._$AR());
    const t = this._$AH;
    let i,
      s = 0;
    for (const n of e)
      s === t.length
        ? t.push((i = new X(this.O(M()), this.O(M()), this, this.options)))
        : (i = t[s]),
        i._$AI(n),
        s++;
    s < t.length && (this._$AR(i && i._$AB.nextSibling, s), (t.length = s));
  }
  _$AR(e = this._$AA.nextSibling, t) {
    for (this._$AP?.(!1, !0, t); e !== this._$AB; ) {
      const t = w(e).nextSibling;
      w(e).remove(), (e = t);
    }
  }
  setConnected(e) {
    void 0 === this._$AM && ((this._$Cv = e), this._$AP?.(e));
  }
}
class ee {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, i, s, n) {
    (this.type = 1),
      (this._$AH = W),
      (this._$AN = void 0),
      (this.element = e),
      (this.name = t),
      (this._$AM = s),
      (this.options = n),
      i.length > 2 || "" !== i[0] || "" !== i[1]
        ? ((this._$AH = Array(i.length - 1).fill(new String())),
          (this.strings = i))
        : (this._$AH = W);
  }
  _$AI(e, t = this, i, s) {
    const n = this.strings;
    let r = !1;
    if (void 0 === n)
      (e = J(this, e, t, 0)),
        (r = !U(e) || (e !== this._$AH && e !== K)),
        r && (this._$AH = e);
    else {
      const s = e;
      let a, o;
      for (e = n[0], a = 0; a < n.length - 1; a++)
        (o = J(this, s[i + a], t, a)),
          o === K && (o = this._$AH[a]),
          (r ||= !U(o) || o !== this._$AH[a]),
          o === W ? (e = W) : e !== W && (e += (o ?? "") + n[a + 1]),
          (this._$AH[a] = o);
    }
    r && !s && this.j(e);
  }
  j(e) {
    e === W
      ? this.element.removeAttribute(this.name)
      : this.element.setAttribute(this.name, e ?? "");
  }
}
class te extends ee {
  constructor() {
    super(...arguments), (this.type = 3);
  }
  j(e) {
    this.element[this.name] = e === W ? void 0 : e;
  }
}
class ie extends ee {
  constructor() {
    super(...arguments), (this.type = 4);
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== W);
  }
}
class se extends ee {
  constructor(e, t, i, s, n) {
    super(e, t, i, s, n), (this.type = 5);
  }
  _$AI(e, t = this) {
    if ((e = J(this, e, t, 0) ?? W) === K) return;
    const i = this._$AH,
      s =
        (e === W && i !== W) ||
        e.capture !== i.capture ||
        e.once !== i.once ||
        e.passive !== i.passive,
      n = e !== W && (i === W || s);
    s && this.element.removeEventListener(this.name, this, i),
      n && this.element.addEventListener(this.name, this, e),
      (this._$AH = e);
  }
  handleEvent(e) {
    "function" == typeof this._$AH
      ? this._$AH.call(this.options?.host ?? this.element, e)
      : this._$AH.handleEvent(e);
  }
}
class ne {
  constructor(e, t, i) {
    (this.element = e),
      (this.type = 6),
      (this._$AN = void 0),
      (this._$AM = t),
      (this.options = i);
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    J(this, e);
  }
}
const re = A.litHtmlPolyfillSupport;
re?.(Q, X), (A.litHtmlVersions ??= []).push("3.3.2");
const ae = globalThis;
class oe extends x {
  constructor() {
    super(...arguments),
      (this.renderOptions = { host: this }),
      (this._$Do = void 0);
  }
  createRenderRoot() {
    const e = super.createRenderRoot();
    return (this.renderOptions.renderBefore ??= e.firstChild), e;
  }
  update(e) {
    const t = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected),
      super.update(e),
      (this._$Do = ((e, t, i) => {
        const s = i?.renderBefore ?? t;
        let n = s._$litPart$;
        if (void 0 === n) {
          const e = i?.renderBefore ?? null;
          s._$litPart$ = n = new X(t.insertBefore(M(), e), e, void 0, i ?? {});
        }
        return n._$AI(e), n;
      })(t, this.renderRoot, this.renderOptions));
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return K;
  }
}
(oe._$litElement$ = !0),
  (oe.finalized = !0),
  ae.litElementHydrateSupport?.({ LitElement: oe });
const de = ae.litElementPolyfillSupport;
de?.({ LitElement: oe }), (ae.litElementVersions ??= []).push("4.2.2");
const ce = (e) => (t, i) => {
    if (customElements.get(e)) return;
    void 0 !== i
      ? i.addInitializer(() => {
          customElements.get(e) || customElements.define(e, t);
        })
      : customElements.define(e, t);
  },
  le = {
    attribute: !0,
    type: String,
    converter: y,
    reflect: !1,
    hasChanged: $,
  },
  he = (e = le, t, i) => {
    const { kind: s, metadata: n } = i;
    let r = globalThis.litPropertyMetadata.get(n);
    if (
      (void 0 === r && globalThis.litPropertyMetadata.set(n, (r = new Map())),
      "setter" === s && ((e = Object.create(e)).wrapped = !0),
      r.set(i.name, e),
      "accessor" === s)
    ) {
      const { name: s } = i;
      return {
        set(i) {
          const n = t.get.call(this);
          t.set.call(this, i), this.requestUpdate(s, n, e, !0, i);
        },
        init(t) {
          return void 0 !== t && this.C(s, void 0, e, t), t;
        },
      };
    }
    if ("setter" === s) {
      const { name: s } = i;
      return function (i) {
        const n = this[s];
        t.call(this, i), this.requestUpdate(s, n, e, !0, i);
      };
    }
    throw Error("Unsupported decorator location: " + s);
  };
function pe(e) {
  return (t, i) =>
    "object" == typeof i
      ? he(e, t, i)
      : ((e, t, i) => {
          const s = t.hasOwnProperty(i);
          return (
            t.constructor.createProperty(i, e),
            s ? Object.getOwnPropertyDescriptor(t, i) : void 0
          );
        })(e, t, i);
}
function ue(e) {
  return pe({ ...e, state: !0, attribute: !1 });
}
const _e = a`
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
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: var(--primary-color);
    font-size: 14px;
    padding: 8px 0;
    background: none;
    border: none;
    font-family: inherit;
  }

  .back-button:hover {
    text-decoration: underline;
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

    .action-bar button {
      width: 100%;
    }

    .status-grid {
      grid-template-columns: 1fr;
    }
  }
`;
async function ve(e, t) {
  return (
    await e.callWS({
      type: "homematicip_local/config/list_devices",
      entry_id: t,
    })
  ).devices;
}
const ge = {
  en: {
    common: {
      back: "Back",
      loading: "Loading...",
      save: "Save",
      cancel: "Cancel",
      yes: "Yes",
      no: "No",
      toggle_on: "On",
      toggle_off: "Off",
    },
    device_list: {
      title: "Homematic Device Configuration",
      select_ccu: "CCU",
      select_placeholder: "Select a CCU...",
      search_placeholder: "Search devices...",
      no_entry_selected: "Please select a CCU to view devices.",
      no_devices: "No configurable devices found.",
      channels: "channels",
    },
    device_detail: {
      address: "Address",
      firmware: "Firmware",
      channel: "Channel",
      configure_master: "Configure MASTER",
      no_master_config: "No MASTER configuration available.",
      not_found: "Device not found.",
      yes: "Yes",
      no: "No",
      reachable: "Reachable",
      unreachable: "Unreachable",
    },
    channel_config: {
      save: "Save",
      saving: "Saving...",
      discard: "Discard Changes",
      reset_defaults: "Reset to Defaults",
      confirm_save_title: "Save Changes",
      confirm_save_text: "Apply {count} change(s) to the device?",
      unsaved_title: "Unsaved Changes",
      unsaved_warning: "You have unsaved changes. Discard them and go back?",
      save_success: "Changes saved successfully.",
      save_failed: "Failed to save changes.",
      validation_failed:
        "Validation failed. Please check the highlighted fields.",
    },
  },
  de: {
    common: {
      back: "Zurück",
      loading: "Laden...",
      save: "Speichern",
      cancel: "Abbrechen",
      yes: "Ja",
      no: "Nein",
      toggle_on: "Ein",
      toggle_off: "Aus",
    },
    device_list: {
      title: "Homematic Gerätekonfiguration",
      select_ccu: "CCU",
      select_placeholder: "CCU auswählen...",
      search_placeholder: "Geräte suchen...",
      no_entry_selected: "Bitte eine CCU auswählen, um Geräte anzuzeigen.",
      no_devices: "Keine konfigurierbaren Geräte gefunden.",
      channels: "Kanäle",
    },
    device_detail: {
      address: "Adresse",
      firmware: "Firmware",
      channel: "Kanal",
      configure_master: "MASTER konfigurieren",
      no_master_config: "Keine MASTER-Konfiguration verfügbar.",
      not_found: "Gerät nicht gefunden.",
      yes: "Ja",
      no: "Nein",
      reachable: "Erreichbar",
      unreachable: "Nicht erreichbar",
    },
    channel_config: {
      save: "Speichern",
      saving: "Speichern...",
      discard: "Änderungen verwerfen",
      reset_defaults: "Standardwerte laden",
      confirm_save_title: "Änderungen speichern",
      confirm_save_text: "{count} Änderung(en) auf das Gerät anwenden?",
      unsaved_title: "Ungespeicherte Änderungen",
      unsaved_warning:
        "Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",
      save_success: "Änderungen erfolgreich gespeichert.",
      save_failed: "Fehler beim Speichern der Änderungen.",
      validation_failed:
        "Validierung fehlgeschlagen. Bitte die markierten Felder prüfen.",
    },
  },
};
function fe(e, t = "") {
  const i = {};
  for (const [s, n] of Object.entries(e)) {
    const e = t ? `${t}.${s}` : s;
    "string" == typeof n
      ? (i[e] = n)
      : "object" == typeof n && null !== n && Object.assign(i, fe(n, e));
  }
  return i;
}
const me = new Map();
function ye(e) {
  if (me.has(e)) return me.get(e);
  const t = fe(ge[e] ?? ge.en);
  return me.set(e, t), t;
}
function $e(e, t, i) {
  const s = ye(e.config.language ?? "en");
  let n = s[t] ?? s[t.replace(/^panel\./, "")] ?? t;
  if (i)
    for (const [e, t] of Object.entries(i)) n = n.replace(`{${e}}`, String(t));
  return n;
}
let be = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.entries = []),
      (this._devices = []),
      (this._loading = !1),
      (this._searchQuery = ""),
      (this._error = "");
  }
  updated(e) {
    e.has("entryId") && this.entryId && this._fetchDevices();
  }
  async _fetchDevices() {
    if (this.entryId) {
      (this._loading = !0), (this._error = "");
      try {
        this._devices = await ve(this.hass, this.entryId);
      } catch (e) {
        (this._error = String(e)), (this._devices = []);
      } finally {
        this._loading = !1;
      }
    }
  }
  _l(e, t) {
    return $e(this.hass, e, t);
  }
  get _filteredDevices() {
    if (!this._searchQuery) return this._devices;
    const e = this._searchQuery.toLowerCase();
    return this._devices.filter(
      (t) =>
        t.name.toLowerCase().includes(e) ||
        t.address.toLowerCase().includes(e) ||
        t.model.toLowerCase().includes(e),
    );
  }
  get _groupedDevices() {
    const e = new Map();
    for (const t of this._filteredDevices) {
      const i = t.interface_id.split("-").slice(1).join("-") || t.interface_id;
      e.has(i) || e.set(i, []), e.get(i).push(t);
    }
    for (const t of e.values()) {
      t.sort((a, b) => a.name.localeCompare(b.name));
    }
    return e;
  }
  _handleEntryChanged(e) {
    const t = e.target;
    this.dispatchEvent(
      new CustomEvent("entry-changed", {
        detail: { entryId: t.value },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _handleDeviceClick(e) {
    this.dispatchEvent(
      new CustomEvent("device-selected", {
        detail: { device: e.address, interfaceId: e.interface_id },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  render() {
    return V`
      <div class="panel-header">
        <h1>${this._l("device_list.title")}</h1>
      </div>

      ${
        this.entries.length > 1
          ? V`
            <div class="entry-selector">
              <label>${this._l("device_list.select_ccu")}</label>
              <select @change=${this._handleEntryChanged}>
                <option value="" ?selected=${!this.entryId}>
                  ${this._l("device_list.select_placeholder")}
                </option>
                ${this.entries.map(
                  (e) => V`
                    <option
                      value=${e.entry_id}
                      ?selected=${e.entry_id === this.entryId}
                    >
                      ${e.title}
                    </option>
                  `,
                )}
              </select>
            </div>
          `
          : W
      }

      ${
        this.entryId
          ? V`
            <div class="search-bar">
              <input
                type="text"
                .value=${this._searchQuery}
                @input=${(e) => {
                  this._searchQuery = e.target.value;
                }}
                placeholder=${this._l("device_list.search_placeholder")}
              />
            </div>
          `
          : W
      }

      ${
        this._loading
          ? V`<div class="loading"><span>${this._l(
              "common.loading",
            )}</span></div>`
          : this._error
            ? V`<div class="error">${this._error}</div>`
            : this.entryId
              ? 0 === this._filteredDevices.length
                ? V`<div class="empty-state">${this._l(
                    "device_list.no_devices",
                  )}</div>`
                : this._renderDeviceGroups()
              : V`<div class="empty-state">${this._l(
                  "device_list.no_entry_selected",
                )}</div>`
      }
    `;
  }
  _renderDeviceGroups() {
    return V`
      ${Array.from(this._groupedDevices.entries()).map(
        ([e, t]) => V`
          <div class="interface-group">
            <div class="interface-header">${e}</div>
            ${t.map(
              (e) => V`
                <div
                  class="device-card"
                  @click=${() => this._handleDeviceClick(e)}
                >
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
                  <div class="device-arrow">\u25B8</div>
                </div>
              `,
            )}
          </div>
        `,
      )}
    `;
  }
  static {
    this.styles = [
      _e,
      a`
      .panel-header h1 {
        margin: 0 0 16px;
        font-size: 24px;
        font-weight: 400;
      }

      .entry-selector {
        margin-bottom: 16px;
      }

      .entry-selector label {
        display: block;
        font-size: 14px;
        color: var(--secondary-text-color);
        margin-bottom: 4px;
      }

      .entry-selector select {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid var(--divider-color);
        border-radius: 4px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
        font-size: 14px;
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

      .device-arrow {
        color: var(--secondary-text-color);
        font-size: 18px;
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
    `,
    ];
  }
};
e([pe({ attribute: !1 })], be.prototype, "hass", void 0),
  e([pe()], be.prototype, "entryId", void 0),
  e([pe({ attribute: !1 })], be.prototype, "entries", void 0),
  e([ue()], be.prototype, "_devices", void 0),
  e([ue()], be.prototype, "_loading", void 0),
  e([ue()], be.prototype, "_searchQuery", void 0),
  e([ue()], be.prototype, "_error", void 0),
  (be = e([ce("hm-device-list")], be));
const xe = [
  "RSSI_DEVICE",
  "RSSI_PEER",
  "DUTY_CYCLE",
  "LOW_BAT",
  "UNREACH",
  "SABOTAGE",
  "CONFIG_PENDING",
  "UPDATE_PENDING",
];
let Ae = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.deviceAddress = ""),
      (this._device = null),
      (this._maintenanceValues = {}),
      (this._loading = !0),
      (this._error = "");
  }
  updated(e) {
    (e.has("entryId") || e.has("deviceAddress")) &&
      this.entryId &&
      this.deviceAddress &&
      this._fetchDevice();
  }
  async _fetchDevice() {
    (this._loading = !0), (this._error = "");
    try {
      const e = await ve(this.hass, this.entryId);
      if (
        ((this._device =
          e.find((e) => e.address === this.deviceAddress) ?? null),
        this._device)
      ) {
        const e = this._device.channels.find((e) => e.address.endsWith(":0"));
        e &&
          e.paramset_keys.includes("VALUES") &&
          (this._maintenanceValues = await (async function (
            e,
            t,
            i,
            s,
            n = "MASTER",
          ) {
            return (
              await e.callWS({
                type: "homematicip_local/config/get_paramset",
                entry_id: t,
                interface_id: i,
                channel_address: s,
                paramset_key: n,
              })
            ).values;
          })(this.hass, this.entryId, this.interfaceId, e.address, "VALUES"));
      }
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return $e(this.hass, e, t);
  }
  _handleBack() {
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  _handleChannelClick(e) {
    this.dispatchEvent(
      new CustomEvent("channel-selected", {
        detail: {
          channel: e.address,
          interfaceId: this.interfaceId,
          channelType: e.channel_type,
          paramsetKey: "MASTER",
          deviceName: this._device?.name ?? "",
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  render() {
    if (this._loading)
      return V`<div class="loading">${this._l("common.loading")}</div>`;
    if (this._error) return V`<div class="error">${this._error}</div>`;
    if (!this._device)
      return V`<div class="empty-state">${this._l(
        "device_detail.not_found",
      )}</div>`;
    const e = this._device,
      t = e.channels.find((e) => e.address.endsWith(":0")),
      i = e.channels.filter((e) => !e.address.endsWith(":0"));
    return V`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="device-header">
        <h2>${e.model} \u2014 ${e.name}</h2>
        <div class="device-info">
          ${this._l("device_detail.address")}: ${e.address} |
          ${this._l("device_detail.firmware")}: ${e.firmware}
        </div>
      </div>

      ${t ? this._renderMaintenanceChannel(t) : W}
      ${i.map((e) => this._renderChannel(e))}
    `;
  }
  _renderMaintenanceChannel(e) {
    const t = Object.keys(this._maintenanceValues).length > 0,
      i = e.paramset_keys.includes("MASTER"),
      l = e.channel_type_label || e.channel_type;
    return V`
      <div class="channel-card maintenance">
        <div class="channel-header">
          ${this._l("device_detail.channel")} 0: ${l}
        </div>
        ${t ? this._renderStatusSummary() : W}
        ${
          i
            ? V`
              <div class="channel-actions">
                <button
                  class="configure-button"
                  @click=${() => this._handleChannelClick(e)}
                >
                  ${this._l("device_detail.configure_master")} \u25B8
                </button>
              </div>
            `
            : W
        }
      </div>
    `;
  }
  _renderStatusSummary() {
    const e = this._maintenanceValues,
      t = [];
    for (const i of xe) {
      if (!(i in e)) continue;
      const s = e[i];
      let n, r;
      switch (i) {
        case "RSSI_DEVICE":
        case "RSSI_PEER":
          (n = `${s} dBm`), (r = "📶");
          break;
        case "DUTY_CYCLE":
          (n = "number" == typeof s ? `${s.toFixed(1)}%` : String(s)),
            (r = "⏱");
          break;
        case "LOW_BAT":
          (n = s ? this._l("device_detail.yes") : this._l("device_detail.no")),
            (r = "🔋");
          break;
        case "UNREACH":
          (n = s
            ? this._l("device_detail.unreachable")
            : this._l("device_detail.reachable")),
            (r = s ? "❌" : "✅");
          break;
        default:
          (n = String(s)), (r = "ℹ️");
      }
      t.push({ label: i.replace(/_/g, " "), value: n, icon: r });
    }
    return 0 === t.length
      ? W
      : V`
      <div class="status-grid">
        ${t.map(
          (e) => V`
            <div class="status-item">
              <span class="status-icon">${e.icon}</span>
              <span>${e.label}: ${e.value}</span>
            </div>
          `,
        )}
      </div>
    `;
  }
  _renderChannel(e) {
    const t = e.address.split(":").pop() ?? "",
      i = e.paramset_keys.includes("MASTER"),
      l = e.channel_type_label || e.channel_type;
    return V`
      <div class="channel-card">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${l}
        </div>
        ${
          i
            ? V`
              <div class="channel-actions">
                <button
                  class="configure-button"
                  @click=${() => this._handleChannelClick(e)}
                >
                  ${this._l("device_detail.configure_master")} \u25B8
                </button>
              </div>
            `
            : V`
              <div class="channel-no-config">
                ${this._l("device_detail.no_master_config")}
              </div>
            `
        }
      </div>
    `;
  }
  static {
    this.styles = [
      _e,
      a`
      .device-header {
        margin-bottom: 16px;
      }

      .device-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
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
      }

      .channel-no-config {
        padding: 8px 16px;
        color: var(--secondary-text-color);
        font-size: 13px;
      }

      .configure-button {
        background: none;
        border: 1px solid var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        padding: 6px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
      }

      .configure-button:hover {
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }
    `,
    ];
  }
};
function we(e, t) {
  return new Promise((i) => {
    const s = new CustomEvent("hass-dialog", {
      bubbles: !0,
      composed: !0,
      detail: {
        dialogTag: "ha-confirmation-dialog",
        dialogImport: () => Promise.resolve(),
        dialogParams: { ...t, confirm: () => i(!0), cancel: () => i(!1) },
      },
    });
    e.dispatchEvent(s);
  });
}
function Ee(e, t) {
  const i = new CustomEvent("hass-notification", {
    bubbles: !0,
    composed: !0,
    detail: t,
  });
  e.dispatchEvent(i);
}
e([pe({ attribute: !1 })], Ae.prototype, "hass", void 0),
  e([pe()], Ae.prototype, "entryId", void 0),
  e([pe()], Ae.prototype, "interfaceId", void 0),
  e([pe()], Ae.prototype, "deviceAddress", void 0),
  e([ue()], Ae.prototype, "_device", void 0),
  e([ue()], Ae.prototype, "_maintenanceValues", void 0),
  e([ue()], Ae.prototype, "_loading", void 0),
  e([ue()], Ae.prototype, "_error", void 0),
  (Ae = e([ce("hm-device-detail")], Ae));
let Ce = class extends oe {
  constructor() {
    super(...arguments),
      (this.value = null),
      (this.modified = !1),
      (this.validationError = "");
  }
  _emitChange(e) {
    this.dispatchEvent(
      new CustomEvent("value-changed", {
        detail: {
          parameterId: this.parameter.id,
          value: e,
          currentValue: this.parameter.current_value,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  render() {
    const e = this.parameter,
      t = !e.writable;
    return V`
      <div class="parameter-row ${t ? "read-only" : ""}">
        <div class="parameter-label">
          ${e.label}
          ${e.unit ? V`<span class="parameter-unit">(${e.unit})</span>` : W}
          ${this.modified ? V`<span class="modified-dot"></span>` : W}
        </div>
        <div class="parameter-control">
          ${this._renderWidget(e, t)}
        </div>
      </div>
      ${
        this.validationError
          ? V`<div class="validation-error">${this.validationError}</div>`
          : W
      }
    `;
  }
  _renderWidget(e, t) {
    switch (e.widget) {
      case "toggle":
        return V`
          <label class="toggle">
            <input
              type="checkbox"
              .checked=${Boolean(this.value)}
              ?disabled=${t}
              @change=${(e) => {
                this._emitChange(e.target.checked);
              }}
            />
            <span class="toggle-label">${
              this.value
                ? $e(this.hass, "common.toggle_on")
                : $e(this.hass, "common.toggle_off")
            }</span>
          </label>
        `;
      case "slider_with_input":
        return V`
          <div class="slider-group">
            <input
              type="range"
              .min=${String(e.min ?? 0)}
              .max=${String(e.max ?? 100)}
              .step=${String(e.step ?? 1)}
              .value=${String(this.value ?? e.min ?? 0)}
              ?disabled=${t}
              @input=${(t) => {
                const i = Number(t.target.value);
                this._emitChange("integer" === e.type ? Math.round(i) : i);
              }}
            />
            <input
              type="number"
              class="number-input"
              .min=${String(e.min ?? "")}
              .max=${String(e.max ?? "")}
              .step=${String(e.step ?? 1)}
              .value=${String(this.value ?? "")}
              ?disabled=${t}
              @change=${(t) => {
                const i = Number(t.target.value);
                this._emitChange("integer" === e.type ? Math.round(i) : i);
              }}
            />
          </div>
        `;
      case "number_input":
        return V`
          <input
            type="number"
            class="number-input"
            .min=${String(e.min ?? "")}
            .max=${String(e.max ?? "")}
            .step=${String(e.step ?? 1)}
            .value=${String(this.value ?? "")}
            ?disabled=${t}
            @change=${(t) => {
              const i = Number(t.target.value);
              this._emitChange("integer" === e.type ? Math.round(i) : i);
            }}
          />
        `;
      case "dropdown":
        return V`
          <select
            ?disabled=${t}
            @change=${(e) => {
              const t = e.target.selectedIndex;
              this._emitChange(t);
            }}
          >
            ${(e.options ?? []).map(
              (i, s) => V`
                <option value=${s} ?selected=${this.value === s}>${
                  e.option_labels?.[i] ?? i
                }</option>
              `,
            )}
          </select>
        `;
      case "radio_group":
        return V`
          <div class="radio-group">
            ${(e.options ?? []).map(
              (i, s) => V`
                <label class="radio-item">
                  <input
                    type="radio"
                    name=${e.id}
                    .checked=${this.value === s}
                    ?disabled=${t}
                    @change=${() => this._emitChange(s)}
                  />
                  ${e.option_labels?.[i] ?? i}
                </label>
              `,
            )}
          </div>
        `;
      case "text_input":
        return V`
          <input
            type="text"
            .value=${String(this.value ?? "")}
            ?disabled=${t}
            @change=${(e) => {
              this._emitChange(e.target.value);
            }}
          />
        `;
      case "button":
        return V`
          <button
            class="action-button"
            ?disabled=${t}
            @click=${() => this._emitChange(!0)}
          >
            ${e.label}
          </button>
        `;
      default:
        return V`<span class="read-only-value">${String(
          this.value ?? "",
        )}</span>`;
    }
  }
  static {
    this.styles = [
      _e,
      a`
      .read-only {
        opacity: 0.7;
      }

      .toggle {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
      }

      .toggle input[type="checkbox"] {
        width: 18px;
        height: 18px;
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

      .number-input {
        width: 80px;
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      select {
        padding: 6px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
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

      .action-button {
        padding: 6px 16px;
        border: 1px solid var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        background: transparent;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
      }

      .read-only-value {
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      @media (max-width: 600px) {
        .slider-group {
          width: 100%;
        }

        .number-input {
          width: 100%;
          box-sizing: border-box;
        }

        select {
          width: 100%;
          box-sizing: border-box;
        }

        input[type="text"] {
          width: 100%;
          box-sizing: border-box;
        }
      }
    `,
    ];
  }
};
e([pe({ attribute: !1 })], Ce.prototype, "hass", void 0),
  e([pe({ attribute: !1 })], Ce.prototype, "parameter", void 0),
  e([pe()], Ce.prototype, "value", void 0),
  e([pe({ type: Boolean })], Ce.prototype, "modified", void 0),
  e([pe()], Ce.prototype, "validationError", void 0),
  (Ce = e([ce("hm-form-parameter")], Ce));
let Se = class extends oe {
  constructor() {
    super(...arguments),
      (this.pendingChanges = new Map()),
      (this.validationErrors = {});
  }
  _getEffectiveValue(e) {
    return this.pendingChanges.has(e.id)
      ? this.pendingChanges.get(e.id)
      : e.current_value;
  }
  _isModified(e) {
    return this.pendingChanges.has(e.id);
  }
  render() {
    return this.schema && this.schema.sections
      ? V`
      ${this.schema.sections.map(
        (e) => V`
          <div class="form-section">
            <div class="section-header">${e.title}</div>
            ${e.parameters.map(
              (e) => V`
                <hm-form-parameter
                  .hass=${this.hass}
                  .parameter=${e}
                  .value=${this._getEffectiveValue(e)}
                  .modified=${this._isModified(e)}
                  .validationError=${this.validationErrors[e.id] ?? ""}
                  @value-changed=${this._handleValueChanged}
                ></hm-form-parameter>
              `,
            )}
          </div>
        `,
      )}
    `
      : W;
  }
  _handleValueChanged(e) {
    this.dispatchEvent(
      new CustomEvent("value-changed", {
        detail: e.detail,
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  static {
    this.styles = [
      _e,
      a`
      .form-section {
        margin-bottom: 16px;
      }
    `,
    ];
  }
};
e([pe({ attribute: !1 })], Se.prototype, "hass", void 0),
  e([pe({ attribute: !1 })], Se.prototype, "schema", void 0),
  e([pe({ attribute: !1 })], Se.prototype, "pendingChanges", void 0),
  e([pe({ attribute: !1 })], Se.prototype, "validationErrors", void 0),
  (Se = e([ce("hm-config-form")], Se));
let ke = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.channelAddress = ""),
      (this.channelType = ""),
      (this.paramsetKey = "MASTER"),
      (this.deviceName = ""),
      (this._schema = null),
      (this._pendingChanges = new Map()),
      (this._loading = !0),
      (this._saving = !1),
      (this._error = ""),
      (this._validationErrors = {});
  }
  updated(e) {
    (e.has("channelAddress") || e.has("entryId")) &&
      this.entryId &&
      this.channelAddress &&
      this._fetchSchema();
  }
  async _fetchSchema() {
    (this._loading = !0),
      (this._error = ""),
      (this._pendingChanges = new Map()),
      (this._validationErrors = {});
    try {
      this._schema = await (async function (e, t, i, s, n = "", r = "MASTER") {
        return e.callWS({
          type: "homematicip_local/config/get_form_schema",
          entry_id: t,
          interface_id: i,
          channel_address: s,
          channel_type: n,
          paramset_key: r,
        });
      })(
        this.hass,
        this.entryId,
        this.interfaceId,
        this.channelAddress,
        this.channelType,
        this.paramsetKey,
      );
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return $e(this.hass, e, t);
  }
  get _isDirty() {
    return this._pendingChanges.size > 0;
  }
  _handleValueChanged(e) {
    const { parameterId: t, value: i, currentValue: s } = e.detail;
    i === s ? this._pendingChanges.delete(t) : this._pendingChanges.set(t, i),
      (this._pendingChanges = new Map(this._pendingChanges));
  }
  _handleDiscard() {
    (this._pendingChanges = new Map()), (this._validationErrors = {});
  }
  _handleResetDefaults() {
    if (this._schema) {
      this._pendingChanges = new Map();
      for (const e of this._schema.sections)
        for (const t of e.parameters)
          t.writable &&
            void 0 !== t.default &&
            t.default !== t.current_value &&
            this._pendingChanges.set(t.id, t.default);
      this._pendingChanges = new Map(this._pendingChanges);
    }
  }
  async _handleSave() {
    if (!this._isDirty || this._saving) return;
    const e = Object.fromEntries(this._pendingChanges),
      t = Object.keys(e).length,
      i = Object.entries(e)
        .map(([e, t]) => {
          const i = this._findParameter(e);
          return `${i?.label ?? e}: ${i?.current_value ?? "?"} → ${t}`;
        })
        .join("\n");
    if (
      await we(this, {
        title: this._l("channel_config.confirm_save_title"),
        text: `${this._l("channel_config.confirm_save_text", {
          count: t,
        })}\n\n${i}`,
        confirmText: this._l("common.save"),
        dismissText: this._l("common.cancel"),
      })
    ) {
      (this._saving = !0), (this._validationErrors = {});
      try {
        const t = await (async function (e, t, i, s, n, r = "MASTER", a = !0) {
          return e.callWS({
            type: "homematicip_local/config/put_paramset",
            entry_id: t,
            interface_id: i,
            channel_address: s,
            paramset_key: r,
            values: n,
            validate: a,
          });
        })(
          this.hass,
          this.entryId,
          this.interfaceId,
          this.channelAddress,
          e,
          this.paramsetKey,
        );
        t.success
          ? ((this._pendingChanges = new Map()),
            Ee(this, { message: this._l("channel_config.save_success") }),
            await this._fetchSchema())
          : Object.keys(t.validation_errors).length > 0 &&
            ((this._validationErrors = t.validation_errors),
            Ee(this, { message: this._l("channel_config.validation_failed") }));
      } catch (e) {
        (this._error = String(e)),
          Ee(this, { message: this._l("channel_config.save_failed") });
      } finally {
        this._saving = !1;
      }
    }
  }
  _findParameter(e) {
    if (this._schema)
      for (const t of this._schema.sections) {
        const i = t.parameters.find((t) => t.id === e);
        if (i) return i;
      }
  }
  async _handleBack() {
    if (this._isDirty) {
      if (
        !(await we(this, {
          title: this._l("channel_config.unsaved_title"),
          text: this._l("channel_config.unsaved_warning"),
          confirmText: this._l("channel_config.discard"),
          dismissText: this._l("common.cancel"),
          destructive: !0,
        }))
      )
        return;
    }
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  render() {
    return this._loading
      ? V`<div class="loading">${this._l("common.loading")}</div>`
      : this._error && !this._schema
        ? V`<div class="error">${this._error}</div>`
        : V`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="config-header">
        <h2>${this.deviceName || this.channelAddress}</h2>
        <div class="device-info">
          ${this.channelAddress}${
            this._schema?.channel_type_label || this._schema?.channel_type
              ? ` \u2014 ${
                  this._schema?.channel_type_label || this._schema?.channel_type
                }`
              : ""
          }
        </div>
      </div>

      ${this._error ? V`<div class="error">${this._error}</div>` : W}

      ${
        this._schema
          ? V`
            <hm-config-form
              .hass=${this.hass}
              .schema=${this._schema}
              .pendingChanges=${this._pendingChanges}
              .validationErrors=${this._validationErrors}
              @value-changed=${this._handleValueChanged}
            ></hm-config-form>
          `
          : W
      }

      <div class="action-bar">
        <button
          class="btn btn-secondary"
          @click=${this._handleResetDefaults}
          ?disabled=${this._saving}
        >
          ${this._l("channel_config.reset_defaults")}
        </button>
        <button
          class="btn btn-secondary"
          @click=${this._handleDiscard}
          ?disabled=${!this._isDirty || this._saving}
        >
          ${this._l("channel_config.discard")}
        </button>
        <button
          class="btn btn-primary"
          @click=${this._handleSave}
          ?disabled=${!this._isDirty || this._saving}
        >
          ${
            this._saving
              ? this._l("channel_config.saving")
              : this._l("channel_config.save")
          }
        </button>
      </div>
    `;
  }
  static {
    this.styles = [
      _e,
      a`
      .config-header {
        margin-bottom: 16px;
      }

      .config-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .btn {
        padding: 8px 20px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
        border: 1px solid transparent;
      }

      .btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      .btn-primary {
        background: var(--primary-color, #03a9f4);
        color: #fff;
        border-color: var(--primary-color, #03a9f4);
      }

      .btn-primary:hover:not(:disabled) {
        opacity: 0.9;
      }

      .btn-secondary {
        background: transparent;
        color: var(--primary-text-color);
        border-color: var(--divider-color, #e0e0e0);
      }

      .btn-secondary:hover:not(:disabled) {
        background: var(--secondary-background-color, #f5f5f5);
      }
    `,
    ];
  }
};
e([pe({ attribute: !1 })], ke.prototype, "hass", void 0),
  e([pe()], ke.prototype, "entryId", void 0),
  e([pe()], ke.prototype, "interfaceId", void 0),
  e([pe()], ke.prototype, "channelAddress", void 0),
  e([pe()], ke.prototype, "channelType", void 0),
  e([pe()], ke.prototype, "paramsetKey", void 0),
  e([pe()], ke.prototype, "deviceName", void 0),
  e([ue()], ke.prototype, "_schema", void 0),
  e([ue()], ke.prototype, "_pendingChanges", void 0),
  e([ue()], ke.prototype, "_loading", void 0),
  e([ue()], ke.prototype, "_saving", void 0),
  e([ue()], ke.prototype, "_error", void 0),
  e([ue()], ke.prototype, "_validationErrors", void 0),
  (ke = e([ce("hm-channel-config")], ke));
let Ie = class extends oe {
  constructor() {
    super(...arguments),
      (this.narrow = !1),
      (this._view = "device-list"),
      (this._entryId = ""),
      (this._entries = []),
      (this._selectedDevice = ""),
      (this._selectedInterfaceId = ""),
      (this._selectedChannel = ""),
      (this._selectedChannelType = ""),
      (this._selectedParamsetKey = "MASTER"),
      (this._selectedDeviceName = "");
  }
  connectedCallback() {
    super.connectedCallback(), this._resolveEntryId();
  }
  async _resolveEntryId() {
    const e = await this.hass.callWS({
      type: "config_entries/get",
      domain: "homematicip_local",
    });
    (this._entries = e
      .filter((e) => "loaded" === e.state)
      .map((e) => ({ entry_id: e.entry_id, title: e.title }))),
      1 === this._entries.length && (this._entryId = this._entries[0].entry_id);
  }
  _navigateTo(e, t) {
    (this._view = e),
      t?.device && (this._selectedDevice = t.device),
      t?.interfaceId && (this._selectedInterfaceId = t.interfaceId),
      t?.channel && (this._selectedChannel = t.channel),
      t?.channelType && (this._selectedChannelType = t.channelType),
      t?.paramsetKey && (this._selectedParamsetKey = t.paramsetKey),
      t?.deviceName && (this._selectedDeviceName = t.deviceName);
  }
  render() {
    switch (this._view) {
      case "device-list":
        return V`
          <hm-device-list
            .hass=${this.hass}
            .entryId=${this._entryId}
            .entries=${this._entries}
            @entry-changed=${(e) => {
              this._entryId = e.detail.entryId;
            }}
            @device-selected=${(e) =>
              this._navigateTo("device-detail", e.detail)}
          ></hm-device-list>
        `;
      case "device-detail":
        return V`
          <hm-device-detail
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            @channel-selected=${(e) =>
              this._navigateTo("channel-config", e.detail)}
            @back=${() => this._navigateTo("device-list")}
          ></hm-device-detail>
        `;
      case "channel-config":
        return V`
          <hm-channel-config
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .channelAddress=${this._selectedChannel}
            .channelType=${this._selectedChannelType}
            .paramsetKey=${this._selectedParamsetKey}
            .deviceName=${this._selectedDeviceName}
            @back=${() =>
              this._navigateTo("device-detail", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
          ></hm-channel-config>
        `;
    }
  }
  static {
    this.styles = a`
    :host {
      display: block;
      padding: 16px;
      max-width: 1200px;
      margin: 0 auto;
      font-family: var(--paper-font-body1_-_font-family, "Roboto", sans-serif);
      color: var(--primary-text-color);
      background-color: var(--primary-background-color);
    }

    @media (max-width: 600px) {
      :host {
        padding: 8px;
      }
    }
  `;
  }
};
e([pe({ attribute: !1 })], Ie.prototype, "hass", void 0),
  e([pe({ attribute: !1 })], Ie.prototype, "panel", void 0),
  e([pe({ type: Boolean, reflect: !0 })], Ie.prototype, "narrow", void 0),
  e([ue()], Ie.prototype, "_view", void 0),
  e([ue()], Ie.prototype, "_entryId", void 0),
  e([ue()], Ie.prototype, "_entries", void 0),
  e([ue()], Ie.prototype, "_selectedDevice", void 0),
  e([ue()], Ie.prototype, "_selectedInterfaceId", void 0),
  e([ue()], Ie.prototype, "_selectedChannel", void 0),
  e([ue()], Ie.prototype, "_selectedChannelType", void 0),
  e([ue()], Ie.prototype, "_selectedParamsetKey", void 0),
  (Ie = e([ce("homematic-config")], Ie));
export { Ie as HomematicConfigPanel };
