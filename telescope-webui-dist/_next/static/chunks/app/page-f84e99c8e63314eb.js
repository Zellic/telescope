(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{1942:function(e,n,t){Promise.resolve().then(t.bind(t,1812))},1812:function(e,n,t){"use strict";t.d(n,{default:function(){return z}});var s,l,c=t(7437),a=t(2265),r=t(9386),o=t(8740),i=t(9629),u=t(9139),d=t(964),h=t(3908),x=t(1272),m=t(4794);function g(e){var n,t,s;let l=e.user;return(0,c.jsxs)("div",{className:"flex flex-col",children:[(0,c.jsx)("p",{className:"text-bold text-sm",children:null!==(t=null!==(n=l.username)&&void 0!==n?n:l.name)&&void 0!==t?t:"<no username>"}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:11===(s=l.phone).length?"+".concat(s[0],"-").concat(s.slice(1,4),"-").concat(s.slice(4,7),"-").concat(s.slice(7)):10===s.length?"".concat(s.slice(0,3),"-").concat(s.slice(3,6),"-").concat(s.slice(6)):7===s.length?"".concat(s.slice(0,3),"-").concat(s.slice(3)):s}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:l.email}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:l.comment})]})}let p=[{name:"NAME",uid:"name"},{name:"STATUS",uid:"status"},{name:"AUTHENTICATION",uid:"authentication"},{name:"ACTIONS",uid:"actions"}];function f(e){let n=a.useCallback((n,t)=>{let s="warning";switch("AuthorizationSuccess"===n.status.stage?s="success":"ClientNotStarted"===n.status.stage?s="default":("ConnectionClosed"===n.status.stage||"ErrorOccurred"===n.status.stage||!0===n.status.inputRequired)&&(s="danger"),t){case"name":return(0,c.jsx)("div",{className:"flex",children:(0,c.jsx)("div",{className:"flex flex-col",children:(0,c.jsx)(g,{user:n})})});case"status":return(0,c.jsx)(r.z,{className:"capitalize",color:s,size:"sm",variant:"flat",children:n.status.stage});case"authentication":if(null!==n.status.error)return(0,c.jsx)("p",{children:n.status.error});if("success"===s||!n.status.inputRequired)return null;return(0,c.jsx)(m.A,{isLoading:"warning"===s,onClick:()=>{e.onProvideClicked(n)},children:"Provide"});case"actions":return(0,c.jsx)("div",{className:"relative flex items-center gap-2",children:e.renderActionButtons(n)})}},[]);return(0,c.jsxs)(o.b,{"aria-label":"Example table with custom cells",children:[(0,c.jsx)(i.J,{columns:p,children:e=>(0,c.jsx)(u.j,{align:"actions"===e.uid?"center":"start",children:e.name},e.uid)}),(0,c.jsx)(d.y,{items:e.users,children:e=>(0,c.jsxs)(h.g,{children:[(0,c.jsx)(x.X,{children:n(e,"name")}),(0,c.jsx)(x.X,{children:n(e,"status")}),(0,c.jsx)(x.X,{children:n(e,"authentication")}),(0,c.jsx)(x.X,{children:n(e,"actions")})]},e.phone)})]})}class j{static getInstance(){return j.instance||(j.instance=new j),j.instance}async request(e,n){try{let t=await fetch("".concat(this.baseURL).concat(e),n),s=await t.json();if(!t.ok)return{success:!1,error:s.error||"Unknown error occurred"};return{success:!0,data:s}}catch(e){return{success:!1,error:e instanceof Error?e.message:"Unknown error occurred"}}}async getClients(e){return e?this.request("/clients?hash="+e):this.request("/clients")}async connectClient(e){return this.request("/tgconnect?phone="+e)}async disconnectClient(e){return this.request("/tgdisconnect?phone="+e)}async deleteaccount(e){return this.request("/deleteaccount?phone="+e)}async submitValue(e,n,t){return this.request("/submitvalue",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:e,stage:n,value:t})})}async addAccount(e,n,t){return this.request("/addtgaccount",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone_number:e,email:n,comment:t})})}constructor(){let e=window.location.protocol,n=window.location.hostname,t="https:"===e?"https":"http";if("localhost"===n)this.baseURL="".concat(t,"://localhost:8888");else{let e=window.location.port;""==e?this.baseURL="".concat(t,"://").concat(n):this.baseURL="".concat(t,"://").concat(n,":").concat(e)}}}var v=t(9834),C=t(8941),b=t(9991),y=t(5448),E=t(6801),R=t(1496),A=t(9960),S=t(5256),O=t(1025),w=t(7971),N=t(1094),P=t(5286);let k={PasswordRequired:{name:"PasswordRequired",inputType:"text",label:"Password",placeholder:"Enter the account password",filter_regex:/\s/g,validate:e=>e.length>0?null:"Cannot be empty."},AuthCodeRequired:{name:"AuthCodeRequired",inputType:"text",label:"Auth Code",placeholder:"Enter the Telegram auth code",maxLength:5,filter_regex:/\D/g,validate:e=>/^[0-9]{5}$/.test(e)?null:"Auth code is exactly 5 digits."},EmailCodeRequired:{name:"EmailCodeRequired",inputType:"text",label:"E-mail code",placeholder:"Enter code from email",filter_regex:/\s/g,validate:e=>e.length>0?null:"Must enter an email code."}};function I(e){let{isOpen:n,onOpenChange:t}=(0,E.q)({isOpen:e.isOpen}),s=e.isOpen?k[e.user.status.stage]:null,l=null;return null!==s&&(null==s?void 0:s.validate)!==null&&(l=s.validate(e.value)),(0,c.jsx)(R.R,{isOpen:n,onOpenChange:t,onClose:()=>{e.onClose()},children:(0,c.jsx)(A.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(S.k,{className:"flex flex-col gap-1",children:e.user.status.stage}),e.submitting?(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:"Submitting..."}),(0,c.jsx)(w.R,{children:(0,c.jsx)(b.c,{})})]}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)(O.I,{children:[(0,c.jsx)("p",{children:"Please enter the thingy."}),(0,c.jsx)("div",{children:(0,c.jsx)(P.Y,{isRequired:!0,type:s.inputType,label:s.label,placeholder:s.placeholder,maxLength:null==s?void 0:s.maxLength,isInvalid:null!==l,color:null!==l?"danger":"success",errorMessage:null!=l?l:"",value:e.value,onValueChange:n=>{(null==s?void 0:s.filter_regex)?e.setValue(n.replaceAll(s.filter_regex,"")):e.setValue(n)}})})]}),(0,c.jsxs)(w.R,{children:[(0,c.jsx)(N.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,c.jsx)(N.A,{color:"primary",onPress:()=>{var n;n=e.value,e.onSubmit(n)},children:"Submit"})]})]})]})})})}function T(e){return e&&e.length>0?e:null}function q(e){let{isOpen:n,onOpenChange:t}=(0,E.q)({isOpen:!0}),[s,l]=(0,a.useState)(!1),[r,o]=(0,a.useState)(""),[i,u]=(0,a.useState)(""),[d,h]=(0,a.useState)("");return(0,c.jsx)(R.R,{isOpen:n,isDismissable:!s,onOpenChange:t,onClose:()=>{e.onClose()},children:(0,c.jsx)(A.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(S.k,{className:"flex flex-col gap-1",children:"Add Telegram Account"}),s?(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:"Submitting..."}),(0,c.jsx)(w.R,{children:(0,c.jsx)(b.c,{})})]}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:(0,c.jsxs)("div",{className:"flex flex-col gap-6",children:[(0,c.jsx)(P.Y,{isRequired:!0,type:"text",label:"Phone number",placeholder:"Enter phone number...",labelPlacement:"outside",maxLength:11,pattern:"d{11}",value:r,onValueChange:e=>{o(e)}}),(0,c.jsx)(P.Y,{isRequired:!1,type:"email",label:"E-mail",placeholder:"Enter email...",labelPlacement:"outside",maxLength:255,value:i,onValueChange:e=>{u(e)}}),(0,c.jsx)(P.Y,{isRequired:!1,type:"text",label:"Comment",placeholder:"Account belongs to...",labelPlacement:"outside",maxLength:300,value:d,onValueChange:e=>{h(e)}})]})}),(0,c.jsxs)(w.R,{children:[(0,c.jsx)(N.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,c.jsx)(N.A,{color:"primary",onPress:()=>{l(!0),e.onSubmit({phone:r,email:T(i),comment:T(d)})},children:"Submit"})]})]})]})})})}function L(e){let{isOpen:n,onOpenChange:t}=(0,E.q)({isOpen:e.isOpen});return(0,c.jsx)(R.R,{isOpen:n,onOpenChange:t,onClose:e.onClose,children:(0,c.jsx)(A.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(S.k,{className:"flex flex-col gap-1",children:e.title}),(0,c.jsx)(O.I,{children:(0,c.jsx)("p",{children:e.message})}),(0,c.jsx)(w.R,{children:e.buttons.map(e=>(0,c.jsx)(N.A,{color:e.color,onPress:()=>{e.onPress(e.key)},children:e.label}))})]})})})}let D=[{unit:"year",seconds:31104e3},{unit:"month",seconds:2592e3},{unit:"day",seconds:86400},{unit:"hour",seconds:3600},{unit:"minute",seconds:60},{unit:"second",seconds:1}];var U=t(9726),F=t(6356),_=t(4983),V=t(1810);function M(e){let{isOpen:n,onOpenChange:t}=(0,E.q)({isOpen:e.isOpen}),[s,l]=(0,a.useState)("");return(0,c.jsx)(R.R,{isOpen:n,onOpenChange:t,onClose:e.onClose,children:(0,c.jsx)(A.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(S.k,{className:"flex flex-col gap-1",children:"Remove account"}),(0,c.jsxs)(O.I,{children:[(0,c.jsx)("p",{children:"Really remove this account from Telescope and delete all associated data?"}),(0,c.jsx)("div",{className:"flex items-center ml-6",children:(0,c.jsx)(g,{user:e.user})})]}),(0,c.jsx)(w.R,{children:(0,c.jsxs)("div",{className:"w-full flex flex-col gap-3",children:[(0,c.jsx)("div",{children:(0,c.jsx)(P.Y,{isRequired:!0,type:"text",label:"Confirm",placeholder:"Type DELETE to confirm...",labelPlacement:"outside",maxLength:6,value:s,onValueChange:e=>{l(e.toUpperCase())}})}),(0,c.jsxs)("div",{className:"flex flex-row gap-2",children:[(0,c.jsx)(N.A,{color:"danger",isDisabled:"DELETE"!=s.toUpperCase(),onPress:()=>{l(""),e.onConfirmed(e.user)},children:"Delete User"}),(0,c.jsx)(N.A,{color:"default",onPress:()=>{e.onClose()},children:"Cancel"})]})]})})]})})})}function z(){let[e,n]=(0,a.useState)(null),t=(0,a.useRef)(null),[s,l]=(0,a.useState)(!1),[r,o]=(0,a.useState)(!1),[i,u]=(0,a.useState)(null),[d,h]=(0,a.useState)(!1),[x,g]=(0,a.useState)(""),[p,E]=(0,a.useState)(0),[R,A]=(0,a.useState)(null),[S,O]=(0,a.useState)(null),w=(0,a.useCallback)(async()=>{if(!r){l(!0);try{let e=j.getInstance(),s=await e.getClients(t.current);s.success?(s.data.hash!==t.current&&n(s.data.items),t.current=s.data.hash):console.error("Error fetching from server: ".concat(s.error)),o(!s.success)}catch(e){console.error("Error fetching clients: ",e),o(!0)}finally{l(!1)}}},[r]);if(!function(e,n){let t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];arguments.length>3&&void 0!==arguments[3]&&arguments[3];let s=function(){let e=(0,a.useRef)(!0);return(0,a.useEffect)(()=>{let n=()=>{e.current=!document.hidden};return document.addEventListener("visibilitychange",n),()=>{document.removeEventListener("visibilitychange",n)}},[]),e}();!function(e,n){let t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],s=!(arguments.length>3)||void 0===arguments[3]||arguments[3],l=(0,a.useRef)(),c=(0,a.useRef)(!1),r=(0,a.useRef)(!1);(0,a.useEffect)(()=>{l.current=n},[n]);let o=(0,a.useCallback)(async()=>{if(!c.current){c.current=!0;try{var e;await (null===(e=l.current)||void 0===e?void 0:e.call(l))}finally{c.current=!1,r.current=!0}}},[]);(0,a.useEffect)(()=>{s?o():r.current=!0},[]),(0,a.useEffect)(()=>{if(null!==e){let n=setInterval(()=>{r.current&&o()},e);return()=>clearInterval(n)}},[e,o,...t])}(e,(0,a.useCallback)(async()=>{s.current&&await n()},[n]),t)}(5e3,w,[w]),r)return(0,c.jsx)(v.w,{children:(0,c.jsx)(y.G,{children:"Failed to reach server. Please try again later."})});async function N(e){E(2);let n=await j.getInstance().addAccount(e.phone,e.email,e.comment);n.success||P("Error","Failed to add account: ".concat(n.error)),E(0)}function P(e,n){A({title:e,message:n,onClose:()=>{A(null)},buttons:[{key:"okay",label:"Okay",color:"primary",onPress:()=>{A(null)}}]})}return(0,c.jsxs)(c.Fragment,{children:[0===p?null:(0,c.jsx)(q,{onClose:()=>{E(0)},onSubmit:e=>{N(e)}}),(0,c.jsxs)("div",{className:"flex flex-col gap-4",children:[(0,c.jsx)(M,{isOpen:null!=S,user:S,onClose:()=>{O(null)},onConfirmed:e=>{O(null),async function(){let n=await j.getInstance().deleteaccount(e.phone);n.success||P("Error","Failed to delete account: ".concat(n.error))}()}}),(0,c.jsx)(L,{isOpen:null!=R,...null!==R?R:{title:"",message:"",buttons:[],onClose:()=>{}}}),(0,c.jsx)(I,{submitting:d,isOpen:null!==i,onClose:()=>{u(null)},onSubmit:t=>{g(""),function(t){(async()=>{try{let s=j.getInstance();h(!0);let l=null==i?void 0:i.status.stage,c=await s.submitValue(null==i?void 0:i.phone,null==i?void 0:i.status.stage,t);if(await new Promise(e=>setTimeout(e,2e3)),h(!1),c.success){if(null===e||null===i)return;let t=e.map(e=>e.phone===i.phone&&e.status.stage===l?{...e,status:{...e.status,inputRequired:!1}}:e);n(t)}else console.error("Error submitting code to server: ".concat(c.error)),o(!0)}catch(e){console.error("Error submitting code to server: ",e),o(!0)}u(null)})()}(t)},value:x,setValue:g,user:i}),null===e?(0,c.jsx)(v.w,{children:(0,c.jsx)(y.G,{children:"Waiting for data..."})}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)("div",{className:"flex gap-4 justify-between",children:[(0,c.jsx)("span",{}),(0,c.jsx)(m.A,{size:"sm",onClick:()=>{E(1)},children:"Add Account"})]}),(0,c.jsx)(f,{users:e,onProvideClicked:function(e){u(e)},renderActionButtons:e=>(0,c.jsxs)(V.Pd.Provider,{value:{size:"19px"},children:[(0,c.jsx)(C.e,{content:"Retrieve auth code",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Retrieve auth code",isDisabled:!e.lastCode,onClick:()=>{var n;P("Auth code","As of ".concat((n=e.lastCode.date,function(e){for(let{unit:n,seconds:t}of D)if(e>=t){let s=Math.floor(e/t);return"".concat(s," ").concat(n).concat(1!==s?"s":"")}return"0 seconds"}(Math.floor(Date.now()/1e3)-n))," ago the login code is: ").concat(e.lastCode.value))},children:(0,c.jsx)(_.dgU,{})})}),"ClientNotStarted"===e.status.stage?(0,c.jsx)(C.e,{content:"Connect",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Connect",onClick:()=>{j.getInstance().connectClient(e.phone).then(n=>{n.success?P("Success","Connected account ".concat(e.phone,".")):P("Error","Couldn't connect account ".concat(e.phone,": ").concat(n.error))})},children:(0,c.jsx)(F.y6x,{})})}):(0,c.jsx)(C.e,{content:"Disconnect",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Disconnect",onClick:()=>{A({title:"Disconnect",message:"Really disconnect ".concat(e.phone,"?"),onClose:()=>{A(null)},buttons:[{key:"disconnect",label:"Disconnect",color:"danger",onPress:()=>{A(null),j.getInstance().disconnectClient(e.phone).then(n=>{n.success?P("Success","Disconnected account ".concat(e.phone,".")):P("Error","Couldn't disconnect account ".concat(e.phone,": ").concat(n.error))})}},{key:"cancel",label:"Cancel",color:"default",onPress:()=>{A(null)}}]})},children:(0,c.jsx)(U.ZUl,{className:"font-bold"})})}),(0,c.jsx)(C.e,{content:"Remove account from Telescope",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"danger","aria-label":"Remove account from Telescope",onClick:()=>{O(e)},children:(0,c.jsx)(F.FH3,{})})})]})})]})]}),(0,c.jsx)("div",{children:s&&(0,c.jsx)(b.c,{})})]})}(s=l||(l={}))[s.CLOSED=0]="CLOSED",s[s.OPEN=1]="OPEN",s[s.SUBMITTING=2]="SUBMITTING"}},function(e){e.O(0,[217,821,51,265,798,971,23,744],function(){return e(e.s=1942)}),_N_E=e.O()}]);