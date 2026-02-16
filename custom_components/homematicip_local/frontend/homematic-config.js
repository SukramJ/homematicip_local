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
    getPrototypeOf: _,
  } = Object,
  v = globalThis,
  u = v.trustedTypes,
  g = u ? u.emptyScript : "",
  f = v.reactiveElementPolyfillSupport,
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
  b = (e, t) => !d(e, t),
  x = {
    attribute: !0,
    type: String,
    converter: y,
    reflect: !1,
    useDefault: !1,
    hasChanged: b,
  };
(Symbol.metadata ??= Symbol("metadata")),
  (v.litPropertyMetadata ??= new WeakMap());
let $ = class extends HTMLElement {
  static addInitializer(e) {
    this._$Ei(), (this.l ??= []).push(e);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(e, t = x) {
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
    return this.elementProperties.get(e) ?? x;
  }
  static _$Ei() {
    if (this.hasOwnProperty(m("elementProperties"))) return;
    const e = _(this);
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
          (i.hasChanged ?? b)(n, t) ||
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
($.elementStyles = []),
  ($.shadowRootOptions = { mode: "open" }),
  ($[m("elementProperties")] = new Map()),
  ($[m("finalized")] = new Map()),
  f?.({ ReactiveElement: $ }),
  (v.reactiveElementVersions ??= []).push("2.1.2");
const k = globalThis,
  w = (e) => e,
  C = k.trustedTypes,
  A = C ? C.createPolicy("lit-html", { createHTML: (e) => e }) : void 0,
  S = "$lit$",
  E = `lit$${Math.random().toFixed(9).slice(2)}$`,
  I = "?" + E,
  T = `<${I}>`,
  R = document,
  z = () => R.createComment(""),
  D = (e) => null === e || ("object" != typeof e && "function" != typeof e),
  P = Array.isArray,
  M = "[ \t\n\f\r]",
  N = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,
  U = /-->/g,
  L = />/g,
  O = RegExp(
    `>|${M}(?:([^\\s"'>=/]+)(${M}*=${M}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,
    "g",
  ),
  K = /'/g,
  H = /"/g,
  j = /^(?:script|style|textarea|title)$/i,
  B = (
    (e) =>
    (t, ...i) => ({ _$litType$: e, strings: t, values: i })
  )(1),
  V = Symbol.for("lit-noChange"),
  W = Symbol.for("lit-nothing"),
  F = new WeakMap(),
  G = R.createTreeWalker(R, 129);
function Q(e, t) {
  if (!P(e) || !e.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return void 0 !== A ? A.createHTML(t) : t;
}
const q = (e, t) => {
  const i = e.length - 1,
    s = [];
  let n,
    r = 2 === t ? "<svg>" : 3 === t ? "<math>" : "",
    a = N;
  for (let t = 0; t < i; t++) {
    const i = e[t];
    let o,
      d,
      c = -1,
      l = 0;
    for (; l < i.length && ((a.lastIndex = l), (d = a.exec(i)), null !== d); )
      (l = a.lastIndex),
        a === N
          ? "!--" === d[1]
            ? (a = U)
            : void 0 !== d[1]
              ? (a = L)
              : void 0 !== d[2]
                ? (j.test(d[2]) && (n = RegExp("</" + d[2], "g")), (a = O))
                : void 0 !== d[3] && (a = O)
          : a === O
            ? ">" === d[0]
              ? ((a = n ?? N), (c = -1))
              : void 0 === d[1]
                ? (c = -2)
                : ((c = a.lastIndex - d[2].length),
                  (o = d[1]),
                  (a = void 0 === d[3] ? O : '"' === d[3] ? H : K))
            : a === H || a === K
              ? (a = O)
              : a === U || a === L
                ? (a = N)
                : ((a = O), (n = void 0));
    const h = a === O && e[t + 1].startsWith("/>") ? " " : "";
    r +=
      a === N
        ? i + T
        : c >= 0
          ? (s.push(o), i.slice(0, c) + S + i.slice(c) + E + h)
          : i + E + (-2 === c ? t : h);
  }
  return [
    Q(e, r + (e[i] || "<?>") + (2 === t ? "</svg>" : 3 === t ? "</math>" : "")),
    s,
  ];
};
class Y {
  constructor({ strings: e, _$litType$: t }, i) {
    let s;
    this.parts = [];
    let n = 0,
      r = 0;
    const a = e.length - 1,
      o = this.parts,
      [d, c] = q(e, t);
    if (
      ((this.el = Y.createElement(d, i)),
      (G.currentNode = this.el.content),
      2 === t || 3 === t)
    ) {
      const e = this.el.content.firstChild;
      e.replaceWith(...e.childNodes);
    }
    for (; null !== (s = G.nextNode()) && o.length < a; ) {
      if (1 === s.nodeType) {
        if (s.hasAttributes())
          for (const e of s.getAttributeNames())
            if (e.endsWith(S)) {
              const t = c[r++],
                i = s.getAttribute(e).split(E),
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
              e.startsWith(E) &&
                (o.push({ type: 6, index: n }), s.removeAttribute(e));
        if (j.test(s.tagName)) {
          const e = s.textContent.split(E),
            t = e.length - 1;
          if (t > 0) {
            s.textContent = C ? C.emptyScript : "";
            for (let i = 0; i < t; i++)
              s.append(e[i], z()),
                G.nextNode(),
                o.push({ type: 2, index: ++n });
            s.append(e[t], z());
          }
        }
      } else if (8 === s.nodeType)
        if (s.data === I) o.push({ type: 2, index: n });
        else {
          let e = -1;
          for (; -1 !== (e = s.data.indexOf(E, e + 1)); )
            o.push({ type: 7, index: n }), (e += E.length - 1);
        }
      n++;
    }
  }
  static createElement(e, t) {
    const i = R.createElement("template");
    return (i.innerHTML = e), i;
  }
}
function J(e, t, i = e, s) {
  if (t === V) return t;
  let n = void 0 !== s ? i._$Co?.[s] : i._$Cl;
  const r = D(t) ? void 0 : t._$litDirective$;
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
      s = (e?.creationScope ?? R).importNode(t, !0);
    G.currentNode = s;
    let n = G.nextNode(),
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
      r !== o?.index && ((n = G.nextNode()), r++);
    }
    return (G.currentNode = R), s;
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
      D(e)
        ? e === W || null == e || "" === e
          ? (this._$AH !== W && this._$AR(), (this._$AH = W))
          : e !== this._$AH && e !== V && this._(e)
        : void 0 !== e._$litType$
          ? this.$(e)
          : void 0 !== e.nodeType
            ? this.T(e)
            : ((e) => P(e) || "function" == typeof e?.[Symbol.iterator])(e)
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
    this._$AH !== W && D(this._$AH)
      ? (this._$AA.nextSibling.data = e)
      : this.T(R.createTextNode(e)),
      (this._$AH = e);
  }
  $(e) {
    const { values: t, _$litType$: i } = e,
      s =
        "number" == typeof i
          ? this._$AC(e)
          : (void 0 === i.el &&
              (i.el = Y.createElement(Q(i.h, i.h[0]), this.options)),
            i);
    if (this._$AH?._$AD === s) this._$AH.p(t);
    else {
      const e = new Z(s, this),
        i = e.u(this.options);
      e.p(t), this.T(i), (this._$AH = e);
    }
  }
  _$AC(e) {
    let t = F.get(e.strings);
    return void 0 === t && F.set(e.strings, (t = new Y(e))), t;
  }
  k(e) {
    P(this._$AH) || ((this._$AH = []), this._$AR());
    const t = this._$AH;
    let i,
      s = 0;
    for (const n of e)
      s === t.length
        ? t.push((i = new X(this.O(z()), this.O(z()), this, this.options)))
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
        (r = !D(e) || (e !== this._$AH && e !== V)),
        r && (this._$AH = e);
    else {
      const s = e;
      let a, o;
      for (e = n[0], a = 0; a < n.length - 1; a++)
        (o = J(this, s[i + a], t, a)),
          o === V && (o = this._$AH[a]),
          (r ||= !D(o) || o !== this._$AH[a]),
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
    if ((e = J(this, e, t, 0) ?? W) === V) return;
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
const re = k.litHtmlPolyfillSupport;
re?.(Y, X), (k.litHtmlVersions ??= []).push("3.3.2");
const ae = globalThis;
class oe extends $ {
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
          s._$litPart$ = n = new X(t.insertBefore(z(), e), e, void 0, i ?? {});
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
    return V;
  }
}
(oe._$litElement$ = !0),
  (oe.finalized = !0),
  ae.litElementHydrateSupport?.({ LitElement: oe });
const de = ae.litElementPolyfillSupport;
de?.({ LitElement: oe }), (ae.litElementVersions ??= []).push("4.2.2");
const ce = {
    attribute: !0,
    type: String,
    converter: y,
    reflect: !1,
    hasChanged: b,
  },
  le = (e = ce, t, i) => {
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
function he(e) {
  return (t, i) =>
    "object" == typeof i
      ? le(e, t, i)
      : ((e, t, i) => {
          const s = t.hasOwnProperty(i);
          return (
            t.constructor.createProperty(i, e),
            s ? Object.getOwnPropertyDescriptor(t, i) : void 0
          );
        })(e, t, i);
}
function pe(e) {
  return he({ ...e, state: !0, attribute: !1 });
}
function _e(e) {
  return (t) => (customElements.get(e) || customElements.define(e, t), t);
}
const ve = a`
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
`,
  ue = new Set(["BidCos-RF", "BidCos-Wired", "HmIP-RF"]);
async function ge(e, t) {
  return (
    await e.callWS({
      type: "homematicip_local/config/list_devices",
      entry_id: t,
    })
  ).devices;
}
async function fe(e, t, i, s, n = "", r = "MASTER") {
  return e.callWS({
    type: "homematicip_local/config/get_form_schema",
    entry_id: t,
    interface_id: i,
    channel_address: s,
    channel_type: n,
    paramset_key: r,
  });
}
async function me(e, t, i, s, n = "MASTER") {
  return e.callWS({
    type: "homematicip_local/config/session_open",
    entry_id: t,
    interface_id: i,
    channel_address: s,
    paramset_key: n,
  });
}
async function ye(e, t, i, s = "MASTER") {
  return e.callWS({
    type: "homematicip_local/config/session_discard",
    entry_id: t,
    channel_address: i,
    paramset_key: s,
  });
}
const be = {
  en: {
    common: {
      back: "Back",
      loading: "Loading...",
      save: "Save",
      cancel: "Cancel",
      yes: "Yes",
      no: "No",
    },
    device_list: {
      title: "Homematic Device Configuration",
      select_ccu: "CCU",
      select_placeholder: "Select a CCU...",
      search_placeholder: "Search devices...",
      no_entry_selected: "Please select a CCU to view devices.",
      no_devices: "No configurable devices found.",
      channels: "channels",
      unreachable: "Unreachable",
      reachable: "Reachable",
      low_battery: "Low battery",
      config_pending: "Configuration pending",
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
      export: "Export",
      import: "Import",
      export_success: "Configuration exported successfully.",
      export_failed: "Failed to export configuration.",
      import_confirm_title: "Import Configuration",
      import_confirm_text:
        "Import and apply configuration to channel {channel}?",
      import_success: "Configuration imported successfully.",
      import_failed: "Failed to import configuration.",
      import_validation_failed: "Import validation failed.",
      show_history: "Change History",
      show_links: "Direct Links",
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
      undo: "Undo",
      redo: "Redo",
    },
    change_history: {
      title: "Change History",
      empty: "No configuration changes recorded.",
      clear: "Clear History",
      clear_confirm_title: "Clear History",
      clear_confirm_text: "Delete all history entries? This cannot be undone.",
      clear_success: "History cleared ({count} entries removed).",
      source_manual: "Manual",
      source_import: "Import",
      source_copy: "Copy",
      parameters_changed: "{count} parameter(s) changed",
    },
    device_links: {
      title: "Direct Links",
      subtitle: "Direct links for {device}",
      empty: "No direct links configured.",
      add_link: "New Link",
      outgoing: "Outgoing",
      incoming: "Incoming",
      configure: "Configure",
      delete: "Delete",
      delete_confirm_title: "Delete Link",
      delete_confirm_text:
        "Remove the direct link from {sender} to {receiver}? The devices will no longer communicate directly.",
      delete_success: "Link deleted successfully.",
      delete_failed: "Failed to delete link.",
      channel_group: "Channel {channel}",
    },
    link_config: {
      title: "Link Configuration",
      sender: "Sender",
      receiver: "Receiver",
      save_success: "Link configuration saved.",
      save_failed: "Failed to save link configuration.",
      discard: "Discard Changes",
      confirm_save_title: "Save Link Changes",
      confirm_save_text: "Apply {count} change(s) to this link?",
      unsaved_title: "Unsaved Changes",
      unsaved_warning: "You have unsaved changes. Discard them and go back?",
    },
    add_link: {
      title: "New Direct Link",
      step_channel: "Step 1/3 — Select Channel",
      step_peer: "Step 2/3 — Select Partner",
      step_confirm: "Step 3/3 — Confirm",
      select_channel: "Select a channel from this device:",
      select_role: "Role of selected channel:",
      role_sender: "Sender (sends commands)",
      role_receiver: "Receiver (receives commands)",
      search_devices: "Search devices...",
      no_compatible: "No compatible channels found.",
      link_name: "Link name (optional)",
      create: "Create Link",
      create_success: "Link created successfully.",
      create_failed: "Failed to create link.",
      next: "Next",
      back: "Back",
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
    },
    device_list: {
      title: "Homematic Gerätekonfiguration",
      select_ccu: "CCU",
      select_placeholder: "CCU auswählen...",
      search_placeholder: "Geräte suchen...",
      no_entry_selected: "Bitte eine CCU auswählen, um Geräte anzuzeigen.",
      no_devices: "Keine konfigurierbaren Geräte gefunden.",
      channels: "Kanäle",
      unreachable: "Nicht erreichbar",
      reachable: "Erreichbar",
      low_battery: "Batterie schwach",
      config_pending: "Konfiguration ausstehend",
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
      export: "Exportieren",
      import: "Importieren",
      export_success: "Konfiguration erfolgreich exportiert.",
      export_failed: "Export der Konfiguration fehlgeschlagen.",
      import_confirm_title: "Konfiguration importieren",
      import_confirm_text:
        "Konfiguration importieren und auf Kanal {channel} anwenden?",
      import_success: "Konfiguration erfolgreich importiert.",
      import_failed: "Import der Konfiguration fehlgeschlagen.",
      import_validation_failed: "Import-Validierung fehlgeschlagen.",
      show_history: "Änderungsverlauf",
      show_links: "Direktverknüpfungen",
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
      undo: "Rückgängig",
      redo: "Wiederherstellen",
    },
    change_history: {
      title: "Änderungsverlauf",
      empty: "Keine Konfigurationsänderungen aufgezeichnet.",
      clear: "Verlauf löschen",
      clear_confirm_title: "Verlauf löschen",
      clear_confirm_text:
        "Alle Verlaufseinträge löschen? Dies kann nicht rückgängig gemacht werden.",
      clear_success: "Verlauf gelöscht ({count} Einträge entfernt).",
      source_manual: "Manuell",
      source_import: "Import",
      source_copy: "Kopie",
      parameters_changed: "{count} Parameter geändert",
    },
    device_links: {
      title: "Direktverknüpfungen",
      subtitle: "Direktverknüpfungen für {device}",
      empty: "Keine Direktverknüpfungen konfiguriert.",
      add_link: "Neue Verknüpfung",
      outgoing: "Ausgehend",
      incoming: "Eingehend",
      configure: "Konfigurieren",
      delete: "Löschen",
      delete_confirm_title: "Verknüpfung löschen",
      delete_confirm_text:
        "Direktverknüpfung von {sender} nach {receiver} entfernen? Die Geräte kommunizieren dann nicht mehr direkt.",
      delete_success: "Verknüpfung erfolgreich gelöscht.",
      delete_failed: "Fehler beim Löschen der Verknüpfung.",
      channel_group: "Kanal {channel}",
    },
    link_config: {
      title: "Link-Konfiguration",
      sender: "Sender",
      receiver: "Empfänger",
      save_success: "Link-Konfiguration gespeichert.",
      save_failed: "Fehler beim Speichern der Link-Konfiguration.",
      discard: "Änderungen verwerfen",
      confirm_save_title: "Link-Änderungen speichern",
      confirm_save_text: "{count} Änderung(en) auf diese Verknüpfung anwenden?",
      unsaved_title: "Ungespeicherte Änderungen",
      unsaved_warning:
        "Es gibt ungespeicherte Änderungen. Verwerfen und zurückgehen?",
    },
    add_link: {
      title: "Neue Direktverknüpfung",
      step_channel: "Schritt 1/3 — Kanal wählen",
      step_peer: "Schritt 2/3 — Partner wählen",
      step_confirm: "Schritt 3/3 — Bestätigen",
      select_channel: "Kanal dieses Geräts auswählen:",
      select_role: "Rolle des gewählten Kanals:",
      role_sender: "Sender (sendet Kommandos)",
      role_receiver: "Empfänger (empfängt Kommandos)",
      search_devices: "Geräte suchen...",
      no_compatible: "Keine kompatiblen Kanäle gefunden.",
      link_name: "Verknüpfungsname (optional)",
      create: "Verknüpfung erstellen",
      create_success: "Verknüpfung erfolgreich erstellt.",
      create_failed: "Fehler beim Erstellen der Verknüpfung.",
      next: "Weiter",
      back: "Zurück",
    },
  },
};
function xe(e, t = "") {
  const i = {};
  for (const [s, n] of Object.entries(e)) {
    const e = t ? `${t}.${s}` : s;
    "string" == typeof n
      ? (i[e] = n)
      : "object" == typeof n && null !== n && Object.assign(i, xe(n, e));
  }
  return i;
}
const $e = new Map();
function ke(e) {
  if ($e.has(e)) return $e.get(e);
  const t = xe(be[e] ?? be.en);
  return $e.set(e, t), t;
}
function we(e, t, i) {
  const s = ke(e.config.language ?? "en");
  let n = s[t] ?? s[t.replace(/^panel\./, "")] ?? t;
  if (i)
    for (const [e, t] of Object.entries(i)) n = n.replace(`{${e}}`, String(t));
  return n;
}
let Ce = class extends oe {
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
        this._devices = await ge(this.hass, this.entryId);
      } catch (e) {
        (this._error = String(e)), (this._devices = []);
      } finally {
        this._loading = !1;
      }
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
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
    const e = [...this._filteredDevices].sort((e, t) =>
        e.name.localeCompare(t.name),
      ),
      t = new Map();
    for (const i of e) {
      const e = i.interface_id.split("-").slice(1).join("-") || i.interface_id;
      t.has(e) || t.set(e, []), t.get(e).push(i);
    }
    return t;
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
  _renderMaintenanceIcons(e) {
    return e && 0 !== Object.keys(e).length
      ? B`
      <div class="device-status">
        ${
          !0 === e.unreach
            ? B`<span class="status-badge unreachable" title="${this._l(
                "device_list.unreachable",
              )}">&#x274C;</span>`
            : !1 === e.unreach
              ? B`<span class="status-badge reachable" title="${this._l(
                  "device_list.reachable",
                )}">&#x2705;</span>`
              : W
        }
        ${
          !0 === e.low_bat
            ? B`<span class="status-badge low-bat" title="${this._l(
                "device_list.low_battery",
              )}">&#x1F50B;</span>`
            : W
        }
        ${
          !0 === e.config_pending
            ? B`<span class="status-badge config-pending" title="${this._l(
                "device_list.config_pending",
              )}">&#x23F3;</span>`
            : W
        }
      </div>
    `
      : W;
  }
  render() {
    return B`
      <div class="panel-header">
        <h1>${this._l("device_list.title")}</h1>
      </div>

      ${
        this.entries.length > 1
          ? B`
            <div class="entry-selector">
              <label>${this._l("device_list.select_ccu")}</label>
              <select @change=${this._handleEntryChanged}>
                <option value="" ?selected=${!this.entryId}>
                  ${this._l("device_list.select_placeholder")}
                </option>
                ${this.entries.map(
                  (e) => B`
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
          ? B`
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
          ? B`<div class="loading"><span>${this._l(
              "common.loading",
            )}</span></div>`
          : this._error
            ? B`<div class="error">${this._error}</div>`
            : this.entryId
              ? 0 === this._filteredDevices.length
                ? B`<div class="empty-state">${this._l(
                    "device_list.no_devices",
                  )}</div>`
                : this._renderDeviceGroups()
              : B`<div class="empty-state">${this._l(
                  "device_list.no_entry_selected",
                )}</div>`
      }
    `;
  }
  _renderDeviceGroups() {
    return B`
      ${Array.from(this._groupedDevices.entries()).map(
        ([e, t]) => B`
          <div class="interface-group">
            <div class="interface-header">${e}</div>
            ${t.map(
              (e) => B`
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
                  ${this._renderMaintenanceIcons(e.maintenance)}
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
      ve,
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

      .device-status {
        display: flex;
        gap: 4px;
        align-items: center;
        margin-right: 8px;
      }

      .status-badge {
        font-size: 14px;
        cursor: default;
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
function Ae(e, t) {
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
function Se(e, t) {
  const i = new CustomEvent("hass-notification", {
    bubbles: !0,
    composed: !0,
    detail: t,
  });
  e.dispatchEvent(i);
}
e([he({ attribute: !1 })], Ce.prototype, "hass", void 0),
  e([he()], Ce.prototype, "entryId", void 0),
  e([he({ attribute: !1 })], Ce.prototype, "entries", void 0),
  e([pe()], Ce.prototype, "_devices", void 0),
  e([pe()], Ce.prototype, "_loading", void 0),
  e([pe()], Ce.prototype, "_searchQuery", void 0),
  e([pe()], Ce.prototype, "_error", void 0),
  (Ce = e([_e("hm-device-list")], Ce));
let Ee = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.deviceAddress = ""),
      (this._device = null),
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
      const e = await ge(this.hass, this.entryId);
      this._device = e.find((e) => e.address === this.deviceAddress) ?? null;
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
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
          deviceName: this._device?.name || this.deviceAddress,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _handleShowHistory() {
    this.dispatchEvent(
      new CustomEvent("show-history", {
        detail: { device: this.deviceAddress },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _handleShowLinks() {
    this.dispatchEvent(
      new CustomEvent("show-links", {
        detail: {
          device: this.deviceAddress,
          interfaceId: this.interfaceId,
          deviceName: this._device?.name || this.deviceAddress,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  async _handleExport(e) {
    try {
      const t = await (async function (e, t, i, s, n = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/export_paramset",
            entry_id: t,
            interface_id: i,
            channel_address: s,
            paramset_key: n,
          });
        })(this.hass, this.entryId, this.interfaceId, e.address, "MASTER"),
        i = new Blob([t.json_data], { type: "application/json" }),
        s = URL.createObjectURL(i),
        n = document.createElement("a");
      (n.href = s),
        (n.download = `${e.address.replace(/:/g, "_")}_MASTER.json`),
        n.click(),
        URL.revokeObjectURL(s),
        Se(this, { message: this._l("device_detail.export_success") });
    } catch {
      Se(this, { message: this._l("device_detail.export_failed") });
    }
  }
  async _handleImport(e) {
    const t = document.createElement("input");
    (t.type = "file"),
      (t.accept = ".json"),
      (t.onchange = async () => {
        const i = t.files?.[0];
        if (i)
          try {
            const t = await i.text();
            if (
              !(await Ae(this, {
                title: this._l("device_detail.import_confirm_title"),
                text: this._l("device_detail.import_confirm_text", {
                  channel: e.address,
                }),
                confirmText: this._l("device_detail.import"),
                dismissText: this._l("common.cancel"),
              }))
            )
              return;
            const s = await (async function (e, t, i, s, n, r = "MASTER") {
              return e.callWS({
                type: "homematicip_local/config/import_paramset",
                entry_id: t,
                interface_id: i,
                channel_address: s,
                json_data: n,
                paramset_key: r,
              });
            })(
              this.hass,
              this.entryId,
              this.interfaceId,
              e.address,
              t,
              "MASTER",
            );
            s.success
              ? Se(this, { message: this._l("device_detail.import_success") })
              : Se(this, {
                  message: this._l("device_detail.import_validation_failed"),
                });
          } catch {
            Se(this, { message: this._l("device_detail.import_failed") });
          }
      }),
      t.click();
  }
  render() {
    if (this._loading)
      return B`<div class="loading">${this._l("common.loading")}</div>`;
    if (this._error) return B`<div class="error">${this._error}</div>`;
    if (!this._device)
      return B`<div class="empty-state">${this._l(
        "device_detail.not_found",
      )}</div>`;
    const e = this._device,
      t = e.channels.find((e) => e.address.endsWith(":0")),
      i = e.channels.filter((e) => !e.address.endsWith(":0"));
    return B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="device-header">
        <h2>${e.model} \u2014 ${e.name}</h2>
        <div class="device-info">
          ${this._l("device_detail.address")}: ${e.address} |
          ${this._l("device_detail.firmware")}: ${e.firmware}
        </div>
        <div class="header-actions">
          ${
            ue.has(e.interface)
              ? B`
                <button class="history-button" @click=${this._handleShowLinks}>
                  ${this._l("device_detail.show_links")}
                </button>
              `
              : W
          }
          <button class="history-button" @click=${this._handleShowHistory}>
            ${this._l("device_detail.show_history")}
          </button>
        </div>
      </div>

      ${t ? this._renderMaintenanceChannel(t, e.maintenance) : W}
      ${i.map((e) => this._renderChannel(e))}
    `;
  }
  _renderMaintenanceChannel(e, t) {
    const i = t && Object.keys(t).length > 0,
      s = e.paramset_keys.includes("MASTER");
    return B`
      <div class="channel-card maintenance">
        <div class="channel-header">
          ${this._l("device_detail.channel")} 0: ${e.channel_type}
        </div>
        ${i ? this._renderStatusSummary(t) : W}
        ${
          s
            ? B`
              <div class="channel-actions">
                <button
                  class="configure-button"
                  @click=${() => this._handleChannelClick(e)}
                >
                  ${this._l("device_detail.configure_master")} \u25B8
                </button>
                <button
                  class="configure-button"
                  @click=${() => this._handleExport(e)}
                >
                  ${this._l("device_detail.export")} &#x2B07;
                </button>
                <button
                  class="configure-button"
                  @click=${() => this._handleImport(e)}
                >
                  ${this._l("device_detail.import")} &#x2B06;
                </button>
              </div>
            `
            : W
        }
      </div>
    `;
  }
  _renderStatusSummary(e) {
    const t = [];
    return (
      void 0 !== e.rssi_device &&
        t.push({
          label: "RSSI DEVICE",
          value: `${e.rssi_device} dBm`,
          icon: "📶",
        }),
      void 0 !== e.rssi_peer &&
        t.push({ label: "RSSI PEER", value: `${e.rssi_peer} dBm`, icon: "📶" }),
      void 0 !== e.dutycycle &&
        t.push({ label: "DUTYCYCLE", value: String(e.dutycycle), icon: "⏱" }),
      void 0 !== e.low_bat &&
        t.push({
          label: "LOW BAT",
          value: e.low_bat
            ? this._l("device_detail.yes")
            : this._l("device_detail.no"),
          icon: "🔋",
        }),
      void 0 !== e.unreach &&
        t.push({
          label: "UNREACH",
          value: e.unreach
            ? this._l("device_detail.unreachable")
            : this._l("device_detail.reachable"),
          icon: e.unreach ? "❌" : "✅",
        }),
      void 0 !== e.config_pending &&
        t.push({
          label: "CONFIG PENDING",
          value: e.config_pending
            ? this._l("device_detail.yes")
            : this._l("device_detail.no"),
          icon: "ℹ️",
        }),
      0 === t.length
        ? W
        : B`
      <div class="status-grid">
        ${t.map(
          (e) => B`
            <div class="status-item">
              <span class="status-icon">${e.icon}</span>
              <span>${e.label}: ${e.value}</span>
            </div>
          `,
        )}
      </div>
    `
    );
  }
  _renderChannel(e) {
    const t = e.address.split(":").pop() ?? "",
      i = e.paramset_keys.includes("MASTER");
    return B`
      <div class="channel-card">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${e.channel_type}
        </div>
        ${
          i
            ? B`
              <div class="channel-actions">
                <button
                  class="configure-button"
                  @click=${() => this._handleChannelClick(e)}
                >
                  ${this._l("device_detail.configure_master")} \u25B8
                </button>
                <button
                  class="configure-button"
                  @click=${() => this._handleExport(e)}
                >
                  ${this._l("device_detail.export")} &#x2B07;
                </button>
                <button
                  class="configure-button"
                  @click=${() => this._handleImport(e)}
                >
                  ${this._l("device_detail.import")} &#x2B06;
                </button>
              </div>
            `
            : B`
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
      ve,
      a`
      .device-header {
        margin-bottom: 16px;
      }

      .device-header h2 {
        margin: 8px 0 4px;
        font-size: 20px;
        font-weight: 400;
      }

      .header-actions {
        display: flex;
        gap: 8px;
        margin-top: 8px;
      }

      .history-button {
        background: none;
        border: 1px solid var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        padding: 4px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 13px;
        font-family: inherit;
      }

      .history-button:hover {
        background: var(--primary-color, #03a9f4);
        color: #fff;
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
e([he({ attribute: !1 })], Ee.prototype, "hass", void 0),
  e([he()], Ee.prototype, "entryId", void 0),
  e([he()], Ee.prototype, "interfaceId", void 0),
  e([he()], Ee.prototype, "deviceAddress", void 0),
  e([pe()], Ee.prototype, "_device", void 0),
  e([pe()], Ee.prototype, "_loading", void 0),
  e([pe()], Ee.prototype, "_error", void 0),
  (Ee = e([_e("hm-device-detail")], Ee));
let Ie = class extends oe {
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
    return B`
      <div class="parameter-row ${t ? "read-only" : ""}">
        <div class="parameter-label">
          ${e.label}
          ${e.unit ? B`<span class="parameter-unit">(${e.unit})</span>` : W}
          ${this.modified ? B`<span class="modified-dot"></span>` : W}
        </div>
        <div class="parameter-control">
          ${this._renderWidget(e, t)}
        </div>
      </div>
      ${
        this.validationError
          ? B`<div class="validation-error">${this.validationError}</div>`
          : W
      }
    `;
  }
  _renderWidget(e, t) {
    switch (e.widget) {
      case "toggle":
        return B`
          <label class="toggle">
            <input
              type="checkbox"
              .checked=${Boolean(this.value)}
              ?disabled=${t}
              @change=${(e) => {
                this._emitChange(e.target.checked);
              }}
            />
            <span class="toggle-label">${this.value ? "On" : "Off"}</span>
          </label>
        `;
      case "slider_with_input":
        return B`
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
        return B`
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
        return B`
          <select
            ?disabled=${t}
            @change=${(e) => {
              const t = e.target.selectedIndex;
              this._emitChange(t);
            }}
          >
            ${(e.options ?? []).map(
              (e, t) => B`
                <option value=${t} ?selected=${this.value === t}>${e}</option>
              `,
            )}
          </select>
        `;
      case "radio_group":
        return B`
          <div class="radio-group">
            ${(e.options ?? []).map(
              (i, s) => B`
                <label class="radio-item">
                  <input
                    type="radio"
                    name=${e.id}
                    .checked=${this.value === s}
                    ?disabled=${t}
                    @change=${() => this._emitChange(s)}
                  />
                  ${i}
                </label>
              `,
            )}
          </div>
        `;
      case "text_input":
        return B`
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
        return B`
          <button
            class="action-button"
            ?disabled=${t}
            @click=${() => this._emitChange(!0)}
          >
            ${e.label}
          </button>
        `;
      default:
        return B`<span class="read-only-value">${String(
          this.value ?? "",
        )}</span>`;
    }
  }
  static {
    this.styles = [
      ve,
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
e([he({ attribute: !1 })], Ie.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Ie.prototype, "parameter", void 0),
  e([he()], Ie.prototype, "value", void 0),
  e([he({ type: Boolean })], Ie.prototype, "modified", void 0),
  e([he()], Ie.prototype, "validationError", void 0),
  (Ie = e([_e("hm-form-parameter")], Ie));
let Te = class extends oe {
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
      ? B`
      ${this.schema.sections.map(
        (e) => B`
          <div class="form-section">
            <div class="section-header">${e.title}</div>
            ${e.parameters.map(
              (e) => B`
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
      ve,
      a`
      .form-section {
        margin-bottom: 16px;
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Te.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Te.prototype, "schema", void 0),
  e([he({ attribute: !1 })], Te.prototype, "pendingChanges", void 0),
  e([he({ attribute: !1 })], Te.prototype, "validationErrors", void 0),
  (Te = e([_e("hm-config-form")], Te));
let Re = class extends oe {
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
      (this._validationErrors = {}),
      (this._sessionActive = !1),
      (this._canUndo = !1),
      (this._canRedo = !1);
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
      (this._validationErrors = {}),
      (this._canUndo = !1),
      (this._canRedo = !1);
    try {
      (this._schema = await fe(
        this.hass,
        this.entryId,
        this.interfaceId,
        this.channelAddress,
        this.channelType,
        this.paramsetKey,
      )),
        await me(
          this.hass,
          this.entryId,
          this.interfaceId,
          this.channelAddress,
          this.paramsetKey,
        ),
        (this._sessionActive = !0);
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
  }
  get _isDirty() {
    return this._pendingChanges.size > 0;
  }
  async _handleValueChanged(e) {
    const { parameterId: t, value: i, currentValue: s } = e.detail;
    if (
      (i === s
        ? this._pendingChanges.delete(t)
        : this._pendingChanges.set(t, i),
      (this._pendingChanges = new Map(this._pendingChanges)),
      this._sessionActive)
    )
      try {
        const e = await (async function (e, t, i, s, n, r = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/session_set",
            entry_id: t,
            channel_address: i,
            parameter: s,
            value: n,
            paramset_key: r,
          });
        })(
          this.hass,
          this.entryId,
          this.channelAddress,
          t,
          i,
          this.paramsetKey,
        );
        (this._canUndo = e.can_undo),
          (this._canRedo = e.can_redo),
          (this._validationErrors = e.validation_errors);
      } catch {}
  }
  async _handleUndo() {
    if (this._sessionActive)
      try {
        const e = await (async function (e, t, i, s = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/session_undo",
            entry_id: t,
            channel_address: i,
            paramset_key: s,
          });
        })(this.hass, this.entryId, this.channelAddress, this.paramsetKey);
        (this._canUndo = e.can_undo),
          (this._canRedo = e.can_redo),
          e.performed && (await this._refreshSchemaValues());
      } catch (e) {
        this._error = String(e);
      }
  }
  async _handleRedo() {
    if (this._sessionActive)
      try {
        const e = await (async function (e, t, i, s = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/session_redo",
            entry_id: t,
            channel_address: i,
            paramset_key: s,
          });
        })(this.hass, this.entryId, this.channelAddress, this.paramsetKey);
        (this._canUndo = e.can_undo),
          (this._canRedo = e.can_redo),
          e.performed && (await this._refreshSchemaValues());
      } catch (e) {
        this._error = String(e);
      }
  }
  async _refreshSchemaValues() {
    try {
      (this._schema = await fe(
        this.hass,
        this.entryId,
        this.interfaceId,
        this.channelAddress,
        this.channelType,
        this.paramsetKey,
      )),
        (this._pendingChanges = new Map());
    } catch (e) {
      this._error = String(e);
    }
  }
  _handleDiscard() {
    (this._pendingChanges = new Map()),
      (this._validationErrors = {}),
      this._sessionActive &&
        ye(this.hass, this.entryId, this.channelAddress, this.paramsetKey)
          .then(
            () => (
              (this._canUndo = !1),
              (this._canRedo = !1),
              me(
                this.hass,
                this.entryId,
                this.interfaceId,
                this.channelAddress,
                this.paramsetKey,
              )
            ),
          )
          .catch(() => {});
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
    const e = this._pendingChanges.size,
      t = [...this._pendingChanges.entries()]
        .map(([e, t]) => {
          const i = this._findParameter(e);
          return `${i?.label ?? e}: ${i?.current_value ?? "?"} → ${t}`;
        })
        .join("\n");
    if (
      await Ae(this, {
        title: this._l("channel_config.confirm_save_title"),
        text: `${this._l("channel_config.confirm_save_text", {
          count: e,
        })}\n\n${t}`,
        confirmText: this._l("common.save"),
        dismissText: this._l("common.cancel"),
      })
    ) {
      (this._saving = !0), (this._validationErrors = {});
      try {
        if (this._sessionActive) {
          const e = await (async function (e, t, i, s, n = "MASTER") {
            return e.callWS({
              type: "homematicip_local/config/session_save",
              entry_id: t,
              interface_id: i,
              channel_address: s,
              paramset_key: n,
            });
          })(
            this.hass,
            this.entryId,
            this.interfaceId,
            this.channelAddress,
            this.paramsetKey,
          );
          e.success
            ? ((this._pendingChanges = new Map()),
              (this._sessionActive = !1),
              Se(this, { message: this._l("channel_config.save_success") }),
              await this._fetchSchema())
            : Object.keys(e.validation_errors).length > 0 &&
              ((this._validationErrors = e.validation_errors),
              Se(this, {
                message: this._l("channel_config.validation_failed"),
              }));
        } else {
          const e = Object.fromEntries(this._pendingChanges),
            t = await (async function (e, t, i, s, n, r = "MASTER", a = !0) {
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
              Se(this, { message: this._l("channel_config.save_success") }),
              await this._fetchSchema())
            : Object.keys(t.validation_errors).length > 0 &&
              ((this._validationErrors = t.validation_errors),
              Se(this, {
                message: this._l("channel_config.validation_failed"),
              }));
        }
      } catch (e) {
        (this._error = String(e)),
          Se(this, { message: this._l("channel_config.save_failed") });
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
        !(await Ae(this, {
          title: this._l("channel_config.unsaved_title"),
          text: this._l("channel_config.unsaved_warning"),
          confirmText: this._l("channel_config.discard"),
          dismissText: this._l("common.cancel"),
          destructive: !0,
        }))
      )
        return;
    }
    if (this._sessionActive) {
      try {
        await ye(
          this.hass,
          this.entryId,
          this.channelAddress,
          this.paramsetKey,
        );
      } catch {}
      this._sessionActive = !1;
    }
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  render() {
    return this._loading
      ? B`<div class="loading">${this._l("common.loading")}</div>`
      : this._error && !this._schema
        ? B`<div class="error">${this._error}</div>`
        : B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="config-header">
        ${this.deviceName ? B`<h2>${this.deviceName}</h2>` : W}
        <div class="device-info">
          ${this.channelAddress} \u2014 ${
            this._schema?.channel_type ?? ""
          } \u2014 ${this.paramsetKey}
        </div>
      </div>

      ${this._error ? B`<div class="error">${this._error}</div>` : W}

      ${
        this._schema
          ? B`
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

      <div class="action-bar-split">
        <div class="action-bar-left">
          <button
            class="btn btn-icon"
            @click=${this._handleUndo}
            ?disabled=${!this._canUndo || this._saving}
            title="${this._l("channel_config.undo")}"
          >
            &#x21A9;
          </button>
          <button
            class="btn btn-icon"
            @click=${this._handleRedo}
            ?disabled=${!this._canRedo || this._saving}
            title="${this._l("channel_config.redo")}"
          >
            &#x21AA;
          </button>
        </div>
        <div class="action-bar-right">
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
      </div>
    `;
  }
  static {
    this.styles = [
      ve,
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

      .btn-icon {
        background: none;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        padding: 6px 10px;
        cursor: pointer;
        font-size: 16px;
        color: var(--primary-text-color);
      }

      .btn-icon:disabled {
        opacity: 0.3;
        cursor: not-allowed;
      }

      .btn-icon:hover:not(:disabled) {
        background: var(--secondary-background-color, #f5f5f5);
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

        .action-bar-right button {
          width: 100%;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Re.prototype, "hass", void 0),
  e([he()], Re.prototype, "entryId", void 0),
  e([he()], Re.prototype, "interfaceId", void 0),
  e([he()], Re.prototype, "channelAddress", void 0),
  e([he()], Re.prototype, "channelType", void 0),
  e([he()], Re.prototype, "paramsetKey", void 0),
  e([he()], Re.prototype, "deviceName", void 0),
  e([pe()], Re.prototype, "_schema", void 0),
  e([pe()], Re.prototype, "_pendingChanges", void 0),
  e([pe()], Re.prototype, "_loading", void 0),
  e([pe()], Re.prototype, "_saving", void 0),
  e([pe()], Re.prototype, "_error", void 0),
  e([pe()], Re.prototype, "_validationErrors", void 0),
  e([pe()], Re.prototype, "_sessionActive", void 0),
  e([pe()], Re.prototype, "_canUndo", void 0),
  e([pe()], Re.prototype, "_canRedo", void 0),
  (Re = e([_e("hm-channel-config")], Re));
let ze = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.filterDevice = ""),
      (this._entries = []),
      (this._total = 0),
      (this._loading = !0),
      (this._error = ""),
      (this._expandedEntries = new Set());
  }
  updated(e) {
    (e.has("entryId") || e.has("filterDevice")) &&
      this.entryId &&
      this._fetchHistory();
  }
  async _fetchHistory() {
    (this._loading = !0), (this._error = "");
    try {
      const e = await (async function (e, t, i = "", s = 50) {
        return e.callWS({
          type: "homematicip_local/config/get_change_history",
          entry_id: t,
          channel_address: i,
          limit: s,
        });
      })(this.hass, this.entryId, this.filterDevice);
      (this._entries = e.entries), (this._total = e.total);
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
  }
  _handleBack() {
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  _toggleEntry(e) {
    const t = new Set(this._expandedEntries);
    t.has(e) ? t.delete(e) : t.add(e), (this._expandedEntries = t);
  }
  async _handleClear() {
    if (
      await Ae(this, {
        title: this._l("change_history.clear_confirm_title"),
        text: this._l("change_history.clear_confirm_text"),
        confirmText: this._l("change_history.clear"),
        dismissText: this._l("common.cancel"),
        destructive: !0,
      })
    )
      try {
        const e = await (async function (e, t) {
          return e.callWS({
            type: "homematicip_local/config/clear_change_history",
            entry_id: t,
          });
        })(this.hass, this.entryId);
        e.success &&
          (Se(this, {
            message: this._l("change_history.clear_success", {
              count: e.cleared,
            }),
          }),
          (this._entries = []),
          (this._total = 0));
      } catch {
        Se(this, { message: this._l("channel_config.save_failed") });
      }
  }
  _formatTimestamp(e) {
    try {
      return new Date(e).toLocaleString(this.hass.config.language || "en");
    } catch {
      return e;
    }
  }
  _getSourceLabel(e) {
    switch (e) {
      case "manual":
        return this._l("change_history.source_manual");
      case "import":
        return this._l("change_history.source_import");
      case "copy":
        return this._l("change_history.source_copy");
      default:
        return e;
    }
  }
  render() {
    return B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="history-header-bar">
        <h2>${this._l("change_history.title")}</h2>
      </div>

      ${
        this._loading
          ? B`<div class="loading">${this._l("common.loading")}</div>`
          : this._error
            ? B`<div class="error">${this._error}</div>`
            : 0 === this._entries.length
              ? B`<div class="empty-state">${this._l(
                  "change_history.empty",
                )}</div>`
              : this._renderEntries()
      }

      ${
        !this._loading && this._entries.length > 0
          ? B`
            <div class="action-bar">
              <button class="btn btn-secondary destructive" @click=${
                this._handleClear
              }>
                ${this._l("change_history.clear")}
              </button>
            </div>
          `
          : W
      }
    `;
  }
  _renderEntries() {
    return B`
      <div class="history-list">
        ${this._entries.map((e, t) => {
          const i = `${e.timestamp}-${t}`,
            s = this._expandedEntries.has(i),
            n = Object.keys(e.changes).length;
          return B`
            <div class="history-entry">
              <div
                class="history-entry-header"
                @click=${() => this._toggleEntry(i)}
              >
                <div class="history-entry-info">
                  <div class="history-entry-time">
                    ${this._formatTimestamp(e.timestamp)}
                  </div>
                  <div class="history-entry-device">
                    ${e.device_name} (${e.device_model})
                    \u2014 ${e.channel_address}
                  </div>
                  <div class="history-entry-meta">
                    ${this._l("change_history.parameters_changed", {
                      count: n,
                    })}
                  </div>
                </div>
                <div class="history-entry-badges">
                  <span class="source-badge">${this._getSourceLabel(
                    e.source,
                  )}</span>
                  <span class="expand-icon">${s ? "▾" : "▸"}</span>
                </div>
              </div>
              ${
                s
                  ? B`
                    <div class="history-details">
                      ${Object.entries(e.changes).map(
                        ([e, t]) => B`
                          <div class="change-row">
                            <span class="change-param">${e}</span>
                            <span class="change-values">
                              <span class="change-old">${String(t.old)}</span>
                              \u2192
                              <span class="change-new">${String(t.new)}</span>
                            </span>
                          </div>
                        `,
                      )}
                    </div>
                  `
                  : W
              }
            </div>
          `;
        })}
      </div>
    `;
  }
  static {
    this.styles = [
      ve,
      a`
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
        font-size: 16px;
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

      .btn {
        padding: 8px 20px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
        border: 1px solid transparent;
      }

      .btn-secondary {
        background: transparent;
        color: var(--primary-text-color);
        border-color: var(--divider-color, #e0e0e0);
      }

      .btn-secondary:hover {
        background: var(--secondary-background-color, #f5f5f5);
      }

      .btn-secondary.destructive {
        color: var(--error-color, #db4437);
        border-color: var(--error-color, #db4437);
      }

      .btn-secondary.destructive:hover {
        background: var(--error-color, #db4437);
        color: #fff;
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
    `,
    ];
  }
};
e([he({ attribute: !1 })], ze.prototype, "hass", void 0),
  e([he()], ze.prototype, "entryId", void 0),
  e([he()], ze.prototype, "filterDevice", void 0),
  e([pe()], ze.prototype, "_entries", void 0),
  e([pe()], ze.prototype, "_total", void 0),
  e([pe()], ze.prototype, "_loading", void 0),
  e([pe()], ze.prototype, "_error", void 0),
  e([pe()], ze.prototype, "_expandedEntries", void 0),
  (ze = e([_e("hm-change-history")], ze));
let De = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.deviceAddress = ""),
      (this.deviceName = ""),
      (this._links = []),
      (this._loading = !0),
      (this._error = "");
  }
  updated(e) {
    (e.has("entryId") || e.has("deviceAddress") || e.has("interfaceId")) &&
      this.entryId &&
      this.deviceAddress &&
      this.interfaceId &&
      this._fetchLinks();
  }
  async _fetchLinks() {
    (this._loading = !0), (this._error = "");
    try {
      this._links = await (async function (e, t, i, s) {
        return (
          await e.callWS({
            type: "homematicip_local/config/list_device_links",
            entry_id: t,
            interface_id: i,
            device_address: s,
          })
        ).links;
      })(this.hass, this.entryId, this.interfaceId, this.deviceAddress);
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
  }
  _handleBack() {
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  _handleAddLink() {
    this.dispatchEvent(
      new CustomEvent("add-link", {
        detail: {
          deviceAddress: this.deviceAddress,
          interfaceId: this.interfaceId,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _handleConfigure(e) {
    this.dispatchEvent(
      new CustomEvent("configure-link", {
        detail: {
          senderAddress: e.sender_address,
          receiverAddress: e.receiver_address,
          interfaceId: this.interfaceId,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  async _handleDelete(e) {
    if (
      await Ae(this, {
        title: this._l("device_links.delete_confirm_title"),
        text: this._l("device_links.delete_confirm_text", {
          sender: e.sender_address,
          receiver: e.receiver_address,
        }),
        confirmText: this._l("device_links.delete"),
        dismissText: this._l("common.cancel"),
        destructive: !0,
      })
    )
      try {
        await (async function (e, t, i, s) {
          return e.callWS({
            type: "homematicip_local/config/remove_link",
            entry_id: t,
            sender_channel_address: i,
            receiver_channel_address: s,
          });
        })(this.hass, this.entryId, e.sender_address, e.receiver_address),
          Se(this, { message: this._l("device_links.delete_success") }),
          await this._fetchLinks();
      } catch {
        Se(this, { message: this._l("device_links.delete_failed") });
      }
  }
  _groupByChannel() {
    const e = new Map();
    for (const t of this._links) {
      const i =
        (t.sender_address.startsWith(this.deviceAddress)
          ? t.sender_address
          : t.receiver_address
        )
          .split(":")
          .pop() ?? "";
      e.has(i) || e.set(i, []), e.get(i).push(t);
    }
    return e;
  }
  render() {
    return B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="links-header">
        <h2>${this._l("device_links.title")}</h2>
        <div class="device-info">
          ${this._l("device_links.subtitle", {
            device: this.deviceName || this.deviceAddress,
          })}
        </div>
      </div>

      <button class="btn btn-primary add-link-btn" @click=${
        this._handleAddLink
      }>
        + ${this._l("device_links.add_link")}
      </button>

      ${
        this._loading
          ? B`<div class="loading">${this._l("common.loading")}</div>`
          : this._error
            ? B`<div class="error">${this._error}</div>`
            : 0 === this._links.length
              ? B`<div class="empty-state">${this._l(
                  "device_links.empty",
                )}</div>`
              : this._renderGroupedLinks()
      }
    `;
  }
  _renderGroupedLinks() {
    const e = this._groupByChannel(),
      t = [...e.keys()].sort((e, t) => parseInt(e) - parseInt(t));
    return B`
      ${t.map((t) => {
        const i = e.get(t);
        return B`
          <div class="link-channel-group">
            <div class="link-channel-header">
              ${this._l("device_links.channel_group", { channel: t })}
            </div>
            ${i.map((e) => this._renderLinkCard(e))}
          </div>
        `;
      })}
    `;
  }
  _renderLinkCard(e) {
    const t = "outgoing" === e.direction;
    return B`
      <div class="link-card ${t ? "outgoing" : "incoming"}">
        <div class="link-direction">
          <span class="direction-badge ${e.direction}">
            ${
              t
                ? this._l("device_links.outgoing")
                : this._l("device_links.incoming")
            }
          </span>
        </div>
        <div class="link-info">
          <div class="link-addresses">
            <span class="link-sender">${e.sender_address}</span>
            <span class="link-arrow">\u2192</span>
            <span class="link-receiver">${e.receiver_address}</span>
          </div>
          <div class="link-devices">
            ${e.sender_device_name} (${e.sender_device_model})
            \u2192
            ${e.receiver_device_name} (${e.receiver_device_model})
          </div>
          ${e.name ? B`<div class="link-name">"${e.name}"</div>` : W}
        </div>
        <div class="link-actions">
          <button
            class="configure-button"
            @click=${() => this._handleConfigure(e)}
          >
            ${this._l("device_links.configure")}
          </button>
          <button
            class="configure-button destructive"
            @click=${() => this._handleDelete(e)}
          >
            ${this._l("device_links.delete")}
          </button>
        </div>
      </div>
    `;
  }
  static {
    this.styles = [
      ve,
      a`
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

      .btn {
        padding: 8px 20px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
        border: 1px solid transparent;
      }

      .btn-primary {
        background: var(--primary-color, #03a9f4);
        color: #fff;
        border-color: var(--primary-color, #03a9f4);
      }

      .btn-primary:hover {
        opacity: 0.9;
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

      .link-addresses {
        font-family: monospace;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 8px 0 4px;
      }

      .link-arrow {
        color: var(--secondary-text-color);
      }

      .link-devices {
        font-size: 13px;
        color: var(--secondary-text-color);
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

      .configure-button.destructive {
        border-color: var(--error-color, #db4437);
        color: var(--error-color, #db4437);
      }

      .configure-button.destructive:hover {
        background: var(--error-color, #db4437);
        color: #fff;
      }

      @media (max-width: 600px) {
        .link-addresses {
          flex-direction: column;
          align-items: flex-start;
          gap: 2px;
        }

        .link-arrow {
          display: none;
        }

        .link-actions {
          flex-direction: column;
        }

        .configure-button {
          width: 100%;
          text-align: center;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], De.prototype, "hass", void 0),
  e([he()], De.prototype, "entryId", void 0),
  e([he()], De.prototype, "interfaceId", void 0),
  e([he()], De.prototype, "deviceAddress", void 0),
  e([he()], De.prototype, "deviceName", void 0),
  e([pe()], De.prototype, "_links", void 0),
  e([pe()], De.prototype, "_loading", void 0),
  e([pe()], De.prototype, "_error", void 0),
  (De = e([_e("hm-device-links")], De));
let Pe = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.senderAddress = ""),
      (this.receiverAddress = ""),
      (this._schema = null),
      (this._pendingChanges = new Map()),
      (this._loading = !0),
      (this._saving = !1),
      (this._error = ""),
      (this._validationErrors = {});
  }
  updated(e) {
    (e.has("senderAddress") || e.has("receiverAddress") || e.has("entryId")) &&
      this.entryId &&
      this.senderAddress &&
      this.receiverAddress &&
      this._fetchSchema();
  }
  async _fetchSchema() {
    (this._loading = !0),
      (this._error = ""),
      (this._pendingChanges = new Map()),
      (this._validationErrors = {});
    try {
      this._schema = await (async function (e, t, i, s, n) {
        return e.callWS({
          type: "homematicip_local/config/get_link_form_schema",
          entry_id: t,
          interface_id: i,
          sender_channel_address: s,
          receiver_channel_address: n,
        });
      })(
        this.hass,
        this.entryId,
        this.interfaceId,
        this.senderAddress,
        this.receiverAddress,
      );
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
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
  async _handleSave() {
    if (!this._isDirty || this._saving) return;
    const e = this._pendingChanges.size,
      t = [...this._pendingChanges.entries()]
        .map(([e, t]) => {
          const i = this._findParameter(e);
          return `${i?.label ?? e}: ${i?.current_value ?? "?"} → ${t}`;
        })
        .join("\n");
    if (
      await Ae(this, {
        title: this._l("link_config.confirm_save_title"),
        text: `${this._l("link_config.confirm_save_text", {
          count: e,
        })}\n\n${t}`,
        confirmText: this._l("common.save"),
        dismissText: this._l("common.cancel"),
      })
    ) {
      (this._saving = !0), (this._validationErrors = {});
      try {
        (
          await (async function (e, t, i, s, n, r) {
            return e.callWS({
              type: "homematicip_local/config/put_link_paramset",
              entry_id: t,
              interface_id: i,
              sender_channel_address: s,
              receiver_channel_address: n,
              values: r,
            });
          })(
            this.hass,
            this.entryId,
            this.interfaceId,
            this.senderAddress,
            this.receiverAddress,
            Object.fromEntries(this._pendingChanges),
          )
        ).success &&
          ((this._pendingChanges = new Map()),
          Se(this, { message: this._l("link_config.save_success") }),
          await this._fetchSchema());
      } catch (e) {
        (this._error = String(e)),
          Se(this, { message: this._l("link_config.save_failed") });
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
        !(await Ae(this, {
          title: this._l("link_config.unsaved_title"),
          text: this._l("link_config.unsaved_warning"),
          confirmText: this._l("link_config.discard"),
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
      ? B`<div class="loading">${this._l("common.loading")}</div>`
      : this._error && !this._schema
        ? B`<div class="error">${this._error}</div>`
        : B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${this._l("common.back")}
      </button>

      <div class="config-header">
        <h2>${this._l("link_config.title")}</h2>
        <div class="link-info-bar">
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.sender")}</span>
            <span class="link-address">${this.senderAddress}</span>
          </div>
          <span class="link-direction-arrow">\u2192</span>
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.receiver")}</span>
            <span class="link-address">${this.receiverAddress}</span>
          </div>
        </div>
      </div>

      ${this._error ? B`<div class="error">${this._error}</div>` : W}

      ${
        this._schema
          ? B`
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
          @click=${this._handleDiscard}
          ?disabled=${!this._isDirty || this._saving}
        >
          ${this._l("link_config.discard")}
        </button>
        <button
          class="btn btn-primary"
          @click=${this._handleSave}
          ?disabled=${!this._isDirty || this._saving}
        >
          ${
            this._saving
              ? this._l("channel_config.saving")
              : this._l("common.save")
          }
        </button>
      </div>
    `;
  }
  static {
    this.styles = [
      ve,
      a`
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

      .link-address {
        font-family: monospace;
        font-size: 14px;
      }

      .link-direction-arrow {
        font-size: 20px;
        color: var(--primary-color, #03a9f4);
        flex-shrink: 0;
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

      @media (max-width: 600px) {
        .link-info-bar {
          flex-direction: column;
          align-items: flex-start;
          gap: 8px;
        }

        .link-direction-arrow {
          align-self: center;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Pe.prototype, "hass", void 0),
  e([he()], Pe.prototype, "entryId", void 0),
  e([he()], Pe.prototype, "interfaceId", void 0),
  e([he()], Pe.prototype, "senderAddress", void 0),
  e([he()], Pe.prototype, "receiverAddress", void 0),
  e([pe()], Pe.prototype, "_schema", void 0),
  e([pe()], Pe.prototype, "_pendingChanges", void 0),
  e([pe()], Pe.prototype, "_loading", void 0),
  e([pe()], Pe.prototype, "_saving", void 0),
  e([pe()], Pe.prototype, "_error", void 0),
  e([pe()], Pe.prototype, "_validationErrors", void 0),
  (Pe = e([_e("hm-link-config")], Pe));
let Me = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.deviceAddress = ""),
      (this._step = "select-channel"),
      (this._device = null),
      (this._selectedChannel = ""),
      (this._selectedRole = "sender"),
      (this._selectedPeer = ""),
      (this._linkName = ""),
      (this._linkableChannels = []),
      (this._filteredChannels = []),
      (this._searchQuery = ""),
      (this._loading = !1),
      (this._error = "");
  }
  updated(e) {
    (e.has("entryId") || e.has("deviceAddress")) &&
      this.entryId &&
      this.deviceAddress &&
      this._fetchDevice();
  }
  async _fetchDevice() {
    this._loading = !0;
    try {
      const e = await ge(this.hass, this.entryId);
      this._device = e.find((e) => e.address === this.deviceAddress) ?? null;
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return we(this.hass, e, t);
  }
  _handleBack() {
    if ("select-peer" === this._step)
      return (
        (this._step = "select-channel"),
        (this._selectedPeer = ""),
        (this._linkableChannels = []),
        (this._filteredChannels = []),
        void (this._searchQuery = "")
      );
    "confirm" !== this._step
      ? this.dispatchEvent(
          new CustomEvent("back", { bubbles: !0, composed: !0 }),
        )
      : (this._step = "select-peer");
  }
  _getLinkableChannels() {
    return this._device
      ? this._device.channels.filter(
          (e) => !e.address.endsWith(":0") && e.paramset_keys.includes("LINK"),
        )
      : [];
  }
  _handleSelectChannel(e) {
    this._selectedChannel = e;
  }
  async _handleNextToSelectPeer() {
    this._selectedChannel &&
      ((this._step = "select-peer"), await this._fetchLinkableChannels());
  }
  async _fetchLinkableChannels() {
    (this._loading = !0),
      (this._error = ""),
      (this._linkableChannels = []),
      (this._filteredChannels = []),
      (this._searchQuery = "");
    try {
      (this._linkableChannels = await (async function (e, t, i, s, n) {
        return (
          await e.callWS({
            type: "homematicip_local/config/get_linkable_channels",
            entry_id: t,
            interface_id: i,
            channel_address: s,
            role: n,
          })
        ).channels;
      })(
        this.hass,
        this.entryId,
        this.interfaceId,
        this._selectedChannel,
        this._selectedRole,
      )),
        (this._filteredChannels = this._linkableChannels);
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  async _handleRoleChange(e) {
    (this._selectedRole = e),
      (this._selectedPeer = ""),
      await this._fetchLinkableChannels();
  }
  _handleSearchInput(e) {
    const t = e.target.value.toLowerCase();
    (this._searchQuery = t),
      (this._filteredChannels = t
        ? this._linkableChannels.filter(
            (e) =>
              e.address.toLowerCase().includes(t) ||
              e.device_name.toLowerCase().includes(t) ||
              e.device_model.toLowerCase().includes(t) ||
              e.channel_type.toLowerCase().includes(t),
          )
        : this._linkableChannels);
  }
  _handleSelectPeer(e) {
    this._selectedPeer = e;
  }
  _handleNextToConfirm() {
    this._selectedPeer && ((this._linkName = ""), (this._step = "confirm"));
  }
  async _handleCreate() {
    this._loading = !0;
    try {
      const e =
          "sender" === this._selectedRole
            ? this._selectedChannel
            : this._selectedPeer,
        t =
          "sender" === this._selectedRole
            ? this._selectedPeer
            : this._selectedChannel;
      await (async function (e, t, i, s, n, r) {
        return e.callWS({
          type: "homematicip_local/config/add_link",
          entry_id: t,
          sender_channel_address: i,
          receiver_channel_address: s,
          ...(n && { name: n }),
          ...r,
        });
      })(this.hass, this.entryId, e, t, this._linkName || void 0),
        Se(this, { message: this._l("add_link.create_success") }),
        this.dispatchEvent(
          new CustomEvent("link-created", { bubbles: !0, composed: !0 }),
        );
    } catch {
      Se(this, { message: this._l("add_link.create_failed") });
    } finally {
      this._loading = !1;
    }
  }
  render() {
    return this._loading && !this._device
      ? B`<div class="loading">${this._l("common.loading")}</div>`
      : B`
      <button class="back-button" @click=${this._handleBack}>
        \u25C2 ${
          "select-channel" === this._step
            ? this._l("common.back")
            : this._l("add_link.back")
        }
      </button>

      <div class="wizard-header">
        <h2>${this._l("add_link.title")}</h2>
      </div>

      ${this._error ? B`<div class="error">${this._error}</div>` : W}

      ${
        "select-channel" === this._step
          ? this._renderStepChannel()
          : "select-peer" === this._step
            ? this._renderStepPeer()
            : this._renderStepConfirm()
      }
    `;
  }
  _renderStepChannel() {
    const e = this._getLinkableChannels();
    return B`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_channel")}</div>
        <div class="step-description">
          ${this._l("add_link.select_channel")}
        </div>

        <div class="radio-list">
          ${
            0 === e.length
              ? B`<div class="empty-state">${this._l(
                  "add_link.no_compatible",
                )}</div>`
              : e.map((e) => {
                  const t = e.address.split(":").pop() ?? "",
                    i = this._selectedChannel === e.address;
                  return B`
                  <div
                    class="radio-option ${i ? "selected" : ""}"
                    @click=${() => this._handleSelectChannel(e.address)}
                  >
                    <input
                      type="radio"
                      name="channel"
                      .checked=${i}
                    />
                    <div class="radio-content">
                      <div class="radio-title">
                        ${this._l("device_detail.channel")} ${t}: ${
                          e.channel_type
                        }
                      </div>
                      <div class="radio-subtitle">${e.address}</div>
                    </div>
                  </div>
                `;
                })
          }
        </div>

        ${
          e.length > 0
            ? B`
              <div class="wizard-actions">
                <button
                  class="btn btn-primary"
                  ?disabled=${!this._selectedChannel}
                  @click=${this._handleNextToSelectPeer}
                >
                  ${this._l("add_link.next")} \u25B8
                </button>
              </div>
            `
            : W
        }
      </div>
    `;
  }
  _renderStepPeer() {
    return B`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_peer")}</div>

        <div class="role-selector">
          <span class="role-label">${this._l("add_link.select_role")}</span>
          <div class="role-buttons">
            <button
              class="role-btn ${
                "sender" === this._selectedRole ? "active" : ""
              }"
              @click=${() => this._handleRoleChange("sender")}
            >
              ${this._l("add_link.role_sender")}
            </button>
            <button
              class="role-btn ${
                "receiver" === this._selectedRole ? "active" : ""
              }"
              @click=${() => this._handleRoleChange("receiver")}
            >
              ${this._l("add_link.role_receiver")}
            </button>
          </div>
        </div>

        ${
          this._loading
            ? B`<div class="loading">${this._l("common.loading")}</div>`
            : B`
              <div class="search-box">
                <input
                  type="text"
                  .value=${this._searchQuery}
                  @input=${this._handleSearchInput}
                  placeholder="${this._l("add_link.search_devices")}"
                />
              </div>

              <div class="radio-list">
                ${
                  0 === this._filteredChannels.length
                    ? B`<div class="empty-state">${this._l(
                        "add_link.no_compatible",
                      )}</div>`
                    : this._filteredChannels.map((e) => {
                        const t = this._selectedPeer === e.address;
                        return B`
                        <div
                          class="radio-option ${t ? "selected" : ""}"
                          @click=${() => this._handleSelectPeer(e.address)}
                        >
                          <input
                            type="radio"
                            name="peer"
                            .checked=${t}
                          />
                          <div class="radio-content">
                            <div class="radio-title">
                              ${e.device_name} (${e.device_model})
                            </div>
                            <div class="radio-subtitle">
                              ${e.address} \u2014 ${e.channel_type}
                            </div>
                          </div>
                        </div>
                      `;
                      })
                }
              </div>

              ${
                this._filteredChannels.length > 0
                  ? B`
                    <div class="wizard-actions">
                      <button
                        class="btn btn-primary"
                        ?disabled=${!this._selectedPeer}
                        @click=${this._handleNextToConfirm}
                      >
                        ${this._l("add_link.next")} \u25B8
                      </button>
                    </div>
                  `
                  : W
              }
            `
        }
      </div>
    `;
  }
  _renderStepConfirm() {
    const e =
        "sender" === this._selectedRole
          ? this._selectedChannel
          : this._selectedPeer,
      t =
        "sender" === this._selectedRole
          ? this._selectedPeer
          : this._selectedChannel,
      i = this._resolveName(e),
      s = this._resolveName(t);
    return B`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_confirm")}</div>

        <div class="link-summary">
          <div class="link-endpoint">
            <div class="link-endpoint-label">
              ${this._l("link_config.sender")}
            </div>
            <div class="link-endpoint-address">${e}</div>
            <div class="link-endpoint-name">${i}</div>
          </div>

          <div class="link-direction-arrow">\u2192</div>

          <div class="link-endpoint">
            <div class="link-endpoint-label">
              ${this._l("link_config.receiver")}
            </div>
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
            @input=${(e) => {
              this._linkName = e.target.value;
            }}
            placeholder="${e} -> ${t}"
          />
        </div>

        <div class="wizard-actions">
          <button
            class="btn btn-primary"
            ?disabled=${this._loading}
            @click=${this._handleCreate}
          >
            ${
              this._loading
                ? this._l("common.loading")
                : this._l("add_link.create")
            }
          </button>
        </div>
      </div>
    `;
  }
  _resolveName(e) {
    if (!this._device) return e;
    if (e.startsWith(this.deviceAddress))
      return this._device.name || this.deviceAddress;
    const t = this._linkableChannels.find((t) => t.address === e);
    return t ? `${t.device_name} (${t.device_model})` : e;
  }
  static {
    this.styles = [
      ve,
      a`
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

      .role-btn {
        flex: 1;
        padding: 8px 16px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        background: transparent;
        cursor: pointer;
        font-size: 13px;
        font-family: inherit;
        color: var(--primary-text-color);
        transition: all 0.15s;
      }

      .role-btn:hover {
        border-color: var(--primary-color, #03a9f4);
      }

      .role-btn.active {
        border-color: var(--primary-color, #03a9f4);
        background: var(--primary-color, #03a9f4);
        color: #fff;
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

      .radio-option input[type="radio"] {
        margin-right: 12px;
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
        font-size: 24px;
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

      @media (max-width: 600px) {
        .role-buttons {
          flex-direction: column;
        }

        .link-summary {
          padding: 16px;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Me.prototype, "hass", void 0),
  e([he()], Me.prototype, "entryId", void 0),
  e([he()], Me.prototype, "interfaceId", void 0),
  e([he()], Me.prototype, "deviceAddress", void 0),
  e([pe()], Me.prototype, "_step", void 0),
  e([pe()], Me.prototype, "_device", void 0),
  e([pe()], Me.prototype, "_selectedChannel", void 0),
  e([pe()], Me.prototype, "_selectedRole", void 0),
  e([pe()], Me.prototype, "_selectedPeer", void 0),
  e([pe()], Me.prototype, "_linkName", void 0),
  e([pe()], Me.prototype, "_linkableChannels", void 0),
  e([pe()], Me.prototype, "_filteredChannels", void 0),
  e([pe()], Me.prototype, "_searchQuery", void 0),
  e([pe()], Me.prototype, "_loading", void 0),
  e([pe()], Me.prototype, "_error", void 0),
  (Me = e([_e("hm-add-link")], Me));
let Ne = class extends oe {
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
      (this._selectedDeviceName = ""),
      (this._selectedSenderAddress = ""),
      (this._selectedReceiverAddress = ""),
      (this._onPopState = () => {
        this._parseUrlHash();
      });
  }
  connectedCallback() {
    super.connectedCallback(),
      this._resolveEntryId().then(() => this._parseUrlHash()),
      window.addEventListener("popstate", this._onPopState);
  }
  disconnectedCallback() {
    super.disconnectedCallback(),
      window.removeEventListener("popstate", this._onPopState);
  }
  _parseUrlHash() {
    const e = window.location.hash.slice(1);
    if (!e) return;
    const t = new URLSearchParams(e),
      i = t.get("view"),
      s = t.get("entry") || this._entryId,
      n = t.get("device") || "",
      r = t.get("interface") || "",
      a = t.get("channel") || "",
      o = t.get("channel_type") || "",
      d = t.get("paramset") || "MASTER",
      c = t.get("sender") || "",
      l = t.get("receiver") || "";
    s && (this._entryId = s),
      i &&
        this._navigateTo(i, {
          device: n,
          interfaceId: r,
          channel: a,
          channelType: o,
          paramsetKey: d,
          senderAddress: c,
          receiverAddress: l,
        });
  }
  _updateUrlHash() {
    const e = new URLSearchParams();
    e.set("view", this._view),
      this._entryId && e.set("entry", this._entryId),
      "device-list" !== this._view &&
        (this._selectedDevice && e.set("device", this._selectedDevice),
        this._selectedInterfaceId &&
          e.set("interface", this._selectedInterfaceId)),
      "channel-config" === this._view &&
        (this._selectedChannel && e.set("channel", this._selectedChannel),
        this._selectedChannelType &&
          e.set("channel_type", this._selectedChannelType),
        "MASTER" !== this._selectedParamsetKey &&
          e.set("paramset", this._selectedParamsetKey)),
      "link-config" === this._view &&
        (this._selectedSenderAddress &&
          e.set("sender", this._selectedSenderAddress),
        this._selectedReceiverAddress &&
          e.set("receiver", this._selectedReceiverAddress)),
      "add-link" === this._view &&
        this._selectedChannel &&
        e.set("channel", this._selectedChannel);
    const t = e.toString();
    window.history.replaceState(null, "", `#${t}`);
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
      void 0 !== t?.device && (this._selectedDevice = t.device),
      void 0 !== t?.interfaceId && (this._selectedInterfaceId = t.interfaceId),
      void 0 !== t?.channel && (this._selectedChannel = t.channel),
      void 0 !== t?.channelType && (this._selectedChannelType = t.channelType),
      void 0 !== t?.paramsetKey && (this._selectedParamsetKey = t.paramsetKey),
      void 0 !== t?.deviceName && (this._selectedDeviceName = t.deviceName),
      void 0 !== t?.senderAddress &&
        (this._selectedSenderAddress = t.senderAddress),
      void 0 !== t?.receiverAddress &&
        (this._selectedReceiverAddress = t.receiverAddress),
      this._updateUrlHash();
  }
  render() {
    switch (this._view) {
      case "device-list":
        return B`
          <hm-device-list
            .hass=${this.hass}
            .entryId=${this._entryId}
            .entries=${this._entries}
            @entry-changed=${(e) => {
              (this._entryId = e.detail.entryId), this._updateUrlHash();
            }}
            @device-selected=${(e) =>
              this._navigateTo("device-detail", e.detail)}
          ></hm-device-list>
        `;
      case "device-detail":
        return B`
          <hm-device-detail
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            @channel-selected=${(e) =>
              this._navigateTo("channel-config", e.detail)}
            @show-history=${(e) => this._navigateTo("change-history", e.detail)}
            @show-links=${(e) => this._navigateTo("device-links", e.detail)}
            @back=${() => this._navigateTo("device-list")}
          ></hm-device-detail>
        `;
      case "channel-config":
        return B`
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
      case "change-history":
        return B`
          <hm-change-history
            .hass=${this.hass}
            .entryId=${this._entryId}
            .filterDevice=${this._selectedDevice}
            @back=${() =>
              this._navigateTo(
                this._selectedDevice ? "device-detail" : "device-list",
                this._selectedDevice
                  ? {
                      device: this._selectedDevice,
                      interfaceId: this._selectedInterfaceId,
                    }
                  : void 0,
              )}
          ></hm-change-history>
        `;
      case "device-links":
        return B`
          <hm-device-links
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            .deviceName=${this._selectedDeviceName}
            @configure-link=${(e) => this._navigateTo("link-config", e.detail)}
            @add-link=${(e) => this._navigateTo("add-link", e.detail)}
            @back=${() =>
              this._navigateTo("device-detail", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
          ></hm-device-links>
        `;
      case "link-config":
        return B`
          <hm-link-config
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .senderAddress=${this._selectedSenderAddress}
            .receiverAddress=${this._selectedReceiverAddress}
            @back=${() =>
              this._navigateTo("device-links", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
          ></hm-link-config>
        `;
      case "add-link":
        return B`
          <hm-add-link
            .hass=${this.hass}
            .entryId=${this._entryId}
            .interfaceId=${this._selectedInterfaceId}
            .deviceAddress=${this._selectedDevice}
            @link-created=${() =>
              this._navigateTo("device-links", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
            @back=${() =>
              this._navigateTo("device-links", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
          ></hm-add-link>
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
e([he({ attribute: !1 })], Ne.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Ne.prototype, "panel", void 0),
  e([he({ type: Boolean, reflect: !0 })], Ne.prototype, "narrow", void 0),
  e([pe()], Ne.prototype, "_view", void 0),
  e([pe()], Ne.prototype, "_entryId", void 0),
  e([pe()], Ne.prototype, "_entries", void 0),
  e([pe()], Ne.prototype, "_selectedDevice", void 0),
  e([pe()], Ne.prototype, "_selectedInterfaceId", void 0),
  e([pe()], Ne.prototype, "_selectedChannel", void 0),
  e([pe()], Ne.prototype, "_selectedChannelType", void 0),
  e([pe()], Ne.prototype, "_selectedParamsetKey", void 0),
  e([pe()], Ne.prototype, "_selectedDeviceName", void 0),
  e([pe()], Ne.prototype, "_selectedSenderAddress", void 0),
  e([pe()], Ne.prototype, "_selectedReceiverAddress", void 0),
  (Ne = e([_e("homematic-config")], Ne));
export { Ne as HomematicConfigPanel };
