"use strict";(()=>{var Ut=Object.create;var Kr=Object.defineProperty;var Ht=Object.getOwnPropertyDescriptor;var Nt=Object.getOwnPropertyNames;var jt=Object.getPrototypeOf,Xt=Object.prototype.hasOwnProperty;var Yt=(s,r)=>()=>(r||s((r={exports:{}}).exports,r),r.exports);var Gt=(s,r,a,d)=>{if(r&&typeof r=="object"||typeof r=="function")for(let f of Nt(r))!Xt.call(s,f)&&f!==a&&Kr(s,f,{get:()=>r[f],enumerable:!(d=Ht(r,f))||d.enumerable});return s};var Wt=(s,r,a)=>(a=s!=null?Ut(jt(s)):{},Gt(r||!s||!s.__esModule?Kr(a,"default",{value:s,enumerable:!0}):a,s));var Zr=Yt((je,Xe)=>{(function(s,r){typeof je=="object"&&typeof Xe<"u"?Xe.exports=r():typeof define=="function"&&define.amd?define(r):(s=typeof globalThis<"u"?globalThis:s||self,s.DOMPurify=r())})(je,function(){"use strict";let{entries:s,setPrototypeOf:r,isFrozen:a,getPrototypeOf:d,getOwnPropertyDescriptor:f}=Object,{freeze:h,seal:g,create:K}=Object,{apply:Z,construct:$}=typeof Reflect<"u"&&Reflect;h||(h=function(l){return l}),g||(g=function(l){return l}),Z||(Z=function(l,b,p){return l.apply(b,p)}),$||($=function(l,b){return new l(...b)});let U=M(Array.prototype.forEach),J=M(Array.prototype.pop),F=M(Array.prototype.push),H=M(String.prototype.toLowerCase),ve=M(String.prototype.toString),mr=M(String.prototype.match),Q=M(String.prototype.replace),et=M(String.prototype.indexOf),rt=M(String.prototype.trim),L=M(Object.prototype.hasOwnProperty),T=M(RegExp.prototype.test),ee=tt(TypeError);function M(m){return function(l){for(var b=arguments.length,p=new Array(b>1?b-1:0),y=1;y<b;y++)p[y-1]=arguments[y];return Z(m,l,p)}}function tt(m){return function(){for(var l=arguments.length,b=new Array(l),p=0;p<l;p++)b[p]=arguments[p];return $(m,b)}}function c(m,l){let b=arguments.length>2&&arguments[2]!==void 0?arguments[2]:H;r&&r(m,null);let p=l.length;for(;p--;){let y=l[p];if(typeof y=="string"){let D=b(y);D!==y&&(a(l)||(l[p]=D),y=D)}m[y]=!0}return m}function ot(m){for(let l=0;l<m.length;l++)L(m,l)||(m[l]=null);return m}function O(m){let l=K(null);for(let[b,p]of s(m))L(m,b)&&(Array.isArray(p)?l[b]=ot(p):p&&typeof p=="object"&&p.constructor===Object?l[b]=O(p):l[b]=p);return l}function ce(m,l){for(;m!==null;){let p=f(m,l);if(p){if(p.get)return M(p.get);if(typeof p.value=="function")return M(p.value)}m=d(m)}function b(){return null}return b}let fr=h(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","section","select","shadow","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),xe=h(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","filter","font","g","glyph","glyphref","hkern","image","line","lineargradient","marker","mask","metadata","mpath","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),ke=h(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),at=h(["animate","color-profile","cursor","discard","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),ye=h(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover","mprescripts"]),st=h(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),br=h(["#text"]),hr=h(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","face","for","headers","height","hidden","high","href","hreflang","id","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","pattern","placeholder","playsinline","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","xmlns","slot"]),Ce=h(["accent-height","accumulate","additive","alignment-baseline","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),ur=h(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),de=h(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),lt=g(/\{\{[\w\W]*|[\w\W]*\}\}/gm),nt=g(/<%[\w\W]*|[\w\W]*%>/gm),it=g(/\${[\w\W]*}/gm),ct=g(/^data-[\-\w.\u00B7-\uFFFF]/),dt=g(/^aria-[\-\w]+$/),wr=g(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),pt=g(/^(?:\w+script|data):/i),mt=g(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),gr=g(/^html$/i),ft=g(/^[a-z][.\w]*(-[.\w]+)+$/i);var vr=Object.freeze({__proto__:null,MUSTACHE_EXPR:lt,ERB_EXPR:nt,TMPLIT_EXPR:it,DATA_ATTR:ct,ARIA_ATTR:dt,IS_ALLOWED_URI:wr,IS_SCRIPT_OR_DATA:pt,ATTR_WHITESPACE:mt,DOCTYPE_NAME:gr,CUSTOM_ELEMENT:ft});let bt=function(){return typeof window>"u"?null:window},ht=function(l,b){if(typeof l!="object"||typeof l.createPolicy!="function")return null;let p=null,y="data-tt-policy-suffix";b&&b.hasAttribute(y)&&(p=b.getAttribute(y));let D="dompurify"+(p?"#"+p:"");try{return l.createPolicy(D,{createHTML(N){return N},createScriptURL(N){return N}})}catch{return console.warn("TrustedTypes policy "+D+" could not be created."),null}};function xr(){let m=arguments.length>0&&arguments[0]!==void 0?arguments[0]:bt(),l=n=>xr(n);if(l.version="3.0.11",l.removed=[],!m||!m.document||m.document.nodeType!==9)return l.isSupported=!1,l;let{document:b}=m,p=b,y=p.currentScript,{DocumentFragment:D,HTMLTemplateElement:N,Node:ze,Element:kr,NodeFilter:re,NamedNodeMap:wt=m.NamedNodeMap||m.MozNamedAttrMap,HTMLFormElement:gt,DOMParser:vt,trustedTypes:pe}=m,me=kr.prototype,xt=ce(me,"cloneNode"),kt=ce(me,"nextSibling"),yt=ce(me,"childNodes"),Se=ce(me,"parentNode");if(typeof N=="function"){let n=b.createElement("template");n.content&&n.content.ownerDocument&&(b=n.content.ownerDocument)}let S,te="",{implementation:Ee,createNodeIterator:Ct,createDocumentFragment:zt,getElementsByTagName:St}=b,{importNode:Et}=p,R={};l.isSupported=typeof s=="function"&&typeof Se=="function"&&Ee&&Ee.createHTMLDocument!==void 0;let{MUSTACHE_EXPR:Ae,ERB_EXPR:Te,TMPLIT_EXPR:Me,DATA_ATTR:At,ARIA_ATTR:Tt,IS_SCRIPT_OR_DATA:Mt,ATTR_WHITESPACE:yr,CUSTOM_ELEMENT:Lt}=vr,{IS_ALLOWED_URI:Cr}=vr,v=null,zr=c({},[...fr,...xe,...ke,...ye,...br]),x=null,Sr=c({},[...hr,...Ce,...ur,...de]),w=Object.seal(K(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),oe=null,Le=null,Er=!0,Re=!0,Ar=!1,Tr=!0,j=!1,B=!1,De=!1,Pe=!1,X=!1,fe=!1,be=!1,Mr=!0,Lr=!1,Rt="user-content-",_e=!0,ae=!1,Y={},G=null,Rr=c({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]),Dr=null,Pr=c({},["audio","video","img","source","image","track"]),Fe=null,_r=c({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),he="http://www.w3.org/1998/Math/MathML",ue="http://www.w3.org/2000/svg",P="http://www.w3.org/1999/xhtml",W=P,qe=!1,Oe=null,Dt=c({},[he,ue,P],ve),se=null,Pt=["application/xhtml+xml","text/html"],_t="text/html",k=null,V=null,Ft=b.createElement("form"),Fr=function(e){return e instanceof RegExp||e instanceof Function},Be=function(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};if(!(V&&V===e)){if((!e||typeof e!="object")&&(e={}),e=O(e),se=Pt.indexOf(e.PARSER_MEDIA_TYPE)===-1?_t:e.PARSER_MEDIA_TYPE,k=se==="application/xhtml+xml"?ve:H,v=L(e,"ALLOWED_TAGS")?c({},e.ALLOWED_TAGS,k):zr,x=L(e,"ALLOWED_ATTR")?c({},e.ALLOWED_ATTR,k):Sr,Oe=L(e,"ALLOWED_NAMESPACES")?c({},e.ALLOWED_NAMESPACES,ve):Dt,Fe=L(e,"ADD_URI_SAFE_ATTR")?c(O(_r),e.ADD_URI_SAFE_ATTR,k):_r,Dr=L(e,"ADD_DATA_URI_TAGS")?c(O(Pr),e.ADD_DATA_URI_TAGS,k):Pr,G=L(e,"FORBID_CONTENTS")?c({},e.FORBID_CONTENTS,k):Rr,oe=L(e,"FORBID_TAGS")?c({},e.FORBID_TAGS,k):{},Le=L(e,"FORBID_ATTR")?c({},e.FORBID_ATTR,k):{},Y=L(e,"USE_PROFILES")?e.USE_PROFILES:!1,Er=e.ALLOW_ARIA_ATTR!==!1,Re=e.ALLOW_DATA_ATTR!==!1,Ar=e.ALLOW_UNKNOWN_PROTOCOLS||!1,Tr=e.ALLOW_SELF_CLOSE_IN_ATTR!==!1,j=e.SAFE_FOR_TEMPLATES||!1,B=e.WHOLE_DOCUMENT||!1,X=e.RETURN_DOM||!1,fe=e.RETURN_DOM_FRAGMENT||!1,be=e.RETURN_TRUSTED_TYPE||!1,Pe=e.FORCE_BODY||!1,Mr=e.SANITIZE_DOM!==!1,Lr=e.SANITIZE_NAMED_PROPS||!1,_e=e.KEEP_CONTENT!==!1,ae=e.IN_PLACE||!1,Cr=e.ALLOWED_URI_REGEXP||wr,W=e.NAMESPACE||P,w=e.CUSTOM_ELEMENT_HANDLING||{},e.CUSTOM_ELEMENT_HANDLING&&Fr(e.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(w.tagNameCheck=e.CUSTOM_ELEMENT_HANDLING.tagNameCheck),e.CUSTOM_ELEMENT_HANDLING&&Fr(e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(w.attributeNameCheck=e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),e.CUSTOM_ELEMENT_HANDLING&&typeof e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements=="boolean"&&(w.allowCustomizedBuiltInElements=e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),j&&(Re=!1),fe&&(X=!0),Y&&(v=c({},br),x=[],Y.html===!0&&(c(v,fr),c(x,hr)),Y.svg===!0&&(c(v,xe),c(x,Ce),c(x,de)),Y.svgFilters===!0&&(c(v,ke),c(x,Ce),c(x,de)),Y.mathMl===!0&&(c(v,ye),c(x,ur),c(x,de))),e.ADD_TAGS&&(v===zr&&(v=O(v)),c(v,e.ADD_TAGS,k)),e.ADD_ATTR&&(x===Sr&&(x=O(x)),c(x,e.ADD_ATTR,k)),e.ADD_URI_SAFE_ATTR&&c(Fe,e.ADD_URI_SAFE_ATTR,k),e.FORBID_CONTENTS&&(G===Rr&&(G=O(G)),c(G,e.FORBID_CONTENTS,k)),_e&&(v["#text"]=!0),B&&c(v,["html","head","body"]),v.table&&(c(v,["tbody"]),delete oe.tbody),e.TRUSTED_TYPES_POLICY){if(typeof e.TRUSTED_TYPES_POLICY.createHTML!="function")throw ee('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');if(typeof e.TRUSTED_TYPES_POLICY.createScriptURL!="function")throw ee('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');S=e.TRUSTED_TYPES_POLICY,te=S.createHTML("")}else S===void 0&&(S=ht(pe,y)),S!==null&&typeof te=="string"&&(te=S.createHTML(""));h&&h(e),V=e}},qr=c({},["mi","mo","mn","ms","mtext"]),Or=c({},["foreignobject","desc","title","annotation-xml"]),qt=c({},["title","style","font","a","script"]),Br=c({},[...xe,...ke,...at]),Ir=c({},[...ye,...st]),Ot=function(e){let t=Se(e);(!t||!t.tagName)&&(t={namespaceURI:W,tagName:"template"});let o=H(e.tagName),u=H(t.tagName);return Oe[e.namespaceURI]?e.namespaceURI===ue?t.namespaceURI===P?o==="svg":t.namespaceURI===he?o==="svg"&&(u==="annotation-xml"||qr[u]):!!Br[o]:e.namespaceURI===he?t.namespaceURI===P?o==="math":t.namespaceURI===ue?o==="math"&&Or[u]:!!Ir[o]:e.namespaceURI===P?t.namespaceURI===ue&&!Or[u]||t.namespaceURI===he&&!qr[u]?!1:!Ir[o]&&(qt[o]||!Br[o]):!!(se==="application/xhtml+xml"&&Oe[e.namespaceURI]):!1},q=function(e){F(l.removed,{element:e});try{e.parentNode.removeChild(e)}catch{e.remove()}},Ie=function(e,t){try{F(l.removed,{attribute:t.getAttributeNode(e),from:t})}catch{F(l.removed,{attribute:null,from:t})}if(t.removeAttribute(e),e==="is"&&!x[e])if(X||fe)try{q(t)}catch{}else try{t.setAttribute(e,"")}catch{}},Ur=function(e){let t=null,o=null;if(Pe)e="<remove></remove>"+e;else{let z=mr(e,/^[\r\n\t ]+/);o=z&&z[0]}se==="application/xhtml+xml"&&W===P&&(e='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+e+"</body></html>");let u=S?S.createHTML(e):e;if(W===P)try{t=new vt().parseFromString(u,se)}catch{}if(!t||!t.documentElement){t=Ee.createDocument(W,"template",null);try{t.documentElement.innerHTML=qe?te:u}catch{}}let C=t.body||t.documentElement;return e&&o&&C.insertBefore(b.createTextNode(o),C.childNodes[0]||null),W===P?St.call(t,B?"html":"body")[0]:B?t.documentElement:C},Hr=function(e){return Ct.call(e.ownerDocument||e,e,re.SHOW_ELEMENT|re.SHOW_COMMENT|re.SHOW_TEXT|re.SHOW_PROCESSING_INSTRUCTION|re.SHOW_CDATA_SECTION,null)},Bt=function(e){return e instanceof gt&&(typeof e.nodeName!="string"||typeof e.textContent!="string"||typeof e.removeChild!="function"||!(e.attributes instanceof wt)||typeof e.removeAttribute!="function"||typeof e.setAttribute!="function"||typeof e.namespaceURI!="string"||typeof e.insertBefore!="function"||typeof e.hasChildNodes!="function")},Nr=function(e){return typeof ze=="function"&&e instanceof ze},_=function(e,t,o){R[e]&&U(R[e],u=>{u.call(l,t,o,V)})},jr=function(e){let t=null;if(_("beforeSanitizeElements",e,null),Bt(e))return q(e),!0;let o=k(e.nodeName);if(_("uponSanitizeElement",e,{tagName:o,allowedTags:v}),e.hasChildNodes()&&!Nr(e.firstElementChild)&&T(/<[/\w]/g,e.innerHTML)&&T(/<[/\w]/g,e.textContent)||e.nodeType===7)return q(e),!0;if(!v[o]||oe[o]){if(!oe[o]&&Yr(o)&&(w.tagNameCheck instanceof RegExp&&T(w.tagNameCheck,o)||w.tagNameCheck instanceof Function&&w.tagNameCheck(o)))return!1;if(_e&&!G[o]){let u=Se(e)||e.parentNode,C=yt(e)||e.childNodes;if(C&&u){let z=C.length;for(let E=z-1;E>=0;--E)u.insertBefore(xt(C[E],!0),kt(e))}}return q(e),!0}return e instanceof kr&&!Ot(e)||(o==="noscript"||o==="noembed"||o==="noframes")&&T(/<\/no(script|embed|frames)/i,e.innerHTML)?(q(e),!0):(j&&e.nodeType===3&&(t=e.textContent,U([Ae,Te,Me],u=>{t=Q(t,u," ")}),e.textContent!==t&&(F(l.removed,{element:e.cloneNode()}),e.textContent=t)),_("afterSanitizeElements",e,null),!1)},Xr=function(e,t,o){if(Mr&&(t==="id"||t==="name")&&(o in b||o in Ft))return!1;if(!(Re&&!Le[t]&&T(At,t))){if(!(Er&&T(Tt,t))){if(!x[t]||Le[t]){if(!(Yr(e)&&(w.tagNameCheck instanceof RegExp&&T(w.tagNameCheck,e)||w.tagNameCheck instanceof Function&&w.tagNameCheck(e))&&(w.attributeNameCheck instanceof RegExp&&T(w.attributeNameCheck,t)||w.attributeNameCheck instanceof Function&&w.attributeNameCheck(t))||t==="is"&&w.allowCustomizedBuiltInElements&&(w.tagNameCheck instanceof RegExp&&T(w.tagNameCheck,o)||w.tagNameCheck instanceof Function&&w.tagNameCheck(o))))return!1}else if(!Fe[t]){if(!T(Cr,Q(o,yr,""))){if(!((t==="src"||t==="xlink:href"||t==="href")&&e!=="script"&&et(o,"data:")===0&&Dr[e])){if(!(Ar&&!T(Mt,Q(o,yr,"")))){if(o)return!1}}}}}}return!0},Yr=function(e){return e!=="annotation-xml"&&mr(e,Lt)},Gr=function(e){_("beforeSanitizeAttributes",e,null);let{attributes:t}=e;if(!t)return;let o={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:x},u=t.length;for(;u--;){let C=t[u],{name:z,namespaceURI:E,value:I}=C,le=k(z),A=z==="value"?I:rt(I);if(o.attrName=le,o.attrValue=A,o.keepAttr=!0,o.forceKeepAttr=void 0,_("uponSanitizeAttribute",e,o),A=o.attrValue,o.forceKeepAttr||(Ie(z,e),!o.keepAttr))continue;if(!Tr&&T(/\/>/i,A)){Ie(z,e);continue}j&&U([Ae,Te,Me],Vr=>{A=Q(A,Vr," ")});let Wr=k(e.nodeName);if(Xr(Wr,le,A)){if(Lr&&(le==="id"||le==="name")&&(Ie(z,e),A=Rt+A),S&&typeof pe=="object"&&typeof pe.getAttributeType=="function"&&!E)switch(pe.getAttributeType(Wr,le)){case"TrustedHTML":{A=S.createHTML(A);break}case"TrustedScriptURL":{A=S.createScriptURL(A);break}}try{E?e.setAttributeNS(E,z,A):e.setAttribute(z,A),J(l.removed)}catch{}}}_("afterSanitizeAttributes",e,null)},It=function n(e){let t=null,o=Hr(e);for(_("beforeSanitizeShadowDOM",e,null);t=o.nextNode();)_("uponSanitizeShadowNode",t,null),!jr(t)&&(t.content instanceof D&&n(t.content),Gr(t));_("afterSanitizeShadowDOM",e,null)};return l.sanitize=function(n){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=null,o=null,u=null,C=null;if(qe=!n,qe&&(n="<!-->"),typeof n!="string"&&!Nr(n))if(typeof n.toString=="function"){if(n=n.toString(),typeof n!="string")throw ee("dirty is not a string, aborting")}else throw ee("toString is not a function");if(!l.isSupported)return n;if(De||Be(e),l.removed=[],typeof n=="string"&&(ae=!1),ae){if(n.nodeName){let I=k(n.nodeName);if(!v[I]||oe[I])throw ee("root node is forbidden and cannot be sanitized in-place")}}else if(n instanceof ze)t=Ur("<!---->"),o=t.ownerDocument.importNode(n,!0),o.nodeType===1&&o.nodeName==="BODY"||o.nodeName==="HTML"?t=o:t.appendChild(o);else{if(!X&&!j&&!B&&n.indexOf("<")===-1)return S&&be?S.createHTML(n):n;if(t=Ur(n),!t)return X?null:be?te:""}t&&Pe&&q(t.firstChild);let z=Hr(ae?n:t);for(;u=z.nextNode();)jr(u)||(u.content instanceof D&&It(u.content),Gr(u));if(ae)return n;if(X){if(fe)for(C=zt.call(t.ownerDocument);t.firstChild;)C.appendChild(t.firstChild);else C=t;return(x.shadowroot||x.shadowrootmode)&&(C=Et.call(p,C,!0)),C}let E=B?t.outerHTML:t.innerHTML;return B&&v["!doctype"]&&t.ownerDocument&&t.ownerDocument.doctype&&t.ownerDocument.doctype.name&&T(gr,t.ownerDocument.doctype.name)&&(E="<!DOCTYPE "+t.ownerDocument.doctype.name+`>
`+E),j&&U([Ae,Te,Me],I=>{E=Q(E,I," ")}),S&&be?S.createHTML(E):E},l.setConfig=function(){let n=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};Be(n),De=!0},l.clearConfig=function(){V=null,De=!1},l.isValidAttribute=function(n,e,t){V||Be({});let o=k(n),u=k(e);return Xr(o,u,t)},l.addHook=function(n,e){typeof e=="function"&&(R[n]=R[n]||[],F(R[n],e))},l.removeHook=function(n){if(R[n])return J(R[n])},l.removeHooks=function(n){R[n]&&(R[n]=[])},l.removeAllHooks=function(){R={}},l}var ut=xr();return ut})});var Ue=class extends HTMLElement{constructor(){super(),this.blockId=this.dataset.blockId,this.pageId=this.dataset.pageId,this.isSubscribed=this.dataset.isSubscribed!==void 0,this.button=this.querySelector("button"),this.button.addEventListener("click",r=>this.#e())}async#e(){this.button.classList.add("btn-disabled"),this.button.textContent="Loading",(await fetch(`/api-v2/change/${this.isSubscribed?"unsubscribe":"subscribe"}/`,{method:"POST",body:JSON.stringify({page:this.pageId,flashcards:this.blockId})})).ok&&(this.isSubscribed=!this.isSubscribed),this.button.classList.remove("btn-disabled"),this.button.textContent=this.isSubscribed?"Unsubscribe":"Subscribe"}};customElements.define("yapity-flashcards-subscribe-button",Ue);var He=class{constructor(r){this.cards=r,this.#r()}draw(){return this.cards.shift()}insert(r){this.cards.push(r),this.#r()}score(){let r=0;for(let a of this.cards)a.lastScore&&(r+=a.lastScore);return r}#e(r){let a=Date.now()/1e3-r.last_displayed_float,d=150*Math.exp(-a/60);return r.weight-d}#r(){this.cards.sort((r,a)=>this.#e(a)-this.#e(r))}#o(){this.cards.map(r=>`${this.#e(r)}: ${Date.now()/1e3-r.last_displayed_float}: ${r.weight}: ${r.q.slice(0,40)}...`).forEach(r=>console.log(r)),console.log(this.cards)}},Ne=class extends HTMLElement{constructor(){super(),this.flashcards=JSON.parse(this.dataset.cards),this.deck=new He(this.flashcards),this.cardNumber=1,this.progressBadge=this.querySelector("#progress-badge"),this.scoreBadge=this.querySelector("#score-badge"),this.interactionButtons=this.querySelectorAll("[data-score]"),this.interactionButtons.forEach(r=>r.addEventListener("click",()=>this.#o(parseFloat(r.dataset.score)))),this.querySelector("#face-container")?.addEventListener("click",()=>this.#e()),this.frontFace=this.querySelector("#front-face"),this.frontFaceContent=this.frontFace.querySelector("#face-content"),this.backFace=this.querySelector("#back-face"),this.backFaceContent=this.backFace.querySelector("#face-content"),this.currentCard=this.deck.draw(),this.faceUp="back"}#e(){this.faceUp=this.faceUp=="front"?"back":"front",this.frontFace.classList.toggle("flashcard-flip-in"),this.frontFace.classList.toggle("flashcard-flip-out"),this.backFace.classList.toggle("flashcard-flip-in"),this.backFace.classList.toggle("flashcard-flip-out"),this.faceUp=="front"?this.#s():this.#t(),this.#r()}#r(){this.faceUp=="front"?this.frontFaceContent.innerHTML=this.currentCard.q:this.backFaceContent.innerHTML=this.currentCard.a}async#o(r){this.#s();let a=await this.#a(this.currentCard,r),d={...this.currentCard,...a,lastScore:r};this.deck.insert(d),this.scoreBadge.textContent=this.deck.score().toFixed(1),this.currentCard=this.deck.draw(),this.progressBadge.textContent=(++this.cardNumber).toString(),this.#e()}async#a(r,a){return await(await fetch("/api-v2/change/flashcard-interaction/",{method:"POST",body:JSON.stringify({page:r.notepage_id,flashcards:r.block_id,flashcard:r.id,score:a})})).json()}#s(){this.interactionButtons.forEach(r=>r.classList.add("btn-disabled"))}#t(){this.interactionButtons.forEach(r=>r.classList.remove("btn-disabled"))}};customElements.define("yapity-flashcards",Ne);var Qr=Wt(Zr());var $r=(s,r,a=[])=>{let d=document.createElementNS("http://www.w3.org/2000/svg",s);return Object.keys(r).forEach(f=>{d.setAttribute(f,String(r[f]))}),a.length&&a.forEach(f=>{let h=$r(...f);d.appendChild(h)}),d},ne=([s,r,a])=>$r(s,r,a);var Vt=s=>Array.from(s.attributes).reduce((r,a)=>(r[a.name]=a.value,r),{}),Kt=s=>typeof s=="string"?s:!s||!s.class?"":s.class&&typeof s.class=="string"?s.class.split(" "):s.class&&Array.isArray(s.class)?s.class:"",Zt=s=>s.flatMap(Kt).map(a=>a.trim()).filter(Boolean).filter((a,d,f)=>f.indexOf(a)===d).join(" "),$t=s=>s.replace(/(\w)(\w*)(_|-|\s*)/g,(r,a,d)=>a.toUpperCase()+d.toLowerCase()),Ye=(s,{nameAttr:r,icons:a,attrs:d})=>{let f=s.getAttribute(r);if(f==null)return;let h=$t(f),g=a[h];if(!g)return console.warn(`${s.outerHTML} icon name was not found in the provided icons object.`);let K=Vt(s),[Z,$,U]=g,J={...$,"data-lucide":f,...d,...K},F=Zt(["lucide",`lucide-${f}`,K,d]);F&&Object.assign(J,{class:F});let H=ne([Z,J,U]);return s.parentNode?.replaceChild(H,s)};var i={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};var Ge=["svg",i,[["path",{d:"M20 6 9 17l-5-5"}]]];var We=["svg",i,[["path",{d:"M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"}],["path",{d:"M14 2v4a2 2 0 0 0 2 2h4"}],["path",{d:"M10 9H8"}],["path",{d:"M16 13H8"}],["path",{d:"M16 17H8"}]]];var Ve=["svg",i,[["path",{d:"M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0 15 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"}],["path",{d:"M20 21a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-2.9a1 1 0 0 1-.88-.55l-.42-.85a1 1 0 0 0-.92-.6H13a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z"}],["path",{d:"M3 5a2 2 0 0 0 2 2h3"}],["path",{d:"M3 3v13a2 2 0 0 0 2 2h3"}]]];var Ke=["svg",i,[["path",{d:"M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"}],["path",{d:"M9 18c-4.51 2-5-2-7-2"}]]];var Ze=["svg",i,[["circle",{cx:"12",cy:"12",r:"10"}],["path",{d:"M12 16v-4"}],["path",{d:"M12 8h.01"}]]];var $e=["svg",i,[["path",{d:"M2 18v3c0 .6.4 1 1 1h4v-3h3v-3h2l1.4-1.4a6.5 6.5 0 1 0-4-4Z"}],["circle",{cx:"16.5",cy:"7.5",r:".5",fill:"currentColor"}]]];var Je=["svg",i,[["circle",{cx:"12",cy:"12",r:"10"}],["path",{d:"M18 13a6 6 0 0 1-6 5 6 6 0 0 1-6-5h12Z"}],["line",{x1:"9",x2:"9.01",y1:"9",y2:"9"}],["line",{x1:"15",x2:"15.01",y1:"9",y2:"9"}]]];var ie=["svg",i,[["path",{d:"M3 3v18h18"}],["path",{d:"m19 9-5 5-4-4-3 3"}]]];var Qe=["svg",i,[["path",{d:"M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"}],["polyline",{points:"10 17 15 12 10 7"}],["line",{x1:"15",x2:"3",y1:"12",y2:"12"}]]];var er=["svg",i,[["line",{x1:"4",x2:"20",y1:"12",y2:"12"}],["line",{x1:"4",x2:"20",y1:"6",y2:"6"}],["line",{x1:"4",x2:"20",y1:"18",y2:"18"}]]];var rr=["svg",i,[["path",{d:"M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"}],["path",{d:"m15 5 4 4"}]]];var tr=["svg",i,[["path",{d:"M21 7v6h-6"}],["path",{d:"M3 17a9 9 0 0 1 9-9 9 9 0 0 1 6 2.3l3 2.7"}]]];var or=["svg",i,[["circle",{cx:"11",cy:"11",r:"8"}],["path",{d:"m21 21-4.3-4.3"}]]];var ar=["svg",i,[["circle",{cx:"18",cy:"5",r:"3"}],["circle",{cx:"6",cy:"12",r:"3"}],["circle",{cx:"18",cy:"19",r:"3"}],["line",{x1:"8.59",x2:"15.42",y1:"13.51",y2:"17.49"}],["line",{x1:"15.41",x2:"8.59",y1:"6.51",y2:"10.49"}]]];var sr=["svg",i,[["circle",{cx:"12",cy:"12",r:"10"}],["path",{d:"M8 14s1.5 2 4 2 4-2 4-2"}],["line",{x1:"9",x2:"9.01",y1:"9",y2:"9"}],["line",{x1:"15",x2:"15.01",y1:"9",y2:"9"}]]];var lr=["svg",i,[["path",{d:"M11 17a4 4 0 0 1-8 0V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2Z"}],["path",{d:"M16.7 13H19a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H7"}],["path",{d:"M 7 17h0.01"}],["path",{d:"m11 8 2.3-2.3a2.4 2.4 0 0 1 3.404.004L18.6 7.6a2.4 2.4 0 0 1 .026 3.434L9.9 19.8"}]]];var nr=["svg",i,[["path",{d:"M12 3v18"}],["rect",{width:"18",height:"18",x:"3",y:"3",rx:"2"}],["path",{d:"M3 9h18"}],["path",{d:"M3 15h18"}]]];var ir=["svg",i,[["path",{d:"M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"}],["circle",{cx:"7.5",cy:"7.5",r:".5",fill:"currentColor"}]]];var we=["svg",i,[["circle",{cx:"12",cy:"8",r:"5"}],["path",{d:"M20 21a8 8 0 0 0-16 0"}]]];var cr=["svg",i,[["path",{d:"M18 6 6 18"}],["path",{d:"m6 6 12 12"}]]];var Jr=({icons:s={},nameAttr:r="data-lucide",attrs:a={}}={})=>{if(!Object.values(s).length)throw new Error(`Please provide an icons object.
If you want to use all the icons you can import it like:
 \`import { createIcons, icons } from 'lucide';
lucide.createIcons({icons});\``);if(typeof document>"u")throw new Error("`createIcons()` only works in a browser environment.");let d=document.querySelectorAll(`[${r}]`);if(Array.from(d).forEach(f=>Ye(f,{nameAttr:r,icons:s,attrs:a})),r==="data-lucide"){let f=document.querySelectorAll("[icon-name]");f.length>0&&(console.warn("[Lucide] Some icons were found with the now deprecated icon-name attribute. These will still be replaced for backwards compatibility, but will no longer be supported in v1.0 and you should switch to data-lucide"),Array.from(f).forEach(h=>Ye(h,{nameAttr:"icon-name",icons:s,attrs:a})))}};var ge=s=>{let r=ne(s);return r.classList.add("w-4","h-4"),r},Jt={page:ge(We),datastore:ge(ie),user:ge(we),tag:ge(ir)},dr=class extends HTMLElement{constructor(){super(),this.searchButton=this.querySelector("#search-button"),this.searchModal=this.querySelector("#search-modal"),this.searchInput=this.querySelector("#search-input"),this.searchResultsContainer=this.querySelector("#search-results"),this.noSearchResultsContainer=this.querySelector("#no-search-results"),this.searchIcon=this.querySelector("#search-icon"),this.loadingIcon=this.querySelector("#loading-icon"),this.searchButton.addEventListener("click",()=>{this.#e()}),document.addEventListener("keydown",r=>{if(r.key==="k"&&r.ctrlKey&&(r.preventDefault(),this.searchModal.open||(this.searchInput.value=""),this.#e()),this.searchModal.open&&r.target===this.searchInput&&this.focusIndex!==void 0){let a=0;switch(r.key){case"ArrowUp":a=-1;break;case"ArrowDown":a=1;break;case"Enter":this.#l();break}if(a!==0){r.preventDefault();let d=this.focusableElements.length;this.#t((this.focusIndex+d+a)%d,!0)}}}),this.focusableElements=[],this.searchInput.addEventListener("input",r=>{this.#r(this.searchInput.value)})}#e(){this.searchModal.showModal()}async#r(r){try{this.#a(!0);let a=await this.#o(r);this.#a(!1),this.#s(a)}catch(a){console.log(a)}}async#o(r){this.abortController&&this.abortController.abort(),this.abortController=new AbortController;let a=await fetch("/search/?"+new URLSearchParams({query:r}),{method:"GET",signal:this.abortController.signal});return a.ok?await a.json():{}}#a(r){clearTimeout(this.iconTimeout),this.iconTimeout=setTimeout(()=>{this.loadingIcon.classList.toggle("hidden",!r),this.searchIcon.classList.toggle("hidden",r)},r?0:150)}#s(r){let a=[];for(let f in r){if(r[f].length<=0)continue;let h=document.createElement("div");h.classList.add("menu"),h.innerHTML+=`<li class="opacity-60 pb-2">${f}</li>`,h.innerHTML+=r[f].map(g=>`<li>
                    <a href="${g.url}" class="">
                        ${Jt[g.type]?.outerHTML||""}${Qr.default.sanitize(g.name,{USE_PROFILES:{html:!0}})}
                    </a>
                </li>`).join(""),a.push(h)}let d=a.length>0;this.searchResultsContainer.replaceChildren(...a),this.focusableElements=[...this.searchResultsContainer.querySelectorAll("a")],this.focusableElements.forEach((f,h)=>{f.addEventListener("mouseenter",()=>{this.#t(h,!1)})}),this.searchResultsContainer.classList.toggle("hidden",!d),this.noSearchResultsContainer.classList.toggle("hidden",d),this.#t(d?0:void 0,!0)}#t(r,a){if(this.focusIndex!==void 0&&this.focusableElements[this.focusIndex]?.classList.remove("focus"),this.focusIndex=r,this.focusIndex!==void 0){let d=this.focusableElements[this.focusIndex];d.classList.add("focus"),a&&d.scrollIntoView({block:"center",behavior:"smooth"})}}#l(){if(this.focusIndex!==void 0){let r=this.focusableElements[this.focusIndex];document.location.href=r.href}}};customElements.define("yapity-search",dr);var pr=class extends HTMLElement{constructor(){super(),[...this.querySelectorAll(".alert")].forEach(a=>{let d=()=>setTimeout(()=>a.classList.add("toast-fly-out"),1e4),f=d();a.addEventListener("mouseover",()=>{console.log("mouseover"),clearTimeout(f)}),a.addEventListener("mouseleave",()=>{console.log("mouseleave"),f=d()})})}};customElements.define("yapity-toaster",pr);Jr({icons:{Check:Ge,FolderTree:Ve,Github:Ke,Info:Ze,KeyRound:$e,Laugh:Je,LineChart:ie,LogIn:Qe,Menu:er,Pencil:rr,Redo:tr,Search:or,Share2:ar,Smile:sr,SwatchBook:lr,Table:nr,X:cr}});})();
/*! Bundled license information:

dompurify/dist/purify.js:
  (*! @license DOMPurify 3.0.11 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.0.11/LICENSE *)

lucide/dist/esm/createElement.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/replaceElement.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/defaultAttributes.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/check.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/file-text.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/folder-tree.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/github.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/info.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/key-round.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/laugh.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/line-chart.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/log-in.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/menu.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/pencil.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/redo.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/search.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/share-2.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/smile.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/swatch-book.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/table.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/tag.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/user-round.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/icons/x.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)

lucide/dist/esm/lucide.js:
  (**
   * @license lucide v0.364.0 - ISC
   *
   * This source code is licensed under the ISC license.
   * See the LICENSE file in the root directory of this source tree.
   *)
*/
//# sourceMappingURL=main.js.map
