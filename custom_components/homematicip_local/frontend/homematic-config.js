function e(e, t, i, s) {
  var r,
    a = arguments.length,
    n =
      a < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    n = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (r = e[o]) && (n = (a < 3 ? r(n) : a > 3 ? r(t, i, n) : r(t, i)) || n);
  return a > 3 && n && Object.defineProperty(t, i, n), n;
}
"function" == typeof SuppressedError && SuppressedError;
const t = globalThis,
  i =
    t.ShadowRoot &&
    (void 0 === t.ShadyCSS || t.ShadyCSS.nativeShadow) &&
    "adoptedStyleSheets" in Document.prototype &&
    "replace" in CSSStyleSheet.prototype,
  s = Symbol(),
  r = new WeakMap();
let a = class {
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
      i && (e = r.get(t)),
        void 0 === e &&
          ((this.o = e = new CSSStyleSheet()).replaceSync(this.cssText),
          i && r.set(t, e));
    }
    return e;
  }
  toString() {
    return this.cssText;
  }
};
const n = (e, ...t) => {
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
    return new a(i, e, s);
  },
  o = i
    ? (e) => e
    : (e) =>
        e instanceof CSSStyleSheet
          ? ((e) => {
              let t = "";
              for (const i of e.cssRules) t += i.cssText;
              return ((e) =>
                new a("string" == typeof e ? e : e + "", void 0, s))(t);
            })(e)
          : e,
  {
    is: d,
    defineProperty: l,
    getOwnPropertyDescriptor: c,
    getOwnPropertyNames: h,
    getOwnPropertySymbols: p,
    getPrototypeOf: _,
  } = Object,
  u = globalThis,
  v = u.trustedTypes,
  m = v ? v.emptyScript : "",
  g = u.reactiveElementPolyfillSupport,
  f = (e, t) => e,
  y = {
    toAttribute(e, t) {
      switch (t) {
        case Boolean:
          e = e ? m : null;
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
  (u.litPropertyMetadata ??= new WeakMap());
let k = class extends HTMLElement {
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
      void 0 !== s && l(this.prototype, e, s);
    }
  }
  static getPropertyDescriptor(e, t, i) {
    const { get: s, set: r } = c(this.prototype, e) ?? {
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
        const a = s?.call(this);
        r?.call(this, t), this.requestUpdate(e, a, i);
      },
      configurable: !0,
      enumerable: !0,
    };
  }
  static getPropertyOptions(e) {
    return this.elementProperties.get(e) ?? x;
  }
  static _$Ei() {
    if (this.hasOwnProperty(f("elementProperties"))) return;
    const e = _(this);
    e.finalize(),
      void 0 !== e.l && (this.l = [...e.l]),
      (this.elementProperties = new Map(e.elementProperties));
  }
  static finalize() {
    if (this.hasOwnProperty(f("finalized"))) return;
    if (
      ((this.finalized = !0), this._$Ei(), this.hasOwnProperty(f("properties")))
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
              r = t.litNonce;
            void 0 !== r && s.setAttribute("nonce", r),
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
      const r = (
        void 0 !== i.converter?.toAttribute ? i.converter : y
      ).toAttribute(t, i.type);
      (this._$Em = e),
        null == r ? this.removeAttribute(s) : this.setAttribute(s, r),
        (this._$Em = null);
    }
  }
  _$AK(e, t) {
    const i = this.constructor,
      s = i._$Eh.get(e);
    if (void 0 !== s && this._$Em !== s) {
      const e = i.getPropertyOptions(s),
        r =
          "function" == typeof e.converter
            ? { fromAttribute: e.converter }
            : void 0 !== e.converter?.fromAttribute
              ? e.converter
              : y;
      this._$Em = s;
      const a = r.fromAttribute(t, e.type);
      (this[s] = a ?? this._$Ej?.get(s) ?? a), (this._$Em = null);
    }
  }
  requestUpdate(e, t, i, s = !1, r) {
    if (void 0 !== e) {
      const a = this.constructor;
      if (
        (!1 === s && (r = this[e]),
        (i ??= a.getPropertyOptions(e)),
        !(
          (i.hasChanged ?? b)(r, t) ||
          (i.useDefault &&
            i.reflect &&
            r === this._$Ej?.get(e) &&
            !this.hasAttribute(a._$Eu(e, i)))
        ))
      )
        return;
      this.C(e, t, i);
    }
    !1 === this.isUpdatePending && (this._$ES = this._$EP());
  }
  C(e, t, { useDefault: i, reflect: s, wrapped: r }, a) {
    (i &&
      !(this._$Ej ??= new Map()).has(e) &&
      (this._$Ej.set(e, a ?? t ?? this[e]), !0 !== r || void 0 !== a)) ||
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
(k.elementStyles = []),
  (k.shadowRootOptions = { mode: "open" }),
  (k[f("elementProperties")] = new Map()),
  (k[f("finalized")] = new Map()),
  g?.({ ReactiveElement: k }),
  (u.reactiveElementVersions ??= []).push("2.1.2");
const $ = globalThis,
  w = (e) => e,
  S = $.trustedTypes,
  E = S ? S.createPolicy("lit-html", { createHTML: (e) => e }) : void 0,
  C = "$lit$",
  A = `lit$${Math.random().toFixed(9).slice(2)}$`,
  D = "?" + A,
  T = `<${D}>`,
  I = document,
  M = () => I.createComment(""),
  P = (e) => null === e || ("object" != typeof e && "function" != typeof e),
  z = Array.isArray,
  N = "[ \t\n\f\r]",
  R = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,
  B = /-->/g,
  L = />/g,
  U = RegExp(
    `>|${N}(?:([^\\s"'>=/]+)(${N}*=${N}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,
    "g",
  ),
  O = /'/g,
  W = /"/g,
  j = /^(?:script|style|textarea|title)$/i,
  V = (e, ...t) => ({ _$litType$: 1, strings: e, values: t }),
  F = Symbol.for("lit-noChange"),
  K = Symbol.for("lit-nothing"),
  H = new WeakMap(),
  Y = I.createTreeWalker(I, 129);
function G(e, t) {
  if (!z(e) || !e.hasOwnProperty("raw"))
    throw Error("invalid template strings array");
  return void 0 !== E ? E.createHTML(t) : t;
}
class Z {
  constructor({ strings: e, _$litType$: t }, i) {
    let s;
    this.parts = [];
    let r = 0,
      a = 0;
    const n = e.length - 1,
      o = this.parts,
      [d, l] = ((e, t) => {
        const i = e.length - 1,
          s = [];
        let r,
          a = 2 === t ? "<svg>" : 3 === t ? "<math>" : "",
          n = R;
        for (let t = 0; t < i; t++) {
          const i = e[t];
          let o,
            d,
            l = -1,
            c = 0;
          for (
            ;
            c < i.length && ((n.lastIndex = c), (d = n.exec(i)), null !== d);

          )
            (c = n.lastIndex),
              n === R
                ? "!--" === d[1]
                  ? (n = B)
                  : void 0 !== d[1]
                    ? (n = L)
                    : void 0 !== d[2]
                      ? (j.test(d[2]) && (r = RegExp("</" + d[2], "g")),
                        (n = U))
                      : void 0 !== d[3] && (n = U)
                : n === U
                  ? ">" === d[0]
                    ? ((n = r ?? R), (l = -1))
                    : void 0 === d[1]
                      ? (l = -2)
                      : ((l = n.lastIndex - d[2].length),
                        (o = d[1]),
                        (n = void 0 === d[3] ? U : '"' === d[3] ? W : O))
                  : n === W || n === O
                    ? (n = U)
                    : n === B || n === L
                      ? (n = R)
                      : ((n = U), (r = void 0));
          const h = n === U && e[t + 1].startsWith("/>") ? " " : "";
          a +=
            n === R
              ? i + T
              : l >= 0
                ? (s.push(o), i.slice(0, l) + C + i.slice(l) + A + h)
                : i + A + (-2 === l ? t : h);
        }
        return [
          G(
            e,
            a +
              (e[i] || "<?>") +
              (2 === t ? "</svg>" : 3 === t ? "</math>" : ""),
          ),
          s,
        ];
      })(e, t);
    if (
      ((this.el = Z.createElement(d, i)),
      (Y.currentNode = this.el.content),
      2 === t || 3 === t)
    ) {
      const e = this.el.content.firstChild;
      e.replaceWith(...e.childNodes);
    }
    for (; null !== (s = Y.nextNode()) && o.length < n; ) {
      if (1 === s.nodeType) {
        if (s.hasAttributes())
          for (const e of s.getAttributeNames())
            if (e.endsWith(C)) {
              const t = l[a++],
                i = s.getAttribute(e).split(A),
                n = /([.?@])?(.*)/.exec(t);
              o.push({
                type: 1,
                index: r,
                name: n[2],
                strings: i,
                ctor:
                  "." === n[1] ? ee : "?" === n[1] ? te : "@" === n[1] ? ie : X,
              }),
                s.removeAttribute(e);
            } else
              e.startsWith(A) &&
                (o.push({ type: 6, index: r }), s.removeAttribute(e));
        if (j.test(s.tagName)) {
          const e = s.textContent.split(A),
            t = e.length - 1;
          if (t > 0) {
            s.textContent = S ? S.emptyScript : "";
            for (let i = 0; i < t; i++)
              s.append(e[i], M()),
                Y.nextNode(),
                o.push({ type: 2, index: ++r });
            s.append(e[t], M());
          }
        }
      } else if (8 === s.nodeType)
        if (s.data === D) o.push({ type: 2, index: r });
        else {
          let e = -1;
          for (; -1 !== (e = s.data.indexOf(A, e + 1)); )
            o.push({ type: 7, index: r }), (e += A.length - 1);
        }
      r++;
    }
  }
  static createElement(e, t) {
    const i = I.createElement("template");
    return (i.innerHTML = e), i;
  }
}
function J(e, t, i = e, s) {
  if (t === F) return t;
  let r = void 0 !== s ? i._$Co?.[s] : i._$Cl;
  const a = P(t) ? void 0 : t._$litDirective$;
  return (
    r?.constructor !== a &&
      (r?._$AO?.(!1),
      void 0 === a ? (r = void 0) : ((r = new a(e)), r._$AT(e, i, s)),
      void 0 !== s ? ((i._$Co ??= [])[s] = r) : (i._$Cl = r)),
    void 0 !== r && (t = J(e, r._$AS(e, t.values), r, s)),
    t
  );
}
class q {
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
      s = (e?.creationScope ?? I).importNode(t, !0);
    Y.currentNode = s;
    let r = Y.nextNode(),
      a = 0,
      n = 0,
      o = i[0];
    for (; void 0 !== o; ) {
      if (a === o.index) {
        let t;
        2 === o.type
          ? (t = new Q(r, r.nextSibling, this, e))
          : 1 === o.type
            ? (t = new o.ctor(r, o.name, o.strings, this, e))
            : 6 === o.type && (t = new se(r, this, e)),
          this._$AV.push(t),
          (o = i[++n]);
      }
      a !== o?.index && ((r = Y.nextNode()), a++);
    }
    return (Y.currentNode = I), s;
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
class Q {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(e, t, i, s) {
    (this.type = 2),
      (this._$AH = K),
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
      P(e)
        ? e === K || null == e || "" === e
          ? (this._$AH !== K && this._$AR(), (this._$AH = K))
          : e !== this._$AH && e !== F && this._(e)
        : void 0 !== e._$litType$
          ? this.$(e)
          : void 0 !== e.nodeType
            ? this.T(e)
            : ((e) => z(e) || "function" == typeof e?.[Symbol.iterator])(e)
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
    this._$AH !== K && P(this._$AH)
      ? (this._$AA.nextSibling.data = e)
      : this.T(I.createTextNode(e)),
      (this._$AH = e);
  }
  $(e) {
    const { values: t, _$litType$: i } = e,
      s =
        "number" == typeof i
          ? this._$AC(e)
          : (void 0 === i.el &&
              (i.el = Z.createElement(G(i.h, i.h[0]), this.options)),
            i);
    if (this._$AH?._$AD === s) this._$AH.p(t);
    else {
      const e = new q(s, this),
        i = e.u(this.options);
      e.p(t), this.T(i), (this._$AH = e);
    }
  }
  _$AC(e) {
    let t = H.get(e.strings);
    return void 0 === t && H.set(e.strings, (t = new Z(e))), t;
  }
  k(e) {
    z(this._$AH) || ((this._$AH = []), this._$AR());
    const t = this._$AH;
    let i,
      s = 0;
    for (const r of e)
      s === t.length
        ? t.push((i = new Q(this.O(M()), this.O(M()), this, this.options)))
        : (i = t[s]),
        i._$AI(r),
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
class X {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, t, i, s, r) {
    (this.type = 1),
      (this._$AH = K),
      (this._$AN = void 0),
      (this.element = e),
      (this.name = t),
      (this._$AM = s),
      (this.options = r),
      i.length > 2 || "" !== i[0] || "" !== i[1]
        ? ((this._$AH = Array(i.length - 1).fill(new String())),
          (this.strings = i))
        : (this._$AH = K);
  }
  _$AI(e, t = this, i, s) {
    const r = this.strings;
    let a = !1;
    if (void 0 === r)
      (e = J(this, e, t, 0)),
        (a = !P(e) || (e !== this._$AH && e !== F)),
        a && (this._$AH = e);
    else {
      const s = e;
      let n, o;
      for (e = r[0], n = 0; n < r.length - 1; n++)
        (o = J(this, s[i + n], t, n)),
          o === F && (o = this._$AH[n]),
          (a ||= !P(o) || o !== this._$AH[n]),
          o === K ? (e = K) : e !== K && (e += (o ?? "") + r[n + 1]),
          (this._$AH[n] = o);
    }
    a && !s && this.j(e);
  }
  j(e) {
    e === K
      ? this.element.removeAttribute(this.name)
      : this.element.setAttribute(this.name, e ?? "");
  }
}
class ee extends X {
  constructor() {
    super(...arguments), (this.type = 3);
  }
  j(e) {
    this.element[this.name] = e === K ? void 0 : e;
  }
}
class te extends X {
  constructor() {
    super(...arguments), (this.type = 4);
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== K);
  }
}
class ie extends X {
  constructor(e, t, i, s, r) {
    super(e, t, i, s, r), (this.type = 5);
  }
  _$AI(e, t = this) {
    if ((e = J(this, e, t, 0) ?? K) === F) return;
    const i = this._$AH,
      s =
        (e === K && i !== K) ||
        e.capture !== i.capture ||
        e.once !== i.once ||
        e.passive !== i.passive,
      r = e !== K && (i === K || s);
    s && this.element.removeEventListener(this.name, this, i),
      r && this.element.addEventListener(this.name, this, e),
      (this._$AH = e);
  }
  handleEvent(e) {
    "function" == typeof this._$AH
      ? this._$AH.call(this.options?.host ?? this.element, e)
      : this._$AH.handleEvent(e);
  }
}
class se {
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
const re = { I: Q },
  ae = $.litHtmlPolyfillSupport;
ae?.(Z, Q), ($.litHtmlVersions ??= []).push("3.3.2");
const ne = globalThis;
let oe = class extends k {
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
        let r = s._$litPart$;
        if (void 0 === r) {
          const e = i?.renderBefore ?? null;
          s._$litPart$ = r = new Q(t.insertBefore(M(), e), e, void 0, i ?? {});
        }
        return r._$AI(e), r;
      })(t, this.renderRoot, this.renderOptions));
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return F;
  }
};
(oe._$litElement$ = !0),
  (oe.finalized = !0),
  ne.litElementHydrateSupport?.({ LitElement: oe });
const de = ne.litElementPolyfillSupport;
de?.({ LitElement: oe }), (ne.litElementVersions ??= []).push("4.2.2");
const le = {
    attribute: !0,
    type: String,
    converter: y,
    reflect: !1,
    hasChanged: b,
  },
  ce = (e = le, t, i) => {
    const { kind: s, metadata: r } = i;
    let a = globalThis.litPropertyMetadata.get(r);
    if (
      (void 0 === a && globalThis.litPropertyMetadata.set(r, (a = new Map())),
      "setter" === s && ((e = Object.create(e)).wrapped = !0),
      a.set(i.name, e),
      "accessor" === s)
    ) {
      const { name: s } = i;
      return {
        set(i) {
          const r = t.get.call(this);
          t.set.call(this, i), this.requestUpdate(s, r, e, !0, i);
        },
        init(t) {
          return void 0 !== t && this.C(s, void 0, e, t), t;
        },
      };
    }
    if ("setter" === s) {
      const { name: s } = i;
      return function (i) {
        const r = this[s];
        t.call(this, i), this.requestUpdate(s, r, e, !0, i);
      };
    }
    throw Error("Unsupported decorator location: " + s);
  };
function he(e) {
  return (t, i) =>
    "object" == typeof i
      ? ce(e, t, i)
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
const ue = n`
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
  ve = new Set(["BidCos-RF", "BidCos-Wired", "HmIP-RF"]);
async function me(e, t) {
  return (
    await e.callWS({
      type: "homematicip_local/config/list_devices",
      entry_id: t,
    })
  ).devices;
}
async function ge(e, t, i, s, r = "", a = "MASTER") {
  return e.callWS({
    type: "homematicip_local/config/get_form_schema",
    entry_id: t,
    interface_id: i,
    channel_address: s,
    channel_type: r,
    paramset_key: a,
  });
}
async function fe(e, t, i, s, r = "MASTER") {
  return e.callWS({
    type: "homematicip_local/config/session_open",
    entry_id: t,
    interface_id: i,
    channel_address: s,
    paramset_key: r,
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
async function be(e, t, i, s, r) {
  return e.callWS({
    type: "homematicip_local/config/get_link_form_schema",
    entry_id: t,
    interface_id: i,
    sender_channel_address: s,
    receiver_channel_address: r,
  });
}
async function xe(e, t, i, s, r, a) {
  return e.callWS({
    type: "homematicip_local/config/put_link_paramset",
    entry_id: t,
    interface_id: i,
    sender_channel_address: s,
    receiver_channel_address: r,
    values: a,
  });
}
async function ke(e, t) {
  return (
    await e.callWS({
      type: "homematicip_local/config/list_schedule_devices",
      entry_id: t,
    })
  ).devices;
}
async function $e(e, t, i, s, r, a, n) {
  return e.callWS({
    type: "homematicip_local/config/set_climate_schedule_weekday",
    entry_id: t,
    device_address: i,
    profile: s,
    weekday: r,
    base_temperature: a,
    simple_weekday_list: n,
  });
}
async function we(e, t, i, s) {
  return e.callWS({
    type: "homematicip_local/config/set_device_schedule",
    entry_id: t,
    device_address: i,
    schedule_data: s,
  });
}
async function Se(e, t, i, s, r) {
  try {
    return await e.callWS({
      type: "homematicip_local/config/get_link_profiles",
      entry_id: t,
      interface_id: i,
      sender_channel_address: s,
      receiver_channel_address: r,
    });
  } catch {
    return null;
  }
}
const Ee = {
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
      show_schedules: "Schedules",
      rssi_device: "RSSI Device",
      rssi_peer: "RSSI Peer",
      dutycycle: "Duty Cycle",
      low_bat: "Low Battery",
      unreach: "Reachability",
      config_pending_label: "Config Pending",
    },
    form_parameter: { toggle_on: "On", toggle_off: "Off" },
    time_selector: { base: "Base", factor: "Factor" },
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
      receiver_params: "Receiver Parameters",
      sender_params: "Sender Parameters",
      no_params: "No configurable parameters for this link.",
      profile: "Profile",
      short_keypress: "Short keypress",
      long_keypress: "Long keypress",
      last_value: "Last value",
      custom_time: "Custom",
    },
    device_schedule: {
      title: "Schedules",
      subtitle: "Schedules for {device}",
      select_device: "Select a device...",
      no_devices: "No devices with schedule support found.",
      schedule_type_climate: "Climate",
      schedule_type_default: "Device",
      profile: "Profile",
      active_profile: "Active profile",
      weekdays: "Mon,Tue,Wed,Thu,Fri,Sat,Sun",
      weekday_monday: "Monday",
      weekday_tuesday: "Tuesday",
      weekday_wednesday: "Wednesday",
      weekday_thursday: "Thursday",
      weekday_friday: "Friday",
      weekday_saturday: "Saturday",
      weekday_sunday: "Sunday",
      base_temperature: "Base temperature",
      temperature: "Temperature",
      time: "Time",
      from: "From",
      to: "To",
      add_period: "Add period",
      delete_period: "Delete",
      save: "Save",
      saving: "Saving...",
      save_success: "Schedule saved successfully.",
      save_failed: "Failed to save schedule.",
      load_failed: "Failed to load schedule.",
      reload: "Reload from device",
      reload_success: "Device configuration reloaded.",
      reload_failed: "Failed to reload device configuration.",
      export: "Export",
      import: "Import",
      import_confirm_title: "Import Schedule",
      import_confirm_text: "Import and apply this schedule?",
      import_success: "Schedule imported.",
      import_failed: "Failed to import schedule.",
      no_schedule_data: "No schedule data available.",
      click_to_edit: "Click on a time slot to edit the schedule",
      copy_schedule: "Copy schedule",
      paste_schedule: "Paste schedule",
      edit: "Edit {weekday}",
      add_time_block: "+ Add Time Block",
      edit_slot: "Edit",
      save_slot: "Save",
      cancel_slot_edit: "Cancel",
      undo_shortcut: "Undo (Ctrl+Z)",
      redo_shortcut: "Redo (Ctrl+Y)",
      warnings_title: "Validation Warnings",
      base_temperature_description: "Temperature for unscheduled periods",
      temperature_periods: "Temperature Periods",
      invalid_schedule: "Invalid schedule: {error}",
      validation_block_end_before_start:
        "Block {block}: End time is before start time",
      validation_block_zero_duration: "Block {block}: Block has zero duration",
      validation_invalid_start_time: "Block {block}: Invalid start time",
      validation_invalid_end_time: "Block {block}: Invalid end time",
      validation_temp_out_of_range:
        "Block {block}: Temperature out of range ({min}-{max}°C)",
      validation_invalid_slot_count:
        "Invalid number of slots: {count} (expected 13)",
      validation_invalid_slot_key:
        "Invalid slot key: {key} (must be integer 1-13)",
      validation_missing_slot: "Missing slot {slot}",
      validation_slot_missing_values:
        "Slot {slot} missing ENDTIME or TEMPERATURE",
      validation_slot_time_backwards: "Slot {slot} time goes backwards: {time}",
      validation_slot_time_exceeds_day:
        "Slot {slot} time exceeds 24:00: {time}",
      validation_last_slot_must_end: "Last slot must end at 24:00",
      validation_schedule_must_be_object: "Schedule data must be an object",
      validation_missing_weekday: "Missing weekday: {weekday}",
      validation_invalid_weekday_data: "Invalid data for {weekday}",
      validation_weekday_error: "{weekday}: {details}",
      entries: "{count} entries",
      max_entries: "Max entries: {max}",
      level: "Level",
      duration: "Duration",
      condition: "Condition",
      target_channel: "Target channel",
      add_event: "Add Event",
      edit_event: "Edit Event",
      confirm_delete: "Are you sure you want to delete this event?",
      weekdays_label: "Weekdays",
      level_on: "On",
      level_off: "Off",
      slat: "Slat Position",
      ramp_time: "Ramp Time",
      astro_sunrise: "Sunrise",
      astro_sunset: "Sunset",
      astro_offset: "Astro Offset (min)",
      condition_fixed_time: "Fixed Time",
      condition_astro: "Astro",
      condition_fixed_if_before_astro: "Fixed if before Astro",
      condition_astro_if_before_fixed: "Astro if before Fixed",
      condition_fixed_if_after_astro: "Fixed if after Astro",
      condition_astro_if_after_fixed: "Astro if after Fixed",
      condition_earliest: "Earliest",
      condition_latest: "Latest",
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
      show_schedules: "Zeitpläne",
      rssi_device: "RSSI Gerät",
      rssi_peer: "RSSI Peer",
      dutycycle: "Duty Cycle",
      low_bat: "Batterie schwach",
      unreach: "Erreichbarkeit",
      config_pending_label: "Konfig. ausstehend",
    },
    form_parameter: { toggle_on: "Ein", toggle_off: "Aus" },
    time_selector: { base: "Basis", factor: "Faktor" },
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
      receiver_params: "Empfänger-Parameter",
      sender_params: "Sender-Parameter",
      no_params: "Keine konfigurierbaren Parameter für diese Verknüpfung.",
      profile: "Profil",
      short_keypress: "Kurzer Tastendruck",
      long_keypress: "Langer Tastendruck",
      last_value: "Letzter Wert",
      custom_time: "Benutzerdefiniert",
    },
    device_schedule: {
      title: "Zeitpläne",
      subtitle: "Zeitpläne für {device}",
      select_device: "Gerät auswählen...",
      no_devices: "Keine Geräte mit Zeitplan-Unterstützung gefunden.",
      schedule_type_climate: "Heizung",
      schedule_type_default: "Gerät",
      profile: "Profil",
      active_profile: "Aktives Profil",
      weekdays: "Mo,Di,Mi,Do,Fr,Sa,So",
      weekday_monday: "Montag",
      weekday_tuesday: "Dienstag",
      weekday_wednesday: "Mittwoch",
      weekday_thursday: "Donnerstag",
      weekday_friday: "Freitag",
      weekday_saturday: "Samstag",
      weekday_sunday: "Sonntag",
      base_temperature: "Basistemperatur",
      temperature: "Temperatur",
      time: "Uhrzeit",
      from: "Von",
      to: "Bis",
      add_period: "Zeitraum hinzufügen",
      delete_period: "Löschen",
      save: "Speichern",
      saving: "Speichern...",
      save_success: "Zeitplan erfolgreich gespeichert.",
      save_failed: "Fehler beim Speichern des Zeitplans.",
      load_failed: "Fehler beim Laden des Zeitplans.",
      reload: "Vom Gerät laden",
      reload_success: "Gerätekonfiguration neu geladen.",
      reload_failed: "Fehler beim Laden der Gerätekonfiguration.",
      export: "Exportieren",
      import: "Importieren",
      import_confirm_title: "Zeitplan importieren",
      import_confirm_text: "Diesen Zeitplan importieren und anwenden?",
      import_success: "Zeitplan importiert.",
      import_failed: "Fehler beim Importieren des Zeitplans.",
      no_schedule_data: "Keine Zeitplan-Daten verfügbar.",
      click_to_edit:
        "Klicken Sie auf einen Zeitabschnitt, um den Zeitplan zu bearbeiten",
      copy_schedule: "Zeitplan kopieren",
      paste_schedule: "Zeitplan einfügen",
      edit: "{weekday} bearbeiten",
      add_time_block: "+ Zeitblock hinzufügen",
      edit_slot: "Bearbeiten",
      save_slot: "Speichern",
      cancel_slot_edit: "Abbrechen",
      undo_shortcut: "Rückgängig (Strg+Z)",
      redo_shortcut: "Wiederholen (Strg+Y)",
      warnings_title: "Validierungswarnungen",
      base_temperature_description: "Temperatur für nicht geplante Zeiträume",
      temperature_periods: "Temperaturperioden",
      invalid_schedule: "Ungültiger Zeitplan: {error}",
      validation_block_end_before_start:
        "Block {block}: Die Endzeit liegt vor der Startzeit",
      validation_block_zero_duration:
        "Block {block}: Der Block hat keine Dauer",
      validation_invalid_start_time: "Block {block}: Ungültige Startzeit",
      validation_invalid_end_time: "Block {block}: Ungültige Endzeit",
      validation_temp_out_of_range:
        "Block {block}: Temperatur außerhalb des Bereichs ({min}-{max}°C)",
      validation_invalid_slot_count:
        "Ungültige Anzahl an Slots: {count} (erwartet 13)",
      validation_invalid_slot_key:
        "Ungültiger Slot-Schlüssel: {key} (muss eine Ganzzahl 1-13 sein)",
      validation_missing_slot: "Slot {slot} fehlt",
      validation_slot_missing_values:
        "Slot {slot} fehlt ENDTIME oder TEMPERATURE",
      validation_slot_time_backwards:
        "Slot {slot}: Zeit läuft rückwärts: {time}",
      validation_slot_time_exceeds_day:
        "Slot {slot}: Zeit überschreitet 24:00: {time}",
      validation_last_slot_must_end: "Der letzte Slot muss um 24:00 enden",
      validation_schedule_must_be_object:
        "Zeitplandaten müssen ein Objekt sein",
      validation_missing_weekday: "Fehlender Wochentag: {weekday}",
      validation_invalid_weekday_data: "Ungültige Daten für {weekday}",
      validation_weekday_error: "{weekday}: {details}",
      entries: "{count} Einträge",
      max_entries: "Max. Einträge: {max}",
      level: "Wert",
      duration: "Dauer",
      condition: "Bedingung",
      target_channel: "Zielkanal",
      add_event: "Ereignis hinzufügen",
      edit_event: "Ereignis bearbeiten",
      confirm_delete: "Möchten Sie dieses Ereignis wirklich löschen?",
      weekdays_label: "Wochentage",
      level_on: "Ein",
      level_off: "Aus",
      slat: "Lamellenposition",
      ramp_time: "Rampenzeit",
      astro_sunrise: "Sonnenaufgang",
      astro_sunset: "Sonnenuntergang",
      astro_offset: "Astro-Offset (Min.)",
      condition_fixed_time: "Feste Zeit",
      condition_astro: "Astro",
      condition_fixed_if_before_astro: "Fest wenn vor Astro",
      condition_astro_if_before_fixed: "Astro wenn vor Fest",
      condition_fixed_if_after_astro: "Fest wenn nach Astro",
      condition_astro_if_after_fixed: "Astro wenn nach Fest",
      condition_earliest: "Frühester",
      condition_latest: "Spätester",
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
function Ce(e, t = "") {
  const i = {};
  for (const [s, r] of Object.entries(e)) {
    const e = t ? `${t}.${s}` : s;
    "string" == typeof r
      ? (i[e] = r)
      : "object" == typeof r && null !== r && Object.assign(i, Ce(r, e));
  }
  return i;
}
const Ae = new Map();
function De(e) {
  if (Ae.has(e)) return Ae.get(e);
  const t = Ce(Ee[e] ?? Ee.en);
  return Ae.set(e, t), t;
}
function Te(e, t, i) {
  const s = De(e.config.language ?? "en");
  let r = s[t] ?? s[t.replace(/^panel\./, "")] ?? t;
  if (i)
    for (const [e, t] of Object.entries(i)) r = r.replace(`{${e}}`, String(t));
  return r;
}
let Ie = class extends oe {
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
        this._devices = await me(this.hass, this.entryId);
      } catch (e) {
        (this._error = String(e)), (this._devices = []);
      } finally {
        this._loading = !1;
      }
    }
  }
  _l(e, t) {
    return Te(this.hass, e, t);
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
    this.dispatchEvent(
      new CustomEvent("entry-changed", {
        detail: { entryId: e.target.value },
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
      ? V`
      <div class="device-status">
        ${
          !0 === e.unreach
            ? V`<span
              class="status-badge unreachable"
              title="${this._l("device_list.unreachable")}"
              >&#x274C;</span
            >`
            : !1 === e.unreach
              ? V`<span class="status-badge reachable" title="${this._l(
                  "device_list.reachable",
                )}"
                >&#x2705;</span
              >`
              : K
        }
        ${
          !0 === e.low_bat
            ? V`<span class="status-badge low-bat" title="${this._l(
                "device_list.low_battery",
              )}"
              >&#x1F50B;</span
            >`
            : K
        }
        ${
          !0 === e.config_pending
            ? V`<span
              class="status-badge config-pending"
              title="${this._l("device_list.config_pending")}"
              >&#x23F3;</span
            >`
            : K
        }
      </div>
    `
      : K;
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
                    <option value=${e.entry_id} ?selected=${
                      e.entry_id === this.entryId
                    }>
                      ${e.title}
                    </option>
                  `,
                )}
              </select>
            </div>
          `
          : K
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
          : K
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
                <div class="device-card" @click=${() =>
                  this._handleDeviceClick(e)}>
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
                  <div class="device-arrow">▸</div>
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
      ue,
      n`
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
function Me(e, t) {
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
function Pe(e, t) {
  const i = new CustomEvent("hass-notification", {
    bubbles: !0,
    composed: !0,
    detail: t,
  });
  e.dispatchEvent(i);
}
e([he({ attribute: !1 })], Ie.prototype, "hass", void 0),
  e([he()], Ie.prototype, "entryId", void 0),
  e([he({ attribute: !1 })], Ie.prototype, "entries", void 0),
  e([pe()], Ie.prototype, "_devices", void 0),
  e([pe()], Ie.prototype, "_loading", void 0),
  e([pe()], Ie.prototype, "_searchQuery", void 0),
  e([pe()], Ie.prototype, "_error", void 0),
  (Ie = e([_e("hm-device-list")], Ie));
let ze = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.deviceAddress = ""),
      (this._device = null),
      (this._hasSchedule = !1),
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
      const [e, t] = await Promise.all([
        me(this.hass, this.entryId),
        ke(this.hass, this.entryId).catch(() => []),
      ]);
      (this._device = e.find((e) => e.address === this.deviceAddress) ?? null),
        (this._hasSchedule = t.some((e) => e.address === this.deviceAddress));
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return Te(this.hass, e, t);
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
  _handleShowSchedules() {
    this.dispatchEvent(
      new CustomEvent("show-schedules", {
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
      const t = await (async function (e, t, i, s, r = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/export_paramset",
            entry_id: t,
            interface_id: i,
            channel_address: s,
            paramset_key: r,
          });
        })(this.hass, this.entryId, this.interfaceId, e.address, "MASTER"),
        i = new Blob([t.json_data], { type: "application/json" }),
        s = URL.createObjectURL(i),
        r = document.createElement("a");
      (r.href = s),
        (r.download = `${e.address.replace(/:/g, "_")}_MASTER.json`),
        r.click(),
        URL.revokeObjectURL(s),
        Pe(this, { message: this._l("device_detail.export_success") });
    } catch {
      Pe(this, { message: this._l("device_detail.export_failed") });
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
              !(await Me(this, {
                title: this._l("device_detail.import_confirm_title"),
                text: this._l("device_detail.import_confirm_text", {
                  channel: e.address,
                }),
                confirmText: this._l("device_detail.import"),
                dismissText: this._l("common.cancel"),
              }))
            )
              return;
            const s = await (async function (e, t, i, s, r, a = "MASTER") {
              return e.callWS({
                type: "homematicip_local/config/import_paramset",
                entry_id: t,
                interface_id: i,
                channel_address: s,
                json_data: r,
                paramset_key: a,
              });
            })(
              this.hass,
              this.entryId,
              this.interfaceId,
              e.address,
              t,
              "MASTER",
            );
            Pe(
              this,
              s.success
                ? { message: this._l("device_detail.import_success") }
                : {
                    message: this._l("device_detail.import_validation_failed"),
                  },
            );
          } catch {
            Pe(this, { message: this._l("device_detail.import_failed") });
          }
      }),
      t.click();
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
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

      <div class="device-header">
        <h2>${e.model} — ${e.name}</h2>
        <div class="device-info">
          ${this._l("device_detail.address")}: ${e.address} |
          ${this._l("device_detail.firmware")}: ${e.firmware}
        </div>
        <div class="header-actions">
          ${
            ve.has(e.interface)
              ? V`
                <button class="history-button" @click=${this._handleShowLinks}>
                  ${this._l("device_detail.show_links")}
                </button>
              `
              : K
          }
          ${
            this._hasSchedule
              ? V`
                <button class="history-button" @click=${
                  this._handleShowSchedules
                }>
                  ${this._l("device_detail.show_schedules")}
                </button>
              `
              : K
          }
          <button class="history-button" @click=${this._handleShowHistory}>
            ${this._l("device_detail.show_history")}
          </button>
        </div>
      </div>

      ${t ? this._renderMaintenanceChannel(t, e.maintenance) : K}
      ${i.map((e) => this._renderChannel(e))}
    `;
  }
  _renderMaintenanceChannel(e, t) {
    const i = t && Object.keys(t).length > 0,
      s = e.paramset_keys.includes("MASTER");
    return V`
      <div class="channel-card maintenance">
        <div class="channel-header">
          ${this._l("device_detail.channel")} 0: ${e.channel_type_label}
        </div>
        ${i ? this._renderStatusSummary(t) : K}
        ${
          s
            ? V`
              <div class="channel-actions">
                <button class="configure-button" @click=${() =>
                  this._handleChannelClick(e)}>
                  ${this._l("device_detail.configure_master")} ▸
                </button>
                <button class="configure-button" @click=${() =>
                  this._handleExport(e)}>
                  ${this._l("device_detail.export")} &#x2B07;
                </button>
                <button class="configure-button" @click=${() =>
                  this._handleImport(e)}>
                  ${this._l("device_detail.import")} &#x2B06;
                </button>
              </div>
            `
            : K
        }
      </div>
    `;
  }
  _renderStatusSummary(e) {
    const t = [];
    return (
      void 0 !== e.rssi_device &&
        t.push({
          label: this._l("device_detail.rssi_device"),
          value: `${e.rssi_device} dBm`,
          icon: "📶",
        }),
      void 0 !== e.rssi_peer &&
        t.push({
          label: this._l("device_detail.rssi_peer"),
          value: `${e.rssi_peer} dBm`,
          icon: "📶",
        }),
      void 0 !== e.dutycycle &&
        t.push({
          label: this._l("device_detail.dutycycle"),
          value: String(e.dutycycle),
          icon: "⏱",
        }),
      void 0 !== e.low_bat &&
        t.push({
          label: this._l("device_detail.low_bat"),
          value: this._l(e.low_bat ? "device_detail.yes" : "device_detail.no"),
          icon: "🔋",
        }),
      void 0 !== e.unreach &&
        t.push({
          label: this._l("device_detail.unreach"),
          value: this._l(
            e.unreach ? "device_detail.unreachable" : "device_detail.reachable",
          ),
          icon: e.unreach ? "❌" : "✅",
        }),
      void 0 !== e.config_pending &&
        t.push({
          label: this._l("device_detail.config_pending_label"),
          value: this._l(
            e.config_pending ? "device_detail.yes" : "device_detail.no",
          ),
          icon: "ℹ️",
        }),
      0 === t.length
        ? K
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
    `
    );
  }
  _renderChannel(e) {
    const t = e.address.split(":").pop() ?? "",
      i = e.paramset_keys.includes("MASTER");
    return V`
      <div class="channel-card">
        <div class="channel-header">
          ${this._l("device_detail.channel")} ${t}: ${e.channel_type_label}
        </div>
        ${
          i
            ? V`
              <div class="channel-actions">
                <button class="configure-button" @click=${() =>
                  this._handleChannelClick(e)}>
                  ${this._l("device_detail.configure_master")} ▸
                </button>
                <button class="configure-button" @click=${() =>
                  this._handleExport(e)}>
                  ${this._l("device_detail.export")} &#x2B07;
                </button>
                <button class="configure-button" @click=${() =>
                  this._handleImport(e)}>
                  ${this._l("device_detail.import")} &#x2B06;
                </button>
              </div>
            `
            : V`
              <div class="channel-no-config">${this._l(
                "device_detail.no_master_config",
              )}</div>
            `
        }
      </div>
    `;
  }
  static {
    this.styles = [
      ue,
      n`
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
e([he({ attribute: !1 })], ze.prototype, "hass", void 0),
  e([he()], ze.prototype, "entryId", void 0),
  e([he()], ze.prototype, "interfaceId", void 0),
  e([he()], ze.prototype, "deviceAddress", void 0),
  e([pe()], ze.prototype, "_device", void 0),
  e([pe()], ze.prototype, "_hasSchedule", void 0),
  e([pe()], ze.prototype, "_loading", void 0),
  e([pe()], ze.prototype, "_error", void 0),
  (ze = e([_e("hm-device-detail")], ze));
let Ne = class extends oe {
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
          ${e.unit ? V`<span class="parameter-unit">(${e.unit})</span>` : K}
          ${this.modified ? V`<span class="modified-dot"></span>` : K}
        </div>
        <div class="parameter-control">${this._renderWidget(e, t)}</div>
      </div>
      ${
        this.validationError
          ? V`<div class="validation-error">${this.validationError}</div>`
          : K
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
            <span class="toggle-label"
              >${Te(
                this.hass,
                this.value
                  ? "form_parameter.toggle_on"
                  : "form_parameter.toggle_off",
              )}</span
            >
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
              this._emitChange(e.target.selectedIndex);
            }}
          >
            ${(e.options ?? []).map(
              (e, t) =>
                V` <option value=${t} ?selected=${
                  this.value === t
                }>${e}</option> `,
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
                  ${i}
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
      ue,
      n`
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
e([he({ attribute: !1 })], Ne.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Ne.prototype, "parameter", void 0),
  e([he()], Ne.prototype, "value", void 0),
  e([he({ type: Boolean })], Ne.prototype, "modified", void 0),
  e([he()], Ne.prototype, "validationError", void 0),
  (Ne = e([_e("hm-form-parameter")], Ne));
let Re = class extends oe {
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
      : K;
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
      ue,
      n`
      .form-section {
        margin-bottom: 16px;
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Re.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Re.prototype, "schema", void 0),
  e([he({ attribute: !1 })], Re.prototype, "pendingChanges", void 0),
  e([he({ attribute: !1 })], Re.prototype, "validationErrors", void 0),
  (Re = e([_e("hm-config-form")], Re));
let Be = class extends oe {
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
      (this._schema = await ge(
        this.hass,
        this.entryId,
        this.interfaceId,
        this.channelAddress,
        this.channelType,
        this.paramsetKey,
      )),
        await fe(
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
    return Te(this.hass, e, t);
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
        const e = await (async function (e, t, i, s, r, a = "MASTER") {
          return e.callWS({
            type: "homematicip_local/config/session_set",
            entry_id: t,
            channel_address: i,
            parameter: s,
            value: r,
            paramset_key: a,
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
      (this._schema = await ge(
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
              fe(
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
      await Me(this, {
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
          const e = await (async function (e, t, i, s, r = "MASTER") {
            return e.callWS({
              type: "homematicip_local/config/session_save",
              entry_id: t,
              interface_id: i,
              channel_address: s,
              paramset_key: r,
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
              Pe(this, { message: this._l("channel_config.save_success") }),
              await this._fetchSchema())
            : Object.keys(e.validation_errors).length > 0 &&
              ((this._validationErrors = e.validation_errors),
              Pe(this, {
                message: this._l("channel_config.validation_failed"),
              }));
        } else {
          const e = Object.fromEntries(this._pendingChanges),
            t = await (async function (e, t, i, s, r, a = "MASTER", n = !0) {
              return e.callWS({
                type: "homematicip_local/config/put_paramset",
                entry_id: t,
                interface_id: i,
                channel_address: s,
                paramset_key: a,
                values: r,
                validate: n,
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
              Pe(this, { message: this._l("channel_config.save_success") }),
              await this._fetchSchema())
            : Object.keys(t.validation_errors).length > 0 &&
              ((this._validationErrors = t.validation_errors),
              Pe(this, {
                message: this._l("channel_config.validation_failed"),
              }));
        }
      } catch (e) {
        (this._error = String(e)),
          Pe(this, { message: this._l("channel_config.save_failed") });
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
    if (
      !this._isDirty ||
      (await Me(this, {
        title: this._l("channel_config.unsaved_title"),
        text: this._l("channel_config.unsaved_warning"),
        confirmText: this._l("channel_config.discard"),
        dismissText: this._l("common.cancel"),
        destructive: !0,
      }))
    ) {
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
      this.dispatchEvent(
        new CustomEvent("back", { bubbles: !0, composed: !0 }),
      );
    }
  }
  render() {
    return this._loading
      ? V`<div class="loading">${this._l("common.loading")}</div>`
      : this._error && !this._schema
        ? V`<div class="error">${this._error}</div>`
        : V`
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

      <div class="config-header">
        ${this.deviceName ? V`<h2>${this.deviceName}</h2>` : K}
        <div class="device-info">
          ${this.channelAddress} —
          ${
            this._schema?.channel_type_label || this._schema?.channel_type || ""
          } —
          ${this.paramsetKey}
        </div>
      </div>

      ${this._error ? V`<div class="error">${this._error}</div>` : K}
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
          : K
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
            ${this._l(
              this._saving ? "channel_config.saving" : "channel_config.save",
            )}
          </button>
        </div>
      </div>
    `;
  }
  static {
    this.styles = [
      ue,
      n`
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
e([he({ attribute: !1 })], Be.prototype, "hass", void 0),
  e([he()], Be.prototype, "entryId", void 0),
  e([he()], Be.prototype, "interfaceId", void 0),
  e([he()], Be.prototype, "channelAddress", void 0),
  e([he()], Be.prototype, "channelType", void 0),
  e([he()], Be.prototype, "paramsetKey", void 0),
  e([he()], Be.prototype, "deviceName", void 0),
  e([pe()], Be.prototype, "_schema", void 0),
  e([pe()], Be.prototype, "_pendingChanges", void 0),
  e([pe()], Be.prototype, "_loading", void 0),
  e([pe()], Be.prototype, "_saving", void 0),
  e([pe()], Be.prototype, "_error", void 0),
  e([pe()], Be.prototype, "_validationErrors", void 0),
  e([pe()], Be.prototype, "_sessionActive", void 0),
  e([pe()], Be.prototype, "_canUndo", void 0),
  e([pe()], Be.prototype, "_canRedo", void 0),
  (Be = e([_e("hm-channel-config")], Be));
let Le = class extends oe {
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
    return Te(this.hass, e, t);
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
      await Me(this, {
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
          (Pe(this, {
            message: this._l("change_history.clear_success", {
              count: e.cleared,
            }),
          }),
          (this._entries = []),
          (this._total = 0));
      } catch {
        Pe(this, { message: this._l("channel_config.save_failed") });
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
    return V`
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

      <div class="history-header-bar">
        <h2>${this._l("change_history.title")}</h2>
      </div>

      ${
        this._loading
          ? V`<div class="loading">${this._l("common.loading")}</div>`
          : this._error
            ? V`<div class="error">${this._error}</div>`
            : 0 === this._entries.length
              ? V`<div class="empty-state">${this._l(
                  "change_history.empty",
                )}</div>`
              : this._renderEntries()
      }
      ${
        !this._loading && this._entries.length > 0
          ? V`
            <div class="action-bar">
              <button class="btn btn-secondary destructive" @click=${
                this._handleClear
              }>
                ${this._l("change_history.clear")}
              </button>
            </div>
          `
          : K
      }
    `;
  }
  _renderEntries() {
    return V`
      <div class="history-list">
        ${this._entries.map((e, t) => {
          const i = `${e.timestamp}-${t}`,
            s = this._expandedEntries.has(i),
            r = Object.keys(e.changes).length;
          return V`
            <div class="history-entry">
              <div class="history-entry-header" @click=${() =>
                this._toggleEntry(i)}>
                <div class="history-entry-info">
                  <div class="history-entry-time">${this._formatTimestamp(
                    e.timestamp,
                  )}</div>
                  <div class="history-entry-device">
                    ${e.device_name} (${e.device_model}) — ${e.channel_address}
                  </div>
                  <div class="history-entry-meta">
                    ${this._l("change_history.parameters_changed", {
                      count: r,
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
                  ? V`
                    <div class="history-details">
                      ${Object.entries(e.changes).map(
                        ([e, t]) => V`
                          <div class="change-row">
                            <span class="change-param">${e}</span>
                            <span class="change-values">
                              <span class="change-old">${String(t.old)}</span>
                              →
                              <span class="change-new">${String(t.new)}</span>
                            </span>
                          </div>
                        `,
                      )}
                    </div>
                  `
                  : K
              }
            </div>
          `;
        })}
      </div>
    `;
  }
  static {
    this.styles = [
      ue,
      n`
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
e([he({ attribute: !1 })], Le.prototype, "hass", void 0),
  e([he()], Le.prototype, "entryId", void 0),
  e([he()], Le.prototype, "filterDevice", void 0),
  e([pe()], Le.prototype, "_entries", void 0),
  e([pe()], Le.prototype, "_total", void 0),
  e([pe()], Le.prototype, "_loading", void 0),
  e([pe()], Le.prototype, "_error", void 0),
  e([pe()], Le.prototype, "_expandedEntries", void 0),
  (Le = e([_e("hm-change-history")], Le));
let Ue = class extends oe {
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
    return Te(this.hass, e, t);
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
          senderDeviceName: e.sender_device_name,
          senderDeviceModel: e.sender_device_model,
          senderChannelTypeLabel: e.sender_channel_type_label,
          receiverDeviceName: e.receiver_device_name,
          receiverDeviceModel: e.receiver_device_model,
          receiverChannelTypeLabel: e.receiver_channel_type_label,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  async _handleDelete(e) {
    if (
      await Me(this, {
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
          Pe(this, { message: this._l("device_links.delete_success") }),
          await this._fetchLinks();
      } catch {
        Pe(this, { message: this._l("device_links.delete_failed") });
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
    return V`
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

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
          ? V`<div class="loading">${this._l("common.loading")}</div>`
          : this._error
            ? V`<div class="error">${this._error}</div>`
            : 0 === this._links.length
              ? V`<div class="empty-state">${this._l(
                  "device_links.empty",
                )}</div>`
              : this._renderGroupedLinks()
      }
    `;
  }
  _renderGroupedLinks() {
    const e = this._groupByChannel(),
      t = [...e.keys()].sort((e, t) => parseInt(e) - parseInt(t));
    return V`
      ${t.map((t) => {
        const i = e.get(t);
        return V`
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
    return V`
      <div class="link-card ${t ? "outgoing" : "incoming"}">
        <div class="link-direction">
          <span class="direction-badge ${e.direction}">
            ${this._l(t ? "device_links.outgoing" : "device_links.incoming")}
          </span>
        </div>
        <div class="link-info">
          <div class="link-endpoints">
            <div class="link-endpoint-info">
              <span class="link-device-name">${e.sender_device_name}</span>
              <span class="link-device-detail">
                ${e.sender_device_model}${
                  e.sender_channel_type_label
                    ? V` · ${e.sender_channel_type_label}`
                    : K
                }
              </span>
              <span class="link-endpoint-address">${e.sender_address}</span>
            </div>
            <span class="link-arrow">→</span>
            <div class="link-endpoint-info">
              <span class="link-device-name">${e.receiver_device_name}</span>
              <span class="link-device-detail">
                ${e.receiver_device_model}${
                  e.receiver_channel_type_label
                    ? V` · ${e.receiver_channel_type_label}`
                    : K
                }
              </span>
              <span class="link-endpoint-address">${e.receiver_address}</span>
            </div>
          </div>
          ${e.name ? V`<div class="link-name">"${e.name}"</div>` : K}
        </div>
        <div class="link-actions">
          <button class="configure-button" @click=${() =>
            this._handleConfigure(e)}>
            ${this._l("device_links.configure")}
          </button>
          <button class="configure-button destructive" @click=${() =>
            this._handleDelete(e)}>
            ${this._l("device_links.delete")}
          </button>
        </div>
      </div>
    `;
  }
  static {
    this.styles = [
      ue,
      n`
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
        color: var(--secondary-text-color);
        font-size: 16px;
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

        .configure-button {
          width: 100%;
          text-align: center;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Ue.prototype, "hass", void 0),
  e([he()], Ue.prototype, "entryId", void 0),
  e([he()], Ue.prototype, "interfaceId", void 0),
  e([he()], Ue.prototype, "deviceAddress", void 0),
  e([he()], Ue.prototype, "deviceName", void 0),
  e([pe()], Ue.prototype, "_links", void 0),
  e([pe()], Ue.prototype, "_loading", void 0),
  e([pe()], Ue.prototype, "_error", void 0),
  (Ue = e([_e("hm-device-links")], Ue));
let Oe = class extends oe {
  constructor() {
    super(...arguments),
      (this.baseValue = 0),
      (this.factorValue = 0),
      (this.presets = []),
      (this.modified = !1),
      (this._isCustom = !1);
  }
  _l(e) {
    return Te(this.hass, e);
  }
  get _matchesPreset() {
    return this.presets.some(
      (e) => e.base === this.baseValue && e.factor === this.factorValue,
    );
  }
  _emitChange(e, t, i) {
    this.dispatchEvent(
      new CustomEvent("value-changed", {
        detail: { parameterId: e, value: t, currentValue: i },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _handlePresetChange(e) {
    const t = e.target.value;
    if ("custom" === t) return void (this._isCustom = !0);
    this._isCustom = !1;
    const [i, s] = t.split("-"),
      r = Number(i),
      a = Number(s);
    this._emitChange(this.baseParam.id, r, this.baseParam.current_value),
      this._emitChange(this.factorParam.id, a, this.factorParam.current_value);
  }
  _handleBaseChange(e) {
    const t = Number(e.target.value);
    this._emitChange(this.baseParam.id, t, this.baseParam.current_value);
  }
  _handleFactorChange(e) {
    const t = Number(e.target.value);
    this._emitChange(this.factorParam.id, t, this.factorParam.current_value);
  }
  render() {
    const e = this.baseParam.label.replace(/ Base$/, "").replace(/ Basis$/, ""),
      t = this._matchesPreset,
      i = this._isCustom && !t;
    return V`
      <div class="time-selector">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e} ${this.modified ? V`<span class="modified-dot"></span>` : K}
          </div>
          <div class="parameter-control">
            <select @change=${this._handlePresetChange}>
              ${this.presets.map(
                (e) => V`
                  <option
                    value="${e.base}-${e.factor}"
                    ?selected=${
                      e.base === this.baseValue && e.factor === this.factorValue
                    }
                  >
                    ${e.label}
                  </option>
                `,
              )}
              <option value="custom" ?selected=${!t}>
                ${this._l("link_config.custom_time")}
              </option>
            </select>
          </div>
        </div>
        ${
          i || !t
            ? V`
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
            `
            : K
        }
      </div>
    `;
  }
  static {
    this.styles = [
      ue,
      n`
      .time-selector {
        margin-bottom: 4px;
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

      select:focus {
        outline: none;
        border-color: var(--primary-color, #03a9f4);
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
        select {
          width: 100%;
          box-sizing: border-box;
        }
      }
    `,
    ];
  }
};
e([he({ attribute: !1 })], Oe.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Oe.prototype, "baseParam", void 0),
  e([he({ attribute: !1 })], Oe.prototype, "factorParam", void 0),
  e([he({ type: Number })], Oe.prototype, "baseValue", void 0),
  e([he({ type: Number })], Oe.prototype, "factorValue", void 0),
  e([he({ attribute: !1 })], Oe.prototype, "presets", void 0),
  e([he({ type: Boolean })], Oe.prototype, "modified", void 0),
  e([pe()], Oe.prototype, "_isCustom", void 0),
  (Oe = e([_e("hm-time-selector")], Oe));
let We = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.interfaceId = ""),
      (this.senderAddress = ""),
      (this.receiverAddress = ""),
      (this.senderDeviceName = ""),
      (this.senderDeviceModel = ""),
      (this.senderChannelTypeLabel = ""),
      (this.receiverDeviceName = ""),
      (this.receiverDeviceModel = ""),
      (this.receiverChannelTypeLabel = ""),
      (this._receiverSchema = null),
      (this._senderSchema = null),
      (this._receiverPendingChanges = new Map()),
      (this._senderPendingChanges = new Map()),
      (this._loading = !0),
      (this._saving = !1),
      (this._error = ""),
      (this._validationErrors = {}),
      (this._senderValidationErrors = {}),
      (this._profiles = null),
      (this._activeProfileId = 0),
      (this._selectedProfileId = 0),
      (this._activeKeypressTab = "short");
  }
  updated(e) {
    (e.has("senderAddress") || e.has("receiverAddress") || e.has("entryId")) &&
      this.entryId &&
      this.senderAddress &&
      this.receiverAddress &&
      this._fetchSchemas();
  }
  async _fetchSchemas() {
    (this._loading = !0),
      (this._error = ""),
      (this._receiverPendingChanges = new Map()),
      (this._senderPendingChanges = new Map()),
      (this._validationErrors = {}),
      (this._senderValidationErrors = {});
    try {
      const [e, t, i] = await Promise.all([
        be(
          this.hass,
          this.entryId,
          this.interfaceId,
          this.senderAddress,
          this.receiverAddress,
        ),
        be(
          this.hass,
          this.entryId,
          this.interfaceId,
          this.receiverAddress,
          this.senderAddress,
        ).catch(() => null),
        Se(
          this.hass,
          this.entryId,
          this.interfaceId,
          this.senderAddress,
          this.receiverAddress,
        ),
      ]);
      (this._receiverSchema = e),
        (this._senderSchema = t),
        (this._profiles = i?.profiles ?? null),
        (this._activeProfileId = i?.active_profile_id ?? 0),
        (this._selectedProfileId = this._activeProfileId);
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return Te(this.hass, e, t);
  }
  get _isDirty() {
    return (
      this._receiverPendingChanges.size > 0 ||
      this._senderPendingChanges.size > 0
    );
  }
  get _filteredReceiverSchema() {
    if (
      !this._receiverSchema ||
      !this._profiles ||
      0 === this._selectedProfileId
    )
      return this._receiverSchema;
    const e = this._profiles.find((e) => e.id === this._selectedProfileId);
    if (!e) return this._receiverSchema;
    const t = new Set(e.editable_params),
      i = this._receiverSchema.sections
        .map((e) => ({
          ...e,
          parameters: e.parameters.filter((e) => t.has(e.id)),
        }))
        .filter((e) => e.parameters.length > 0);
    return { ...this._receiverSchema, sections: i };
  }
  get _groupedReceiverParams() {
    const e = this._filteredReceiverSchema;
    if (!e) return null;
    const t = e.sections.flatMap((e) => e.parameters);
    return t.some((e) => e.keypress_group)
      ? {
          short: t.filter((e) => "short" === e.keypress_group),
          long: t.filter((e) => "long" === e.keypress_group),
          common: t.filter(
            (e) => "common" === e.keypress_group || !e.keypress_group,
          ),
        }
      : null;
  }
  _getEffectiveValue(e) {
    return this._receiverPendingChanges.has(e.id)
      ? this._receiverPendingChanges.get(e.id)
      : e.current_value;
  }
  _isModified(e) {
    return this._receiverPendingChanges.has(e.id);
  }
  _emitReceiverChange(e, t) {
    const i = this._findParameter(e),
      s = i?.current_value;
    t === s
      ? this._receiverPendingChanges.delete(e)
      : this._receiverPendingChanges.set(e, t),
      (this._receiverPendingChanges = new Map(this._receiverPendingChanges));
  }
  _handleProfileChange(e) {
    const t = parseInt(e.target.value, 10);
    if (((this._selectedProfileId = t), 0 === t || !this._profiles)) return;
    const i = this._profiles.find((e) => e.id === t);
    if (!i) return;
    const s = new Map();
    for (const [e, t] of Object.entries(i.fixed_params)) {
      const i = this._findParameter(e);
      i && i.current_value !== t && s.set(e, t);
    }
    for (const [e, t] of Object.entries(i.default_values)) {
      const i = this._findParameter(e);
      i && i.current_value !== t && s.set(e, t);
    }
    this._receiverPendingChanges = s;
  }
  _handleReceiverValueChanged(e) {
    const { parameterId: t, value: i, currentValue: s } = e.detail;
    i === s
      ? this._receiverPendingChanges.delete(t)
      : this._receiverPendingChanges.set(t, i),
      (this._receiverPendingChanges = new Map(this._receiverPendingChanges));
  }
  _handleSenderValueChanged(e) {
    const { parameterId: t, value: i, currentValue: s } = e.detail;
    i === s
      ? this._senderPendingChanges.delete(t)
      : this._senderPendingChanges.set(t, i),
      (this._senderPendingChanges = new Map(this._senderPendingChanges));
  }
  _handleDiscard() {
    (this._receiverPendingChanges = new Map()),
      (this._senderPendingChanges = new Map()),
      (this._validationErrors = {}),
      (this._senderValidationErrors = {}),
      (this._selectedProfileId = this._activeProfileId);
  }
  async _handleSave() {
    if (!this._isDirty || this._saving) return;
    const e = [
        ...this._receiverPendingChanges.entries(),
        ...this._senderPendingChanges.entries(),
      ],
      t = e.length,
      i = e
        .map(([e, t]) => {
          const i = this._findParameter(e);
          return `${i?.label ?? e}: ${i?.current_value ?? "?"} → ${t}`;
        })
        .join("\n");
    if (
      await Me(this, {
        title: this._l("link_config.confirm_save_title"),
        text: `${this._l("link_config.confirm_save_text", {
          count: t,
        })}\n\n${i}`,
        confirmText: this._l("common.save"),
        dismissText: this._l("common.cancel"),
      })
    ) {
      (this._saving = !0),
        (this._validationErrors = {}),
        (this._senderValidationErrors = {});
      try {
        const e = [];
        this._receiverPendingChanges.size > 0 &&
          e.push(
            xe(
              this.hass,
              this.entryId,
              this.interfaceId,
              this.senderAddress,
              this.receiverAddress,
              Object.fromEntries(this._receiverPendingChanges),
            ),
          ),
          this._senderPendingChanges.size > 0 &&
            e.push(
              xe(
                this.hass,
                this.entryId,
                this.interfaceId,
                this.receiverAddress,
                this.senderAddress,
                Object.fromEntries(this._senderPendingChanges),
              ),
            ),
          await Promise.all(e),
          (this._receiverPendingChanges = new Map()),
          (this._senderPendingChanges = new Map()),
          Pe(this, { message: this._l("link_config.save_success") }),
          await this._fetchSchemas();
      } catch (e) {
        (this._error = String(e)),
          Pe(this, { message: this._l("link_config.save_failed") });
      } finally {
        this._saving = !1;
      }
    }
  }
  _findParameter(e) {
    for (const t of [this._receiverSchema, this._senderSchema])
      if (t)
        for (const i of t.sections) {
          const t = i.parameters.find((t) => t.id === e);
          if (t) return t;
        }
  }
  async _handleBack() {
    (this._isDirty &&
      !(await Me(this, {
        title: this._l("link_config.unsaved_title"),
        text: this._l("link_config.unsaved_warning"),
        confirmText: this._l("link_config.discard"),
        dismissText: this._l("common.cancel"),
        destructive: !0,
      }))) ||
      this.dispatchEvent(
        new CustomEvent("back", { bubbles: !0, composed: !0 }),
      );
  }
  _hasReceiverParams() {
    return (this._filteredReceiverSchema?.sections.length ?? 0) > 0;
  }
  _hasSenderParams() {
    return (this._senderSchema?.sections.length ?? 0) > 0;
  }
  _renderProfileSelector() {
    if (!this._profiles) return K;
    const e = this._profiles.find((e) => e.id === this._selectedProfileId),
      t = e?.description || "";
    return V`
      <div class="profile-selector">
        <label class="profile-label">${this._l("link_config.profile")}</label>
        <select class="profile-select" @change=${this._handleProfileChange}>
          ${this._profiles.map(
            (e) => V`<option value=${e.id} ?selected=${
              e.id === this._selectedProfileId
            }>
                ${e.name}
              </option>`,
          )}
        </select>
        ${t ? V`<p class="profile-description">${t}</p>` : K}
      </div>
    `;
  }
  _renderParamList(e) {
    const t = new Map(),
      i = [];
    for (const s of e)
      if (s.time_pair_id && s.id.toUpperCase().endsWith("_TIME_BASE")) {
        const e = t.get(s.time_pair_id) ?? {};
        (e.base = s), t.set(s.time_pair_id, e);
      } else if (
        s.time_pair_id &&
        s.id.toUpperCase().endsWith("_TIME_FACTOR")
      ) {
        const e = t.get(s.time_pair_id) ?? {};
        (e.factor = s), t.set(s.time_pair_id, e);
      } else
        (s.hidden_by_default && 0 !== this._selectedProfileId) || i.push(s);
    return V`
      ${[...t.entries()].map(([, e]) =>
        e.base && e.factor
          ? V`
              <hm-time-selector
                .hass=${this.hass}
                .baseParam=${e.base}
                .factorParam=${e.factor}
                .baseValue=${this._getEffectiveValue(e.base)}
                .factorValue=${this._getEffectiveValue(e.factor)}
                .presets=${e.base.time_presets ?? []}
                .modified=${
                  this._isModified(e.base) || this._isModified(e.factor)
                }
                @value-changed=${this._handleReceiverValueChanged}
              ></hm-time-selector>
            `
          : K,
      )}
      ${i.map((e) =>
        e.display_as_percent && e.has_last_value
          ? this._renderLevelParam(e)
          : V`
              <hm-form-parameter
                .hass=${this.hass}
                .parameter=${e}
                .value=${this._getEffectiveValue(e)}
                .modified=${this._isModified(e)}
                @value-changed=${this._handleReceiverValueChanged}
              ></hm-form-parameter>
            `,
      )}
    `;
  }
  _renderLevelParam(e) {
    const t = this._getEffectiveValue(e),
      i = t > 1,
      s = i ? 100 : Math.round(100 * t);
    return V`
      <div class="level-param">
        <div class="parameter-row">
          <div class="parameter-label">
            ${e.label}
            ${this._isModified(e) ? V`<span class="modified-dot"></span>` : K}
          </div>
          <div class="parameter-control level-controls">
            <label class="last-value-toggle">
              <input
                type="checkbox"
                .checked=${i}
                @change=${(t) => {
                  this._emitReceiverChange(e.id, t.target.checked ? 1.005 : 1);
                }}
              />
              ${this._l("link_config.last_value")}
            </label>
            ${
              i
                ? K
                : V`
                  <div class="slider-group">
                    <input
                      type="range"
                      min="0"
                      max="100"
                      step="1"
                      .value=${String(s)}
                      @input=${(t) => {
                        const i = Number(t.target.value);
                        this._emitReceiverChange(e.id, i / 100);
                      }}
                    />
                    <span class="percent-display">${s}%</span>
                  </div>
                `
            }
          </div>
        </div>
      </div>
    `;
  }
  _renderReceiverParams() {
    const e = this._groupedReceiverParams;
    if (e) {
      const t = e.short.length > 0,
        i = e.long.length > 0,
        s = t && i;
      return V`
        <div class="param-section">
          <h3>${this._l("link_config.receiver_params")}</h3>
          ${
            s
              ? V`
                <div class="keypress-tabs">
                  <button
                    class="tab ${
                      "short" === this._activeKeypressTab ? "active" : ""
                    }"
                    @click=${() => {
                      this._activeKeypressTab = "short";
                    }}
                  >
                    ${this._l("link_config.short_keypress")}
                  </button>
                  <button
                    class="tab ${
                      "long" === this._activeKeypressTab ? "active" : ""
                    }"
                    @click=${() => {
                      this._activeKeypressTab = "long";
                    }}
                  >
                    ${this._l("link_config.long_keypress")}
                  </button>
                </div>
                <div class="keypress-params">
                  ${this._renderParamList(
                    "short" === this._activeKeypressTab ? e.short : e.long,
                  )}
                </div>
              `
              : t
                ? this._renderParamList(e.short)
                : i
                  ? this._renderParamList(e.long)
                  : K
          }
          ${
            e.common.length > 0
              ? V` <div class="common-params">${this._renderParamList(
                  e.common,
                )}</div> `
              : K
          }
        </div>
      `;
    }
    return V`
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
    `;
  }
  render() {
    return this._loading
      ? V`<div class="loading">${this._l("common.loading")}</div>`
      : !this._error || this._receiverSchema || this._senderSchema
        ? V`
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

      <div class="config-header">
        <h2>${this._l("link_config.title")}</h2>
        <div class="link-info-bar">
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.sender")}</span>
            ${
              this.senderDeviceName
                ? V`<span class="link-device-name">${this.senderDeviceName}</span>`
                : K
            }
            ${
              this.senderDeviceModel || this.senderChannelTypeLabel
                ? V`<span class="link-device-detail">
                  ${this.senderDeviceModel}${
                    this.senderChannelTypeLabel
                      ? V` &middot; ${this.senderChannelTypeLabel}`
                      : K
                  }
                </span>`
                : K
            }
            <span class="link-address">${this.senderAddress}</span>
          </div>
          <span class="link-direction-arrow">→</span>
          <div class="link-endpoint">
            <span class="link-label">${this._l("link_config.receiver")}</span>
            ${
              this.receiverDeviceName
                ? V`<span class="link-device-name">${this.receiverDeviceName}</span>`
                : K
            }
            ${
              this.receiverDeviceModel || this.receiverChannelTypeLabel
                ? V`<span class="link-device-detail">
                  ${this.receiverDeviceModel}${
                    this.receiverChannelTypeLabel
                      ? V` &middot; ${this.receiverChannelTypeLabel}`
                      : K
                  }
                </span>`
                : K
            }
            <span class="link-address">${this.receiverAddress}</span>
          </div>
        </div>
      </div>

      ${this._error ? V`<div class="error">${this._error}</div>` : K}
      ${this._renderProfileSelector()}
      ${this._hasReceiverParams() ? this._renderReceiverParams() : K}
      ${
        this._hasSenderParams()
          ? V`
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
          `
          : K
      }
      ${
        this._hasReceiverParams() || this._hasSenderParams()
          ? K
          : V`<div class="empty-state">${this._l(
              "link_config.no_params",
            )}</div>`
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
          ${this._l(this._saving ? "channel_config.saving" : "common.save")}
        </button>
      </div>
    `
        : V`<div class="error">${this._error}</div>`;
  }
  static {
    this.styles = [
      ue,
      n`
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
        font-size: 20px;
        color: var(--primary-color, #03a9f4);
        flex-shrink: 0;
      }

      .profile-selector {
        margin: 16px 0;
        padding: 12px;
        background: var(--secondary-background-color, #fafafa);
        border-radius: 8px;
      }

      .profile-label {
        display: block;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        color: var(--secondary-text-color);
        margin-bottom: 6px;
      }

      .profile-select {
        width: 100%;
        padding: 8px 12px;
        font-size: 14px;
        font-family: inherit;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
        cursor: pointer;
      }

      .profile-select:focus {
        outline: none;
        border-color: var(--primary-color, #03a9f4);
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
        font-family: inherit;
        font-weight: 500;
        background: none;
        border: none;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
        cursor: pointer;
        color: var(--secondary-text-color);
        transition:
          color 0.2s,
          border-color 0.2s;
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

      .last-value-toggle input[type="checkbox"] {
        width: 16px;
        height: 16px;
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
    `,
    ];
  }
};
e([he({ attribute: !1 })], We.prototype, "hass", void 0),
  e([he()], We.prototype, "entryId", void 0),
  e([he()], We.prototype, "interfaceId", void 0),
  e([he()], We.prototype, "senderAddress", void 0),
  e([he()], We.prototype, "receiverAddress", void 0),
  e([he()], We.prototype, "senderDeviceName", void 0),
  e([he()], We.prototype, "senderDeviceModel", void 0),
  e([he()], We.prototype, "senderChannelTypeLabel", void 0),
  e([he()], We.prototype, "receiverDeviceName", void 0),
  e([he()], We.prototype, "receiverDeviceModel", void 0),
  e([he()], We.prototype, "receiverChannelTypeLabel", void 0),
  e([pe()], We.prototype, "_receiverSchema", void 0),
  e([pe()], We.prototype, "_senderSchema", void 0),
  e([pe()], We.prototype, "_receiverPendingChanges", void 0),
  e([pe()], We.prototype, "_senderPendingChanges", void 0),
  e([pe()], We.prototype, "_loading", void 0),
  e([pe()], We.prototype, "_saving", void 0),
  e([pe()], We.prototype, "_error", void 0),
  e([pe()], We.prototype, "_validationErrors", void 0),
  e([pe()], We.prototype, "_senderValidationErrors", void 0),
  e([pe()], We.prototype, "_profiles", void 0),
  e([pe()], We.prototype, "_activeProfileId", void 0),
  e([pe()], We.prototype, "_selectedProfileId", void 0),
  e([pe()], We.prototype, "_activeKeypressTab", void 0),
  (We = e([_e("hm-link-config")], We));
let je = class extends oe {
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
      const e = await me(this.hass, this.entryId);
      this._device = e.find((e) => e.address === this.deviceAddress) ?? null;
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return Te(this.hass, e, t);
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
      (this._linkableChannels = await (async function (e, t, i, s, r) {
        return (
          await e.callWS({
            type: "homematicip_local/config/get_linkable_channels",
            entry_id: t,
            interface_id: i,
            channel_address: s,
            role: r,
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
      await (async function (e, t, i, s, r) {
        return e.callWS({
          type: "homematicip_local/config/add_link",
          entry_id: t,
          sender_channel_address: i,
          receiver_channel_address: s,
          ...(r && { name: r }),
        });
      })(this.hass, this.entryId, e, t, this._linkName || void 0),
        Pe(this, { message: this._l("add_link.create_success") }),
        this.dispatchEvent(
          new CustomEvent("link-created", { bubbles: !0, composed: !0 }),
        );
    } catch {
      Pe(this, { message: this._l("add_link.create_failed") });
    } finally {
      this._loading = !1;
    }
  }
  render() {
    return this._loading && !this._device
      ? V`<div class="loading">${this._l("common.loading")}</div>`
      : V`
      <button class="back-button" @click=${this._handleBack}>
        ◂ ${this._l(
          "select-channel" === this._step ? "common.back" : "add_link.back",
        )}
      </button>

      <div class="wizard-header">
        <h2>${this._l("add_link.title")}</h2>
      </div>

      ${this._error ? V`<div class="error">${this._error}</div>` : K}
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
    return V`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_channel")}</div>
        <div class="step-description">${this._l(
          "add_link.select_channel",
        )}</div>

        <div class="radio-list">
          ${
            0 === e.length
              ? V`<div class="empty-state">${this._l(
                  "add_link.no_compatible",
                )}</div>`
              : e.map((e) => {
                  const t = e.address.split(":").pop() ?? "",
                    i = this._selectedChannel === e.address;
                  return V`
                  <div
                    class="radio-option ${i ? "selected" : ""}"
                    @click=${() => this._handleSelectChannel(e.address)}
                  >
                    <input type="radio" name="channel" .checked=${i} />
                    <div class="radio-content">
                      <div class="radio-title">
                        ${this._l("device_detail.channel")} ${t}: ${
                          e.channel_type_label
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
            ? V`
              <div class="wizard-actions">
                <button
                  class="btn btn-primary"
                  ?disabled=${!this._selectedChannel}
                  @click=${this._handleNextToSelectPeer}
                >
                  ${this._l("add_link.next")} ▸
                </button>
              </div>
            `
            : K
        }
      </div>
    `;
  }
  _renderStepPeer() {
    return V`
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
            ? V`<div class="loading">${this._l("common.loading")}</div>`
            : V`
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
                    ? V`<div class="empty-state">${this._l(
                        "add_link.no_compatible",
                      )}</div>`
                    : this._filteredChannels.map((e) => {
                        const t = this._selectedPeer === e.address;
                        return V`
                        <div
                          class="radio-option ${t ? "selected" : ""}"
                          @click=${() => this._handleSelectPeer(e.address)}
                        >
                          <input type="radio" name="peer" .checked=${t} />
                          <div class="radio-content">
                            <div class="radio-title">${e.device_name} (${
                              e.device_model
                            })</div>
                            <div class="radio-subtitle">
                              ${e.address} — ${e.channel_type_label}
                            </div>
                          </div>
                        </div>
                      `;
                      })
                }
              </div>

              ${
                this._filteredChannels.length > 0
                  ? V`
                    <div class="wizard-actions">
                      <button
                        class="btn btn-primary"
                        ?disabled=${!this._selectedPeer}
                        @click=${this._handleNextToConfirm}
                      >
                        ${this._l("add_link.next")} ▸
                      </button>
                    </div>
                  `
                  : K
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
    return V`
      <div class="wizard-step">
        <div class="step-indicator">${this._l("add_link.step_confirm")}</div>

        <div class="link-summary">
          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l(
              "link_config.sender",
            )}</div>
            <div class="link-endpoint-address">${e}</div>
            <div class="link-endpoint-name">${i}</div>
          </div>

          <div class="link-direction-arrow">→</div>

          <div class="link-endpoint">
            <div class="link-endpoint-label">${this._l(
              "link_config.receiver",
            )}</div>
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
          <button class="btn btn-primary" ?disabled=${this._loading} @click=${
            this._handleCreate
          }>
            ${this._l(this._loading ? "common.loading" : "add_link.create")}
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
      ue,
      n`
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
function Ve(e) {
  return (t) => (customElements.get(e) || customElements.define(e, t), t);
}
e([he({ attribute: !1 })], je.prototype, "hass", void 0),
  e([he()], je.prototype, "entryId", void 0),
  e([he()], je.prototype, "interfaceId", void 0),
  e([he()], je.prototype, "deviceAddress", void 0),
  e([pe()], je.prototype, "_step", void 0),
  e([pe()], je.prototype, "_device", void 0),
  e([pe()], je.prototype, "_selectedChannel", void 0),
  e([pe()], je.prototype, "_selectedRole", void 0),
  e([pe()], je.prototype, "_selectedPeer", void 0),
  e([pe()], je.prototype, "_linkName", void 0),
  e([pe()], je.prototype, "_linkableChannels", void 0),
  e([pe()], je.prototype, "_filteredChannels", void 0),
  e([pe()], je.prototype, "_searchQuery", void 0),
  e([pe()], je.prototype, "_loading", void 0),
  e([pe()], je.prototype, "_error", void 0),
  (je = e([_e("hm-add-link")], je));
let Fe = class {
  constructor(e) {}
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AT(e, t, i) {
    (this._$Ct = e), (this._$AM = t), (this._$Ci = i);
  }
  _$AS(e, t) {
    return this.update(e, t);
  }
  update(e, t) {
    return this.render(...t);
  }
};
const { I: Ke } = re,
  He = (e) => e,
  Ye = () => document.createComment(""),
  Ge = (e, t, i) => {
    const s = e._$AA.parentNode,
      r = void 0 === t ? e._$AB : t._$AA;
    if (void 0 === i) {
      const t = s.insertBefore(Ye(), r),
        a = s.insertBefore(Ye(), r);
      i = new Ke(t, a, e, e.options);
    } else {
      const t = i._$AB.nextSibling,
        a = i._$AM,
        n = a !== e;
      if (n) {
        let t;
        i._$AQ?.(e),
          (i._$AM = e),
          void 0 !== i._$AP && (t = e._$AU) !== a._$AU && i._$AP(t);
      }
      if (t !== r || n) {
        let e = i._$AA;
        for (; e !== t; ) {
          const t = He(e).nextSibling;
          He(s).insertBefore(e, r), (e = t);
        }
      }
    }
    return i;
  },
  Ze = (e, t, i = e) => (e._$AI(t, i), e),
  Je = {},
  qe = (e, t = Je) => (e._$AH = t),
  Qe = (e) => {
    e._$AR(), e._$AA.remove();
  },
  Xe = (e, t, i) => {
    const s = new Map();
    for (let r = t; r <= i; r++) s.set(e[r], r);
    return s;
  },
  et = (
    (e) =>
    (...t) => ({ _$litDirective$: e, values: t })
  )(
    class extends Fe {
      constructor(e) {
        if ((super(e), 2 !== e.type))
          throw Error("repeat() can only be used in text expressions");
      }
      dt(e, t, i) {
        let s;
        void 0 === i ? (i = t) : void 0 !== t && (s = t);
        const r = [],
          a = [];
        let n = 0;
        for (const t of e) (r[n] = s ? s(t, n) : n), (a[n] = i(t, n)), n++;
        return { values: a, keys: r };
      }
      render(e, t, i) {
        return this.dt(e, t, i).values;
      }
      update(e, [t, i, s]) {
        const r = ((e) => e._$AH)(e),
          { values: a, keys: n } = this.dt(t, i, s);
        if (!Array.isArray(r)) return (this.ut = n), a;
        const o = (this.ut ??= []),
          d = [];
        let l,
          c,
          h = 0,
          p = r.length - 1,
          _ = 0,
          u = a.length - 1;
        for (; h <= p && _ <= u; )
          if (null === r[h]) h++;
          else if (null === r[p]) p--;
          else if (o[h] === n[_]) (d[_] = Ze(r[h], a[_])), h++, _++;
          else if (o[p] === n[u]) (d[u] = Ze(r[p], a[u])), p--, u--;
          else if (o[h] === n[u])
            (d[u] = Ze(r[h], a[u])), Ge(e, d[u + 1], r[h]), h++, u--;
          else if (o[p] === n[_])
            (d[_] = Ze(r[p], a[_])), Ge(e, r[h], r[p]), p--, _++;
          else if (
            (void 0 === l && ((l = Xe(n, _, u)), (c = Xe(o, h, p))),
            l.has(o[h]))
          )
            if (l.has(o[p])) {
              const t = c.get(n[_]),
                i = void 0 !== t ? r[t] : null;
              if (null === i) {
                const t = Ge(e, r[h]);
                Ze(t, a[_]), (d[_] = t);
              } else (d[_] = Ze(i, a[_])), Ge(e, r[h], i), (r[t] = null);
              _++;
            } else Qe(r[p]), p--;
          else Qe(r[h]), h++;
        for (; _ <= u; ) {
          const t = Ge(e, d[u + 1]);
          Ze(t, a[_]), (d[_++] = t);
        }
        for (; h <= p; ) {
          const e = r[h++];
          null !== e && Qe(e);
        }
        return (this.ut = n), qe(e, d), F;
      }
    },
  ),
  tt = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
  ],
  it = [
    "fixed_time",
    "astro",
    "fixed_if_before_astro",
    "astro_if_before_fixed",
    "fixed_if_after_astro",
    "astro_if_after_fixed",
    "earliest",
    "latest",
  ],
  st = {
    switch: {
      levelType: "binary",
      hasLevel2: !1,
      hasDuration: !0,
      hasRampTime: !1,
    },
    light: {
      levelType: "percentage",
      hasLevel2: !1,
      hasDuration: !0,
      hasRampTime: !0,
    },
    cover: {
      levelType: "percentage",
      hasLevel2: !0,
      hasDuration: !1,
      hasRampTime: !1,
    },
    valve: {
      levelType: "percentage",
      hasLevel2: !1,
      hasDuration: !0,
      hasRampTime: !1,
    },
  },
  rt = ["ms", "s", "min", "h"];
function at(e) {
  const [t, i] = e.split(":").map(Number);
  return 60 * t + i;
}
function nt(e) {
  const t = e % 60;
  return `${Math.floor(e / 60)
    .toString()
    .padStart(2, "0")}:${t.toString().padStart(2, "0")}`;
}
function ot(e, t = "24") {
  if ("24" === t) return e;
  const [i, s] = e.split(":");
  let r = parseInt(i, 10);
  if (24 === r) return "12:00 AM";
  const a = r >= 12 ? "PM" : "AM";
  return 0 === r ? (r = 12) : r > 12 && (r -= 12), `${r}:${s || "00"} ${a}`;
}
function dt(e) {
  return e < 10
    ? "#2b9af9"
    : e < 14
      ? "#40c4ff"
      : e < 17
        ? "#26c6da"
        : e < 19
          ? "#66bb6a"
          : e < 21
            ? "#9ccc65"
            : e < 23
              ? "#ffb74d"
              : e < 25
                ? "#ff8100"
                : "#f4511e";
}
function lt(e) {
  const { base_temperature: t, periods: i } = e,
    s = [],
    r = [...i].sort((e, t) => at(e.starttime) - at(t.starttime));
  for (let e = 0; e < r.length; e++) {
    const t = r[e];
    s.push({
      startTime: t.starttime,
      startMinutes: at(t.starttime),
      endTime: t.endtime,
      endMinutes: at(t.endtime),
      temperature: t.temperature,
      slot: e + 1,
    });
  }
  return { blocks: s, baseTemperature: t };
}
function ct(e, t) {
  const i = [],
    s = [...e].sort((e, t) => e.startMinutes - t.startMinutes);
  for (const e of s)
    i.push({
      starttime: e.startTime,
      endtime: e.endTime,
      temperature: e.temperature,
    });
  return { base_temperature: t, periods: i };
}
function ht(e) {
  if (0 === e.length) return [];
  const t = [...e].sort((e, t) => e.startMinutes - t.startMinutes),
    i = [];
  let s = { ...t[0] };
  for (let e = 1; e < t.length; e++) {
    const r = t[e];
    s.endMinutes === r.startMinutes && s.temperature === r.temperature
      ? (s = { ...s, endTime: r.endTime, endMinutes: r.endMinutes })
      : (i.push(s), (s = { ...r }));
  }
  return i.push(s), i.map((e, t) => ({ ...e, slot: t + 1 }));
}
function pt(e, t) {
  if (0 === e.length)
    return [
      {
        startTime: "00:00",
        startMinutes: 0,
        endTime: "24:00",
        endMinutes: 1440,
        temperature: t,
        slot: 1,
      },
    ];
  const i = [...e].sort((e, t) => e.startMinutes - t.startMinutes),
    s = [];
  let r = 0;
  for (const e of i)
    e.startMinutes > r &&
      s.push({
        startTime: nt(r),
        startMinutes: r,
        endTime: e.startTime,
        endMinutes: e.startMinutes,
        temperature: t,
        slot: s.length + 1,
      }),
      s.push({ ...e, slot: s.length + 1 }),
      (r = e.endMinutes);
  return (
    r < 1440 &&
      s.push({
        startTime: nt(r),
        startMinutes: r,
        endTime: "24:00",
        endMinutes: 1440,
        temperature: t,
        slot: s.length + 1,
      }),
    ht(s)
  );
}
function _t(e) {
  return [...e]
    .sort((e, t) => e.startMinutes - t.startMinutes)
    .map((e, t) => ({ ...e, slot: t + 1 }));
}
function ut(e) {
  return Boolean(
    Array.isArray(e.weekdays) &&
      e.weekdays.length > 0 &&
      Array.isArray(e.target_channels) &&
      e.target_channels.length > 0,
  );
}
function vt(e) {
  return "fixed_time" !== e;
}
const mt = /^(\d+(?:\.\d+)?)\s*(ms|s|min|h)$/;
function gt(e) {
  const t = e.trim().match(mt);
  return t ? { value: parseFloat(t[1]), unit: t[2] } : null;
}
function ft(e, t) {
  return `${e}${t}`;
}
function yt(e) {
  return mt.test(e.trim());
}
function bt(e) {
  const t = {
    weekdays: e.weekdays,
    time: e.time,
    target_channels: e.target_channels,
    level: e.level,
  };
  return (
    "fixed_time" !== e.condition && (t.condition = e.condition),
    null !== e.astro_type && (t.astro_type = e.astro_type),
    0 !== e.astro_offset_minutes &&
      (t.astro_offset_minutes = e.astro_offset_minutes),
    null !== e.level_2 && (t.level_2 = e.level_2),
    null !== e.duration && (t.duration = e.duration),
    null !== e.ramp_time && (t.ramp_time = e.ramp_time),
    t
  );
}
function xt(e) {
  const t = {};
  for (const [i, s] of Object.entries(e)) t[i] = bt(s);
  return t;
}
function kt(e, t = 5, i = 30.5) {
  const { base_temperature: s, periods: r } = e;
  if (s < t || s > i)
    return {
      key: "temperatureOutOfRange",
      params: { block: "base", min: `${t}`, max: `${i}` },
    };
  let a = 0;
  for (let e = 0; e < r.length; e++) {
    const s = r[e];
    if (!s.starttime || !s.endtime || void 0 === s.temperature)
      return { key: "slotMissingValues", params: { slot: `${e + 1}` } };
    const n = at(s.starttime),
      o = at(s.endtime);
    if (o <= n)
      return { key: "blockEndBeforeStart", params: { block: `${e + 1}` } };
    if (n < a)
      return {
        key: "slotTimeBackwards",
        params: { slot: `${e + 1}`, time: s.starttime },
      };
    if (s.temperature < t || s.temperature > i)
      return {
        key: "temperatureOutOfRange",
        params: { block: `${e + 1}`, min: `${t}`, max: `${i}` },
      };
    a = o;
  }
  return null;
}
const $t = n`
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
  }

  .weekday-label {
    font-weight: 500;
    font-size: 14px;
  }

  .weekday-actions {
    display: flex;
    gap: 4px;
  }

  .copy-btn,
  .paste-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    padding: 2px 4px;
    border-radius: 3px;
    transition: background-color 0.2s;
    opacity: 0.7;
  }

  .copy-btn:hover,
  .paste-btn:not(:disabled):hover {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.2);
  }

  .copy-btn.active {
    opacity: 1;
    background-color: rgba(255, 255, 255, 0.3);
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

  .paste-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
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
      gap: 6px;
    }

    .copy-btn,
    .paste-btn {
      font-size: 16px;
      padding: 6px 8px;
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

    .weekday-label {
      font-size: 11px;
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

    /* Disable hover effects, use active states */
    .copy-btn:hover,
    .paste-btn:not(:disabled):hover {
      opacity: 1;
      background-color: transparent;
    }

    .copy-btn:active,
    .paste-btn:not(:disabled):active {
      background-color: rgba(255, 255, 255, 0.3);
    }
  }
`;
var wt = function (e, t, i, s) {
  var r,
    a = arguments.length,
    n =
      a < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    n = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (r = e[o]) && (n = (a < 3 ? r(n) : a > 3 ? r(t, i, n) : r(t, i)) || n);
  return a > 3 && n && Object.defineProperty(t, i, n), n;
};
let St = class extends oe {
  constructor() {
    super(...arguments),
      (this.editable = !1),
      (this.showTemperature = !0),
      (this.showGradient = !1),
      (this.temperatureUnit = "°C"),
      (this.hourFormat = "24"),
      (this.editorOpen = !1),
      (this._currentTimePercent = 0),
      (this._currentTimeMinutes = 0);
  }
  connectedCallback() {
    super.connectedCallback(),
      this._updateCurrentTime(),
      (this._timeUpdateInterval = window.setInterval(() => {
        this._updateCurrentTime();
      }, 6e4));
  }
  disconnectedCallback() {
    super.disconnectedCallback(),
      void 0 !== this._timeUpdateInterval &&
        (clearInterval(this._timeUpdateInterval),
        (this._timeUpdateInterval = void 0));
  }
  willUpdate(e) {
    super.willUpdate(e);
  }
  _updateCurrentTime() {
    const e = new Date(),
      t = 60 * e.getHours() + e.getMinutes();
    (this._currentTimePercent = (t / 1440) * 100),
      (this._currentTimeMinutes = t);
    const i = e.getDay();
    this._currentWeekday = [
      "SUNDAY",
      "MONDAY",
      "TUESDAY",
      "WEDNESDAY",
      "THURSDAY",
      "FRIDAY",
      "SATURDAY",
    ][i];
  }
  _isBlockActive(e, t) {
    return (
      !(!this._currentWeekday || this._currentWeekday !== e) &&
      this._currentTimeMinutes >= t.startMinutes &&
      this._currentTimeMinutes < t.endMinutes
    );
  }
  _getTimeLabels() {
    const e = [];
    for (let t = 0; t <= 24; t += 3) {
      const i = `${t.toString().padStart(2, "0")}:00`;
      e.push({
        hour: t,
        label: ot(i, this.hourFormat),
        position: (t / 24) * 100,
      });
    }
    return e;
  }
  _formatTimeDisplay(e) {
    return ot(e, this.hourFormat);
  }
  _getBaseTemperature(e) {
    if (this.scheduleData) {
      const t = this.scheduleData[e];
      if (t) {
        const { baseTemperature: e } = lt(t);
        return e;
      }
    }
    return 20;
  }
  _getParsedBlocks(e) {
    if (this.scheduleData) {
      const t = this.scheduleData[e];
      if (!t) return [];
      const { blocks: i } = lt(t);
      return i;
    }
    return [];
  }
  _getWeekdayLabel(e) {
    return this.translations?.weekdayShortLabels[e] ?? e.slice(0, 2);
  }
  _handleWeekdayClick(e) {
    this.editable &&
      this.dispatchEvent(
        new CustomEvent("weekday-click", {
          detail: { weekday: e },
          bubbles: !0,
          composed: !0,
        }),
      );
  }
  _handleCopy(e, t) {
    t.stopPropagation(),
      this.dispatchEvent(
        new CustomEvent("copy-schedule", {
          detail: { weekday: e },
          bubbles: !0,
          composed: !0,
        }),
      );
  }
  _handlePaste(e, t) {
    t.stopPropagation(),
      this.dispatchEvent(
        new CustomEvent("paste-schedule", {
          detail: { weekday: e },
          bubbles: !0,
          composed: !0,
        }),
      );
  }
  render() {
    return this.scheduleData
      ? V`
      <div class="schedule-container">
        <!-- Empty cell for time-axis header alignment -->
        <div class="time-axis-header"></div>

        <!-- Weekday headers -->
        ${et(
          tt,
          (e) => `header-${e}`,
          (e) => {
            const t = this.copiedWeekday === e;
            return V`
              <div class="weekday-header">
                <div class="weekday-label">${this._getWeekdayLabel(e)}</div>
                ${
                  this.editable
                    ? V`
                      <div class="weekday-actions">
                        <button
                          class="copy-btn ${t ? "active" : ""}"
                          @click=${(t) => this._handleCopy(e, t)}
                          title="${this.translations?.copySchedule ?? ""}"
                        >
                          📋
                        </button>
                        <button
                          class="paste-btn"
                          @click=${(t) => this._handlePaste(e, t)}
                          title="${this.translations?.pasteSchedule ?? ""}"
                          ?disabled=${!this.copiedWeekday}
                        >
                          📄
                        </button>
                      </div>
                    `
                    : ""
                }
              </div>
            `;
          },
        )}

        <!-- Time axis labels -->
        <div class="time-axis-labels">
          ${et(
            this._getTimeLabels(),
            (e) => e.hour,
            (e) => V`
              <div class="time-label" style="top: ${e.position}%">${e.label}</div>
            `,
          )}
        </div>

        <!-- Time blocks content wrapper (for correct indicator positioning) -->
        <div class="schedule-content">
          ${et(
            tt,
            (e) => `${e}-${this.currentProfile}-${this.scheduleDataHash}`,
            (e) => {
              const t = this._getParsedBlocks(e),
                i = this._getBaseTemperature(e),
                s = pt(t, i);
              return V`
                <div
                  class="time-blocks ${this.editable ? "editable" : ""}"
                  @click=${() => this._handleWeekdayClick(e)}
                >
                  ${et(
                    s,
                    (e) => `${e.slot}-${e.startMinutes}-${this.currentProfile}`,
                    (r, a) => {
                      const n = this._isBlockActive(e, r),
                        o =
                          r.temperature === i &&
                          !t.some(
                            (e) =>
                              e.startMinutes === r.startMinutes &&
                              e.endMinutes === r.endMinutes,
                          );
                      let d;
                      if (o)
                        d =
                          "background-color: var(--secondary-background-color, #e0e0e0);";
                      else if (this.showGradient) {
                        d = `background: ${(function (e, t, i) {
                          const s = dt(e);
                          return null === t && null === i
                            ? s
                            : null !== t && null === i
                              ? `linear-gradient(to bottom, ${dt(t)}, ${s})`
                              : null === t && null !== i
                                ? `linear-gradient(to bottom, ${s}, ${dt(i)})`
                                : `linear-gradient(to bottom, ${dt(
                                    t,
                                  )}, ${s} 50%, ${dt(i)})`;
                        })(
                          r.temperature,
                          a > 0 ? s[a - 1].temperature : null,
                          a < s.length - 1 ? s[a + 1].temperature : null,
                        )};`;
                      } else d = `background-color: ${dt(r.temperature)};`;
                      return V`
                        <div
                          class="time-block ${n ? "active" : ""} ${
                            o ? "base-temp-block" : ""
                          }"
                          style="
                              height: ${
                                ((r.endMinutes - r.startMinutes) / 1440) * 100
                              }%;
                              ${d}
                            "
                        >
                          ${
                            this.showTemperature
                              ? V`<span class="temperature"
                                >${r.temperature.toFixed(1)}°</span
                              >`
                              : ""
                          }
                          <div class="time-block-tooltip">
                            <div class="tooltip-time">
                              ${this._formatTimeDisplay(r.startTime)} -
                              ${this._formatTimeDisplay(r.endTime)}
                            </div>
                            <div class="tooltip-temp">
                              ${(function (e, t = "°C") {
                                return `${e.toFixed(1)}${t}`;
                              })(r.temperature, this.temperatureUnit)}
                            </div>
                          </div>
                        </div>
                      `;
                    },
                  )}
                </div>
              `;
            },
          )}

          <!-- Current time indicator line (hidden when editor is open) -->
          ${
            this.editorOpen
              ? ""
              : V`<div
                class="current-time-indicator"
                style="top: ${this._currentTimePercent}%"
              ></div>`
          }
        </div>
      </div>

      ${
        this.editable
          ? V`<div class="hint">${this.translations?.clickToEdit ?? ""}</div>`
          : ""
      }
    `
      : V``;
  }
  static {
    this.styles = $t;
  }
};
wt([he({ attribute: !1 })], St.prototype, "scheduleData", void 0),
  wt([he({ type: Boolean })], St.prototype, "editable", void 0),
  wt([he({ type: Boolean })], St.prototype, "showTemperature", void 0),
  wt([he({ type: Boolean })], St.prototype, "showGradient", void 0),
  wt([he({ type: String })], St.prototype, "temperatureUnit", void 0),
  wt([he({ type: String })], St.prototype, "hourFormat", void 0),
  wt([he({ attribute: !1 })], St.prototype, "translations", void 0),
  wt([he({ type: String })], St.prototype, "copiedWeekday", void 0),
  wt([he({ type: Boolean })], St.prototype, "editorOpen", void 0),
  wt([he({ type: String })], St.prototype, "currentProfile", void 0),
  wt([he({ type: String })], St.prototype, "scheduleDataHash", void 0),
  wt([pe()], St.prototype, "_currentTimePercent", void 0),
  wt([pe()], St.prototype, "_currentTimeMinutes", void 0),
  wt([pe()], St.prototype, "_currentWeekday", void 0),
  (St = wt([Ve("hmip-schedule-grid")], St));
const Et = n`
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
    gap: 8px;
    align-items: center;
  }

  .undo-btn,
  .redo-btn,
  .close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--secondary-text-color);
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition:
      background-color 0.2s,
      opacity 0.2s;
  }

  .undo-btn:hover:not(:disabled),
  .redo-btn:hover:not(:disabled),
  .close-btn:hover {
    background-color: var(--divider-color);
  }

  .undo-btn:disabled,
  .redo-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .validation-warnings {
    background-color: rgba(255, 152, 0, 0.1);
    border: 1px solid rgba(255, 152, 0, 0.3);
    border-radius: 4px;
    padding: 12px;
    margin: 12px 0;
  }

  .warnings-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--primary-text-color);
  }

  .warning-icon {
    font-size: 18px;
  }

  .warnings-title {
    font-size: 14px;
  }

  .warnings-list {
    margin: 0;
    padding-left: 28px;
    list-style-type: disc;
  }

  .warning-item {
    color: var(--secondary-text-color);
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

  .slot-edit-btn,
  .slot-save-btn,
  .slot-cancel-btn {
    padding: 4px 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 12px;
    cursor: pointer;
    white-space: nowrap;
  }

  .slot-edit-btn:hover,
  .slot-save-btn:hover,
  .slot-cancel-btn:hover {
    background-color: var(--divider-color);
  }

  .slot-save-btn {
    background-color: var(--primary-color);
    color: var(--text-primary-color);
    border-color: var(--primary-color);
  }

  .slot-cancel-btn {
    background-color: var(--error-color, #e74c3c);
    color: white;
    border-color: var(--error-color, #e74c3c);
  }

  .slot-edit-btn:disabled,
  .remove-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
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
    background: none;
    border: none;
    cursor: pointer;
    font-size: 18px;
    padding: 4px;
  }

  .remove-btn:hover {
    opacity: 0.7;
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
    padding: 10px 16px;
    background-color: var(--primary-color);
    color: var(--text-primary-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    width: 100%;
  }

  .add-btn:hover {
    opacity: 0.9;
  }

  .editor-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--divider-color);
  }

  .cancel-btn,
  .save-btn {
    padding: 10px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
  }

  .cancel-btn {
    background-color: var(--divider-color);
    color: var(--primary-text-color);
  }

  .save-btn {
    background-color: var(--primary-color);
    color: var(--text-primary-color);
  }

  .cancel-btn:hover,
  .save-btn:hover {
    opacity: 0.9;
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

    .undo-btn,
    .redo-btn,
    .close-btn {
      width: 44px;
      height: 44px;
      font-size: 28px;
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

    .remove-btn {
      font-size: 22px;
      padding: 8px;
      min-width: 44px;
      min-height: 44px;
    }

    .add-btn {
      padding: 14px 16px;
      font-size: 16px;
      min-height: 48px;
    }

    .editor-footer {
      flex-direction: column-reverse;
      gap: 8px;
    }

    .cancel-btn,
    .save-btn {
      width: 100%;
      padding: 14px 24px;
      font-size: 16px;
      min-height: 48px;
    }

    .validation-warnings {
      padding: 10px;
      margin: 10px 0;
    }

    .warnings-title {
      font-size: 13px;
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

  /* Touch-specific optimizations */
  @media (hover: none) and (pointer: coarse) {
    .undo-btn:hover:not(:disabled),
    .redo-btn:hover:not(:disabled),
    .close-btn:hover,
    .add-btn:hover,
    .cancel-btn:hover,
    .save-btn:hover,
    .remove-btn:hover {
      opacity: 1;
      background-color: transparent;
    }

    .undo-btn:active:not(:disabled),
    .redo-btn:active:not(:disabled),
    .close-btn:active {
      background-color: var(--divider-color);
    }

    .add-btn:active,
    .save-btn:active {
      opacity: 0.85;
    }

    .cancel-btn:active {
      opacity: 0.85;
    }

    .remove-btn:active {
      opacity: 0.5;
    }
  }
`;
var Ct = function (e, t, i, s) {
  var r,
    a = arguments.length,
    n =
      a < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    n = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (r = e[o]) && (n = (a < 3 ? r(n) : a > 3 ? r(t, i, n) : r(t, i)) || n);
  return a > 3 && n && Object.defineProperty(t, i, n), n;
};
let At = class extends oe {
  constructor() {
    super(),
      (this.open = !1),
      (this.minTemp = 5),
      (this.maxTemp = 30.5),
      (this.tempStep = 0.5),
      (this.temperatureUnit = "°C"),
      (this.hourFormat = "24"),
      (this._validationWarnings = []),
      (this._historyStack = []),
      (this._historyIndex = -1),
      (this._keyDownHandler = this._handleKeyDown.bind(this));
  }
  connectedCallback() {
    super.connectedCallback(),
      window.addEventListener("keydown", this._keyDownHandler);
  }
  disconnectedCallback() {
    super.disconnectedCallback(),
      window.removeEventListener("keydown", this._keyDownHandler);
  }
  willUpdate(e) {
    if (
      (super.willUpdate(e),
      (e.has("open") || e.has("weekday")) && this.open && this.weekday)
    ) {
      const t = e.get("open"),
        i = e.get("weekday");
      ((!t && this.open) || (this.open && i !== this.weekday)) &&
        this._initializeEditor(this.weekday);
    }
  }
  _initializeEditor(e) {
    (this._editingWeekday = e),
      (this._editingBlocks = this._getParsedBlocks(e)),
      (this._editingSlotIndex = void 0),
      (this._editingSlotData = void 0);
    const t = this.scheduleData?.[e];
    if (t) {
      const { baseTemperature: e } = lt(t);
      this._editingBaseTemperature = e;
    } else this._editingBaseTemperature = 20;
    (this._historyStack = [JSON.parse(JSON.stringify(this._editingBlocks))]),
      (this._historyIndex = 0),
      this._updateValidationWarnings();
  }
  _getParsedBlocks(e) {
    if (this.scheduleData) {
      const t = this.scheduleData[e];
      if (!t) return [];
      const { blocks: i } = lt(t);
      return i;
    }
    return [];
  }
  _getWeekdayLabel(e, t) {
    return "long" === t
      ? this.translations?.weekdayLongLabels[e] ?? e
      : this.translations?.weekdayShortLabels[e] ?? e.slice(0, 2);
  }
  _formatTimeDisplay(e) {
    return ot(e, this.hourFormat);
  }
  _formatValidationParams(e) {
    if (!e) return {};
    const t = {};
    for (const [i, s] of Object.entries(e))
      "weekday" === i && tt.includes(s)
        ? (t.weekday = this._getWeekdayLabel(s, "long"))
        : (t[i] = s);
    return t;
  }
  _translateValidationMessage(e) {
    const t = this.translations?.validationMessages[e.key] || e.key,
      i = this._formatValidationParams(e.params);
    e.nested && (i.details = this._translateValidationMessage(e.nested));
    let s = t;
    for (const [e, t] of Object.entries(i)) s = s.replace(`{${e}}`, t);
    return s;
  }
  _saveHistoryState() {
    if (!this._editingBlocks) return;
    const e = JSON.parse(JSON.stringify(this._editingBlocks));
    (this._historyStack = this._historyStack.slice(0, this._historyIndex + 1)),
      this._historyStack.push(e),
      this._historyIndex++,
      this._historyStack.length > 50 &&
        (this._historyStack.shift(), this._historyIndex--);
  }
  _undo() {
    this._historyIndex <= 0 ||
      (this._historyIndex--,
      (this._editingBlocks = JSON.parse(
        JSON.stringify(this._historyStack[this._historyIndex]),
      )),
      this._updateValidationWarnings());
  }
  _redo() {
    this._historyIndex >= this._historyStack.length - 1 ||
      (this._historyIndex++,
      (this._editingBlocks = JSON.parse(
        JSON.stringify(this._historyStack[this._historyIndex]),
      )),
      this._updateValidationWarnings());
  }
  _canUndo() {
    return this._historyIndex > 0;
  }
  _canRedo() {
    return this._historyIndex < this._historyStack.length - 1;
  }
  _handleKeyDown(e) {
    if (!this.open || !this._editingWeekday || !this._editingBlocks) return;
    const t = e.ctrlKey || e.metaKey;
    t && "z" === e.key && !e.shiftKey
      ? (e.preventDefault(), this._undo())
      : t &&
        ("y" === e.key || ("z" === e.key && e.shiftKey)) &&
        (e.preventDefault(), this._redo());
  }
  _updateValidationWarnings() {
    this._validationWarnings = this._editingBlocks
      ? (function (e, t = 5, i = 30.5) {
          const s = [];
          if (0 === e.length) return s;
          for (let t = 0; t < e.length - 1; t++) {
            const i = e[t];
            i.endMinutes < i.startMinutes &&
              s.push({
                key: "blockEndBeforeStart",
                params: { block: `${t + 1}` },
              }),
              i.endMinutes === i.startMinutes &&
                s.push({
                  key: "blockZeroDuration",
                  params: { block: `${t + 1}` },
                });
          }
          const r = e[e.length - 1];
          return (
            r.endMinutes < r.startMinutes &&
              s.push({
                key: "blockEndBeforeStart",
                params: { block: `${e.length}` },
              }),
            e.forEach((e, r) => {
              (e.startMinutes < 0 || e.startMinutes > 1440) &&
                s.push({
                  key: "invalidStartTime",
                  params: { block: `${r + 1}` },
                }),
                (e.endMinutes < 0 || e.endMinutes > 1440) &&
                  s.push({
                    key: "invalidEndTime",
                    params: { block: `${r + 1}` },
                  }),
                (e.temperature < t || e.temperature > i) &&
                  s.push({
                    key: "temperatureOutOfRange",
                    params: { block: `${r + 1}`, min: `${t}`, max: `${i}` },
                  });
            }),
            s
          );
        })(this._editingBlocks, this.minTemp, this.maxTemp)
      : [];
  }
  _startSlotEdit(e) {
    if (!this._editingBlocks || e < 0 || e >= this._editingBlocks.length)
      return;
    const t = this._editingBlocks[e];
    (this._editingSlotIndex = e),
      (this._editingSlotData = {
        startTime: t.startTime,
        endTime: t.endTime,
        temperature: t.temperature,
      });
  }
  _startSlotEditFromDisplay(e, t) {
    if (!this._editingBlocks) return;
    const i = t[e],
      s = this._editingBlocks.findIndex(
        (e) =>
          e.startMinutes === i.startMinutes &&
          e.endMinutes === i.endMinutes &&
          e.temperature === i.temperature,
      );
    -1 !== s && this._startSlotEdit(s);
  }
  _cancelSlotEdit() {
    (this._editingSlotIndex = void 0), (this._editingSlotData = void 0);
  }
  _saveSlotEdit() {
    if (
      void 0 === this._editingSlotIndex ||
      !this._editingSlotData ||
      !this._editingBlocks ||
      void 0 === this._editingBaseTemperature
    )
      return;
    const e = this._editingSlotIndex,
      { startTime: t, endTime: i, temperature: s } = this._editingSlotData,
      r = {
        startTime: t,
        startMinutes: at(t),
        endTime: i,
        endMinutes: at(i),
        temperature: s,
        slot: e + 1,
      },
      a = this._editingBlocks.filter((t, i) => i !== e),
      n = (function (e, t) {
        const i = [],
          s = t.startMinutes,
          r = t.endMinutes,
          a = [...e].sort((e, t) => e.startMinutes - t.startMinutes);
        for (const e of a) {
          const t = e.startMinutes,
            a = e.endMinutes;
          a <= s || t >= r
            ? i.push(e)
            : (t < s &&
                i.push({
                  ...e,
                  endTime: nt(s),
                  endMinutes: s,
                  slot: i.length + 1,
                }),
              a > r &&
                i.push({
                  ...e,
                  startTime: nt(r),
                  startMinutes: r,
                  slot: i.length + 1,
                }));
        }
        i.push({ ...t, slot: i.length + 1 });
        const n = i.sort((e, t) => e.startMinutes - t.startMinutes);
        return ht(n);
      })(a, r),
      o = ht(_t(n));
    this._saveHistoryState(),
      (this._editingBlocks = o),
      (this._editingSlotIndex = void 0),
      (this._editingSlotData = void 0),
      this._updateValidationWarnings();
  }
  _addNewSlot() {
    if (!this._editingBlocks || void 0 === this._editingBaseTemperature) return;
    if (this._editingBlocks.length >= 12) return;
    let e = 0,
      t = 60;
    if (this._editingBlocks.length > 0) {
      const i = _t(this._editingBlocks),
        s = i[i.length - 1];
      if (s.endMinutes < 1440) (e = s.endMinutes), (t = Math.min(e + 60, 1440));
      else {
        let s = !1;
        for (let r = 0; r < i.length; r++) {
          const a = 0 === r ? 0 : i[r - 1].endMinutes;
          if (i[r].startMinutes > a) {
            (e = a), (t = i[r].startMinutes), (s = !0);
            break;
          }
        }
        if (!s) return;
      }
    }
    const i = Math.min(this._editingBaseTemperature + 2, this.maxTemp),
      s = {
        startTime: nt(e),
        startMinutes: e,
        endTime: nt(t),
        endMinutes: t,
        temperature: i,
        slot: this._editingBlocks.length + 1,
      };
    this._saveHistoryState();
    const r = _t([...this._editingBlocks, s]);
    this._editingBlocks = r;
    const a = r.findIndex((i) => i.startMinutes === e && i.endMinutes === t);
    a >= 0 && this._startSlotEdit(a), this._updateValidationWarnings();
  }
  _removeTimeBlockByIndex(e, t) {
    if (!this._editingBlocks || void 0 === this._editingBaseTemperature) return;
    const i = t[e],
      s = this._editingBlocks.findIndex(
        (e) =>
          e.startMinutes === i.startMinutes &&
          e.endMinutes === i.endMinutes &&
          e.temperature === i.temperature,
      );
    if (-1 === s) return;
    this._saveHistoryState();
    const r = this._editingBlocks.filter((e, t) => t !== s);
    (this._editingBlocks = ht(_t(r))), this._updateValidationWarnings();
  }
  _switchToWeekday(e) {
    e !== this._editingWeekday && this._initializeEditor(e);
  }
  _closeEditor() {
    (this._editingWeekday = void 0),
      (this._editingBlocks = void 0),
      (this._editingBaseTemperature = void 0),
      (this._editingSlotIndex = void 0),
      (this._editingSlotData = void 0),
      (this._historyStack = []),
      (this._historyIndex = -1),
      this.dispatchEvent(
        new CustomEvent("editor-closed", { bubbles: !0, composed: !0 }),
      );
  }
  _saveSchedule() {
    if (
      !this._editingWeekday ||
      !this._editingBlocks ||
      void 0 === this._editingBaseTemperature
    )
      return;
    const e = kt(
      ct(this._editingBlocks, this._editingBaseTemperature),
      this.minTemp,
      this.maxTemp,
    );
    if (e) {
      const t = this._translateValidationMessage(e);
      return void this.dispatchEvent(
        new CustomEvent("validation-failed", {
          detail: { error: t },
          bubbles: !0,
          composed: !0,
        }),
      );
    }
    this.dispatchEvent(
      new CustomEvent("save-schedule", {
        detail: {
          weekday: this._editingWeekday,
          blocks: this._editingBlocks,
          baseTemperature: this._editingBaseTemperature,
        },
        bubbles: !0,
        composed: !0,
      }),
    );
  }
  _saveAndClose() {
    this._saveSchedule();
  }
  render() {
    return this.open && this._editingWeekday
      ? V`
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
            ${tt.map(
              (e) => V`
                <button
                  class="weekday-tab ${
                    e === this._editingWeekday ? "active" : ""
                  }"
                  @click=${() => this._switchToWeekday(e)}
                >
                  ${this._getWeekdayLabel(e, "short")}
                </button>
              `,
            )}
          </div>

          <!-- Editor content in dialog -->
          <div class="dialog-editor">${this._renderEditor()}</div>
        </div>

        <mwc-button slot="primaryAction" @click=${
          this._saveAndClose
        } dialogAction="close">
          ${this.translations?.save ?? "Save"}
        </mwc-button>
        <mwc-button slot="secondaryAction" @click=${
          this._closeEditor
        } dialogAction="close">
          ${this.translations?.cancel ?? "Cancel"}
        </mwc-button>
      </ha-dialog>
    `
      : V``;
  }
  _formatEdit(e) {
    return (this.translations?.edit ?? "Edit {weekday}").replace(
      "{weekday}",
      this._getWeekdayLabel(e, "long"),
    );
  }
  _renderEditor() {
    if (!this._editingWeekday || !this._editingBlocks) return V``;
    const e =
      void 0 !== this._editingBaseTemperature
        ? pt(this._editingBlocks, this._editingBaseTemperature)
        : this._editingBlocks;
    return V`
      <div class="editor">
        <div class="editor-header">
          <h3>${this._formatEdit(this._editingWeekday)}</h3>
          <div class="editor-actions">
            <button
              class="undo-btn"
              @click=${this._undo}
              ?disabled=${!this._canUndo()}
              title="${this.translations?.undoShortcut ?? ""}"
            >
              ↶
            </button>
            <button
              class="redo-btn"
              @click=${this._redo}
              ?disabled=${!this._canRedo()}
              title="${this.translations?.redoShortcut ?? ""}"
            >
              ↷
            </button>
            <button class="close-btn" @click=${this._closeEditor}>✕</button>
          </div>
        </div>

        ${
          this._validationWarnings.length > 0
            ? V`
              <div class="validation-warnings">
                <div class="warnings-header">
                  <span class="warning-icon">⚠️</span>
                  <span class="warnings-title">${
                    this.translations?.warningsTitle ?? ""
                  }</span>
                </div>
                <ul class="warnings-list">
                  ${this._validationWarnings.map(
                    (e) => V`<li class="warning-item">
                        ${this._translateValidationMessage(e)}
                      </li>`,
                  )}
                </ul>
              </div>
            `
            : ""
        }

        <!-- Base Temperature Section -->
        <div class="base-temperature-section">
          <div class="base-temperature-header">
            <span class="base-temp-label">${
              this.translations?.baseTemperature ?? ""
            }</span>
            <span class="base-temp-description"
              >${this.translations?.baseTemperatureDescription ?? ""}</span
            >
          </div>
          <div class="base-temperature-input">
            <input
              type="number"
              class="temp-input base-temp-input"
              .value=${this._editingBaseTemperature?.toString() || "20.0"}
              step=${this.tempStep}
              min=${this.minTemp}
              max=${this.maxTemp}
              @change=${(e) => {
                this._saveHistoryState(),
                  (this._editingBaseTemperature = parseFloat(e.target.value)),
                  this.requestUpdate();
              }}
            />
            <span class="temp-unit">${this.temperatureUnit}</span>
            <div
              class="color-indicator"
              style="background-color: ${dt(
                this._editingBaseTemperature || 20,
              )}"
            ></div>
          </div>
        </div>

        <div class="editor-content-label">${
          this.translations?.temperaturePeriods ?? ""
        }</div>
        <div class="editor-content">
          <div class="time-block-header">
            <span class="header-cell header-from">${
              this.translations?.from ?? ""
            }</span>
            <span class="header-cell header-to">${
              this.translations?.to ?? ""
            }</span>
            <span class="header-cell header-temp">Temp</span>
            <span class="header-cell header-actions"></span>
          </div>
          ${e.map((t, i) => {
            const s = this._editingBlocks.findIndex(
                (e) =>
                  e.startMinutes === t.startMinutes &&
                  e.endMinutes === t.endMinutes,
              ),
              r = !(-1 !== s);
            return void 0 !== this._editingSlotIndex &&
              this._editingSlotIndex === s &&
              void 0 !== this._editingSlotData &&
              this._editingSlotData
              ? V`
                <div class="time-block-editor editing">
                  <input
                    type="time"
                    class="time-input"
                    .value=${this._editingSlotData.startTime}
                    @change=${(e) => {
                      this._editingSlotData &&
                        ((this._editingSlotData = {
                          ...this._editingSlotData,
                          startTime: e.target.value,
                        }),
                        this.requestUpdate());
                    }}
                  />
                  <input
                    type="time"
                    class="time-input"
                    .value=${
                      "24:00" === this._editingSlotData.endTime
                        ? "23:59"
                        : this._editingSlotData.endTime
                    }
                    @change=${(e) => {
                      if (this._editingSlotData) {
                        let t = e.target.value;
                        "23:59" === t && (t = "24:00"),
                          (this._editingSlotData = {
                            ...this._editingSlotData,
                            endTime: t,
                          }),
                          this.requestUpdate();
                      }
                    }}
                  />
                  <div class="temp-input-group">
                    <input
                      type="number"
                      class="temp-input"
                      .value=${this._editingSlotData.temperature.toString()}
                      step=${this.tempStep}
                      min=${this.minTemp}
                      max=${this.maxTemp}
                      @change=${(e) => {
                        this._editingSlotData &&
                          ((this._editingSlotData = {
                            ...this._editingSlotData,
                            temperature: parseFloat(e.target.value),
                          }),
                          this.requestUpdate());
                      }}
                    />
                    <span class="temp-unit">${this.temperatureUnit}</span>
                  </div>
                  <div class="slot-actions">
                    <button class="slot-save-btn" @click=${this._saveSlotEdit}>
                      ${this.translations?.saveSlot ?? "Save"}
                    </button>
                    <button class="slot-cancel-btn" @click=${
                      this._cancelSlotEdit
                    }>
                      ${this.translations?.cancelSlotEdit ?? "Cancel"}
                    </button>
                  </div>
                  <div
                    class="color-indicator"
                    style="background-color: ${dt(
                      this._editingSlotData.temperature,
                    )}"
                  ></div>
                </div>
              `
              : V`
              <div class="time-block-editor ${r ? "base-temp-slot" : ""}">
                <span class="time-display">${this._formatTimeDisplay(
                  t.startTime,
                )}</span>
                <span class="time-display">${this._formatTimeDisplay(
                  t.endTime,
                )}</span>
                <div class="temp-display-group">
                  <span class="temp-display">${t.temperature.toFixed(1)}</span>
                  <span class="temp-unit">${this.temperatureUnit}</span>
                </div>
                <div class="slot-actions">
                  ${
                    r
                      ? V``
                      : V`
                        <button
                          class="slot-edit-btn"
                          @click=${() => this._startSlotEditFromDisplay(i, e)}
                          ?disabled=${void 0 !== this._editingSlotIndex}
                        >
                          ${this.translations?.editSlot ?? "Edit"}
                        </button>
                        <button
                          class="remove-btn"
                          @click=${() => this._removeTimeBlockByIndex(i, e)}
                          ?disabled=${void 0 !== this._editingSlotIndex}
                        >
                          🗑️
                        </button>
                      `
                  }
                </div>
                <div
                  class="color-indicator"
                  style="background-color: ${dt(t.temperature)}"
                ></div>
              </div>
            `;
          })}
          ${
            this._editingBlocks.length < 12 && void 0 === this._editingSlotIndex
              ? V`
                <button class="add-btn" @click=${this._addNewSlot}>
                  ${this.translations?.addTimeBlock ?? "+ Add Time Block"}
                </button>
              `
              : ""
          }
        </div>

        <div class="editor-footer">
          <button class="cancel-btn" @click=${this._closeEditor}>
            ${this.translations?.cancel ?? "Cancel"}
          </button>
          <button class="save-btn" @click=${this._saveSchedule}>
            ${this.translations?.save ?? "Save"}
          </button>
        </div>
      </div>
    `;
  }
  static {
    this.styles = Et;
  }
};
Ct([he({ type: Boolean })], At.prototype, "open", void 0),
  Ct([he({ type: String })], At.prototype, "weekday", void 0),
  Ct([he({ attribute: !1 })], At.prototype, "scheduleData", void 0),
  Ct([he({ type: Number })], At.prototype, "minTemp", void 0),
  Ct([he({ type: Number })], At.prototype, "maxTemp", void 0),
  Ct([he({ type: Number })], At.prototype, "tempStep", void 0),
  Ct([he({ type: String })], At.prototype, "temperatureUnit", void 0),
  Ct([he({ type: String })], At.prototype, "hourFormat", void 0),
  Ct([he({ attribute: !1 })], At.prototype, "translations", void 0),
  Ct([pe()], At.prototype, "_editingWeekday", void 0),
  Ct([pe()], At.prototype, "_editingBlocks", void 0),
  Ct([pe()], At.prototype, "_editingBaseTemperature", void 0),
  Ct([pe()], At.prototype, "_validationWarnings", void 0),
  Ct([pe()], At.prototype, "_editingSlotIndex", void 0),
  Ct([pe()], At.prototype, "_editingSlotData", void 0),
  (At = Ct([Ve("hmip-schedule-editor")], At));
const Dt = n`
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

  .add-button {
    padding: 10px 16px;
    background-color: var(--primary-color);
    color: var(--text-primary-color);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: opacity 0.2s;
  }

  .add-button:hover {
    opacity: 0.9;
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
    gap: 8px;
    justify-content: flex-end;
  }

  .icon-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    font-size: 16px;
    opacity: 0.7;
    transition: opacity 0.2s;
  }

  .icon-button:hover {
    opacity: 1;
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    .add-button {
      min-height: 44px;
      padding: 10px 16px;
      font-size: 16px;
      width: 100%;
    }

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
    .icon-button {
      padding: 8px;
      font-size: 20px;
    }

    .event-row:hover {
      background-color: transparent;
    }

    .event-row:active {
      background-color: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
    }
  }
`;
var Tt = function (e, t, i, s) {
  var r,
    a = arguments.length,
    n =
      a < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    n = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (r = e[o]) && (n = (a < 3 ? r(n) : a > 3 ? r(t, i, n) : r(t, i)) || n);
  return a > 3 && n && Object.defineProperty(t, i, n), n;
};
let It = class extends oe {
  constructor() {
    super(...arguments), (this.editable = !0);
  }
  static {
    this.styles = Dt;
  }
  _handleAdd() {
    this.dispatchEvent(
      new CustomEvent("add-event", { bubbles: !0, composed: !0 }),
    );
  }
  _handleEdit(e) {
    this.dispatchEvent(
      new CustomEvent("edit-event", {
        bubbles: !0,
        composed: !0,
        detail: { entry: e },
      }),
    );
  }
  _handleDelete(e) {
    this.dispatchEvent(
      new CustomEvent("delete-event", {
        bubbles: !0,
        composed: !0,
        detail: { entry: e },
      }),
    );
  }
  render() {
    if (!this.scheduleData)
      return V`<div class="no-data">${this.translations.loading}</div>`;
    const e = (function (e) {
      const t = [];
      for (const [i, s] of Object.entries(e))
        t.push({ ...s, groupNo: i, isActive: ut(s) });
      return t.sort((e, t) => e.time.localeCompare(t.time)), t;
    })(this.scheduleData);
    return 0 === e.length
      ? V`
        <div class="no-data">
          <p>${this.translations.noScheduleEvents}</p>
          ${
            this.editable
              ? V`<button @click=${this._handleAdd} class="add-button">
                ${this.translations.addEvent}
              </button>`
              : ""
          }
        </div>
      `
      : V`
      <div class="schedule-list">
        ${
          this.editable
            ? V`<div class="toolbar">
              <button @click=${this._handleAdd} class="add-button">
                ${this.translations.addEvent}
              </button>
            </div>`
            : ""
        }
        <div class="events-table">
          <div class="events-header ${this.editable ? "" : "no-actions"}">
            <div class="col-time">${this.translations.time}</div>
            <div class="col-weekdays">${this.translations.weekdays}</div>
            <div class="col-state">${this.translations.state}</div>
            <div class="col-duration">${this.translations.duration}</div>
            ${this.editable ? V`<div class="col-actions"></div>` : ""}
          </div>
          ${et(
            e,
            (e) => e.groupNo,
            (e) => this._renderEvent(e),
          )}
        </div>
      </div>
    `;
  }
  _renderEvent(e) {
    const t = (function (e, t) {
        const i = t ? st[t] : void 0;
        return "binary" === i?.levelType
          ? 0 === e
            ? "Off"
            : "On"
          : `${Math.round(100 * e)}%`;
      })(e.level, this.domain),
      i = (function (e) {
        if (!e) return "-";
        const t = gt(e);
        return t
          ? `${t.value}${{ ms: "ms", s: "s", min: "min", h: "h" }[t.unit]}`
          : e;
      })(e.duration);
    return V`
      <div
        class="event-row ${e.isActive ? "active" : "inactive"} ${
          this.editable ? "" : "no-actions"
        }"
      >
        <div class="col-time">${e.time}</div>
        <div class="col-weekdays">
          <div class="weekday-badges">
            ${tt.map((t) => {
              const i = e.weekdays.includes(t);
              return V`<span class="weekday-badge ${i ? "active" : "inactive"}"
                >${this.translations.weekdayShortLabels[t]}</span
              >`;
            })}
          </div>
        </div>
        <div class="col-state">
          ${t}
          ${
            null !== e.level_2
              ? V`<span class="level-2"
                >, ${this.translations.slat}: ${Math.round(
                  100 * e.level_2,
                )}%</span
              >`
              : ""
          }
        </div>
        <div class="col-duration">${i}</div>
        ${
          this.editable
            ? V`<div class="col-actions">
              <button @click=${() =>
                this._handleEdit(e)} class="icon-button" title="Edit">
                ✏️
              </button>
              <button @click=${() =>
                this._handleDelete(e)} class="icon-button" title="Delete">
                🗑️
              </button>
            </div>`
            : ""
        }
      </div>
    `;
  }
};
Tt([he({ attribute: !1 })], It.prototype, "scheduleData", void 0),
  Tt([he({ attribute: !1 })], It.prototype, "domain", void 0),
  Tt([he({ type: Boolean })], It.prototype, "editable", void 0),
  Tt([he({ attribute: !1 })], It.prototype, "translations", void 0),
  (It = Tt([Ve("hmip-device-schedule-list")], It));
const Mt = n`
  :host {
    display: block;
  }

  /* Editor Overlay */
  .editor-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .editor-dialog {
    background-color: var(--card-background-color);
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow: auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .editor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid var(--divider-color);
  }

  .editor-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 500;
    color: var(--primary-text-color);
  }

  .close-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--secondary-text-color);
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition:
      background-color 0.2s,
      color 0.2s;
  }

  .close-button:hover {
    background-color: var(--divider-color);
    color: var(--primary-text-color);
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
  .form-group input[type="number"],
  .form-group select {
    padding: 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
  }

  .form-group input[type="range"] {
    width: 100%;
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

  .duration-row select {
    padding: 8px;
    border: 1px solid var(--divider-color);
    border-radius: 4px;
    background-color: var(--card-background-color);
    color: var(--primary-text-color);
    font-size: 14px;
  }

  .weekday-checkboxes,
  .channel-checkboxes {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    font-size: 14px;
  }

  .checkbox-label input[type="checkbox"] {
    cursor: pointer;
  }

  .editor-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px;
    border-top: 1px solid var(--divider-color);
  }

  .button-primary,
  .button-secondary {
    padding: 10px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: opacity 0.2s;
  }

  .button-primary {
    background-color: var(--primary-color);
    color: var(--text-primary-color);
  }

  .button-primary:hover {
    opacity: 0.9;
  }

  .button-secondary {
    background-color: var(--divider-color);
    color: var(--primary-text-color);
    border: none;
  }

  .button-secondary:hover {
    opacity: 0.9;
  }

  .validation-errors {
    background-color: rgba(231, 76, 60, 0.1);
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 4px;
    padding: 12px;
    margin: 0;
  }

  .validation-errors ul {
    margin: 0;
    padding-left: 20px;
    list-style-type: disc;
  }

  .validation-errors li {
    color: var(--error-color, #e74c3c);
    font-size: 13px;
    line-height: 1.6;
    margin: 4px 0;
  }

  /* Mobile Optimization */
  @media (max-width: 768px) {
    .button-primary,
    .button-secondary {
      min-height: 44px;
      padding: 10px 16px;
    }
  }
`;
var Pt = function (e, t, i, s) {
  var r,
    a = arguments.length,
    n =
      a < 3 ? t : null === s ? (s = Object.getOwnPropertyDescriptor(t, i)) : s;
  if ("object" == typeof Reflect && "function" == typeof Reflect.decorate)
    n = Reflect.decorate(e, t, i, s);
  else
    for (var o = e.length - 1; o >= 0; o--)
      (r = e[o]) && (n = (a < 3 ? r(n) : a > 3 ? r(t, i, n) : r(t, i)) || n);
  return a > 3 && n && Object.defineProperty(t, i, n), n;
};
let zt = class extends oe {
  constructor() {
    super(...arguments),
      (this.open = !1),
      (this.isNewEvent = !1),
      (this._validationErrors = []);
  }
  static {
    this.styles = Mt;
  }
  willUpdate(e) {
    (e.has("open") || e.has("entry")) &&
      (this.open && this.entry
        ? ((this._editingEntry = { ...this.entry }),
          (this._validationErrors = []))
        : this.open ||
          ((this._editingEntry = void 0), (this._validationErrors = [])));
  }
  _updateEditingEntry(e) {
    this._editingEntry &&
      ((this._editingEntry = { ...this._editingEntry, ...e }),
      (this._validationErrors = []),
      this.requestUpdate());
  }
  _handleClose() {
    this.dispatchEvent(
      new CustomEvent("editor-closed", { bubbles: !0, composed: !0 }),
    );
  }
  _handleSave() {
    if (!this._editingEntry || void 0 === this.groupNo) return;
    const e = (function (e, t) {
      const i = [];
      (function (e) {
        try {
          return (
            (function (e) {
              const t = e.split(":");
              if (2 !== t.length) throw new Error(`Invalid time format: ${e}`);
              const i = parseInt(t[0], 10),
                s = parseInt(t[1], 10);
              if (isNaN(i) || isNaN(s) || i < 0 || i > 23 || s < 0 || s > 59)
                throw new Error(`Invalid time values: ${e}`);
            })(e),
            !0
          );
        } catch {
          return !1;
        }
      })(e.time) ||
        i.push({
          field: "time",
          message: "Time must be in HH:MM format (00:00-23:59)",
        }),
        (e.weekdays && 0 !== e.weekdays.length) ||
          i.push({
            field: "weekdays",
            message: "At least one weekday must be selected",
          }),
        (e.target_channels && 0 !== e.target_channels.length) ||
          i.push({
            field: "target_channels",
            message: "At least one target channel must be selected",
          });
      const s = t ? st[t] : void 0;
      return (
        "binary" === s?.levelType
          ? 0 !== e.level &&
            1 !== e.level &&
            i.push({
              field: "level",
              message: "Level must be 0 or 1 for switch",
            })
          : (e.level < 0 || e.level > 1) &&
            i.push({
              field: "level",
              message: "Level must be between 0.0 and 1.0",
            }),
        "cover" === t &&
          null !== e.level_2 &&
          (e.level_2 < 0 || e.level_2 > 1) &&
          i.push({
            field: "level_2",
            message: "Slat position must be between 0.0 and 1.0",
          }),
        vt(e.condition) &&
          (e.astro_offset_minutes < -720 || e.astro_offset_minutes > 720) &&
          i.push({
            field: "astro_offset_minutes",
            message: "Astro offset must be between -720 and 720 minutes",
          }),
        null === e.duration ||
          yt(e.duration) ||
          i.push({ field: "duration", message: "Invalid duration format" }),
        null === e.ramp_time ||
          yt(e.ramp_time) ||
          i.push({ field: "ramp_time", message: "Invalid ramp time format" }),
        i
      );
    })(this._editingEntry, this.domain);
    e.length > 0
      ? (this._validationErrors = e.map((e) => `${e.field}: ${e.message}`))
      : this.dispatchEvent(
          new CustomEvent("save-event", {
            bubbles: !0,
            composed: !0,
            detail: { entry: { ...this._editingEntry }, groupNo: this.groupNo },
          }),
        );
  }
  render() {
    return this.open && this._editingEntry
      ? V`
      <div class="editor-overlay" @click=${this._handleClose}>
        <div class="editor-dialog" @click=${(e) => e.stopPropagation()}>
          <div class="editor-header">
            <h3>${
              this.isNewEvent
                ? this.translations.addEvent
                : this.translations.editEvent
            }</h3>
            <button @click=${this._handleClose} class="close-button">✕</button>
          </div>
          <div class="editor-content">
            ${this._renderTimeFields()} ${this._renderConditionFields()}
            ${this._renderWeekdayFields()} ${this._renderLevelFields()}
            ${this._renderDurationFields()} ${this._renderRampTimeFields()}
            ${this._renderChannelFields()} ${this._renderValidationErrors()}
          </div>
          <div class="editor-footer">
            <button @click=${this._handleClose} class="button-secondary">
              ${this.translations.cancel}
            </button>
            <button @click=${this._handleSave} class="button-primary">
              ${this.translations.save}
            </button>
          </div>
        </div>
      </div>
    `
      : V``;
  }
  _renderValidationErrors() {
    return 0 === this._validationErrors.length
      ? V``
      : V`
      <div class="validation-errors">
        <ul>
          ${this._validationErrors.map((e) => V`<li>${e}</li>`)}
        </ul>
      </div>
    `;
  }
  _renderTimeFields() {
    return this._editingEntry
      ? V`
      <div class="form-group">
        <label>${this.translations.time}</label>
        <input
          type="time"
          .value=${this._editingEntry.time}
          @change=${(e) => {
            this._updateEditingEntry({ time: e.target.value });
          }}
        />
      </div>
    `
      : V``;
  }
  _renderConditionFields() {
    if (!this._editingEntry) return V``;
    const e = vt(this._editingEntry.condition);
    return V`
      <div class="form-group">
        <label>${this.translations.condition}</label>
        <select
          .value=${this._editingEntry.condition}
          @change=${(e) => {
            const t = e.target.value,
              i = { condition: t };
            "fixed_time" === t
              ? ((i.astro_type = null), (i.astro_offset_minutes = 0))
              : null === this._editingEntry.astro_type &&
                (i.astro_type = "sunrise"),
              this._updateEditingEntry(i);
          }}
        >
          ${it.map(
            (e) => V`
              <option value=${e} ?selected=${
                e === this._editingEntry.condition
              }>
                ${this.translations.conditionLabels[e] || e}
              </option>
            `,
          )}
        </select>
      </div>
      ${
        e
          ? V`
            <div class="form-group">
              <label>${this.translations.astroSunrise}/${
                this.translations.astroSunset
              }</label>
              <select
                .value=${this._editingEntry.astro_type || "sunrise"}
                @change=${(e) => {
                  this._updateEditingEntry({ astro_type: e.target.value });
                }}
              >
                <option value="sunrise" ?selected=${
                  "sunrise" === this._editingEntry.astro_type
                }>
                  ${this.translations.astroSunrise}
                </option>
                <option value="sunset" ?selected=${
                  "sunset" === this._editingEntry.astro_type
                }>
                  ${this.translations.astroSunset}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>${this.translations.astroOffset}</label>
              <input
                type="number"
                min="-720"
                max="720"
                .value=${String(this._editingEntry.astro_offset_minutes)}
                @input=${(e) => {
                  const t = parseInt(e.target.value, 10);
                  isNaN(t) ||
                    this._updateEditingEntry({ astro_offset_minutes: t });
                }}
              />
            </div>
          `
          : ""
      }
    `;
  }
  _renderWeekdayFields() {
    return this._editingEntry
      ? V`
      <div class="form-group">
        <label>${this.translations.weekdaysLabel}</label>
        <div class="weekday-checkboxes">
          ${tt.map((e) => {
            const t = this._editingEntry.weekdays.includes(e);
            return V`
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  .checked=${t}
                  @change=${(t) => {
                    const i = t.target.checked,
                      s = [...this._editingEntry.weekdays];
                    if (i && !s.includes(e)) s.push(e);
                    else if (!i) {
                      const t = s.indexOf(e);
                      t > -1 && s.splice(t, 1);
                    }
                    this._updateEditingEntry({ weekdays: s });
                  }}
                />
                ${this.translations.weekdayShortLabels[e]}
              </label>
            `;
          })}
        </div>
      </div>
    `
      : V``;
  }
  _renderLevelFields() {
    if (!this._editingEntry) return V``;
    const e = this.domain ? st[this.domain] : void 0;
    return V`
      <div class="form-group">
        <label>${this.translations.stateLabel}</label>
        ${
          "binary" === e?.levelType
            ? V`
              <select
                .value=${String(this._editingEntry.level)}
                @change=${(e) => {
                  const t = parseInt(e.target.value, 10);
                  this._updateEditingEntry({ level: t });
                }}
              >
                <option value="0">${this.translations.levelOff}</option>
                <option value="1">${this.translations.levelOn}</option>
              </select>
            `
            : V`
              <input
                type="range"
                min="0"
                max="100"
                .value=${String(Math.round(100 * this._editingEntry.level))}
                @input=${(e) => {
                  const t = parseInt(e.target.value, 10) / 100;
                  this._updateEditingEntry({ level: t });
                }}
              />
              <span>${Math.round(100 * this._editingEntry.level)}%</span>
            `
        }
      </div>
      ${
        e?.hasLevel2
          ? V`
            <div class="form-group">
              <label>${this.translations.slat}</label>
              <input
                type="range"
                min="0"
                max="100"
                .value=${String(
                  Math.round(100 * (this._editingEntry.level_2 || 0)),
                )}
                @input=${(e) => {
                  const t = parseInt(e.target.value, 10) / 100;
                  this._updateEditingEntry({ level_2: t });
                }}
              />
              <span>${Math.round(
                100 * (this._editingEntry.level_2 || 0),
              )}%</span>
            </div>
          `
          : ""
      }
    `;
  }
  _renderDurationFields() {
    if (!this._editingEntry) return V``;
    const e = this.domain ? st[this.domain] : void 0;
    if (e && !e.hasDuration) return V``;
    const t = this._editingEntry.duration
        ? gt(this._editingEntry.duration)
        : null,
      i = t?.value ?? 0,
      s = t?.unit ?? "s";
    return V`
      <div class="form-group">
        <label>${this.translations.duration}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${(e) => {
              const t = parseFloat(e.target.value);
              !isNaN(t) && t > 0
                ? this._updateEditingEntry({ duration: ft(t, s) })
                : this._updateEditingEntry({ duration: null });
            }}
          />
          <select
            .value=${s}
            @change=${(e) => {
              i > 0 &&
                this._updateEditingEntry({ duration: ft(i, e.target.value) });
            }}
          >
            ${rt.map(
              (e) => V` <option value=${e} ?selected=${e === s}>${e}</option> `,
            )}
          </select>
        </div>
      </div>
    `;
  }
  _renderRampTimeFields() {
    if (!this._editingEntry) return V``;
    const e = this.domain ? st[this.domain] : void 0;
    if (e && !e.hasRampTime) return V``;
    const t = this._editingEntry.ramp_time
        ? gt(this._editingEntry.ramp_time)
        : null,
      i = t?.value ?? 0,
      s = t?.unit ?? "s";
    return V`
      <div class="form-group">
        <label>${this.translations.rampTime}</label>
        <div class="duration-row">
          <input
            type="number"
            min="0"
            .value=${String(i)}
            @input=${(e) => {
              const t = parseFloat(e.target.value);
              !isNaN(t) && t > 0
                ? this._updateEditingEntry({ ramp_time: ft(t, s) })
                : this._updateEditingEntry({ ramp_time: null });
            }}
          />
          <select
            .value=${s}
            @change=${(e) => {
              i > 0 &&
                this._updateEditingEntry({ ramp_time: ft(i, e.target.value) });
            }}
          >
            ${rt.map(
              (e) => V` <option value=${e} ?selected=${e === s}>${e}</option> `,
            )}
          </select>
        </div>
      </div>
    `;
  }
  _renderChannelFields() {
    return this._editingEntry
      ? this.availableTargetChannels &&
        Object.keys(this.availableTargetChannels).length > 0
        ? V`
        <div class="form-group">
          <label>${this.translations.channels}</label>
          <div class="channel-checkboxes">
            ${Object.entries(this.availableTargetChannels).map(([e, t]) => {
              const i = this._editingEntry.target_channels.includes(e);
              return V`
                <label class="checkbox-label">
                  <input
                    type="checkbox"
                    .checked=${i}
                    @change=${(t) => {
                      const i = t.target.checked,
                        s = [...this._editingEntry.target_channels];
                      if (i && !s.includes(e)) s.push(e);
                      else if (!i) {
                        const t = s.indexOf(e);
                        t > -1 && s.splice(t, 1);
                      }
                      this._updateEditingEntry({ target_channels: s });
                    }}
                  />
                  ${t.name || e}
                </label>
              `;
            })}
          </div>
        </div>
      `
        : V`
      <div class="form-group">
        <label>${this.translations.channels}</label>
        <input
          type="text"
          .value=${this._editingEntry.target_channels.join(", ")}
          @input=${(e) => {
            const t = e.target.value
              .split(",")
              .map((e) => e.trim())
              .filter((e) => e.length > 0);
            this._updateEditingEntry({ target_channels: t });
          }}
          placeholder="1_1, 2_1"
        />
      </div>
    `
      : V``;
  }
};
Pt([he({ type: Boolean })], zt.prototype, "open", void 0),
  Pt([he({ attribute: !1 })], zt.prototype, "entry", void 0),
  Pt([he()], zt.prototype, "groupNo", void 0),
  Pt([he({ type: Boolean })], zt.prototype, "isNewEvent", void 0),
  Pt([he({ attribute: !1 })], zt.prototype, "domain", void 0),
  Pt([he({ attribute: !1 })], zt.prototype, "availableTargetChannels", void 0),
  Pt([he({ attribute: !1 })], zt.prototype, "translations", void 0),
  Pt([pe()], zt.prototype, "_editingEntry", void 0),
  Pt([pe()], zt.prototype, "_validationErrors", void 0),
  (zt = Pt([Ve("hmip-device-schedule-editor")], zt));
let Nt = class extends oe {
  constructor() {
    super(...arguments),
      (this.entryId = ""),
      (this.deviceAddress = ""),
      (this.deviceName = ""),
      (this._devices = []),
      (this._selectedDevice = null),
      (this._climateData = null),
      (this._deviceData = null),
      (this._selectedProfile = ""),
      (this._loading = !0),
      (this._saving = !1),
      (this._error = ""),
      (this._deviceShowEditor = !1),
      (this._deviceIsNewEvent = !1);
  }
  updated(e) {
    (e.has("entryId") || e.has("deviceAddress")) &&
      this.entryId &&
      this._fetchDevices();
  }
  async _fetchDevices() {
    (this._loading = !0), (this._error = "");
    try {
      if (
        ((this._devices = await ke(this.hass, this.entryId)),
        this.deviceAddress)
      ) {
        const e = this._devices.find((e) => e.address === this.deviceAddress);
        e && ((this._selectedDevice = e), await this._loadSchedule(e));
      }
    } catch (e) {
      this._error = String(e);
    } finally {
      this._loading = !1;
    }
  }
  async _loadSchedule(e) {
    (this._loading = !0),
      (this._error = ""),
      (this._climateData = null),
      (this._deviceData = null);
    try {
      if ("climate" === e.schedule_type) {
        const t = await (async function (e, t, i, s) {
          return e.callWS({
            type: "homematicip_local/config/get_climate_schedule",
            entry_id: t,
            device_address: i,
            ...(s && { profile: s }),
          });
        })(this.hass, this.entryId, e.address, this._selectedProfile || void 0);
        (this._climateData = t),
          this._selectedProfile || (this._selectedProfile = t.active_profile);
      } else
        this._deviceData = await (async function (e, t, i) {
          return e.callWS({
            type: "homematicip_local/config/get_device_schedule",
            entry_id: t,
            device_address: i,
          });
        })(this.hass, this.entryId, e.address);
    } catch {
      this._error = this._l("device_schedule.load_failed");
    } finally {
      this._loading = !1;
    }
  }
  _l(e, t) {
    return Te(this.hass, e, t);
  }
  _handleBack() {
    this.dispatchEvent(new CustomEvent("back", { bubbles: !0, composed: !0 }));
  }
  async _handleDeviceSelect(e) {
    const t = e.target.value;
    if (!t) return void (this._selectedDevice = null);
    const i = this._devices.find((e) => e.address === t);
    i &&
      ((this._selectedDevice = i),
      (this._selectedProfile = ""),
      (this._editingWeekday = void 0),
      (this._copiedSchedule = void 0),
      (this._deviceShowEditor = !1),
      (this._deviceEditingEntry = void 0),
      (this._deviceEditingGroupNo = void 0),
      (this._deviceIsNewEvent = !1),
      await this._loadSchedule(i));
  }
  async _handleProfileChange(e) {
    (this._selectedProfile = e.target.value),
      this._selectedDevice && (await this._loadSchedule(this._selectedDevice));
  }
  async _handleSetActiveProfile() {
    if (this._selectedDevice && this._selectedProfile)
      try {
        await (async function (e, t, i, s) {
          return e.callWS({
            type: "homematicip_local/config/set_climate_active_profile",
            entry_id: t,
            device_address: i,
            profile: s,
          });
        })(
          this.hass,
          this.entryId,
          this._selectedDevice.address,
          this._selectedProfile,
        ),
          this._climateData &&
            (this._climateData = {
              ...this._climateData,
              active_profile: this._selectedProfile,
            }),
          Pe(this, { message: this._l("device_schedule.save_success") });
      } catch {
        Pe(this, { message: this._l("device_schedule.save_failed") });
      }
  }
  _onWeekdayClick(e) {
    this._editingWeekday = e.detail.weekday;
  }
  _onCopySchedule(e) {
    const t = e.detail.weekday;
    if (!this._climateData) return;
    const i = this._climateData.schedule_data[t];
    if (!i) return;
    const { blocks: s, baseTemperature: r } = lt(i);
    this._copiedSchedule = {
      weekday: t,
      blocks: JSON.parse(JSON.stringify(s)),
      baseTemperature: r,
    };
  }
  async _onPasteSchedule(e) {
    const t = e.detail.weekday;
    if (!this._selectedDevice || !this._copiedSchedule || !this._climateData)
      return;
    const i =
        this._copiedSchedule.baseTemperature ??
        (function (e) {
          if (0 === e.length) return 20;
          const t = new Map();
          for (const i of e) {
            const e = i.endMinutes - i.startMinutes,
              s = t.get(i.temperature) || 0;
            t.set(i.temperature, s + e);
          }
          let i = 0,
            s = 20;
          for (const [e, r] of t.entries()) r > i && ((i = r), (s = e));
          return s;
        })(this._copiedSchedule.blocks),
      s = ct(this._copiedSchedule.blocks, i);
    if (
      kt(s, this._climateData.min_temp ?? 5, this._climateData.max_temp ?? 30.5)
    )
      Pe(this, { message: this._l("device_schedule.invalid_schedule") });
    else {
      this._saving = !0;
      try {
        const { base_temperature: e, periods: i } = s;
        await $e(
          this.hass,
          this.entryId,
          this._selectedDevice.address,
          this._selectedProfile,
          t,
          e,
          i.map((e) => ({ ...e })),
        ),
          Pe(this, { message: this._l("device_schedule.save_success") }),
          await this._loadSchedule(this._selectedDevice);
      } catch {
        Pe(this, { message: this._l("device_schedule.save_failed") });
      } finally {
        this._saving = !1;
      }
    }
  }
  async _onSaveSchedule(e) {
    if (!this._selectedDevice || !this._climateData) return;
    const { weekday: t, blocks: i, baseTemperature: s } = e.detail,
      r = ct(i, s);
    if (
      kt(r, this._climateData.min_temp ?? 5, this._climateData.max_temp ?? 30.5)
    )
      Pe(this, { message: this._l("device_schedule.invalid_schedule") });
    else {
      this._saving = !0;
      try {
        const { base_temperature: e, periods: i } = r;
        await $e(
          this.hass,
          this.entryId,
          this._selectedDevice.address,
          this._selectedProfile,
          t,
          e,
          i.map((e) => ({ ...e })),
        ),
          Pe(this, { message: this._l("device_schedule.save_success") }),
          (this._editingWeekday = void 0),
          await this._loadSchedule(this._selectedDevice);
      } catch {
        Pe(this, { message: this._l("device_schedule.save_failed") });
      } finally {
        this._saving = !1;
      }
    }
  }
  _onValidationFailed(e) {
    Pe(this, {
      message: this._l("device_schedule.invalid_schedule", {
        error: e.detail.error,
      }),
    });
  }
  _onEditorClosed() {
    this._editingWeekday = void 0;
  }
  async _handleReload() {
    if (this._selectedDevice)
      try {
        await (async function (e, t, i) {
          return e.callWS({
            type: "homematicip_local/config/reload_device_config",
            entry_id: t,
            device_address: i,
          });
        })(this.hass, this.entryId, this._selectedDevice.address),
          Pe(this, { message: this._l("device_schedule.reload_success") }),
          await this._loadSchedule(this._selectedDevice);
      } catch {
        Pe(this, { message: this._l("device_schedule.reload_failed") });
      }
  }
  async _handleExport() {
    const e =
      this._climateData?.schedule_data ?? this._deviceData?.schedule_data;
    if (!e) return;
    const t = JSON.stringify(e, null, 2),
      i = new Blob([t], { type: "application/json" }),
      s = URL.createObjectURL(i),
      r = document.createElement("a");
    r.href = s;
    const a = this._selectedDevice?.address.replace(/:/g, "_") ?? "schedule";
    (r.download = `${a}_schedule.json`), r.click(), URL.revokeObjectURL(s);
  }
  async _handleImport() {
    const e = document.createElement("input");
    (e.type = "file"),
      (e.accept = ".json"),
      (e.onchange = async () => {
        const t = e.files?.[0];
        if (t && this._selectedDevice)
          try {
            const e = await t.text(),
              i = JSON.parse(e);
            if (
              !(await Me(this, {
                title: this._l("device_schedule.import_confirm_title"),
                text: this._l("device_schedule.import_confirm_text"),
                confirmText: this._l("device_schedule.import"),
                dismissText: this._l("common.cancel"),
              }))
            )
              return;
            "climate" === this._selectedDevice.schedule_type
              ? ((this._climateData = {
                  ...this._climateData,
                  schedule_data: i,
                }),
                Pe(this, {
                  message: this._l("device_schedule.import_success"),
                }))
              : (await we(
                  this.hass,
                  this.entryId,
                  this._selectedDevice.address,
                  i,
                ),
                Pe(this, {
                  message: this._l("device_schedule.import_success"),
                }),
                await this._loadSchedule(this._selectedDevice));
          } catch {
            Pe(this, { message: this._l("device_schedule.import_failed") });
          }
      }),
      e.click();
  }
  _buildGridTranslations() {
    return {
      weekdayShortLabels: {
        MONDAY: this._l("device_schedule.weekdays").split(",")[0],
        TUESDAY: this._l("device_schedule.weekdays").split(",")[1],
        WEDNESDAY: this._l("device_schedule.weekdays").split(",")[2],
        THURSDAY: this._l("device_schedule.weekdays").split(",")[3],
        FRIDAY: this._l("device_schedule.weekdays").split(",")[4],
        SATURDAY: this._l("device_schedule.weekdays").split(",")[5],
        SUNDAY: this._l("device_schedule.weekdays").split(",")[6],
      },
      clickToEdit: this._l("device_schedule.click_to_edit"),
      copySchedule: this._l("device_schedule.copy_schedule"),
      pasteSchedule: this._l("device_schedule.paste_schedule"),
    };
  }
  _buildEditorTranslations() {
    const e = this._l("device_schedule.weekdays").split(",");
    return {
      weekdayShortLabels: {
        MONDAY: e[0],
        TUESDAY: e[1],
        WEDNESDAY: e[2],
        THURSDAY: e[3],
        FRIDAY: e[4],
        SATURDAY: e[5],
        SUNDAY: e[6],
      },
      weekdayLongLabels: {
        MONDAY: this._l("device_schedule.weekday_monday"),
        TUESDAY: this._l("device_schedule.weekday_tuesday"),
        WEDNESDAY: this._l("device_schedule.weekday_wednesday"),
        THURSDAY: this._l("device_schedule.weekday_thursday"),
        FRIDAY: this._l("device_schedule.weekday_friday"),
        SATURDAY: this._l("device_schedule.weekday_saturday"),
        SUNDAY: this._l("device_schedule.weekday_sunday"),
      },
      edit: this._l("device_schedule.edit"),
      cancel: this._l("common.cancel"),
      save: this._l("device_schedule.save"),
      addTimeBlock: this._l("device_schedule.add_time_block"),
      from: this._l("device_schedule.from"),
      to: this._l("device_schedule.to"),
      baseTemperature: this._l("device_schedule.base_temperature"),
      baseTemperatureDescription: this._l(
        "device_schedule.base_temperature_description",
      ),
      temperaturePeriods: this._l("device_schedule.temperature_periods"),
      editSlot: this._l("device_schedule.edit_slot"),
      saveSlot: this._l("device_schedule.save_slot"),
      cancelSlotEdit: this._l("device_schedule.cancel_slot_edit"),
      undoShortcut: this._l("device_schedule.undo_shortcut"),
      redoShortcut: this._l("device_schedule.redo_shortcut"),
      warningsTitle: this._l("device_schedule.warnings_title"),
      validationMessages: {
        blockEndBeforeStart: this._l(
          "device_schedule.validation_block_end_before_start",
        ),
        blockZeroDuration: this._l(
          "device_schedule.validation_block_zero_duration",
        ),
        invalidStartTime: this._l(
          "device_schedule.validation_invalid_start_time",
        ),
        invalidEndTime: this._l("device_schedule.validation_invalid_end_time"),
        temperatureOutOfRange: this._l(
          "device_schedule.validation_temp_out_of_range",
        ),
        invalidSlotCount: this._l(
          "device_schedule.validation_invalid_slot_count",
        ),
        invalidSlotKey: this._l("device_schedule.validation_invalid_slot_key"),
        missingSlot: this._l("device_schedule.validation_missing_slot"),
        slotMissingValues: this._l(
          "device_schedule.validation_slot_missing_values",
        ),
        slotTimeBackwards: this._l(
          "device_schedule.validation_slot_time_backwards",
        ),
        slotTimeExceedsDay: this._l(
          "device_schedule.validation_slot_time_exceeds_day",
        ),
        lastSlotMustEnd: this._l(
          "device_schedule.validation_last_slot_must_end",
        ),
        scheduleMustBeObject: this._l(
          "device_schedule.validation_schedule_must_be_object",
        ),
        missingWeekday: this._l("device_schedule.validation_missing_weekday"),
        invalidWeekdayData: this._l(
          "device_schedule.validation_invalid_weekday_data",
        ),
        weekdayValidationError: this._l(
          "device_schedule.validation_weekday_error",
        ),
      },
    };
  }
  render() {
    return this._loading && 0 === this._devices.length
      ? V`<div class="loading">${this._l("common.loading")}</div>`
      : this._error && 0 === this._devices.length
        ? V`<div class="error">${this._error}</div>`
        : V`
      <button class="back-button" @click=${this._handleBack}>◂ ${this._l(
        "common.back",
      )}</button>

      <div class="schedule-header">
        <h2>${this._l("device_schedule.title")}</h2>

        <div class="device-selector">
          <select @change=${this._handleDeviceSelect}>
            <option value="">${this._l(
              "device_schedule.select_device",
            )}</option>
            ${[...this._devices]
              .sort((e, t) => e.name.localeCompare(t.name))
              .map(
                (e) => V`
                  <option
                    value="${e.address}"
                    ?selected=${e.address === this._selectedDevice?.address}
                  >
                    ${e.name} (${e.model}) -
                    ${this._l(
                      `device_schedule.schedule_type_${e.schedule_type}`,
                    )}
                  </option>
                `,
              )}
          </select>
        </div>
      </div>

      ${
        0 === this._devices.length
          ? V`<div class="empty-state">${this._l(
              "device_schedule.no_devices",
            )}</div>`
          : K
      }
      ${
        this._selectedDevice && this._loading
          ? V`<div class="loading">${this._l("common.loading")}</div>`
          : K
      }
      ${
        this._error && this._selectedDevice
          ? V`<div class="error">${this._error}</div>`
          : K
      }
      ${
        "climate" === this._selectedDevice?.schedule_type && this._climateData
          ? this._renderClimateSchedule()
          : K
      }
      ${
        "default" === this._selectedDevice?.schedule_type && this._deviceData
          ? this._renderDeviceSchedule()
          : K
      }
    `;
  }
  _renderClimateSchedule() {
    const e = this._climateData,
      t = e.schedule_data;
    return V`
      <div class="schedule-content">
        <div class="toolbar">
          <div class="profile-selector">
            <label>${this._l("device_schedule.profile")}:</label>
            <select @change=${this._handleProfileChange}>
              ${e.available_profiles.map(
                (t) => V`
                  <option value="${t}" ?selected=${t === this._selectedProfile}>
                    ${t}${t === e.active_profile ? " ✓" : ""}
                  </option>
                `,
              )}
            </select>
            ${
              this._selectedProfile !== e.active_profile
                ? V`
                  <button class="action-btn small" @click=${
                    this._handleSetActiveProfile
                  }>
                    ${this._l("device_schedule.active_profile")}
                  </button>
                `
                : K
            }
          </div>
          <div class="toolbar-actions">
            <button class="action-btn" @click=${this._handleExport}>
              ${this._l("device_schedule.export")}
            </button>
            <button class="action-btn" @click=${this._handleImport}>
              ${this._l("device_schedule.import")}
            </button>
            <button class="action-btn" @click=${this._handleReload}>
              ${this._l("device_schedule.reload")}
            </button>
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
          .minTemp=${e.min_temp ?? 5}
          .maxTemp=${e.max_temp ?? 30.5}
          .tempStep=${e.step ?? 0.5}
          temperatureUnit="°C"
          hourFormat="24"
          .translations=${this._buildEditorTranslations()}
          @save-schedule=${this._onSaveSchedule}
          @validation-failed=${this._onValidationFailed}
          @editor-closed=${this._onEditorClosed}
        ></hmip-schedule-editor>
      </div>

      ${
        this._saving
          ? V`<div class="saving-overlay">${this._l(
              "device_schedule.saving",
            )}</div>`
          : K
      }
    `;
  }
  _onDeviceAddEvent() {
    if (!this._deviceData) return;
    const e = this._deviceData.schedule_data?.entries ?? {},
      t = this._deviceData.max_entries;
    if (t && Object.keys(e).length >= t)
      return void Pe(this, {
        message: this._l("device_schedule.max_entries", { max: t }),
      });
    const i = (function (e) {
        const t = {
          weekdays: [],
          time: "00:00",
          condition: "fixed_time",
          astro_type: null,
          astro_offset_minutes: 0,
          target_channels: [],
          level: 0,
          level_2: null,
          duration: null,
          ramp_time: null,
        };
        return "cover" === e && (t.level_2 = 0), t;
      })(this._deviceData.schedule_domain ?? void 0),
      s = this._deviceData.available_target_channels;
    if (s) {
      const e = Object.keys(s)[0];
      e && (i.target_channels = [e]);
    }
    const r = Object.keys(e).map((e) => parseInt(e, 10)),
      a = r.length > 0 ? Math.max(...r) : 0;
    (this._deviceEditingGroupNo = String(a + 1)),
      (this._deviceEditingEntry = { ...i }),
      (this._deviceIsNewEvent = !0),
      (this._deviceShowEditor = !0);
  }
  _onDeviceEditEvent(e) {
    const t = e.detail.entry;
    (this._deviceEditingGroupNo = t.groupNo),
      (this._deviceEditingEntry = { ...t }),
      (this._deviceIsNewEvent = !1),
      (this._deviceShowEditor = !0);
  }
  async _onDeviceDeleteEvent(e) {
    if (!confirm(this._l("device_schedule.confirm_delete"))) return;
    if (!this._deviceData || !this._selectedDevice) return;
    const t = { ...(this._deviceData.schedule_data?.entries ?? {}) };
    delete t[e.detail.entry.groupNo], (this._saving = !0);
    try {
      await we(this.hass, this.entryId, this._selectedDevice.address, {
        entries: xt(t),
      }),
        Pe(this, { message: this._l("device_schedule.save_success") }),
        await this._loadSchedule(this._selectedDevice);
    } catch {
      Pe(this, { message: this._l("device_schedule.save_failed") });
    } finally {
      this._saving = !1;
    }
  }
  async _onDeviceSaveEvent(e) {
    if (!this._deviceData || !this._selectedDevice) return;
    const { entry: t, groupNo: i } = e.detail,
      s = { ...(this._deviceData.schedule_data?.entries ?? {}), [i]: t };
    (this._saving = !0),
      (this._deviceShowEditor = !1),
      (this._deviceEditingEntry = void 0),
      (this._deviceEditingGroupNo = void 0),
      (this._deviceIsNewEvent = !1);
    try {
      await we(this.hass, this.entryId, this._selectedDevice.address, {
        entries: xt(s),
      }),
        Pe(this, { message: this._l("device_schedule.save_success") }),
        await this._loadSchedule(this._selectedDevice);
    } catch {
      Pe(this, { message: this._l("device_schedule.save_failed") });
    } finally {
      this._saving = !1;
    }
  }
  _onDeviceEditorClosed() {
    (this._deviceShowEditor = !1),
      (this._deviceEditingEntry = void 0),
      (this._deviceEditingGroupNo = void 0),
      (this._deviceIsNewEvent = !1);
  }
  _buildDeviceListTranslations() {
    const e = this._l("device_schedule.weekdays").split(",");
    return {
      weekdayShortLabels: {
        MONDAY: e[0],
        TUESDAY: e[1],
        WEDNESDAY: e[2],
        THURSDAY: e[3],
        FRIDAY: e[4],
        SATURDAY: e[5],
        SUNDAY: e[6],
      },
      time: this._l("device_schedule.time"),
      weekdays: this._l("device_schedule.weekdays_label"),
      duration: this._l("device_schedule.duration"),
      state: this._l("device_schedule.level"),
      addEvent: this._l("device_schedule.add_event"),
      slat: this._l("device_schedule.slat"),
      noScheduleEvents: this._l("device_schedule.no_schedule_data"),
      loading: this._l("common.loading"),
    };
  }
  _buildDeviceEditorTranslations() {
    const e = this._l("device_schedule.weekdays").split(",");
    return {
      weekdayShortLabels: {
        MONDAY: e[0],
        TUESDAY: e[1],
        WEDNESDAY: e[2],
        THURSDAY: e[3],
        FRIDAY: e[4],
        SATURDAY: e[5],
        SUNDAY: e[6],
      },
      addEvent: this._l("device_schedule.add_event"),
      editEvent: this._l("device_schedule.edit_event"),
      cancel: this._l("common.cancel"),
      save: this._l("device_schedule.save"),
      time: this._l("device_schedule.time"),
      condition: this._l("device_schedule.condition"),
      weekdaysLabel: this._l("device_schedule.weekdays_label"),
      stateLabel: this._l("device_schedule.level"),
      duration: this._l("device_schedule.duration"),
      rampTime: this._l("device_schedule.ramp_time"),
      channels: this._l("device_schedule.target_channel"),
      levelOn: this._l("device_schedule.level_on"),
      levelOff: this._l("device_schedule.level_off"),
      slat: this._l("device_schedule.slat"),
      astroSunrise: this._l("device_schedule.astro_sunrise"),
      astroSunset: this._l("device_schedule.astro_sunset"),
      astroOffset: this._l("device_schedule.astro_offset"),
      confirmDelete: this._l("device_schedule.confirm_delete"),
      conditionLabels: {
        fixed_time: this._l("device_schedule.condition_fixed_time"),
        astro: this._l("device_schedule.condition_astro"),
        fixed_if_before_astro: this._l(
          "device_schedule.condition_fixed_if_before_astro",
        ),
        astro_if_before_fixed: this._l(
          "device_schedule.condition_astro_if_before_fixed",
        ),
        fixed_if_after_astro: this._l(
          "device_schedule.condition_fixed_if_after_astro",
        ),
        astro_if_after_fixed: this._l(
          "device_schedule.condition_astro_if_after_fixed",
        ),
        earliest: this._l("device_schedule.condition_earliest"),
        latest: this._l("device_schedule.condition_latest"),
      },
    };
  }
  _renderDeviceSchedule() {
    const e = this._deviceData,
      t = e.schedule_data,
      i = t?.entries ?? {},
      s = Object.keys(i).length,
      r = e.schedule_domain ?? void 0,
      a = e.available_target_channels;
    return V`
      <div class="schedule-content">
        <div class="toolbar">
          <div class="schedule-info">
            ${this._l("device_schedule.entries", { count: s })} |
            ${this._l("device_schedule.max_entries", { max: e.max_entries })}
            ${e.schedule_domain ? V` | ${e.schedule_domain}` : K}
          </div>
          <div class="toolbar-actions">
            <button class="action-btn" @click=${this._handleExport}>
              ${this._l("device_schedule.export")}
            </button>
            <button class="action-btn" @click=${this._handleImport}>
              ${this._l("device_schedule.import")}
            </button>
            <button class="action-btn" @click=${this._handleReload}>
              ${this._l("device_schedule.reload")}
            </button>
          </div>
        </div>

        <div class="device-schedule-container">
          <hmip-device-schedule-list
            .scheduleData=${i}
            .domain=${r}
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
          .domain=${r}
          .availableTargetChannels=${a}
          .translations=${this._buildDeviceEditorTranslations()}
          @save-event=${this._onDeviceSaveEvent}
          @editor-closed=${this._onDeviceEditorClosed}
        ></hmip-device-schedule-editor>
      </div>

      ${
        this._saving
          ? V`<div class="saving-overlay">${this._l(
              "device_schedule.saving",
            )}</div>`
          : K
      }
    `;
  }
  static {
    this.styles = [
      ue,
      n`
      .schedule-header {
        margin-bottom: 16px;
      }

      .schedule-header h2 {
        margin: 8px 0 12px;
        font-size: 20px;
        font-weight: 400;
      }

      .device-selector select {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        font-family: inherit;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
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

      .profile-selector select {
        padding: 4px 8px;
        border: 1px solid var(--divider-color, #e0e0e0);
        border-radius: 4px;
        font-size: 14px;
        font-family: inherit;
        background: var(--card-background-color, #fff);
        color: var(--primary-text-color);
      }

      .toolbar-actions {
        display: flex;
        gap: 8px;
      }

      .schedule-info {
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      .action-btn {
        background: none;
        border: 1px solid var(--primary-color, #03a9f4);
        color: var(--primary-color, #03a9f4);
        padding: 4px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 13px;
        font-family: inherit;
      }

      .action-btn:hover {
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }

      .action-btn.primary {
        background: var(--primary-color, #03a9f4);
        color: #fff;
      }

      .action-btn.primary:hover {
        opacity: 0.9;
      }

      .action-btn.small {
        padding: 2px 8px;
        font-size: 12px;
      }

      .action-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
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
    `,
    ];
  }
};
e([he({ attribute: !1 })], Nt.prototype, "hass", void 0),
  e([he()], Nt.prototype, "entryId", void 0),
  e([he()], Nt.prototype, "deviceAddress", void 0),
  e([he()], Nt.prototype, "deviceName", void 0),
  e([pe()], Nt.prototype, "_devices", void 0),
  e([pe()], Nt.prototype, "_selectedDevice", void 0),
  e([pe()], Nt.prototype, "_climateData", void 0),
  e([pe()], Nt.prototype, "_deviceData", void 0),
  e([pe()], Nt.prototype, "_selectedProfile", void 0),
  e([pe()], Nt.prototype, "_editingWeekday", void 0),
  e([pe()], Nt.prototype, "_copiedSchedule", void 0),
  e([pe()], Nt.prototype, "_loading", void 0),
  e([pe()], Nt.prototype, "_saving", void 0),
  e([pe()], Nt.prototype, "_error", void 0),
  e([pe()], Nt.prototype, "_deviceEditingEntry", void 0),
  e([pe()], Nt.prototype, "_deviceEditingGroupNo", void 0),
  e([pe()], Nt.prototype, "_deviceShowEditor", void 0),
  e([pe()], Nt.prototype, "_deviceIsNewEvent", void 0),
  (Nt = e([_e("hm-device-schedule")], Nt));
let Rt = class extends oe {
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
      (this._senderDeviceName = ""),
      (this._senderDeviceModel = ""),
      (this._senderChannelTypeLabel = ""),
      (this._receiverDeviceName = ""),
      (this._receiverDeviceModel = ""),
      (this._receiverChannelTypeLabel = ""),
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
      r = t.get("device") || "",
      a = t.get("interface") || "",
      n = t.get("channel") || "",
      o = t.get("channel_type") || "",
      d = t.get("paramset") || "MASTER",
      l = t.get("sender") || "",
      c = t.get("receiver") || "";
    s && (this._entryId = s),
      i &&
        this._navigateTo(i, {
          device: r,
          interfaceId: a,
          channel: n,
          channelType: o,
          paramsetKey: d,
          senderAddress: l,
          receiverAddress: c,
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
      void 0 !== t?.senderDeviceName &&
        (this._senderDeviceName = t.senderDeviceName),
      void 0 !== t?.senderDeviceModel &&
        (this._senderDeviceModel = t.senderDeviceModel),
      void 0 !== t?.senderChannelTypeLabel &&
        (this._senderChannelTypeLabel = t.senderChannelTypeLabel),
      void 0 !== t?.receiverDeviceName &&
        (this._receiverDeviceName = t.receiverDeviceName),
      void 0 !== t?.receiverDeviceModel &&
        (this._receiverDeviceModel = t.receiverDeviceModel),
      void 0 !== t?.receiverChannelTypeLabel &&
        (this._receiverChannelTypeLabel = t.receiverChannelTypeLabel),
      this._updateUrlHash();
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
              (this._entryId = e.detail.entryId), this._updateUrlHash();
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
            @show-history=${(e) => this._navigateTo("change-history", e.detail)}
            @show-links=${(e) => this._navigateTo("device-links", e.detail)}
            @show-schedules=${(e) =>
              this._navigateTo("device-schedule", e.detail)}
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
      case "change-history":
        return V`
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
        return V`
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
        return V`
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
            @back=${() =>
              this._navigateTo("device-links", {
                device: this._selectedDevice,
                interfaceId: this._selectedInterfaceId,
              })}
          ></hm-link-config>
        `;
      case "add-link":
        return V`
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
      case "device-schedule":
        return V`
          <hm-device-schedule
            .hass=${this.hass}
            .entryId=${this._entryId}
            .deviceAddress=${this._selectedDevice}
            .deviceName=${this._selectedDeviceName}
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
          ></hm-device-schedule>
        `;
    }
  }
  static {
    this.styles = n`
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
e([he({ attribute: !1 })], Rt.prototype, "hass", void 0),
  e([he({ attribute: !1 })], Rt.prototype, "panel", void 0),
  e([he({ type: Boolean, reflect: !0 })], Rt.prototype, "narrow", void 0),
  e([pe()], Rt.prototype, "_view", void 0),
  e([pe()], Rt.prototype, "_entryId", void 0),
  e([pe()], Rt.prototype, "_entries", void 0),
  e([pe()], Rt.prototype, "_selectedDevice", void 0),
  e([pe()], Rt.prototype, "_selectedInterfaceId", void 0),
  e([pe()], Rt.prototype, "_selectedChannel", void 0),
  e([pe()], Rt.prototype, "_selectedChannelType", void 0),
  e([pe()], Rt.prototype, "_selectedParamsetKey", void 0),
  e([pe()], Rt.prototype, "_selectedDeviceName", void 0),
  e([pe()], Rt.prototype, "_selectedSenderAddress", void 0),
  e([pe()], Rt.prototype, "_selectedReceiverAddress", void 0),
  e([pe()], Rt.prototype, "_senderDeviceName", void 0),
  e([pe()], Rt.prototype, "_senderDeviceModel", void 0),
  e([pe()], Rt.prototype, "_senderChannelTypeLabel", void 0),
  e([pe()], Rt.prototype, "_receiverDeviceName", void 0),
  e([pe()], Rt.prototype, "_receiverDeviceModel", void 0),
  e([pe()], Rt.prototype, "_receiverChannelTypeLabel", void 0),
  (Rt = e([_e("homematic-config")], Rt));
export { Rt as HomematicConfigPanel };
